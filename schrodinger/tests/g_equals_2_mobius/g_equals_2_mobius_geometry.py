
#!/usr/bin/env python3
"""
g_equals_2_mobius_geometry.py
--------------------------------
Geometry-first companion to `g_equals_2_mobius.py`.

Purpose
- Isolate the *geometric* correction to g arising from finite strip width on a
  Möbius loop with anti-periodic (spinor) boundary conditions.
- Provide a clean baseline where g -> 2 as ε = a/R -> 0, with a small, tunable
  correction δg ∝ ε^p (p even by symmetry; default p=2).

Model
- ε = a/R  (strip half-width over centerline radius), 0 ≤ ε << 1
- g_geo(ε) = 2 * (1 - k * ε^p),  with k > 0, p ∈ {2,4} by default.
  This captures the leading reduction of effective area / path coupling.
- Optional relativistic factor from the prior demo, controlled by `--variant`:
    leading     : F_rel(γ)=1
    td_current  : F_rel(γ)=1/γ
    gamma_S     : F_rel(γ)=1/γ
    combined    : F_rel(γ)=1/γ^2
  with γ = 1/sqrt(1-β^2) and β supplied directly (no r·ω here).

Outputs
- CSV of (ε, β, γ, g_total, g_geo, F_rel)
- Plot of g vs ε for one or more β curves

License: MIT
"""
import math, argparse, csv
from typing import List

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

def gamma_from_beta(beta: float) -> float:
    if beta >= 1.0:
        return math.inf
    if beta <= 0.0:
        return 1.0
    return 1.0 / math.sqrt(1.0 - beta*beta)

def F_rel(variant: str, gamma: float) -> float:
    if variant == "leading":
        return 1.0
    elif variant in ("td_current","gamma_S"):
        return 1.0/max(gamma,1e-15)
    elif variant == "combined":
        return 1.0/max(gamma*gamma,1e-15)
    else:
        raise ValueError("unknown variant")

def g_geo(eps: float, k: float, power: int) -> float:
    return 2.0 * (1.0 - k * (eps ** power))

def sweep(eps_vals: List[float], betas: List[float], k: float, power: int, variant: str):
    rows = []
    for eps in eps_vals:
        for beta in betas:
            gamma = gamma_from_beta(beta)
            g_total = g_geo(eps, k, power) * F_rel(variant, gamma)
            rows.append((eps, beta, gamma, g_total, g_geo(eps,k,power), F_rel(variant,gamma)))
    return rows

def write_csv(path: str, rows, variant: str, k: float, power: int):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["variant","k","power","eps","beta","gamma","g_total","g_geo","F_rel"])
        for r in rows:
            eps, beta, gamma, g_total, g_g, f_rel = r
            w.writerow([variant, f"{k:.6f}", power, f"{eps:.6f}", f"{beta:.6f}", f"{gamma:.12f}", f"{g_total:.12f}", f"{g_g:.12f}", f"{f_rel:.12f}"])

def plot_g_vs_eps(path_png: str, rows, betas: List[float], title: str):
    if plt is None:
        print("matplotlib not available; skipping plot")
        return
    # rows contain mixed betas; split
    by_beta = {beta: [] for beta in betas}
    for eps, beta, gamma, g_total, g_g, f_rel in rows:
        by_beta[beta].append((eps, g_total))
    import numpy as np
    plt.figure()
    for beta in betas:
        data = sorted(by_beta[beta], key=lambda t: t[0])
        if not data:
            continue
        xs = [x for x,_ in data]
        ys = [y for _,y in data]
        plt.plot(xs, ys, label=f"β={beta:.2f}")
    plt.xlabel("ε = a/R")
    plt.ylabel("g(ε)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path_png, dpi=160)
    plt.close()

def parse_betas(s: str) -> List[float]:
    vals = []
    for tok in s.split(","):
        tok = tok.strip()
        if not tok:
            continue
        vals.append(float(tok))
    return vals

def main():
    ap = argparse.ArgumentParser(description="Geometry-only g-factor sweep for Möbius loop (ε = a/R).")
    ap.add_argument("--variant", choices=["leading","td_current","gamma_S","combined"], default="leading")
    ap.add_argument("--k", type=float, default=0.5, help="geometric correction coefficient (dimensionless)")
    ap.add_argument("--power", type=int, default=2, help="even power for ε (e.g., 2 or 4)")
    ap.add_argument("--emin", type=float, default=0.0, help="min ε (a/R)")
    ap.add_argument("--emax", type=float, default=0.3, help="max ε (a/R)")
    ap.add_argument("--neps", type=int, default=61, help="number of ε points")
    ap.add_argument("--betas", type=str, default="0.00,0.20,0.40,0.60", help="comma-separated β values")
    ap.add_argument("--csv", type=str, default=None, help="write CSV to PATH")
    ap.add_argument("--plot", type=str, default=None, help="save plot PNG to PATH")
    args = ap.parse_args()

    if args.power % 2 != 0 or args.power <= 0:
        raise SystemExit("--power must be a positive even integer (e.g. 2, 4).")

    betas = parse_betas(args.betas)
    eps_vals = [args.emin + (args.emax-args.emin)*i/max(1,args.neps-1) for i in range(args.neps)]
    rows = sweep(eps_vals, betas, args.k, args.power, args.variant)

    # Print a few rows
    print(f"Variant={args.variant}, k={args.k}, power={args.power}, ε∈[{args.emin},{args.emax}], betas={betas}")
    for (eps, beta, gamma, g_total, g_g, f_rel) in rows[:min(8,len(rows))]:
        print(f"eps={eps:.3f}, β={beta:.2f}, γ={gamma:.6f} → g_total={g_total:.12f}  (g_geo={g_g:.12f}, F_rel={f_rel:.12f})")

    if args.csv:
        write_csv(args.csv, rows, args.variant, args.k, args.power)
        print(f"Wrote CSV: {args.csv}")

    if args.plot:
        plot_g_vs_eps(args.plot, rows, betas, f"g vs ε — {args.variant}, k={args.k}, p={args.power}")

if __name__ == "__main__":
    main()
