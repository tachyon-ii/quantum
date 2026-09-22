#!/usr/bin/env python3
"""
B. Mobius crossing geometry, from first principles.
Claim (James, 2026-08-23): cross 2 loops at the centre -> 4-lobed cruciform,
likely tetrahedral; cross 3 -> 6-vertex symmetrical(ish) cruciform.

Model: N unit rings (closed loops of uniformly distributed like-charge /
self-repelling wave density) constrained to pass through a common centre
region -> approximated as N unit circles sharing a common centre.
Energy: pairwise Coulomb-like repulsion between ring elements
(discretised).  Minimise over relative orientations.
If minimum for N=2 is orthogonal planes -> 4 extremal lobes (cruciform),
and for N=3 mutually orthogonal planes -> 6 vertices (octahedron), the
posited geometry follows from pure energy minimisation, no tuning.
"""
import numpy as np
from scipy.optimize import minimize

M = 72  # elements per ring

def ring(euler):
    """Unit circle in plane defined by euler angles (alpha,beta) - normal direction."""
    a, b = euler
    n = np.array([np.sin(b)*np.cos(a), np.sin(b)*np.sin(a), np.cos(b)])
    # basis in plane
    u = np.array([-np.sin(a), np.cos(a), 0.0])
    if np.linalg.norm(np.cross(n, u)) < 1e-9:
        u = np.array([1.0, 0, 0])
    u = u - n*np.dot(u, n); u /= np.linalg.norm(u)
    v = np.cross(n, u)
    t = np.linspace(0, 2*np.pi, M, endpoint=False)
    return np.outer(np.cos(t), u) + np.outer(np.sin(t), v)

def energy(angles, N, soft=0.05):
    rings = [ring(angles[2*i:2*i+2]) for i in range(N)]
    E = 0.0
    for i in range(N):
        for j in range(i+1, N):
            d = np.linalg.norm(rings[i][:, None, :] - rings[j][None, :, :], axis=2)
            E += np.sum(1.0/np.sqrt(d**2 + soft**2))
    return E / M**2

rng = np.random.default_rng(42)
for N in (2, 3, 4):
    best = None
    for trial in range(12):
        x0 = rng.uniform(0, np.pi, 2*N)
        x0[:2] = [0, 0]  # fix ring 1 orientation (gauge)
        res = minimize(energy, x0, args=(N,), method='Nelder-Mead',
                       options={'maxiter': 4000, 'xatol':1e-6, 'fatol':1e-10})
        if best is None or res.fun < best.fun: best = res
    # report pairwise angles between ring normals
    normals = []
    for i in range(N):
        a, b = best.x[2*i:2*i+2]
        normals.append([np.sin(b)*np.cos(a), np.sin(b)*np.sin(a), np.cos(b)])
    normals = np.array(normals)
    print(f"\nN={N}: E_min={best.fun:.6f}")
    for i in range(N):
        for j in range(i+1, N):
            c = abs(np.dot(normals[i], normals[j]))
            print(f"  angle(normal_{i},normal_{j}) = {np.degrees(np.arccos(np.clip(c,0,1))):.2f} deg")
    # vertices = extremal points (lobes): the +-u, +-v of each ring where rings are farthest from others?
    # For orthogonal planes the extremes along each plane's in-plane axes -> count distinct extreme directions
