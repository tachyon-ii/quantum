#!/usr/bin/env python3
"""
build3_closure.py — Build 3: lane closure on the Kelvin bond graph (Grace, 16 Oct 2026).

Declared before running (James 16 Oct; Argon's guardrails; Grace's one rule):
  R1  Nucleons sit on BCC sites (integer triples, all even or all odd; unit = R_p = 0.8409 fm).
      Contacts: S-S at distance 2 (face area 1 sq-unit), H-H at sqrt3 (area 2.598076). Overlap (< sqrt3) forbidden.
  R2  Closure rule, ONE law: for contact (i,j) on c_ij triangles of the bond graph,
         A_ij = A_open                      if c_ij = 0   (open chain / bridge)
         A_ij = min(1, c_ij/2) * A_face     if c_ij >= 1  (each triangle activates half the Kelvin face; cap at one face)
  R3  Calibration: P from He-4 alone (Option I: y=A, full Coulomb, R4 intact) -> P = 2.1044 MeV/sq-unit;
      A_open from D alone -> 0.3747 sq-units.  Nothing else is fitted.
  R4  Slingshot A*Y(A) with c' = 0.91864 (three-term-binding §7a).  Coulomb: alpha*hbar*c / r_ij over all proton pairs
      at rigid lattice distances.
  R5  Squeeze (Argon's guardrail 3): phi = (V_i/V_alpha)^gamma_V for nucleons with z_i >= 4, phi = 1 for z_i <= 3.
      Per-facet volume loss shared from the Kelvin-cell total (V/V0 = 0.868): dV_S = 0.00493, dV_H = 0.01281 per facet.
      gamma_V = 1 declared; NOT used for A <= 9 (all z <= 3 except the Be-9 bridge neutron, reported both ways).
  R6  Seating / orientation rule for the blinds: the ground state is the lattice placement of LOWEST energy among all
      non-overlapping placements with at least one inter-cluster contact; the full range is reported, not just the best.
Blinds declared: Be-8 unbound (neck is a bridge, c=0); Be-9 bound (bridge neutron closes triangles across the gap).
"""
import math, itertools, numpy as np

HC=197.3269804; AHC=1.439964547; ME=0.510998950; DM=1.2933323; RP=0.8409
G=DM/ME; CP=math.sqrt(1-1/G**2)
def Y(n): return ME*(G-1/math.sqrt(1-(CP/n)**2)) if n>1 else 0.0
A_S=1.0; A_H=2.598076; dV_S=0.132*A_S/(6*A_S+8*A_H); dV_H=0.132*A_H/(6*A_S+8*A_H)
BE={'D':2.224566,'T':8.481795,'He3':7.718043,'He4':28.29566,'Be8':56.4995,'Be9':58.1650,'Li6':31.9941,'Li7':39.2446,'Be7':37.6004}
ALPHA=np.array([[0,0,0],[2,0,0],[1,1,1],[1,-1,1]]); ALPHA_SP=['p','n','p','n']  # protons at (0,0,0),(1,1,1): 1 pp H-H pair inside

def contacts(pos):
    A=len(pos); C={}
    for i,j in itertools.combinations(range(A),2):
        d2=int(((pos[i]-pos[j])**2).sum())
        if d2==4: C[(i,j)]=('S',A_S)
        elif d2==3: C[(i,j)]=('H',A_H)
        elif d2<3: return None   # overlap
    return C
def energy(pos,sp,P,A_open,gamma_V=1.0,squeeze=True,verbose=False):
    pos=np.array(pos); A=len(pos); C=contacts(pos)
    if C is None: return None
    nb={i:set() for i in range(A)}
    for (i,j) in C: nb[i].add(j); nb[j].add(i)
    z={i:len(nb[i]) for i in range(A)}
    # per-nucleon squeeze
    phi={}
    Valpha=1-dV_S-2*dV_H
    for i in range(A):
        if squeeze and z[i]>=4:
            loss=sum(dV_S if C[tuple(sorted((i,j)))][0]=='S' else dV_H for j in nb[i])
            phi[i]=((1-loss)/Valpha)**gamma_V
        else: phi[i]=1.0
    face=0.0; rows=[]
    for (i,j),(kind,af) in C.items():
        c=len(nb[i]&nb[j])
        a=A_open if c==0 else min(1.0,c/2)*af
        a*=math.sqrt(phi[i]*phi[j])
        face+=a; rows.append((i,j,kind,c,round(a,3)))
    pr=[i for i in range(A) if sp[i]=='p']
    EC=sum(AHC/(math.sqrt(((pos[i]-pos[j])**2).sum())*RP) for i,j in itertools.combinations(pr,2))
    be=P*face+A*Y(A)-EC
    if verbose: return be,dict(face=face,EC=EC,sling=A*Y(A),rows=rows,z=z)
    return be

