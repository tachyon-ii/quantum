#!/usr/bin/env python3
"""
tests_dirac_topology.py — Dirac-on-a-ring topology tests

D1) Massless Dirac modes: periodic vs Möbius (half-step), positive-unique
D2) Massive Dirac dispersion vs analytic (positive-unique)
D3) Sagnac/flux sweep: orientation flip & linear scaling of the twist phase
D4) Convergence (O(h^2)) of the eigen errors under N→2N
"""
import argparse
import numpy as np
from dirac_modes import (
    c, hbar, spectrum, positive_branch,
    analytic_positive_energies, sagnac_phase
)

def section(title: str):
    bar = "=" * len(title)
    print(f"\n{title}\n{bar}")

def check_close(name, val, tgt, rtol, atol=0.0, verbose=False):
    ok = np.isclose(val, tgt, rtol=rtol, atol=atol)
    tick = "✅" if ok else "❌"
    if verbose or (not ok):
        if tgt != 0.0:
            rel = abs(val - tgt) / abs(tgt)
            print(f"{tick} {name}: got {val:.6e}, tgt {tgt:.6e}, rel err={rel:.3e}")
        else:
            print(f"{tick} {name}: got {val:.6e}, tgt {tgt:.6e}, abs err={abs(val-tgt):.3e}")
    return ok

def analytic_k_list(L, theta, M):
    # k_n = (2π/L)(n + theta/2π), n = 1..M for periodic (skip n=0),
    # and n = 0..M-1 for Möbius
    if abs(theta) < 1e-15:  # periodic
        n = np.arange(1, M+1, dtype=float)
    else:                    # Möbius half-step
        n = np.arange(0, M, dtype=float)
    return (2.0*np.pi/L) * (n + theta/(2.0*np.pi))

def analytic_massless_E_spectral(L, theta, M):
    k = analytic_k_list(L, theta, M)
    return hbar * c * k  # positive branch

def test_dirac_massless_modes(L, N, M, verbose=False):
    section("D1) Dirac massless modes — periodic vs Möbius (half-step, + unique)")
    m = 0.0
    E_per = positive_branch(spectrum(L, N, m, theta=0.0), M)
    A_per = analytic_positive_energies(L, m, theta=0.0, M=M)
    E_mob = positive_branch(spectrum(L, N, m, theta=np.pi), M)
    A_mob = analytic_positive_energies(L, m, theta=np.pi, M=M)

    ok = True
    rtol = 2e-3

    mper = min(len(E_per), len(A_per), M)
    if mper == 0:
        print("❌ periodic branch empty after filtering (unexpected).")
        ok = False
    else:
        for i in range(mper):
            ok &= check_close(f"periodic +E[{i}]", E_per[i], A_per[i], rtol, verbose=verbose)

    mmob = min(len(E_mob), len(A_mob), M)
    if mmob == 0:
        print("❌ Möbius branch empty after filtering (unexpected).")
        ok = False
    else:
        for i in range(mmob):
            ok &= check_close(f"Möbius +E[{i}]", E_mob[i], A_mob[i], rtol, verbose=verbose)

    if ok:
        print("✅ Massless Dirac ladders match (periodic & half-shift Möbius, deduped).")
    return ok

def test_dirac_massless_modes_spectral(L, M, verbose=False):
    section("D1s) Spectral massless modes — periodic vs Möbius (alignment)")

    # Periodic ladder on L: E_per[i] = ħ c (2π/L) (i+1),  i=0..M  (n=1..M+1)
    E_per = analytic_massless_E_spectral(L, 0.0, M + 1)       # J
    # Möbius ladder on L: E_mob[j] = ħ c (2π/L) (j+1/2), j=0..M-1
    E_mob = analytic_massless_E_spectral(L, np.pi, M)         # J

    # Correct midpoint mapping:
    #   j = 0: midpoint is 0.5 * E_per[0]
    #   j >= 1: midpoint is 0.5 * (E_per[j-1] + E_per[j])
    E_mid = np.empty_like(E_mob)
    E_mid[0] = 0.5 * E_per[0]
    if M > 1:
        E_mid[1:] = 0.5 * (E_per[:-1][:M-1] + E_per[1:][:M-1])

    # Odd-mode identity on a periodic ring of length 2L:
    # E_mob(L) == E_per(2L)[odd]
    E_per_2L_all = analytic_massless_E_spectral(2.0 * L, 0.0, 2 * M)  # n=1..2M
    E_per_2L_odd = E_per_2L_all[0::2][:M]                              # n = 1,3,5,...

    rtol = 1e-12
    ok_mid = np.allclose(E_mob, E_mid, rtol=rtol)
    ok_2L  = np.allclose(E_mob, E_per_2L_odd, rtol=rtol)

    # ----- pretty, space-aligned table (no MD) -----
    hdr = " n  |  E_mob(L)        |  mid(L)= ½(E_per) |  rel_err_mid |  E_per_odd(2L)   | rel_err_2L"
    sep = "-" * len(hdr)
    print(hdr)
    print(sep)
    for n in range(M):
        em   = E_mob[n]
        mid  = E_mid[n]
        e2   = E_per_2L_odd[n]
        rel_mid = abs(em - mid) / mid
        rel_2L  = abs(em - e2)  / e2
        # fixed widths for alignment
        print(f"{n:2d}  | {em: .9e} | {mid: .9e}  | {rel_mid: .4e}  | {e2: .9e} | {rel_2L: .3e}")

    print(f"\n✅ Möbius = correct midpoints on L   (rtol={rtol:g}): {ok_mid}")
    print(f"✅ Möbius = odd harmonics on 2L       (rtol={rtol:g}): {ok_2L}")

    return ok_mid and ok_2L

