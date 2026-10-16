#!/usr/bin/env python3
"""
soft_capsid_relax2.py — second build: ANISOTROPIC capsids (Grace, 16 Oct 2026).
Same posits P1-P5 as soft_capsid_relax.py, plus: each capsid is an ellipsoid with semi-axes (a,b,c) and free
orientation, constrained to the fixed skin area A0 (Knud Thomsen p=1.6075).  Shape costs nothing by itself;
it costs through the interior volume (4/3 pi abc < sphere volume at equal area) via E_inflate.  Directional
radius along a bond R(n) = (n^T S^-2 n)^(-1/2); transverse mean radius R_perp = sqrt(abc/R_par).
This is the 'bulge escape' test: can a z=1 capsid go oblate to keep its patch small while z=3 capsids are
locked flat?  Variables per nucleon: position (3), log(b/a), log(c/a), rotation vector (3) = 8.
"""
import math, sys, itertools, numpy as np
from scipy.optimize import minimize
from scipy.spatial.transform import Rotation
HC=197.3269804; AHC=1.439964547; ME=0.510998950; DM=1.2933323
RP=0.8409; RN=1.023*RP; GAMMA_V=1.0; PTH=1.6075
G=DM/ME; CP=math.sqrt(1-1/G**2)
def Y(n): return ME*(G-1/math.sqrt(1-(CP/n)**2))
BE={'D':2.224566,'T':8.481795,'He3':7.718043,'He4':28.29566,'Be8':56.4995,'C12':92.1617,'O16':127.6193}
def thomsen(a,b,c): return 4*math.pi*(((a*b)**PTH+(a*c)**PTH+(b*c)**PTH)/3)**(1/PTH)
class Nucleus:
    def __init__(s,name,species,x0):
        s.name=name; s.sp=np.array(species); s.A=len(species); s.Z=int((s.sp=='p').sum())
        s.R=np.where(s.sp=='p',RP,RN); s.A0=4*math.pi*s.R**2; s.V0=4/3*math.pi*s.R**3; s.x0=np.array(x0,float)
def unpack(x,nuc):
    A=nuc.A; v=x.reshape(A,8); r=v[:,:3]; lb=v[:,3]; lc=v[:,4]; rot=v[:,5:8]
    axes=[]; mats=[]
    for i in range(A):
        b_a=math.exp(lb[i]); c_a=math.exp(lc[i])
        # a from area constraint: thomsen(a, a*b_a, a*c_a) = A0  -> scales as a^2
        a=math.sqrt(nuc.A0[i]/thomsen(1,b_a,c_a))
        axes.append((a,a*b_a,a*c_a)); mats.append(Rotation.from_rotvec(rot[i]).as_matrix())
    return r,np.array(axes),mats
def energy(x,nuc,P,E0,parts=False):
    r,axes,mats=unpack(x,nuc); A=nuc.A
    Sinv2=[M@np.diag(1/ax**2)@M.T for M,ax in zip(mats,axes)]
    Vell=4/3*math.pi*axes.prod(axis=1)
    d=np.linalg.norm(r[:,None,:]-r[None,:,:],axis=2)+np.eye(A)
    nhat=(r[None,:,:]-r[:,None,:])/d[:,:,None]
    Rpar=np.zeros((A,A)); 
    for i in range(A):
        for j in range(A):
            if i!=j: Rpar[i,j]=(nhat[i,j]@Sinv2[i]@nhat[i,j])**-0.5
    Rperp=np.sqrt(np.maximum(axes.prod(axis=1)[:,None]/np.maximum(Rpar,1e-6),1e-9))
    delta=np.maximum(0.0,Rpar+Rpar.T-d); np.fill_diagonal(delta,0)
    h=delta/2; Pi=np.ones(A); V=Vell.copy()
    for _ in range(3):
        dV=(math.pi*Rperp**2*Rpar*(h/np.maximum(Rpar,1e-9))**2*(3-h/np.maximum(Rpar,1e-9))/3)
        dV=np.where(delta>0,dV,0).sum(axis=1)
        dA=(math.pi*Rperp**2*(h/np.maximum(Rpar,1e-9))**2); dA=np.where(delta>0,dA,0).sum(axis=1)
        scale=(1+dA/nuc.A0)**1.5   # restore skin area: linear dims grow by sqrt(1+dA/A0)
        V=Vell*scale-dV
        Vr=np.maximum(V/nuc.V0,0.05)
        Pi=GAMMA_V*E0*Vr**(-GAMMA_V-1)/nuc.V0
        w=Pi[None,:]/(Pi[:,None]+Pi[None,:]); h=delta*w
    Aij=math.pi*Rperp**2*(2*h/np.maximum(Rpar,1e-9)-(h/np.maximum(Rpar,1e-9))**2); Aij=np.where(delta>0,Aij,0)
    Ap=0.5*(Aij+Aij.T); iu=np.triu_indices(A,1)
    E_adh=-P*Ap[iu].sum(); E_inf=(E0*(Vr**(-GAMMA_V)-1)).sum()
    pr=np.where(nuc.sp=='p')[0]; E_C=sum(AHC/d[i,j] for i,j in itertools.combinations(pr,2)) if len(pr)>1 else 0.0
    E_sl=-A*Y(A) if A>1 else 0.0
    E=E_adh+E_inf+E_C+E_sl
    if parts: return E,dict(adh=E_adh,inf=E_inf,coul=E_C,sling=E_sl,patch=Ap[iu].sum(),Vr=Vr,axes=axes,ncontact=int((delta[iu]>0).sum()))
    return E
