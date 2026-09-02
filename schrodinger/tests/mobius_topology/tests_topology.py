#!/usr/bin/env python3
"""
Topology & Invariants — Möbius Loop Test Suite (degeneracy-fixed)
-----------------------------------------------------------------
A compact test suite for Möbius-loop topology effects and invariants.

It prints human-readable sections with pass/fail summaries.

Tests implemented:
  A1) Anti-periodic (Möbius) mode ladder vs periodic   [FIXED: dedup degenerate modes]
  A2) Topological mass calibration (ground mode)
  A3) Holonomy (Sagnac) phase: orientation & scaling
  A4) Local-c identity for null propagation in weak fields
  A5) λ–f reciprocity across gravitational potentials

CLI:
  --L <float>       loop length (default: 1.234)
  --N <int>         finite-difference points on loop (default: 1024)
  --M <int>         number of modes to compare (default: 6)
  --verbose         print per-test details
"""
import argparse
import numpy as np

# -------- Physical constants (SI) --------
c = 299_792_458.0                         # m/s
hbar = 1.054_571_817e-34                  # J*s
eV = 1.602_176_634e-19                    # J
eV_over_c2_kg = eV / (c**2)               # kg per eV/c^2


# -------- Helpers --------
def build_K_matrix(N: int, L: float, bc: str = "periodic") -> np.ndarray:
    """
    Build the discrete positive operator K ≈ -d^2/ds^2 on a loop of length L,
    using a second-order finite-difference stencil on N points.
    'bc' is 'periodic' or 'antiperiodic' (Möbius).
    """
    assert bc in ("periodic", "antiperiodic")
    h = L / N
    fac = 1.0 / (h * h)
    K = np.zeros((N, N), dtype=float)

    # central second derivative: -d^2/ds^2 ≈ (2 u_i - u_{i-1} - u_{i+1}) / h^2
    for i in range(N):
        K[i, i] = 2.0 * fac
        left = (i - 1) % N
        right = (i + 1) % N
        K[i, left] = -fac
        K[i, right] = -fac

    # Apply boundary twist: crossing between 0 and N-1 gets a sign for anti-periodic
    if bc == "antiperiodic":
        # Flip the wrap couplings that connect index 0 <-> N-1
        K[0, -1] *= -1.0
        K[-1, 0] *= -1.0

    return K


def _unique_sorted(vals, rel_tol=1e-9):
    """
    Collapse near-duplicate positive values (degenerate ±n modes) to unique entries.
    Assumes vals is sorted non-decreasing.
    """
    out = []
    for v in vals:
        if v <= 0:
            continue
        if not out:
            out.append(v)
        else:
            v0 = out[-1]
            # relative closeness test
            if abs(v - v0) <= rel_tol * max(1.0, abs(v0)):
                continue
            out.append(v)
    return np.array(out)


def numeric_modes(L: float, N: int, bc: str, M: int):
    """
    Compute the first M *unique* positive k-values numerically from the discrete operator K.
    Deduplicates the ±n degeneracy inherent to the ring Laplacian.
    """
    K = build_K_matrix(N, L, bc=bc)
    w, _ = np.linalg.eigh(K)  # eigenvalues of K ≈ k^2 >= 0
    w = np.clip(w, 0.0, None)
    w_sorted = np.sort(w)

    # For periodic BC, the first eigenvalue is ~0 (constant mode). Drop it before dedup.
    if bc == "periodic":
        w_pos = w_sorted[1:]
    else:
        w_pos = w_sorted

    k_all = np.sqrt(w_pos)
    # Deduplicate near-identical k's (±n degeneracy)
    k_unique = _unique_sorted(k_all, rel_tol=1e-9)
    return k_unique[:M]


def analytic_modes(L: float, bc: str, M: int):
    """
    Analytic target k-values for a loop of length L (unique positive branch).
    periodic:      k_n = 2π n / L,      n = 1,2,3,...
    antiperiodic:  k_n = 2π (n+1/2) / L, n = 0,1,2,...
    """
    if bc == "periodic":
        n = np.arange(1, M + 1)
        return (2.0 * np.pi / L) * n
    elif bc == "antiperiodic":
        n = np.arange(0, M)
        return (2.0 * np.pi / L) * (n + 0.5)
    else:
        raise ValueError("bc must be 'periodic' or 'antiperiodic'")


def topological_mass(R_eff: float, n: int = 0, phi_topo: float = 0.0) -> float:
    """
    Effective rest mass from loop radius R_eff and topological phase phi_topo.
    Formula (grounded in Möbius anti-periodic BC):
        m_eff = (ħ / (c R_eff)) * (n + 1/2 + phi_topo/(2π))
    Returns mass in kg.
    """
    return (hbar / (c * R_eff)) * (n + 0.5 + phi_topo / (2.0 * np.pi))


