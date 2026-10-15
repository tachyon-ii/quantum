# the-turtle-conjecture.md §3c — the funnel conform: cross% = 1 - sqrt(1-2GM/rc^2) down the well; the sheared-coordinate lobe energy (-0.083 eps) is the STRUCK artefact, kept so it is not rebuilt. Grace, 2026-10-15.
import numpy as np, math
# regular tetra lobes: apex along +z (time), three base lobes in/near the surface
R=1.0
apex=np.array([0,0,1.0])
base=[np.array([math.sqrt(8/9)*math.cos(a),math.sqrt(8/9)*math.sin(a),-1/3]) for a in (0,2*math.pi/3,4*math.pi/3)]
def E(pts):
    return sum(1/np.linalg.norm(p-q) for i,p in enumerate(pts) for q in pts[i+1:])
def conform(g):  # funnel conform: apex (time) x 1/g, radial base lobe (x) x g ; area-preserving shear
    pts=[apex/g]+[b*np.array([g,1,1]) for b in base]
    return pts
E0=E([apex]+base); print(f"regular tetra E={E0:.4f}  square(cross)={E([np.array(v) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)]]):.4f}")
print("r/r_s   v_esc/c   gamma   cos(theta)  cross%   dE/E0")
for rr in [1e9*0.7e-9**-1*0 + 1/7e-10, 1/2.1e-6, 1/3e-4, 2.5, 1.5, 1.2, 1.05, 1.01]:
    v=math.sqrt(1/rr); g=1/math.sqrt(1-1/rr)
    print(f"{rr:9.3g} {v:8.4f} {g:8.4f} {1/g:9.4f} {100*(1-1/g):8.3g}  {(E(conform(g))-E0)/E0:+.3e}")
# spring: dE/E0 vs eps=g-1 small
for eps in [1e-3,1e-2,3e-2,0.1]:
    g=1+eps; print(f"eps={eps:<6} dE/E0={(E(conform(g))-E0)/E0:+.4e}  ratio/eps^2={(E(conform(g))-E0)/E0/eps**2:.3f}")
# where is the apex stretched vs compressed at horizon?
g=50; print("g=50 apex z:",1/g, " radial lobe x:", g*math.sqrt(8/9))