def relax(nuc,P,E0,restarts=3,seed=0):
    rng=np.random.default_rng(seed); best=None
    for k in range(restarts):
        x0=np.zeros((nuc.A,8)); x0[:,:3]=nuc.x0
        if k: x0[:,:3]+=rng.normal(0,0.1,(nuc.A,3)); x0[:,3:5]=rng.normal(0,0.05,(nuc.A,2))
        res=minimize(energy,x0.ravel(),args=(nuc,P,E0),method='L-BFGS-B',options={'maxiter':4000,'ftol':1e-12,'gtol':1e-8})
        if best is None or res.fun<best.fun: best=res
    E,p=energy(best.x,nuc,P,E0,True); return -E,p
def tetra(a=1.0): return [[0,0,0],[a,a,0],[a,0,a],[0,a,a]]
NUC={'D':Nucleus('D',['p','n'],[[0,0,0],[1.4,0,0]]),
     'T':Nucleus('T',['p','n','n'],[[0,0,0],[1.4,0,0],[0.7,1.2,0]]),
     'He3':Nucleus('He3',['p','p','n'],[[0,0,0],[1.4,0,0],[0.7,1.2,0]]),
     'He4':Nucleus('He4',['p','p','n','n'],tetra())}
def two_alpha(sep=2.4):
    t=np.array(tetra()); c=t.mean(axis=0); return np.vstack([t-c,t-c+[sep,0,0]]).tolist()
NUC['Be8']=Nucleus('Be8',['p','p','n','n']*2,two_alpha())
def calibrate():
    def miss(v):
        P,E0=v
        if P<=0 or E0<=0: return 1e6
        a=relax(NUC['D'],P,E0,1)[0]-BE['D']; b=relax(NUC['He4'],P,E0,1)[0]-BE['He4']; return a*a+b*b
    best=None
    for P in [4,8,16,32]:
        for E0 in [50,150,400,1000]:
            m=miss((P,E0)); 
            if best is None or m<best[0]: best=(m,P,E0)
    res=minimize(miss,[best[1],best[2]],method='Nelder-Mead',options={'xatol':1e-3,'fatol':1e-6,'maxiter':150}); return res.x
if __name__=='__main__':
    P,E0=(float(sys.argv[1]),float(sys.argv[2])) if len(sys.argv)>2 else calibrate()
    print(f"P_adh={P:.4f} MeV/fm^2  E0={E0:.3f} MeV  gamma_V={GAMMA_V}")
    print(f"{'nuc':5s} {'pred':>8s} {'meas':>8s} {'miss%':>7s}  adh    inflate coul  sling  patch  contacts  V/V0        axes (a,b,c) of nucleon 0")
    for n in ['D','T','He3','He4','Be8']:
        be,p=relax(NUC[n],P,E0)
        print(f"{n:5s} {be:8.3f} {BE[n]:8.3f} {100*(be/BE[n]-1):7.2f} {p['adh']:7.2f} {p['inf']:7.2f} {p['coul']:5.2f} {p['sling']:6.2f} {p['patch']:6.3f}  {p['ncontact']:3d}   {p['Vr'].min():.3f}-{p['Vr'].max():.3f}  {np.round(p['axes'][0],3)}")
