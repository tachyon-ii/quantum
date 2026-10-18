#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Scientific acceptance gates. Dependencies run only when their data exist."""
from __future__ import annotations
from dataclasses import replace
from math import pi
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.spatial.transform import Rotation
from .. import constants as C
from ..mesh import make_system, numpy_geometry
from ..energy import Functional
from ..relax import Constraints, relax
from ..analyse import patch_geometry


def gate(name, passed, measurements=None, reason=None, **extra):
    return {'test': name, 'status': 'pass' if passed else 'fail',
            'measurements': measurements or {}, 'reason': reason, **extra}


def isolated(subdivision=C.SUBDIV, *, area_factor=C.AREA_FACTOR,
             bend_fraction=C.BEND_PRIMARY, deadline=None):
    rows, passed = [], True
    for species in ('p', 'n'):
        system = make_system(species, subdivision)
        p = C.Parameters(C.TEST_EAD, C.TEST_E0, C.DELTA_GRID[0] * C.RP,
                         area_factor=area_factor, bend_fraction=bend_fraction)
        fun = Functional(system, p)
        result = relax(fun, deadline=deadline)
        if result.evaluation is not None:
            volume = result.evaluation.capsids[0]['volume']
            relative_error = abs(volume - system.rest_volume[0]) / system.rest_volume[0]
            energy = result.evaluation.energy
            radii = np.linalg.norm(result.vertices[0] - result.vertices[0].mean(axis=0), axis=-1)
        else:
            volume = relative_error = energy = None
            radii = None
        ok = bool(result.converged and relative_error < C.ISOLATED_VOLUME_TOL and energy < C.ISOLATED_ENERGY_TOL * p.E0)
        passed &= ok
        rows.append({'species': species, 'subdivision': subdivision, 'vertices': system.topology.n_vertices,
                     'faces': system.topology.n_faces, 'volume': volume, 'rest_volume': system.rest_volume[0],
                     'relative_volume_error': relative_error, 'allowed_volume_error': C.ISOLATED_VOLUME_TOL,
                     'E_total': energy, 'allowed_energy_upper_bound': C.ISOLATED_ENERGY_TOL * p.E0,
                     'relative_radial_standard_deviation': float(np.std(radii) / np.mean(radii)) if radii is not None else None,
                     'area_factor': area_factor, 'bend_fraction': bend_fraction,
                     'literal_energy_inequality_passed': bool(energy < C.ISOLATED_ENERGY_TOL * p.E0) if energy is not None else False,
                     'relaxation': result.summary(), 'passed': ok})
    return gate('A1_isolated_capsid', passed, {'skins': rows},
        None if passed else 'The literal inflation and finite area-penalty functional does not meet the isolated reference-volume acceptance gate.')


def scale_diagnostic(subdivision=C.SUBDIV, area_factor=C.AREA_FACTOR):
    system = make_system('p', subdivision)
    geometry = numpy_geometry(system.initial[0], system.topology.faces)
    area_ratio = geometry['face_areas'].sum() / system.rest_total_area[0]
    volume_ratio_inverse = system.rest_volume[0] / geometry['volume']
    def energy(scale):
        return volume_ratio_inverse / scale ** 3 - 1 + area_factor * area_ratio * (scale ** 2 - 1) ** 2
    minimum = minimize_scalar(energy, bounds=(C.SCALE_LOWER, C.SCALE_UPPER), method='bounded',
                              options={'xatol': C.SCALAR_XATOL})
    return {'subdivision': subdivision, 'area_factor': area_factor,
            'mesh_area_over_analytic_area': float(area_ratio),
            'mesh_volume_over_analytic_volume': float(1 / volume_ratio_inverse),
            'd_E_over_E0_d_scale_at_rest': float(-3 * volume_ratio_inverse),
            'uniform_scale_minimum': float(minimum.x), 'E_over_E0_at_scale_minimum': float(minimum.fun),
            'relative_volume_error_at_scale_minimum': float(minimum.x ** 3 / volume_ratio_inverse - 1),
            'minimizer_success': bool(minimum.success),
            'formula': 'E(t)/E0 = (V0/Vmesh)*t^(-3) - 1 + area_factor*(Amesh/A0)*(t^2-1)^2',
            'interpretation': 'The area term has zero first derivative at the rest mesh; the inflation term has a nonzero expansive derivative.'}


