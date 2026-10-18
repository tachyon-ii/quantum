#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Workflow/control tests. Mocked equilibria here are NOT physical measurements.

The isolated scientific gate prevents executing a validated calibrated production
path under the supplied functional. These tests exercise otherwise unreachable
control flow with clearly synthetic fixtures; no fixture enters report tables.
"""
from types import SimpleNamespace
from pathlib import Path
import json
import numpy as np
import pytest
from .. import constants as C
from .. import paths, analyse, chain, calibrate, reporting
from ..mesh import make_system
from ..energy import Functional
from ..relax import Relaxation
from ..tests import acceptance as A


def parameters():
    return C.Parameters(C.TEST_EAD, C.TEST_E0, C.DELTA_GRID[-1] * C.RP)


def synthetic_stationary(functional, vertices=None, constraints=None, **kwargs):
    """Control-flow fixture, deliberately not a numerical-relaxation claim."""
    v = np.asarray(functional.system.initial if vertices is None else vertices).copy()
    if constraints is not None:
        v = constraints.decode(constraints.pack(v))
    evaluation = functional.evaluate(v)
    return Relaxation(v, evaluation, True, 'test_fixture', 'Synthetic workflow fixture, not an equilibrium.',
                      0., 0, 0, 0., evaluation.energy)


@pytest.mark.parametrize('nucleus', ['T', 'He3'])
def test_all_load_directions(nucleus):
    system = make_system(nucleus, C.TEST_SUBDIV)
    for labels in paths.LABELINGS[nucleus]:
        directions = paths.directions(system.initial, labels)
        for vector in directions.values():
            assert abs(np.linalg.norm(vector) - 1) < C.GEOM_TEST_TOL
        assert abs(directions['tangential'] @ directions['radial_outward']) < C.GEOM_TEST_TOL
        centers = system.initial.mean(axis=1)
        assert directions['tangential'] @ (centers[labels.p3] - centers[labels.p1]) >= 0


def test_inversion_detected_from_sign_change_not_load_number():
    rows = [{'force_MeV_fm': k * C.FORCE_STEP, 'patches': {'0-1': {'hub_bias_sign': sign}}}
            for k, sign in enumerate((1, 1, 0, -1))]
    observed = paths._first_inversion(rows, '0-1')
    assert observed['load'] == rows[-1]['force_MeV_fm']
    assert observed['from_sign'] == 1 and observed['to_sign'] == -1


def test_no_inversion_is_not_reported_as_zero_load():
    rows = [{'force_MeV_fm': k * C.FORCE_STEP, 'patches': {'0-1': {'hub_bias_sign': 1}}} for k in range(3)]
    assert paths._first_inversion(rows, '0-1') is None


def test_optimizer_failure_is_not_snap(monkeypatch):
    system = make_system('T', C.TEST_SUBDIV)
    def fail(functional, initial, capsid, force, **kwargs):
        result = synthetic_stationary(functional, initial)
        result.converged = False; result.status = 'optimizer_failure'
        return result, {'status': 'synthetic_failure'}
    monkeypatch.setattr(paths, 'relax_under_traction', fail)
    result = paths.load_path(system, parameters(), system.initial, paths.LABELINGS['T'][0], 'tangential')
    assert result['event']['F_snap'] is None
    assert result['event']['status'] == 'unresolved_relaxation'
    assert result['motion']['theta_snap_rad'] is None


def test_contact_loss_bracket_and_last_stable_geometry(monkeypatch):
    system = make_system('T', C.TEST_SUBDIV)
    calls = []
    def controlled(functional, initial, capsid, force, **kwargs):
        result = synthetic_stationary(functional, initial)
        calls.append(force)
        if len(calls) > 1:
            result.evaluation.pairs[(0, 1)]['contact'] = False
        return result, {'status': 'synthetic_fixture'}
    monkeypatch.setattr(paths, 'relax_under_traction', controlled)
    result = paths.load_path(system, parameters(), system.initial, paths.LABELINGS['T'][0], 'tangential')
    assert result['event']['F_snap'] == C.FORCE_STEP
    assert result['event']['F_snap_bracket'] == [0., C.FORCE_STEP]
    assert len(result['steps']) == 1
    assert np.allclose(result['last_stable_geometry'], system.initial)


def test_force_limit_is_censoring(monkeypatch):
    system = make_system('T', C.TEST_SUBDIV)
    def controlled(functional, initial, capsid, force, **kwargs):
        return synthetic_stationary(functional, initial), {'status': 'synthetic_fixture'}
    monkeypatch.setattr(paths, 'relax_under_traction', controlled)
    monkeypatch.setattr(C, 'FORCE_MAX', C.FORCE_STEP)
    result = paths.load_path(system, parameters(), system.initial, paths.LABELINGS['T'][0], 'tangential')
    assert result['event']['F_snap'] is None
    assert result['event']['status'] == 'right_censored_at_force_limit'
    assert len(result['steps']) == 2


def test_area_uniform_traction_fixed_point(monkeypatch):
    system = make_system('T', C.TEST_SUBDIV)
    monkeypatch.setattr(paths, 'relax', synthetic_stationary)
    force = C.FORCE_STEP * np.eye(3)[0]
    result, status = paths.relax_under_traction(Functional(system, parameters()), system.initial, 0, force)
    assert result.converged
    assert status['status'] == 'current_area_traction_converged'
    assert np.allclose(status['total_nodal_force'], force)


def test_quartic_fits_sampled_fixture_not_inserted_coefficients(monkeypatch):
    system = make_system('T', C.TEST_SUBDIV)
    origin = system.initial[0].mean(axis=0)
    coefficient2 = C.TEST_E0 / C.RP ** 2
    coefficient4 = C.TEST_E0 / C.RP ** 4
    def fixture(functional, initial, constraints, **kwargs):
        result = synthetic_stationary(functional, initial, constraints)
        dz = result.vertices[0].mean(axis=0)[-1] - origin[-1]
        result.evaluation.energy = C.TEST_E0 + coefficient2 * dz ** 2 + coefficient4 * dz ** 4
        return result
    monkeypatch.setattr(analyse, 'relax', fixture)
    result = analyse.quartic_scan(system, parameters(), system.initial)
    assert result['status'] == 'sampled_and_fitted'
    assert abs(result['k2'] - coefficient2) < C.FD_TOL
    assert abs(result['k4'] - coefficient4) < C.FD_TOL
    assert len(result['samples']) == len(C.Z_GRID)


def test_chain_starts_collinear_and_uses_measured_distances(monkeypatch):
    system = make_system('T', C.TEST_SUBDIV)
    inputs = []
    def fixture(functional, initial=None, **kwargs):
        if initial is not None:
            inputs.append(initial.copy())
        return synthetic_stationary(functional, initial, **kwargs)
    monkeypatch.setattr(chain, 'relax', fixture)
    result = chain.chain_scan(system, parameters(), system.initial, -C.BE_D)
    centers = inputs[0].mean(axis=1)
    assert np.linalg.norm(np.cross(centers[0] - centers[2], centers[1] - centers[2])) < C.GEOM_TEST_TOL
    measured = np.linalg.norm(system.initial.mean(axis=1)[0] - system.initial.mean(axis=1)[2])
    assert abs(result['initial_contact_distances']['P1P3'] - measured) < C.GEOM_TEST_TOL
    assert len(result['separation_scan']) == C.CHAIN_STEPS


def test_nested_calibration_algorithm_with_synthetic_response(monkeypatch):
    # Here only, model BE_D=e0 and BE_He4=E0. This is an algorithm fixture.
    def fixture(functional, **kwargs):
        be = functional.p.e0 if functional.system.name == 'D' else functional.p.E0
        return SimpleNamespace(converged=True, evaluation=SimpleNamespace(binding_energy=be),
                               summary=lambda: {'status': 'synthetic_calibration_fixture'})
    monkeypatch.setattr(calibrate, 'relax', fixture)
    fit = calibrate.calibrate(C.DELTA_GRID[0] * C.RP, C.TEST_SUBDIV)
    assert fit.converged
    assert abs(fit.parameters.e0 - C.BE_D) <= C.CALIBRATION_TOL
    assert abs(fit.parameters.E0 - C.BE_HE4) <= C.CALIBRATION_TOL
    assert all(row['parameters']['delta'] == C.DELTA_GRID[0] * C.RP for row in fit.history)


def test_failed_inner_calibration_not_fitted(monkeypatch):
    def fixture(functional, **kwargs):
        return SimpleNamespace(converged=False, summary=lambda: {'status': 'synthetic_failure'})
    monkeypatch.setattr(calibrate, 'relax', fixture)
    fit = calibrate.calibrate(C.DELTA_GRID[0] * C.RP, C.TEST_SUBDIV)
    assert not fit.converged and fit.parameters is None
    assert fit.history[0]['status'] == 'inner_relaxation_failed'


def test_sensitivity_missing_measurement_does_not_pass():
    a = {'quartic': {'status': 'constrained_relaxation_failed'}}
    result = A.area_sensitivity(a, a)
    assert result['status'] == 'fail'


def test_sensitivity_detects_physical_change():
    a = {'observables': {'binding_energy': C.BE_D}}
    b = {'observables': {'binding_energy': C.BE_D * (1 + 2 * C.AREA_SENSITIVITY_TOL)}}
    assert A.area_sensitivity(a, b)['status'] == 'fail'
    assert A.area_sensitivity(a, a)['status'] == 'pass'


def test_json_standard_no_nan_and_numpy_support(tmp_path):
    path = tmp_path / 'test.json'
    reporting.write_json(path, {'array': np.asarray([1., 2.]), 'missing': None, 'flag': np.bool_(True)})
    data = json.loads(path.read_text())
    assert data == {'array': [1., 2.], 'missing': None, 'flag': True}


def test_all_modules_compile_and_model_attribution():
    root = Path(__file__).parents[1]
    for path in root.rglob('*.py'):
        text = path.read_text()
        assert 'GPT-6 Astra Pro' in text.splitlines()[1]
        compile(text, str(path), 'exec')


def test_rich_report_handles_unresolved_paths(tmp_path, monkeypatch):
    system = make_system('T', C.TEST_SUBDIV)
    functional = Functional(system, parameters())
    fixture = synthetic_stationary(functional)
    record = analyse.nucleus_record(system, parameters(), fixture)
    record.update(variant='synthetic_report_fixture', delta_ratio=C.DELTA_GRID[0])
    def fail(functional, initial, capsid, force, **kwargs):
        result = synthetic_stationary(functional, initial)
        result.converged = False; result.status = 'optimizer_failure'
        return result, {'status': 'synthetic_failure'}
    monkeypatch.setattr(paths, 'relax_under_traction', fail)
    path = paths.load_path(system, parameters(), system.initial, paths.LABELINGS['T'][0], 'tangential')
    record['loads'] = {'paths': [path], 'snap_ratios': []}
    record['quartic'] = {'status': 'constrained_relaxation_failed', 'k2': None, 'k4': None}
    record['chain'] = {'status': 'chain_or_free_nucleon_relaxation_failed'}
    state = {'provenance': reporting.provenance(Path(__file__).parents[4]), 'nuclei': {'T': {'cases': [record]}},
             'acceptance': [], 'status': 'synthetic_report_fixture'}
    report = tmp_path / 'report.md'
    reporting.render_report(report, state)
    assert 'unresolved_relaxation' in report.read_text()
    assert '§7.7' in report.read_text()