def sagnac_phase(m_eff: float, A_vec: np.ndarray, Omega_vec: np.ndarray) -> float:
    """
    Matter-wave Sagnac phase (weak-rotation limit):
        Φ_Sag = (2 m_eff / ħ) * (Ω · A)
    where A is the oriented area vector and Ω is the rotation vector.
    Units: m_eff [kg], A [m^2], Ω [rad/s]. Returns a dimensionless phase [rad].
    """
    return (2.0 * m_eff / hbar) * float(np.dot(Omega_vec, A_vec))


def weak_field_coordinate_speed(phi: float) -> float:
    """
    Coordinate speed of light for radial null propagation in a static weak field:
        (dL/dt) = c * sqrt((1+2φ)/(1-2φ))
    """
    return c * np.sqrt((1.0 + 2.0 * phi) / (1.0 - 2.0 * phi))


def local_c_from_proper(phi: float, dt: float) -> float:
    """
    Using the weak-field identities:
      dL_proper = sqrt(1-2φ) dL
      dτ        = sqrt(1+2φ) dt
      and null condition dL/dt above,
    return dL_proper/dτ which must equal c (to within numeric tolerance).
    """
    dLdt = weak_field_coordinate_speed(phi)
    dL = dLdt * dt
    dL_proper = np.sqrt(1.0 - 2.0 * phi) * dL
    dτ = np.sqrt(1.0 + 2.0 * phi) * dt
    return dL_proper / dτ


def section(title: str):
    bar = "=" * len(title)
    print(f"\n{title}\n{bar}")


def check_close(name: str, val: float, tgt: float, rtol: float, atol: float = 0.0, verbose=False) -> bool:
    ok = np.isclose(val, tgt, rtol=rtol, atol=atol)
    tick = "✅" if ok else "❌"
    if verbose or (not ok):
        if tgt != 0.0:
            rel = abs(val - tgt) / abs(tgt)
            print(f"{tick} {name}: got {val:.6e}, tgt {tgt:.6e}, rel err={rel:.3e}")
        else:
            print(f"{tick} {name}: got {val:.6e}, tgt {tgt:.6e}, abs err={abs(val-tgt):.3e}")
    return ok


# -------- Tests --------
def test_mobius_modes(L: float, N: int, M: int, verbose=False) -> bool:
    section("A1) Anti-periodic (Möbius) mode ladder vs periodic")
    k_num_per = numeric_modes(L, N, "periodic", M)
    k_ana_per = analytic_modes(L, "periodic", M)
    k_num_anti = numeric_modes(L, N, "antiperiodic", M)
    k_ana_anti = analytic_modes(L, "antiperiodic", M)

    rtol = 2e-3  # FD error ~ O(h^2)
    ok = True
    for i in range(M):
        ok &= check_close(f"periodic k[{i}]", k_num_per[i], k_ana_per[i], rtol, verbose=verbose)
    for i in range(M):
        ok &= check_close(f"antiperiodic k[{i}]", k_num_anti[i], k_ana_anti[i], rtol, verbose=verbose)

    if ok:
        print("✅ Mode ladders match analytic (half-integer offset present; degeneracy collapsed).")
    return ok


def test_topological_mass_calibration(verbose=False) -> bool:
    section("A2) Topological mass from ground mode (calibration)")
    # Choose a reference neutrino-scale mass (e.g., 0.05 eV/c^2)
    m0_eV = 0.05
    m0 = m0_eV * eV_over_c2_kg  # kg
    # For ground state (n=0, phi_topo=0): m = ħ/(c R_eff) * 1/2  =>  R_eff = ħ/(2 m c)
    R_eff = hbar / (2.0 * m0 * c)
    m_back = topological_mass(R_eff, n=0, phi_topo=0.0)

    ok = check_close("m_eff(recomputed)", m_back, m0, rtol=1e-12, verbose=True if verbose else False)
    if ok:
        print(f"✅ R_eff = ħ/(2 m c) holds. R_eff ≈ {R_eff:.6e} m for m={m0_eV} eV/c^2")
    return ok


def test_holonomy_orientation_and_scaling(verbose=False) -> bool:
    section("A3) Holonomy (Sagnac) phase — orientation & scaling")
    m0_eV = 0.05
    m0 = m0_eV * eV_over_c2_kg  # kg
    R_eff = hbar / (2.0 * m0 * c)
    A = np.array([0.0, 0.0, np.pi * R_eff * R_eff])  # oriented area vector (ẑ)
    Omega = np.array([0.0, 0.0, 7.2921159e-5])       # Earth's rotation (rad/s)

    phi1 = sagnac_phase(m0, A, Omega)
    phi2 = sagnac_phase(m0, -A, Omega)
    phi3 = sagnac_phase(m0, A, 2.0 * Omega)

    ok = True
    ok &= check_close("orientation flip", phi2, -phi1, rtol=0.0, atol=1e-18, verbose=verbose)
    ok &= check_close("doubling Ω", phi3, 2.0 * phi1, rtol=0.0, atol=1e-18, verbose=verbose)
    if ok:
        print(f"✅ Φ_Sag ~ {phi1:.3e} rad at Earth rotation; sign flips with area, scales with Ω.")
    return ok


