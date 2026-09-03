#!/usr/bin/env python3
"""
A. The bonding-surface ("gossamer balloon") model, quantified.
Posit (James 2026-08-23): hollow inflated capsids; on contact, faces
flatten; bond energy = "magnetic-type force proportional to the bonding
surface", one constant; Coulomb between proton cores is standard EM.

Model (adhesive deformable spheres, foam/vesicle physics):
- N nucleons, rest volume V0 = 4pi/3 (rest radius r0 = 1; physical scale
  r0 = 0.9 fm fixed a priori from the docs' orbital radius, NOT fitted).
- Cluster = graph of contacts; contacting pair at centre distance d
  shares a flat facet on the bisector plane (cap height h = R - d/2).
- Volume conservation (incompressible contents): R inflates to keep
  V(R) - sum(caps) = V0 for each sphere.
- Energy:  E = sigma*(free surface area)  -  w*(total facet area)
           + Coulomb(point protons at centres, 1.44 MeV.fm / d)
- Binding B = E(separated spheres) - E(cluster), maximised over d.
- TWO physical constants (sigma, w) calibrated on H2 AND He4.
  Everything else (H3, He3, Li6, Li7, Be8) is then PREDICTION,
  including all Coulomb terms (parameter-free).
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar

R0   = 0.9      # fm, rest radius (fixed a priori)
ALPHA= 1.439965 # MeV.fm

# ---------- cluster geometries (unit edge, scaled by d) ----------
def geom(name):
    s2=np.sqrt(2); s3=np.sqrt(3)
    if name=="dimer":   pts=[[0,0,0],[1,0,0]]
    elif name=="tri":   pts=[[0,0,0],[1,0,0],[0.5,s3/2,0]]
    elif name=="tetra": pts=[[0,0,0],[1,0,0],[0.5,s3/2,0],[0.5,s3/6,np.sqrt(2.0/3)]]
    elif name=="octa":  pts=[[0.5,0.5,0],[0.5,-0.5,0],[-0.5,0.5,0],[-0.5,-0.5,0],[0,0,1/s2],[0,0,-1/s2]]
    elif name=="pentabipy":
        c=[[np.cos(2*np.pi*k/5),np.sin(2*np.pi*k/5),0] for k in range(5)]
        rr=1/(2*np.sin(np.pi/5))  # circumradius for unit edge pentagon
        pts=[[rr*x,rr*y,0] for x,y,_ in c]
        zz=np.sqrt(max(1-rr**2,1e-12))
        pts+= [[0,0,zz],[0,0,-zz]]
    elif name=="2tetra": # two unit tetrahedra tip-to-tip sharing one contact (alpha-alpha)
        t1=np.array(geom("tetra")[0]); t2=t1+np.array([0,0,10]) # placeholder, built below
        return None
    return np.array(pts,float)

def contacts(pts, d, tol=1e-6):
    """pairs within ~edge distance (unit-edge geoms scaled by d)"""
    out=[]
    n=len(pts)
    for i in range(n):
        for j in range(i+1,n):
            if abs(np.linalg.norm(pts[i]-pts[j])-1.0)<0.05: out.append((i,j))
    return out

# ---------- sphere with k caps of height h: volume & areas ----------
def capV(R,h): return np.pi*h*h*(R - h/3.0)
def solve_R(k, d):
    """Smallest R >= 1 with sphere-minus-k-caps volume = 4pi/3.
    For k>2 f(R) rises then falls (caps eat growth); take the first root.
    Returns None if infeasible (too many contacts at too small d)."""
    V0=4*np.pi/3
    def f(R):
        h=max(R-d/2,0.0)
        return (4*np.pi/3)*R**3 - k*capV(R,h) - V0
    if k==0: return 1.0
    R=1.0; step=0.002
    fprev=f(R)
    while R<4.0:
        R2=R+step; fnew=f(R2)
        if fprev<0<=fnew:
            return brentq(f,R,R2)
        # detect passing the maximum while still negative -> infeasible
        R, fprev = R2, fnew
        if k>2 and R > k*d/(2*(k-2)) and fprev<0:
            return None
    return None

def cluster_energy(name, d, sigma, w, protons):
    pts=geom(name); con=contacts(pts,d)
    if d>=2.0 or not con:  # no overlap => no binding
        return 0.0
    deg=np.zeros(len(pts),int)
    for i,j in con: deg[i]+=1; deg[j]+=1
    Rs=[solve_R(deg[i], d) for i in range(len(pts))]
    if any(r is None for r in Rs): return 1e6  # infeasible geometry
    Afree=0.0; Afac=0.0
    for i in range(len(pts)):
        R=Rs[i]; h=R-d/2
        Afree += 4*np.pi*R*R - deg[i]*2*np.pi*R*h
    for i,j in con:
        a2=min(Rs[i]**2, Rs[j]**2)-(d/2)**2
        Afac += np.pi*max(a2,0.0)
    E_surf = sigma*(Afree - len(pts)*4*np.pi)   # stretch beyond rest area
    E_bond = -w*Afac
    # Coulomb: physical distances = d * R0? NO: unit-edge geometry scaled by d, and d in units of r0 -> phys dist = d*... 
    # We work in units where rest radius = 1 <=> R0 fm. Centre distance d (model units) -> d*R0 fm.
    U=0.0
    for a in range(len(protons)):
        for b in range(a+1,len(protons)):
            i,j=protons[a],protons[b]
            r=np.linalg.norm(pts[i]-pts[j])*d*R0
            U+=ALPHA/r
    return E_surf+E_bond+U

def binding(name, sigma, w, protons):
    res=minimize_scalar(lambda d: cluster_energy(name,d,sigma,w,protons),
                        bounds=(1.0,1.999), method='bounded')
    return -res.fun, res.x  # B = -E (E_separated = 0)

# ---------- calibrate on H2 (np) and He4 (2p2n tetra) ----------
from scipy.optimize import fsolve
def calib(x):
    sigma,w=x
    B2,_=binding("dimer",sigma,w,protons=[0])      # d: p at 0, n at 1 -> no pp
    B4,_=binding("tetra",sigma,w,protons=[0,1])    # 2 protons
    return [B2-2.2246, B4-28.2957]
sol=fsolve(calib,[2.0,4.0],full_output=True)
(sigma,w),info,ok,msg=sol
print(f"calibrated: sigma={sigma:.4f} MeV/r0^2, w={w:.4f} MeV/r0^2, converged={ok==1}")
B2,d2=binding("dimer",sigma,w,[0]);  B4,d4=binding("tetra",sigma,w,[0,1])
print(f"  H2 : B={B2:7.3f} (exp  2.225)  d={d2:.3f}")
print(f"  He4: B={B4:7.3f} (exp 28.296)  d={d4:.3f}")
# ---------- predictions, zero further freedom ----------
tests=[("H3","tri",[0],8.4818),("He3","tri",[0,1],7.7180),
       ("Li6","octa",[0,2,4],31.9941),      # 3 protons max separated on octahedron
       ("Li7","pentabipy",[0,2,5],39.2445)] # 3 protons spread
print("\npredictions (no further tuning):")
for label,g,pr,exp in tests:
    B,d=binding(g,sigma,w,pr)
    print(f"  {label:4s}: B={B:8.3f}  exp={exp:8.3f}   ratio={B/exp:5.2f}   d_opt={d:.3f}")
