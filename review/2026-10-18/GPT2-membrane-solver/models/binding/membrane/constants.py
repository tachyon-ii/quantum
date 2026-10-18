#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Only source of physical, numerical, algorithmic and acceptance constants.

Integers that specify dimensions, array indices and algebraic operations are not
model constants. Validation-only prediction targets live in targets.py instead.
"""
from __future__ import annotations
from math import pi, sqrt
from dataclasses import dataclass, asdict

HC = 197.3269804
AHC = 1.439964547
ME = 0.510998950
MP = 938.2720882
MN = 939.5654205
RP = 0.8409
RN_FACTOR = 1.023
RN = RN_FACTOR * RP
BE_D = 2.224566
BE_HE4 = 28.29566
E_SINGLET = -0.0660
CPRIME = sqrt(1 - (ME / (MN - MP)) ** 2)


def Y(n: int) -> float:
    """Literal per-capsid slingshot, eq. in build spec §2."""
    return ME * ((MN - MP) / ME - 1 / sqrt(1 - (CPRIME / n) ** 2)) if n > 1 else 0.0


# Audit-only decimal claims printed in §4.2; never used as fit inputs.
SPEC_PRINTED_PATCH_D = 0.788624
SPEC_PRINTED_MESH = 0.854624
E_PATCH_D = BE_D - 2 * Y(2)
E_MESH = E_PATCH_D - E_SINGLET
SUBDIV = 3
CONVERGENCE_SUBDIV = 4
AREA_FACTOR = 50.0
AREA_DOUBLE = 2.0
PEN_FACTOR = 10.0
PEN_SCALE = 0.05 * RP
BEND_PRIMARY = 0.0
BEND_VARIANT = 0.01
DELTA_GRID = (0.05, 0.10, 0.20, 0.30)  # dimensionless multiples of RP
NEIGHBOUR_REACH = 3.0                  # times current mean edge length of target skin
GTOL = 1e-8
FORCE_STEP = 0.02                     # MeV/fm
Z_GRID = (0.0, -0.05, 0.05, -0.10, 0.10, -0.20, 0.20, -0.30, 0.30)
START_EDGE = 1.70
START_TRI_X = 0.85
START_TRI_Y = 1.47                    # literal (not silently regularized)
ISOLATED_VOLUME_TOL = 1e-4
ISOLATED_ENERGY_TOL = 1e-6
CALIBRATION_TOL = 1e-4
DISC_ASPECT_TOL = 0.02
SYMMETRY_TOL = 0.005
MESH_BE_TOL = 0.01
AREA_SENSITIVITY_TOL = 0.005
ROTATION_BE_TOL = 1e-4
INVERSION_SIMULTANEOUS_STEPS = 2
RUNTIME_TARGET_S = 30 * 60

# Added numerical/operational constants: every entry is automatically reported.
# None is a fitted physics parameter; all are nucleus independent.
ADDED = {
    'TORCH_THREADS': (1, 'CPU thread count; avoids small-tensor thread overhead.'),
    'FTOL': (0.0, 'Disable energy-change termination; require the stated gradient tolerance.'),
    'MAXITER': (2000, 'Finite inner L-BFGS-B iteration budget; exhaustion is failure, not snap.'),
    'MAXFUN': (60000, 'Finite inner function evaluation budget.'),
    'MAXLS': (50, 'L-BFGS-B line-search trial budget.'),
    'MAXCOR': (20, 'L-BFGS-B history length.'),
    'DEGENERATE_EPS': (1e-14, 'Reject degenerate faces/zero volume, never change their energy.'),
    'RAY_EPS': (1e-11, 'Parity ray boundary tolerance; ambiguous hits use solid-angle winding.'),
    'WINDING_INSIDE': (0.5, 'Integer winding-number threshold defining an interior point.'),
    'WINDING_CHUNK': (64, 'Batch size for winding fallback; memory only.'),
    'KD_WORKERS': (1, 'Deterministic KD-tree worker count.'),
    'FIT_E0_INITIAL': (1.0, 'Outer optimizer initial guess in MeV, not a calibration datum.'),
    'FIT_EAD_INITIAL': (1.0, 'Outer optimizer initial guess in MeV/fm^2.'),
    'FIT_MAXITER': (250, 'Nelder-Mead evaluation/iteration budgets are explicit.'),
    'FIT_MAXFEV': (500, 'Maximum outer calibration function calls.'),
    'FIT_XATOL': (1e-8, 'Outer log-parameter coordinate tolerance.'),
    'FIT_FATOL': (1e-12, 'Outer sum-of-squared-energy-residual tolerance.'),
    'LOG_PARAMETER_MIN': (-12.0, 'Numerical overflow guard on log fit parameters, not a best-fit bound.'),
    'LOG_PARAMETER_MAX': (12.0, 'Numerical overflow guard; a guard hit is reported as failure.'),
    'TRACTION_MAXITER': (12, 'Area-weight redistribution fixed-point budget per force step.'),
    'TRACTION_TOL': (1e-7, 'Maximum absolute change of normalized nodal force weights.'),
    'FORCE_MAX': (3.0, 'Finite force scan ceiling; absence of snap is right-censored.'),
    'HESSIAN_STEP': (1e-5, 'Finite-difference gradient step for optional stability probe.'),
    'HESSIAN_TOL': (1e-6, 'Eigenvalue solver tolerance, not a physics stiffness.'),
    'HESSIAN_MAXITER': (300, 'Finite stability-eigensolver budget.'),
    'HESSIAN_NEGATIVE_TOL': (1e-5, 'Negative curvature rejection tolerance, MeV/fm^2.'),
    'HESSIAN_MODES': (6, 'Number of lowest modes probed when confirming a local minimum.'),
    'FRONT_BINS': (16, 'Patch line-energy sampling bins along the measured principal axis.'),
    'FRONT_EDGE_FRACTION': (0.15, 'Terminal-bin fraction used for point/hub front estimates.'),
    'ASYMMETRY_ZERO_TOL': (1e-10, 'Numerical zero for inversion sign, fm.'),
    'SCHRODINGER_N': (801, 'Initial odd number of interior finite-difference nodes.'),
    'SCHRODINGER_BOX': (4.0, 'Initial quantum half-box, fm; verified by box and mesh doubling.'),
    'SCHRODINGER_REFINEMENTS': (4, 'Maximum box/grid refinements; failure leaves outputs null.'),
    'SCHRODINGER_TOL': (0.005, 'Relative E_zp and p_rms convergence tolerance.'),
    'QUANTUM_ABS_FLOOR': (1e-9, 'Absolute comparison floor near zero, not a confining term.'),
    'CHAIN_STEPS': (25, 'Number of constrained separation samples.'),
    'CHAIN_EXTRA_DISTANCE': (3.0, 'Scan extension beyond relaxed contact distance, fm.'),
    'ED_SCAN_STEPS': (13, 'Distance scan samples in the pair acceptance test.'),
    'ED_SCAN_FRACTION': (0.15, 'Relative range around relaxed D distance in acceptance test.'),
    'TEST_SUBDIV': (1, 'Coarse mesh used ONLY in software tests, not physical reports.'),
    'TEST_E0': (1.0, 'Arbitrary positive normalization for scale-free isolated acceptance test.'),
    'TEST_EAD': (1.0, 'Uncalibrated adhesion coefficient used ONLY in software/isolated tests.'),
    'FD_STEP': (1e-7, 'Software directional-gradient test step.'),
    'FD_TOL': (1e-5, 'Software directional-gradient relative tolerance.'),
    'GEOM_TEST_TOL': (1e-10, 'Software geometric identity tolerance.'),
    'TEST_PERTURBATION': (0.001, 'Random fixture displacement in fm ONLY to avoid exact face-selection kinks in derivative tests.'),
    'TEST_SEED': (7341, 'Reproducible software-test seed.'),
    'ROTATION_ANGLE': (0.731, 'Rotation used to test covariance, radians.'),
    'SCALE_LOWER': (0.95, 'Lower bracket for diagnostic uniform-scaling minimization.'),
    'SCALE_UPPER': (1.05, 'Upper bracket for diagnostic uniform-scaling minimization.'),
    'SCALAR_XATOL': (1e-13, 'Diagnostic scalar minimizer tolerance.'),
    'JSON_INDENT': (2, 'Machine output formatting only.'),
    'REPORT_DIGITS': (12, 'Significant digits in automatically generated report tables.'),
    'SMOKE_BUDGET': (25, 'Uncalibrated smoke-test optimizer budget; not an accepted relaxation.'),
}
globals().update({name: entry[0] for name, entry in ADDED.items()})

# Structural directions, not fitted parameters. Winding sign is geometric.
RAY_DIRECTION = (1.0, sqrt(2), sqrt(3))
ROTATION_AXIS = (1.0, sqrt(2), sqrt(3))
PHYSICAL_SOURCES = {
    'HC': 'CODATA 2018, supplied build spec §2',
    'AHC': 'CODATA 2018, supplied build spec §2',
    'ME': 'CODATA 2018, supplied build spec §2',
    'MP': 'CODATA 2018, supplied build spec §2',
    'MN': 'CODATA 2018, supplied build spec §2',
    'RP': 'CODATA 2018, supplied build spec §2',
    'RN': 'Posit P1, supplied build spec §2 (not an empirical radius)',
    'BE_D': 'AME2020, supplied calibration input',
    'BE_HE4': 'AME2020, supplied calibration input',
    'E_SINGLET': 'Supplied calibration input',
    'CPRIME': 'Computed from supplied masses',
    'E_PATCH_D': 'Computed BE_D - 2 Y(2)',
    'E_MESH': 'Computed E_PATCH_D - E_SINGLET, literal §4.2',
}


@dataclass(frozen=True)
class Parameters:
    e0: float
    E0: float
    delta: float
    area_factor: float = AREA_FACTOR
    bend_fraction: float = BEND_PRIMARY
    fade: str = 'linear'
    mesh_energy: float = E_MESH

    def __post_init__(self):
        if not (self.e0 > 0 and self.E0 > 0 and self.delta > 0):
            raise ValueError('e0, E0 and delta must be strictly positive.')
        if self.fade not in ('linear', 'quadratic'):
            raise ValueError('Unknown adhesion fade.')
        if self.area_factor <= 0 or self.bend_fraction < 0:
            raise ValueError('Invalid skin penalty or bending coefficient.')

    def to_dict(self):
        return asdict(self)


def K_AREA(E0: float, radius: float, factor: float = AREA_FACTOR) -> float:
    return factor * E0 / (4 * pi * radius ** 2)


def K_PEN(e0: float) -> float:
    return PEN_FACTOR * e0 / PEN_SCALE ** 2


def K_BEND(E0: float, fraction: float = BEND_PRIMARY) -> float:
    return fraction * E0
