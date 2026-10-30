"""rungB/kissing.py — SPEC v5 Rung B1-B2: Fe-52 as 12 alphas kissing 1; infer the alpha-alpha well reach; predict Ni-56, Zn-60, Cr-48 blind.
Minimised: sum over alpha pairs q*s(stretch) [+ explicit Coulomb in convention (b)]. Constraints: alphas rigid spheres, contact 3.139 fm;
dome fade s(x)=1-x^2, x=(d-3.139)/rho, counted if x<1. Precursors: alphas. Grace (Claude Fable 5.1), 20 Oct 2026."""
import numpy as np,itertools,json,sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data as D
d0=3.139; A4=D.be(2,2); AHC=D.AHC
def resid(Z,N,na): return D.be(Z,N)-na*A4
MEAS={'C12':(6,6,3),'O16':(8,8,4),'Cr48':(24,24,12),'Fe52':(26,26,13),'Ni56':(28,28,14),'Zn60':(30,30,15)}
phi=(1+5**.5)/2
ico=np.array([[0,1,phi],[0,-1,phi],[0,1,-phi],[0,-1,-phi],[1,phi,0],[-1,phi,0],[1,-phi,0],[-1,-phi,0],[phi,0,1],[-phi,0,1],[phi,0,-1],[-phi,0,-1]],float); ico*=d0/np.linalg.norm(ico[0])
cub=np.array([[1,1,0],[1,-1,0],[-1,1,0],[-1,-1,0],[1,0,1],[1,0,-1],[-1,0,1],[-1,0,-1],[0,1,1],[0,1,-1],[0,-1,1],[0,-1,-1]],float)*d0/np.sqrt(2)
def shell(kind): return np.vstack([[0,0,0],ico if kind=='ico' else cub])
def face_pocket(P,shellidx,tri):
    c=P[list(tri)].mean(0); n=c/np.linalg.norm(c); rc=np.linalg.norm(P[tri[0]]-c); h=np.sqrt(max(d0*d0-rc*rc,0)); return c+n*h
def energy(P,rho,q,coul):
    E=0.0;bonds=0.0;EC=0.0
    for i,j in itertools.combinations(range(len(P)),2):
        d=np.linalg.norm(P[i]-P[j]); x=(d-d0)/rho
        if d<d0-1e-9: x=0.0   # compressed counts as full (rigid spheres never are; guard)
        if x<1: s=1-x*x; E+=q*s; bonds+=s
        if coul: EC+=4*AHC/d
    return E-EC if coul else E, bonds, EC
def calib_q(coul):
    # C-12 triangle: 3 bonds at d0
    P=np.array([[0,0,0],[d0,0,0],[d0/2,d0*np.sqrt(3)/2,0]])
    _,b,EC=energy(P,0.3,1.0,coul); r=resid(6,6,3)
    return (r+EC)/b if coul else r/b
def configs(kind):
    S=shell(kind); out={'Fe52':S}
    # Cr-48: remove one shell alpha
    out['Cr48']=S[:-1] if kind=='cub' else np.delete(S,1,axis=0)
    # Ni-56: shell + one alpha in the best face pocket (search all triangles of mutually-touching shell alphas)
    best=None
    sh=range(1,13)
    for tri in itertools.combinations(sh,3):
        dd=[np.linalg.norm(S[a]-S[b]) for a,b in itertools.combinations(tri,2)]
        if max(dd)>d0*1.08: continue
        p=face_pocket(S,sh,tri); P=np.vstack([S,p])
        if min(np.linalg.norm(P[:-1]-p,axis=1))<d0-1e-6: continue
        E,b,_=energy(P,0.3,1.0,False)
        if best is None or E>best[0]: best=(E,P,tri)
    out['Ni56']=best[1]; out['_Ni56_tri']=best[2]
    # Zn-60: two pockets, best pair
    best2=None
    pockets=[]
    for tri in itertools.combinations(sh,3):
        dd=[np.linalg.norm(S[a]-S[b]) for a,b in itertools.combinations(tri,2)]
        if max(dd)>d0*1.08: continue
        p=face_pocket(S,sh,tri)
        if min(np.linalg.norm(S-p,axis=1))<d0-1e-6: continue
        pockets.append(p)
    for p1,p2 in itertools.combinations(pockets,2):
        if np.linalg.norm(p1-p2)<d0-1e-6: continue
        P=np.vstack([S,p1,p2]); E,b,_=energy(P,0.3,1.0,False)
        if best2 is None or E>best2[0]: best2=(E,P)
    out['Zn60']=best2[1]
    return out
if __name__=='__main__':
    res={}
    for coul in (False,True):
        q=calib_q(coul); tag='(b) explicit Coulomb' if coul else '(a) ladder convention'
        print(f"\n=== {tag}: q = {q:.3f} MeV per closed alpha-alpha bond (C-12) ===")
        for kind in ('ico','cub'):
            cf=configs(kind)
            print(f"-- {kind}: shell-shell bonds {'30 @ +5.15%' if kind=='ico' else '24 @ 0%'}; Ni-56 pocket on triangle {cf['_Ni56_tri']}")
            # infer rho from Fe-52
            rows=[]
            for rho in [0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.50,0.70]:
                line={'rho':rho}
                for nuc in ('Cr48','Fe52','Ni56','Zn60'):
                    Z,N,na=MEAS[nuc]; E,b,EC=energy(cf[nuc],rho,q,coul); r=resid(Z,N,na)
                    line[nuc]=(E,r,100*(E/r-1))
                rows.append(line)
                print(f"  rho={rho:.2f}: "+"  ".join(f"{n} {line[n][0]:6.2f}/{line[n][1]:6.2f} ({line[n][2]:+5.1f}%)" for n in ('Cr48','Fe52','Ni56','Zn60')))
            res[(tag,kind)]=rows
    json.dump({f"{k[0]}|{k[1]}":v for k,v in res.items()},open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'kissing_results.json'),'w'),indent=1)