def calibration_targets(calibration):
    rows = []
    for name, target in (('D', C.BE_D), ('He4', C.BE_HE4)):
        result = calibration.relaxed.get(name)
        be = result.evaluation.binding_energy if result and result.converged else None
        rows.append({'nucleus': name, 'binding_energy': be, 'calibration_target': target,
                     'absolute_residual': abs(be - target) if be is not None else None})
    passed = all(row['absolute_residual'] is not None and row['absolute_residual'] <= C.CALIBRATION_TOL for row in rows)
    return gate('A3_calibration_reproduction', passed, {'rows': rows, 'tolerance_MeV': C.CALIBRATION_TOL})


def dimer_patch(system, parameters, relaxed, *, deadline=None):
    fun = Functional(system, parameters)
    centers = relaxed.vertices.mean(axis=1)
    hub = centers.mean(axis=0)
    axis = (centers[1] - centers[0]); distance = np.linalg.norm(axis); axis /= distance
    pushed = relaxed.vertices.copy()
    pushed[0] += C.ED_SCAN_FRACTION * distance * axis / 2
    pushed[1] -= C.ED_SCAN_FRACTION * distance * axis / 2
    released = relax(fun, pushed, deadline=deadline)
    if not released.converged:
        return gate('A2_pair_patch_and_single_minimum', False, {'released': released.summary()}, 'Pushed-and-released pair did not converge.')
    patches = patch_geometry(system, released.vertices, released.evaluation, parameters.e0)
    aspect = patches['0-1'].get('aspect_ratio')
    rows = []
    for d in np.linspace(distance * (1 - C.ED_SCAN_FRACTION), distance * (1 + C.ED_SCAN_FRACTION), C.ED_SCAN_STEPS):
        constraint = Constraints(relaxed.vertices, pinned_centres={0: hub - d * axis / 2, 1: hub + d * axis / 2})
        result = relax(fun, relaxed.vertices, constraints=constraint, deadline=deadline)
        rows.append({'distance': float(d), 'energy': result.evaluation.energy if result.converged else None,
                     'relaxation': result.summary()})
        if not result.converged:
            return gate('A2_pair_patch_and_single_minimum', False, {'distance_scan': rows, 'aspect_ratio': aspect}, 'Constrained distance scan failed.')
    values = np.array([row['energy'] for row in rows])
    minima = np.flatnonzero((values[1:-1] < values[:-2]) & (values[1:-1] < values[2:])) + 1
    passed = bool(released.evaluation.all_pairs_contact and aspect is not None and abs(aspect - 1) <= C.DISC_ASPECT_TOL and len(minima) == 1)
    return gate('A2_pair_patch_and_single_minimum', passed,
                {'aspect_ratio': aspect, 'aspect_tolerance': C.DISC_ASPECT_TOL, 'distance_scan': rows,
                 'sampled_minimum_indices': minima.tolist(), 'released': released.summary()},
                qualification='A finite distance scan cannot establish uniqueness outside the declared scan interval.')


def tritium_symmetry(system, parameters, relaxed):
    patches = patch_geometry(system, relaxed.vertices, relaxed.evaluation, parameters.e0)
    rows = []
    for field in ('area', 'well_integral', 'aspect_ratio', 'patch_energy'):
        a, b = patches['0-1'].get(field), patches['0-2'].get(field)
        relative = abs(a - b) / max(abs(a), abs(b)) if a is not None and b is not None and max(abs(a), abs(b)) > 0 else None
        rows.append({'field': field, 'np_1': a, 'np_2': b, 'relative_difference': relative})
    passed = all(row['relative_difference'] is not None and row['relative_difference'] <= C.SYMMETRY_TOL for row in rows)
    return gate('A4_tritium_np_symmetry', passed, {'rows': rows, 'tolerance': C.SYMMETRY_TOL})


def rotation_invariance(system, parameters, relaxed, *, deadline=None):
    axis = np.asarray(C.ROTATION_AXIS); axis /= np.linalg.norm(axis)
    rotation = Rotation.from_rotvec(C.ROTATION_ANGLE * axis).as_matrix()
    rotated_initial = system.initial @ rotation.T
    result = relax(Functional(system, parameters), rotated_initial, deadline=deadline)
    difference = abs(result.evaluation.binding_energy - relaxed.evaluation.binding_energy) if result.converged else None
    return gate('A7_rotational_invariance', bool(difference is not None and difference <= C.ROTATION_BE_TOL),
                {'nucleus': system.name, 'absolute_BE_difference': difference, 'tolerance': C.ROTATION_BE_TOL,
                 'rotated_relaxation': result.summary()})


