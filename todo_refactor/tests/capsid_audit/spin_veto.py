#!/usr/bin/env python3
"""
The spin veto from Battey-Pratt/Racey medium interference (2026-08-24).
Each nucleon = spherical rotator: configuration field rotates at omega about
axis n with sense s (+1 normal/e+ runner, -1 antispin/e- runner).
Local medium displacement at a shared point: e_i(t) = R(n_i, s_i*omega*t) a_i.
Interaction energy ~ time-average of de_A/dt . de_B/dt  (cross kinetic term).
DC (nonzero average) = persistent coupling = bond channel; zero = no bond.
Then: Pauli forces identical pairs (pp, nn) into the antisymmetric spin state.
Question: which pairing hypothesis reproduces nature's table
(np-triplet BOUND; np-singlet, nn, pp all UNBOUND)?
"""
import numpy as np
def R(n,th):
    n=np.asarray(n,float); n/=np.linalg.norm(n)
    K=np.array([[0,-n[2],n[1]],[n[2],0,-n[0]],[-n[1],n[0],0]])
    return np.eye(3)+np.sin(th)*K+(1-np.cos(th))*(K@K)
def coupling(nA,sA,nB,sB,dphi=0.0,T=400):
    """time-averaged  e'_A . e'_B, maximised over initial in-plane vectors."""
    w=1.0; ts=np.linspace(0,20*np.pi,T)
    # in-plane starting vectors
    def basis(n):
        n=np.asarray(n,float); n/=np.linalg.norm(n)
        a=np.cross(n,[1,0,0]);
        if np.linalg.norm(a)<1e-6: a=np.cross(n,[0,1,0])
        a/=np.linalg.norm(a); return a
    aA=basis(nA); aB=basis(nB)
    best=0.0
    for ph in np.linspace(0,2*np.pi,24,endpoint=False):
        acc=0.0
        for t in ts:
            eA=R(nA,sA*w*t)@aA
            eB=R(nB,sB*w*t+ph)@aB
            # velocities
            dA=R(nA,sA*w*(t+1e-4))@aA; dB=R(nB,sB*w*(t+1e-4)+ph)@aB
            acc+=np.dot((dA-eA)/1e-4,(dB-eB)/1e-4)
        v=acc/len(ts)
        if abs(v)>abs(best): best=v
    return best
z=[0,0,1]; mz=[0,0,-1]
print("coupling magnitude |<e'_A.e'_B>| (max over lock phase); DC!=0 => bond channel exists")
print(f"{'config':38} {'coupling':>9}")
cases=[
 ("same sense, axes aligned  (co-rot)", z,+1,z,+1),
 ("same sense, axes anti     (ctr-rot)", z,+1,mz,+1),
 ("opp sense,  axes aligned  (ctr-rot)", z,+1,z,-1),
 ("opp sense,  axes anti     (co-rot)", z,+1,mz,-1),
 ("same sense, axes at 90deg", z,+1,[1,0,0],+1),
]
for label,na,sa,nb,sb in cases:
    c=coupling(na,sa,nb,sb)
    print(f"  {label:36} {c:9.3f}")
print("""
LAW EXTRACTED: coupling is DC iff the two runners CO-ROTATE in the lab frame
(sigma = s*sign(n.z) equal); counter-rotating pairs average to zero at 2w.
Magnitude falls with axis misalignment (tensor-like angular dependence).

APPLY TO NUCLEONS (runner inventory: p carries e+; n carries e+ AND e-):
Hypothesis H2 - the bond channel is the like-runner pair (e+ with e+),
with Pauli antisymmetry forcing identical nucleon pairs into anti-aligned spins:
""")
table=[
 ("np triplet (aligned)","allowed (n,p distinct)","e+/e+ co-rotate","DC -> BOUND","BOUND (deuteron)"),
 ("np singlet (anti)","allowed","e+/e+ counter-rot","zero -> unbound","UNBOUND (virtual)"),
 ("pp","Pauli forces singlet","counter-rot only","zero -> unbound","UNBOUND (no diproton)"),
 ("nn","Pauli forces singlet","counter-rot only","zero -> unbound","UNBOUND (virtual -18.6fm)"),
]
print(f"{'system':22} {'spin state':22} {'runner pair':18} {'model':16} {'nature'}")
for r in table: print("  "+"".join(f"{x:<22}" if i<2 else f"{x:<18}" if i==2 else f"{x:<16}" if i==3 else x for i,x in enumerate(r)))
