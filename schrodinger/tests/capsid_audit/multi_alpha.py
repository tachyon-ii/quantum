#!/usr/bin/env python3
"""
The alpha ladder on the honeycomb: Be8 placements, Be9 (bridge neutron),
C12 (triangle vs chain -> Hoyle geometry question), O16 if budget allows.
Exact degree<=2 channel optimisation (with branch&bound) over ALL hex edges,
so alphas may sacrifice internal channels to form bridges - no hand steering.
Constants k=2.2246, kappa=5.0316 (from H2/He4, unchanged). U_pp hollow shells.
Targets: Be9-(2a+n)=+1.573; C12-3a=+7.275; O16-4a=+14.437; Be8-2a=-0.092.
"""
import numpy as np, itertools, time
HEXV=set(itertools.product((0.5,-0.5),repeat=3))
SQV=set([(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])
SCALE=1.71/np.sqrt(0.75); ASH=0.945; ALPHA=1.439965
K=2.2246; KAPPA=5.0316
def contact(a,b):
    d=tuple(round(y-x,4) for x,y in zip(a,b))
    return 'H' if d in HEXV else ('S' if d in SQV else None)
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
K4=[(0.,0.,0.),(0.,0.,1.),(0.5,-0.5,0.5),(0.5,0.5,0.5)]  # sub0 pair then sub1 pair
def shift(cells,t): return [tuple(round(x+y,4) for x,y in zip(c,t)) for c in cells]
def B_exact(cells,pset,tlimit=25.0):
    n=len(cells); pairs={}
    for a,b in itertools.combinations(range(n),2):
        t=contact(cells[a],cells[b])
        if t: pairs[(a,b)]=t
    Ha=[(a,b) for (a,b),t in pairs.items() if t=='H' and ((a in pset)!=(b in pset))]
    # order edges to help pruning: internal-alpha edges first
    Ha.sort()
    best=[-1e9,None]; deg=[0]*n; t0=time.time()
    def T_of(sub):
        T=0
        for v in range(n):
            ch=[e for e in sub if v in e]
            for e1,e2 in itertools.combinations(ch,2):
                u=e1[0] if e1[1]==v else e1[1]; w=e2[0] if e2[1]==v else e2[1]
                if (min(u,w),max(u,w)) in pairs: T+=1
        return T
    def rec(i,sub,val_lb):
        if time.time()-t0>tlimit: return
        if i==len(Ha):
            val=K*len(sub)+KAPPA*T_of(sub)
            if val>best[0]: best[0]=val; best[1]=list(sub)
            return
        rem=len(Ha)-i
        if K*(len(sub)+rem)+KAPPA*2*(len(sub)+rem)<best[0]: return
        a,b=Ha[i]
        if deg[a]<2 and deg[b]<2:
            deg[a]+=1; deg[b]+=1
            rec(i+1,sub+[Ha[i]],val_lb)
            deg[a]-=1; deg[b]-=1
        rec(i+1,sub,val_lb)
    rec(0,[],0)
    U=sum(Ur(np.linalg.norm(np.array(cells[a])-np.array(cells[b]))*SCALE)
          for a,b in itertools.combinations(sorted(pset),2))
    return best[0]-U, len(best[1]) if best[1] else 0
# lattice translations that keep BCC validity: integer or all-half-integer vectors
def valid_ts(rmax=2.5):
    ts=[]
    for v in itertools.product(np.arange(-2,2.5,0.5),repeat=3):
        if all(abs(x-round(x))<1e-9 for x in v) or all(abs(x-np.floor(x)-0.5)<1e-9 for x in v):
            r=np.linalg.norm(v)
            if 0.5<r<=rmax: ts.append(tuple(round(x,4) for x in v))
    return ts
def touching(c1,c2):
    return sum(1 for a in c1 for b in c2 if contact(a,b))
# --- Be8: best two-alpha placement ---
print("Be8: two alphas, all lattice placements with contact:")
bestBe8=(-1e9,None)
seen=set()
for t in valid_ts():
    c2=shift(K4,t)
    if set(c2)&set(K4): continue
    nc=touching(K4,c2)
    if nc==0: continue
    key=tuple(sorted(set(K4)|set(c2)))
    if key in seen: continue
    seen.add(key)
    cells=K4+c2
    # proton choices: sub0 pair or sub1 pair per alpha (4 combos)
    for pa in ([0,1],[2,3]):
        for pb in ([4,5],[6,7]):
            B,nch=B_exact(cells,set(pa+pb),tlimit=8)
            if B>bestBe8[0]: bestBe8=(B,(t,pa,pb,nch,cells))
print(f"  best: B={bestBe8[0]:.3f}  vs 2a={2*28.2957:.3f}  margin={bestBe8[0]-56.5914:+.3f} (exp -0.092)  t={bestBe8[1][0]} channels={bestBe8[1][3]}")
# --- Be9: add one neutron to the best Be8 frame, all adjacent sites ---
t,pa,pb,_,cells8=bestBe8[1]
sites=set()
for c in cells8:
    for v in list(HEXV)+list(SQV):
        s=tuple(round(x+y,4) for x,y in zip(c,v))
        if s not in cells8: sites.add(s)
print(f"\nBe9: bridge-neutron over {len(sites)} candidate sites (exact channel re-optimisation, sacrifices allowed):")
bestBe9=(-1e9,None)
for s in sorted(sites):
    cells=cells8+[s]
    B,nch=B_exact(cells,set(pa+pb),tlimit=6)
    if B>bestBe9[0]: bestBe9=(B,(s,nch))
print(f"  best: B={bestBe9[0]:.3f}  vs 2a+n={56.5914:.3f}  margin={bestBe9[0]-56.5914:+.3f} (exp +1.573)  site={bestBe9[1][0]} channels={bestBe9[1][1]}")
