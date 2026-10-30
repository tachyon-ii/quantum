"""rungB/ladder_stretch.py — SPEC v5 B3: the 4n ladder C-12 .. Zn-60 as soft-well alpha clusters. Energy per pair: hard core below d0,
dome well -q*(1-x^2) for 0<=x<1, x=(d-d0)/rho. q=2.425 (C-12), rho=0.30 fm (Fe-52), both from B1; everything else blind.
Global minimum per N by multi-start local minimisation (declared: 80 starts, seed 0). Grace (Claude Fable 5.1), 20 Oct 2026."""
import numpy as np,sys,os,json,itertools
from scipy.optimize import minimize
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data as D
d0=3.139; rho=float(sys.argv[1]) if len(sys.argv)>1 else 0.30; KC=200.0
KAPPA=float(sys.argv[2]) if len(sys.argv)>2 else 0.0      # screened inter-alpha Coulomb: KAPPA * 4*AHC/d over ALL pairs (declared test)
q=(7.27+KAPPA*5.50)/3.0                                   # C-12 exact by construction
MEAS={'C12':(6,6,3),'O16':(8,8,4),'Ne20':(10,10,5),'Mg24':(12,12,6),'Si28':(14,14,7),'S32':(16,16,8),'Ar36':(18,18,9),'Ca40':(20,20,10),'Ti44':(22,22,11),'Cr48':(24,24,12),'Fe52':(26,26,13),'Ni56':(28,28,14),'Zn60':(30,30,15)}
def E_and_bonds(x,N):
    P=x.reshape(N,3); E=0.0; b=0.0; G=np.zeros_like(P)
    for i in range(N):
        for j in range(i+1,N):
            r=P[i]-P[j]; d=np.linalg.norm(r); u=r/d
            if KAPPA>0:
                E+=KAPPA*4*D.AHC/d; dEc=-KAPPA*4*D.AHC/d**2; G[i]+=dEc*u; G[j]-=dEc*u
            if d<d0:
                E+=KC*(d0-d)**2-q; b+=1.0; g=-2*KC*(d0-d)*(-1)  # dE/dd = 2KC(d-d0)
                dE=2*KC*(d-d0)
            else:
                xx=(d-d0)/rho
                if xx<1: s=1-xx*xx; E+=-q*s; b+=s; dE=q*2*xx/rho
                else: dE=0.0
            G[i]+=dE*u; G[j]-=dE*u
    return E,G.ravel(),b
def solve(N,starts=60,seed=0):
    """two-stage: (1) weak harmonic confinement toward the centroid so the short-range well can be found; (2) release."""
    rng=np.random.default_rng(seed); best=None
    R0=0.55*d0*N**(1/3)
    for k in range(starts):
        x0=rng.uniform(-R0,R0,(N,3)).ravel()
        for kc in (0.6,0.15,0.0):
            def f(x):
                E,G,_=E_and_bonds(x,N); P=x.reshape(N,3); c=P.mean(0)
                return E+kc*((P-c)**2).sum(), G+(kc*2*(P-c)).ravel()
            res=minimize(f,x0,jac=True,method='L-BFGS-B',options=dict(maxiter=2000)); x0=res.x
        E,_,_=E_and_bonds(res.x,N)
        if best is None or E<best.fun: best=res; best.fun=E
    E,_,b=E_and_bonds(best.x,N); return -E,b,best.x.reshape(N,3)
if __name__=='__main__':
    print(f"rho={rho} q={q:.3f} kappa={KAPPA}   | nucleus: model binding (eff. bonds) vs measured residual")
    out={}
    for nuc,(Z,Nn,na) in MEAS.items():
        if na<3: continue
        Eb,b,P=solve(na); r=D.be(Z,Nn)-na*D.be(2,2)
        # count exact contacts and stretched ones
        dd=[np.linalg.norm(P[i]-P[j]) for i,j in itertools.combinations(range(na),2)]
        nc=sum(1 for d in dd if d<d0+1e-3); ns=sum(1 for d in dd if d0+1e-3<=d<d0+rho)
        out[nuc]=dict(model=Eb,meas=r,bonds=b,contacts=nc,stretched=ns)
        print(f"  {nuc:5s} Nα={na:2d}: {Eb:7.2f} ({b:5.2f} eff; {nc} exact + {ns} stretched) vs {r:6.2f}  {100*(Eb/r-1):+6.1f}%",flush=True)
    json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),f'ladder_stretch_rho{rho}_kappa{KAPPA}.json'),'w'),indent=1)
