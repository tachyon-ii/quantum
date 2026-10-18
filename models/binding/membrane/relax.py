"""relax.py — L-BFGS-B over all vertex coordinates (BUILD-SPEC §4.1). Implementer: Grace (Claude Opus 5.5)."""
import numpy as np
from scipy.optimize import minimize
def relax(sys,x0=None,maxiter=20000):
    x0=sys.X0.ravel() if x0 is None else x0
    r=minimize(sys.energy,x0,jac=True,method='L-BFGS-B',options=dict(maxiter=maxiter,maxfun=4*maxiter,gtol=1e-8,ftol=1e-14,maxcor=30))
    return r.x,r
