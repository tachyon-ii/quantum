#!/usr/bin/env python3
"""
soft_capsid_relax.py — the trash compactor, first build (Grace, 16 Oct 2026).

Posits declared before any number (the-fractal-nucleus.md §6a; review/deepmind-2026-10-16/ARGON-soft-capsid):
  P1  each nucleon is an inflated capsid with a bendable, (nearly) inextensible skin of area A0 = 4 pi R^2,
      R_p = 0.8409 fm, R_n = 1.023 R_p.  Faceting at fixed skin area squeezes the interior volume.
  P2  the interior holds the carrier/governor circulation energy; its cost of compression is
      E_inflate(V) = E0 * [ (V_sphere/V)^gamma_V - 1 ],   gamma_V = 1 (3-D cavity law; 1/3 = loop law is the alternative).
  P3  a flat contact patch between two capsids is worth  -P_adh * A_patch  (adhesion per unit area; no rim barrier —
      thermal (n,gamma) capture is barrierless, so kappa_rim = 0).
  P4  Coulomb: full pairwise alpha*hbar*c / r_ij between proton centres.
  P5  slingshot: A * Y(n) with n = A (lane length = number of capsids), Y from three-term-binding §7a, c' = 0.91864.
Geometry (first build, isotropic): a pair with centre distance d < R_i + R_j forms a flat facet; the overlap
  delta = R_i + R_j - d is split into indentations h_i, h_j inversely to the capsids' current internal pressures.
  Facet area  A_ij = pi (2 R h - h^2)   (exact spherical cap base).   Cap volume removed  dV = pi h^2 (3R - h)/3.
  Skin area conserved: each facet removes a cap (2 pi R h) and adds a disk, net -pi h^2; the capsid radius grows
  by dR/R = sum_j h_j^2 / (8 R^2) to restore A0 (NOT 1/4 — Argon's stated factor is a slip; his boxed V-formula
  is consistent with 1/8).   V_i = 4/3 pi (R+dR)^3 - sum_j dV_ij.
Calibration: P_adh and E0 solved simultaneously on D (2.224566) and He-4 (28.29566); everything else untouched.
Output: first numbers, no re-tuning.  Everything here is [CONSTRUCT] until it lands.
"""
import math, sys, itertools
import numpy as np
from scipy.optimize import minimize, fsolve

HC=197.3269804; AHC=1.439964547; ME=0.510998950; DM=1.2933323
RP=0.8409; RN=1.023*RP
GAMMA_V=1.0
G=DM/ME; CP=math.sqrt(1-1/G**2)
def Y(n): return ME*(G-1/math.sqrt(1-(CP/n)**2))

BE={'D':2.224566,'T':8.481795,'He3':7.718043,'He4':28.29566,'Be8':56.4995,'C12':92.1617,'O16':127.6193,
    'Li7':39.2446,'Be7':37.6004,'Li6':31.9941}

class Nucleus:
    def __init__(self,name,species,x0):
        self.name=name; self.sp=np.array(species); self.A=len(species); self.Z=int((self.sp=='p').sum())
        self.R=np.where(self.sp=='p',RP,RN); self.x0=np.array(x0,float)
        self.V0=4/3*math.pi*self.R**3

def energy(x,nuc,P,E0,return_parts=False):
    r=x.reshape(-1,3); A=nuc.A; R=nuc.R
    # pass 1: equal split to get pressures; pass 2: pressure-weighted split
    d=np.linalg.norm(r[:,None,:]-r[None,:,:],axis=2)
    iu=np.triu_indices(A,1)
    delta=np.maximum(0.0, R[:,None]+R[None,:]-d); np.fill_diagonal(delta,0)
    h=delta/2.0
    Pi=np.ones(A)
    for _ in range(3):
        hi=h.copy()
        # geometry per capsid
        dR=(hi**2).sum(axis=1)/(8*R**2)*R
        Rg=R+dR
        dV=(math.pi*hi**2*(3*R[:,None]-hi)/3).sum(axis=1)
        V=4/3*math.pi*Rg**3-dV
        Vr=np.maximum(V/nuc.V0,0.05)
        Pi=GAMMA_V*E0*Vr**(-GAMMA_V-1)/nuc.V0   # internal pressure
        # pressure-weighted split: h_ij = Pi_j/(Pi_i+Pi_j) * delta
        w=Pi[None,:]/(Pi[:,None]+Pi[None,:])
        h=delta*w
    Aij=math.pi*(2*R[:,None]*h-h**2); Aij=np.where(delta>0,Aij,0.0)
    # shared facet: use the mean of the two caps' base areas (they should match at equilibrium split)
    Apatch=0.5*(Aij+Aij.T)
    E_adh=-P*Apatch[iu].sum()
    E_inf=(E0*(Vr**(-GAMMA_V)-1)).sum()
    pr=np.where(nuc.sp=='p')[0]
    E_C=sum(AHC/d[i,j] for i,j in itertools.combinations(pr,2)) if len(pr)>1 else 0.0
    E_sl=-nuc.A*Y(nuc.A) if nuc.A>1 else 0.0
    E=E_adh+E_inf+E_C+E_sl
    if return_parts: return E,dict(adh=E_adh,inf=E_inf,coul=E_C,sling=E_sl,patch=Apatch[iu].sum(),Vr=Vr,Rg=Rg)
    return E

