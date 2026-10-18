# models/binding/membrane/analyse.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import math
import numpy as np
from scipy.linalg import eigh
import constants as C
import mesh as M
import relax as R


def analyse_patch(i, j, coords, info, params):
    """
    §7.2 & §7.4 Patch geometry and local peel resistance for pair (i, j):
      - area, perimeter, well-weighted centroid vs geometric centroid
      - principal axes and aspect ratio of the energy-weighted distribution
      - sign of (well_centroid - geom_centroid) . hub_direction
      - fraction of patch energy in the hub half
      - local line-energy e0*s * front_width at point, broadside, and hub end
    """
    key = (min(i, j), max(i, j))
    pd = info['pair_details'][key]
    if not pd['connected']:
        return {'connected': False}

    e0 = float(params['e0'])
    A_num = len(coords)
    cents = info['centroids']
    c_i, c_j = cents[i], cents[j]
    mid_ij = 0.5 * (c_i + c_j)
    bond_hat = (c_j - c_i) / np.linalg.norm(c_j - c_i)

    # Hub direction in the contact plane perpendicular to bond_hat
    cluster_hub = np.mean(cents, axis=0)
    hub_vec = cluster_hub - mid_ij
    hub_vec = hub_vec - np.dot(hub_vec, bond_hat) * bond_hat
    hub_norm = float(np.linalg.norm(hub_vec))
    if hub_norm > 1e-8:
        hub_hat = hub_vec / hub_norm
    else:
        # For A=2 (D), choose arbitrary axis perpendicular to bond_hat
        ref = np.array([0.0, 1.0, 0.0]) if abs(bond_hat[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
        hub_hat = np.cross(bond_hat, ref)
        hub_hat /= np.linalg.norm(hub_hat)
    trans_hat = np.cross(bond_hat, hub_hat)

    # Collect active contact vertices from both skins (s > 0)
    s_i = pd['s_ij'] if i < j else pd['s_ji']
    s_j = pd['s_ji'] if i < j else pd['s_ij']
    Av_i = info['A_v_list'][i]
    Av_j = info['A_v_list'][j]

    mask_i = s_i > 0.0
    mask_j = s_j > 0.0
    pts = np.vstack([coords[i, mask_i], coords[j, mask_j]])
    areas = 0.5 * np.concatenate([Av_i[mask_i], Av_j[mask_j]])  # single-interface equivalent area
    weights = e0 * np.concatenate([Av_i[mask_i] * s_i[mask_i], Av_j[mask_j] * s_j[mask_j]])

    patch_area = float(np.sum(areas))
    patch_energy = float(np.sum(weights))
    if patch_area <= 1e-12 or len(pts) < 3:
        return {'connected': False}

    # Project contact points into 2D contact plane (u along hub_hat, v along trans_hat)
    rel = pts - mid_ij[None, :]
    u = rel @ hub_hat    # +u toward hub, -u toward outer point
    v = rel @ trans_hat  # transverse width

    u_geom = float(np.sum(areas * u) / patch_area)
    v_geom = float(np.sum(areas * v) / patch_area)
    u_well = float(np.sum(weights * u) / patch_energy)
    v_well = float(np.sum(weights * v) / patch_energy)

    # Energy-weighted covariance matrix and principal axes
    du = u - u_well
    dv = v - v_well
    cov = np.array([
        [np.sum(weights * du * du), np.sum(weights * du * dv)],
        [np.sum(weights * du * dv), np.sum(weights * dv * dv)],
    ]) / patch_energy
    evals = np.sort(np.maximum(1e-12, np.linalg.eigvalsh(cov)))
    aspect_ratio = float(math.sqrt(evals[1] / evals[0]))

    # Perimeter estimate from convex / radial hull in (u, v)
    r_uv = np.sqrt((u - u_geom)**2 + (v - v_geom)**2)
    r_eff = float(np.percentile(r_uv, 90)) if len(r_uv) > 4 else float(math.sqrt(patch_area / math.pi))
    perimeter = float(2.0 * math.pi * r_eff * math.sqrt(0.5 * (1.0 + aspect_ratio**2)) / aspect_ratio**0.5)

    # Hub orientation check (§7.2): (well_centroid - geom_centroid) . hub_direction = u_well - u_geom
    hub_shift = float(u_well - u_geom)
    hub_half_frac = float(np.sum(weights[u >= u_geom]) / patch_energy) if A_num >= 3 else 0.5

    # §7.4 Local line-energy (e0 * s * front_width) by slicing along u in 10 bins from outer point to hub
    u_min, u_max = float(np.min(u)), float(np.max(u))
    span = max(1e-6, u_max - u_min)
    bins = np.linspace(u_min, u_max, 9)
    du_bin = span / 8.0
    line_energies = []
    for b_idx in range(len(bins) - 1):
        in_b = (u >= bins[b_idx]) & (u <= bins[b_idx + 1])
        line_energies.append(float(np.sum(weights[in_b]) / du_bin) if np.any(in_b) else 0.0)

    peel_point = float(np.mean(line_energies[:2])) if len(line_energies) >= 2 else 0.0
    peel_broad = float(np.max(line_energies)) if len(line_energies) > 0 else 0.0
    peel_hub   = float(np.mean(line_energies[-2:])) if len(line_energies) >= 2 else 0.0

    return {
        'connected': True,
        'area_fm2': patch_area,
        'perimeter_fm': perimeter,
        'E_adh_pair_MeV': patch_energy,
        'u_geom_fm': u_geom,
        'u_well_fm': u_well,
        'hub_shift_fm': hub_shift,
        'hub_shift_sign': int(np.sign(hub_shift)) if abs(hub_shift) > 1e-9 else 0,
        'hub_half_energy_frac': hub_half_frac,
        'aspect_ratio': aspect_ratio,
        'peel_line_point_MeV_fm': peel_point,
        'peel_line_broadside_MeV_fm': peel_broad,
        'peel_line_hub_MeV_fm': peel_hub,
    }


def quartic_out_of_plane_mode(templates, species, eq_coords, params):
    """
    §7.3 Displace P1's centroid out of plane by z in Z_DISPL_GRID (rigid shift of P1's vertices,
    relax P2, P3 with P1's centroid pinned at z), fit E(z) = E0 + k2*z^2 + k4*z^4,
    and solve 1D Schrödinger ground state for reduced mass mu = (2/3)*(MP+MN)/2: E_zp and p_rms.
    """
    z_vals = np.array(C.Z_DISPL_GRID, dtype=np.float64)
    E_vals = np.zeros_like(z_vals)
    c0_P1 = np.mean(eq_coords[0], axis=0)

    for idx, z in enumerate(z_vals):
        coords_z = eq_coords.copy()
        coords_z[0, :, 2] += z
        target_c = c0_P1 + np.array([0.0, 0.0, z])
        _, info_z = R.relax_system(templates, species, coords_z, params,
                                   pin_capsid=(0, target_c), gtol=1e-6, maxiter=150)
        E_vals[idx] = info_z['E_total']

    dE = E_vals - E_vals[0]
    # Linear least-squares fit of dE(z) = k2 * z^2 + k4 * z^4
    A_mat = np.column_stack([z_vals**2, z_vals**4])
    k2, k4 = np.linalg.lstsq(A_mat, dE, rcond=None)[0]
    k2, k4 = float(k2), float(max(1e-6, k4))

    # Solve 1D Schrödinger equation [- (hc)^2 / (2 mu) d^2/dz^2 + max(0, k2)*z^2 + k4*z^4] psi = E psi on finite grid
    mu = (2.0 / 3.0) * 0.5 * (C.MP + C.MN)
    N_grid = 400
    z_grid = np.linspace(-2.5, 2.5, N_grid)
    dz = z_grid[1] - z_grid[0]
    kin_pref = (C.HC**2) / (2.0 * mu * dz**2)
    V_grid = np.maximum(0.0, k2 * z_grid**2 + k4 * z_grid**4)
    diag = 2.0 * kin_pref + V_grid
    off  = -kin_pref * np.ones(N_grid - 1)
    evals, evecs = eigh(np.diag(diag) + np.diag(off, 1) + np.diag(off, -1))
    E_zp = float(evals[0])
    psi0 = evecs[:, 0] / math.sqrt(np.sum(evecs[:, 0]**2) * dz)
    dpsi = np.gradient(psi0, dz)
    p_rms = float(C.HC * math.sqrt(np.sum(dpsi**2) * dz))

    return {
        'z_grid_fm': z_vals.tolist(),
        'dE_MeV': dE.tolist(),
        'k2_MeV_fm2': k2,
        'k4_MeV_fm4': k4,
        'E_zp_MeV': E_zp,
        'p_rms_MeV_c': p_rms,
    }


def kabsch_rotation_angle(P_init, P_final):
    """§7.6 Kabsch algorithm: rotation angle (deg) and unit axis of P1's vertex set about its centroid."""
    X = P_init - np.mean(P_init, axis=0, keepdims=True)
    Y = P_final - np.mean(P_final, axis=0, keepdims=True)
    H = X.T @ Y
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    D_mat = np.diag([1.0, 1.0, d])
    R_mat = Vt.T @ D_mat @ U.T
    tr = np.clip(np.trace(R_mat), -1.0, 3.0)
    angle_rad = math.acos(np.clip((tr - 1.0) / 2.0, -1.0, 1.0))
    axis = np.array([R_mat[2, 1] - R_mat[1, 2], R_mat[0, 2] - R_mat[2, 0], R_mat[1, 0] - R_mat[0, 1]])
    norm_a = float(np.linalg.norm(axis))
    axis = (axis / norm_a).tolist() if norm_a > 1e-9 else [0.0, 0.0, 1.0]
    return float(math.degrees(angle_rad)), axis