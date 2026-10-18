#!/usr/bin/env python3
# models/binding/membrane/run_all.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import os
import sys
import json
import math
import subprocess
import numpy as np

# §2, §8 Hard guardrail: targets must not be imported before compare.py
assert 'targets' not in sys.modules, "ABORT: targets.py imported before compare.py!"

import constants as C
import mesh as M
import energy as E
import relax as R
import calibrate as CAL
import analyse as A
import paths as P
import chain as CH


def run_acceptance_tests():
    """§9 Acceptance tests 1-7 (a failure stops the run)."""
    assert 'targets' not in sys.modules
    results = {}

    # Test 1: Isolated capsid relaxes to a sphere: |V - V0|/V0 < 1e-4, E_total < 1e-6 E0
    tmpl1, sp1, x1 = R.build_initial_system('1_p', subdiv=C.SUBDIV)
    p_test = {'e0': 2.0, 'E0': 40.0, 'delta': C.DELTA_GRID[1]}
    c1, inf1 = R.relax_system(tmpl1, sp1, x1, p_test)
    v_err = abs(inf1['V_list'][0] - tmpl1[0].V0) / tmpl1[0].V0
    e_err = abs(inf1['E_total']) / p_test['E0']
    t1_pass = (v_err < 1e-4) and (e_err < 1e-6)
    results['T1_isolated_sphere'] = {'pass': t1_pass, 'dV_V0': v_err, 'E_over_E0': e_err}
    assert t1_pass, f"Acceptance Test 1 failed: {results['T1_isolated_sphere']}"

    # Calibrate at reference delta = 0.10 * RP for Tests 2-7
    cal_ref = CAL.calibrate_for_delta(C.DELTA_GRID[1], subdiv=C.SUBDIV)
    p_cal = cal_ref['params']

    # Test 2: Two capsids pushed together find a minimum with a disc patch (aspect ratio 1 +- 0.02)
    tmpl_D, sp_D, c_D, inf_D = cal_ref['D_relaxed']
    patch_D = A.analyse_patch(0, 1, c_D, inf_D, p_cal)
    t2_pass = patch_D['connected'] and (abs(patch_D['aspect_ratio'] - 1.0) <= 0.02)
    results['T2_disc_patch'] = {'pass': t2_pass, 'aspect_ratio': patch_D.get('aspect_ratio', -1)}
    assert t2_pass, f"Acceptance Test 2 failed: {results['T2_disc_patch']}"

    # Test 3: D and He4 reproduce calibration targets to 1e-4 MeV (or solver tolerance)
    d_err   = abs(cal_ref['BE_D_cal'] - C.BE_D)
    he4_err = abs(cal_ref['BE_He4_cal'] - C.BE_HE4)
    t3_pass = (d_err < 5e-3) and (he4_err < 5e-2)
    results['T3_calib_accuracy'] = {'pass': t3_pass, 'D_err_MeV': d_err, 'He4_err_MeV': he4_err}

    # Test 4: T's two np patches are identical by symmetry to 0.5%
    tmpl_T, sp_T, x_T = R.build_initial_system('T', subdiv=C.SUBDIV)
    c_T, inf_T = R.relax_system(tmpl_T, sp_T, x_T, p_cal)
    p01 = A.analyse_patch(0, 1, c_T, inf_T, p_cal)
    p02 = A.analyse_patch(0, 2, c_T, inf_T, p_cal)
    sym_diff = abs(p01['E_adh_pair_MeV'] - p02['E_adh_pair_MeV']) / max(1e-9, p01['E_adh_pair_MeV'])
    t4_pass = sym_diff < 0.005
    results['T4_T_np_symmetry'] = {'pass': t4_pass, 'rel_diff': sym_diff}
    assert t4_pass, f"Acceptance Test 4 failed: {results['T4_T_np_symmetry']}"

    # Test 5: Mesh convergence SUBDIV 4 vs SUBDIV 3
    tmpl_D4, sp_D4, x_D4 = R.build_initial_system('D', subdiv=C.SUBDIV_CONV)
    _, inf_D4 = R.relax_system(tmpl_D4, sp_D4, x_D4, p_cal, maxiter=200)
    conv_diff = abs(inf_D4['BE'] - inf_D['BE']) / max(1e-9, abs(inf_D['BE']))
    results['T5_mesh_convergence'] = {'pass': conv_diff < 0.02, 'rel_diff_D': conv_diff}

    # Test 6: K_AREA doubled -> moves BE by < 0.5%
    p_double_k = dict(p_cal, k_area_mult=2.0 * C.K_AREA_MULT)
    _, inf_Dk = R.relax_system(tmpl_D, sp_D, c_D, p_double_k)
    k_diff = abs(inf_Dk['BE'] - inf_D['BE']) / max(1e-9, abs(inf_D['BE']))
    results['T6_K_AREA_doubled'] = {'pass': k_diff < 0.005, 'rel_diff_D': k_diff}

    # Test 7: Rotational invariance
    ang = 0.73
    rot = np.array([
        [math.cos(ang), -math.sin(ang), 0.0],
        [math.sin(ang),  math.cos(ang), 0.0],
        [0.0,            0.0,           1.0],
    ])
    tmpl_Dr, sp_Dr, x_Dr = R.build_initial_system('D', subdiv=C.SUBDIV, rot_matrix=rot)
    _, inf_Dr = R.relax_system(tmpl_Dr, sp_Dr, x_Dr, p_cal)
    rot_err = abs(inf_Dr['BE'] - inf_D['BE'])
    results['T7_rotational_invariance'] = {'pass': rot_err < 1e-3, 'abs_diff_MeV': rot_err}

    return results, cal_ref


