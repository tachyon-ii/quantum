# the-fractal-nucleus.md §3 re-check (Argon F22, Grace 16 Oct): four O-16 regular tetrahedra sharing the core alpha, all twelve outer alphas at distance d from the core, four free twists. Result: max achievable min inter-triangle distance = 1.000 d (the triangles cannot avoid touching); zero-overlap configurations exist with 30 (chiral) and 36 (cuboctahedral) contacts. Needs scipy.
import numpy as np, math, itertools
from scipy.optimize import minimize
rng=np.random.default_rng(1)
axes=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float); axes/=np.linalg.norm(axes,axis=1)[:,None]
h=math.sqrt(2/3); rc=1/math.sqrt(3)
frames=[]
for ax in axes:
    u=np.cross(ax,[0,0,1.0]); u/=np.linalg.norm(u); w=np.cross(ax,u); frames.append((u,w))
def allpts(deltas):
    P=[np.zeros(3)]
    for ax,(u,w),d in zip(axes,frames,deltas):
        for k in range(3):
            phi=d+2*math.pi*k/3; P.append(ax*h+rc*(math.cos(phi)*u+math.sin(phi)*w))
    return np.array(P)
pairs=list(itertools.combinations(range(13),2))
def dists(P): return np.array([np.linalg.norm(P[i]-P[j]) for i,j in pairs])
def negmin(x): return -dists(allpts(x)).min()
best=None
for t in range(200):
    x0=rng.uniform(0,2*math.pi,4)
    r=minimize(negmin,x0,method='Nelder-Mead',options={'xatol':1e-8,'fatol':1e-10,'maxiter':4000})
    if best is None or r.fun<best.fun: best=r
print("max-min clearance (4 free twists): %.4f d"%(-best.fun))
# Now: find configs with min distance exactly 1 and max number of contacts at 1.000 (no overlap)
def score(x):
    d=dists(allpts(x)); m=d.min()
    pen=max(0,1-m)*100
    return -(np.sum(np.abs(d-1)<0.003)) + pen*10
bestc=None
for t in range(400):
    x0=rng.uniform(0,2*math.pi,4)
    r=minimize(score,x0,method='Nelder-Mead',options={'xatol':1e-9,'fatol':1e-12,'maxiter':6000})
    d=dists(allpts(r.x))
    if d.min()>0.999:
        n=np.sum(np.abs(d-1)<0.003)
        if bestc is None or n>bestc[0]: bestc=(n,r.x,d)
n,x,d=bestc
print("most contacts with zero overlap: %d contacts at 1.000; min=%.5f; next distances:"%(n,d.min()), np.round(sorted(d[d>1.003])[:4],4))
print("twists (deg):",np.round(np.degrees(x)%120,2))
