#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Strict JSON, provenance, and deterministic tables from actual run records."""
from __future__ import annotations
from dataclasses import is_dataclass, asdict
from pathlib import Path
import hashlib
import json
import math
import platform
import subprocess
import sys
import numpy as np
from . import constants as C

IMPLEMENTER = 'OpenAI ChatGPT — GPT-6 Astra Pro'


def plain(value):
    if is_dataclass(value):
        return plain(asdict(value))
    if isinstance(value, np.ndarray):
        return plain(value.tolist())
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [plain(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return float(value) if math.isfinite(value) else None
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, Path):
        return str(value)
    return value


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(plain(value), indent=C.JSON_INDENT, allow_nan=False, sort_keys=True) + '\n')
    temporary.replace(path)


def number(value):
    if value is None:
        return 'not available'
    if isinstance(value, (float, np.floating)):
        return format(float(value), f'.{C.REPORT_DIGITS}g')
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(plain(value), separators=(',', ':'))
    return str(value)


def table(headers, rows):
    def cell(value):
        return number(value).replace('|', '\\|').replace('\n', ' ')
    rows = list(rows)
    return '\n'.join(['| ' + ' | '.join(map(cell, headers)) + ' |',
                      '| ' + ' | '.join('---' for _ in headers) + ' |'] +
                     ['| ' + ' | '.join(map(cell, row)) + ' |' for row in rows]) + '\n'


def provenance(root: Path):
    def git(*args):
        p = subprocess.run(['git', *args], cwd=root, text=True, capture_output=True)
        return p.stdout.strip() if p.returncode == 0 else None
    try:
        commit = git('rev-parse', 'HEAD')
        dirty = git('status', '--porcelain', '--untracked-files=no')
    except FileNotFoundError:
        commit, dirty = None, None
    digest = hashlib.sha256()
    source_files = []
    own_sources = list((root / 'models').rglob('*.py')) + list(root.glob('*.py'))
    for p in sorted(own_sources):
        if '.git' in p.parts:
            continue
        rel = p.relative_to(root).as_posix()
        data = p.read_bytes()
        digest.update(rel.encode()); digest.update(data)
        source_files.append({'file': rel, 'sha256': hashlib.sha256(data).hexdigest()})
    spec = root / 'BUILD-SPEC-membrane-solver.md'
    import scipy, torch
    return {'implementer': IMPLEMENTER, 'git_hash': commit, 'git_dirty_tracked_files': bool(dirty) if dirty is not None else None,
            'source_tree_sha256': digest.hexdigest(), 'source_files': source_files,
            'spec_sha256': hashlib.sha256(spec.read_bytes()).hexdigest() if spec.exists() else None,
            'python': sys.version, 'numpy': np.__version__, 'scipy': scipy.__version__,
            'torch': torch.__version__, 'platform': platform.platform(),
            'gradient_backend': 'PyTorch float64 autograd; SciPy L-BFGS-B',
            'precision': 'float64', 'torch_threads': C.TORCH_THREADS}