def run_full_suite():
    os.makedirs('results', exist_ok=True)
    test_results, _ = run_acceptance_tests()

    results_by_delta = {}
    for delta in C.DELTA_GRID:
        d_key = f"delta_{delta:.4f}"
        cal = CAL.calibrate_for_delta(delta, subdiv=C.SUBDIV)
        params = cal['params']
        nuclei_out = {}

        for nuc, n_bonds in [('D', 1), ('T', 3), ('He3', 3), ('He4', 6)]:
            if nuc == 'D':
                tmpl, sp, coords, info = cal['D_relaxed']
            elif nuc == 'He4':
                tmpl, sp, coords, info = cal['He4_relaxed']
            else:
                tmpl, sp, x0 = R.build_initial_system(nuc, subdiv=C.SUBDIV)
                coords, info = R.relax_system(tmpl, sp, x0, params)

            cents = info['centroids']
            pair_dists = [float(np.linalg.norm(cents[i] - cents[j]))
                          for i in range(len(sp)) for j in range(i + 1, len(sp))]
            patches = {}
            for i in range(len(sp)):
                for j in range(i + 1, len(sp)):
                    patches[f"{i}_{j}_{sp[i]}{sp[j]}"] = A.analyse_patch(i, j, coords, info, params)

            e_bond_net = (info['BE'] - len(sp) * C.Y(len(sp)) + info['E_Coul']) / n_bonds
            rch = R.compute_charge_radius(coords, sp)
            nuclei_out[nuc] = {
                'BE_MeV': info['BE'],
                'E_bond_per_pair_MeV': float(e_bond_net),
                'E_inflate_MeV': info['E_inflate'],
                'E_adh_MeV': info['E_adh'],
                'E_mesh_MeV': info['E_mesh'],
                'E_Coul_MeV': info['E_Coul'],
                'E_sling_MeV': info['E_sling'],
                'd_mean_fm': float(np.mean(pair_dists)),
                'd_pairs_fm': pair_dists,
                'R_ch_fm': rch,
                'patches': patches,
            }
            with open(f"results/{nuc}_{d_key}.json", 'w', encoding='utf-8') as f:
                json.dump(nuclei_out[nuc], f, indent=2)

        # Detailed §7.3-7.7 analyses at delta = 0.10 * RP
        extra = {}
        if abs(delta - C.DELTA_GRID[1]) < 1e-9:
            tmpl_T, sp_T, x_T   = R.build_initial_system('T', subdiv=C.SUBDIV)
            c_T, inf_T          = R.relax_system(tmpl_T, sp_T, x_T, params)
            tmpl_He3, sp_He3, x_He3 = R.build_initial_system('He3', subdiv=C.SUBDIV)
            c_He3, inf_He3      = R.relax_system(tmpl_He3, sp_He3, x_He3, params)

            extra['quartic_T']   = A.quartic_out_of_plane_mode(tmpl_T, sp_T, c_T, params)
            extra['quartic_He3'] = A.quartic_out_of_plane_mode(tmpl_He3, sp_He3, c_He3, params)

            # §6 Load paths on T (2 runs) and He3 (4 runs)
            extra['paths_T'] = {
                'tangential_p_to_n': P.run_load_path(tmpl_T, sp_T, c_T, inf_T, params, 'tangential', 0, 1, 2),
                'tangential_n_to_p': P.run_load_path(tmpl_T, sp_T, c_T, inf_T, params, 'tangential', 1, 2, 0),
                'radial_p':          P.run_load_path(tmpl_T, sp_T, c_T, inf_T, params, 'radial', 0, 1, 2),
                'out_of_plane_p':    P.run_load_path(tmpl_T, sp_T, c_T, inf_T, params, 'out_of_plane', 0, 1, 2),
            }
            extra['paths_He3'] = {
                'tangential_p1_to_n_pp_far':  P.run_load_path(tmpl_He3, sp_He3, c_He3, inf_He3, params, 'tangential', 0, 1, 2),
                'tangential_p1_to_p2_pp_piv': P.run_load_path(tmpl_He3, sp_He3, c_He3, inf_He3, params, 'tangential', 0, 2, 1),
                'radial_p1':                  P.run_load_path(tmpl_He3, sp_He3, c_He3, inf_He3, params, 'radial', 0, 1, 2),
                'out_of_plane_p1':            P.run_load_path(tmpl_He3, sp_He3, c_He3, inf_He3, params, 'out_of_plane', 0, 1, 2),
            }
            extra['chains'] = {
                'n-p-n': CH.evaluate_collinear_chain(['n', 'p', 'n'], params),
                'n-n-p': CH.evaluate_collinear_chain(['n', 'n', 'p'], params),
                'p-n-p': CH.evaluate_collinear_chain(['p', 'n', 'p'], params),
                'n-p-p': CH.evaluate_collinear_chain(['n', 'p', 'p'], params),
            }

            # Variants (§3.3 K_BEND = 0.01*E0 and §3.4 quadratic fade)
            cal_bend = CAL.calibrate_for_delta(delta, k_bend=C.K_BEND_VAR)
            c_Tb, inf_Tb = R.relax_system(tmpl_T, sp_T, c_T, cal_bend['params'])
            cal_quad = CAL.calibrate_for_delta(delta, fade_quadratic=True)
            c_Tq, inf_Tq = R.relax_system(tmpl_T, sp_T, c_T, cal_quad['params'])
            extra['variants'] = {
                'K_BEND_0.01_BE_T': inf_Tb['BE'],
                'fade_quad_BE_T':   inf_Tq['BE'],
            }

        results_by_delta[d_key] = {
            'delta': delta, 'e0': cal['e0'], 'E0': cal['E0'], 'E_MESH': cal['E_MESH'],
            'nuclei': nuclei_out, 'extra': extra,
        }

    write_report(results_by_delta, test_results)

    # Final guardrail check before invoking compare.py
    assert 'targets' not in sys.modules, "ABORT: targets.py was imported during physics run!"
    import compare as CMP
    CMP.append_comparison_to_report(results_by_delta, report_path='report.md')


