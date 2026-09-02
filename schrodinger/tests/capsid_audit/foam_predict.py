#!/usr/bin/env python3
"""A5. Fixed operating point (d_core=0.95; sigma,w calibrated on H2+He4).
Alpha-cluster composites: Li5/He5 (alpha+N), Li6 (alpha+d), Li7 (alpha+t), Be8 (alpha+alpha).
Inter-cluster gap optimised; all pairs respect the hard core. Zero new constants."""
import numpy as np
from scipy.optimize import brentq, minimize_scalar, minimize
np.seterr(all='ignore')
R0=0.9; ALPHA=1.439965; V0=4*np.pi/3
DCORE=0.95; SIGMA=0.3433812460645254; W=0.26056533763836087
def capV(R,h): return np.pi*h*h*(R-h/3.0)
def solve_R(hs_fun):
    def f(R):
        hs=[h for h in hs_fun(R) if h>0]
        return (4*np.pi/3)*R**3-sum(capV(R,h) for h in hs)-V0
    R=1.0; fp=f(R)
    if fp>=0: return 1.0
    while R<4.0:
        R2=R+0.002; fn=f(R2)
        if fp<0<=fn: return brentq(f,R,R2)
        R,fp=R2,fn
    return None
def fib(n=160):
    i=np.arange(n)+0.5
    ph=np.arccos(1-2*i/n); th=np.pi*(1+5**0.5)*i
    return np.stack([np.sin(ph)*np.cos(th),np.sin(ph)*np.sin(th),np.cos(ph)],1)
_P=fib()
def U_shell(r,a1,a2):
    p1=_P*a1; p2=_P*a2+np.array([r,0,0])
    d=np.linalg.norm(p1[:,None,:]-p2[None,:,:],axis=2)
    return ALPHA*np.mean(1.0/d)
def E(pos,kinds):
    n=len(pos); pos=np.asarray(pos,float)
    D=np.linalg.norm(pos[:,None]-pos[None,:],axis=2)
    if any(D[i,j]<DCORE-1e-9 for i in range(n) for j in range(i+1,n)): return 1e6
    edges=[(i,j) for i in range(n) for j in range(i+1,n) if D[i,j]<1.999]
    Rs=[]
    for i in range(n):
        hf=lambda R,i=i:[R-D[i,j]/2 for j in range(n) if j!=i and D[i,j]<1.999]
        R=solve_R(hf)
        if R is None: return 1e6
        Rs.append(R)
    Afree=0; Afac=0
    for i in range(n):
        R=Rs[i]
        caps=[R-D[i,j]/2 for j in range(n) if j!=i and D[i,j]<1.999 and R-D[i,j]/2>0]
        Afree+=4*np.pi*R*R-sum(2*np.pi*R*h for h in caps)
    for i,j in edges:
        a2=min(Rs[i],Rs[j])**2-(D[i,j]/2)**2
        if a2>0: Afac+=np.pi*a2
    out=SIGMA*(Afree-n*4*np.pi)-W*Afac
    for i in range(n):
        for j in range(i+1,n):
            if kinds[i]=='p'==kinds[j]: out+=U_shell(D[i,j]*R0,Rs[i]*R0,Rs[j]*R0)
    return out
def tetra(d):
    s3=np.sqrt(3)
    return d*np.array([[0,0,0],[1,0,0],[0.5,s3/2,0],[0.5,s3/6,np.sqrt(2/3)]])
def tri(d): return d*np.array([[0,0,0],[1,0,0],[0.5,np.sqrt(3)/2,0]])
def dimer(d): return d*np.array([[0,0,0],[1,0,0]])
# recompute exact alpha optimum at this operating point
r=minimize_scalar(lambda d:E(tetra(d),['p','p','n','n']),bounds=(DCORE,1.999),method='bounded')
B4,d4=-r.fun,r.x
r=minimize_scalar(lambda d:E(dimer(d),['p','n']),bounds=(DCORE,1.999),method='bounded')
B2,d2=-r.fun,r.x
r=minimize_scalar(lambda d:E(tri(d),['p','n','n']),bounds=(DCORE,1.999),method='bounded'); B3=-r.fun
r=minimize_scalar(lambda d:E(tri(d),['p','n','p']),bounds=(DCORE,1.999),method='bounded'); Bh3=-r.fun
print(f"check: H2={B2:.3f} He4={B4:.3f} (d4={d4:.3f}) H3={B3:.3f} He3={Bh3:.3f}")
def composite(groupf,gk,label,exp,extra_axis=False):
    base=tetra(d4); face=base[[0,1,2]].mean(0)
    def posf(x):
        dg,g=x
        gp=groupf(dg); gc=gp.mean(0)
        return np.vstack([base,gp+(face+np.array([0,0,-g])-gc)])
    kinds=['p','p','n','n']+gk
    best=None
    for dg0 in (DCORE,1.0,1.1,d4):
        for g0 in (0.7,0.85,1.0,1.2):
            r=minimize(lambda x:E(posf(x),kinds),[dg0,g0],method='Nelder-Mead',
                       options={'xatol':1e-4,'fatol':1e-7,'maxiter':600})
            if best is None or r.fun<best.fun: best=r
    Bt=-best.fun
    print(f"  {label:5s}: B={Bt:8.3f}  exp={exp:>8}  extra-over-parts noted below  x={np.round(best.x,3)}")
    return Bt
print("\ncomposites (alpha core fixed at its optimum, zero new constants):")
B5p=composite(lambda d:np.zeros((1,3)),['p'],"Li5","UNBOUND")
B5n=composite(lambda d:np.zeros((1,3)),['n'],"He5","UNBOUND")
B6=composite(dimer,['p','n'],"Li6","31.994")
B7=composite(tri,['p','n','n'],"Li7","39.245")
B8=composite(tetra,['p','p','n','n'],"Be8","56.500")
print(f"\nseparation energies (model): Li5-alpha={B5p-B4:+.3f} (exp -1.97)  He5-alpha={B5n-B4:+.3f} (exp -0.89)")
print(f"Li6-(alpha+d)={B6-B4-B2:+.3f} (exp +1.474)   Li7-(alpha+t)={B7-B4-B3:+.3f} (exp +2.467)")
print(f"Be8-2alpha={B8-2*B4:+.3f} (exp -0.092)")