CONVENTIONS = [
    'The supplied build document is the physics source. Referenced companion physics documents were not supplied and their contents are not presumed.',
    'Literal inflation, analytic rest volume/total area, and mesh face rest areas are retained; no pressure offset, isolated-energy subtraction, volume constraint, or renormalization is inserted.',
    'The mesh calibration follows the stated formula, even though the connected-graph slingshot makes its total-singlet interpretation inconsistent. Formula-derived values take precedence over rounded decimal claims.',
    'Local gap is minimum absolute distance to a candidate face plane, then signed by closed-surface inside/outside. The plane is not replaced by nearest triangle distance.',
    'Outside vertices without a local candidate have no local contact. Inside vertices without a candidate make the literal objective undefined and stop that relaxation. This missing-neighbour convention is an added interpretation.',
    'Candidate faces, inside signs and graph switches are recomputed at every evaluation; they are discrete. Autograd includes both participating skins within each branch. No smoothing or frozen-neighbour shortcut is used.',
    'No self-intersection barrier or additional skin shear regularizer is supplied; none is inserted. Nonpositive volumes and degenerate faces are rejected as undefined geometries.',
    'The lane mesh is a per-contact constant, so it contributes no continuous shear derivative on a fixed contact branch. It is not replaced by a spring.',
    'Global contact-graph slingshot is not cluster separable: a disconnected dimer inside a larger calculation does not receive the standalone dimer slingshot. The literal rule is retained.',
    'Gradient tolerance is checked independently of optimizer success. Invalid trial geometry, line-search exhaustion and wall-time limits are not counted as minima or snap evidence.',
    'Acceptance tests requiring fitted parameters are dependency-staged after calibration. The isolated test and software checks precede any calibration; a failing scientific gate stops the production run.',
    'Primary, quadratic-well and bending variants are independently calibrated at each scanned reach. Area-penalty sensitivity and mesh-convergence comparisons hold calibration parameters fixed.',
    'A requested finer-mesh promotion repeats calibration and applicable gates at the promoted mesh, rather than using a coarse-mesh fit as a fine-mesh calibration.',
    'Patch areas use the specified lumped vertex quadrature on both skins. Perimeters are barycentric dual-cell boundaries; principal axes and hub biases are measured, never prescribed.',
    'Point/hub/broadside line energies use declared bins on the measured major axis. The build does not uniquely define front-width sampling; every bin and the estimator definition are recorded.',
    'The charge-radius origin is the mass-weighted nucleon centroid. Measured charge radii and unfolded rms distances remain sealed until comparison. The spec expects classical minima to underestimate quantum rms averages; no such inequality is forced.',
    'Force directions are fixed in the initial laboratory frame. Area-uniform nodal force weights are converged by outer reweighting; no derivative of weight redistribution is misidentified as an applied force.',
    'All listed particle labelings are run along all requested directions. Numerical failure is unresolved; first pair loss on converged continuation is an operational contact-loss load, not a mathematical proof of a saddle-node.',
    'The quartic scan freezes the shifted P1 vertex set and relaxes everything else with the system centroid pinned. No extra plane clamp is inserted; rigid rotations can relax away a laboratory-frame displacement.',
    'Quantum energies require a confining fitted polynomial and independently converged box and grid. The global polynomial extrapolation is explicitly reported. Unconfined or unresolved problems yield null, not a box artifact.',
    'The chain may bend after a collinear start. Sampled separation-profile maxima are saddle candidates, not certified full-dimensional saddles.',
    'The area-sensitivity comparison covers computed physical scalar families, excluding solver telemetry and discretization metadata; coordinate components are compared in the common pinned frame. Missing/defined changes fail. No uncomputed quantity is claimed to have passed.',
    'No prediction targets, fitted nuclear-specific crease factors, imposed egg profiles, or polarization-sign mappings enter the solver.',
]