# --- calibration (R3) ---
Upp=AHC/(2*RP)
P=(BE['He4']+Upp-4*Y(4))/(2*A_S+4*A_H)
A_open=(BE['D']-2*Y(2))/P
print(f"calibration: P = {P:.4f} MeV/sq-unit (He-4), A_open = {A_open:.4f} sq-units (D)")

# --- A <= 4 ---
cases={'D':([[0,0,0],[2,0,0]],['p','n']),
       'T':([[0,0,0],[2,0,0],[1,1,1]],['p','n','n']),
       'He3':([[0,0,0],[2,0,0],[1,1,1]],['p','p','n']),
       'He4':(ALPHA.tolist(),ALPHA_SP)}
print(f"\n{'nuc':5s} {'pred':>8s} {'meas':>8s} {'miss%':>7s}  face(sq-u)  sling   Coul   per-edge (i,j,kind,c,area)")
for n,(pos,sp) in cases.items():
    be,p=energy(pos,sp,P,A_open,verbose=True)
    print(f"{n:5s} {be:8.3f} {BE[n]:8.3f} {100*(be/BE[n]-1):7.2f}  {p['face']:8.3f}  {p['sling']:6.3f} {p['EC']:6.3f}  {p['rows']}")

# --- Be-8 blind (R6): all placements of a second alpha with >=1 inter contact, no overlap ---
mats=[]
for perm in itertools.permutations(range(3)):
    for signs in itertools.product([1,-1],repeat=3):
        M=np.zeros((3,3),int)
        for r,pc in enumerate(perm): M[r,pc]=signs[r]
        mats.append(M)
def placements(base,base_sp,unit,unit_sp,rng=5):
    out={}
    for M in mats:
        rot=unit@M.T
        for sh in itertools.product(range(-rng,rng+1),repeat=3):
            u=rot+np.array(sh)
            if (u.sum(axis=1)%2!=u[0].sum()%2).any(): pass
            pos=np.vstack([base,u]); C=contacts(pos)
            if C is None: continue
            nb=len(base); inter=[k for k in C if k[0]<nb<=k[1]]
            if not inter: continue
            key=tuple(map(tuple,u.tolist()))
            out[key]=(pos,list(base_sp)+list(unit_sp),len(inter))
    return out
pl=placements(ALPHA,ALPHA_SP,ALPHA,ALPHA_SP)
res=[]
for key,(pos,sp,ninter) in pl.items():
    be,p=energy(pos,sp,P,A_open,verbose=True)
    neck=[r for r in p['rows'] if r[0]<4<=r[1]]
    res.append((be,ninter,neck,p,pos,sp))
res.sort(key=lambda r:-r[0])
print(f"\nBe-8 (alpha+alpha): {len(res)} placements. 2*BE(He4) = {2*BE['He4']:.3f}; measured BE = {BE['Be8']:.4f} (unbound by {2*BE['He4']-BE['Be8']:.3f} MeV)")
for be,ninter,neck,p,pos,sp in res[:5]:
    print(f"  BE={be:.3f}  vs 2a: {be-2*BE['He4']:+.3f} MeV  inter-contacts={ninter} neck edges={[(r[2],r[3],r[4]) for r in neck]}  EC={p['EC']:.3f}")
print(f"  range over all placements: {res[-1][0]-2*BE['He4']:+.3f} .. {res[0][0]-2*BE['He4']:+.3f} MeV relative to 2 alphas")
best8=res[0]

# --- Be-9 blind: add one neutron to the best Be-8 placements, any lattice site with >=1 contact ---
print(f"\nBe-9 (alpha+alpha+n): measured BE = {BE['Be9']:.3f}; Be-8 + n -> bound by {BE['Be9']-BE['Be8']:.3f} MeV above Be-8")
top=res[:8]
best9=None
for be8,ninter,neck,p8,pos8,sp8 in top:
    for sh in itertools.product(range(-4,5),repeat=3):
        s=np.array(sh)
        if len(set(s%2))!=1: continue
        pos=np.vstack([pos8,s]); sp=sp8+['n']
        C=contacts(pos)
        if C is None: continue
        if not any(8 in k for k in C): continue
        for sq in (False,True):
            be,p=energy(pos,sp,P,A_open,squeeze=sq,verbose=True)
            if best9 is None or be>best9[0][sq]:
                if best9 is None: best9=({False:-1e9,True:-1e9},None,None)
                best9[0][sq]=be;
                if not sq: best9=({**best9[0]},p,pos)
print(f"  best Be-9: BE = {best9[0][False]:.3f} (no squeeze) / {best9[0][True]:.3f} (squeeze gamma=1)  vs measured {BE['Be9']:.3f}; "
      f"relative to best Be-8 + free n: {best9[0][False]-best8[0]:+.3f} MeV (measured {BE['Be9']-BE['Be8']:+.3f})")
p=best9[1]; print("  neutron edges:",[(r[0],r[1],r[2],r[3],r[4]) for r in p['rows'] if 8 in (r[0],r[1])], " z:",p['z'])
