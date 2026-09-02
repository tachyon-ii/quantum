#!/usr/bin/env python3
"""
Unified capsid model v3 (James's refinements, 2026-08-23):
  B = channels (k*H + kappa*T, capacity 2/nucleon, exact opt)
    + surface wells (Derjaguin annular-optimum: u_s per contact, GATED)
    - Coulomb (hollow shells)
Gates for the surface well ("cancellation of wave pattern"):
  G1: every contact gets the well
  G2: only N-P contacts (cancellation needs opposite phase)
  G3: only contacts that also carry an active channel
Calibrate (k,kappa,u_s) on H2 + He4 + Li6. PREDICT the rest.
Discriminators: He5 must be unbound; Be8 margin should approach -0.092.
"""
import numpy as np, itertools, time
exec(open('multi_alpha.py').read().split('# --- Be8')[0].replace('K=2.2246; KAPPA=5.0316',''))  # reuse geometry+Coulomb helpers
K4=[(0.,0.,0.),(0.,0.,1.),(0.5,-0.5,0.5),(0.5,0.5,0.5)]
TRI=[(0.,0.,0.),(0.,0.,1.),(0.5,0.5,0.5)]
DIMER=[(0.,0.,0.),(0.5,0.5,0.5)]
def B_full(cells,pset,k,kap,us,gate,tlimit=8.0):
    n=len(cells); pairs={}
    for a,b in itertools.combinations(range(n),2):
        t=contact(cells[a],cells[b])
        if t: pairs[(a,b)]=t
    Ha=[(a,b) for (a,b),t in pairs.items() if t=='H' and ((a in pset)!=(b in pset))]
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
    def rec(i,sub):
        if time.time()-t0>tlimit: return
        if i==len(Ha):
            val=k*len(sub)+kap*T_of(sub)
            if val>best[0]: best[0]=val; best[1]=list(sub)
            return
        rem=len(Ha)-i
        if k*(len(sub)+rem)+kap*2*(len(sub)+rem)<best[0]: return
        a,b=Ha[i]
        if deg[a]<2 and deg[b]<2:
            deg[a]+=1; deg[b]+=1; rec(i+1,sub+[Ha[i]]); deg[a]-=1; deg[b]-=1
        rec(i+1,sub)
    rec(0,[])
    chan=set(map(tuple,best[1])) if best[1] else set()
    S=0
    for (a,b),t in pairs.items():
        np_pair=(a in pset)!=(b in pset)
        if gate=='G1': S+=1
        elif gate=='G2' and np_pair: S+=1
        elif gate=='G3' and (a,b) in chan: S+=1
    U=sum(Ur(np.linalg.norm(np.array(cells[a])-np.array(cells[b]))*SCALE)
          for a,b in itertools.combinations(sorted(pset),2))
    return best[0]+us*S-U
def bestB(cellsets,psets,k,kap,us,gate):
    return max(B_full(c,p,k,kap,us,gate) for c,p in zip(cellsets,psets))
# geometries: Li6 = best K4+dimer lattice placement (search); same machinery for Li7/Be8/He5
def placements(base, group, maxr=2.5):
    outs=[]
    seen=set()
    for t in valid_ts(maxr):
        g2=shift(group,t)
        if set(g2)&set(base): continue
        if touching(base,g2)==0: continue
        key=tuple(sorted(set(base)|set(g2)))
        if key in seen: continue
        seen.add(key)
        outs.append(base+g2)
    return outs
PL6=placements(K4,DIMER); PL7=placements(K4,TRI); PL8=placements(K4,K4); PL5=placements(K4,[(0.,0.,0.)])
print(f"placements: Li6 {len(PL6)}, Li7 {len(PL7)}, Be8 {len(PL8)}, A5 {len(PL5)}")
def nucleus_best(pls, Zextra_opts, k,kap,us,gate,tl=4.0):
    best=-1e9
    for cells in pls:
        n=len(cells)
        for pa in ([0,1],[2,3]):
            for pext in Zextra_opts(n):
                B=B_full(cells,set(pa)|set(pext),k,kap,us,gate,tlimit=tl)
                if B>best: best=B
    return best
from scipy.optimize import fsolve
for gate in ('G2','G3','G1'):
    def calib(x):
        k,kap,us=x
        b2=B_full(DIMER,{0},k,kap,us,gate)
        b4=max(B_full(K4,{0,1},k,kap,us,gate),B_full(K4,{2,3},k,kap,us,gate))
        b6=nucleus_best(PL6, lambda n:[ [n-2],[n-1] ], k,kap,us,gate,tl=2.0)
        return [b2-2.2246, b4-28.2957, b6-31.9941]
    try:
        (k,kap,us),info,ok,msg=fsolve(calib,[1.5,5.0,0.7],full_output=True)
        if ok!=1: print(f"{gate}: calibration failed"); continue
        b3 =B_full(TRI,{2},k,kap,us,gate)          # H3: proton = the lone sublattice-1 cell? try both
        b3 =max(b3, B_full(TRI,{0},k,kap,us,gate))
        bh3=max(B_full(TRI,{0,1},k,kap,us,gate), B_full(TRI,{0,2},k,kap,us,gate))
        b7=nucleus_best(PL7, lambda n:[ [n-3],[n-2],[n-1] ], k,kap,us,gate,tl=2.0)
        b8=nucleus_best(PL8, lambda n:[ [n-4,n-3],[n-2,n-1] ], k,kap,us,gate,tl=3.0)
        b5n=nucleus_best(PL5, lambda n:[ [] ], k,kap,us,gate,tl=2.0)
        b5p=nucleus_best(PL5, lambda n:[ [n-1] ], k,kap,us,gate,tl=2.0)
        print(f"\n[{gate}] k={k:.3f} kappa={kap:.3f} u_s={us:.3f}")
        print(f"  H3  {b3:8.3f} (8.482)   He3 {bh3:8.3f} (7.718)   split {b3-bh3:+.3f} (0.764)")
        print(f"  Li7 {b7:8.3f} (39.245)  Be8-2a {b8-56.5914:+.3f} (-0.092)")
        print(f"  He5-a {b5n-28.2957:+.3f} (must be <0; exp -0.89)   Li5-a {b5p-28.2957:+.3f} (exp -1.97)")
    except Exception as e:
        print(f"{gate}: error {e}")
