#!/usr/bin/env python3
"""
The sock model (James, 2026-08-23): organic packing, no lattice.
- Two species of compressible spheres:
    proton : radius Rp, stiffness Kp, charge +1 (cares where it sits)
    neutron: radius Rn = Rp*2^(1/3) (2x inflation pressure), stiffness 2*Kp
- Isotropic annular adhesion well (Derjaguin): every close pair, any species
    U_well(gap) = -EPS * exp(-(gap-GSTAR)^2 / 2 LAM^2)
- Hertzian compression: U_rep = (2/5) Keff * overlap^(5/2)
- Coulomb: hollow-shell pp
- "Twist and rattle" = basin hopping (random starts + BFGS)
- "Jiggle" kept quantum: E_zp = (hbar/2) * sum internal normal modes
Constants fitted: EPS on H2, Kp scale on He4 (2 total). All else fixed a priori.
"""
import numpy as np, itertools
from scipy.optimize import minimize
rng=np.random.default_rng(7)
HBARC=197.3269804; MN=938.918; ALPHA=1.439965
Rp=0.84; Rn=Rp*2**(1/3)          # fm
GSTAR=0.0; LAM=0.90               # well at contact, width 0.25 fm (fixed)
ASH=0.84
def fib(n=96):
    i=np.arange(n)+0.5
    ph=np.arccos(1-2*i/n); th=np.pi*(1+5**0.5)*i
    return np.stack([np.sin(ph)*np.cos(th),np.sin(ph)*np.sin(th),np.cos(ph)],1)
_P=fib(); _UC={}
def Ur(r):
    key=round(r,3)
    if key not in _UC:
        p1=_P*ASH; p2=_P*ASH+np.array([r,0,0])
        _UC[key]=ALPHA*np.mean(1.0/np.linalg.norm(p1[:,None,:]-p2[None,:,:],axis=2))
    return _UC[key]
def energy(x, kinds, EPS, KP):
    n=len(kinds); pos=x.reshape(n,3); E=0.0
    for i,j in itertools.combinations(range(n),2):
        r=np.linalg.norm(pos[i]-pos[j])
        Ri=Rn if kinds[i]=='n' else Rp; Rj=Rn if kinds[j]=='n' else Rp
        Ki=2*KP if kinds[i]=='n' else KP; Kj=2*KP if kinds[j]=='n' else KP
        Keff=Ki*Kj/(Ki+Kj)
        gap=r-(Ri+Rj)
        if gap<0: E+=0.4*Keff*(-gap)**2.5
        E+=-EPS*np.exp(-(gap-GSTAR)**2/(2*LAM**2))
        if kinds[i]=='p'==kinds[j]: E+=Ur(r)
    return E
def minimize_cluster(kinds, EPS, KP, tries=24):
    n=len(kinds); best=None
    for t in range(tries):
        x0=rng.normal(0,0.8,(n,3)).ravel()
        r=minimize(energy,x0,args=(kinds,EPS,KP),method='L-BFGS-B')
        if best is None or r.fun<best.fun: best=r
    return best
def zero_point(x, kinds, EPS, KP):
    n=len(kinds); h=1e-4; N=3*n
    H=np.zeros((N,N))
    f0=energy(x,kinds,EPS,KP)
    for a in range(N):
        for b in range(a,N):
            xa=x.copy(); xa[a]+=h; xa[b]+=h; fpp=energy(xa,kinds,EPS,KP)
            xa=x.copy(); xa[a]+=h; xa[b]-=h; fpm=energy(xa,kinds,EPS,KP)
            xa=x.copy(); xa[a]-=h; xa[b]+=h; fmp=energy(xa,kinds,EPS,KP)
            xa=x.copy(); xa[a]-=h; xa[b]-=h; fmm=energy(xa,kinds,EPS,KP)
            H[a,b]=H[b,a]=(fpp-fpm-fmp+fmm)/(4*h*h)
    w2=np.linalg.eigvalsh(H)          # MeV/fm^2
    w2=w2[w2>1e-4]                     # drop 6 rigid modes
    return 0.5*HBARC*np.sum(np.sqrt(np.maximum(w2,0)/MN))
def B_of(kinds, EPS, KP, zp=True):
    r=minimize_cluster(kinds,EPS,KP)
    n=len(kinds)
    # reference: isolated nucleons have well self-energy 0 -> E_sep=0
    Ezp=zero_point(r.x,kinds,EPS,KP) if (zp and n>1) else 0.0
    return -(r.fun)-Ezp, r
# --- calibrate EPS on H2 (with zp), KP on He4 ---
from scipy.optimize import brentq
def calib():
    def f2(EPS,KP): return B_of(['p','n'],EPS,KP)[0]-2.2246
    def f4(KP):
        EPS=brentq(lambda e: f2(e,KP), 1.0, 80.0, xtol=1e-3)
        return B_of(['p','p','n','n'],EPS,KP)[0]-28.2957, EPS
    lo,hi=20.0,2000.0
    for KP in np.geomspace(lo,hi,10):
        d,E=f4(KP)
        print(f"  scan KP={KP:8.1f}: He4 err={d:+8.3f} (EPS={E:.3f})")
    return None
calib()
