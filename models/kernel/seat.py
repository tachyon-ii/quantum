"""kernel/seat.py — rung-0 seatings: connected clusters on the BCC lattice (Build 3 convention), all species assignments,
per-contact descriptors (species pair, contact type S/H, triangles c, coordinations z_i,z_j). Grace (Claude Fable 5.1), 19 Oct 2026.
Lattice: integer triples with all coordinates of equal parity; unit = R_p. Contacts: d^2=3 (H, 1.456 fm) and d^2=4 (S, 1.682 fm)."""
import itertools,numpy as np,pickle,os,sys
from data import AHC,RP,Y
HERE=os.path.dirname(os.path.abspath(__file__))
NB=[np.array(v) for v in itertools.product([-1,1],repeat=3)]+[np.array(v) for v in [(2,0,0),(-2,0,0),(0,2,0),(0,-2,0),(0,0,2),(0,0,-2)]]
MATS=[]
for perm in itertools.permutations(range(3)):
    for signs in itertools.product([1,-1],repeat=3):
        M=np.zeros((3,3),int)
        for r,pc in enumerate(perm): M[r,pc]=signs[r]
        MATS.append(M)
def canon(sites):
    S=np.array(sorted(sites)); best=None
    for M in MATS:
        T=S@M.T; T=T-T.min(axis=0); 
        # keep lattice parity consistent: shift so that the first site has even coords (translate by (1,1,1) if odd)
        if (T[0]%2).any(): pass
        key=tuple(map(tuple,sorted(map(tuple,T.tolist()))))
        if best is None or key<best: best=key
    return best
def clusters(A):
    """all connected clusters of A sites up to cubic symmetry + translation."""
    cur={canon([(0,0,0)])}
    for a in range(2,A+1):
        nxt=set()
        for c in cur:
            S=set(c)
            for s in c:
                for d in NB:
                    t=tuple(np.array(s)+d)
                    if t in S: continue
                    nxt.add(canon(list(S)+[t]))
        cur=nxt
    return [np.array(c) for c in cur]
def contacts(P):
    A=len(P); C=[]
    for i,j in itertools.combinations(range(A),2):
        d2=int(((P[i]-P[j])**2).sum())
        if d2==3: C.append((i,j,'H'))
        elif d2==4: C.append((i,j,'S'))
    return C
def features(P,sp):
    """descriptor counts for one seating. Returns dict desc->count, Coulomb (MeV), connected flag, triplet-gate flag."""
    A=len(P); C=contacts(P); nb={i:set() for i in range(A)}
    for i,j,t in C: nb[i].add(j); nb[j].add(i)
    z={i:len(nb[i]) for i in range(A)}
    feats={}
    for i,j,t in C:
        c=len(nb[i]&nb[j]); pair='np' if sp[i]!=sp[j] else ('pp' if sp[i]=='p' else 'nn')
        key=(pair,t,min(c,3),min(z[i],z[j],5),min(max(z[i],z[j]),5))
        feats[key]=feats.get(key,0)+1
    pr=[i for i in range(A) if sp[i]=='p']
    coul=sum(AHC/(np.sqrt(((P[i]-P[j])**2).sum())*RP) for i,j in itertools.combinations(pr,2))
    # connected?
    seen={0}; st=[0]
    while st:
        u=st.pop()
        for v in nb[u]:
            if v not in seen: seen.add(v); st.append(v)
    connected=len(seen)==A
    triplet=all(any(sp[j]!=sp[i] for j in nb[i]) for i in range(A))
    return feats,coul,connected,triplet
def seatings(A,Z):
    out=[]
    for P in clusters(A):
        for pr in itertools.combinations(range(A),Z):
            sp=['p' if i in pr else 'n' for i in range(A)]
            f,coul,conn,trip=features(P,sp)
            out.append(dict(P=P,sp=sp,feats=f,coul=coul,connected=conn,triplet=trip))
    return out
if __name__=='__main__':
    import time
    for A in range(1,7):
        t=time.time(); cl=clusters(A); print(f'A={A}: {len(cl)} clusters ({time.time()-t:.1f}s)')
