# visualize_lensing.py
# Single, clean visualizer for point-mass lensing using libgravity only.
# - Sweeps impact parameters b
# - Uses libgravity.ray_trace_point_analytic(...) for numeric θ
# - Compares with analytic θ_γ = (1+γ)*2GM/(c^2 b)
# - Saves θ(b) plot and relative error plot

import argparse, math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from libgravity import c, G, deflection_angle_point_mass, ray_trace_point_analytic

R_SUN = 6.9634e8
ARCSEC = (180.0/math.pi)*3600.0

def parse_length(s: str) -> float:
    return float(s[:-4])*R_SUN if s.endswith("Rsun") else float(s)

def parse_b_list(s: str):
    return [parse_length(tok.strip()) for tok in s.split(",")]

def main():
    ap = argparse.ArgumentParser(description="Point-mass lens visualizer")
    mass = ap.add_mutually_exclusive_group(required=True)
    mass.add_argument("--M-solar", action="store_true", help="Use solar mass")
    mass.add_argument("--M", type=float, help="Custom mass in kg")
    ap.add_argument("--L", type=str, default="20Rsun", help="Half-domain length for ray tracing (meters or 'Rsun')")
    ap.add_argument("--b", type=str, default="0.5Rsun,1Rsun,2Rsun,3Rsun,5Rsun",
                    help="Comma-separated impact parameters (meters or 'Rsun')")
    ap.add_argument("--gamma", type=float, default=1.0, help="PPN gamma (default 1.0)")
    ap.add_argument("--steps", type=int, default=20000, help="RK4 steps for numeric ray")
    ap.add_argument("--out", type=str, default="lens_point", help="Output basename for plots")
    args = ap.parse_args()

    M = 1.98847e30 if args.M_solar else float(args.M)
    L = parse_length(args.L)
    bs = parse_b_list(args.b)
    gamma = float(args.gamma)
    steps = int(args.steps)
    out = args.out

    # Colors (Matplotlib ≥3.7: use colormap.colors, not cmap[])
    cmap = mpl.colormaps["tab10"]
    colors = cmap.colors  # list of RGBA

    # Compute numeric/analytic θ over sweep
    numeric = []
    analytic = []
    for b in bs:
        # Numeric (analytic Fermat inside lib)
        theta_num = ray_trace_point_analytic(M, b, L, steps=steps, gamma=gamma)  # radians
        # Analytic PPN-γ
        theta_ana = (1.0 + gamma) * 2.0 * G * M / (c*c*b)  # radians

        numeric.append(theta_num*ARCSEC)
        analytic.append(theta_ana*ARCSEC)

    numeric = np.array(numeric); analytic = np.array(analytic)
    brsun = np.array(bs)/R_SUN
    rel_err = 100.0*np.abs(numeric-analytic)/np.maximum(analytic, 1e-30)

    # --- Plot θ(b) ---
    plt.figure(figsize=(7.0,5.2))
    plt.plot(brsun, analytic, color=colors[1], lw=2.0, label=f"Analytic θ (γ={gamma:g})")
    plt.plot(brsun, numeric, "o", color=colors[0], ms=5.0, label="Numeric θ (libgravity)")
    for xb, thn, tha in zip(brsun, numeric, analytic):
        plt.plot([xb, xb], [min(thn,tha), max(thn,tha)], color="0.75", lw=0.8, alpha=0.8)
    plt.xlabel("impact b / R$_\\odot$")
    plt.ylabel("deflection θ [arcsec]")
    plt.title("Point-mass lens: numeric vs analytic")
    plt.grid(alpha=0.2)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out}_theta_vs_b.png", dpi=140)

    # --- Plot relative error ---
    plt.figure(figsize=(7.0,5.0))
    plt.plot(brsun, rel_err, "s-", color=colors[2], lw=1.5, ms=5.0)
    plt.xlabel("impact b / R$_\\odot$")
    plt.ylabel("relative error [%]")
    plt.title("Numeric vs analytic deflection — relative error")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(f"{out}_error_vs_b.png", dpi=140)

    # --- Console table ---
    print("\nResults (point mass, PPN-γ={:g})".format(gamma))
    print("b/Rsun    θ_num[arcsec]   θ_ana[arcsec]   rel_err[%]")
    for xb, thn, tha, er in zip(brsun, numeric, analytic, rel_err):
        print(f"{xb:6.2f}    {thn:12.6f}    {tha:12.6f}    {er:9.4f}")

    print(f"\nSaved: {out}_theta_vs_b.png, {out}_error_vs_b.png")

if __name__ == "__main__":
    main()

