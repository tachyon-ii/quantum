
#!/usr/bin/env python3
"""
g_equals_2_mobius_variants_v2.py

Extension of the variants demo:
- Adds CSV export (--csv PATH) of sampled points: r,omega,beta,gamma,g,expected,variant,units
- Adds plotting (--plot PATH.png) of g vs beta for the chosen variant
  (one figure, single line as required; samples log-uniform in r,ω under β_max).

Notes:
- This is still a pedagogical sandbox: the "relativistic" toggles illustrate
  how different modeling choices nudge μ/S, not a full QED treatment.
"""

import math
import random
import argparse
import csv
from typing import Tuple, List

C = 299_792_458.0  # m/s

def gamma_from_r_omega(r: float, omega: float) -> float:
    v = abs(r * omega)
    beta2 = (v / C)**2
    if beta2 >= 1.0:
        return math.inf
    return 1.0 / math.sqrt(1.0 - beta2)

def expected_g(variant: str, gamma: float) -> float:
    if variant == "leading":
        return 2.0
    elif variant in ("td_current", "gamma_S"):
        return 2.0 / gamma
    elif variant == "combined":
        return 2.0 / (gamma*gamma)
    else:
        raise ValueError("unknown variant")

def g_factor(q: float, m: float, r: float, omega: float, variant: str) -> Tuple[float, float, float]:
    gamma = gamma_from_r_omega(r, omega)
    if variant == "leading":
        mu_total = q * omega * r**2
        S = m * r**2 * omega
    elif variant == "td_current":
        mu_total = (q * omega * r**2) / gamma
        S = m * r**2 * omega
    elif variant == "gamma_S":
        mu_total = q * omega * r**2
        S = (gamma * m) * r**2 * omega
    elif variant == "combined":
        mu_total = (q * omega * r**2) / gamma
        S = (gamma * m) * r**2 * omega
    else:
        raise ValueError("unknown variant")
    g = 2.0 * m * mu_total / (q * S)
    beta = abs(r*omega)/C
    return g, gamma, beta

def clip_omega_to_beta_max(r: float, omega: float, beta_max: float) -> float:
    if beta_max <= 0.0:
        return 0.0
    vmax = beta_max * C
    max_omega = vmax / max(r, 1e-300)
    return min(omega, max_omega)

def sample_points(n: int, rmin: float, rmax: float, omin: float, omax: float,
                  beta_max: float, q: float, m: float, variant: str, seed=None):
    if seed is not None:
        random.seed(seed)
    rows = []
    for _ in range(n):
        r = 10.0 ** random.uniform(math.log10(rmin), math.log10(rmax))
        omega_raw = 10.0 ** random.uniform(math.log10(omin), math.log10(omax))
        omega = clip_omega_to_beta_max(r, omega_raw, beta_max)
        g, gamma, beta = g_factor(q, m, r, omega, variant)
        rows.append((r, omega, beta, gamma, g))
    return rows

def write_csv(path: str, rows, variant: str, units: str):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["variant", "units", "r_m", "omega_rad_s", "beta", "gamma", "g", "g_expected"])
        for r, omega, beta, gamma, g in rows:
            w.writerow([variant, units, f"{r:.9e}", f"{omega:.9e}", f"{beta:.9e}", f"{gamma:.12f}", f"{g:.12f}", f"{expected_g(variant, gamma):.12f}"])

def plot_g_vs_beta(path_png: str, rows, variant: str):
    # Lazy import matplotlib so script works headless when not plotting
    import matplotlib.pyplot as plt
    betas = [row[2] for row in rows]
    gs = [row[4] for row in rows]
    # Sort by beta for a clean curve
    pairs = sorted(zip(betas, gs), key=lambda x: x[0])
    betas_sorted = [b for b, _ in pairs]
    gs_sorted = [g for _, g in pairs]
    plt.figure()
    plt.scatter(betas_sorted, gs_sorted, s=12)  # single chart, no specific colors
    plt.xlabel("β = v/c")
    plt.ylabel("g")
    plt.title(f"g vs β — {variant}")
    plt.tight_layout()
    plt.savefig(path_png, dpi=160)
    plt.close()

