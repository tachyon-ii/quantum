# Grace 16 Oct — Be-8 as two he4_cross alphas on the BCC lattice, fixed species (protons at (0,0,0),(1,1,1)), all 48 orientations x translations: inter-alpha pp Coulomb by contact type. Shows the result is orientation-dependent (1.29-3.69 MeV).
import numpy as np, itertools, math
a_hc=1.439964547; Rp=0.8409
t=np.array([[0,0,0],[2,0,0],[1,1,1],[1,-1,1]],float); prot=[0,2]  # protons at (0,0,0),(1,1,1)
# cubic point group rotations (24) as signed permutation matrices with det +1, plus improper (48) — use all 48 (mirror image alphas allowed)
mats=[]
for perm in itertools.permutations(range(3)):
    for signs in itertools.product([1,-1],repeat=3):
        M=np.zeros((3,3)); 
        for i,p in enumerate(perm): M[i,p]=signs[i]
        mats.append(M)
cen=t.mean(axis=0)
results={}
for M in mats:
    t2r=(t-cen)@M.T+cen
    for dx,dy,dz in itertools.product(range(-5,6),repeat=3):
        t2=t2r+np.array([dx,dy,dz])
        d=np.array([[np.linalg.norm(p-q) for q in t2] for p in t])
        m=d.min()
        if abs(m-2)<1e-6 or abs(m-math.sqrt(3))<1e-6:
            ncont=int(np.sum(np.abs(d-m)<1e-6))
            E=sum(a_hc/(d[i,j]*Rp) for i in prot for j in prot)
            key=(round(m,3),ncont); results.setdefault(key,[]).append(round(E,4))
for k,v in sorted(results.items()):
    print("min dist %.3f units, %d contacts: inter-alpha pp Coulomb range %.3f .. %.3f MeV"%(k[0],k[1],min(v),max(v)))
