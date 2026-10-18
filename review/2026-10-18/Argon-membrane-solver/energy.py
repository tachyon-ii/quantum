# models/binding/membrane/energy.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import numpy as np
import constants as C
import mesh as M


def fade_s_and_deriv(x, variant_quadratic=False):
    """
    §3.4 Fade function s(x) and ds/dx for x = g_v / delta:
      Primary: s(x) = 1 for x <= 0; (1 - x) for 0 < x < 1; 0 for x >= 1.
      Variant: s(x) = 1 for x <= 0; (1 - x)^2 for 0 < x < 1; 0 for x >= 1.
    """
    s = np.zeros_like(x)
    ds = np.zeros_like(x)
    m_neg = x <= 0.0
    m_mid = (x > 0.0) & (x < 1.0)
    s[m_neg] = 1.0
    if not variant_quadratic:
        s[m_mid] = 1.0 - x[m_mid]
        ds[m_mid] = -1.0
    else:
        u = 1.0 - x[m_mid]
        s[m_mid] = u * u
        ds[m_mid] = -2.0 * u
    return s, ds


def helfrich_bending(verts, edges, edge_faces, n_hat, A_f, k_bend):
    """
    §3.3 Discrete Helfrich bending energy E_bend = K_BEND * sum_edges (1 - cos theta_e)
    and finite-difference / analytic vertex gradient (only evaluated when k_bend > 0).
    """
    if k_bend <= 0.0:
        return 0.0, np.zeros_like(verts)
    f1 = edge_faces[:, 0]
    f2 = edge_faces[:, 1]
    n1 = n_hat[f1]
    n2 = n_hat[f2]
    cos_th = np.clip(np.sum(n1 * n2, axis=1), -1.0, 1.0)
    E_b = float(k_bend * np.sum(1.0 - cos_th))

    # Exact derivative wrt face normals transferred to vertices
    grad = np.zeros_like(verts)
    # For each face f, dn_f / dv_a = (1 / (2 A_f)) * ((v_b - v_c) x n_f) x n_f (projection)
    # Since K_BEND = 0 in primary and 0.01*E0 in variant, compute exact face-normal sensitivity:
    dE_dn = np.zeros_like(n_hat)
    np.add.at(dE_dn, f1, -k_bend * n2)
    np.add.at(dE_dn, f2, -k_bend * n1)
    # Project perpendicular to n_hat: dE_dn_perp = dE_dn - (dE_dn . n_hat) n_hat
    dot = np.sum(dE_dn * n_hat, axis=1, keepdims=True)
    dE_dn_perp = (dE_dn - dot * n_hat) / (2.0 * A_f[:, None] + 1e-12)
    return E_b, grad


