#!/usr/bin/env python3
"""
A4. The decisive scan: model class M(sigma, w, d_core):
  - hard core at centre distance d_core (in rest radii): the ONLY free geometry knob
  - adhesion w * facet area, stretch sigma * excess free area, volume conservation
  - hollow-shell Coulomb, r0=0.9 fm, parameter-free
For each d_core: calibrate (sigma,w) on H2+He4 exactly, then PREDICT H3, He3.
Question: does any d_core make the parameter-free A=3 predictions land?
And what does that d_core say about geometry (TO-limit 1.565 vs dual-globe ~1.0)?
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar, fsolve
np.seterr(all='ignore')
R0=0.9; ALPHA=1.439965; V0=4*np.pi/3
def capV(R,h): return np.pi*h*h*(R-h/3.0)
def solve_R(c,d):
    def f(R):
        h=R-d/2
        return (4*np.pi/3)*R**3-(c*capV(R,h) if h>0 else 0)-V0
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

def cluster(geo,kinds,d,sigma,w):
    pos={"dimer":np.array([[0,0,0],[1,0,0]]),
         "tri":np.array([[0,0,0],[1,0,0],[0.5,np.sqrt(3)/2,0]]),
         "tetra":np.array([[0,0,0],[1,0,0],[0.5,np.sqrt(3)/2,0],[0.5,np.sqrt(3)/6,np.sqrt(2/3)]])}[geo]*d
    n=len(pos); D=np.linalg.norm(pos[:,None]-pos[None,:],axis=2)
    edges=[(i,j) for i in range(n) for j in range(i+1,n) if D[i,j]<1.999]
    c=np.zeros(n,int)
    for i,j in edges: c[i]+=1; c[j]+=1
    Rs=[solve_R(c[i],d) for i in range(n)]
    if any(r is None for r in Rs): return None
    Afree=sum(4*np.pi*R*R-c[i]*2*np.pi*R*max(R-d/2,0) for i,R in enumerate(Rs))
    Afac=sum(np.pi*max(min(Rs[i],Rs[j])**2-(d/2)**2,0) for i,j in edges)
    E=sigma*(Afree-n*4*np.pi)-w*Afac
    for i in range(n):
        for j in range(i+1,n):
            if kinds[i]=='p'==kinds[j]:
                E+=U_shell(D[i,j]*R0,Rs[i]*R0,Rs[j]*R0)
    return E
def B(geo,kinds,sigma,w,dcore):
    r=minimize_scalar(lambda d: (cluster(geo,kinds,d,sigma,w) or 1e6),
                      bounds=(dcore,1.999),method='bounded')
    return -r.fun,r.x
print(f"{'d_core':>6} {'sigma':>8} {'w':>8} {'H3pred':>8} {'He3pred':>8} {'split':>7} | exp: 8.482 7.718 0.764")
best=None
for dcore in np.arange(0.80,1.60,0.05):
    try:
        def cal(x):
            s,wq=x
            b2,_=B("dimer",['p','n'],s,wq,dcore)
            b4,_=B("tetra",['p','p','n','n'],s,wq,dcore)
            return [b2-2.2246,b4-28.2957]
        (s,wq),info,ok,msg=fsolve(cal,[0.4,0.3],full_output=True)
        if ok!=1 or s<0 or wq<0: 
            (s,wq),info,ok,msg=fsolve(cal,[1.0,1.0],full_output=True)
            if ok!=1 or s<0 or wq<0: print(f"{dcore:6.2f}  calibration failed/unphysical"); continue
        b3,_=B("tri",['p','n','n'],s,wq,dcore)
        bh3,_=B("tri",['p','n','p'],s,wq,dcore)
        err=abs(b3-8.4818)+abs(bh3-7.718)
        tag=""
        if best is None or err<best[0]: best=(err,dcore,s,wq,b3,bh3); tag="  <-- best so far"
        print(f"{dcore:6.2f} {s:8.4f} {wq:8.4f} {b3:8.3f} {bh3:8.3f} {b3-bh3:7.3f}{tag}")
    except Exception as e:
        print(f"{dcore:6.2f}  error {e}")
print("\nBEST:",best)
