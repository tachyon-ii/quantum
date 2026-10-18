#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Run the software checks, scientific gates, measurements and generated report.

Default: strict production run. A failed scientific gate stops production with
nonzero exit status and an explicit report; no target leakage or fabricated table.
"""
from __future__ import annotations
from pathlib import Path
import sys

# Support both python -m models.binding.membrane.run_all and python run_all.py.
if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    __package__ = 'models.binding.membrane'

import argparse
from dataclasses import replace
import importlib
import os
import subprocess
import time
import traceback
import xml.etree.ElementTree as ET
from . import constants as C
# Set before importing numerical backends; these are numerical, reported choices.
os.environ.setdefault('OMP_NUM_THREADS', str(C.TORCH_THREADS))
os.environ.setdefault('OPENBLAS_NUM_THREADS', str(C.TORCH_THREADS))
os.environ.setdefault('MKL_NUM_THREADS', str(C.TORCH_THREADS))
import numpy as np
import torch
from .guard import TargetFirewall, assert_targets_not_loaded, static_audit
from .mesh import make_system
from .energy import Functional
from .relax import Deadline, DeadlineExceeded, relax
from .calibrate import calibrate, singlet_audit
from .analyse import nucleus_record, quartic_scan
from .paths import all_load_paths
from .chain import chain_scan
from .reporting import write_json, render_report, provenance
from .tests import acceptance as A

NUCLEI = ('D', 'T', 'He3', 'He4')
VARIANTS = (('primary', 'linear', C.BEND_PRIMARY),
            ('quadratic_well', 'quadratic', C.BEND_PRIMARY),
            ('bending', 'linear', C.BEND_VARIANT))
GATES = ('A1_isolated_capsid', 'A2_pair_patch_and_single_minimum', 'A3_calibration_reproduction',
         'A4_tritium_np_symmetry', 'A5_mesh_convergence', 'A6_area_penalty_doubled', 'A7_rotational_invariance')


class GateFailure(RuntimeError):
    pass


def software_checks(root, results):
    log = results / 'software-tests.txt'
    xml = results / 'software-tests.xml'
    command = [sys.executable, '-m', 'pytest', str(Path(__file__).parent / 'tests'), '-q',
               '--junitxml=' + str(xml)]
    run = subprocess.run(command, cwd=root, capture_output=True, text=True)
    log.write_text(run.stdout + run.stderr)
    cases = []
    if xml.exists():
        for case in ET.parse(xml).getroot().iter('testcase'):
            status = 'failed' if case.find('failure') is not None or case.find('error') is not None else ('skipped' if case.find('skipped') is not None else 'passed')
            cases.append({'name': case.get('name'), 'status': status})
    return {'return_code': run.returncode, 'collected': len(cases),
            'passed': sum(case['status'] == 'passed' for case in cases),
            'failed': sum(case['status'] == 'failed' for case in cases),
            'skipped': sum(case['status'] == 'skipped' for case in cases),
            'log_file': log.name, 'junit_file': xml.name, 'cases': cases}


def candidate_reach_audit():
    from .mesh import SurfaceQuery
    rows = []
    for subdivision in (C.SUBDIV, C.CONVERGENCE_SUBDIV):
        for species in ('p', 'n'):
            system = make_system(species, subdivision)
            query = SurfaceQuery(system.initial[0], system.topology)
            reach = C.NEIGHBOUR_REACH * query.mean_edge
            for ratio in C.DELTA_GRID:
                rows.append({'species': species, 'subdivision': subdivision, 'delta_ratio': ratio,
                             'delta': ratio * C.RP, 'search_reach': reach, 'cuts_off_well': ratio * C.RP > reach})
    return rows


def save_snapshot(results_dir, case_key, system, name, vertices):
    directory = results_dir / 'geometry' / case_key
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (name + '.npz')
    np.savez_compressed(path, vertices=np.asarray(vertices), faces=system.topology.faces,
                        species=np.asarray(system.species), rest_areas=system.rest_areas,
                        radius=system.radii)
    return path.relative_to(results_dir.parent).as_posix()


def measure_case(system, parameters, result, variant, ratio, results_dir, deuteron_energy,
                 *, deadline=None, sensitivity=False):
    case_key = f'{system.name}_{variant}_delta_{ratio:g}_subdiv_{system.topology.subdivision}'
    if sensitivity:
        case_key += '_area_doubled'
    data = nucleus_record(system, parameters, result)
    data.update(variant=variant, delta_ratio=ratio, case_key=case_key)
    data['geometry_file'] = save_snapshot(results_dir, case_key, system, 'relaxed', result.vertices)
    if not result.converged:
        return data
    if system.name in ('T', 'He3'):
        data['quartic'] = quartic_scan(system, parameters, result.vertices, deadline=deadline)
        data['loads'] = all_load_paths(system, parameters, result.vertices, deadline=deadline,
            snapshot_writer=lambda labeling, path, step, vertices: save_snapshot(
                results_dir, case_key, system, f'{labeling}_{path}_{step}', vertices))
        data['chain'] = chain_scan(system, parameters, result.vertices, deuteron_energy, deadline=deadline)
    return data


def strict_production(state, results_dir, deadline):
    def record_gate(test, **context):
        test.update(context)
        state['acceptance'].append(test)
        assert_targets_not_loaded()
        if test['status'] == 'fail':
            raise GateFailure(test.get('reason') or test['test'])

    record_gate(A.isolated(deadline=deadline))
    for variant, fade, bend in VARIANTS:
        for ratio in state['delta_grid']:
            subdivision = C.SUBDIV
            context = {'variant': variant, 'delta_ratio': ratio}
            # A promotion can happen only once, to the spec's convergence mesh.
            while True:
                fit = calibrate(ratio * C.RP, subdivision, fade=fade, bend_fraction=bend, deadline=deadline)
                state['calibrations'].append({**context, 'subdivision': subdivision, **fit.summary()})
                assert_targets_not_loaded()
                if not fit.converged:
                    state['acceptance'].append(A.gate('A3_calibration_reproduction', False,
                        {'calibration': fit.summary()}, 'Nested calibration failed; predictions were not computed.', **context))
                    raise GateFailure(fit.status)
                record_gate(A.calibration_targets(fit), **context)
                parameters = fit.parameters
                systems = {name: make_system(name, subdivision) for name in NUCLEI}
                relaxed = dict(fit.relaxed)
                for name in ('T', 'He3'):
                    relaxed[name] = relax(Functional(systems[name], parameters), deadline=deadline)
                    if not relaxed[name].converged:
                        state['nuclei'][name]['cases'].append(nucleus_record(systems[name], parameters, relaxed[name]))
                        raise GateFailure(f'{name} relaxation failed; no minimum reported.')
                record_gate(A.dimer_patch(systems['D'], parameters, relaxed['D'], deadline=deadline), **context)
                record_gate(A.tritium_symmetry(systems['T'], parameters, relaxed['T']), **context)
                for name in ('D', 'T'):
                    record_gate(A.rotation_invariance(systems[name], parameters, relaxed[name], deadline=deadline), **context)
                if subdivision == C.SUBDIV:
                    mesh_check, _ = A.mesh_convergence(parameters, relaxed, deadline=deadline)
                    record_gate(mesh_check, **context)
                    if mesh_check.get('promoted'):
                        subdivision = C.CONVERGENCE_SUBDIV
                        continue
                break
            measured = {}
            for name in NUCLEI:
                measured[name] = measure_case(systems[name], parameters, relaxed[name], variant, ratio,
                    results_dir, relaxed['D'].evaluation.energy, deadline=deadline)
                state['nuclei'][name]['cases'].append(measured[name])
                state['nuclei'][name]['status'] = 'computed_cases_available'
                write_json(results_dir / (name + '.json'), state['nuclei'][name])
                assert_targets_not_loaded()
            # Fixed-parameter area doubling; do not refit away the sensitivity.
            doubled_p = replace(parameters, area_factor=parameters.area_factor * C.AREA_DOUBLE)
            doubled_relaxed = {name: relax(Functional(systems[name], doubled_p), deadline=deadline) for name in NUCLEI}
            if not all(r.converged for r in doubled_relaxed.values()):
                record_gate(A.gate('A6_area_penalty_doubled', False,
                    {'relaxations': {name: r.summary() for name, r in doubled_relaxed.items()}},
                    'Area-doubled relaxation failed.'), **context)
            for name in NUCLEI:
                doubled = measure_case(systems[name], doubled_p, doubled_relaxed[name], variant, ratio,
                    results_dir, doubled_relaxed['D'].evaluation.energy, deadline=deadline, sensitivity=True)
                test = A.area_sensitivity(measured[name], doubled)
                measured[name]['area_doubled_run'] = doubled
                record_gate(test, nucleus=name, **context)
    state['status'] = 'production_computations_completed'
    state['exit_code'] = 0


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('full', 'diagnostics', 'tests'), default='full',
                        help='full stops at the first failed scientific gate; diagnostics performs uncalibrated audits only.')
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent,
                        help='Directory containing generated report.md and results/.')
    parser.add_argument('--two-deltas', action='store_true',
                        help='Use the first and last declared reaches, explicitly recorded; no fitting of delta.')
    parser.add_argument('--budget-seconds', type=float, default=C.RUNTIME_TARGET_S,
                        help='Finite run budget. Exceeding it produces censored/unfinished output, not predictions.')
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.budget_seconds <= 0:
        raise SystemExit('budget-seconds must be positive')
    torch.set_num_threads(C.TORCH_THREADS)
    directory = args.output_dir.resolve()
    results = directory / 'results'; results.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[3]
    started = time.monotonic()
    deadline = Deadline(args.budget_seconds)
    firewall = TargetFirewall().install()
    state = {'status': 'started', 'mode': args.mode, 'stop_reason': None, 'exit_code': 0,
             'provenance': provenance(root), 'runtime_budget_seconds': args.budget_seconds,
             'delta_grid': [C.DELTA_GRID[0], C.DELTA_GRID[-1]] if args.two_deltas else list(C.DELTA_GRID),
             'delta_grid_choice': 'user_requested_two_extremes' if args.two_deltas else 'full_spec_grid',
             'variant_plan': [name for name, _, _ in VARIANTS],
             'acceptance': [], 'calibrations': [], 'audits': {},
             'nuclei': {name: {'nucleus': name, 'status': 'not_run', 'cases': []} for name in NUCLEI}}
    try:
        state['target_firewall'] = static_audit(Path(__file__).parent)
        state['software_tests'] = software_checks(root, results)
        if state['software_tests']['return_code'] != 0:
            raise GateFailure('Software checks failed; production and scientific acceptance tests were not run.')
        assert_targets_not_loaded()
        # These audits are calibration-independent algebra/mesh tests. No held-out targets.
        state['audits']['singlet'] = singlet_audit()
        state['audits']['uniform_scaling'] = [A.scale_diagnostic(level, area)
            for level in (C.SUBDIV, C.CONVERGENCE_SUBDIV) for area in (C.AREA_FACTOR, C.AREA_DOUBLE * C.AREA_FACTOR)]
        state['audits']['candidate_reach'] = candidate_reach_audit()
        if args.mode == 'full':
            strict_production(state, results, deadline)
        elif args.mode == 'diagnostics':
            first = A.isolated(deadline=deadline)
            state['acceptance'].append(first)
            state['audits']['isolated_variants'] = [
                A.isolated(C.CONVERGENCE_SUBDIV, deadline=deadline),
                A.isolated(C.SUBDIV, area_factor=C.AREA_DOUBLE * C.AREA_FACTOR, deadline=deadline),
                A.isolated(C.SUBDIV, bend_fraction=C.BEND_VARIANT, deadline=deadline)]
            state['status'] = 'diagnostics_only'
            state['stop_reason'] = 'Diagnostic mode: no calibration or nuclear predictions attempted.'
            state['exit_code'] = 2 if first['status'] == 'fail' else 0
        else:
            state['status'] = 'software_tests_only'
            state['stop_reason'] = 'Only software checks and calibration-independent audits were requested.'
    except GateFailure as error:
        state.update(status='stopped_at_failed_gate', stop_reason=str(error), exit_code=2)
    except DeadlineExceeded as error:
        state.update(status='budget_exhausted', stop_reason=str(error), exit_code=3)
    except Exception as error:
        state.update(status='implementation_error', stop_reason=str(error), exit_code=3,
                     exception_traceback=traceback.format_exc())
    finally:
        # Materialize all state BEFORE unsealing the targets. Even failures have reports.
        for name in GATES:
            if not any(test['test'] == name for test in state['acceptance']):
                state['acceptance'].append({'test': name, 'status': 'not_run',
                                            'reason': state.get('stop_reason') or 'Required upstream data unavailable.'})
        state['acceptance'].sort(key=lambda test: test['test'])
        state['elapsed_seconds'] = time.monotonic() - started
        for name, data in state['nuclei'].items():
            if not data['cases']:
                data['reason'] = state.get('stop_reason')
            write_json(results / (name + '.json'), data)
        write_json(results / 'acceptance.json', state['acceptance'])
        write_json(results / 'calibration.json', state['calibrations'])
        write_json(results / 'audit.json', state['audits'])
        write_json(results / 'run.json', state)
        assert_targets_not_loaded()
        report = directory / 'report.md'
        render_report(report, state)
        firewall.enable_comparison()
        compare = importlib.import_module('.compare', package=__package__)
        compare.append_comparison(report, state['nuclei'], results)
        firewall.remove()
    print(f"State: {state['status']}")
    print(f"Report: {report}")
    print(f"Results: {results}")
    if state.get('stop_reason'):
        print(state['stop_reason'])
    return state['exit_code']


if __name__ == '__main__':
    raise SystemExit(main())
