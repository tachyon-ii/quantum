"""rungB/nz_geom.py — vectorised re-solve of the soft-well ladder (same energy as ladder_stretch.py), SAVING positions.
Usage: nz_geom.py kappa  -> nz_geom_kappa{kappa}.json (resumable per nucleus). Grace (Claude Fable 5.2), 17 Nov 2026."""
import numpy as np,sys,os,json
from scipy.optimize import minimize
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data as D
d0=3.139; rho=0.30; KC=200.0; KAPPA=float(sys.argv[1]); q=(7.27+KAPPA*5.50)/3.0
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,f'nz_geom_kappa{KAPPA}.json')
def EG(x,N,kc=0.0):
    P=x.reshape(N,3); iu=np.triu_indices(N,1); r=P[iu[0]]-P[iu[1]]; d=np.linalg.norm(r,axis=1); u=r/d[:,None]
    E=KAPPA*4*D.AHC/d; dE=-KAPPA*4*D.AHC/d**2
    core=d<d0; xx=(d-d0)/rho; well=(~core)&(xx<1)
    E=E+np.where(core,KC*(d0-d)**2-q,0)+np.where(well,-q*(1-xx**2),0)
    dE=dE+np.where(core,2*KC*(d-d0),0)+np.where(well,q*2*xx/rho,0)
    G=np.zeros_like(P); np.add.at(G,iu[0],dE[:,None]*u); np.add.at(G,iu[1],-dE[:,None]*u)
    c=P.mean(0); return E.sum()+kc*((P-c)**2).sum(), (G+kc*2*(P-c)).ravel()
def solve(N,starts=60,seed=0):
    rng=np.random.default_rng(seed); best=None; R0=0.55*d0*N**(1/3)
    for k in range(starts):
        x0=rng.uniform(-R0,R0,(N,3)).ravel()
        for kc in (0.6,0.15,0.0):
            res=minimize(EG,x0,args=(N,kc),jac=True,method='L-BFGS-B',options=dict(maxiter=2000)); x0=res.x
        E=EG(res.x,N)[0]
        if best is None or E<best[0]: best=(E,res.x.copy())
    return best
out=json.load(open(OUT)) if os.path.exists(OUT) else {}
for N in range(3,16):
    if str(N) in out: continue
    E,x=solve(N); out[str(N)]=dict(E=-E,P=x.reshape(N,3).tolist())
    tmp=OUT+'.tmp'; json.dump(out,open(tmp,'w')); os.replace(tmp,OUT); print(N,round(-E,3),flush=True)