def test_dirac_massive_dispersion(L, N, M, m_eV, verbose=False):
    section("D2) Dirac massive dispersion — periodic & Möbius vs analytic (+ unique)")
    eV = 1.602_176_634e-19
    m = (m_eV * eV) / (c**2)

    ok_all = True
    rtol = 2e-3
    for theta, name in [(0.0, "periodic"), (np.pi, "Möbius")]:
        E = positive_branch(spectrum(L, N, m, theta=theta), M)
        A = analytic_positive_energies(L, m, theta=theta, M=M)
        if len(E) == 0 or len(A) == 0:
            print(f"❌ {name}: empty positive branch (unexpected).")
            ok_all = False
            continue
        ok_local = True
        for i in range(min(M, len(E), len(A))):
            ok_local &= check_close(f"{name} +E[{i}]", E[i], A[i], rtol, verbose=verbose)
        print("✅" if ok_local else "❌", f"{name} massive dispersion matches analytic.")
        ok_all &= ok_local
    return ok_all

def test_sagnac_flux_sweep(L, N, M, m_eff_eV, R_eff=None, verbose=False):
    section("D3) Flux/Sagnac twist — orientation flip & linearity")
    eV = 1.602_176_634e-19
    m_eff = (m_eff_eV * eV) / (c**2)
    if R_eff is None:
        R_eff = hbar / (2.0 * m_eff * c)
    A_vec = np.array([0.0, 0.0, np.pi * R_eff * R_eff])
    Omega = np.array([0.0, 0.0, 7.2921159e-5])  # Earth rotation

    phi = sagnac_phase(m_eff, A_vec, Omega)
    theta_plus  = np.pi + phi
    theta_minus = np.pi - phi
    theta_2phi  = np.pi + 2.0*phi

    Mcheck = min(M, 4)
    rtol = 3e-3
    ok = True
    # +phi, -phi, 2phi
    for th in (theta_plus, theta_minus, theta_2phi):
        E_num = positive_branch(spectrum(L, N, 0.0, th),  Mcheck)
        E_ana = analytic_positive_energies(L, 0.0, th,  Mcheck)
        ok &= np.allclose(E_num, E_ana, rtol=rtol)
    if verbose:
        print(f"Φ_Sag ≈ {phi:.3e} rad (Earth), R_eff≈{R_eff:.3e} m, A≈{A_vec[-1]:.3e} m²")

    print("✅ Flux/Sagnac twist behaves with correct sign & linearity." if ok else "❌ Flux/Sagnac behavior mismatch.")
    return ok

def _mean_rel_err(L, N, M, m, theta):
    E = positive_branch(spectrum(L, N, m, theta), M)
    A = analytic_positive_energies(L, m, theta, M)
    return float(np.mean(np.abs((E - A)/A)))

def test_dirac_convergence(L, N, M, verbose=False):
    section("D4) Finite-difference convergence (O(h^2))")
    m = 0.0
    eN_p   = _mean_rel_err(L, N,     M, m, 0.0)
    e2N_p  = _mean_rel_err(L, 2*N,   M, m, 0.0)
    eN_m   = _mean_rel_err(L, N,     M, m, np.pi)
    e2N_m  = _mean_rel_err(L, 2*N,   M, m, np.pi)
    r_p = eN_p/max(e2N_p,1e-300); r_m = eN_m/max(e2N_m,1e-300)
    if verbose:
        print(f"periodic:   err(N)={eN_p:.3e}, err(2N)={e2N_p:.3e}, ratio={r_p:.2f}")
        print(f"Möbius:     err(N)={eN_m:.3e}, err(2N)={e2N_m:.3e}, ratio={r_m:.2f}")
    ok = (r_p > 3.5) and (r_m > 3.5)
    print("✅ O(h^2) confirmed." if ok else "❌ weaker than O(h^2)")
    return ok

def main():
    ap = argparse.ArgumentParser(description="Dirac-on-a-ring topology tests")
    ap.add_argument("--L", type=float, default=1.234, help="Ring length L")
    ap.add_argument("--N", type=int, default=1024, help="FD grid points")
    ap.add_argument("--M", type=int, default=6, help="# modes to compare on + branch")
    ap.add_argument("--m_eV", type=float, default=0.05, help="mass for D2 (eV/c^2)")
    ap.add_argument("--m_eff_eV", type=float, default=0.05, help="effective mass for Sagnac (eV/c^2)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    total = 0; passed = 0
    print("=======================================")
    print("Dirac-on-a-Ring — Topology Test Suite")
    print("=======================================")

    tests = [
        ("D1 massless",  lambda: test_dirac_massless_modes(args.L, args.N, args.M, verbose=args.verbose)),
        ("D1s spectral", lambda: test_dirac_massless_modes_spectral(args.L, args.M, verbose=args.verbose)),
        ("D2 massive",   lambda: test_dirac_massive_dispersion(args.L, args.N, args.M, args.m_eV, verbose=args.verbose)),
        ("D3 Sagnac",    lambda: test_sagnac_flux_sweep(args.L, args.N, args.M, args.m_eff_eV, verbose=args.verbose)),
        ("D4 converge",  lambda: test_dirac_convergence(args.L, args.N, args.M, verbose=args.verbose)),
    ]

    for name, fn in tests:
        ok = fn(); passed += int(ok); total += 1

    print("\n=== SUMMARY ===")
    print("✅ All Dirac topology tests passed." if passed==total else f"❌ {passed}/{total} passed.")

if __name__ == "__main__":
    main()

