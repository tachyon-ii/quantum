#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Force-controlled continuation, patch trajectories, roll, inversion and spin."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from . import constants as C
from .mesh import System, numpy_geometry
from .energy import Functional
from .relax import Constraints, ExternalForce, Relaxation, relax, Deadline
from .analyse import unit, patch_geometry, contact_maps, kabsch


@dataclass(frozen=True)
class Labeling:
    name: str
    p1: int
    p2: int
    p3: int


LABELINGS = {
    'T': (Labeling('proton_toward_neutron', 0, 1, 2), Labeling('neutron_toward_proton', 1, 2, 0)),
    'He3': (Labeling('P1a_pp_P1P2', 0, 1, 2), Labeling('P1a_pp_P1P3', 0, 2, 1),
            Labeling('P1b_pp_P1P2', 1, 0, 2), Labeling('P1b_pp_P1P3', 1, 2, 0)),
}
PATH_NAMES = ('tangential', 'radial_outward', 'out_of_plane')


def directions(vertices, labels):
    centers = vertices.mean(axis=1)
    a, b, c = labels.p1, labels.p2, labels.p3
    radial = unit(centers[a] - centers.mean(axis=0))
    normal = unit(np.cross(centers[b] - centers[a], centers[c] - centers[a]))
    if radial is None or normal is None:
        raise ValueError('Load directions require a nondegenerate reference triangle.')
    tangent = unit(np.cross(normal, radial))
    if np.dot(tangent, centers[c] - centers[a]) < 0:
        tangent *= -1
    return {'radial_outward': radial, 'out_of_plane': normal, 'tangential': tangent}


def _area_force_weights(system, vertices, capsid):
    areas = numpy_geometry(vertices[capsid], system.topology.faces)['vertex_areas']
    return areas / areas.sum()


def relax_under_traction(functional, initial, capsid, force, *, deadline=None):
    """Area-uniform traction via frozen-weight conservative inner solves.

    Outer reweighting enforces current-area nodal forces at convergence. Different
    inner potentials are not confused with the model's internal E_total.
    """
    weights = _area_force_weights(functional.system, initial, capsid)
    vertices = initial
    history = []
    result = None
    for _ in range(C.TRACTION_MAXITER):
        external = ExternalForce(capsid, force, weights)
        result = relax(functional, vertices, constraints=Constraints(initial), external=external, deadline=deadline)
        if not result.converged:
            return result, {'status': 'inner_relaxation_failed', 'reweighting_history': history}
        new_weights = _area_force_weights(functional.system, result.vertices, capsid)
        change = float(np.max(np.abs(new_weights - weights)))
        history.append({'maximum_weight_change': change, 'relaxation': result.summary()})
        if change <= C.TRACTION_TOL:
            return result, {'status': 'current_area_traction_converged', 'reweighting_history': history,
                            'total_nodal_force': (new_weights.sum() * force).tolist()}
        vertices, weights = result.vertices, new_weights
    result.converged = False
    result.status = 'traction_reweighting_unconverged'
    return result, {'status': result.status, 'reweighting_history': history}


def _pair_key(a, b):
    return f'{min(a, b)}-{max(a, b)}'


def _first_inversion(rows, pair_key):
    previous = None
    for row in rows:
        data = row['patches'][pair_key]
        sign = data.get('hub_bias_sign', 0)
        if sign:
            if previous is not None and previous[1] != sign:
                return {'load': row['force_MeV_fm'], 'bracket': [previous[0], row['force_MeV_fm']],
                        'from_sign': previous[1], 'to_sign': sign}
            previous = (row['force_MeV_fm'], sign)
    return None


def _motion_summary(system, initial, rows, labels, snap_found):
    if not rows:
        return {'status': 'no_stable_steps', 'theta_snap_rad': None, 'theta_last_stable_rad': None,
                'P1P3_inversion': None, 'P2P3_inversion': None, 'inversion_delta_force': None,
                'inversion_sequence': 'not_both_observed', 'trajectories': [], 'beta_D_rad': None,
                'spin_at_snap': None, 'spin_last_stable': None}
    a, b, c = labels.p1, labels.p2, labels.p3
    first, last = rows[0], rows[-1]
    normal = directions(initial, labels)['out_of_plane']
    start_centers, final_centers = np.asarray(first['centers']), np.asarray(last['centers'])
    v0, v1 = start_centers[a] - start_centers[c], final_centers[a] - final_centers[c]
    v0 -= normal * (v0 @ normal); v1 -= normal * (v1 @ normal)
    theta = float(np.arctan2(normal @ np.cross(v0, v1), v0 @ v1))
    pair12, pair13, pair23 = _pair_key(a, b), _pair_key(a, c), _pair_key(b, c)
    inv13, inv23 = _first_inversion(rows, pair13), _first_inversion(rows, pair23)
    difference = abs(inv13['load'] - inv23['load']) if inv13 is not None and inv23 is not None else None
    sequence = ('simultaneous' if difference < C.INVERSION_SIMULTANEOUS_STEPS * C.FORCE_STEP else 'sequential') if difference is not None else 'not_both_observed'
    initial_area12 = first['patches'][pair12]['area']
    trajectories = []
    for row in rows:
        p12, p13, p23 = (row['patches'][key] for key in (pair12, pair13, pair23))
        center23 = p23.get('well_centroid')
        distance23 = float(np.linalg.norm(np.asarray(center23) - np.asarray(row['centers']).mean(axis=0))) if center23 is not None else None
        trajectories.append({'force_MeV_fm': row['force_MeV_fm'],
                             'P1P2_unzip_fraction': 1 - p12['area'] / initial_area12 if initial_area12 > 0 else None,
                             'P1P3_well_centroid': p13.get('well_centroid'),
                             'P2P3_well_centroid': center23, 'P2P3_well_centroid_hub_distance': distance23,
                             'P1P3_hub_bias': p13.get('hub_bias'), 'P2P3_hub_bias': p23.get('hub_bias')})
    beta = None
    if snap_found and len(rows) > 1 and sorted((system.species[b], system.species[c])) == ['n', 'p']:
        velocity = unit(np.asarray(rows[-1]['centers'])[a] - np.asarray(rows[-2]['centers'])[a])
        bond = unit(final_centers[c] - final_centers[b])
        if velocity is not None and bond is not None:
            # Undirected D bond axis: choose the acute angle, state convention.
            beta = float(np.arccos(np.clip(abs(bond @ velocity), 0, 1)))
    return {'theta_snap_rad': theta if snap_found else None, 'theta_last_stable_rad': theta,
            'P1P3_inversion': inv13, 'P2P3_inversion': inv23, 'inversion_delta_force': difference,
            'inversion_sequence': sequence, 'trajectories': trajectories,
            'beta_D_rad': beta, 'beta_D_convention': 'Acute angle of undirected remaining np bond to last stable finite-step P1 velocity.',
            'spin_at_snap': last['spin'] if snap_found else None, 'spin_last_stable': last['spin']}


