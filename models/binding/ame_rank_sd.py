#!/usr/bin/env python3
"""ame_rank_sd.py — what the raw data says about directional scatter (Grace, 17 Oct 2026).
Input: data/ame2020-mass-table.txt (AME2020, measured entries only; # = extrapolated, skipped).
Outputs: 5-term liquid-drop fit (A>=16) and its residual SD by A-bin, by class, by distance to magic;
         odd-even stagger Delta3_n by N relative to magic.  Nothing else is fitted.  See review/2026-10-18/SPEC-peel-and-roll.md §3.
"""
import numpy as np, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rows=[]
for line in open('../../data/ame2020-mass-table.txt',encoding='latin-1'):
    if len(line)<80 or not line[1:4].strip().lstrip('-').isdigit(): continue
    try:
        N=int(line[4:9]); Z=int(line[9:14]); A=int(line[14:19]); el=line[20:23].strip()
        be=line[54:68]   # BE/A keV
        if '#' in be: continue
        bea=float(be); 
    except Exception as e: continue
    rows.append((N,Z,A,bea*A/1000.0))
d=np.array(rows); print("measured nuclides:",len(d))
N,Z,A,B=d.T
# 1. liquid drop fit, A>=16
m=A>=16
delta=np.where((N%2==0)&(Z%2==0),1,np.where((N%2==1)&(Z%2==1),-1,0))
X=np.c_[A, -A**(2/3), -Z*(Z-1)/A**(1/3), -(N-Z)**2/A, delta/np.sqrt(A)]
coef,*_=np.linalg.lstsq(X[m],B[m],rcond=None)
res=B-X@coef
print("LD coef a_v a_s a_c a_a a_p:",np.round(coef,3))
print(f"residual SD A>=16: {res[m].std():.3f} MeV  (n={m.sum()})")
magic=np.array([2,8,20,28,50,82,126])
dist=lambda x: np.min(np.abs(x[:,None]-magic[None,:]),axis=1)
dn=dist(N); dz=dist(Z)
for lo,hi in [(16,40),(40,80),(80,140),(140,200),(200,300)]:
    mm=m&(A>=lo)&(A<hi); 
    print(f"  A {lo:3d}-{hi:3d}: SD {res[mm].std():6.3f} MeV  n={mm.sum():4d}   SD/A^(2/3)={res[mm].std()/((lo+hi)/2)**(2/3):.3f}  SD/A^(1/2)={res[mm].std()/((lo+hi)/2)**0.5:.3f}")
# class split A>=16
ee=(N%2==0)&(Z%2==0); oo=(N%2==1)&(Z%2==1); oa=~ee&~oo; lad=ee&(N==Z)&(A%4==0)
for name,sel in [('alpha ladder N=Z 4n',lad),('even-even (other)',ee&~lad),('odd-A',oa),('odd-odd',oo)]:
    mm=m&sel; print(f"  {name:22s} SD {res[mm].std():6.3f}  mean {res[mm].mean():+6.3f}  n={mm.sum()}")
# by distance to magic (either N or Z)
dmin=np.minimum(dn,dz)
for k in range(0,7):
    mm=m&(dmin==k); print(f"  dist-to-magic {k}: residual SD {res[mm].std():6.3f} mean {res[mm].mean():+6.3f} n={mm.sum()}")
mm=m&(dmin>=7); print(f"  dist>=7: SD {res[mm].std():6.3f} mean {res[mm].mean():+6.3f} n={mm.sum()}")
# 2. odd-even stagger Delta3_n at fixed Z, by N distance from magic
Bm={(int(n),int(z)):b for n,z,b in zip(N,Z,B)}
D3={}
for (n,z),b in Bm.items():
    if (n-1,z) in Bm and (n+1,z) in Bm and n+z>=16:
        D3[(n,z)]=(-1)**n*0.5*(Bm[(n+1,z)]-2*b+Bm[(n-1,z)])
k=np.array(list(D3.keys())); v=np.array(list(D3.values()))
nn=k[:,0]; A2=k.sum(axis=1); sign=np.where(nn%2==0,1,-1)
print("\nodd-even stagger Delta3_n (MeV), scaled by sqrt(A)/12 -> dimensionless; by N relative to magic:")
rel=np.array([ (n-magic[np.argmin(np.abs(n-magic))]) for n in nn])
for r in range(-3,5):
    sel=(rel==r)&(nn%2==0)
    s=v[sel]*np.sqrt(A2[sel])/12
    print(f"  N = magic{r:+d} (even N): Delta3 mean {v[sel].mean():6.3f} SD {v[sel].std():6.3f}  scaled mean {s.mean():.3f} n={sel.sum()}")
sel=(np.abs(rel)>=5)&(nn%2==0); s=v[sel]*np.sqrt(A2[sel])/12
print(f"  |N-magic|>=5 (even N): Delta3 mean {v[sel].mean():6.3f} SD {v[sel].std():6.3f} scaled {s.mean():.3f} n={sel.sum()}")
