"""energy.py — the functional of BUILD-SPEC v2 (§1 fixes F1,F2,F4; §3 rim-recovery term), analytic gradients (numpy).
v1: Grace (Claude Opus 5.5), 18 Oct 2026.  v2 changes: Grace (Claude Fable 5.1), 18 Oct 2026 evening.  v1 kept as energy_v1.py."""
import numpy as np
from scipy.spatial import cKDTree
import constants as K
from mesh import Topo, face_geom, tri_grad

_TOPO={}
def topo(n):
    if n not in _TOPO: _TOPO[n]=Topo(n)
    return _TOPO[n]

class System:
    def __init__(self,species,centres,e0,E0,delta,subdiv=K.SUBDIV,fade=K.FADE,kbend_fac=K.K_BEND_FAC,karea_fac=K.K_AREA_FAC,E1=0.0,singlet_np=False,lam=0.0,lane_mode='triplet',lane_form='linear'):
        self.T=topo(subdiv); self.sp=list(species); self.C=len(species)
        self.R=np.array([K.RP if s=='p' else K.RN for s in species])
        self.e0,self.E0,self.delta,self.fade=e0,E0,delta,fade
        self.E1=E1; self.singlet_np=singlet_np   # v2 §3 cooperative constant; F4 singlet flag
        self.lam=lam; self.lane_mode=lane_mode; self.lane_form=lane_form   # v3: lane/graph cooperativity f_ij = 1 + lam*phi(c_ij)
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
        # v2 F7: bending measured from the REST dihedral (the icosphere's own curvature costs nothing): E_bend = K sum (1 - cos(theta - theta0))
        _a,_b,_c,_n,_nn=face_geom(U,F); _nh=_n/_nn[:,None]; d0=(_nh[self.edges[:,0]]*_nh[self.edges[:,1]]).sum(1)
        self.cos0=np.clip(d0,-1,1); self.sin0=np.sqrt(1-self.cos0**2)
        self.X0=np.array([U*r+np.asarray(c0,float) for r,c0 in zip(self.R,centres)])
        e=np.linalg.norm(U[F[:,0]]-U[F[:,1]],axis=1).mean(); self.edge0=e*self.R
        self.fixed=np.zeros(self.C,bool); self.tether={}; self.Fext={}
        self.mesh_pairs=[(i,j) for i in range(self.C) for j in range(i+1,self.C) if self.sp[i]==self.sp[j] or singlet_np]
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
        rhok=np.sqrt(np.maximum(rho2,1e-24)); uk=w/rhok[...,None]              # distances and unit vectors to the K centroids
        rhos=(pk*rhok).sum(1); gfar=rhos-self.edge0[j]                             # SMOOTH floor (v4): blended centroid distance - 1 rest edge
        eps=K.SMAX_EPS*self.delta; D=np.sqrt((gpl-gfar)**2+eps*eps)
        g=0.5*(gpl+gfar+D); apl=0.5*(1+(gpl-gfar)/D); afar=1-apl                   # smooth max weights
        return idx,f,g,dict(nh=nh,w=w,gk=gk,pk=pk,h=h,nn=nn[f],a=a,b=b,c=c,rhok=rhok,uk=uk,gpl=gpl,gfar=gfar,apl=apl,afar=afar,rho=rhok[:,0])
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
        # ---- pass 1: gaps and fade for every ordered pair (v2) ----
        PR={}
        for i in range(self.C):
            for j in range(self.C):
                if i==j: continue
                idx,f,g,P=self.gaps(X,i,j,cache)
                if len(idx)==0: continue
                s,ds=self.s(g); PR[(i,j)]=(idx,f,g,P,s,ds)
        # ---- v4 (A1 fix): CONTINUOUS contact graph. w_ij = tanh(2 W_ij / A_REF), W_ij = raw weighted patch area (both skins);
        #      f_ij = 1 + lam * T_ij * sum_k w_ik w_jk  (T_ij = 1 for triplet pairs; or all).  Exact gradient through w.
        Wraw={}
        for (i,j),(idx,f,g,P,s,ds) in PR.items():
            key=(min(i,j),max(i,j)); Wraw[key]=Wraw.get(key,0.0)+(Av[i][idx]*s).sum()
        xw={k:2*v/K.A_REF for k,v in Wraw.items()}
        wgt={k:np.tanh(x) for k,x in xw.items()}; dwgt={k:(1-np.tanh(x)**2)*2/K.A_REF for k,x in xw.items()}
        def W_(a,b): return wgt.get((min(a,b),max(a,b)),0.0)
        Graw={k:0.0 for k in Wraw}
        for (i,j),(idx,f,g,P,s,ds) in PR.items():
            key=(min(i,j),max(i,j)); Graw[key]+=-self.e0*(Av[i][idx]*s).sum()
        pairs=list(Wraw)
        def factors(wv):
            """lane factors from a dict of contact weights. forms: linear 1+lam c; sat 1+lam min(c,2)/2; cap3 = sat x capacity min(1,3/z_i,3/z_j)."""
            Wf=lambda a,b: wv.get((min(a,b),max(a,b)),0.0)
            z=[sum(Wf(i,k) for k in range(self.C) if k!=i) for i in range(self.C)]
            F={}
            for (i,j) in pairs:
                trip=((i,j) not in self.mesh_pairs); T_=1.0 if (self.lane_mode=='all' or trip) else 0.0
                c=sum(Wf(i,k)*Wf(j,k) for k in range(self.C) if k not in (i,j))
                if self.lane_form=='linear': phi=c
                else: phi=min(c,2.0)/2.0 if c<2.0 else 1.0
                if self.lane_form=='cap3': phi*=min(1.0,K.Z_CAP/max(z[i],1e-9),K.Z_CAP/max(z[j],1e-9))
                F[(i,j)]=1.0+self.lam*T_*phi
            return F
        self._fac=factors(wgt)
        # Lam_ab = dE_lane/dw_ab = sum_ij G_ij dF_ij/dw_ab   (central differences on the tiny w-vector; exact to O(h^2))
        Lam={}
        for ab in pairs:
            wp=dict(wgt); wm=dict(wgt); hh=1e-5; wp[ab]+=hh; wm[ab]-=hh; Fp=factors(wp); Fm=factors(wm)
            Lam[ab]=sum(Graw[ij]*(Fp[ij]-Fm[ij])/(2*hh) for ij in pairs)
        self._Lam=Lam; self._dw=dwgt
        # ---- per-vertex sums for the cooperative term: S_v = sum_j s_j(v) ----
        Ssum=[np.zeros(self.T.nv) for _ in range(self.C)]; Ssq=[np.zeros(self.T.nv) for _ in range(self.C)]
        for (i,j),(idx,f,g,P,s,ds) in PR.items():
            Ssum[i][idx]+=s; Ssq[i][idx]+=s*s
        Ecp=0.0
        for i in range(self.C):
            coop=0.5*(Ssum[i]**2-Ssq[i])          # sum_{j<k} s_j s_k
            W[i]+=-self.E1*coop; Ecp+=(-self.E1*coop*Av[i]).sum()
        # ---- pass 2: energies and gradients ----
        for (i,j),(idx,f,g,P,s,ds) in PR.items():
                pen=np.maximum(0,-g); key=(min(i,j),max(i,j)); fij=self._fac.get(key,1.0)
                lamw=self._Lam.get(key,0.0)*self._dw.get(key,0.0)          # dE/dW_ij  (through the lane factors of neighbouring pairs)
                wv=-fij*self.e0*s+lamw*s+self.Kpen*pen**2; dw=-fij*self.e0*ds+lamw*ds-2*self.Kpen*pen
                dw=dw-self.E1*(Ssum[i][idx]-s)*ds          # d/dg of the coop density: -E1 (S - s_j) ds_j
                W[i][idx]+=wv
                Ead+=(-fij*self.e0*s*Av[i][idx]).sum(); Epe+=(self.Kpen*pen**2*Av[i][idx]).sum()
                coef=Av[i][idx]*dw                                   # dE/dg  (m,)
                nh,w,gk,pk,h=P['nh'],P['w'],P['gk'],P['pk'],P['h']; rhok,uk,gpl,gfar,apl,afar=P['rhok'],P['uk'],P['gpl'],P['gfar'],P['apl'],P['afar']
                cpl=coef*apl; cfr=coef*afar                                        # dE/dgpl, dE/dgfar
                wbar=(pk[...,None]*w).sum(1); dpk_dx=pk[...,None]*(-2*(w-wbar[:,None,:])/h**2)
                dgpl_dx=(pk[...,None]*nh).sum(1)+((gk-gpl[:,None])[...,None]*dpk_dx).sum(1)
                dgfar_dx=(pk[...,None]*uk).sum(1)+((rhok-rhos_(gfar,self.edge0[j])[:,None])[...,None]*dpk_dx).sum(1)
                G[i][idx]+=cpl[:,None]*dgpl_dx+cfr[:,None]*dgfar_dx
                ck=(cpl[:,None]*pk)
                q=(w-nh*gk[...,None])/P['nn'][...,None]*ck[...,None]
                A_,B_,C_=P['a'][f],P['b'][f],P['c'][f]
                ga,gb,gc=tri_grad(A_,B_,C_,q)
                dcen=-ck[...,None]*nh + (cpl[:,None]*pk*(gk-gpl[:,None]))[...,None]*2*w/h**2 \
                     -(cfr[:,None]*pk)[...,None]*uk + (cfr[:,None]*pk*(rhok-rhos_(gfar,self.edge0[j])[:,None]))[...,None]*2*w/h**2
                m=dcen/3
                nvj=self.T.nv
                for corner,gg in ((0,ga),(1,gb),(2,gc)):
                    ids=F[f,corner].ravel(); vals=(gg+m).reshape(-1,3)
                    for ax in range(3): Gacc[j][:,ax]+=np.bincount(ids,vals[:,ax],minlength=nvj)
        for j in range(self.C): G[j]+=Gacc[j]
        for i in range(self.C):
            a,b,c,n,nn=geo[i]; Af=0.5*nn; nh=n/nn[:,None]
            V=(a*np.cross(b,c)).sum()/6; V0=self.V0m[i]
            Ein+=self.E0*(V0/V+V/V0-2); dEdV=self.E0*(-V0/V**2+1/V0)      # v2 F1: stationary at V0
            gV=self.T.scatter(np.cross(b,c),np.cross(c,a),np.cross(a,b))/6*dEdV
            A0f=self.Af0[i]; Ear+=self.Karea[i]*((Af-A0f)**2/A0f).sum()
            cA=2*self.Karea[i]*(Af-A0f)/A0f + W[i][F].mean(1)
            ga,gb,gc=tri_grad(a,b,c,(0.5*cA)[:,None]*nh)
            G[i]+=gV+self.T.scatter(ga,gb,gc)
            if self.Kbend>0:
                f1,f2=self.edges[:,0],self.edges[:,1]; d=np.clip((nh[f1]*nh[f2]).sum(1),-1,1); sd=np.sqrt(np.maximum(1-d*d,1e-12))
                Ebe+=self.Kbend*(1-d*self.cos0-sd*self.sin0).sum()
                fac=self.Kbend*(-self.cos0+d*self.sin0/sd)                    # dE/dd per edge
                q1=fac[:,None]*(nh[f2]-nh[f1]*d[:,None])/nn[f1][:,None]
                q2=fac[:,None]*(nh[f1]-nh[f2]*d[:,None])/nn[f2][:,None]
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
        E=Ein+Ear+Ebe+Ead+Epe+Ecp+Eco+Eext+Ete
        if parts:
            return E,G.ravel(),dict(inflate=Ein,area=Ear,bend=Ebe,adh=Ead,pen=Epe,coop=Ecp,coul=Eco,ext=Eext,tether=Ete,
                                    cont=Ein+Ear+Ebe+Ead+Epe+Ecp+Eco)
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
        # v2 F4 (ruling): a singlet pair fuses no lane. Slingshot = -A*Y(SLING_N) iff connected AND every capsid has >=1 triplet contact.
        trip=[any(((a,b) not in self.mesh_pairs) for (a,b) in con if i in (a,b)) for i in range(self.C)]
        Esl=-self.C*K.Y(K.SLING_N) if (connected and all(trip)) else 0.0
        Emesh=nmesh*E_MESH()
        return -(p['cont']+Emesh+Esl),dict(p,mesh=Emesh,sling=Esl,contacts=con,connected=connected,all_triplet=all(trip),lane_factors={f'{a}{b}':v for (a,b),v in self._fac.items()})

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

def rhos_(gfar,e0): return gfar+e0

def E_MESH():
    """BUILD-SPEC §4.2 closed form: E_patch(D) - E_SINGLET."""
    return (K.BE_D-2*K.Y(2))-K.E_SINGLET