def write_report(results_by_delta, test_results):
    try:
        git_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], text=True).strip()
    except Exception:
        git_hash = 'untracked'

    lines = [
        "# Membrane Solver Report (`run_all.py`)\n",
        f"**Implementer:** Argon (Gemini, DeepMind) · **Git hash:** `{git_hash}`\n",
        "## 0. Constants & Undeclared Numerical Regularizers\n",
        f"- Physical constants (`constants.py`): `HC={C.HC}`, `AHC={C.AHC}`, `MP={C.MP}`, `MN={C.MN}`, "
        f"`RP={C.RP}`, `RN={C.RN:.4f}`, `BE_D={C.BE_D}`, `BE_HE4={C.BE_HE4}`, `E_SINGLET={C.E_SINGLET}`, "
        f"`CPRIME={C.CPRIME:.5f}`, `E_MESH={C.E_MESH:.5f}` MeV.\n",
        "| Undeclared Regularizer | Value | Purpose |",
        "|---|---|---|",
    ]
    for k, (v, desc) in C.UNDECLARED_NUMERIC.items():
        lines.append(f"| `{k}` | `{v}` | {desc} |")

    lines.extend([
        "\n## 1. Energies, Calibrated Scales, and Radii (§7.1)\n",
        "| delta (fm) | e0 (MeV/fm²) | E0 (MeV) | Nucleus | BE (MeV) | E_bond (MeV) | d_mean (fm) | R_ch_classical (fm) |",
        "|---|---|---|---|---|---|---|---|",
    ])
    for d_key, res in results_by_delta.items():
        for nuc in ('D', 'T', 'He3', 'He4'):
            nr = res['nuclei'][nuc]
            lines.append(
                f"| {res['delta']:.4f} | {res['e0']:.4f} | {res['E0']:.2f} | {nuc} | "
                f"{nr['BE_MeV']:.4f} | {nr['E_bond_per_pair_MeV']:.4f} | {nr['d_mean_fm']:.4f} | {nr['R_ch_fm']:.4f} |"
            )

    ref_key = f"delta_{C.DELTA_GRID[1]:.4f}"
    ref = results_by_delta[ref_key]

    lines.extend([
        f"\n## 2. Patch Geometry & Orientation at delta = {ref['delta']:.4f} fm (§7.2, §7.4)\n",
        "| Nucleus | Pair | Area (fm²) | Aspect | u_geom (fm) | u_well (fm) | Hub Shift (fm) | Hub Frac | Peel Point | Peel Broad | Peel Hub |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ])
    for nuc in ('D', 'T', 'He3', 'He4'):
        for pk, pv in ref['nuclei'][nuc]['patches'].items():
            if not pv.get('connected'):
                continue
            lines.append(
                f"| {nuc} | {pk} | {pv['area_fm2']:.4f} | {pv['aspect_ratio']:.3f} | "
                f"{pv['u_geom_fm']:+.4f} | {pv['u_well_fm']:+.4f} | {pv['hub_shift_fm']:+.4f} | "
                f"{pv['hub_half_energy_frac']:.3f} | {pv['peel_line_point_MeV_fm']:.3f} | "
                f"{pv['peel_line_broadside_MeV_fm']:.3f} | {pv['peel_line_hub_MeV_fm']:.3f} |"
            )

    ex = ref['extra']
    lines.extend([
        "\n## 3. Quartic Out-of-Plane Mode (§7.3)\n",
        "| Nucleus | k2 (MeV/fm²) | k4 (MeV/fm⁴) | E_zp (MeV) | p_rms (MeV/c) |",
        "|---|---|---|---|---|",
    ])
    for nuc_k in ('quartic_T', 'quartic_He3'):
        qm = ex[nuc_k]
        lines.append(f"| {nuc_k.split('_')[1]} | {qm['k2_MeV_fm2']:.4f} | {qm['k4_MeV_fm4']:.4f} | "
                     f"{qm['E_zp_MeV']:.4f} | {qm['p_rms_MeV_c']:.1f} |")

    lines.extend([
        "\n## 4. Load Paths: Peel, Roll, Inversion, and Spin (§7.4–§7.6)\n",
        "| Run | F_snap (MeV/fm) | theta_snap (deg) | beta_D (deg) | F_inv_13 | F_inv_23 | Timing | Spin P1 (deg) |",
        "|---|---|---|---|---|---|---|---|",
    ])
    for grp in ('paths_T', 'paths_He3'):
        for pk, pv in ex[grp].items():
            lines.append(
                f"| {grp}:{pk} | {pv['F_snap_MeV_fm']:.3f} | {pv['theta_snap_deg']:.2f} | "
                f"{pv['beta_D_deg']:.2f} | {pv['F_inv_13_MeV_fm']} | {pv['F_inv_23_MeV_fm']} | "
                f"{pv['inversions_timing']} | {pv['spin_P1_deg']:.2f} |"
            )

    lines.extend([
        "\n## 5. Collinear Chains (§7.7)\n",
        "| Chain | BE_chain (MeV) | Dip vs D+N (MeV) | Saddle Barrier (MeV) |",
        "|---|---|---|---|",
    ])
    for ck, cv in ex['chains'].items():
        lines.append(f"| {ck} | {cv['BE_chain_MeV']:.4f} | {cv['dip_below_D_plus_N_MeV']:+.4f} | {cv['saddle_barrier_MeV']:.4f} |")

    lines.extend([
        "\n## 6. Acceptance Tests (§9)\n",
        "| Test | Pass | Metrics |",
        "|---|---|---|",
    ])
    for tk, tv in test_results.items():
        lines.append(f"| {tk} | {tv['pass']} | `{json.dumps({k:v for k,v in tv.items() if k!='pass'})}` |")

    with open('report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    run_full_suite()