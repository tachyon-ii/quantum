#!/usr/bin/env python3
"""
A3. Bonding-surface model with the TO truncation limit as the hard core.
Key physics added (NO new fitted constants):
  A truncated octahedron's hexagonal face is a fixed fraction of its
  surface. Flattening a contact facet beyond the hex-face area would cut
  into the capsid frame => forbidden. For a sphere of radius R this caps
  the facet: A_facet <= f_hex * 4*pi*R^2, with f_hex = (3*sqrt(3)/2)/(12*sqrt(3)+6)
  from pure TO geometry. Equivalently d >= d_min(R). "Closer it rejects" is
  the truncation limit, not a tuned repulsion.
Coulomb: hollow-shell charges (posit-consistent). r0 = 0.9 fm fixed.
Constants sigma, w calibrated on H2 + He4; all else predicted.
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar, minimize, fsolve

R0=0.9; ALPHA=1.439965; V0=4*np.pi/3
F_HEX=(3*np.sqrt(3)/2)/(12*np.sqrt(3)+6)   # single hex face / TO surface = 0.09703
CHI = 1-4*F_HEX                            # facet: R^2-(d/2)^2 <= 4*f_hex*R^2 -> (d/2R)^2 >= 1-4f_hex
DMIN_OVER_R = 2*np.sqrt(CHI)               # = 1.5652

def capV(R,h): return np.pi*h*h*(R-h/3.0)
def solve_R(hlist_fun):
    def f(R):
        hs=[h for h in hlist_fun(R) if h>0]
        return (4*np.pi/3)*R**3 - sum(capV(R,h) for h in hs) - V0
    R=1.0; fprev=f(R)
    if fprev>=0: return 1.0
    while R<4.0:
        R2=R+0.002; fnew=f(R2)
        if fprev<0<=fnew: return brentq(f,R,R2)
        R,fprev=R2,fnew
    return None

def fib_sphere(n=192):
    i=np.arange(n)+0.5
    phi=np.arccos(1-2*i/n); th=np.pi*(1+5**0.5)*i
    return np.stack([np.sin(phi)*np.cos(th),np.sin(phi)*np.sin(th),np.cos(phi)],1)
_PTS=fib_sphere(192)
def U_shell(r,a1,a2):
    p1=_PTS*a1; p2=_PTS*a2+np.array([r,0,0])
    d=np.linalg.norm(p1[:,None,:]-p2[None,:,:],axis=2)
    return ALPHA*np.mean(1.0/d)

def cluster_energy(pos,kinds,sigma,w,dmax=1.999):
    n=len(pos); pos=np.asarray(pos,float)
    D=np.linalg.norm(pos[:,None]-pos[None,:],axis=2)
    edges=[(i,j) for i in range(n) for j in range(i+1,n) if D[i,j]<dmax]
    Rs=[]
    for i in range(n):
        hf=lambda R,i=i:[R-D[i,j]/2 for j in range(n) if j!=i and D[i,j]<dmax]
        R=solve_R(hf)
        if R is None: return 1e6
        Rs.append(R)
    # TO truncation constraint: every contact facet within hex limit
    for i,j in edges:
        if D[i,j] < DMIN_OVER_R*max(Rs[i],Rs[j]) - 1e-9: return 1e6
    Afree=0.0; Afac=0.0
    for i in range(n):
        R=Rs[i]
        caps=[R-D[i,j]/2 for j in range(n) if j!=i and D[i,j]<dmax and R-D[i,j]/2>0]
        Afree += 4*np.pi*R*R - sum(2*np.pi*R*h for h in caps)
    for i,j in edges:
        a2=min(Rs[i]**2,Rs[j]**2)-(D[i,j]/2)**2
        if a2>0: Afac+=np.pi*a2
    E=sigma*(Afree-n*4*np.pi)-w*Afac
    for i in range(n):
        for j in range(i+1,n):
            if kinds[i]=='p' and kinds[j]=='p':
                E+=U_shell(D[i,j]*R0,Rs[i]*R0,Rs[j]*R0)
    return E

def tetra(d):
    s3=np.sqrt(3)
    return d*np.array([[0,0,0],[1,0,0],[0.5,s3/2,0],[0.5,s3/6,np.sqrt(2/3)]])
def tri(d):
    s3=np.sqrt(3); return d*np.array([[0,0,0],[1,0,0],[0.5,s3/2,0]])
def dimer(d): return d*np.array([[0,0,0],[1,0,0]])

def B_of(posf,kinds,sigma,w):
    f=lambda d: cluster_energy(posf(d),kinds,sigma,w)
    r=minimize_scalar(f,bounds=(1.2,1.999),method='bounded')
    return -r.fun,r.x

def alpha_plus(group_posf,group_kinds,da,sigma,w,gaps=(1.5,1.7,1.9),dgs=(1.55,1.65,1.75)):
    base=tetra(da); cf=base[[0,1,2]].mean(0)
    def posf(x):
        dg,g=x; gp=group_posf(dg); gc=gp.mean(0)
        return np.vstack([base, gp+(cf+np.array([0,0,-g])-gc)])
    kinds_all=['p','p','n','n']+group_kinds
    f=lambda x: cluster_energy(posf(x),kinds_all,sigma,w)
    best=None
    for dg0 in dgs:
        for g0 in gaps:
            r=minimize(f,[dg0,g0],method='Nelder-Mead',options={'xatol':1e-4,'fatol':1e-7,'maxiter':500})
            if best is None or r.fun<best.fun: best=r
    return -best.fun,best.x

def calib(x):
    s,wq=x
    B2,_=B_of(dimer,['p','n'],s,wq)
    B4,_=B_of(tetra,['p','p','n','n'],s,wq)
    return [B2-2.2246,B4-28.2957]
(sigma,w),info,ok,msg=fsolve(calib,[0.3,3.0],full_output=True)
B2,d2=B_of(dimer,['p','n'],sigma,w);B4,d4=B_of(tetra,['p','p','n','n'],sigma,w)
print(f"sigma={sigma:.4f} w={w:.4f} converged={ok==1}; TO limit d/R={DMIN_OVER_R:.4f}")
print(f"H2 {B2:7.3f} (2.225) d={d2:.3f} | He4 {B4:7.3f} (28.296) d={d4:.3f}")
print("\npredictions (zero further freedom):")
B,d=B_of(tri,['p','n','n'],sigma,w); print(f"  H3  : {B:8.3f}  exp  8.482  d={d:.3f}")
B,d=B_of(tri,['p','n','p'],sigma,w); print(f"  He3 : {B:8.3f}  exp  7.718  d={d:.3f}")
B6,x6=alpha_plus(dimer,['p','n'],d4,sigma,w);   print(f"  Li6 : {B6:8.3f}  exp 31.994  x={np.round(x6,3)}")
B7,x7=alpha_plus(tri,['p','n','n'],d4,sigma,w); print(f"  Li7 : {B7:8.3f}  exp 39.245  x={np.round(x7,3)}")
B8,x8=alpha_plus(tetra,['p','p','n','n'],d4,sigma,w); print(f"  Be8 : {B8:8.3f}  target ~56.50 (unbound vs 2alpha by 0.092) x={np.round(x8,3)}")
# A=5 test: alpha + 1 proton (Li5) and alpha + 1 neutron (He5) - both unbound in nature
B5p,x5p=alpha_plus(lambda d: np.zeros((1,3)),['p'],d4,sigma,w)
B5n,x5n=alpha_plus(lambda d: np.zeros((1,3)),['n'],d4,sigma,w)
print(f"  Li5 : {B5p:8.3f}  exp UNBOUND (-1.97 rel alpha+p => B<29.3 means unbound if B-28.296<1.0?) raw alpha+p extra={B5p-B4:.3f}")
print(f"  He5 : {B5n:8.3f}  exp UNBOUND (-0.89) extra={B5n-B4:.3f}")
