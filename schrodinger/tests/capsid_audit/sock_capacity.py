#!/usr/bin/env python3
"""
Sock model + capacity: organic packing with each marble owning TWO HANDS
(the lemniscate's two lobes, continuum form). Per-marble adhesion saturates:
   s_i = sum_j phi(gap_ij),  phi = EPS*exp(-gap^2/2LAM^2)  (NP pairs only carry
   the well at full strength; NN at 0.75 per the docs' persistence ratio; PP none)
   E_well = -(1/2) * sum_i SMAX*tanh(s_i/SMAX),  SMAX = 2*EPS  (two hands)
Plus Hertz compression (neutron 2x stiffness, 2^(1/3) radius), shell Coulomb,
basin-hopped minima, harmonic zero-point (h=2e-3).
Constants: EPS calibrated on H2; KP=100 fixed; LAM=0.9 fm fixed (pion-range).
Everything else predicted.
"""
import numpy as np, itertools
from scipy.optimize import minimize, brentq
rng=np.random.default_rng(11)
HBARC=197.3269804; MN=938.918; ALPHA=1.439965
Rp=0.84; Rn=Rp*2**(1/3); LAM=0.90; KP=100.0; ASH=0.84; FNN=0.75
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
def energy(x,kinds,EPS):
    n=len(kinds); pos=x.reshape(n,3); E=0.0
    s=np.zeros(n); SMAX=2*EPS
    for i,j in itertools.combinations(range(n),2):
        r=np.linalg.norm(pos[i]-pos[j])
        Ri=Rn if kinds[i]=='n' else Rp; Rj=Rn if kinds[j]=='n' else Rp
        Ki=2*KP if kinds[i]=='n' else KP; Kj=2*KP if kinds[j]=='n' else KP
        gap=r-(Ri+Rj)
        if gap<0: E+=0.4*(Ki*Kj/(Ki+Kj))*(-gap)**2.5
        w=np.exp(-gap*gap/(2*LAM*LAM))
        if kinds[i]!=kinds[j]: f=1.0
        elif kinds[i]=='n': f=FNN
        else: f=0.0
        s[i]+=f*EPS*w; s[j]+=f*EPS*w
        if kinds[i]=='p'==kinds[j]: E+=Ur(r)
    E+=-0.5*np.sum(SMAX*np.tanh(s/SMAX))
    return E
def minimize_cluster(kinds,EPS,tries=28):
    n=len(kinds); best=None
    for t in range(tries):
        x0=rng.normal(0,0.9,(n,3)).ravel()
        r=minimize(energy,x0,args=(kinds,EPS),method='L-BFGS-B')
        if best is None or r.fun<best.fun: best=r
    return best
def zero_point(x,kinds,EPS,h=2e-3):
    N=len(x); H=np.zeros((N,N))
    for a in range(N):
        for b in range(a,N):
            xa=x.copy(); xa[a]+=h; xa[b]+=h; f1=energy(xa,kinds,EPS)
            xa=x.copy(); xa[a]+=h; xa[b]-=h; f2=energy(xa,kinds,EPS)
            xa=x.copy(); xa[a]-=h; xa[b]+=h; f3=energy(xa,kinds,EPS)
            xa=x.copy(); xa[a]-=h; xa[b]-=h; f4=energy(xa,kinds,EPS)
            H[a,b]=H[b,a]=(f1-f2-f3+f4)/(4*h*h)
    w2=np.linalg.eigvalsh(H)
    w2=w2[w2>0.5]   # drop rigid modes robustly
    return 0.5*HBARC*np.sum(np.sqrt(w2/MN))
def B_of(kinds,EPS):
    r=minimize_cluster(kinds,EPS)
    zp=zero_point(r.x,kinds,EPS) if len(kinds)>1 else 0.0
    return -r.fun-zp, r, zp
# calibrate
EPS=brentq(lambda e: B_of(['p','n'],e)[0]-2.2246, 15.0, 80.0, xtol=2e-2)
print(f"EPS={EPS:.2f} MeV (calibrated on H2; SMAX=2EPS; LAM=0.9; KP=100; nn=0.75, pp=0)")
tests=[("H2",['p','n'],2.2246),("H3",['p','n','n'],8.4818),("He3",['p','p','n'],7.7180),
       ("He4",['p','p','n','n'],28.2957),("He5",['p','p','n','n','n'],27.41),
       ("Li5",['p','p','p','n','n'],26.33),("Li6",['p','p','p','n','n','n'],31.9941),
       ("Li7",['p','p','p','n','n','n','n'],39.2445),("Be8",['p','p','p','p','n','n','n','n'],56.4996),
       ("Be9",['p','p','p','p','n','n','n','n','n'],58.164)]
print(f"{'nuc':5} {'model':>9} {'exp':>8} {'E_zp':>7}  shape (sorted pair dists)")
out={}
for name,kinds,exp in tests:
    B,r,zp=B_of(kinds,EPS)
    out[name]=B
    pos=r.x.reshape(len(kinds),3)
    d=sorted(round(np.linalg.norm(pos[i]-pos[j]),2) for i,j in itertools.combinations(range(len(kinds)),2))[:8]
    print(f"{name:5} {B:9.3f} {exp:8.3f} {zp:7.2f}  {d}")
print(f"\nstability margins: He5-He4={out['He5']-out['He4']:+.3f} (exp -0.89)  Li5-He4={out['Li5']-out['He4']:+.3f} (exp -1.97)")
print(f"  Be8-2He4={out['Be8']-2*out['He4']:+.3f} (exp -0.092)  Be9-Be8-n={out['Be9']-out['Be8']:+.3f} (exp +1.665)")
print(f"  Li6-(He4+H2)={out['Li6']-out['He4']-out['H2']:+.3f} (exp +1.474)  Li7-(He4+H3)={out['Li7']-out['He4']-out['H3']:+.3f} (exp +2.467)")