def load_path(system: System, parameters: C.Parameters, initial: np.ndarray,
              labels: Labeling, path: str, *, deadline: Deadline | None = None,
              snapshot_writer=None):
    functional = Functional(system, parameters)
    direction = directions(initial, labels)[path]
    vertices = initial.copy()
    rows, event = [], None
    force_levels = np.arange(int(round(C.FORCE_MAX / C.FORCE_STEP)) + 1) * C.FORCE_STEP
    for force in force_levels:
        if deadline:
            deadline.check()
        result, traction = relax_under_traction(functional, vertices, labels.p1, force * direction, deadline=deadline)
        if not result.converged:
            # An optimizer budget/line-search failure is not evidence of a saddle-node.
            event = {'status': 'unresolved_relaxation', 'force_MeV_fm': float(force),
                     'F_snap': None, 'relaxation': result.summary(), 'traction': traction,
                     'trial_contact_pairs': [list(k) for k, v in result.evaluation.pairs.items() if v['contact']] if result.evaluation else None}
            break
        evaluation = result.evaluation
        if not evaluation.all_pairs_contact:
            event = {'status': 'contact_loss_on_converged_continuation', 'force_MeV_fm': float(force),
                     'F_snap': float(force), 'F_snap_bracket': [rows[-1]['force_MeV_fm'], float(force)] if rows else None,
                     'qualification': 'First observed loss of a pair on converged local continuation; not a global proof of a saddle-node.',
                     'relaxation': result.summary(), 'contact_maps': contact_maps(evaluation)}
            break
        row = {'force_MeV_fm': float(force), 'E_total': evaluation.energy, 'loaded_objective': result.objective,
               'terms': evaluation.terms, 'centers': evaluation.centers.tolist(), 'contact_maps': contact_maps(evaluation),
               'patches': patch_geometry(system, result.vertices, evaluation, parameters.e0),
               'spin': kabsch(initial[labels.p1], result.vertices[labels.p1]),
               'relaxation': result.summary(), 'traction': traction}
        if snapshot_writer:
            row['geometry_file'] = snapshot_writer(labels.name, path, len(rows), result.vertices)
        rows.append(row)
        vertices = result.vertices
    if event is None:
        event = {'status': 'right_censored_at_force_limit', 'F_snap': None, 'lower_bound': float(force_levels[-1])}
    snap_found = event.get('F_snap') is not None
    return {'labeling': {'name': labels.name, 'P1': labels.p1, 'P2': labels.p2, 'P3': labels.p3},
            'path': path, 'reference_direction': direction.tolist(), 'direction_convention': 'Fixed in the initial laboratory frame.',
            'event': event, 'steps': rows,
            'last_stable_geometry': vertices.tolist() if rows else None,
            'motion': _motion_summary(system, initial, rows, labels, snap_found) if path == 'tangential' else None}


def all_load_paths(system, parameters, initial, *, deadline=None, snapshot_writer=None):
    results = []
    for labels in LABELINGS[system.name]:
        for path in PATH_NAMES:
            results.append(load_path(system, parameters, initial, labels, path,
                                     deadline=deadline, snapshot_writer=snapshot_writer))
    ratios = []
    for labels in LABELINGS[system.name]:
        group = {r['path']: r['event'].get('F_snap') for r in results if r['labeling']['name'] == labels.name}
        for first, second in (('tangential', 'radial_outward'), ('out_of_plane', 'radial_outward')):
            num, den = group[first], group[second]
            ratios.append({'labeling': labels.name, 'numerator_path': first, 'denominator_path': second,
                           'ratio': num / den if num is not None and den is not None and den > 0 else None})
    return {'paths': results, 'snap_ratios': ratios,
            'interpretation': 'Each specified particle labeling is run along all three force directions. Symmetry-related labelings are retained, not averaged.'}
