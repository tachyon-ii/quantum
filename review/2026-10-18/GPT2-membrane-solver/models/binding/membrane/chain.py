#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Collinear P1--P3--P2 starts, free relaxation and constrained separation scans."""
from __future__ import annotations
import numpy as np
from . import constants as C
from .mesh import System, make_system
from .energy import Functional
from .relax import Constraints, relax, Deadline
from .analyse import unit, energy_and_radius


def chain_scan(system: System, parameters: C.Parameters, reference: np.ndarray,
               deuteron_energy: float, *, p1=0, p3=2, deadline: Deadline | None = None):
    p2 = next(i for i in range(system.count) if i not in (p1, p3))
    centers = reference.mean(axis=1)
    d13 = np.linalg.norm(centers[p1] - centers[p3])
    d23 = np.linalg.norm(centers[p2] - centers[p3])
    axis = unit(centers[p2] - centers[p3])
    if axis is None:
        return {'status': 'undefined_reference_contact_distance'}
    chain_centers = centers.copy()
    chain_centers[p3] = np.zeros(3)
    chain_centers[p1] = -d13 * axis
    chain_centers[p2] = d23 * axis
    chain_initial = reference - centers[:, None] + chain_centers[:, None]
    functional = Functional(system, parameters)
    constraint = Constraints(chain_initial, pin_system=False, pinned_centres={p3: np.zeros(3)})
    chain = relax(functional, chain_initial, constraints=constraint, deadline=deadline)
    extra_species = 'n' if system.name == 'T' else 'p'
    single = make_system(extra_species, system.topology.subdivision)
    free_nucleon = relax(Functional(single, parameters), deadline=deadline)
    if not chain.converged or not free_nucleon.converged:
        return {'status': 'chain_or_free_nucleon_relaxation_failed', 'chain_relaxation': chain.summary(),
                'isolated_relaxation': free_nucleon.summary(), 'energy_relative_D_plus_N': None}
    threshold = deuteron_energy + free_nucleon.evaluation.energy
    initial_separation = np.linalg.norm(chain.vertices[p1].mean(axis=0) - chain.vertices[p3].mean(axis=0))
    separation = np.linspace(initial_separation, initial_separation + C.CHAIN_EXTRA_DISTANCE, C.CHAIN_STEPS)
    current = chain.vertices.copy()
    rows = []
    for distance in separation:
        pinned = {p3: np.zeros(3), p1: -float(distance) * axis}
        con = Constraints(current, pin_system=False, pinned_centres=pinned)
        result = relax(functional, current, constraints=con, deadline=deadline)
        rows.append({'P1_P3_separation_fm': float(distance), 'relaxation': result.summary(),
                     'energy_relative_D_plus_N': result.evaluation.energy - threshold if result.converged else None,
                     'E_total': result.evaluation.energy if result.converged else None,
                     'centers': result.vertices.mean(axis=1).tolist()})
        if not result.converged:
            break
        current = result.vertices
    maxima = []
    for before, row, after in zip(rows, rows[1:], rows[2:]):
        energies = [r['E_total'] for r in (before, row, after)]
        if all(e is not None for e in energies) and energies[1] > energies[0] and energies[1] > energies[2]:
            maxima.append({'separation_fm': row['P1_P3_separation_fm'], 'E_total': row['E_total'],
                           'energy_relative_D_plus_N': row['energy_relative_D_plus_N'],
                           'qualification': 'Sampled constrained-profile maximum; not a verified full-dimensional saddle.'})
    final_centers = chain.vertices.mean(axis=1)
    bend_area = np.linalg.norm(np.cross(final_centers[p1] - final_centers[p3], final_centers[p2] - final_centers[p3])) / 2
    return {'status': 'sampled' if all(row['E_total'] is not None for row in rows) else 'partial_scan',
            'initial_contact_distances': {'P1P3': float(d13), 'P2P3': float(d23)},
            'labeling': {'P1': p1, 'P2': p2, 'P3': p3},
            'chain_relaxation': chain.summary(), 'chain_observables': energy_and_radius(system, chain.evaluation),
            'energy_relative_D_plus_N': chain.evaluation.energy - threshold,
            'D_plus_N_reference': {'deuteron_energy': deuteron_energy,
                                  'free_nucleon_energy': free_nucleon.evaluation.energy,
                                  'free_nucleon_species': extra_species},
            'relaxed_centroid_triangle_area': float(bend_area), 'separation_scan': rows,
            'saddle_candidates': maxima,
            'qualification': 'Initial chain is not artificially kept straight. P3 is pinned; scan additionally constrains P1 centroid. Literal graph-global slingshot is not cluster separable.'}
