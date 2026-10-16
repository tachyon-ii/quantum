#!/usr/bin/env python3
"""build3b — Build 3 as declared FAILED Be-8 (+25.6 MeV, lowest-energy seating packs the two alphas into one lump).
Declared alternative, tested second, NOT fitted: R2' alpha saturation (James's posit, 16 Oct): a nucleon's first three
facets (its alpha tripod) are closure-eligible; every facet beyond the third gets only the open-chain patch A_open.
Everything else as build3_closure.py.  Reports D,T,He3,He4 (unchanged by construction), Be-8 range + lowest energy, Be-9."""
import math, itertools, numpy as np
import build3_closure as b
def energy_sat(pos,sp,P,A_open,verbose=False):
    pos=np.array(pos); A=len(pos); C=b.contacts(pos)
    if C is None: return None
    nb={i:set() for i in range(A)}
    for (i,j) in C: nb[i].add(j); nb[j].add(i)
    # rank each nucleon's facets by closure-eligible area; keep top 3 eligible
    elig={}
    for i in range(A):
        cand=[]
        for j in nb[i]:
            kind,af=C[tuple(sorted((i,j)))]; c=len(nb[i]&nb[j])
            cand.append((min(1.0,c/2)*af if c>0 else A_open, j))
        cand.sort(reverse=True); elig[i]=set(j for _,j in cand[:3])
    face=0; rows=[]
    for (i,j),(kind,af) in C.items():
        c=len(nb[i]&nb[j])
        full=min(1.0,c/2)*af if c>0 else A_open
        a=full if (j in elig[i] and i in elig[j]) else A_open
        face+=a; rows.append((i,j,kind,c,round(a,3)))
    pr=[i for i in range(A) if sp[i]=='p']
    EC=sum(b.AHC/(math.sqrt(((pos[i]-pos[j])**2).sum())*b.RP) for i,j in itertools.combinations(pr,2))
    be=P*face+A*b.Y(A)-EC
    return (be,dict(face=face,EC=EC,rows=rows)) if verbose else be
P,A_open=b.P,b.A_open
for n,(pos,sp) in b.cases.items():
    be,p=energy_sat(pos,sp,P,A_open,True); print(f"{n:5s} {be:8.3f} vs {b.BE[n]:8.3f}  {100*(be/b.BE[n]-1):+.2f}%")
pl=b.placements(b.ALPHA,b.ALPHA_SP,b.ALPHA,b.ALPHA_SP)
res=[]
for key,(pos,sp,ninter) in pl.items():
    be,p=energy_sat(pos,sp,P,A_open,True); res.append((be,ninter,p,pos,sp))
res.sort(key=lambda r:-r[0])
two=2*b.BE['He4']
print(f"\nBe-8 under alpha saturation: lowest-energy placement BE={res[0][0]:.3f} -> {res[0][0]-two:+.3f} MeV vs 2 alphas (measured -0.092); inter-contacts={res[0][1]}; EC={res[0][2]['EC']:.3f}")
print(f"  range: {res[-1][0]-two:+.3f} .. {res[0][0]-two:+.3f}")
# distribution by number of inter contacts
from collections import defaultdict
d=defaultdict(list)
for be,ninter,p,pos,sp in res: d[ninter].append(be-two)
for k in sorted(d): print(f"  {k} inter-contacts: best {max(d[k]):+.3f}, worst {min(d[k]):+.3f} (n={len(d[k])})")
# Be-9
best9=None
for be8,ninter,p8,pos8,sp8 in res[:12]:
    for sh in itertools.product(range(-4,5),repeat=3):
        s=np.array(sh)
        if len(set(s%2))!=1: continue
        pos=np.vstack([pos8,s]); sp=sp8+['n']; C=b.contacts(pos)
        if C is None or not any(8 in k for k in C): continue
        be,p=energy_sat(pos,sp,P,A_open,True)
        if best9 is None or be>best9[0]: best9=(be,p,pos,be8)
print(f"\nBe-9 under alpha saturation: best BE={best9[0]:.3f} vs measured {b.BE['Be9']:.3f} ({100*(best9[0]/b.BE['Be9']-1):+.2f}%); vs its Be-8 parent + n: {best9[0]-best9[3]:+.3f} MeV (measured +1.666)")
print("  neutron edges:",[r for r in best9[1]['rows'] if 8 in (r[0],r[1])])
