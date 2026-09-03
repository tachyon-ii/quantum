#!/usr/bin/env python3
"""
Energy on the honeycomb: B = k*H_active + kappa*T - Coulomb(shells)
  H_active = hex contacts joining a neutron and a proton (channels)
  T        = triangle-closed channel pairs: two channels sharing a nucleon
             whose far ends are themselves in contact (the lock's third side)
  Coulomb  = hollow-shell pp at lattice distances; scale: hex distance = 1.71 fm
Constants k, kappa calibrated on H2 + He4 ONLY. All else predicted.
Species assignment (which cells are protons) OPTIMISED per nucleus = "the permutes".
"""
import numpy as np, itertools
HEXV=set(itertools.product((0.5,-0.5),repeat=3))
SQV=set([(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])
SCALE=1.71/np.sqrt(3/4)   # fm per lattice unit so hex distance = 1.71 fm
ASH=0.945                  # fm shell radius for Coulomb smearing
ALPHA=1.439965
def contact(a,b):
    d=tuple(round(y-x,4) for x,y in zip(a,b))
    return 'H' if d in HEXV else ('S' if d in SQV else None)
def fib(n=128):
    i=np.arange(n)+0.5
    ph=np.arccos(1-2*i/n); th=np.pi*(1+5**0.5)*i
    return np.stack([np.sin(ph)*np.cos(th),np.sin(ph)*np.sin(th),np.cos(ph)],1)
_P=fib()
def U_shell(r):
    p1=_P*ASH; p2=_P*ASH+np.array([r,0,0])
    d=np.linalg.norm(p1[:,None,:]-p2[None,:,:],axis=2)
    return ALPHA*np.mean(1.0/d)
_UC={}
def Ur(r):
    key=round(r,3)
    if key not in _UC: _UC[key]=U_shell(r)
    return _UC[key]

def cluster_B(cells, Z, k, kappa, detail=False):
    n=len(cells)
    pairs={}
    for a,b in itertools.combinations(range(n),2):
        t=contact(cells[a],cells[b])
        if t: pairs[(a,b)]=t
    bestB=-1e9; bestinfo=None
    for prot in itertools.combinations(range(n),Z):
        pset=set(prot)
        Ha=[(a,b) for (a,b),t in pairs.items() if t=='H' and ((a in pset)!=(b in pset))]
        # triangle-closed channel pairs
        T=0
        for v in range(n):
            ch=[e for e in Ha if v in e]
            for e1,e2 in itertools.combinations(ch,2):
                u=[x for x in e1 if x!=v][0]; w=[x for x in e2 if x!=v][0]
                if (min(u,w),max(u,w)) in pairs: T+=1
        U=0.0
        for a,b in itertools.combinations(sorted(pset),2):
            r=np.linalg.norm(np.array(cells[a])-np.array(cells[b]))*SCALE
            U+=Ur(r)
        B=k*len(Ha)+kappa*T-U
        if B>bestB: bestB=B; bestinfo=(len(Ha),T,U,prot)
    if detail: return bestB,bestinfo
    return bestB

# geometries from the beam search (canonical instances)
K4=[(0.,0.,0.),(0.,0.,1.),(0.5,-0.5,0.5),(0.5,0.5,0.5)]
DIMER=[(0.,0.,0.),(0.5,0.5,0.5)]
TRI=[(0.,0.,0.),(0.,0.,1.),(0.5,0.5,0.5)]
def beam_best(N,Z,k,kappa,width=800):
    # beam-search clusters maximizing B itself
    core=(0.,0.,0.)
    beam={frozenset([core])}
    bestB=-1e9; bestcl=None
    for size in range(2,N+1):
        nxt=set()
        for cl in beam:
            for c in cl:
                for v in list(HEXV)+list(SQV):
                    nc=tuple(round(x+y,4) for x,y in zip(c,v))
                    if nc not in cl and max(abs(np.array(nc)))<=2.0:
                        nxt.add(cl|{nc})
        scored=[]
        for cl in nxt:
            if len(cl)!=size: continue
            b=cluster_B(sorted(cl),min(Z,size),k,kappa) if size==N else quick(cl)
            scored.append((b,cl))
        scored.sort(key=lambda x:-x[0])
        beam={cl for _,cl in scored[:width]}
        if size==N and scored:
            bestB,bestcl=scored[0]
    return bestB,sorted(bestcl)
def quick(cl):
    cl=sorted(cl); H=S=0
    for a,b in itertools.combinations(cl,2):
        t=contact(a,b)
        if t=='H':H+=1
        elif t=='S':S+=1
    return H*3+S
# calibrate k on H2, kappa on He4
k=2.2246/1.0
B4,info=cluster_B(K4,2,k,0,detail=True)
Ha4,T4,U4,_=info
kappa=(28.2957+U4-k*4)/4  # T=4 in K4
print(f"k={k:.4f} (H2), K4: H={Ha4} T={T4} U_pp={U4:.3f} -> kappa={kappa:.4f}")
print(f"\n{'nucleus':8} {'model':>8} {'exp':>8}  (H,T,U_pp)")
tests=[("H2",DIMER,1,2.2246),("H3",TRI,1,8.4818),("He3",TRI,2,7.7180),("He4",K4,2,28.2957)]
for name,g,Z,exp in tests:
    B,inf=cluster_B(g,Z,k,kappa,detail=True)
    print(f"{name:8} {B:8.3f} {exp:8.3f}  H={inf[0]} T={inf[1]} U={inf[2]:.3f}")
print("\nlattice-optimal larger nuclei (beam over geometry AND permutes):")
for name,N,Z,exp in [("Li5",5,3,"unbound"),("He5",5,2,"unbound"),
                     ("Li6",6,3,"31.994"),("Li7",7,3,"39.245"),("Be8",8,4,"56.500")]:
    B,cl=beam_best(N,Z,k,kappa)
    Bd,inf=cluster_B(cl,Z,k,kappa,detail=True)
    print(f"  {name:4}: B={B:8.3f}  exp={exp:>8}  H={inf[0]} T={inf[1]} U={inf[2]:.3f}")
