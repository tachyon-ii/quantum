#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Measured patches, charge radii, quartic scans, quantum mode and rotations.

No egg, hub orientation, stiffness, inversion or binding prediction is inserted.
Missing or mathematically undefined measurements are null with an explanation.
"""
from __future__ import annotations
from math import pi
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.spatial.transform import Rotation
from . import constants as C
from .energy import Functional, Evaluation
from .mesh import System, numpy_geometry
from .relax import Constraints, relax, Deadline


def unit(vector):
    vector = np.asarray(vector, dtype=float)
    norm = np.linalg.norm(vector)
    return vector / norm if norm > C.DEGENERATE_EPS else None


def dual_perimeter(vertices, faces, active):
    """Boundary of active vertices' barycentric dual cells on the skin.

    Each vertex owns one third of each incident triangle, matching A_v. For a
    mixed triangle, each active/inactive edge contributes its midpoint-to-face-
    centroid segment. No ellipse/disc approximation or hand-drawn front is used.
    """
    tri = vertices[faces]
    face_centers = tri.mean(axis=1)
    length = 0.
    for k in range(3):
        nxt = (k + 1) % 3
        mixed = active[faces[:, k]] != active[faces[:, nxt]]
        midpoints = (tri[:, k] + tri[:, nxt]) / 2
        length += np.linalg.norm(midpoints[mixed] - face_centers[mixed], axis=-1).sum()
    return float(length)


def _distribution(positions, vertex_areas, well_weights, hub):
    active = well_weights > 0
    area_weights = vertex_areas * active
    well = vertex_areas * well_weights
    area, integral = area_weights.sum(), well.sum()
    if area <= 0 or integral <= 0:
        return {'status': 'no_patch', 'area': 0., 'well_integral': 0.,
                'geometric_centroid': None, 'well_centroid': None,
                'aspect_ratio': None, 'hub_bias': None, 'hub_half_fraction': None}
    geometric = (area_weights[:, None] * positions).sum(axis=0) / area
    weighted = (well[:, None] * positions).sum(axis=0) / integral
    diff = positions - weighted
    covariance = np.einsum('v,vi,vj->ij', well, diff, diff) / integral
    eig, axes = np.linalg.eigh(covariance)
    order = np.argsort(eig)[::-1]
    eig, axes = eig[order], axes[:, order]
    hub_direction = unit(np.asarray(hub) - geometric)
    if hub_direction is not None and np.dot(axes[:, 0], hub_direction) < 0:
        axes[:, 0] *= -1
    if np.linalg.det(axes) < 0:
        axes[:, -1] *= -1
    # On a locally flat patch the two leading eigenvectors are the in-plane axes.
    aspect = float(np.sqrt(eig[0] / eig[1])) if eig[1] > C.DEGENERATE_EPS else None
    bias = float((weighted - geometric) @ hub_direction) if hub_direction is not None else None
    projection = (positions - geometric) @ hub_direction if hub_direction is not None else None
    fraction = float(well[projection > 0].sum() / integral) if projection is not None else None
    return {'status': 'measured', 'area': float(area), 'well_integral': float(integral),
            'geometric_centroid': geometric.tolist(), 'well_centroid': weighted.tolist(),
            'principal_axes': axes.T.tolist(), 'covariance_eigenvalues': eig.tolist(),
            'aspect_ratio': aspect, 'hub_direction': hub_direction.tolist() if hub_direction is not None else None,
            'hub_bias': bias, 'hub_bias_sign': int(np.sign(bias)) if bias is not None and abs(bias) > C.ASYMMETRY_ZERO_TOL else 0,
            'hub_half_fraction': fraction}


def front_line_energies(positions, areas, weights, distribution, e0):
    """Sample measured front widths; return e0 * mean(s) * width in MeV/fm.

    Point/hub are the terminal portions along the measured major axis oriented
    toward the hub. Broadside is the widest sampled bin. All bins are retained.
    This is a declared discretization of underspecified §7.4, not a peel law.
    """
    active = weights > 0
    if active.sum() < 3 or distribution['status'] != 'measured':
        return {'status': 'insufficient_patch_samples', 'point': None, 'broadside': None, 'hub_end': None}
    axes = np.asarray(distribution['principal_axes'])
    relative = positions[active] - np.asarray(distribution['geometric_centroid'])
    long = relative @ axes[0]
    across = relative @ axes[1]
    if long.max() - long.min() <= C.DEGENERATE_EPS:
        return {'status': 'degenerate_patch', 'point': None, 'broadside': None, 'hub_end': None}
    edges = np.linspace(long.min(), long.max(), C.FRONT_BINS + 1)
    index = np.clip(np.searchsorted(edges, long, side='right') - 1, 0, C.FRONT_BINS - 1)
    a, s = areas[active], weights[active]
    bins = []
    for b in range(C.FRONT_BINS):
        mask = index == b
        if mask.sum() < 2:
            bins.append({'position': float((edges[b] + edges[b + 1]) / 2), 'width': None, 'line_energy': None})
            continue
        width = float(np.ptp(across[mask]))
        mean_well = float(np.average(s[mask], weights=a[mask]))
        bins.append({'position': float((edges[b] + edges[b + 1]) / 2), 'width': width,
                     'mean_well': mean_well, 'line_energy': e0 * mean_well * width})
    valid = [row for row in bins if row['width'] is not None]
    if not valid:
        return {'status': 'insufficient_patch_samples', 'point': None, 'broadside': None, 'hub_end': None, 'bins': bins}
    terminal = max(1, int(np.ceil(C.FRONT_BINS * C.FRONT_EDGE_FRACTION)))
    def average_terminal(rows):
        values = [row['line_energy'] for row in rows if row['line_energy'] is not None]
        return float(np.mean(values)) if values else None
    return {'status': 'sampled', 'point': average_terminal(bins[:terminal]),
            'broadside': max(valid, key=lambda row: row['width'])['line_energy'],
            'hub_end': average_terminal(bins[-terminal:]), 'bins': bins,
            'units': 'MeV/fm', 'definition': 'e0 * local area-weighted fade * sampled transverse front width'}


def patch_geometry(system: System, vertices: np.ndarray, evaluation: Evaluation, e0: float):
    hub = evaluation.centers.mean(axis=0)
    result = {}
    for (i, j), pair in evaluation.pairs.items():
        sides = []
        for index, suffix in ((i, 'i'), (j, 'j')):
            positions = vertices[index]
            areas, weights = pair[f'area_{suffix}'], pair[f'weight_{suffix}']
            data = _distribution(positions, areas, weights, hub)
            data['capsid'] = index
            data['perimeter'] = dual_perimeter(positions, system.topology.faces, weights > 0)
            data['front_line_energies'] = front_line_energies(positions, areas, weights, data, e0)
            sides.append(data)
        positions = np.concatenate((vertices[i], vertices[j]))
        areas = np.concatenate((pair['area_i'], pair['area_j']))
        weights = np.concatenate((pair['weight_i'], pair['weight_j']))
        combined = _distribution(positions, areas, weights, hub)
        combined.update(pair=[i, j], species=[system.species[i], system.species[j]], contact=pair['contact'],
                        skins=sides, two_skin_perimeter=sum(side['perimeter'] for side in sides),
                        patch_energy=e0 * float(np.dot(areas, weights)),
                        area_convention='Sum of both skins; no factor of one half.',
                        perimeter_convention='Barycentric dual-cell boundary on each skin.')
        result[f'{i}-{j}'] = combined
    return result


def contact_maps(evaluation: Evaluation):
    return {f'{i}-{j}': {'contact': pair['contact'],
                'skin_i': {'active': (pair['weight_i'] > 0).tolist(), 'well_weights': pair['weight_i'].tolist()},
                'skin_j': {'active': (pair['weight_j'] > 0).tolist(), 'well_weights': pair['weight_j'].tolist()}}
            for (i, j), pair in evaluation.pairs.items()}


def energy_and_radius(system: System, evaluation: Evaluation):
    centers = evaluation.centers
    masses = np.asarray([C.MP if s == 'p' else C.MN for s in system.species])
    mass_center = np.average(centers, axis=0, weights=masses)
    protons = np.asarray([s == 'p' for s in system.species])
    rch = float(np.sqrt(np.mean(np.sum((centers[protons] - mass_center) ** 2, axis=-1)) + C.RP ** 2)) if protons.any() else None
    count = sum(pair['contact'] for pair in evaluation.pairs.values())
    corrected = evaluation.binding_energy + evaluation.terms['slingshot'] + evaluation.terms['coulomb']
    return {'binding_energy': evaluation.binding_energy, 'total_energy': evaluation.energy,
            'terms': evaluation.terms, 'centers': centers.tolist(), 'mass_center': mass_center.tolist(),
            'charge_radius_fm': rch, 'radius_origin': 'Mass-weighted nucleon centroid; intrinsic RP added in quadrature.',
            'radius_caveat': 'Classical minimum, not a quantum rms average. Measured rms distances are not contact inputs.',
            'centroid_distances': {f'{i}-{j}': pair['distance'] for (i, j), pair in evaluation.pairs.items()},
            'rms_pair_centroid_distance': float(np.sqrt(np.mean([p['distance'] ** 2 for p in evaluation.pairs.values()]))) if evaluation.pairs else None,
            'active_bonds': count, 'per_bond_after_sling_and_coulomb': corrected / count if count else None,
            'connected': evaluation.connected, 'capsids': evaluation.capsids}


def kabsch(initial: np.ndarray, current: np.ndarray):
    a, b = initial - initial.mean(axis=0), current - current.mean(axis=0)
    u, _, vh = np.linalg.svd(a.T @ b)
    correction = np.eye(3); correction[-1, -1] = np.linalg.det(vh.T @ u.T)
    rotation = vh.T @ correction @ u.T
    vector = Rotation.from_matrix(rotation).as_rotvec()
    angle = float(np.linalg.norm(vector))
    return {'angle_rad': angle, 'axis': (vector / angle).tolist() if angle > C.DEGENERATE_EPS else None,
            'rms_nonrigid_residual_fm': float(np.sqrt(np.mean(np.sum((a @ rotation.T - b) ** 2, axis=-1))))}


def _quantum_on_grid(k2: float, k4: float, mass: float, half_box: float, nodes: int):
    # Interior nodes, homogeneous Dirichlet boundary conditions at +/-half_box.
    spacing = 2 * half_box / (nodes + 1)
    z = -half_box + spacing * np.arange(1, nodes + 1)
    kinetic_scale = C.HC ** 2 / (2 * mass * spacing ** 2)
    potential = k2 * z ** 2 + k4 * z ** 4
    diagonal = 2 * kinetic_scale + potential
    off_diagonal = np.full(nodes - 1, -kinetic_scale)
    values, vectors = eigh_tridiagonal(diagonal, off_diagonal, select='i', select_range=(0, 0))
    psi = vectors[:, 0]
    kinetic = float(2 * kinetic_scale * np.dot(psi, psi) - 2 * kinetic_scale * np.dot(psi[:-1], psi[1:]))
    return {'E_zp_MeV': float(values[0]), 'p_rms_MeV_c': float(np.sqrt(max(0., 2 * mass * kinetic))),
            'kinetic_MeV': kinetic, 'half_box_fm': half_box, 'interior_nodes': nodes,
            'boundary_probability': float(psi[0] ** 2 + psi[-1] ** 2)}


def schrodinger_ground_state(k2: float, k4: float):
    mass = (2 / 3) * (C.MP + C.MN) / 2
    if not np.isfinite([k2, k4]).all() or k4 < 0 or (k4 == 0 and k2 <= 0):
        return {'status': 'no_confining_polynomial_on_real_line', 'E_zp_MeV': None, 'p_rms_MeV_c': None,
                'mass_MeV_c2': mass, 'reason': 'No artificial box-bound state is reported for an unconfined or unbounded-below fit.'}
    half_box, nodes = C.SCHRODINGER_BOX, C.SCHRODINGER_N
    history = []
    def agrees(a, b):
        return all(abs(a[k] - b[k]) <= C.SCHRODINGER_TOL * max(abs(b[k]), C.QUANTUM_ABS_FLOOR)
                   for k in ('E_zp_MeV', 'p_rms_MeV_c'))
    for _ in range(C.SCHRODINGER_REFINEMENTS):
        base = _quantum_on_grid(k2, k4, mass, half_box, nodes)
        wide = _quantum_on_grid(k2, k4, mass, 2 * half_box, 2 * nodes + 1)
        fine = _quantum_on_grid(k2, k4, mass, half_box, 2 * nodes + 1)
        history.append({'base': base, 'doubled_box_fixed_spacing': wide, 'halved_spacing_fixed_box': fine})
        if agrees(base, wide) and agrees(base, fine):
            return {'status': 'box_and_mesh_converged', **fine, 'mass_MeV_c2': mass, 'convergence': history,
                    'qualification': 'Assumes the locally fitted polynomial is the potential over the whole real line.'}
        if not agrees(base, wide):
            half_box *= 2; nodes = 2 * nodes + 1
        if not agrees(base, fine):
            nodes = 2 * nodes + 1
    return {'status': 'quantum_domain_or_grid_unconverged', 'E_zp_MeV': None, 'p_rms_MeV_c': None,
            'mass_MeV_c2': mass, 'convergence': history}


def quartic_scan(system: System, parameters: C.Parameters, relaxed_vertices: np.ndarray,
                 *, p1: int = 0, deadline: Deadline | None = None):
    if system.count != 3:
        return {'status': 'not_applicable'}
    centers = relaxed_vertices.mean(axis=1)
    normal = unit(np.cross(centers[1] - centers[0], centers[2] - centers[0]))
    if normal is None:
        return {'status': 'undefined_initial_plane', 'k2': None, 'k4': None}
    functional = Functional(system, parameters)
    rows = []
    for displacement in C.Z_GRID:
        frozen = {p1: relaxed_vertices[p1] + displacement * normal}
        constraint = Constraints(relaxed_vertices, pin_system=True, frozen=frozen)
        result = relax(functional, relaxed_vertices, constraints=constraint, deadline=deadline)
        rows.append({'z_fm': displacement, 'E_MeV': result.evaluation.energy if result.converged else None,
                     'relaxation': result.summary(), 'centers': result.vertices.mean(axis=1).tolist()})
        if not result.converged:
            return {'status': 'constrained_relaxation_failed', 'samples': rows, 'k2': None, 'k4': None}
    z = np.asarray([row['z_fm'] for row in rows]); energy = np.asarray([row['E_MeV'] for row in rows])
    design = np.stack((np.ones_like(z), z ** 2, z ** 4), axis=1)
    coefficients, _, _, _ = np.linalg.lstsq(design, energy, rcond=None)
    e0, k2, k4 = map(float, coefficients)
    residual = energy - design @ coefficients
    odd_residual = [abs(rows[list(C.Z_GRID).index(value)]['E_MeV'] - rows[list(C.Z_GRID).index(-value)]['E_MeV']) for value in C.Z_GRID if value > 0]
    return {'status': 'sampled_and_fitted', 'samples': rows, 'E_offset': e0, 'k2': k2, 'k4': k4,
            'fit_rms_residual_MeV': float(np.sqrt(np.mean(residual ** 2))),
            'maximum_odd_residual_MeV': float(max(odd_residual)),
            'constraints': 'P1 vertex set frozen after rigid shift; all other vertices relaxed, system centroid pinned. No additional plane/frame clamp.',
            'qualification': 'Rigid rotations and other-centre relaxation can remove this displacement. No quartic stiffness is presumed.',
            'quantum': schrodinger_ground_state(k2, k4)}


def nucleus_record(system: System, parameters: C.Parameters, result, *, include_maps=True):
    record = {'parameters': parameters.to_dict(), 'subdivision': system.topology.subdivision,
              'relaxation': result.summary(), 'status': 'relaxed' if result.converged else 'relaxation_failed'}
    if result.evaluation is not None:
        record['observables'] = energy_and_radius(system, result.evaluation)
        record['patches'] = patch_geometry(system, result.vertices, result.evaluation, parameters.e0)
        if include_maps:
            record['contact_maps'] = contact_maps(result.evaluation)
        if not result.converged:
            record['qualification'] = 'These are trial-geometry diagnostics, not reported minima or predictions.'
    return record
