#!/usr/bin/env python3
"""
Capacity-constrained honeycomb energetics.
NEW LAW (from the theory's own primitives): one trapped wave per lepton;
a lemniscate has two lobes => each nucleon carries at most 2 active channels.
Channel graph is therefore a union of paths/cycles; He4 = the bipartite
4-cycle inside the max clique: capacity-saturated AND contact-complete.
B = k*H_active + kappa*T - U_pp(shells);  k from H2, kappa from He4.
T = channel pairs sharing a nucleon whose far ends are in contact.
"""
import numpy as np, itertools
HEXV=set(itertools.product((0.5,-0.5),repeat=3))
SQV=set([(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])
SCALE=1.71/np.sqrt(0.75); ASH=0.945; ALPHA=1.439965
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

def best_channels(Ha, pairs, n, k, kappa):
    """max over degree<=2 subsets of Ha of k*|E| + kappa*T; exact recursive."""
    best=[-1e9,None]
    deg=[0]*n
    def T_of(sub):
        T=0
        for v in range(n):
            ch=[e for e in sub if v in e]
            for e1,e2 in itertools.combinations(ch,2):
                u=[x for x in e1 if x!=v][0]; w=[x for x in e2 if x!=v][0]
                if (min(u,w),max(u,w)) in pairs: T+=1
        return T
    def rec(i, sub):
        if i==len(Ha):
            val=k*len(sub)+kappa*T_of(sub)
            if val>best[0]: best[0]=val; best[1]=list(sub)
            return
        # bound: remaining edges all addable
        rem=len(Ha)-i
        if k*(len(sub)+rem)+kappa*(2*(len(sub)+rem))<best[0]: return
        a,b=Ha[i]
        if deg[a]<2 and deg[b]<2:
            deg[a]+=1; deg[b]+=1
            rec(i+1, sub+[Ha[i]])
            deg[a]-=1; deg[b]-=1
        rec(i+1, sub)
    rec(0,[])
    return best

def cluster_B(cells, Z, k, kappa, detail=False):
    n=len(cells); pairs={}
    for a,b in itertools.combinations(range(n),2):
        t=contact(cells[a],cells[b])
        if t: pairs[(a,b)]=t
    bestB=-1e9; bi=None
    for prot in itertools.combinations(range(n),Z):
        pset=set(prot)
        Ha=[(a,b) for (a,b),t in pairs.items() if t=='H' and ((a in pset)!=(b in pset))]
        val,sub=best_channels(Ha,pairs,n,k,kappa)
        U=sum(Ur(np.linalg.norm(np.array(cells[a])-np.array(cells[b]))*SCALE)
              for a,b in itertools.combinations(sorted(pset),2))
        B=val-U
        if B>bestB: bestB=B; bi=(len(sub) if sub else 0, sub, U, prot)
    return (bestB,bi) if detail else bestB

K4=[(0.,0.,0.),(0.,0.,1.),(0.5,-0.5,0.5),(0.5,0.5,0.5)]
DIMER=[(0.,0.,0.),(0.5,0.5,0.5)]
TRI=[(0.,0.,0.),(0.,0.,1.),(0.5,0.5,0.5)]
k=2.2246
B4,bi=cluster_B(K4,2,k,0.0,detail=True)
U4=bi[2]
# kappa from He4 with T=4 (vertex-shared closed pairs in C4)
kappa=(28.2957+U4-4*k)/4
print(f"k={k}  U_pp(He4)={U4:.3f}  kappa={kappa:.4f}")
for name,g,Z,exp in [("H2",DIMER,1,2.2246),("H3",TRI,1,8.4818),("He3",TRI,2,7.7180),("He4",K4,2,28.2957)]:
    B,bi=cluster_B(g,Z,k,kappa,detail=True)
    print(f"  {name:4}: {B:8.3f}  exp {exp:8.3f}   channels={bi[0]} U={bi[2]:.3f}")
# larger: beam over geometry with heuristic, exact scoring on top candidates
def beam_best(N,Z,width=400,report=1):
    core=(0.,0.,0.)
    beam={frozenset([core])}
    for size in range(2,N+1):
        nxt=set()
        for cl in beam:
            for c in cl:
                for v in list(HEXV)+list(SQV):
                    nc=tuple(round(x+y,4) for x,y in zip(c,v))
                    if nc not in cl and max(abs(np.array(nc)))<=2.0: nxt.add(cl|{nc})
        def quick(cl):
            cl=sorted(cl); H=S=0
            for a,b in itertools.combinations(cl,2):
                t=contact(a,b)
                if t=='H':H+=1
                elif t=='S':S+=1
            return 3*H+S
        scored=sorted(((quick(cl),cl) for cl in nxt if len(cl)==size),key=lambda x:-x[0])
        beam={cl for _,cl in scored[:width]}
    top=sorted(beam,key=lambda cl:-len(cl))
    bestB=-1e9; bcl=None
    for cl in list(top)[:60]:
        B=cluster_B(sorted(cl),Z,k,kappa)
        if B>bestB: bestB=B; bcl=sorted(cl)
    return bestB,bcl
print("\ncapacity-constrained predictions:")
res={}
for name,N,Z,exp in [("Li5",5,3,None),("He5",5,2,None),("Li6",6,3,31.994),("Li7",7,3,39.245),("Be8",8,4,56.500)]:
    B,cl=beam_best(N,Z)
    res[name]=B
    tag={"Li5":"exp UNBOUND","He5":"exp UNBOUND"}.get(name,f"exp {exp}")
    print(f"  {name:4}: B={B:8.3f}   {tag}")
print(f"\n  Li5 - He4 = {res['Li5']-28.2957:+.3f} (exp -1.97, must be <0)")
print(f"  He5 - He4 = {res['He5']-28.2957:+.3f} (exp -0.89, must be <0)")
print(f"  Be8 - 2He4 = {res['Be8']-2*28.2957:+.3f} (exp -0.092)")
