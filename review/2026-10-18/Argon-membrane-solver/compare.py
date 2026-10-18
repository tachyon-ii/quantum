# models/binding/membrane/compare.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
# GUARDRAIL (§2, §8): The ONLY module permitted to import targets.py.
import targets as T


def append_comparison_to_report(results_by_delta, report_path='report.md'):
    """Appends the §10 comparison table against targets.py to report.md."""
    lines = [
        "\n---\n",
        "## 8. Comparison Against `targets.py` (Appended by `compare.py`)\n",
        "| delta (fm) | Nucleus | BE_model (MeV) | BE_target (MeV) | BE diff (%) | E_bond_model (MeV) | E_bond_req (MeV) | d_eq_model (fm) | d_rms_quantum (fm) | R_ch_model (fm) | R_ch_target (fm) |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    t_be = {'D': 2.224566, 'T': T.BE_T, 'He3': T.BE_HE3, 'He4': 28.29566}
    t_rch = {'D': T.RCH_D, 'T': T.RCH_T, 'He3': T.RCH_HE3, 'He4': T.RCH_HE4}

    for d_key, res in results_by_delta.items():
        for nuc in ('D', 'T', 'He3', 'He4'):
            nr = res['nuclei'][nuc]
            be_m = nr['BE_MeV']
            be_t = t_be[nuc]
            pct = 100.0 * (be_m / be_t - 1.0)
            eb_m = nr['E_bond_per_pair_MeV']
            eb_t = T.EBOND_REQ[nuc]
            d_m  = nr['d_mean_fm']
            d_q  = T.D_RMS_QUANTUM[nuc]
            rc_m = nr['R_ch_fm']
            rc_t = t_rch[nuc]
            lines.append(
                f"| {res['delta']:.4f} | {nuc} | {be_m:.4f} | {be_t:.4f} | {pct:+.2f}% | "
                f"{eb_m:.4f} | {eb_t:.4f} | {d_m:.4f} | {d_q:.3f} | {rc_m:.4f} | {rc_t:.3f} |"
            )

    lines.append(
        "\n*Classical minimum caveat (§5, §7.1):* `d_eq_model` and `R_ch_model` are static classical energy-minimum "
        "positions of the contacting skins and systematically underestimate the quantum-averaged rms values "
        "`d_rms_quantum` and `R_ch_target`, which include zero-point wave-function tails.\n"
    )
    with open(report_path, 'a', encoding='utf-8') as f:
        f.write('\n'.join(lines))