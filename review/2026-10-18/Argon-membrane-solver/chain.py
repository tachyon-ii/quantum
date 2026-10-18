# models/binding/membrane/chain.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import numpy as np
import constants as C
import mesh as M
import relax as R


def evaluate_collinear_chain(species_order, params, subdiv=C.SUBDIV):
    """
    §7.7 Places P1-P3-P2 collinear at contact distances along x:
      P1 at (-d_init, 0, 0), P3 at (0, 0, 0) [pinned], P2 at (+d_init, 0, 0).
    Relaxes with P3's centroid pinned at (0,0,0), reports BE_chain, energy relative to D + N,
    and scans P1 separation coordinate to check for any saddle barrier.
    """
    templates = [M.CapsidTemplate(C.RP if s == 'p' else C.RN, subdiv=subdiv) for s in species_order]
    N_v = templates[0].n_verts
    centres = np.array([[-C.D_INIT, 0.0, 0.0], [0.0, 0.0, 0.0], [C.D_INIT, 0.0, 0.0]])
    coords = np.zeros((3, N_v, 3), dtype=np.float64)
    for i, tmpl in enumerate(templates):
        coords[i] = tmpl.rest_verts + centres[i][None, :]

    # If end pair has same species, mark as singlet; for n-n-p or p-p-n, one adjacent pair is same-species
    rel_coords, info = R.relax_system(templates, species_order, coords, params,
                                      pin_capsid=(1, np.array([0.0, 0.0, 0.0])), gtol=1e-6, maxiter=250)
    BE_chain = info['BE']
    dE_vs_D_plus_N = BE_chain - C.BE_D  # positive means deeper than D + N threshold

    # Scan P1 separation coordinate x_1 from relaxed position outward by +0.6 fm to locate any saddle
    c0_p1 = np.mean(rel_coords[0], axis=0)
    scan_shifts = [0.0, 0.1, 0.2, 0.3, 0.4, 0.6]
    scan_E = []
    for dx in scan_shifts:
        c_scan = rel_coords.copy()
        c_scan[0, :, 0] -= dx
        _, inf_s = R.relax_system(templates, species_order, c_scan, params,
                                  pin_capsid=(0, c0_p1 - np.array([dx, 0.0, 0.0])), gtol=1e-5, maxiter=80)
        scan_E.append(float(inf_s['E_total']))

    saddle_barrier = float(max(scan_E) - scan_E[0])
    return {
        'chain': '-'.join(species_order),
        'BE_chain_MeV': float(BE_chain),
        'dip_below_D_plus_N_MeV': float(dE_vs_D_plus_N),
        'saddle_barrier_MeV': saddle_barrier,
        'scan_shifts_fm': scan_shifts,
        'scan_E_total_MeV': scan_E,
    }