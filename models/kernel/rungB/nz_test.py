"""rungB/nz_test.py — what kappa=0.18 means, decided on N != Z data. The cleanest N != Z datum is the MIRROR PAIR: the two members
differ only by one proton <-> neutron, so their binding difference is the Coulomb energy of ONE proton in the cluster — no bond model needed.
  hole pairs  (A=4n-1): BE(Z-1,N) - BE(Z,N-1) = Coulomb of a proton inside one alpha with the rest
       model (full point charge): c_int + sum_{j != i} 2*AHC/d_ij ; c_int = BE(T)-BE(3He) = measured in-alpha partner term
  particle pairs (A=4n+1): BE(Z,N+1) - BE(Z+1,N) = Coulomb of a valence proton in a surface pocket (distance x from three bonded alphas; x scanned)
  kappa_eff = (measured - c_int)/(model inter-alpha part).  Screening reading predicts kappa_eff = 0.18; full Coulomb predicts 1.
Geometry: soft-well optimum at kappa=0.18 (nz_geom_kappa0.18.json). Also: q_needed per bond if Coulomb is paid in full.
Sources: AME2020 via kernel/data.py. Grace (Claude Fable 5.2), 17 Nov 2026."""
import numpy as np,json,os,sys,itertools
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data as D
HERE=os.path.dirname(os.path.abspath(__file__)); d0=3.139; rho=0.30
G=json.load(open(os.path.join(HERE,'nz_geom_kappa0.18.json'))); G1=json.load(open(os.path.join(HERE,'nz_geom_kappa1.0.json')))
EL={6:'C',8:'O',10:'Ne',12:'Mg',14:'Si',16:'S',18:'Ar',20:'Ca',22:'Ti',24:'Cr',26:'Fe',28:'Ni',30:'Zn'}
cint=D.be(1,2)-D.be(2,1)
def pockets(P,x):
    out=[]; c=P.mean(0); N=len(P)
    for i,j,k in itertools.combinations(range(N),3):
        if max(np.linalg.norm(P[i]-P[j]),np.linalg.norm(P[i]-P[k]),np.linalg.norm(P[j]-P[k]))>d0+rho: continue
        m=(P[i]+P[j]+P[k])/3; n=np.cross(P[j]-P[i],P[k]-P[i]); n/=np.linalg.norm(n)
        rc=np.linalg.norm(P[i]-m); h2=x*x-rc*rc
        if h2<=0: continue
        for sgn in (1,-1):
            v=m+sgn*np.sqrt(h2)*n
            if np.min(np.linalg.norm(P-v,axis=1))>=x-1e-6: out.append(v)
    return out
rows=[]; print(f"c_int (T - 3He) = {cint:.3f} MeV\n")
print("| core | hole pair | measured | model full (mean over alphas) | kappa_eff | particle pair | measured | model full, x=2.2 / 2.7 / 3.14 (lowest-Coulomb pocket) | kappa_eff (x=2.7) |")
print("|---|---|---|---|---|---|---|---|---|")
ke_h=[];ke_p=[]
for N in range(3,15):
    P=np.array(G[str(N)]['P']); Z=2*N; dm=np.linalg.norm(P[:,None]-P[None],axis=2)+np.eye(N)*1e9
    inter=(2*D.AHC/dm).sum(1)                      # one proton at alpha i with all other alphas
    mh=D.be(Z-1,Z)-D.be(Z,Z-1); kh=(mh-cint)/inter.mean(); ke_h.append(kh)
    mp=D.be(Z,Z+1)-D.be(Z+1,Z); vals=[]
    for x in (2.2,2.7,3.14):
        pk=pockets(P,x); vals.append(min((2*D.AHC/np.linalg.norm(P-v,axis=1)).sum() for v in pk) if pk else np.nan)
    kp=mp/vals[1]; ke_p.append(kp)
    print(f"| {EL[Z]}-{4*N} | A={4*N-1} | {mh:.3f} | {cint+inter.mean():.3f} ({cint+inter.min():.2f}–{cint+inter.max():.2f}) | **{kh:.2f}** | A={4*N+1} | {mp:.3f} | {vals[0]:.2f} / {vals[1]:.2f} / {vals[2]:.2f} | **{kp:.2f}** |")
print(f"\nkappa_eff: hole pairs mean {np.mean(ke_h):.3f} (sd {np.std(ke_h):.3f}); particle pairs (x=2.7) mean {np.mean(ke_p):.3f} (sd {np.std(ke_p):.3f}).  Screening reading requires 0.18.")
print("\n## If Coulomb is paid in full: the bond strength the data then require\n")
print("| nucleus | measured residual | E_C full (point alphas, kappa=0.18 geometry) | eff. bonds b | mean coordination 2b/N | q_needed = (resid + E_C)/b | E_C full, kappa=1 geometry | b | q_needed |")
print("|---|---|---|---|---|---|---|---|---|")
qs=[];zs=[]
for N in range(3,16):
    Z=2*N; r=D.be(Z,Z)-N*D.be(2,2); row=[]
    for GG in (G,G1):
        P=np.array(GG[str(N)]['P']); iu=np.triu_indices(N,1); d=np.linalg.norm(P[iu[0]]-P[iu[1]],axis=1)
        EC=(4*D.AHC/d).sum(); xx=np.clip((d-d0)/rho,0,None); b=np.where(d<d0,1.0,np.where(xx<1,1-xx**2,0)).sum(); row+=[EC,b,(r+EC)/b]
    qs.append(row[2]); zs.append(2*row[1]/N)
    print(f"| {EL[Z]}-{4*N} | {r:.2f} | {row[0]:.1f} | {row[1]:.1f} | {2*row[1]/N:.2f} | **{row[2]:.2f}** | {row[3]:.1f} | {row[4]:.1f} | {row[5]:.2f} |")
qs=np.array(qs);zs=np.array(zs); A=np.c_[np.ones_like(zs),zs]; co=np.linalg.lstsq(A,qs,rcond=None)[0]; fit=A@co
print(f"\nq_needed vs mean coordination z: linear fit q = {co[0]:.2f} + {co[1]:.2f} z, rms {np.sqrt(np.mean((qs-fit)**2)):.2f} MeV; ratio q(Ni-56)/q(C-12) = {qs[11]/qs[0]:.2f}; log-log slope {np.polyfit(np.log(zs),np.log(qs),1)[0]:.2f}")
Ns=np.arange(3,16); print(f"q_needed vs N_alpha log-log slope {np.polyfit(np.log(Ns),np.log(qs),1)[0]:.2f}")
print("\n## Neutron-excess increments (per added neutron, MeV) — what any filler model must produce")
for nm,Z,N0,k in (('Ne-22 - Ne-20',10,10,2),('Mg-26 - Mg-24',12,12,2),('Ca-44 - Ca-40',20,20,4),('Ca-48 - Ca-40',20,20,8),('Fe-56 - Fe-52',26,26,4),('Ni-60 - Ni-56',28,28,4)):
    print(f"  {nm}: {D.be(Z,N0+k)-D.be(Z,N0):.2f} total, {(D.be(Z,N0+k)-D.be(Z,N0))/k:.2f} per neutron")
