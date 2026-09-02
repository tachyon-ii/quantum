
#!/usr/bin/env python3
"""
g_mobius_heatmap.py
-------------------
Geometry + relativity g-factor explorer for the Möbius-loop toy model.

This script DOES NOT overwrite your existing g_equals_2_mobius.py.
It is a companion that reproduces the variant factors we used in
`g_equals_2_mobius_geometry.py` and adds a 2D heatmap over (epsilon, beta).

Definitions
- epsilon (ε) = a/R : strip half-width over loop radius (slenderness)
- geometry term: g_geo(ε) = 2 * (1 + k * ε^p)
  Note: choose k<0 for a *positive anomaly* (g>2) as in torsion-dominant picture.

- relativity factor F_rel(β, variant):
    * leading   : 1
    * gamma_S   : 1/γ = sqrt(1-β^2)

Total: g(ε,β) = g_geo(ε) * F_rel(β)

Outputs
- Heatmap PNG of (g - 2) over a grid of ε×β
- Optional CSV with the grid values

Usage examples
--------------
# Heatmap for gamma_S with positive anomaly (k=-0.35), ε∈[0,0.12], β∈[0,0.8]
python3 tests/g_mobius_heatmap.py \
  --variant gamma_S --k -0.35 --power 2 \
  --eps-min 0.0 --eps-max 0.12 --eps-steps 121 \
  --beta-min 0.0 --beta-max 0.80 --beta-steps 121 \
  --heatmap g_minus_2_heatmap.png --csv g_minus_2_grid.csv

# Leading (no relativistic suppression), same geometric params
python3 tests/g_mobius_heatmap.py --variant leading --k -0.35 --power 2 \
  --heatmap g_minus_2_leading.png
"""
import argparse, math, csv
from dataclasses import dataclass
from typing import List, Tuple

try:
    import numpy as np
    import matplotlib.pyplot as plt
except Exception:
    np = None
    plt = None

@dataclass
class Params:
    variant: str
    k: float
    power: int

def F_rel(beta: float, variant: str) -> float:
    if variant == "leading":
        return 1.0
    elif variant == "gamma_S":
        # simple suppression factor 1/gamma
        if beta >= 1.0:
            return 0.0
        return math.sqrt(1.0 - beta*beta)
    else:
        raise ValueError(f"Unknown variant: {variant}")

def g_total(eps: float, beta: float, P: Params) -> float:
    g_geo = 2.0 * (1.0 + P.k * (eps ** P.power))
    return g_geo * F_rel(beta, P.variant)

def main():
    ap = argparse.ArgumentParser(description="g-factor heatmap for Möbius loop (geometry + relativity).")
    ap.add_argument("--variant", choices=["leading","gamma_S"], default="leading")
    ap.add_argument("--k", type=float, default=-0.35, help="geometry coefficient (k<0 → positive anomaly)")
    ap.add_argument("--power", type=int, default=2, help="geometry power p (typically 2 or 4)")
    ap.add_argument("--eps-min", type=float, default=0.0)
    ap.add_argument("--eps-max", type=float, default=0.12)
    ap.add_argument("--eps-steps", type=int, default=121)
    ap.add_argument("--beta-min", type=float, default=0.0)
    ap.add_argument("--beta-max", type=float, default=0.80)
    ap.add_argument("--beta-steps", type=int, default=121)
    ap.add_argument("--heatmap", type=str, default="g_minus_2_heatmap.png")
    ap.add_argument("--csv", type=str, default=None)
    ap.add_argument("--no-show", action="store_true")
    args = ap.parse_args()

    P = Params(variant=args.variant, k=args.k, power=args.power)
    if np is None or plt is None:
        print("NumPy/Matplotlib not available. Install them to run this script.")
        return

    eps_grid = np.linspace(args.eps_min, args.eps_max, args.eps_steps)
    beta_grid = np.linspace(args.beta_min, args.beta_max, args.beta_steps)
    Z = np.zeros((args.beta_steps, args.eps_steps), dtype=float)  # store g-2

    for j, beta in enumerate(beta_grid):
        for i, eps in enumerate(eps_grid):
            Z[j, i] = g_total(eps, beta, P) - 2.0

    # optional CSV
    if args.csv:
        with open(args.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["eps", "beta", "g_minus_2"])
            for j, beta in enumerate(beta_grid):
                for i, eps in enumerate(eps_grid):
                    w.writerow([f"{eps:.6g}", f"{beta:.6g}", f"{Z[j,i]:.12g}"])
        print(f"Wrote CSV: {args.csv}")

    # Heatmap
    plt.figure()
    extent = [eps_grid.min(), eps_grid.max(), beta_grid.min(), beta_grid.max()]
    im = plt.imshow(Z, origin="lower", extent=extent, aspect="auto")
    cbar = plt.colorbar(im)
    cbar.set_label("g - 2")
    plt.xlabel("ε = a/R")
    plt.ylabel("β = v/c")
    plt.title(f"g-2 heatmap — variant={args.variant}, k={args.k}, p={args.power}")
    plt.tight_layout()
    if args.heatmap:
        plt.savefig(args.heatmap, dpi=160)
        print(f"Saved heatmap: {args.heatmap}")
    if not args.no_show:
        plt.show()
    else:
        plt.close()

if __name__ == "__main__":
    main()
