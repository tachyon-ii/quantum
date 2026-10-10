#!/usr/bin/env python3
"""
tests/alpha-ladder/ladder.py -- the α-ladder test of specs/alpha-ladder.md, then the extension.

Phase 1  α-conjugate nuclei Ne-20..Ni-56: BE = Nα*28.2957 + q*E(Nα), q = 2.42 fixed.
         E from (a) the tetrahedral growth rule 3N-6, (b) maximal sticky-sphere contacts found
         by search (re-derived here, not copied).
Phase 2  Valley of stability A <= 238 (most-bound isobar per A): the fewest-constant extension.
Phase 3  Bethe-Weizsacker, 5 constants fitted on the same set, as the baseline.

Usage: python3 tests/alpha-ladder/ladder.py data/ame2020-mass-table-rows-only.txt > tests/alpha-ladder/results.md
"""
import sys, re, itertools
import numpy as np

BE_ALPHA, Q = 28.2957, 2.42

# ------------------------------------------------------------------ AME 2020
def read_ame(path):
    """rows-only AME2020: N Z A EL [flag] mass_excess unc BE/A unc ...  -> {(Z,A): BE_total_MeV}"""
    out = {}
    for line in open(path, encoding="latin-1"):
        m = re.match(r"\s*(\d+)\s+(\d+)\s+(\d+)\s+([A-Za-z]+)\s+(?:-?[a-z]+\s+)?(-?[\d.]+#?)\s+([\d.]+#?)\s+(-?[\d.]+#?)\s+([\d.]+#?)", line)
        if not m: continue
        N, Z, A = int(m.group(1)), int(m.group(2)), int(m.group(3))
        bea = m.group(7)
        if bea.endswith("#"): continue                       # estimated, not measured
        out[(Z, A)] = float(bea) * A / 1000.0                # BE/A keV -> total MeV
    return out

