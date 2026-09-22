#!/usr/bin/env python3
"""
g_tetrahedron.py

Explore g ≈ 2 for a spinning tetrahedral electron model with small geometric corrections.

Key formulas (thin-shell, rank-2 isotropic case):
    g = 2 * <r^2>_q / <r^2>_m
    a_e = (g - 2) / 2 = <r^2>_q / <r^2>_m - 1

General tensor form (exact):
    ĝ = 2 * I_q * (I_m)^(-1)
where I_m and I_q are (mass- and charge-weighted) inertia tensors:
    I_* = ∫ w_*(r) [ r^2 I - r r^T ] d^3r,  with ∫ w_* d^3r = m (same normalization).

Small quadrupolar anisotropy:
    I_m = c_m (I + ε_m T),   I_q = c_q (I + ε_q T),  Tr(T)=0.
Directional measurement along unit axis L:
    g(L) = L^T ĝ L.

Optional chiral self-coupling shift:
    δg_chiral(θ) = 2 λ / (μ_B B) * cos θ

CLI:
  1) Isotropic thin-shell:
     python g_tetrahedron.py iso --Rm 1.0 --Rq 1.00058
  2) Anisotropy (exact ĝ), canonical T or custom JSON:
     python g_tetrahedron.py aniso --Rm 1.0 --Rq 1.00058 --eps-m 0.002 --eps-q 0.003 --T-axis z --axes x y z
     python g_tetrahedron.py aniso --Rm 1.0 --Rq 1.00058 --eps-m 0.002 --eps-q 0.003 --T-json my_T.json --axes 1,0,0 0,1,0 0,0,1
  3) Chiral shift:
     python g_tetrahedron.py chiral --lambda 1e-29 --B 1.0 --theta-deg 0
  4) Sweep δ = Rq/Rm − 1:
     python g_tetrahedron.py sweep --Rm 1.0 --delta-min -2e-3 --delta-max 2e-3 --N 81 --csv sweep.csv --plot-prefix sweep
"""

from __future__ import annotations
import argparse
import json
import sys
from textwrap import dedent

import numpy as np
import matplotlib.pyplot as plt

# Physical constant
MU_B = 9.2740100783e-24   # J/T (Bohr magneton, CODATA-ish)


# ---------- Core isotropic (thin-shell) model ----------

def g_iso(Rm: float, Rq: float) -> float:
    """Scalar g for thin spherical shells: <r^2>_m = Rm^2, <r^2>_q = Rq^2."""
    return 2.0 * (Rq**2) / (Rm**2)

def a_e_iso(Rm: float, Rq: float) -> float:
    """a_e = (g - 2)/2."""
    return 0.5 * (g_iso(Rm, Rq) - 2.0)


# ---------- Anisotropy (exact tensor ĝ = 2 I_q I_m^{-1}) ----------

def canonical_T(axis: str = "z") -> np.ndarray:
    """Symmetric traceless quadrupole tensor aligned to axis."""
    if axis == "z":
        return np.diag([-0.5, -0.5, 1.0])
    if axis == "x":
        return np.diag([1.0, -0.5, -0.5])
    if axis == "y":
        return np.diag([-0.5, 1.0, -0.5])
    raise ValueError("axis must be one of {'x','y','z'}")

def g_tensor_aniso(Rm: float, Rq: float, T: np.ndarray, eps_m: float, eps_q: float) -> np.ndarray:
    """
    Exact tensor expression:
      I_m = c_m (I + eps_m T),  I_q = c_q (I + eps_q T),  c_* ~ <r^2>_*.
      ĝ = 2 I_q I_m^{-1}
    """
    c_m = Rm**2
    c_q = Rq**2
    I = np.eye(3)
    Im = c_m * (I + eps_m * T)
    Iq = c_q * (I + eps_q * T)
    Im_inv = np.linalg.inv(Im)
    ghat = 2.0 * (Iq @ Im_inv)
    return ghat

def g_along(ghat: np.ndarray, Lhat: np.ndarray) -> float:
    """Scalar g measured along unit axis Lhat."""
    Lhat = np.array(Lhat, dtype=float)
    Lhat = Lhat / np.linalg.norm(Lhat)
    return float(Lhat.T @ ghat @ Lhat)


# ---------- Chiral self-coupling shift ----------

