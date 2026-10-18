#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""All-vertex L-BFGS-B with exact affine constraints and autograd gradients.

Centres are derived observables. Constraints are affine projections of vertex
coordinates, never an optimization over independently introduced centres.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import time
import numpy as np
import torch
from scipy.optimize import minimize
from scipy.sparse.linalg import LinearOperator, eigsh, ArpackNoConvergence
from . import constants as C
from .mesh import DTYPE, GeometryError
from .energy import Functional, Evaluation


class DeadlineExceeded(RuntimeError):
    pass


@dataclass
class Deadline:
    seconds: float | None = C.RUNTIME_TARGET_S
    started: float = field(default_factory=time.monotonic)

    def check(self):
        if self.seconds is not None and time.monotonic() - self.started > self.seconds:
            raise DeadlineExceeded('Declared run wall-time budget exhausted; no unfinished measurement is reported as a result.')


@dataclass
class ExternalForce:
    capsid: int
    force: np.ndarray
    nodal_weights: np.ndarray

    def work_potential(self, x):
        w = torch.as_tensor(self.nodal_weights, dtype=DTYPE)
        f = torch.as_tensor(self.force, dtype=DTYPE)
        return -(w[:, None] * x[self.capsid] * f).sum()


class Constraints:
    """An affine projector; simultaneous equations solved in a small Gram system.

    Frozen skins' vertices are omitted from the variable vector. Free vertex
    centroid constraints use an orthogonal projection, leaving harmless null
    gauge coordinates but pinning the physical geometry to roundoff.
    """
    def __init__(self, reference: np.ndarray, *, pin_system: bool = True,
                 pinned_centres: dict[int, np.ndarray] | None = None,
                 frozen: dict[int, np.ndarray] | None = None):
        self.reference = np.array(reference, dtype=float, copy=True)
        self.shape = self.reference.shape
        self.frozen = frozen or {}
        self.free_capsids = tuple(i for i in range(self.shape[0]) if i not in self.frozen)
        if not self.free_capsids:
            raise ValueError('No unconstrained vertices remain.')
        nv = self.shape[1]
        self.nv = nv
        constraints, rhs = [], []
        for i, value in self.frozen.items():
            value = np.asarray(value)
            if value.shape != self.reference[i].shape:
                raise ValueError('Frozen skin has wrong shape.')
            self.reference[i] = value
        if pin_system:
            # Target is the caller's original system centroid (before freezing).
            target = np.asarray(reference).mean(axis=(0, 1)) * self.shape[0]
            fixed_sum = sum((self.reference[i].mean(axis=0) for i in self.frozen), start=np.zeros(3))
            constraints.append(np.ones(len(self.free_capsids)))
            rhs.append(target - fixed_sum)
        for i, target in (pinned_centres or {}).items():
            if i in self.frozen:
                if not np.allclose(self.reference[i].mean(axis=0), target, atol=C.GEOM_TEST_TOL, rtol=0):
                    raise ValueError('Conflicting frozen and centroid constraints.')
            else:
                row = np.zeros(len(self.free_capsids)); row[self.free_capsids.index(i)] = 1
                constraints.append(row); rhs.append(np.asarray(target))
        self.A = np.asarray(constraints).reshape(-1, len(self.free_capsids))
        self.b = np.asarray(rhs).reshape(-1, 3)
        if len(self.A):
            self.pinv = np.linalg.pinv(self.A @ self.A.T)
            if np.max(np.abs(self.A @ self.A.T @ self.pinv @ self.b - self.b)) > C.GEOM_TEST_TOL:
                raise ValueError('Inconsistent affine constraints.')
        else:
            self.pinv = np.empty((0, 0))

    def pack(self, vertices):
        return np.asarray(vertices)[list(self.free_capsids)].ravel().copy()

    def decode_torch(self, q):
        free = q.reshape(len(self.free_capsids), self.nv, 3)
        if len(self.A):
            a, b, inv = (torch.as_tensor(t, dtype=DTYPE) for t in (self.A, self.b, self.pinv))
            correction = a.T @ inv @ (a @ free.mean(dim=1) - b)
            free = free - correction[:, None]
        skins = []
        for i in range(self.shape[0]):
            skins.append(torch.as_tensor(self.reference[i], dtype=DTYPE) if i in self.frozen
                         else free[self.free_capsids.index(i)])
        return torch.stack(skins)

    def decode(self, q):
        return self.decode_torch(torch.as_tensor(q, dtype=DTYPE)).numpy()