# ------------------------------------------------------------------ sphere packing search
def contacts(P, tol=1e-3):
    D = np.linalg.norm(P[:, None] - P[None], axis=2)
    return int(((D < 1 + tol) & (D > 0)).sum() // 2), D

def tetra_growth(n):
    """tetrahedral growth: each new sphere placed in the 3-fold hollow that maximises contacts."""
    P = [np.zeros(3), np.array([1, 0, 0]), np.array([0.5, np.sqrt(3) / 2, 0])]
    while len(P) < n:
        A = np.array(P); best = None
        for i, j, k in itertools.combinations(range(len(A)), 3):
            if not (abs(np.linalg.norm(A[i] - A[j]) - 1) < 1e-6 and abs(np.linalg.norm(A[i] - A[k]) - 1) < 1e-6
                    and abs(np.linalg.norm(A[j] - A[k]) - 1) < 1e-6): continue
            c = (A[i] + A[j] + A[k]) / 3; nrm = np.cross(A[j] - A[i], A[k] - A[i]); nrm /= np.linalg.norm(nrm)
            h = np.sqrt(2 / 3)
            for s in (1, -1):
                p = c + s * h * nrm
                if np.min(np.linalg.norm(A - p, axis=1)) < 1 - 1e-6: continue
                cnt, _ = contacts(np.vstack([A, p]))
                if best is None or cnt > best[0]: best = (cnt, p)
        P.append(best[1])
    return np.array(P)

def max_contacts_search(n, trials=60, seed=0):
    """sticky-sphere search: start from tetrahedral growth and random hcp/fcc fragments, then
    local moves that keep non-overlap and increase contacts.  Returns the best count found."""
    rng = np.random.default_rng(seed)
    best = contacts(tetra_growth(n))[0]
    # fcc / hcp lattice fragments: pick n lattice sites from a compact ball, many random centres
    a = np.array([[1, 0, 0], [0.5, np.sqrt(3) / 2, 0], [0.5, np.sqrt(3) / 6, np.sqrt(2 / 3)]])
    pts = np.array([i * a[0] + j * a[1] + k * a[2] for i in range(-4, 5) for j in range(-4, 5) for k in range(-4, 5)])
    for t in range(trials):
        c = pts[rng.integers(len(pts))] + rng.normal(0, 0.4, 3)
        order = np.argsort(np.linalg.norm(pts - c, axis=1))
        P = pts[order[:n]].astype(float)
        cnt, _ = contacts(P)
        # greedy improvement: move one sphere to the hollow that maximises contacts
        improved = True
        while improved:
            improved = False
            for idx in range(n):
                A = np.delete(P, idx, 0)
                cand = []
                for i, j, k in itertools.combinations(range(n - 1), 3):
                    if not (abs(np.linalg.norm(A[i] - A[j]) - 1) < 1e-6 and abs(np.linalg.norm(A[i] - A[k]) - 1) < 1e-6
                            and abs(np.linalg.norm(A[j] - A[k]) - 1) < 1e-6): continue
                    cc = (A[i] + A[j] + A[k]) / 3; nrm = np.cross(A[j] - A[i], A[k] - A[i]); nrm /= np.linalg.norm(nrm)
                    for s in (1, -1):
                        p = cc + s * np.sqrt(2 / 3) * nrm
                        if np.min(np.linalg.norm(A - p, axis=1)) < 1 - 1e-6: continue
                        cand.append(p)
                for p in cand:
                    c2, _ = contacts(np.vstack([A, p]))
                    if c2 > cnt: P = np.vstack([A, p]); cnt = c2; improved = True; break
                if improved: break
        best = max(best, cnt)
    return best

# ------------------------------------------------------------------ phases
def phase1(ame):
    print("## Phase 1 — α-conjugate ladder, q = 2.42 fixed, no refit\n")
    print("Contact counts, derived here (tetrahedral growth 3N−6 vs best sticky-sphere packing found by search):\n")
    print("| Nα | 3N−6 | E_max (search) |"); print("|---|---|---|")
    Emax = {}
    for n in range(3, 15):
        Emax[n] = max_contacts_search(n, trials=40 if n <= 10 else 25)
        print(f"| {n} | {3*n-6} | {Emax[n]} |")
    print("\n| nucleus | Nα | AME BE | pred 3N−6 | err | pred E_max | err |"); print("|---|---|---|---|---|---|---|")
    names = {5: "Ne-20", 6: "Mg-24", 7: "Si-28", 8: "S-32", 9: "Ar-36", 10: "Ca-40", 11: "Ti-44", 12: "Cr-48", 13: "Fe-52", 14: "Ni-56"}
    ok_t = ok_m = 0; rows = []
    for n in range(5, 15):
        Z = 2 * n; A = 4 * n; be = ame[(Z, A)]
        pt = n * BE_ALPHA + Q * (3 * n - 6); pm = n * BE_ALPHA + Q * Emax[n]
        et, em = 100 * (pt - be) / be, 100 * (pm - be) / be
        ok_t += abs(et) <= 2; ok_m += abs(em) <= 2
        print(f"| {names[n]} | {n} | {be:.3f} | {pt:.3f} | {et:+.2f}% | {pm:.3f} | {em:+.2f}% |")
    print(f"\nwithin 2 %: 3N−6 rule {ok_t}/10, maximal-contact rule {ok_m}/10.")
    print("Calibration points (not scored): C-12 %.3f vs %.3f, O-16 %.3f vs %.3f; Be-8 excess %.3f (open edge, unbound)." % (
        3 * BE_ALPHA + 3 * Q, ame[(6, 12)], 4 * BE_ALPHA + 6 * Q, ame[(8, 16)], ame[(4, 8)] - 2 * BE_ALPHA))
    # implied bond energy per nucleus under 3N-6, to show drift (or not)
    print("\nImplied q per nucleus under 3N−6 (AME excess / (3N−6)): " +
          "  ".join(f"{names[n]} {(ame[(2*n,4*n)] - n*BE_ALPHA)/(3*n-6):.3f}" for n in range(5, 15)))

def valley(ame, amax=238):
    out = {}
    for (Z, A), be in ame.items():
        if A <= amax and A >= 2 and (A not in out or be > out[A][1]): out[A] = (Z, be)
    return out

def rms(pred, data):
    e = np.array(pred) - np.array(data); return np.sqrt(np.mean(e ** 2)), np.sqrt(np.mean((e / np.array(data)) ** 2)) * 100

def phase2(ame):
    print("\n## Phase 2 — valley of stability to U-238, α-ladder extended with the fewest constants\n")
    V = valley(ame); As = sorted(a for a in V if a >= 12)
    data = [V[a][1] for a in As]
    # decomposition: Nα = min(Z, N)//2 alphas ... honest, simple: Nα = Z//2 (every proton pair is an α with a neutron pair);
    # loose neutrons Nx = N - 2*Nα, loose protons Px = Z - 2*Nα (0 or 1)
    rows = []
    for a in As:
        Z, be = V[a]; N = a - Z; na = Z // 2; nx = N - 2 * na; px = Z - 2 * na
        rows.append((a, Z, N, na, nx, px, be))
    # Model L1: ladder + e_n per loose neutron (1 new constant, fitted)
    X1 = np.array([[nx] for (a, Z, N, na, nx, px, be) in rows], float)
    base = np.array([na * BE_ALPHA + Q * (3 * na - 6) for (a, Z, N, na, nx, px, be) in rows])
    y = np.array(data) - base
    e_n = float(np.linalg.lstsq(X1, y, rcond=None)[0][0])
    pred1 = base + X1[:, 0] * e_n
    r1 = rms(pred1, data)
    print(f"L1: BE = Nα·28.296 + 2.42·(3Nα−6) + e_n·N_loose, e_n fitted = {e_n:.3f} MeV  ->  RMS {r1[0]:.2f} MeV, {r1[1]:.2f} % of BE   (1 new constant)")
    # Model L2: + Coulomb-like growth: loose neutrons pay e_n but α-α bonds weaken as Z grows: q(Z) = q - c*Z... keep it to one more constant:
    X2 = np.column_stack([X1[:, 0], np.array([(3 * na - 6) * Z / a ** (1 / 3) for (a, Z, N, na, nx, px, be) in rows])])
    coef = np.linalg.lstsq(X2, y, rcond=None)[0]
    pred2 = base + X2 @ coef; r2 = rms(pred2, data)
    print(f"L2: L1 + Coulomb-shaped bond weakening c·E·Z/A^(1/3), e_n = {coef[0]:.3f}, c = {coef[1]:.4f}  ->  RMS {r2[0]:.2f} MeV, {r2[1]:.2f} %   (2 new constants)")
    # Model L3: + neutron-excess penalty (I^2/A) -- this is the drop model's symmetry term arriving
    X3 = np.column_stack([X2, np.array([(N - Z) ** 2 / a for (a, Z, N, na, nx, px, be) in rows])])
    coef3 = np.linalg.lstsq(X3, y, rcond=None)[0]
    pred3 = base + X3 @ coef3; r3 = rms(pred3, data)
    print(f"L3: L2 + symmetry (N−Z)²/A, coefs {np.round(coef3, 4).tolist()}  ->  RMS {r3[0]:.2f} MeV, {r3[1]:.2f} %   (3 new constants)")
    print("\n| A | nucleus | AME | L1 | err | L3 | err |"); print("|---|---|---|---|---|---|---|")
    for i, (a, Z, N, na, nx, px, be) in enumerate(rows):
        if a in (12, 16, 20, 28, 40, 56, 90, 120, 138, 160, 180, 208, 232, 238):
            print(f"| {a} | Z={Z} | {be:.1f} | {pred1[i]:.1f} | {100*(pred1[i]-be)/be:+.1f}% | {pred3[i]:.1f} | {100*(pred3[i]-be)/be:+.1f}% |")
    return As, data, rows

def phase3(ame, As, data, rows):
    print("\n## Phase 3 — Bethe–Weizsäcker baseline, 5 constants fitted on the same nuclei\n")
    X = []
    for (a, Z, N, na, nx, px, be) in rows:
        delta = 1 if (Z % 2 == 0 and N % 2 == 0) else (-1 if (Z % 2 == 1 and N % 2 == 1) else 0)
        X.append([a, -a ** (2 / 3), -Z * (Z - 1) / a ** (1 / 3), -(a - 2 * Z) ** 2 / a, delta / a ** 0.5])
    X = np.array(X); coef = np.linalg.lstsq(X, np.array(data), rcond=None)[0]
    pred = X @ coef; r = rms(pred, data)
    print(f"a_v {coef[0]:.3f}  a_s {coef[1]:.3f}  a_c {coef[2]:.4f}  a_a {coef[3]:.3f}  a_p {coef[4]:.2f}  ->  RMS {r[0]:.2f} MeV, {r[1]:.2f} %   (5 constants)")
    # drop model restricted to the α-conjugate ladder, for a like-for-like with phase 1
    sel = [i for i, (a, Z, N, na, nx, px, be) in enumerate(rows) if Z == N and Z % 2 == 0 and 20 <= a <= 56]
    e = [100 * (pred[i] - data[i]) / data[i] for i in sel]
    print(f"on the Phase-1 ladder nuclei the 5-constant drop model errs by {min(e):+.2f}% .. {max(e):+.2f}% (the 1-constant ladder: see Phase 1).")

if __name__ == "__main__":
    ame = read_ame(sys.argv[1])
    print(f"# tests/alpha-ladder results — AME2020, {len(ame)} measured nuclides\n")
    phase1(ame)
    As, data, rows = phase2(ame)
    phase3(ame, As, data, rows)