def main():
    p = argparse.ArgumentParser(description="Möbius two-mode g-factor variants demo (with CSV/plot).")
    p.add_argument("--variant", choices=["leading","td_current","gamma_S","combined"], default="leading")
    p.add_argument("--trials", type=int, default=5, help="number of random test cases")
    p.add_argument("--rmin", type=float, default=1e-15)
    p.add_argument("--rmax", type=float, default=1e-9)
    p.add_argument("--omin", type=float, default=1e6)
    p.add_argument("--omax", type=float, default=1e22)
    p.add_argument("--beta-max", type=float, default=0.99)
    p.add_argument("--units", choices=["physical","arb"], default="physical")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--sweep", nargs=2, type=int, metavar=("NR","NOMEGA"))
    p.add_argument("--check", action="store_true")
    p.add_argument("--tol", type=float, default=1e-12)
    p.add_argument("--csv", type=str, default=None, help="write sampled rows to CSV at PATH")
    p.add_argument("--plot", type=str, default=None, help="save a PNG plot of g vs β at PATH")
    args = p.parse_args()

    if args.units == "physical":
        q = -1.602176634e-19   # C
        m =  9.1093837015e-31  # kg
        units_label = "electron"
    else:
        q = -1.0
        m =  1.0
        units_label = "arb"

    # Sample rows
    n = args.trials if not args.sweep else (args.sweep[0]*args.sweep[1])
    if args.sweep:
        # build grid deterministically (no RNG) for CSV/plot uniformity
        rows = []
        nr, nomega = args.sweep
        for ir in range(nr):
            r = 10.0 ** (math.log10(args.rmin) + (math.log10(args.rmax/args.rmin))*ir/max(1, nr-1))
            for iw in range(nomega):
                omega_raw = 10.0 ** (math.log10(args.omin) + (math.log10(args.omax/args.omin))*iw/max(1, nomega-1))
                omega = clip_omega_to_beta_max(r, omega_raw, args.beta_max)
                g, gamma, beta = g_factor(q, m, r, omega, args.variant)
                rows.append((r, omega, beta, gamma, g))
    else:
        rows = sample_points(args.trials, args.rmin, args.rmax, args.omin, args.omax,
                             args.beta_max, q, m, args.variant, seed=args.seed)

    # Print a few cases to stdout (like v1)
    print(f"Units: {units_label}")
    if args.sweep:
        print(f"Sweep: nr={args.sweep[0]}, nomega={args.sweep[1]}, variant={args.variant}, β_max={args.beta_max:.3f}")
    else:
        print(f"Variant: {args.variant}")
        print(f"Trials={args.trials}, r∈[{args.rmin:.3e}, {args.rmax:.3e}] m, ω∈[{args.omin:.3e}, {args.omax:.3e}] rad/s, β_max={args.beta_max:.3f}")

    # stdout preview (up to 10 rows)
    preview = rows[:min(10, len(rows))]
    for i, (r, omega, beta, gamma, g) in enumerate(preview, 1):
        print(f"Case {i:02d}: r={r:.3e} m, ω={omega:.3e} rad/s, β={beta:.6f}, γ={gamma:.6f} → g={g:.12f} (expected={expected_g(args.variant, gamma):.12f})")

    # CSV
    if args.csv:
        write_csv(args.csv, rows, args.variant, units_label)
        print(f"\nWrote CSV: {args.csv}")

    # Plot
    if args.plot:
        plot_g_vs_beta(args.plot, rows, args.variant)
        print(f"Saved plot: {args.plot}")

    # Optional check
    if args.check:
        for (r, omega, beta, gamma, g) in rows:
            exp = expected_g(args.variant, gamma)
            if abs(g - exp) > args.tol:
                raise SystemExit(f"CHECK FAILED: |g-exp|={abs(g-exp):.3e} > tol={args.tol:.1e} at β={beta:.6f}, γ={gamma:.6f}")
        print(f"\n--check passed: all |g - expected| ≤ {args.tol}")

if __name__ == "__main__":
    main()
