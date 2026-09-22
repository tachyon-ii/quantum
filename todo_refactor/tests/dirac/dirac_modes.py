#!/usr/bin/env python3
"""
dirac_modes.py — 1D Dirac on a ring (periodic / Möbius / AB–Sagnac twist)

H = -i ħ c α ∂_s + β m c^2, with α = σ_x, β = σ_z.
Boundary: ψ(s+L) = exp(i * theta) ψ(s).
"""
from __future__ import annotations
import numpy as np

# constants (SI)
c    = 299_792_458.0
hbar = 1.054_571_817e-34

# Pauli
sigma_x = np.array([[0,1],[1,0]], dtype=complex)
sigma_z = np.array([[1,0],[0,-1]], dtype=complex)

def build_D_matrix(N: int, L: float, theta: float = 0.0) -> np.ndarray:
    """
    Central-difference first derivative ∂/∂s on a ring of length L.
    Twist: ψ_{i+N} = e^{i theta} ψ_i  ⇒ wrap couplings carry e^{±i theta}.
    """
    h = L / N
    D = np.zeros((N, N), dtype=complex)
    for i in range(N):
        D[i, (i+1) % N] +=  0.5 / h
        D[i, (i-1) % N] += -0.5 / h
    # enforce twist phases at the wrap entries
    D[0,  N-1] = - np.exp(-1j*theta) * 0.5 / h
    D[N-1, 0]  =   np.exp(+1j*theta) * 0.5 / h
    return D

def dirac_hamiltonian(L: float, N: int, m_kg: float, theta: float = 0.0) -> np.ndarray:
    """Build the 2N×2N Hermitian Dirac Hamiltonian with twist theta."""
    D = build_D_matrix(N, L, theta)
    I = np.eye(N, dtype=complex)
    H_kin  = -1j * hbar * c * np.kron(sigma_x, D)
    H_mass =        (m_kg * c**2) * np.kron(sigma_z, I)
    return H_kin + H_mass

def spectrum(L: float, N: int, m_kg: float, theta: float = 0.0) -> np.ndarray:
    """Full eigenvalue spectrum (sorted) of the Dirac Hamiltonian."""
    H = dirac_hamiltonian(L, N, m_kg, theta)
    E, _ = np.linalg.eigh(H)     # Hermitian ⇒ real eigenvalues
    return np.sort(np.real(E))

def _scale_eps(arr: np.ndarray) -> float:
    """
    Very gentle, relative cutoff ~ 1e-12 of the spectral scale (no 1.0 J floor).
    Prevents swallowing tiny-but-physical energies on large rings.
    """
    if arr.size == 0:
        return 1e-300
    m = float(np.max(np.abs(arr)))
    return 1e-12 * max(m, 1e-300)

def _unique_sorted(vals: np.ndarray, rel_tol: float = 1e-12) -> np.ndarray:
    """Collapse near-duplicate positive values to unique entries (degeneracy removal)."""
    vals = np.asarray(vals, float)
    vals = vals[vals > 0.0]
    if vals.size == 0:
        return np.array([], float)
    vals = np.sort(vals)
    out = [vals[0]]
    for v in vals[1:]:
        if abs(v - out[-1]) > rel_tol * max(1.0, abs(out[-1])):
            out.append(v)
    return np.array(out, float)

def positive_branch(E: np.ndarray, M: int) -> np.ndarray:
    """
    Return the first M strictly-positive **unique** energies.
    """
    E = np.asarray(E, float)
    eps = _scale_eps(E)                  # relative cutoff
    pos = E[E > eps]                     # drop zero mode & numerical fuzz
    pos_unique = _unique_sorted(pos, rel_tol=1e-12)
    # Fallback: if somehow empty, be permissive and dedup sign-positive
    if pos_unique.size == 0:
        pos_unique = _unique_sorted(E[E > 0.0], rel_tol=1e-12)
    return pos_unique[:M]

def analytic_energies(L: float, m_kg: float, theta: float, n: np.ndarray) -> np.ndarray:
    """E_n = +sqrt( (ħ c k_n)^2 + (m c^2)^2 ),  k_n=(2π/L)(n + theta/2π)."""
    k = (2.0*np.pi/L) * (n + theta/(2.0*np.pi))
    return np.sqrt((hbar*c*k)**2 + (m_kg*c**2)**2)

def analytic_positive_energies(L: float, m_kg: float, theta: float, M: int) -> np.ndarray:
    """
    Analytic counterpart to positive_branch: generate more than needed, drop zeros,
    deduplicate, return first M positive unique energies.
    """
    n = np.arange(0, 4*M + 16, dtype=float)     # overshoot generously
    En = analytic_energies(L, m_kg, theta, n)
    eps = _scale_eps(En)
    pos = En[En > eps]
    pos_unique = _unique_sorted(pos, rel_tol=1e-12)
    return pos_unique[:M]

def sagnac_phase(m_eff: float, A_vec, Omega_vec) -> float:
    """Matter-wave Sagnac phase: Φ_Sag = (2 m_eff / ħ) (Ω·A) [dimensionless]."""
    A_vec = np.asarray(A_vec, float)
    Omega_vec = np.asarray(Omega_vec, float)
    return (2.0 * m_eff / hbar) * float(np.dot(Omega_vec, A_vec))