@dataclass
class Relaxation:
    vertices: np.ndarray
    evaluation: Evaluation | None
    converged: bool
    status: str
    message: str
    gradient_max: float | None
    iterations: int
    evaluations: int
    elapsed_seconds: float
    objective: float | None
    stability: dict | None = None

    def summary(self):
        return {'converged': self.converged, 'status': self.status, 'message': self.message,
                'gradient_max': self.gradient_max, 'iterations': self.iterations,
                'evaluations': self.evaluations, 'elapsed_seconds': self.elapsed_seconds,
                'objective': self.objective, 'stability': self.stability}


def relax(functional: Functional, initial: np.ndarray | None = None, *,
          constraints: Constraints | None = None, external: ExternalForce | None = None,
          maxiter: int = C.MAXITER, deadline: Deadline | None = None,
          check_stability: bool = False) -> Relaxation:
    start = time.monotonic()
    initial = np.asarray(functional.system.initial if initial is None else initial, dtype=float)
    constraints = constraints or Constraints(initial)
    q0 = constraints.pack(initial)
    evaluations = 0
    last_valid_q = q0.copy()

    def objective(q):
        nonlocal evaluations, last_valid_q
        if deadline:
            deadline.check()
        evaluations += 1
        qt = torch.tensor(q, dtype=DTYPE, requires_grad=True)
        x = constraints.decode_torch(qt)
        value, _ = functional.torch_value(x)
        if external:
            value = value + external.work_potential(x)
        if not torch.isfinite(value):
            raise GeometryError('Nonfinite literal energy.')
        grad, = torch.autograd.grad(value, qt)
        gradient = grad.detach().numpy()
        if not np.isfinite(gradient).all():
            raise GeometryError('Nonfinite autograd derivative.')
        last_valid_q = np.array(q, copy=True)
        return float(value.detach()), gradient

    try:
        result = minimize(objective, q0, method='L-BFGS-B', jac=True,
                          options={'gtol': C.GTOL, 'ftol': C.FTOL, 'maxiter': maxiter,
                                   'maxfun': C.MAXFUN, 'maxls': C.MAXLS, 'maxcor': C.MAXCOR})
        vertices = constraints.decode(result.x)
        evaluation = functional.evaluate(vertices)
        gmax = float(np.max(np.abs(result.jac)))
        converged = bool(result.success and gmax <= C.GTOL)
        answer = Relaxation(vertices, evaluation, converged,
            'stationary' if converged else 'optimizer_failure', str(result.message), gmax,
            int(result.nit), evaluations, time.monotonic() - start, float(result.fun))
        if converged and check_stability:
            answer.stability = stability_probe(objective, result.x, deadline)
            if answer.stability['status'] != 'nonnegative_probed_modes':
                answer.converged = False
                answer.status = 'unstable' if answer.stability['status'] == 'negative_curvature' else 'stability_unresolved'
        return answer
    except DeadlineExceeded:
        raise
    except (GeometryError, FloatingPointError, ValueError) as error:
        vertices = constraints.decode(last_valid_q)
        try:
            evaluation = functional.evaluate(vertices)
        except GeometryError:
            evaluation = None
        return Relaxation(vertices, evaluation, False, 'undefined_trial_geometry', str(error), None,
                          0, evaluations, time.monotonic() - start, None)


def stability_probe(objective, point, deadline=None):
    """Numerical negative-curvature probe, not a proof of a saddle-node.

    Gauge zero modes are retained; a positive result only certifies the sampled
    lowest modes. Failed eigensolves remain unresolved, never labelled stable.
    """
    def product(direction):
        if deadline:
            deadline.check()
        length = np.linalg.norm(direction)
        if length == 0:
            return direction
        step = C.HESSIAN_STEP / length
        return (objective(point + step * direction)[1] - objective(point - step * direction)[1]) / (2 * step)
    op = LinearOperator((len(point), len(point)), matvec=product, dtype=float)
    try:
        eigenvalues = np.sort(eigsh(op, k=min(C.HESSIAN_MODES, len(point) - 1), which='SA',
            return_eigenvectors=False, tol=C.HESSIAN_TOL, maxiter=C.HESSIAN_MAXITER))
        status = 'negative_curvature' if eigenvalues.min() < -C.HESSIAN_NEGATIVE_TOL else 'nonnegative_probed_modes'
        return {'status': status, 'eigenvalues': eigenvalues.tolist(),
                'qualification': 'Finite-difference, finite-mode local test; branch-switching energy is nonsmooth.'}
    except (ArpackNoConvergence, GeometryError, ValueError) as error:
        return {'status': 'unresolved', 'reason': str(error)}
