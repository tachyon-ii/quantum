#!/usr/bin/env python3
"""Permutes of octahedra, staged. Facts then beam-search for best clusters."""
import numpy as np, itertools
HEX=set(itertools.product((0.5,-0.5),repeat=3))
SQ=set([(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])
def contact(a,b):
    d=tuple(round(y-x,4) for x,y in zip(a,b))
    return 'H' if d in HEX else ('S' if d in SQ else None)
def sub(c): return 0 if abs(c[0]-round(c[0]))<1e-9 else 1
# ball of BCC cells
cells=[]
for base in ('int','half'):
    rng=np.arange(-2,2.1,1.0) if base=='int' else np.arange(-1.5,1.6,1.0)
    for i in rng:
        for j in rng:
            for k in rng: cells.append((round(i,1),round(j,1),round(k,1)))
cells=sorted(set(cells))
print(f"cells in ball: {len(cells)}")
print("hex crosses sublattices:", all(sub((0,0,0))!=sub(tuple(v)) for v in HEX))
print("square stays on sublattice:", all(sub((0,0,0))==sub(tuple(v)) for v in SQ))
# max clique via edge extension (cheap here)
adj={c:{} for c in cells}
for a,b in itertools.combinations(cells,2):
    t=contact(a,b)
    if t: adj[a][b]=t; adj[b][a]=t
best=[]
def extend(cl,cand):
    global best
    if len(cl)>len(best): best=list(cl)
    for c in list(cand):
        newc=[x for x in cand if x>c and x in adj[c]]
        extend(cl+[c],newc)
core=(0.0,0.0,0.0)
extend([core],[c for c in adj[core] if c>core])
H=sum(1 for x,y in itertools.combinations(best,2) if adj[x].get(y)=='H')
S=sum(1 for x,y in itertools.combinations(best,2) if adj[x].get(y)=='S')
print(f"max clique containing origin: size={len(best)}  H={H} S={S}  cells={best}")
print("  sublattice split:", [sub(c) for c in best])
dists=sorted(round(np.linalg.norm(np.array(a)-np.array(b)),4) for a,b in itertools.combinations(best,2))
print("  pair distances:",dists)
# beam search: best (maxH then maxS) connected cluster of each size
from heapq import nlargest
def score(cl):
    Hc=Sc=0
    for a,b in itertools.combinations(cl,2):
        t=adj[a].get(b)
        if t=='H':Hc+=1
        elif t=='S':Sc+=1
    return Hc,Sc
beam={frozenset([core])}
print("\nbest connected clusters by (H,S):")
for n in range(2,9):
    nxt=set()
    for cl in beam:
        cand=set()
        for c in cl: cand.update(adj[c].keys())
        cand-=cl
        for c in cand: nxt.add(cl|{c})
    scored=sorted(((score(cl),cl) for cl in nxt),reverse=True)
    keep=[cl for _,cl in scored[:3000]]
    beam=set(keep)
    (Hb,Sb),clb=scored[0]
    subs=[sub(c) for c in clb]
    print(f"  N={n}: H={Hb} S={Sb}  sublattice {subs.count(0)}+{subs.count(1)}")
