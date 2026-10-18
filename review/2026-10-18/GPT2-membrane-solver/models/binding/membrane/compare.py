#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""The ONLY importer of targets.py. Invoked after all computation and report writing."""
from __future__ import annotations
from . import constants as C
from .reporting import table, write_json


def append_comparison(report_path, nuclei, results_dir):
    from . import targets
    be_targets = {'D': C.BE_D, 'T': targets.BE_T, 'He3': targets.BE_HE3, 'He4': C.BE_HE4}
    radius_targets = {'D': targets.RCH_D, 'T': targets.RCH_T, 'He3': targets.RCH_HE3, 'He4': targets.RCH_HE4}
    rows = []
    for name, data in nuclei.items():
        cases = [case for case in data.get('cases', []) if case.get('status') == 'relaxed']
        if not cases:
            cases = [{'variant': 'not run', 'delta_ratio': None, 'observables': {}}]
        for case in cases:
            observables = case.get('observables', {})
            for label, key, expected in (
                    ('BE', 'binding_energy', be_targets[name]),
                    ('charge radius', 'charge_radius_fm', radius_targets[name]),
                    ('per-bond corrected energy', 'per_bond_after_sling_and_coulomb', targets.PER_BOND[name]),
                    ('rms centroid distance', 'rms_pair_centroid_distance', targets.QUANTUM_RMS_CENTROID_DISTANCES[name])):
                actual = observables.get(key)
                rows.append({'nucleus': name, 'variant': case['variant'], 'delta_ratio': case['delta_ratio'],
                    'quantity': label, 'model': actual, 'target': expected,
                    'residual': actual - expected if actual is not None else None,
                    'role': 'calibration input' if label == 'BE' and name in ('D', 'He4') else 'held-out comparison'})
    write_json(results_dir / 'comparison.json', {'status': 'comparison_only_no_feedback', 'rows': rows})
    with report_path.open('a') as handle:
        handle.write('\n## Comparison — sealed targets, appended last\n\n')
        handle.write(table(('Nucleus', 'Variant', 'δ/RP', 'Quantity', 'Model', 'Target', 'Residual', 'Role'),
            ((r['nucleus'], r['variant'], r['delta_ratio'], r['quantity'], r['model'], r['target'], r['residual'], r['role']) for r in rows)))
        handle.write('\nClassical minima are not quantum rms averages. The spec’s expected underestimation is a caveat, not an enforced outcome; no measured rms distance entered the contact calculation.\n')
