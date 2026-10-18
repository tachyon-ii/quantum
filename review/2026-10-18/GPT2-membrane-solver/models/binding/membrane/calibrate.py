#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Nested two-parameter calibration; delta is scanned, NEVER optimized."""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from scipy.optimize import minimize
from . import constants as C
from .mesh import make_system
from .energy import Functional
from .relax import relax, Deadline, Relaxation


class CalibrationFailure(RuntimeError):
    pass


@dataclass
class Calibration:
    parameters: C.Parameters | None
    relaxed: dict[str, Relaxation]
    converged: bool
    status: str
    history: list[dict] = field(default_factory=list)
    optimizer: dict = field(default_factory=dict)

    def summary(self):
        return {'parameters': self.parameters.to_dict() if self.parameters else None,
                'converged': self.converged, 'status': self.status, 'history': self.history,
                'optimizer': self.optimizer,
                'relaxations': {name: item.summary() for name, item in self.relaxed.items()}}


def singlet_audit():
    """Compute both incompatible readings of §4.2; do not silently delete sling."""
    total_singlet_be = C.BE_D - C.E_MESH
    return {'Y2': C.Y(2), 'E_patch_D_from_formula': C.E_PATCH_D,
            'E_mesh_from_formula': C.E_MESH,
            'patch_decimal_printed_in_spec': C.SPEC_PRINTED_PATCH_D,
            'mesh_decimal_printed_in_spec': C.SPEC_PRINTED_MESH,
            'patch_formula_minus_printed': C.E_PATCH_D - C.SPEC_PRINTED_PATCH_D,
            'mesh_formula_minus_printed': C.E_MESH - C.SPEC_PRINTED_MESH, 'E_singlet_input': C.E_SINGLET,
            'singlet_BE_if_total_functional_and_triplet_fit': total_singlet_be,
            'singlet_patch_BE_excluding_sling': C.E_PATCH_D - C.E_MESH,
            'total_singlet_residual': total_singlet_be - C.E_SINGLET,
            'mesh_needed_for_total_singlet_target': C.BE_D - C.E_SINGLET,
            'status': 'incompatible_total_energy_and_patch_only_calibration',
            'convention': 'Retain both literal rules: connected graph sling in §3 and mesh formula in §4.2.'}


def calibrate(delta: float, subdivision: int = C.SUBDIV, *,
              fade: str = 'linear', bend_fraction: float = C.BEND_PRIMARY,
              deadline: Deadline | None = None) -> Calibration:
    systems = {name: make_system(name, subdivision) for name in ('D', 'He4')}
    target = np.array((C.BE_D, C.BE_HE4))
    history, cache = [], {}
    best = {'cost': float('inf'), 'p': None, 'relaxed': {}}

    def evaluate(log_parameters):
        if deadline:
            deadline.check()
        if np.any(log_parameters < C.LOG_PARAMETER_MIN) or np.any(log_parameters > C.LOG_PARAMETER_MAX):
            raise CalibrationFailure('Log-parameter overflow guard encountered; no finite penalty or fitted bound substituted.')
        key = tuple(map(float, log_parameters))
        if key in cache:
            return cache[key]
        e0, E0 = np.exp(log_parameters)
        p = C.Parameters(float(e0), float(E0), delta, fade=fade, bend_fraction=bend_fraction)
        relaxed = {name: relax(Functional(system, p), deadline=deadline) for name, system in systems.items()}
        row = {'parameters': p.to_dict(), 'inner': {name: r.summary() for name, r in relaxed.items()}}
        if not all(r.converged for r in relaxed.values()):
            row['status'] = 'inner_relaxation_failed'
            history.append(row)
            raise CalibrationFailure('Inner relaxation did not meet the stated gradient tolerance; failed samples cannot be fitted as minima.')
        values = np.array([relaxed[name].evaluation.binding_energy for name in systems])
        residual = values - target
        cost = float(residual @ residual)
        row.update(status='evaluated', binding_energies=dict(zip(systems, map(float, values))),
                   residuals=dict(zip(systems, map(float, residual))), cost=cost)
        history.append(row)
        if cost < best['cost']:
            best.update(cost=cost, p=p, relaxed=relaxed)
        cache[key] = cost
        return cost

    initial = np.log([C.FIT_EAD_INITIAL, C.FIT_E0_INITIAL])
    try:
        fit = minimize(evaluate, initial, method='Nelder-Mead', options={
            'maxiter': C.FIT_MAXITER, 'maxfev': C.FIT_MAXFEV,
            'xatol': C.FIT_XATOL, 'fatol': C.FIT_FATOL})
        evaluate(fit.x)
        fits = best['relaxed']
        residuals = [fits[name].evaluation.binding_energy - t for name, t in zip(systems, target)] if fits else []
        accepted = bool(residuals and np.max(np.abs(residuals)) <= C.CALIBRATION_TOL)
        return Calibration(best['p'], fits, accepted, 'calibrated' if accepted else 'calibration_residual_failure', history,
            {'success': bool(fit.success), 'message': str(fit.message), 'nfev': int(fit.nfev),
             'iterations': int(fit.nit), 'maximum_absolute_residual': float(np.max(np.abs(residuals))) if residuals else None})
    except CalibrationFailure as error:
        return Calibration(best['p'], best['relaxed'], False, str(error), history)