def delta_g_chiral(lam: float, B: float, theta_rad: float) -> float:
    """δg_chiral = 2 λ / (μ_B B) * cos θ."""
    return (2.0 * lam) / (MU_B * B) * np.cos(theta_rad)


# ---------- Utilities ----------

def save_json(obj, path: str) -> str:
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    return path

def save_csv(rows, header, path: str) -> str:
    with open(path, "w") as f:
        f.write(",".join(header) + "\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    return path

def parse_T_from_args(args) -> np.ndarray:
    if args.T_json:
        with open(args.T_json, "r") as f:
            data = json.load(f)
        T = np.array(data, dtype=float)
        if T.shape != (3, 3):
            raise ValueError("T_json must contain a 3x3 array")
        tr = float(np.trace(T))
        if abs(tr) > 1e-9:
            print(f"Warning: provided T has trace {tr:+.3e}; subtracting (tr/3)I to enforce traceless.")
            T = T - (tr / 3.0) * np.eye(3)
        return T
    return canonical_T(args.T_axis)


# ---------- Subcommand handlers ----------

def cmd_iso(args):
    g = g_iso(args.Rm, args.Rq)
    a = a_e_iso(args.Rm, args.Rq)
    print(f"g = {g:.12f}")
    print(f"a_e = (g-2)/2 = {a:.12e}")
    if args.out:
        save_json({"Rm": args.Rm, "Rq": args.Rq, "g": g, "a_e": a}, args.out)
        print(f"Saved: {args.out}")

def cmd_aniso(args):
    T = parse_T_from_args(args)
    ghat = g_tensor_aniso(args.Rm, args.Rq, T, args.eps_m, args.eps_q)
    print("g-tensor:")
    for row in ghat:
        print("  " + " ".join(f"{v: .9f}" for v in row))
    # axes to evaluate
    axes = []
    if args.axes:
        for ax in args.axes:
            if ax.lower() == 'x':
                axes.append([1, 0, 0])
            elif ax.lower() == 'y':
                axes.append([0, 1, 0])
            elif ax.lower() == 'z':
                axes.append([0, 0, 1])
            else:
                parts = ax.split(",")
                if len(parts) != 3:
                    raise ValueError(f"Axis spec '{ax}' not understood (use x y z or 'ax,ay,az').")
                axes.append([float(parts[0]), float(parts[1]), float(parts[2])])
    else:
        axes = [[1,0,0],[0,1,0],[0,0,1]]

    for a in axes:
        gv = g_along(ghat, a)
        print(f"g along {a} = {gv:.12f}")

    if args.out:
        save_json({"Rm": args.Rm, "Rq": args.Rq, "eps_m": args.eps_m, "eps_q": args.eps_q,
                   "T": T.tolist(), "g_tensor": ghat.tolist()}, args.out)
        print(f"Saved: {args.out}")

def cmd_chiral(args):
    th = np.deg2rad(args.theta_deg) if args.theta_deg is not None else args.theta_rad
    if th is None:
        print("Provide either --theta-deg or --theta-rad", file=sys.stderr)
        sys.exit(2)
    dg = delta_g_chiral(args.lam, args.B, th)
    print(f"delta_g_chiral = {dg:.12e}")
    if args.out:
        save_json({"lambda_J": args.lam, "B_T": args.B, "theta_rad": th, "delta_g": dg}, args.out)
        print(f"Saved: {args.out}")

def cmd_sweep(args):
    Rm = args.Rm
    deltas = np.linspace(args.delta_min, args.delta_max, args.N)
    rows, g_vals, a_vals = [], [], []
    for d in deltas:
        Rq = Rm * (1.0 + d)
        g = g_iso(Rm, Rq)
        a = a_e_iso(Rm, Rq)
        rows.append((d, Rq, g, a))
        g_vals.append(g)
        a_vals.append(a)

    if args.csv:
        save_csv(rows, header=["delta", "Rq", "g", "a_e"], path=args.csv)
        print(f"Saved CSV: {args.csv}")

    if args.plot_prefix:
        plt.figure()
        plt.plot(deltas, g_vals)
        plt.xlabel("delta = Rq/Rm - 1")
        plt.ylabel("g")
        plt.title("g vs radius mismatch (thin-shell)")
        plt.grid(True)
        plt.tight_layout()
        g_path = args.plot_prefix + "_g.png"
        plt.savefig(g_path)
        plt.close()
        print(f"Saved plot: {g_path}")

        plt.figure()
        plt.plot(deltas, a_vals)
        plt.xlabel("delta = Rq/Rm - 1")
        plt.ylabel("a_e = (g-2)/2")
        plt.title("a_e vs radius mismatch (thin-shell)")
        plt.grid(True)
        plt.tight_layout()
        a_path = args.plot_prefix + "_ae.png"
        plt.savefig(a_path)
        plt.close()
        print(f"Saved plot: {a_path}")


# ---------- CLI ----------

def build_parser():
    p = argparse.ArgumentParser(
        prog="g-tetra",
        description="Explore g ≈ 2 with small geometric corrections (spinning tetrahedral model)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent("""
        Examples:
          # 1) Isotropic thin-shell: ~electron-sized anomaly
          g-tetra iso --Rm 1.0 --Rq 1.00058

          # 2) Small quadrupole anisotropy, report g-tensor and g along axes
          g-tetra aniso --Rm 1.0 --Rq 1.00058 --eps-m 0.002 --eps-q 0.003 --T-axis z --axes x y z

          # 3) Chiral shift for given lambda, B, theta
          g-tetra chiral --lambda 1e-29 --B 1.0 --theta-deg 0

          # 4) Sweep delta in ±0.2% and save CSV + plots
          g-tetra sweep --Rm 1.0 --delta-min -2e-3 --delta-max 2e-3 --N 81 \
                        --csv sweep.csv --plot-prefix sweep
        """)
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_iso = sub.add_parser("iso", help="Isotropic thin-shell: g and a_e from Rm,Rq")
    p_iso.add_argument("--Rm", type=float, required=True)
    p_iso.add_argument("--Rq", type=float, required=True)
    p_iso.add_argument("--out", type=str, help="Save JSON with results")
    p_iso.set_defaults(func=cmd_iso)

    p_an = sub.add_parser("aniso", help="Anisotropic (quadrupole) model: ĝ = 2 I_q I_m^{-1}")
    p_an.add_argument("--Rm", type=float, required=True)
    p_an.add_argument("--Rq", type=float, required=True)
    p_an.add_argument("--eps-m", type=float, default=0.0)
    p_an.add_argument("--eps-q", type=float, default=0.0)
    grpT = p_an.add_mutually_exclusive_group(required=False)
    grpT.add_argument("--T-axis", type=str, choices=["x","y","z"], default="z",
                      help="Use canonical traceless T aligned to axis")
    grpT.add_argument("--T-json", type=str, help="Path to JSON file with 3x3 matrix T")
    p_an.add_argument("--axes", type=str, nargs="*", help="Axes to evaluate g along: x y z or 'ax,ay,az'")
    p_an.add_argument("--out", type=str, help="Save JSON with results")
    p_an.set_defaults(func=cmd_aniso)

    p_ch = sub.add_parser("chiral", help="Chiral self-coupling shift: delta_g = 2 λ/(μ_B B) cosθ")
    p_ch.add_argument("--lambda", dest="lam", type=float, required=True, help="λ in Joules")
    p_ch.add_argument("--B", type=float, required=True, help="Magnetic field (Tesla)")
    thg = p_ch.add_mutually_exclusive_group(required=True)
    thg.add_argument("--theta-deg", type=float, help="Angle in degrees")
    thg.add_argument("--theta-rad", type=float, help="Angle in radians")
    p_ch.add_argument("--out", type=str, help="Save JSON with results")
    p_ch.set_defaults(func=cmd_chiral)

    p_sw = sub.add_parser("sweep", help="Sweep delta = Rq/Rm - 1, save CSV and/or plots")
    p_sw.add_argument("--Rm", type=float, required=True)
    p_sw.add_argument("--delta-min", type=float, required=True)
    p_sw.add_argument("--delta-max", type=float, required=True)
    p_sw.add_argument("--N", type=int, default=101)
    p_sw.add_argument("--csv", type=str, help="Output CSV path")
    p_sw.add_argument("--plot-prefix", type=str, help="Prefix path for PNG plots (no extension)")
    p_sw.set_defaults(func=cmd_sweep)

    return p

def main(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())