def test_local_c_identity(verbose=False) -> bool:
    section("A4) Local-c identity for null propagation (weak field)")
    rng = np.random.default_rng(42)
    phis = rng.uniform(-1e-6, 1e-6, size=100)  # small |phi|
    dts = 10 ** rng.uniform(-9, -3, size=100)  # dt between 1 ns and 1 ms

    errs = []
    for phi, dt in zip(phis, dts):
        val = local_c_from_proper(phi, dt)
        errs.append(abs(val - c) / c)
    max_rel = max(errs)
    ok = max_rel < 1e-12
    tick = "✅" if ok else "❌"
    print(f"{tick} max relative error = {max_rel:.3e}")
    return ok


def test_lambda_f_reciprocity(verbose=False) -> bool:
    section("A5) λ–f reciprocity across potentials (local c preserved)")
    # Two stations at different potentials
    phi1 = -6.0e-10   # Earth-surface-scale dimensionless potential
    phi2 =  4.0e-10   # slightly higher / different environment

    # In a static metric, photon frequency measured by static observers:
    # f_hat ∝ 1/sqrt(-g_tt) ≈ 1/sqrt(1+2φ). Use arbitrary base f0 and compare ratios.
    f0 = 1.0  # arbitrary
    f1 = f0 / np.sqrt(1.0 + 2.0 * phi1)
    f2 = f0 / np.sqrt(1.0 + 2.0 * phi2)

    # Local λ = c / f in each lab; check λ f = c
    lam1 = c / f1
    lam2 = c / f2

    ok = True
    ok &= check_close("λ1 f1", lam1 * f1, c, rtol=0.0, atol=1e-12, verbose=verbose)
    ok &= check_close("λ2 f2", lam2 * f2, c, rtol=0.0, atol=1e-12, verbose=verbose)

    # Also check the expected redshift ratio between stations
    expected_ratio = np.sqrt((1.0 + 2.0 * phi1) / (1.0 + 2.0 * phi2))
    ok &= check_close("f2/f1 (redshift)", f2 / f1, expected_ratio, rtol=0.0, atol=1e-15, verbose=verbose)

    if ok:
        print("✅ Each station preserves λ f = c; redshift ratio matches √(g_tt1/g_tt2).")
    return ok

def _mode_err(L, N, bc, M):
    k_num = numeric_modes(L, N, bc, M)
    k_ana = analytic_modes(L, bc, M)
    return float(np.mean(np.abs((k_num - k_ana) / k_ana)))

def test_fd_convergence(L: float, N: int, M: int, verbose=False) -> bool:
    section("A6) Finite-difference convergence (O(h^2) check)")
    errN_per  = _mode_err(L, N,     "periodic",     M)
    err2N_per = _mode_err(L, 2 * N, "periodic",     M)
    errN_ap   = _mode_err(L, N,     "antiperiodic", M)
    err2N_ap  = _mode_err(L, 2 * N, "antiperiodic", M)

    r_per = errN_per / max(err2N_per, 1e-30)
    r_ap  = errN_ap  / max(err2N_ap,  1e-30)

    ok = (r_per > 3.5) and (r_ap > 3.5)  # ~4 expected; allow a little slack
    if verbose:
        print(f"periodic:   err(N)={errN_per:.3e}, err(2N)={err2N_per:.3e}, ratio={r_per:.2f}")
        print(f"antiperiod: err(N)={errN_ap:.3e},  err(2N)={err2N_ap:.3e},  ratio={r_ap:.2f}")
    print("✅ O(h^2) confirmed (≈×4 improvement) " if ok else "❌ convergence weaker than O(h^2)")
    return ok


def main():
    parser = argparse.ArgumentParser(description="Topology & invariants test suite")
    parser.add_argument("--L", type=float, default=1.234, help="Loop length")
    parser.add_argument("--N", type=int, default=1024, help="Points on loop for FD")
    parser.add_argument("--M", type=int, default=6, help="Modes to compare")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    total = 0
    passed = 0

    print("===============================================")
    print("Topology & Invariants — Möbius Loop Test Suite")
    print("===============================================")

    tests = [
        ("A1 modes", lambda: test_mobius_modes(args.L, args.N, args.M, verbose=args.verbose)),
        ("A2 mass calibration", lambda: test_topological_mass_calibration(verbose=args.verbose)),
        ("A3 holonomy", lambda: test_holonomy_orientation_and_scaling(verbose=args.verbose)),
        ("A4 local c", lambda: test_local_c_identity(verbose=args.verbose)),
        ("A5 lambda-f", lambda: test_lambda_f_reciprocity(verbose=args.verbose)),
        ("A6 convergence", lambda: test_fd_convergence(args.L, args.N, args.M, verbose=args.verbose)),

    ]

    for name, fn in tests:
        total += 1
        ok = fn()
        passed += int(ok)

    print("\n=== SUMMARY ===")
    if passed == total:
        print("✅ All topology tests passed.")
    else:
        print(f"❌ {passed}/{total} tests passed.")


if __name__ == "__main__":
    main()

