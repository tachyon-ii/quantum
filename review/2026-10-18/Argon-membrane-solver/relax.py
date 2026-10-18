# models/binding/membrane/relax.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import math
import numpy as np
from scipy.optimize import minimize
import constants as C
import mesh as M
import energy as E


def starting_centres(nucleus, d_init=C.D_INIT):
    """
    §5 Starting centres (fm; relaxed freely afterwards) and species list:
      D:   p (0,0,0), n (1.70,0,0)
      T:   p (0,0,0), n (1.70,0,0), n (0.85, 1.4722, 0)
      He3: p (0,0,0), p (1.70,0,0), n (0.85, 1.4722, 0)
      He4: regular tetrahedron of edge 1.70, p,p,n,n with pp on edge (0,1)
    """
    h_tri = d_init * math.sqrt(3.0) / 2.0
    if nucleus == '1_p':
        centres = np.array([[0.0, 0.0, 0.0]])
        sp = ['p']
    elif nucleus == 'D':
        centres = np.array([[0.0, 0.0, 0.0], [d_init, 0.0, 0.0]])
        sp = ['p', 'n']
    elif nucleus == 'T':
        centres = np.array([[0.0, 0.0, 0.0], [d_init, 0.0, 0.0], [0.5 * d_init, h_tri, 0.0]])
        sp = ['p', 'n', 'n']
    elif nucleus == 'He3':
        centres = np.array([[0.0, 0.0, 0.0], [d_init, 0.0, 0.0], [0.5 * d_init, h_tri, 0.0]])
        sp = ['p', 'p', 'n']
    elif nucleus == 'He4':
        h_tet = d_init * math.sqrt(2.0 / 3.0)
        centres = np.array([
            [0.0, 0.0, 0.0],
            [d_init, 0.0, 0.0],
            [0.5 * d_init, h_tri, 0.0],
            [0.5 * d_init, h_tri / 3.0, h_tet],
        ])
        sp = ['p', 'p', 'n', 'n']
    else:
        raise ValueError(f"Unknown nucleus: {nucleus}")
    centres -= np.mean(centres, axis=0, keepdims=True)
    return centres, sp


def build_initial_system(nucleus, subdiv=C.SUBDIV, d_init=C.D_INIT, rot_matrix=None):
    """Builds templates, species list, and initial vertex coordinates array (A, N_v, 3)."""
    centres, sp = starting_centres(nucleus, d_init=d_init)
    if rot_matrix is not None:
        centres = centres @ rot_matrix.T
    templates = [M.CapsidTemplate(C.RP if s == 'p' else C.RN, subdiv=subdiv) for s in sp]
    N_v = templates[0].n_verts
    coords = np.zeros((len(sp), N_v, 3), dtype=np.float64)
    for i, tmpl in enumerate(templates):
        v = tmpl.rest_verts.copy()
        if rot_matrix is not None:
            v = v @ rot_matrix.T
        coords[i] = v + centres[i][None, :]
    return templates, sp, coords


def relax_system(templates, species, init_coords, params, ext_forces=None, pin_capsid=None,
                 gtol=C.GTOL, maxiter=None):
    """
    §4.1 L-BFGS-B relaxation over all vertex coordinates using analytic gradients.
    """
    if maxiter is None:
        maxiter = C.UNDECLARED_NUMERIC['MAX_ITER_RELAX'][0]

    x0 = init_coords.copy().ravel()
    if pin_capsid is None:
        # Remove initial whole-system COM drift
        c3 = x0.reshape((-1, 3))
        c3 -= np.mean(c3, axis=0, keepdims=True)
        x0 = c3.ravel()

    def obj(x):
        val, g, _ = E.total_energy_and_grad(x, templates, species, params,
                                            ext_forces=ext_forces, pin_capsid=pin_capsid)
        return val, g

    res = minimize(obj, x0, method='L-BFGS-B', jac=True,
                   options={'gtol': gtol, 'ftol': 1e-12, 'maxiter': maxiter})
    _, _, info = E.total_energy_and_grad(res.x, templates, species, params,
                                         ext_forces=ext_forces, pin_capsid=pin_capsid)
    info['converged'] = bool(res.success)
    info['nit'] = int(res.nit)
    info['grad_inf'] = float(np.max(np.abs(res.jac)))
    relaxed_coords = res.x.reshape((len(species), templates[0].n_verts, 3))
    return relaxed_coords, info


def compute_charge_radius(coords, species):
    """§7.1 RMS charge radius from proton centroids plus RP in quadrature."""
    p_idx = [i for i, s in enumerate(species) if s == 'p']
    com = np.mean(coords.reshape(-1, 3), axis=0)
    p_cents = np.mean(coords[p_idx], axis=1) - com[None, :]
    r2_cm = float(np.mean(np.sum(p_cents**2, axis=1)))
    return math.sqrt(r2_cm + C.RP**2)