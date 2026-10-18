"""energy.py — the functional of BUILD-SPEC §3, analytic gradients (numpy). Implementer: Grace (Claude Opus 5.5)."""
import numpy as np
from scipy.spatial import cKDTree
import constants as K
from mesh import Topo, face_geom, tri_grad

_TOPO={}
def topo(n):
    if n not in _TOPO: _TOPO[n]=Topo(n)
    return _TOPO[n]

class System:
    def __init__(self,species,centres,e0,E0,delta,subdiv=K.SUBDIV,fade=K.FADE,kbend_fac=K.K_BEND_FAC,karea_fac=K.K_AREA_FAC):
        self.T=topo(subdiv); self.sp=list(species); self.C=len(species)
        self.R=np.array([K.RP if s=='p' else K.RN for s in species])
        self.e0,self.E0,self.delta,self.fade=e0,E0,delta,fade
        U=self.T.V; F=self.T.F
        a,b,c,n,nn=face_geom(U,F); self.Af0_unit=0.5*nn          # unit-sphere mesh face areas
        self.V0=4/3*np.pi*self.R**3; self.A0=4*np.pi*self.R**2
        self.Af0=[self.Af0_unit*r*r for r in self.R]
        # rest volume of the *mesh* (not the sphere) so an isolated capsid is exactly at rest
        vm=(a*np.cross(b,c)).sum()/6
        self.V0m=vm*self.R**3; self.A0m=self.Af0_unit.sum()*self.R**2
        self.Karea=karea_fac*E0/self.A0
        self.Kpen=K.K_PEN_FAC*e0/(0.05*K.RP)**2
        self.Kbend=kbend_fac*E0
        # edge->face adjacency for bending
        E={}
        for f,(i,j,k) in enumerate(F):
            for u,v in ((i,j),(j,k),(k,i)): E.setdefault((min(u,v),max(u,v)),[]).append(f)
        self.edges=np.array([v for v in E.values()])
        self.X0=np.array([U*r+np.asarray(c0,float) for r,c0 in zip(self.R,centres)])
        e=np.linalg.norm(U[F[:,0]]-U[F[:,1]],axis=1).mean(); self.edge0=e*self.R
        self.fixed=np.zeros(self.C,bool); self.tether={}; self.Fext={}
        self.mesh_pairs=[(i,j) for i in range(self.C) for j in range(i+1,self.C) if self.sp[i]==self.sp[j]]
    # --- fade function ---
    def s(self,g):
        """fade s(x), x=g/delta. 'linear': 1 / 1-x / 0 rounded C1 by softplus over FADE_EPS (declared numerical regularisation)."""
        x=g/self.delta; e=K.FADE_EPS
        def sp(z):  # softplus and its derivative
            return e*np.logaddexp(0,z/e), 0.5*(1+np.tanh(z/(2*e)))
        if self.fade=='linear':
            a,da=sp(x); b,db=sp(x-1); return 1-a+b,(-da+db)/self.delta
        a,da=sp(x); b,db=sp(x-1); u=1-a+b; return u*u,2*u*(-da+db)/self.delta
    def gaps(self,X,i,j,cache=None):
        """signed gaps of candidate vertices of capsid i to capsid j: Gaussian-weighted blend of the signed plane distances
        to the K_NEAR nearest faces of j (h = GAP_H * rest mean edge). Continuous replacement for the spec's nearest-plane gap.
        returns idx, f (m,k), g (m,), and pieces for the gradient."""
        F=self.T.F; Xj=X[j]; cj=Xj.mean(0); rj=np.linalg.norm(Xj-cj,axis=1).max()
        dv=np.linalg.norm(X[i]-cj,axis=1); idx=np.nonzero(dv<rj+self.delta*(1+10*K.FADE_EPS)+K.GAP_MARGIN)[0]
        if len(idx)==0: return idx,None,None,None
        if cache is not None and j in cache: a,b,c,n,nn,cen,tree=cache[j]
        else:
            a,b,c,n,nn=face_geom(Xj,F); cen=(a+b+c)/3; tree=cKDTree(cen)
            if cache is not None: cache[j]=(a,b,c,n,nn,cen,tree)
        _,f=tree.query(X[i][idx],k=K.K_NEAR)
        xv=X[i][idx][:,None,:]; nh=n[f]/nn[f][...,None]; w=xv-cen[f]; gk=(nh*w).sum(-1)
        h=K.GAP_H*self.edge0[j]; rho2=(w*w).sum(-1)
        Wk=np.exp(-(rho2-rho2.min(1,keepdims=True))/h**2); Z=Wk.sum(1,keepdims=True); pk=Wk/Z
        gpl=(pk*gk).sum(1)
        rho=np.sqrt(rho2[:,0]); gfar=rho-self.edge0[j]           # Euclidean floor: nearest-centroid distance - 1 rest edge
        far=gfar>gpl; g=np.where(far,gfar,gpl)
        return idx,f,g,dict(nh=nh,w=w,gk=gk,pk=pk,h=h,nn=nn[f],a=a,b=b,c=c,far=far,rho=rho)
    def energy(self,x,parts=False):
        X=x.reshape(self.C,self.T.nv,3); F=self.T.F; G=np.zeros_like(X)
        Ein=Ear=Ebe=Ead=Epe=Eco=Eext=Ete=0.0
        geo=[face_geom(X[i],F) for i in range(self.C)]
        Av=[]
        for i in range(self.C):
            a,b,c,n,nn=geo[i]; Af=0.5*nn; Av.append(self.T.S@np.tile(Af,3)/3)
        W=[np.zeros(self.T.nv) for _ in range(self.C)]
        cache={j:(*geo[j],(geo[j][0]+geo[j][1]+geo[j][2])/3,cKDTree((geo[j][0]+geo[j][1]+geo[j][2])/3)) for j in range(self.C)}
        Gacc=[np.zeros((self.T.nv,3)) for _ in range(self.C)]
        adj_list=[]
        for i in range(self.C):
            for j in range(self.C):
                if i==j: continue
                idx,f,g,P=self.gaps(X,i,j,cache)
                if len(idx)==0: continue
                s,ds=self.s(g); pen=np.maximum(0,-g)
                wv=-self.e0*s+self.Kpen*pen**2; dw=-self.e0*ds-2*self.Kpen*pen
                W[i][idx]+=wv
                Ead+=(-self.e0*s*Av[i][idx]).sum(); Epe+=(self.Kpen*pen**2*Av[i][idx]).sum()
                coef=Av[i][idx]*dw                                   # dE/dg  (m,)
                nh,w,gk,pk,h=P['nh'],P['w'],P['gk'],P['pk'],P['h']; far=P['far']; near=~far
                cf=np.where(near,coef,0.0); cr=np.where(far,coef,0.0)
                wbar=(pk[...,None]*w).sum(1)
                dpk_dx=pk[...,None]*(-2*(w-wbar[:,None,:])/h**2)
                dg_dx=(pk[...,None]*nh).sum(1)+((gk-g[:,None])[...,None]*dpk_dx).sum(1)
                u0=w[:,0,:]/np.maximum(P['rho'],1e-12)[:,None]
                G[i][idx]+=cf[:,None]*dg_dx+cr[:,None]*u0
                ck=(cf[:,None]*pk)
                q=(w-nh*gk[...,None])/P['nn'][...,None]*ck[...,None]
                A_,B_,C_=P['a'][f],P['b'][f],P['c'][f]
                ga,gb,gc=tri_grad(A_,B_,C_,q)
                dcen=-ck[...,None]*nh + (cf[:,None]*pk*(gk-g[:,None]))[...,None]*2*w/h**2
                dcen[:,0,:]+=-cr[:,None]*u0
                m=dcen/3
                nvj=self.T.nv
                for corner,gg in ((0,ga),(1,gb),(2,gc)):
                    ids=F[f,corner].ravel(); vals=(gg+m).reshape(-1,3)
                    for ax in range(3): Gacc[j][:,ax]+=np.bincount(ids,vals[:,ax],minlength=nvj)
        for j in range(self.C): G[j]+=Gacc[j]
        for i in range(self.C):
            a,b,c,n,nn=geo[i]; Af=0.5*nn; nh=n/nn[:,None]
            V=(a*np.cross(b,c)).sum()/6; V0=self.V0m[i]
            Ein+=self.E0*(V0/V-1); dEdV=-self.E0*V0/V**2
            gV=self.T.scatter(np.cross(b,c),np.cross(c,a),np.cross(a,b))/6*dEdV
            A0f=self.Af0[i]; Ear+=self.Karea[i]*((Af-A0f)**2/A0f).sum()
            cA=2*self.Karea[i]*(Af-A0f)/A0f + W[i][F].mean(1)
            ga,gb,gc=tri_grad(a,b,c,(0.5*cA)[:,None]*nh)
            G[i]+=gV+self.T.scatter(ga,gb,gc)
            if self.Kbend>0:
                f1,f2=self.edges[:,0],self.edges[:,1]; d=(nh[f1]*nh[f2]).sum(1)
                Ebe+=self.Kbend*(1-d).sum()
                q1=-self.Kbend*(nh[f2]-nh[f1]*d[:,None])/nn[f1][:,None]
                q2=-self.Kbend*(nh[f1]-nh[f2]*d[:,None])/nn[f2][:,None]
                Q=np.zeros((len(F),3)); np.add.at(Q,f1,q1); np.add.at(Q,f2,q2)
                ga,gb,gc=tri_grad(a,b,c,Q); G[i]+=self.T.scatter(ga,gb,gc)
        cen=X.mean(1); nv=self.T.nv
        for i in range(self.C):
            for j in range(i+1,self.C):
                if self.sp[i]=='p' and self.sp[j]=='p':
                    r=cen[i]-cen[j]; d=np.linalg.norm(r); Eco+=K.AHC/d
                    gc_=-K.AHC*r/d**3; G[i]+=gc_/nv; G[j]-=gc_/nv
        for i,Fv in self.Fext.items():
            Eext+=-(np.asarray(Fv)*cen[i]).sum(); G[i]-=np.asarray(Fv)/nv
        for i,c0 in self.tether.items():
            r=cen[i]-c0; Ete+=0.5*K.TETHER_K*(r*r).sum(); G[i]+=K.TETHER_K*r/nv
        G[self.fixed]=0
        E=Ein+Ear+Ebe+Ead+Epe+Eco+Eext+Ete
        if parts:
            return E,G.ravel(),dict(inflate=Ein,area=Ear,bend=Ebe,adh=Ead,pen=Epe,coul=Eco,ext=Eext,tether=Ete,
                                    cont=Ein+Ear+Ebe+Ead+Epe+Eco)
        return E,G.ravel()
    def contacts(self,x):
        X=x.reshape(self.C,self.T.nv,3); out=set()
        for i in range(self.C):
            for j in range(self.C):
                if i==j: continue
                idx,f,g,_=self.gaps(X,i,j)
                if len(idx) and (g<0.5*self.delta).any(): out.add((min(i,j),max(i,j)))
        return sorted(out)
    def binding(self,x):
        """BE = -(continuous contact energy + mesh + slingshot) (BUILD-SPEC §3.6, §3.8). Mesh/sling are piecewise constants, applied post-relaxation."""
        E,_,p=self.energy(x,True); con=self.contacts(x)
        p['cont']-=sum(self.ref_energy(s) for s in self.sp)   # zero = relaxed isolated capsids (spec defect fix, see report 'added')
        nmesh=sum(1 for pr in con if pr in self.mesh_pairs)
        # connected?
        par=list(range(self.C))
        def fd(a):
            while par[a]!=a: a=par[a]
            return a
        for i,j in con: par[fd(i)]=fd(j)
        connected=len({fd(i) for i in range(self.C)})==1
        Esl=-self.C*K.Y(self.C) if connected else 0.0
        Emesh=nmesh*E_MESH()
        return -(p['cont']+Emesh+Esl),dict(p,mesh=Emesh,sling=Esl,contacts=con,connected=connected)

_REF={}
def _ref(self,s):
    key=(s,id(self.T),self.e0,self.E0,self.delta,self.fade,self.Kbend,self.Karea[0])
    if key not in _REF:
        from relax import relax
        one=System([s],[[0,0,0]],self.e0,self.E0,self.delta,subdiv=[k for k,v in _TOPO.items() if v is self.T][0],
                   fade=self.fade,kbend_fac=self.Kbend/self.E0,karea_fac=self.Karea[0]*self.A0[0]/self.E0)
        x,_=relax(one); _REF[key]=one.energy(x,True)[2]['cont']
    return _REF[key]
System.ref_energy=_ref

def E_MESH():
    """BUILD-SPEC §4.2 closed form: E_patch(D) - E_SINGLET."""
    return (K.BE_D-2*K.Y(2))-K.E_SINGLET