def render_report(path: Path, state: dict):
    """Called by run_all.py. compare.py appends its sealed-target table LAST."""
    out = ['# Membrane solver — generated report', '<!-- Implementer: ' + IMPLEMENTER + ' -->',
           '', '## Constants', table(('Constant', 'Value', 'Source'),
              ((key, getattr(C, key), source) for key, source in C.PHYSICAL_SOURCES.items()))]
    provenance_data = state['provenance']
    out += ['Git hash: `' + str(provenance_data['git_hash']) + '`.',
            'Source-tree SHA-256: `' + provenance_data['source_tree_sha256'] + '`.',
            'Build-spec SHA-256: `' + str(provenance_data['spec_sha256']) + '`.',
            '', '## Run state', table(('Field', 'Value'), ((key, state.get(key)) for key in
                 ('status', 'stop_reason', 'mode', 'delta_grid', 'delta_grid_choice', 'runtime_budget_seconds', 'elapsed_seconds', 'exit_code'))),
            table(('Backend field', 'Value'), ((key, provenance_data[key]) for key in
                 ('gradient_backend', 'precision', 'python', 'numpy', 'scipy', 'torch', 'platform', 'git_dirty_tracked_files'))),
            '', '## Undeclared at spec time — added numerical constants',
            'Amber flag: added algorithmic constants and explicit interpretations are listed; none is hidden as a fitted physics parameter.',
            table(('Name', 'Value', 'Purpose'), ((key, value, reason) for key, (value, reason) in C.ADDED.items())),
            '', '## Spec-defined numerical settings', table(('Setting', 'Value'),
                ((key, getattr(C, key)) for key in ('SUBDIV', 'CONVERGENCE_SUBDIV', 'AREA_FACTOR', 'PEN_FACTOR',
                    'PEN_SCALE', 'BEND_PRIMARY', 'BEND_VARIANT', 'DELTA_GRID', 'NEIGHBOUR_REACH', 'GTOL',
                    'FORCE_STEP', 'Z_GRID', 'START_EDGE', 'START_TRI_X', 'START_TRI_Y')))]
    out += ['', '## Interpretation and implementation ledger']
    for line in CONVENTIONS:
        out += [line, '']
    out += ['## Pre-calibration audits']
    for item in state.get('acceptance', []):
        if item['test'] == 'A1_isolated_capsid':
            out += ['### All-vertex isolated relaxation', table(
                ('Skin', 'Subdivision', 'Vertices', 'Faces', 'V/V0 − 1 (absolute)', 'Allowed error', 'E_total', 'Max gradient', 'Converged', 'Gate'),
                ((r['species'], r['subdivision'], r['vertices'], r['faces'], r['relative_volume_error'],
                  r['allowed_volume_error'], r['E_total'], r['relaxation']['gradient_max'], r['relaxation']['converged'], r['passed'])
                 for r in item['measurements']['skins']))]
    audit = state.get('audits', {})
    if 'singlet' in audit:
        out += ['### Singlet arithmetic from the supplied formulas', table(('Quantity', 'Value'), audit['singlet'].items())]
    if 'uniform_scaling' in audit:
        out += ['### Independent uniform-scale check',
                'This scalar calculation checks the literal energy along a subset of the all-vertex degrees of freedom; it does not replace the solver.',
                table(('Subdivision', 'Area factor', 'Mesh A/A0', 'Mesh V/V0', 'Derivative at rest', 'Minimizing scale', 'E/E0', 'V/V0 − 1'),
                 ((r['subdivision'], r['area_factor'], r['mesh_area_over_analytic_area'], r['mesh_volume_over_analytic_volume'],
                   r['d_E_over_E0_d_scale_at_rest'], r['uniform_scale_minimum'], r['E_over_E0_at_scale_minimum'],
                   r['relative_volume_error_at_scale_minimum']) for r in audit['uniform_scaling']))]
    if 'isolated_variants' in audit:
        out += ['### Additional isolated diagnostics — not a bypass of the failed gate', table(
            ('Skin', 'Subdivision', 'Area factor', 'Bend fraction', 'Volume error', 'E_total', 'Converged', 'Gate'),
            ((r['species'], r['subdivision'], r['area_factor'], r['bend_fraction'], r['relative_volume_error'], r['E_total'],
              r['relaxation']['converged'], r['passed']) for test in audit['isolated_variants'] for r in test['measurements']['skins']))]
    if 'candidate_reach' in audit:
        out += ['### KD-neighbourhood reach audit', table(('Skin', 'Subdivision', 'δ/RP', 'δ (fm)', 'KD reach (fm)', 'Reach shorter than well'),
             ((r['species'], r['subdivision'], r['delta_ratio'], r['delta'], r['search_reach'], r['cuts_off_well']) for r in audit['candidate_reach']))]
    calibration_rows = list(state.get('calibrations', []))
    attempted = {(r['variant'], r['delta_ratio']) for r in calibration_rows}
    for variant in state.get('variant_plan', []):
        for ratio in state.get('delta_grid', []):
            if (variant, ratio) not in attempted:
                calibration_rows.append({'variant': variant, 'delta_ratio': ratio, 'subdivision': C.SUBDIV,
                                         'parameters': None, 'status': 'not_run_upstream_gate'})
    out += ['', '## Calibration scan', table(('Variant', 'δ/RP', 'Subdivision', 'e0', 'E0', 'State'),
           ((r['variant'], r['delta_ratio'], r['subdivision'], (r.get('parameters') or {}).get('e0'),
             (r.get('parameters') or {}).get('E0'), r['status']) for r in calibration_rows))]
    cases = [(nucleus, case) for nucleus, data in state['nuclei'].items() for case in data.get('cases', [])
             if case.get('status') == 'relaxed']
    if not cases:
        explanation = state.get('stop_reason') or 'No accepted production minima have been computed.'
        for heading in ('§7.1 Energies and radii', '§7.2 Patch geometry', '§7.3 Quartic mode',
                        '§7.4 Peel', '§7.5 Roll', '§7.6 Spin', '§7.7 Chain'):
            out += ['', '## ' + heading, table(('State', 'Reason'), [('not run', explanation)])]
    else:
        def tag(nucleus, case):
            return (nucleus, case['variant'], case['delta_ratio'])
        out += ['', '## §7.1 Energies and radii', table(('Nucleus', 'Variant', 'δ/RP', 'BE', 'Per-bond corrected', 'Charge radius', 'Pair distances'),
             ((*tag(n, c), c['observables']['binding_energy'], c['observables']['per_bond_after_sling_and_coulomb'],
               c['observables']['charge_radius_fm'], c['observables']['centroid_distances']) for n, c in cases))]
        out += ['', '## §7.2 Patch geometry', table(('Nucleus', 'Variant', 'δ/RP', 'Pair', 'Two-skin area', 'Two-skin perimeter', 'Aspect', 'Hub bias', 'Hub half fraction', 'Well centroid', 'Geometric centroid', 'Principal axes'),
             ((*tag(n, c), key, p['area'], p['two_skin_perimeter'], p['aspect_ratio'], p['hub_bias'], p['hub_half_fraction'],
               p['well_centroid'], p['geometric_centroid'], p.get('principal_axes')) for n, c in cases for key, p in c['patches'].items()))]
        out += ['', '## §7.3 Quartic mode', table(('Nucleus', 'Variant', 'δ/RP', 'State', 'k2', 'k4', 'E_zp', 'p_rms'),
             ((*tag(n, c), c.get('quartic', {}).get('status'), c.get('quartic', {}).get('k2'), c.get('quartic', {}).get('k4'),
               c.get('quartic', {}).get('quantum', {}).get('E_zp_MeV'), c.get('quartic', {}).get('quantum', {}).get('p_rms_MeV_c')) for n, c in cases if n in ('T', 'He3')))]
        out += ['', '## §7.4 Peel', table(('Nucleus', 'Variant', 'δ/RP', 'Pair', 'Skin', 'Point line energy', 'Broadside', 'Hub end'),
             ((*tag(n, c), key, skin['capsid'], skin['front_line_energies'].get('point'), skin['front_line_energies'].get('broadside'),
               skin['front_line_energies'].get('hub_end')) for n, c in cases for key, p in c['patches'].items() for skin in p['skins']))]
        out += [table(('Nucleus', 'Variant', 'δ/RP', 'Labeling', 'Path', 'Event', 'F_snap'),
             ((*tag(n, c), p['labeling']['name'], p['path'], p['event']['status'], p['event'].get('F_snap'))
              for n, c in cases for p in c.get('loads', {}).get('paths', []))),
                table(('Nucleus', 'Variant', 'δ/RP', 'Labeling', 'Ratio numerator', 'Ratio denominator', 'Ratio'),
             ((*tag(n, c), r['labeling'], r['numerator_path'], r['denominator_path'], r['ratio'])
              for n, c in cases for r in c.get('loads', {}).get('snap_ratios', [])))]
        out += ['', '## §7.5 Roll', table(('Nucleus', 'Variant', 'δ/RP', 'Labeling', 'θ_snap', 'P1P3 inversion', 'P2P3 inversion', 'Sequence', 'β_D'),
             ((*tag(n, c), p['labeling']['name'], p['motion']['theta_snap_rad'], p['motion']['P1P3_inversion'],
               p['motion']['P2P3_inversion'], p['motion']['inversion_sequence'], p['motion']['beta_D_rad'])
              for n, c in cases for p in c.get('loads', {}).get('paths', []) if p['motion'] is not None)),
                'Well-centroid trajectories, unzip fractions and every force-step contact map are retained in the nucleus JSON and snapshot files.']
        out += ['', '## §7.6 Spin', table(('Nucleus', 'Variant', 'δ/RP', 'Labeling', 'Spin at snap'),
             ((*tag(n, c), p['labeling']['name'], p['motion']['spin_at_snap'])
              for n, c in cases for p in c.get('loads', {}).get('paths', []) if p['motion'] is not None))]
        out += ['', '## §7.7 Chain', table(('Nucleus', 'Variant', 'δ/RP', 'State', 'Energy relative to D + N', 'Saddle candidates'),
             ((*tag(n, c), c.get('chain', {}).get('status'), c.get('chain', {}).get('energy_relative_D_plus_N'), c.get('chain', {}).get('saddle_candidates'))
              for n, c in cases if n in ('T', 'He3')))]
    out += ['', '## §9 Acceptance tests', table(('Test', 'State', 'Reason'),
              ((test['test'], test['status'], test.get('reason')) for test in state.get('acceptance', []))),
            '', '## Software tests', table(('Field', 'Value'), ((k, v) for k, v in state.get('software_tests', {}).items() if k != 'cases')),
            table(('Test case', 'State'), ((r['name'], r['status']) for r in state.get('software_tests', {}).get('cases', []))),
            '', '## Prior art and implementation references',
            'Prior art credited by the build spec: Seifert & Lipowsky — vesicle adhesion/contact potentials; Kendall — peel; Helfrich — bending. No Timoshenko model is used.',
            'Implementation documentation: SciPy L-BFGS-B and cKDTree.query_ball_point; PyTorch autograd. Full source locations are in REFERENCES.md.',
            '', '## Result files', 'Full-precision audit and run records: `results/run.json`, `results/acceptance.json`, `results/calibration.json`, and each `results/<nucleus>.json`.',
            'This document contains computed observations and explicit missing-data states; it assigns no physics grade.', '']
    path.write_text('\n'.join(out))