def mesh_convergence(parameters, base_relaxed, *, deadline=None):
    fine, rows = {}, []
    for name in ('D', 'T'):
        sys = make_system(name, C.CONVERGENCE_SUBDIV)
        result = relax(Functional(sys, parameters), deadline=deadline)
        fine[name] = result
        base = base_relaxed[name].evaluation.binding_energy
        be = result.evaluation.binding_energy if result.converged else None
        difference = abs(be - base) / abs(base) if be is not None and base != 0 else None
        rows.append({'nucleus': name, 'base_BE': base, 'fine_BE': be, 'relative_difference': difference,
                     'fine_relaxation': result.summary()})
    if not all(result.converged for result in fine.values()):
        return gate('A5_mesh_convergence', False, {'rows': rows}, 'Finer-mesh relaxation failed.'), fine
    close = all(row['relative_difference'] is not None and row['relative_difference'] <= C.MESH_BE_TOL for row in rows)
    report = gate('A5_mesh_convergence', True, {'rows': rows, 'tolerance': C.MESH_BE_TOL},
                  promoted=not close, report_subdivision=C.SUBDIV if close else C.CONVERGENCE_SUBDIV)
    if not close:
        report['status'] = 'promote_to_finer_mesh'
        report['reason'] = 'Spec explicitly requests reporting the finer mesh when convergence tolerance is missed; calibration must be repeated at that reported mesh.'
    return report, fine


def physical_numbers(record):
    """Scalars from every required measurement family; exclude bookkeeping.

    Contact maps, vertex arrays, optimizer iterations/timing, force grid indices,
    and quantum box/grid diagnostics are not physical scalars. Undefined values
    and branch changes are audited separately instead of converted into zeros.
    """
    out = {}
    excluded = {'relaxation', 'traction', 'reweighting_history', 'contact_maps', 'parameters',
                'geometry_file', 'last_stable_geometry', 'convergence', 'samples',
                'interior_nodes', 'half_box_fm', 'boundary_probability',
                'labeling', 'subdivision',
                'allowed_volume_error', 'allowed_energy_upper_bound', 'rest_volume', 'rest_total_area'}
    # Coordinates and principal-axis components are compared in the same pinned
    # laboratory frame. A changed exact zero has no finite relative tolerance.
    def visit(value, prefix):
        if isinstance(value, dict):
            for key, item in value.items():
                if key not in excluded:
                    visit(item, f'{prefix}.{key}' if prefix else key)
        elif isinstance(value, (list, tuple)):
            for index, item in enumerate(value):
                visit(item, f'{prefix}[{index}]')
        elif isinstance(value, (float, int, np.floating)) and not isinstance(value, bool):
            if np.isfinite(value):
                out[prefix] = float(value)
        elif value is None:
            out[prefix] = None
    visit(record, '')
    return out


def area_sensitivity(base_record, doubled_record):
    missing = []
    for label, record in (('base', base_record), ('doubled', doubled_record)):
        if 'quartic' in record and record['quartic'].get('status') != 'sampled_and_fitted':
            missing.append(label + ': quartic mode not measured')
        if 'chain' in record and record['chain'].get('status') != 'sampled':
            missing.append(label + ': chain scan incomplete')
        for path in record.get('loads', {}).get('paths', []):
            if path['event']['status'] == 'unresolved_relaxation':
                missing.append(label + ': unresolved load path ' + path['path'])
    if missing:
        return gate('A6_area_penalty_doubled', False, {'unmeasured_families': missing},
                    'Cannot claim sensitivity acceptance for missing measurements.')
    baseline, doubled = physical_numbers(base_record), physical_numbers(doubled_record)
    rows, passed = [], True
    for key in sorted(set(baseline) | set(doubled)):
        a, b = baseline.get(key), doubled.get(key)
        if a is None and b is None:
            continue
        if a is None or b is None:
            relative, ok = None, False
        elif a == b:
            relative, ok = 0., True
        elif a == 0:
            relative, ok = None, False
        else:
            relative = abs(b - a) / abs(a)
            ok = relative <= C.AREA_SENSITIVITY_TOL
        passed &= ok
        rows.append({'observable': key, 'base': a, 'doubled': b, 'relative_change': relative, 'passed': bool(ok)})
    return gate('A6_area_penalty_doubled', passed, {'rows': rows, 'tolerance': C.AREA_SENSITIVITY_TOL},
                definition='Same calibration parameters; re-run every computed physical measurement family. Numerical solver telemetry excluded; physical coordinate components retained. Undefined/defined transitions fail.')
