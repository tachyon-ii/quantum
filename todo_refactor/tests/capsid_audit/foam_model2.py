#!/usr/bin/env python3
"""
A2. Bonding-surface model, round 2.
Changes vs round 1 (each physically forced, none fitted):
 1. Coulomb between HOLLOW shells (uniform charge on capsid surface),
    not point centres - James's hollowness posit, applied consistently.
 2. Alpha-cluster geometries for A>4 (Li6 = alpha+deuteron, Li7 = alpha+triton,
    Be8 = alpha+alpha) - the capsid picture's own reading.
 3. General per-edge distances: sub-clusters keep their own optimal d,
    only the inter-cluster gap is optimised.
Constants: sigma, w calibrated on H2 + He4 only (as round 1). r0=0.9 fm fixed.
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar, fsolve

R0=0.9; ALPHA=1.439965
V0=4*np.pi/3

def capV(R,h): return np.pi*h*h*(R-h/3.0)

def solve_R_general(hfun, R_lo=1.0):
    """R with V(R) - sum caps(R) = V0, caps from hfun(R) -> list of cap heights."""
    def f(R):
        hs=[h for h in hfun(R) if h>0]
        return (4*np.pi/3)*R**3 - sum(capV(R,h) for h in hs) - V0
    R=R_lo; step=0.002; fprev=f(R)
    if fprev>=0: return R
    while R<4.0:
        R2=R+step; fnew=f(R2)
        if fprev<0<=fnew: return brentq(f,R,R2)
        R,fprev=R2,fnew
    return None

# ---- shell-shell Coulomb (uniform charge on sphere surface radius a), numeric
def fib_sphere(n=256):
    i=np.arange(n)+0.5
    phi=np.arccos(1-2*i/n); th=np.pi*(1+5**0.5)*i
    return np.stack([np.sin(phi)*np.cos(th),np.sin(phi)*np.sin(th),np.cos(phi)],1)
_PTS=fib_sphere(256)
def U_shell(r, a1, a2):
    """MeV for unit charges e on shells radius a1,a2 (fm), centres r fm apart."""
    p1=_PTS*a1; p2=_PTS*a2 + np.array([r,0,0])
    d=np.linalg.norm(p1[:,None,:]-p2[None,:,:],axis=2)
    return ALPHA*np.mean(1.0/d)

# ---- cluster spec: positions (fm-free model units, rest radius 1), edges implicit by distance
def cluster_energy(pos, kinds, sigma, w, dmax=1.999):
    n=len(pos); pos=np.asarray(pos,float)
    D=np.linalg.norm(pos[:,None]-pos[None,:],axis=2)
    edges=[(i,j) for i in range(n) for j in range(i+1,n) if D[i,j]<dmax]
    Rs=[]
    for i in range(n):
        hf=lambda R,i=i: [R - D[i,j]/2 for j in range(n) if j!=i and D[i,j]<dmax]
        R=solve_R_general(hf)
        if R is None: return 1e6
        Rs.append(R)
    Afree=0.0; Afac=0.0
    for i in range(n):
        R=Rs[i]
        caps=[R-D[i,j]/2 for j in range(n) if j!=i and D[i,j]<dmax and R-D[i,j]/2>0]
        Afree += 4*np.pi*R*R - sum(2*np.pi*R*h for h in caps)
    for i,j in edges:
        a2=min(Rs[i]**2,Rs[j]**2)-(D[i,j]/2)**2
        if a2>0: Afac += np.pi*a2
    E = sigma*(Afree - n*4*np.pi) - w*Afac
    # Coulomb between protons: hollow shells radius Rs[i]*R0, centres D*R0
    for i in range(n):
        for j in range(i+1,n):
            if kinds[i]=='p' and kinds[j]=='p':
                E += U_shell(D[i,j]*R0, Rs[i]*R0, Rs[j]*R0)
    return E

# ---- geometries ----
def tetra(d):
    s3=np.sqrt(3)
    return d*np.array([[0,0,0],[1,0,0],[0.5,s3/2,0],[0.5,s3/6,np.sqrt(2/3)]])
def tri(d):
    s3=np.sqrt(3); return d*np.array([[0,0,0],[1,0,0],[0.5,s3/2,0]])
def dimer(d): return d*np.array([[0,0,0],[1,0,0]])

def B_of(posf, kinds, sigma, w):
    f=lambda d: cluster_energy(posf(d), kinds, sigma, w)
    r=minimize_scalar(f, bounds=(0.8,1.999), method='bounded')
    return -r.fun, r.x

# composite: alpha (own scale da) + attached group (own scale dg) at gap g along +z axis, group below face
def alpha_plus(group_posf, group_kinds, da, sigma, w):
    """attach group beneath the bottom face (z=0 plane triangle) of tetra"""
    base=tetra(da)
    centroid_face=base[[0,1,2]].mean(0)
    def posf(x):
        dg,g=x
        gp=group_posf(dg)
        gc=gp.mean(0)
        shift=centroid_face + np.array([0,0,-g]) - gc
        return np.vstack([base, gp+shift])
    kinds_all=['p','p','n','n']+group_kinds
    f=lambda x: cluster_energy(posf(x), kinds_all, sigma, w)
    best=None
    for dg0 in (0.9,1.0,1.1):
        for g0 in (0.9,1.1,1.3):
            from scipy.optimize import minimize
            r=minimize(f,[dg0,g0],method='Nelder-Mead',
                       options={'xatol':1e-4,'fatol':1e-6,'maxiter':400})
            if best is None or r.fun<best.fun: best=r
    return -best.fun, best.x

# ---- calibrate ----
def calib(x):
    s,w=x
    B2,_=B_of(dimer,['p','n'],s,w)
    B4,_=B_of(tetra,['p','p','n','n'],s,w)
    return [B2-2.2246, B4-28.2957]
(sigma,w),info,ok,msg=fsolve(calib,[0.37,0.24],full_output=True)
print(f"sigma={sigma:.4f}  w={w:.4f}  (MeV per unit rest-area), converged={ok==1}")
B2,d2=B_of(dimer,['p','n'],sigma,w); B4,d4=B_of(tetra,['p','p','n','n'],sigma,w)
print(f"H2 {B2:7.3f} (2.225) d={d2:.3f} | He4 {B4:7.3f} (28.296) d={d4:.3f}")

print("\npredictions (zero further freedom):")
B,d=B_of(tri,['p','n','n'],sigma,w);   print(f"  H3  : {B:8.3f}  exp  8.482  d={d:.3f}")
B,d=B_of(tri,['p','n','p'],sigma,w);   print(f"  He3 : {B:8.3f}  exp  7.718  d={d:.3f}")
B6,x6=alpha_plus(dimer,['p','n'],d4,sigma,w);  print(f"  Li6 : {B6:8.3f}  exp 31.994  (alpha+d, dg={x6[0]:.3f} gap={x6[1]:.3f})")
B7,x7=alpha_plus(tri,['p','n','n'],d4,sigma,w);print(f"  Li7 : {B7:8.3f}  exp 39.245  (alpha+t, dg={x7[0]:.3f} gap={x7[1]:.3f})")
B8,x8=alpha_plus(tetra,['p','p','n','n'],d4,sigma,w);print(f"  Be8 : {B8:8.3f}  exp 56.500 (2 alpha; unbound vs 2a by 0.092 -> target 2*28.296={2*28.2957:.3f})")
