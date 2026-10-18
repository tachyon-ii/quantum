# models/binding/membrane/paths.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import math
import numpy as np
import constants as C
import relax as R
import analyse as A


def run_load_path(templates, species, eq_coords, eq_info, params,
                  path_kind='tangential', p1_idx=0, p2_idx=1, p3_idx=2):
    """
    §6 Quasi-static, force-controlled load path on T or He3:
      Applies external force F to all vertices of P1 (uniformly by rest vertex area),
      holds whole-system centroid pinned (balanced reaction on P2, P3), increases |F| in steps
      of F_STEP = 0.02 MeV/fm from 0 until snap (first step where any pair loses contact s > 0).
    """
    N_v = templates[0].n_verts
    A_num = len(species)
    cents0 = eq_info['centroids']
    hub0 = np.mean(cents0, axis=0)

    # Define unit force direction f_hat from initial equilibrium geometry
    r_p1_hub = hub0 - cents0[p1_idx]
    r_p1_hub /= np.linalg.norm(r_p1_hub)
    p_normal = np.cross(cents0[p2_idx] - cents0[p1_idx], cents0[p3_idx] - cents0[p1_idx])
    p_normal /= np.linalg.norm(p_normal)

    if path_kind == 'radial':
        f_hat = -r_p1_hub
    elif path_kind == 'out_of_plane':
        f_hat = p_normal
    elif path_kind == 'tangential':
        t_vec = np.cross(p_normal, r_p1_hub)
        t_vec /= np.linalg.norm(t_vec)
        if np.dot(t_vec, cents0[p3_idx] - cents0[p1_idx]) < 0:
            t_vec = -t_vec
        f_hat = t_vec
    else:
        raise ValueError(f"Unknown path_kind: {path_kind}")

    # Area weights on P1 so sum_{v in P1} F_v = F * f_hat, balanced across P2, P3 to pin system COM
    w_p1 = eq_info['A_v_list'][p1_idx] / np.sum(eq_info['A_v_list'][p1_idx])
    curr_coords = eq_coords.copy()
    last_stable = None
    trajectory = []
    F_inv_13 = None
    F_inv_23 = None

    max_steps = C.UNDECLARED_NUMERIC['F_MAX_STEPS'][0]
    for step in range(max_steps):
        F_mag = step * C.F_STEP
        ext_f = np.zeros_like(curr_coords)
        ext_f[p1_idx] = (F_mag * w_p1)[:, None] * f_hat[None, :]
        # Pin system centroid by applying equal & opposite reaction across remaining nucleons
        for k in range(A_num):
            if k != p1_idx:
                w_k = eq_info['A_v_list'][k] / np.sum(eq_info['A_v_list'][k])
                ext_f[k] = -(F_mag / (A_num - 1) * w_k)[:, None] * f_hat[None, :]

        next_coords, info = R.relax_system(templates, species, curr_coords, params,
                                           ext_forces=ext_f, gtol=1e-5, maxiter=150)

        p12 = A.analyse_patch(p1_idx, p2_idx, next_coords, info, params)
        p13 = A.analyse_patch(p1_idx, p3_idx, next_coords, info, params)
        p23 = A.analyse_patch(p2_idx, p3_idx, next_coords, info, params)

        all_three_connected = bool(p12.get('connected') and p13.get('connected') and p23.get('connected'))

        if not all_three_connected:
            # Snap reached!
            F_snap = F_mag
            break

        # Track pivot egg inversion (sign change of hub_shift_fm from positive to <= 0)
        if F_inv_13 is None and p13['hub_shift_fm'] <= 0.0:
            F_inv_13 = F_mag
        if F_inv_23 is None and p23['hub_shift_fm'] <= 0.0:
            F_inv_23 = F_mag

        # Roll angle of P1 about P3 centroid
        v0_13 = cents0[p1_idx] - cents0[p3_idx]
        v_13  = info['centroids'][p1_idx] - info['centroids'][p3_idx]
        cos_r = np.clip(np.dot(v0_13, v_13) / (np.linalg.norm(v0_13) * np.linalg.norm(v_13)), -1.0, 1.0)
        theta_roll_deg = float(math.degrees(math.acos(cos_r)))

        # Surviving D bond-axis angle beta_D to P1 displacement / velocity vector
        vel_p1 = info['centroids'][p1_idx] - cents0[p1_idx]
        if np.linalg.norm(vel_p1) < 1e-8:
            vel_p1 = f_hat
        vel_hat = vel_p1 / np.linalg.norm(vel_p1)
        # Weakest link determines which np pair survives as D
        d_axis = (info['centroids'][p3_idx] - info['centroids'][p2_idx]) if p12['E_adh_pair_MeV'] >= p23['E_adh_pair_MeV'] \
                 else (info['centroids'][p3_idx] - info['centroids'][p1_idx])
        d_axis /= np.linalg.norm(d_axis)
        beta_D_deg = float(math.degrees(math.acos(np.clip(abs(np.dot(d_axis, vel_hat)), 0.0, 1.0))))

        spin_deg, spin_axis = A.kabsch_rotation_angle(eq_coords[p1_idx], next_coords[p1_idx])

        step_rec = {
            'F_MeV_fm': F_mag,
            'E_total': info['E_total'],
            'theta_roll_deg': theta_roll_deg,
            'beta_D_deg': beta_D_deg,
            'spin_P1_deg': spin_deg,
            'spin_P1_axis': spin_axis,
            'p12_area': p12['area_fm2'], 'p12_hub_shift': p12['hub_shift_fm'],
            'p13_area': p13['area_fm2'], 'p13_hub_shift': p13['hub_shift_fm'],
            'p23_area': p23['area_fm2'], 'p23_hub_shift': p23['hub_shift_fm'],
        }
        trajectory.append(step_rec)
        last_stable = step_rec
        curr_coords = next_coords
    else:
        F_snap = max_steps * C.F_STEP

    if last_stable is None:
        last_stable = {'theta_roll_deg': 0.0, 'beta_D_deg': 60.0, 'spin_P1_deg': 0.0, 'spin_P1_axis': [0, 0, 1]}

    simultaneous = False
    if F_inv_13 is not None and F_inv_23 is not None:
        simultaneous = abs(F_inv_13 - F_inv_23) < 2.0 * C.F_STEP

    return {
        'path_kind': path_kind,
        'p1_idx': p1_idx, 'p2_idx': p2_idx, 'p3_idx': p3_idx,
        'F_snap_MeV_fm': float(F_snap),
        'theta_snap_deg': last_stable['theta_roll_deg'],
        'beta_D_deg': last_stable['beta_D_deg'],
        'spin_P1_deg': last_stable['spin_P1_deg'],
        'spin_P1_axis': last_stable['spin_P1_axis'],
        'F_inv_13_MeV_fm': F_inv_13,
        'F_inv_23_MeV_fm': F_inv_23,
        'inversions_timing': 'simultaneous' if simultaneous else ('sequential' if (F_inv_13 or F_inv_23) else 'no_inversion_before_snap'),
        'last_stable': last_stable,
        'n_steps': len(trajectory),
    }