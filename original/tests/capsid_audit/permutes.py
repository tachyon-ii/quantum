#!/usr/bin/env python3
"""
Permutes of octahedra: the TO honeycomb as a bonding graph.
Cells of the bitruncated cubic honeycomb = BCC lattice points.
  HEX contact  (pore/channel-capable): displacement (+-1/2,+-1/2,+-1/2) - 8 per cell
  SQUARE contact (frame-to-frame):     displacement (+-1,0,0) type      - 6 per cell
Facts to establish computationally:
  1. Hex contacts ONLY connect the two BCC sublattices (corner vs centre).
  2. Maximum clique of the contact graph, and its H/S composition.
  3. Whether the max clique is the vertex figure (4 cells round a vertex).
Then: enumerate small connected clusters and their best H/S counts per size.
"""
import numpy as np, itertools
from fractions import Fraction

HEX=[np.array(v) for v in itertools.product((0.5,-0.5),repeat=3)]
SQ =[np.array(v) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]

def sub(c): return int(2*c[0])%2  # 0 = corner lattice, 1 = centre lattice (x half-integer)

def contact(a,b):
    d=tuple(np.round(np.array(b)-np.array(a),6))
    for v in HEX:
        if d==tuple(v): return 'H'
    for v in SQ:
        if d==tuple(v): return 'S'
    return None

# 1. hex crosses sublattices?
c0=(0,0,0)
print("hex neighbours of corner cell are all centre-sublattice:",
      all(sub(np.array(c0)+v)==1 for v in HEX))
print("square neighbours stay on own sublattice:",
      all(sub(np.array(c0)+v)==0 for v in SQ))

# 2. max clique: search around origin (radius-2 ball is ample for cliques)
cells=set()
for i in np.arange(-2,2.5,0.5):
    for j in np.arange(-2,2.5,0.5):
        for k in np.arange(-2,2.5,0.5):
            c=(i,j,k)
            f=[x*2%1==0 for x in c]
            if all(f) and (all(x*2%2==0 for x in (2*i,2*j,2*k)) or True):
                # valid BCC point: all integer or all half-integer
                ints=all(abs(x-round(x))<1e-9 for x in c)
                halves=all(abs(x-np.floor(x)-0.5)<1e-9 for x in c)
                if ints or halves: cells.add(c)
cells=sorted(cells)
idx={c:n for n,c in enumerate(cells)}
adj={c:[] for c in cells}
for a in cells:
    for b in cells:
        if a<b:
            t=contact(a,b)
            if t: adj[a].append((b,t)); adj[b].append((a,t))
# greedy clique extension from every edge
best=[]
def extend(cl):
    global best
    if len(cl)>len(best): best=list(cl)
    last=cl[-1]
    for b,_ in adj[last]:
        if b>last and all(contact(x,b) for x in cl):
            extend(cl+[b])
for a in cells:
    for b,_ in adj[a]:
        if b>a: extend([a,b])
print(f"\nmaximum clique size = {len(best)}: {best}")
Hn=sum(1 for x,y in itertools.combinations(best,2) if contact(x,y)=='H')
Sn=sum(1 for x,y in itertools.combinations(best,2) if contact(x,y)=='S')
subs=[sub(np.array(c)) for c in best]
print(f"composition: {Hn} hex + {Sn} square contacts; sublattice split {subs.count(0)}+{subs.count(1)}")

# 3. vertex figure check: cells of the honeycomb around one honeycomb vertex.
# A vertex of the bitruncated cubic honeycomb sits at points like (1/4,1/4,... )?
# easier: verify that the 4-clique cells share a common point: intersection of the 4 TOs.
# TO cell around centre c: |x-c|_inf-ish region; check centroid of clique
cl=np.array([np.array(c) for c in best],float)
print("clique centroid:", cl.mean(0), " pairwise distances:",
      sorted(set(round(np.linalg.norm(a-b),4) for a,b in itertools.combinations(cl,2))))

# 4. best (max-H) connected clusters, sizes 2..8, exhaustive over lattice ball with pruning
from functools import lru_cache
def neighbours(c):
    out=[]
    for v in HEX+SQ:
        n=tuple(np.round(np.array(c)+v,6))
        if n in idx: out.append(n)
    return out
NB={c:neighbours(c) for c in cells}
def canon(cluster):
    # translate to min; use frozenset of relative coords (no rotations - fine for counting best)
    m=np.min([np.array(c) for c in cluster],axis=0)
    return frozenset(tuple(np.round(np.array(c)-m,6)) for c in cluster)
results={}
seen=set()
def grow(cluster):
    n=len(cluster)
    key=canon(cluster)
    if key in seen: return
    seen.add(key)
    H=S=0
    for a,b in itertools.combinations(cluster,2):
        t=contact(a,b)
        if t=='H': H+=1
        elif t=='S': S+=1
    cur=results.get(n,(-1,-1,None))
    if (H,S)>cur[:2]: results[n]=(H,S,sorted(cluster))
    if n>=8: return
    cand=set()
    for c in cluster: cand.update(NB[c])
    cand-=set(cluster)
    for c in sorted(cand):
        # prune: only grow near origin ball
        if max(abs(np.array(c)))<=1.5: grow(cluster+[c])
grow([(0.0,0.0,0.0)])
print("\nbest (H,S) per cluster size (max hex first):")
for n in sorted(results):
    H,S,cl=results[n]
    print(f"  N={n}: H={H} S={S}")
