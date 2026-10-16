#!/usr/bin/env python3
"""
build4_stiffening.py — Build 4: closure (Build 3) + a per-contact stiffening penalty (Grace, 16 Oct 2026).

Declared before running:
  Closure rule, P, A_open, Coulomb, slingshot, lattice, seating rule R6 — exactly as build3_closure.py.
  Stiffening penalty per nucleon with z_i contacts (James's series; Argon's protocol as amended by Grace):
        pen(z_i) = D4 * sum_{k=4}^{z_i} r^(k-4),   r = pi^(1/3) = 1.4646 (declared form; the only choice),  pen = 0 for z <= 3.
  ONE new scale D4, set so that the lowest-energy lattice placement of THREE alphas reproduces BE(C-12) = 92.162 MeV
  (the alpha ladder's q = 2.425 MeV per alpha-alpha bond lives there).  Nothing is set on Be-8 or Be-9.
  Blinds, declared: Be-8 unbound (measured -0.092 MeV vs 2 alphas); Be-9 bound +1.666 MeV above Be-8 (58.165 total).
  Seating rule R6 for every nucleus: lowest energy over all non-overlapping placements with >= 1 inter-cluster contact
  (second and third alphas placed sequentially: the third alpha is searched over all placements touching the first two,
  for the best N2 placements of the second alpha).
Usage:  python3 build4_stiffening.py calib   (one bisection step per call; state in build4_state.json)
        python3 build4_stiffening.py blinds  (runs Be-8, Be-9 at the calibrated D4)
"""
import math, itertools, json, os, sys, numpy as np
import build3_closure as b

R_PI=math.pi**(1/3)
def pen(z,D4): return 0.0 if z<=3 else D4*sum(R_PI**(k-4) for k in range(4,z+1))

def energy(pos,sp,D4,verbose=False):
    pos=np.asarray(pos); A=len(pos)
    d2=((pos[:,None,:]-pos[None,:,:])**2).sum(axis=2)
    iu=np.triu_indices(A,1)
    if ((d2[iu]<3)).any(): return None
    S=(d2==4); H=(d2==3); adj=S|H
    z=adj.sum(axis=1)
    tri=(adj.astype(int)@adj.astype(int))  # common neighbours count
    face=0.0
    for i,j in zip(*iu):
        if not adj[i,j]: continue
        c=tri[i,j]; af=b.A_S if S[i,j] else b.A_H
        face+= b.A_open if c==0 else min(1.0,c/2)*af
    pr=[i for i in range(A) if sp[i]=='p']
    EC=sum(b.AHC/(math.sqrt(d2[i,j])*b.RP) for i,j in itertools.combinations(pr,2))
    P_=sum(pen(int(zi),D4) for zi in z)
    be=b.P*face+A*b.Y(A)-EC-P_
    return (be,dict(face=face,EC=EC,pen=P_,z=z.tolist(),sling=A*b.Y(A))) if verbose else be

# placements of a unit (alpha) relative to a base cluster: all 48 orientations x translations, >=1 inter contact, no overlap
MATS=[]
for perm in itertools.permutations(range(3)):
    for signs in itertools.product([1,-1],repeat=3):
        M=np.zeros((3,3),int)
        for r,pc in enumerate(perm): M[r,pc]=signs[r]
        MATS.append(M)
def placements(base,rng=6):
    base=np.asarray(base); out=[]
    seen=set()
    for M in MATS:
        rot=b.ALPHA@M.T
        for sh in itertools.product(range(-rng,rng+1),repeat=3):
            u=rot+np.array(sh)
            key=tuple(sorted(map(tuple,u.tolist())))
            if key in seen: continue
            d2=((base[:,None,:]-u[None,:,:])**2).sum(axis=2)
            if (d2<3).any() or not ((d2==3)|(d2==4)).any(): continue
            seen.add(key); out.append(u)
    return out

def best_two_alpha(D4,topn=10):
    res=[]
    for u in placements(b.ALPHA):
        pos=np.vstack([b.ALPHA,u]); e=energy(pos,b.ALPHA_SP*2,D4)
        if e is not None: res.append((e,pos))
    res.sort(key=lambda r:-r[0]); return res[:topn], len(res)

def best_three_alpha(D4,topn2=6):
    top2,_=best_two_alpha(D4,topn2); best=None
    for e2,pos2 in top2:
        for u in placements(pos2):
            # must touch BOTH alphas? R6 only needs >=1 inter contact; keep general
            pos=np.vstack([pos2,u]); e=energy(pos,b.ALPHA_SP*3,D4)
            if e is not None and (best is None or e>best[0]): best=(e,pos)
    return best

STATE='build4_state.json'
if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'calib'
    if mode=='calib':
        st=json.load(open(STATE)) if os.path.exists(STATE) else {'lo':0.0,'hi':6.0,'hist':[]}
        D4=0.5*(st['lo']+st['hi'])
        e,pos=best_three_alpha(D4)
        st['hist'].append([D4,e])
        if e>92.1617: st['lo']=D4
        else: st['hi']=D4
        json.dump(st,open(STATE,'w'))
        print(f"D4={D4:.4f}  best C-12 BE={e:.3f} (target 92.162)  bracket now [{st['lo']:.4f},{st['hi']:.4f}]")
    elif mode=='blinds':
        st=json.load(open(STATE)); D4=0.5*(st['lo']+st['hi'])
        print(f"calibrated D4 = {D4:.4f} MeV per contact-step at z=4 (r = pi^(1/3));  pen(5)={pen(5,D4):.2f}, pen(6)={pen(6,D4):.2f}, pen(7)={pen(7,D4):.2f}, pen(12)={pen(12,D4):.1f} MeV")
        for n,(pos,sp) in b.cases.items():
            e,p=energy(pos,sp,D4,True); print(f"  {n:4s} {e:8.3f} vs {b.BE[n]:8.3f} ({100*(e/b.BE[n]-1):+.2f}%)  z={p['z']}")
        top,ntot=best_two_alpha(D4,5); two=2*b.BE['He4']
        print(f"\nBe-8 blind: {ntot} placements; lowest energy BE={top[0][0]:.3f} -> {top[0][0]-two:+.3f} MeV vs 2 alphas (measured -0.092)")
        for e,pos in top[:3]:
            _,p=energy(pos,b.ALPHA_SP*2,D4,True); print(f"    BE={e:.3f}  face={p['face']:.3f} EC={p['EC']:.3f} pen={p['pen']:.3f} z={p['z']}")
        # Be-9: neutron added to each of the top-8 Be-8 placements, any site with >=1 contact
        best9=None
        for e8,pos8 in top[:8]:
            for sh in itertools.product(range(-5,6),repeat=3):
                s=np.array(sh)
                if len(set(s%2))!=1: continue
                pos=np.vstack([pos8,s]); e=energy(pos,b.ALPHA_SP*2+['n'],D4)
                if e is None: continue
                d2=((pos8-s)**2).sum(axis=1)
                if not ((d2==3)|(d2==4)).any(): continue
                if best9 is None or e>best9[0]: best9=(e,pos,e8)
        e9,pos9,e8=best9; _,p=energy(pos9,b.ALPHA_SP*2+['n'],D4,True)
        print(f"\nBe-9 blind: best BE={e9:.3f} vs measured 58.165 ({100*(e9/58.165-1):+.2f}%); above its Be-8 parent: {e9-e8:+.3f} MeV (measured +1.666); neutron z={p['z'][8]}, z list={p['z']}")