def relax(nuc,P,E0,restarts=4,seed=0):
    rng=np.random.default_rng(seed); best=None
    for k in range(restarts):
        x0=nuc.x0.ravel()+ (0 if k==0 else rng.normal(0,0.15,nuc.A*3))
        res=minimize(energy,x0,args=(nuc,P,E0),method='L-BFGS-B',options={'maxiter':3000,'ftol':1e-12,'gtol':1e-9})
        if best is None or res.fun<best.fun: best=res
    E,parts=energy(best.x,nuc,P,E0,True)
    return -E,parts,best.x.reshape(-1,3)

# starting geometries (fm), BCC-ish
def tetra(a=1.0): return [[0,0,0],[a,a,0],[a,0,a],[0,a,a]]   # edge a*sqrt2 = 1.414 fm < 2R_p: all six pairs overlap at start
NUC={
 'D':   Nucleus('D',['p','n'],[[0,0,0],[1.4,0,0]]),
 'T':   Nucleus('T',['p','n','n'],[[0,0,0],[1.4,0,0],[0.7,1.2,0]]),
 'He3': Nucleus('He3',['p','p','n'],[[0,0,0],[1.4,0,0],[0.7,1.2,0]]),
 'He4': Nucleus('He4',['p','p','n','n'],tetra()),
}
def two_alpha(sep=2.4):
    t=np.array(tetra()); c=t.mean(axis=0); t1=t-c; t2=t-c+np.array([sep,0,0])
    return np.vstack([t1,t2]).tolist()
NUC['Be8']=Nucleus('Be8',['p','p','n','n']*2,two_alpha())
def three_alpha(sep=2.4):
    t=np.array(tetra()); c=t.mean(axis=0); t1=t-c
    pts=[]
    for k in range(3):
        ang=2*math.pi*k/3; off=np.array([sep/math.sqrt(3)*math.cos(ang),sep/math.sqrt(3)*math.sin(ang),0])
        pts+= (t1+off).tolist()
    return pts
NUC['C12']=Nucleus('C12',['p','p','n','n']*3,three_alpha())
def four_alpha(sep=2.4):
    t=np.array(tetra()); c=t.mean(axis=0); t1=t-c
    T=np.array(tetra(sep/math.sqrt(2))); Tc=T-T.mean(axis=0)
    pts=[]
    for off in Tc: pts+=(t1+off).tolist()
    return pts
NUC['O16']=Nucleus('O16',['p','p','n','n']*4,four_alpha())

def calibrate():
    def miss(v):
        P,E0=v
        if P<=0 or E0<=0: return 1e6
        a=relax(NUC['D'],P,E0,restarts=1)[0]-BE['D']; b=relax(NUC['He4'],P,E0,restarts=1)[0]-BE['He4']
        return a*a+b*b
    best=None
    for P in [2,4,8,16,32]:
        for E0 in [20,50,100,200,400]:
            m=miss((P,E0))
            if best is None or m<best[0]: best=(m,P,E0)
    res=minimize(miss,[best[1],best[2]],method='Nelder-Mead',options={'xatol':1e-3,'fatol':1e-6,'maxiter':200})
    return res.x

if __name__=='__main__':
    if len(sys.argv)>2: P,E0=float(sys.argv[1]),float(sys.argv[2])
    else:
        P,E0=calibrate()
    print(f"calibrated on D and He-4:  P_adh = {P:.4f} MeV/fm^2   E0 = {E0:.3f} MeV   (gamma_V={GAMMA_V})")
    print(f"{'nucleus':6s} {'pred':>8s} {'meas':>8s} {'miss%':>7s}   adh     inflate  coul   sling   patch(fm2)  V/V0 range")
    for name in ['D','T','He3','He4','Be8','C12','O16']:
        be,p,x=relax(NUC[name],P,E0)
        print(f"{name:6s} {be:8.3f} {BE[name]:8.3f} {100*(be/BE[name]-1):7.2f}   {p['adh']:7.2f} {p['inf']:7.2f} {p['coul']:6.2f} {p['sling']:7.2f}  {p['patch']:7.3f}   {p['Vr'].min():.3f}-{p['Vr'].max():.3f}")