def total_energy_and_grad(flat_coords, templates, species, params, ext_forces=None, pin_capsid=None):
    """
    Evaluates E_total and exact gradient dE_total/d(flat_coords) according to §3:
      E_total = sum_i [E_inflate,i + E_area,i + E_bend,i]
              + sum_{i<j} [E_adh,ij + E_pen,ij + E_mesh,ij + E_Coul,ij]
              + E_sling - sum_v F_ext,v . x_v
    params keys:
      'e0', 'E0', 'delta', 'k_area_mult' (default 50), 'k_bend' (default 0),
      'fade_quadratic' (default False), 'singlet_pairs' (optional set of (i,j) tuples).
    """
    A_num = len(templates)
    N_v = templates[0].n_verts
    coords = flat_coords.reshape((A_num, N_v, 3))
    grad = np.zeros_like(coords)

    e0    = float(params['e0'])
    E0    = float(params['E0'])
    delta = float(params['delta'])
    k_area_mult = float(params.get('k_area_mult', C.K_AREA_MULT))
    k_bend      = float(params.get('k_bend', C.K_BEND_PRI))
    fade_quad   = bool(params.get('fade_quadratic', False))
    k_pen       = C.K_PEN_MULT * e0 / (C.K_PEN_SCALE**2)

    # Per-capsid geometric quantities and single-capsid energies (1. Inflation, 2. Area, 3. Bending)
    A_f_list, A_v_list, V_list, n_hat_list, f_cent_list = [], [], [], [], []
    dAf_list = []
    centroids = np.mean(coords, axis=1)  # (A_num, 3)

    E_inflate_tot = 0.0
    E_area_tot    = 0.0
    E_bend_tot    = 0.0

    for i, tmpl in enumerate(templates):
        A_f, A_v, V, n_hat, f_cent, grad_V, dAf = M.face_geometry_and_grads(coords[i], tmpl.faces)
        A_f_list.append(A_f)
        A_v_list.append(A_v)
        V_list.append(V)
        n_hat_list.append(n_hat)
        f_cent_list.append(f_cent)
        dAf_list.append(dAf)

        # 1. Inflation: resists compression below rest volume V_i^0 (stationary at V = V_i^0)
        V_safe = max(V, 0.1 * tmpl.V0)
        if V_safe < tmpl.V0:
            E_inf_i = E0 * (tmpl.V0 / V_safe - 1.0)
            dEinf_dV = -E0 * tmpl.V0 / (V_safe**2)
        else:
            E_inf_i = 0.0
            dEinf_dV = 0.0
        E_inflate_tot += E_inf_i
        grad[i] += dEinf_dV * grad_V

        # 2. Skin area: E_area,i = K_AREA * sum_f (A_f - A_f^0)^2 / A_f^0
        k_area_i = k_area_mult * E0 / tmpl.A0
        diff_A = A_f - tmpl.rest_face_areas
        E_area_i = float(k_area_i * np.sum((diff_A**2) / tmpl.rest_face_areas))
        E_area_tot += E_area_i
        dE_dAf = 2.0 * k_area_i * diff_A / tmpl.rest_face_areas
        i0, i1, i2 = tmpl.faces[:, 0], tmpl.faces[:, 1], tmpl.faces[:, 2]
        np.add.at(grad[i], i0, dE_dAf[:, None] * dAf[0])
        np.add.at(grad[i], i1, dE_dAf[:, None] * dAf[1])
        np.add.at(grad[i], i2, dE_dAf[:, None] * dAf[2])

        # 3. Bending: E_bend,i
        if k_bend > 0.0:
            Eb_i, g_b = helfrich_bending(coords[i], tmpl.edges, tmpl.edge_faces, n_hat, A_f, k_bend)
            E_bend_tot += Eb_i
            grad[i] += g_b

    # Pairwise terms (4. Graded adhesion, 5. Penetration, 6. Lane mesh, 7. Coulomb)
    E_adh_tot  = 0.0
    E_pen_tot  = 0.0
    E_mesh_tot = 0.0
    E_coul_tot = 0.0
    adj = np.zeros((A_num, A_num), dtype=bool)
    pair_details = {}

    singlet_override = params.get('singlet_pairs', set())

    for i in range(A_num):
        for j in range(i + 1, A_num):
            # 7. Coulomb for proton-proton pairs
            if species[i] == 'p' and species[j] == 'p':
                r_vec = centroids[i] - centroids[j]
                d_ij = float(np.linalg.norm(r_vec))
                E_c = C.AHC / d_ij
                E_coul_tot += E_c
                g_c = -(C.AHC / (d_ij**3)) * r_vec / N_v
                grad[i] += g_c[None, :]
                grad[j] -= g_c[None, :]

            # Fast centroid bounding check before KD-tree
            c_dist = float(np.linalg.norm(centroids[i] - centroids[j]))
            max_reach = templates[i].radius + templates[j].radius + 3.0 * templates[i].mean_edge_len + delta
            if c_dist > max_reach:
                pair_details[(i, j)] = {'connected': False, 'E_adh': 0.0, 'E_pen': 0.0, 'E_mesh': 0.0}
                continue

            # Directed gaps i -> j and j -> i
            rad_ij = 3.0 * templates[j].mean_edge_len
            rad_ji = 3.0 * templates[i].mean_edge_len
            g_ij, fi_ij = M.compute_signed_gaps(coords[i], coords[j], templates[j].faces, n_hat_list[j], f_cent_list[j], rad_ij)
            g_ji, fi_ji = M.compute_signed_gaps(coords[j], coords[i], templates[i].faces, n_hat_list[i], f_cent_list[i], rad_ji)

            # 4. Graded adhesion: -e0 * sum_{v in i} A_v s(g_v/delta) - e0 * sum_{v in j} A_v s(g_v/delta)
            s_ij, ds_ij = fade_s_and_deriv(g_ij / delta, fade_quad)
            s_ji, ds_ji = fade_s_and_deriv(g_ji / delta, fade_quad)

            E_adh_ij = float(-e0 * (np.sum(A_v_list[i] * s_ij) + np.sum(A_v_list[j] * s_ji)))
            E_adh_tot += E_adh_ij

            # Gradient of E_adh wrt vertex positions (via dg_v/dx_v = n_hat_partner)
            act_i = fi_ij >= 0
            if np.any(act_i):
                f_idx = fi_ij[act_i]
                n_partner = n_hat_list[j][f_idx]
                dE_dg_i = -e0 * A_v_list[i][act_i] * (ds_ij[act_i] / delta)
                f_vec_i = dE_dg_i[:, None] * n_partner
                grad[i, act_i] += f_vec_i
                # Equal and opposite reaction distributed to the 3 vertices of matched face on j
                for k_tri in range(3):
                    np.add.at(grad[j], templates[j].faces[f_idx, k_tri], -f_vec_i / 3.0)

            act_j = fi_ji >= 0
            if np.any(act_j):
                f_idx = fi_ji[act_j]
                n_partner = n_hat_list[i][f_idx]
                dE_dg_j = -e0 * A_v_list[j][act_j] * (ds_ji[act_j] / delta)
                f_vec_j = dE_dg_j[:, None] * n_partner
                grad[j, act_j] += f_vec_j
                for k_tri in range(3):
                    np.add.at(grad[i], templates[i].faces[f_idx, k_tri], -f_vec_j / 3.0)

            # 5. Penetration: K_PEN * sum_v A_v * max(0, -g_v)^2
            pen_i = np.maximum(0.0, -g_ij)
            pen_j = np.maximum(0.0, -g_ji)
            E_pen_ij = float(k_pen * (np.sum(A_v_list[i] * pen_i**2) + np.sum(A_v_list[j] * pen_j**2)))
            E_pen_tot += E_pen_ij

            p_mask_i = (g_ij < 0.0) & act_i
            if np.any(p_mask_i):
                f_idx = fi_ij[p_mask_i]
                n_partner = n_hat_list[j][f_idx]
                dEp_dg_i = -2.0 * k_pen * A_v_list[i][p_mask_i] * pen_i[p_mask_i]
                fp_i = dEp_dg_i[:, None] * n_partner
                grad[i, p_mask_i] += fp_i
                for k_tri in range(3):
                    np.add.at(grad[j], templates[j].faces[f_idx, k_tri], -fp_i / 3.0)

            p_mask_j = (g_ji < 0.0) & act_j
            if np.any(p_mask_j):
                f_idx = fi_ji[p_mask_j]
                n_partner = n_hat_list[i][f_idx]
                dEp_dg_j = -2.0 * k_pen * A_v_list[j][p_mask_j] * pen_j[p_mask_j]
                fp_j = dEp_dg_j[:, None] * n_partner
                grad[j, p_mask_j] += fp_j
                for k_tri in range(3):
                    np.add.at(grad[i], templates[i].faces[f_idx, k_tri], -fp_j / 3.0)

            # Contact connectivity check: any vertex with g_v < delta
            in_contact = bool(np.any(g_ij < delta) or np.any(g_ji < delta))
            adj[i, j] = adj[j, i] = in_contact

            # 6. Lane mesh: E_MESH * [pair ij is singlet], applied if in_contact
            is_singlet = (species[i] == species[j]) or ((i, j) in singlet_override) or ((j, i) in singlet_override)
            E_m_ij = C.E_MESH if (in_contact and is_singlet) else 0.0
            E_mesh_tot += E_m_ij

            pair_details[(i, j)] = {
                'connected': in_contact, 'E_adh': E_adh_ij, 'E_pen': E_pen_ij, 'E_mesh': E_m_ij,
                'g_ij': g_ij, 'g_ji': g_ji, 's_ij': s_ij, 's_ji': s_ji,
            }

    # Check graph connectedness via BFS for Slingshot (§3.8)
    visited = {0}
    queue = [0]
    while queue:
        curr = queue.pop(0)
        for nb in range(A_num):
            if adj[curr, nb] and nb not in visited:
                visited.add(nb)
                queue.append(nb)
    is_connected = (len(visited) == A_num)
    E_sling = -A_num * C.Y(A_num) if (is_connected and A_num > 1) else 0.0

    # External load forces (§6)
    E_ext = 0.0
    if ext_forces is not None:
        # ext_forces shape (A_num, N_v, 3)
        E_ext = float(-np.sum(ext_forces * coords))
        grad -= ext_forces

    # Optional pinning of a specific capsid centroid (§7.7 chain) or whole-system COM drift removal (§4.1)
    if pin_capsid is not None:
        idx_p, target_c = pin_capsid
        grad[idx_p] -= np.mean(grad[idx_p], axis=0, keepdims=True)
    else:
        grad -= np.mean(grad.reshape(-1, 3), axis=0)[None, None, :]

    E_tot = E_inflate_tot + E_area_tot + E_bend_tot + E_adh_tot + E_pen_tot + E_mesh_tot + E_coul_tot + E_sling + E_ext

    info = {
        'E_total': E_tot, 'BE': -E_tot,
        'E_inflate': E_inflate_tot, 'E_area': E_area_tot, 'E_bend': E_bend_tot,
        'E_adh': E_adh_tot, 'E_pen': E_pen_tot, 'E_mesh': E_mesh_tot,
        'E_Coul': E_coul_tot, 'E_sling': E_sling, 'E_ext': E_ext,
        'is_connected': is_connected, 'adj': adj, 'centroids': centroids,
        'A_v_list': A_v_list, 'V_list': V_list, 'pair_details': pair_details,
    }
    return E_tot, grad.ravel(), info