#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unified Nuclear Binding Model v3.6 - Simple Isosceles for A=3
==============================================================

Building on the nearly-working v3.4, this implements a SIMPLE isosceles
approach for A=3 nuclei:

Key changes from v3.4:
1. For A=3, allow slight edge length variations:
   - ³H: nn edge slightly shorter than pn edges (neutrons can get closer)
   - ³He: pp edge slightly longer than pn edges (Coulomb pushes protons apart)
   
2. Simple parameterization:
   - Use base edge length 'a' from optimization
   - Apply small deltas: a_nn = a * (1 - δ_nn), a_pp = a * (1 + δ_pp)
   - δ_nn and δ_pp are small (0.02-0.10 range)

This is a minimal change that should fix the ³He-³H split naturally.
"""

import argparse
import json
import math
from dataclasses import dataclass, field
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.optimize import brentq

# -----------------------------------------------------------------------------
# Constants & Targets
# -----------------------------------------------------------------------------

ALPHA_C = 1.439965  # MeV·fm
HBARC = 197.3269804  # MeV·fm
M_N = 938.918       # MeV/c^2
MU_N = M_N / 2.0

TARGETS = {
    "D": -2.224,
    "3H": -8.482,
    "3He": -7.718,
    "4He": -28.30,
}
SPLIT_EXP = 0.764  # ³He - ³H (MeV)

# -----------------------------------------------------------------------------
# Geometry helpers
# -----------------------------------------------------------------------------

@dataclass
class Geometry:
    A: int
    a: float
    Z: int = 0  # # of protons for A=3; ignored for A=2 and A=4

    def edges(self) -> List[Tuple[int, int, bool]]:
        """Return list of (i, j, is_pp)."""
        if self.A == 2:
            return [(0, 1, False)]
        elif self.A == 3:
            protons = set(range(self.Z))
            out = []
            for i in range(3):
                j = (i + 1) % 3
                is_pp = (i in protons) and (j in protons)
                out.append((i, j, is_pp))
            return out
        elif self.A == 4:
            protons = {0, 1}  # Z=2 default
            out = []
            for i in range(4):
                for j in range(i + 1, 4):
                    is_pp = (i in protons) and (j in protons)
                    out.append((i, j, is_pp))
            return out
        else:
            raise ValueError("Unsupported A")

    def face_altitudes(self) -> List[float]:
        """Return list of face altitudes for equilateral triangle / regular tetrahedron."""
        if self.A == 2:
            return []
        if self.A == 3:
            return [math.sqrt(3.0) / 2.0 * self.a]
        if self.A == 4:
            return [math.sqrt(2.0 / 3.0) * self.a for _ in range(4)]
        raise ValueError("Unsupported A")

def edges_per_nucleon(A: int) -> int:
    """X2=1, X3=2, X4=3 edges per nucleon (total edges = A*X/2)."""
    return {2:1, 3:2, 4:3}[A]

# -----------------------------------------------------------------------------
# Parameter container
# -----------------------------------------------------------------------------

@dataclass
class ModelParams:
    # Ranges
    lam: float = 1.38
    lam_r: float = 0.5
    # Soft Coulomb
    rc_pp: float = 1.10
    # A=3 geometry adjustments (NEW in v3.6)
    delta_nn: float = 0.03  # ³H: nn edge is a*(1-delta_nn)
    delta_pp: float = 0.05  # ³He: pp edge is a*(1+delta_pp)
    # Channel strengths g^2(S,T); repulsive core shared by default
    g2: Dict[Tuple[int, int], float] = field(default_factory=lambda: {
        (1, 0): 100.0,  # will be solved to anchor deuteron
        (0, 1): 75.0,
        (1, 1): 60.0,
        (0, 0): 45.0,
    })
    g2r_all: float = 90.0
    # Three-body
    W: float = 12.0
    Lam3: float = 1.40
    Wr: float = 2.5
    Lam3r: float = 0.70
    three_body_enable: bool = True
    # Phase matching
    phase_enable: bool = False
    k_phi: float = 2.0
    q_phi: int = 2
    # Tensor proxy
    tensor_enable: bool = True
    eta_T: float = 0.04
    # Kinetic (Gaussian modes)
    c2: float = 0.90
    c3: float = 0.87
    c4: float = 0.75
    kA2: float = 0.50
    kA3: float = 0.80
    kA4: float = 0.95

# -----------------------------------------------------------------------------
# Potentials & energies
# -----------------------------------------------------------------------------

def soft_coulomb(r: float, rc_pp: float) -> float:
    r = max(1e-12, float(r))
    return 1.0 / math.sqrt(r * r + rc_pp * rc_pp)

def pair_potential_central(r: float, S: int, T: int, is_pp: bool, P: ModelParams) -> float:
    r = max(1e-12, float(r))
    att = -P.g2.get((S, T), 0.0) * math.exp(-r / P.lam) / r
    rep = P.g2r_all * math.exp(-r / P.lam_r) / r
    if is_pp:
        coul = ALPHA_C * soft_coulomb(r, P.rc_pp)
    else:
        coul = 0.0
    return att + rep + coul

def tensor_factor(S: int, A: int, P: ModelParams) -> float:
    if not P.tensor_enable or S == 0:
        return 1.0
    C = 0.0 if A == 2 else (0.5 if A == 3 else 0.75)
    return 1.0 - P.eta_T * C

def channel_weights_for_edge(A: int, deg_i: int, deg_j: int, is_pp: bool) -> Dict[Tuple[int, int], float]:
    if is_pp:
        wt = {(0, 1): 0.5, (1, 1): 0.5}
    else:
        if A == 2:
            wt = {(1, 0): 1.0}
        elif A == 3:
            wt = {(1, 0): 0.42, (0, 1): 0.33, (1, 1): 0.15, (0, 0): 0.10}
        else:
            wt = {(1, 0): 0.40, (0, 1): 0.30, (1, 1): 0.20, (0, 0): 0.10}
        crowd = (deg_i - 1) + (deg_j - 1) if A > 2 else 0
        scale = 1.0 - 0.12 * crowd
        wt = {k: (v * (scale if k[0] == 1 else 1.0)) for k, v in wt.items()}
    s = sum(wt.values())
    return {k: v / s for k, v in wt.items()} if s > 0 else wt

# -----------------------------------------------------------------------------
# NEW: Isosceles energy for A=3
# -----------------------------------------------------------------------------

def energy_A3_isosceles(a_base: float, Z: int, P: ModelParams):
    """
    Calculate energy for A=3 with isosceles triangle.
    For ³H (Z=1): two np edges at a_base, one nn edge at a_base*(1-delta_nn)
    For ³He (Z=2): two np edges at a_base, one pp edge at a_base*(1+delta_pp)
    """
    # Determine edge lengths
    if Z == 1:  # ³H
        a_pn = a_base
        a_like = a_base * (1 - P.delta_nn)  # nn edge slightly shorter
        is_pp = False
    else:  # ³He
        a_pn = a_base
        a_like = a_base * (1 + P.delta_pp)  # pp edge slightly longer
        is_pp = True
    
    # Calculate pair energies
    E_pairs = 0.0
    deg = 2  # All vertices in triangle have degree 2
    
    # Two pn edges
    for _ in range(2):
        wt = channel_weights_for_edge(3, deg, deg, False)
        for (S, T), w in wt.items():
            tf = tensor_factor(S, 3, P)
            V = pair_potential_central(a_pn, S, T, False, P)
            if S == 1:
                V *= tf
            E_pairs += w * V
    
    # One like-like edge
    wt = channel_weights_for_edge(3, deg, deg, is_pp)
    for (S, T), w in wt.items():
        tf = tensor_factor(S, 3, P)
        V = pair_potential_central(a_like, S, T, is_pp, P)
        if S == 1:
            V *= tf
        E_pairs += w * V
    
    # Three-body face term using effective altitude
    # For nearly equilateral triangle, use approximate altitude
    h_eff = math.sqrt(3.0) / 2.0 * a_base  # Use base edge for simplicity
    E_3 = 0.0
    if P.three_body_enable and h_eff > 0:
        E_3 = -P.W * math.exp(-h_eff / P.Lam3) / h_eff
        if P.Wr > 0:
            E_3 += P.Wr * math.exp(-h_eff / P.Lam3r) / h_eff
    
    # Kinetic energy using effective size
    a_eff = (2*a_pn + a_like) / 3.0  # Average edge length
    cA, kA = P.c3, P.kA3
    bA = cA * a_eff
    E_kin = kA * (HBARC ** 2) / (M_N * bA * bA)
    
    Etot = E_pairs + E_3 + E_kin
    
    return Etot, {"pairs": E_pairs, "three_body": E_3, "kinetic": E_kin, "total": Etot}

# -----------------------------------------------------------------------------
# Standard energy functions (unchanged from v3.4)
# -----------------------------------------------------------------------------

def sum_pair_energy(geom: Geometry, P: ModelParams) -> float:
    A = geom.A
    a = geom.a
    deg = [0] * A
    for (i, j, _) in geom.edges():
        deg[i] += 1; deg[j] += 1
    total = 0.0
    for (i, j, is_pp) in geom.edges():
        wt = channel_weights_for_edge(A, deg[i], deg[j], is_pp)
        for (S, T), w in wt.items():
            tf = tensor_factor(S, A, P)
            V = pair_potential_central(a, S, T, is_pp, P)
            if S == 1:
                V *= tf
            total += w * V
    return total

def sum_three_body_energy(geom: Geometry, P: ModelParams) -> float:
    if not P.three_body_enable:
        return 0.0
    total = 0.0
    for h in geom.face_altitudes():
        total += (-P.W * math.exp(-h / P.Lam3) / h) + (P.Wr * math.exp(-h / P.Lam3r) / h if P.Wr > 0 else 0.0)
    return total

def kinetic_energy(geom: Geometry, P: ModelParams) -> float:
    if geom.A == 2:
        cA, kA = P.c2, P.kA2
    elif geom.A == 3:
        cA, kA = P.c3, P.kA3
    else:
        cA, kA = P.c4, P.kA4
    bA = cA * geom.a
    return kA * (HBARC ** 2) / (M_N * bA * bA)

def phase_mismatch_energy(geom: Geometry, P: ModelParams) -> float:
    return 0.0

def energy_total(geom: Geometry, P: ModelParams):
    # Use isosceles calculation for A=3
    if geom.A == 3:
        return energy_A3_isosceles(geom.a, geom.Z, P)
    
    # Standard calculation for A=2 and A=4
    E_pairs = sum_pair_energy(geom, P)
    E_3 = sum_three_body_energy(geom, P)
    E_kin = kinetic_energy(geom, P)
    E_phase = phase_mismatch_energy(geom, P)
    Etot = E_pairs + E_3 + E_kin + E_phase
    return Etot, {"pairs": E_pairs, "three_body": E_3, "kinetic": E_kin, "phase": E_phase, "total": Etot}

# -----------------------------------------------------------------------------
# Minimizers (unchanged)
# -----------------------------------------------------------------------------

def minimize_1d(f, lo=0.6, hi=3.0, n=801):
    xs = np.linspace(lo, hi, n)
    vals = np.array([f(x) for x in xs])
    j = int(vals.argmin())
    x_min = float(xs[j]); f_min = float(vals[j])
    # Simple quadratic refinement
    if 0 < j < len(xs) - 1:
        x1, x2, x3 = xs[j-1], xs[j], xs[j+1]
        f1, f2, f3 = vals[j-1], vals[j], vals[j+1]
        denom = (x1 - x2) * (x1 - x3) * (x2 - x3)
        if abs(denom) > 1e-12:
            A = (x3 * (f2 - f1) + x2 * (f1 - f3) + x1 * (f3 - f2)) / denom
            B = (x3*x3 * (f1 - f2) + x2*x2 * (f3 - f1) + x1*x1 * (f2 - f3)) / denom
            if A > 0:
                xv = -B / (2*A)
                if lo <= xv <= hi:
                    fv = f(float(xv))
                    if fv < f_min:
                        x_min, f_min = float(xv), float(fv)
    return x_min, f_min

# -----------------------------------------------------------------------------
# Deuteron anchoring (unchanged)
# -----------------------------------------------------------------------------

def solve_deuteron_g2(target_E: float, d_range: Tuple[float, float], P: ModelParams):
    def residual(g2_10: float) -> float:
        Ptmp = ModelParams(**{**P.__dict__})
        Ptmp.g2 = dict(P.g2)
        Ptmp.g2[(1, 0)] = g2_10
        d_opt, E_min = minimize_1d(lambda d: energy_total(Geometry(2, d), Ptmp)[0], lo=d_range[0], hi=d_range[1])
        return E_min - target_E
    try:
        root = brentq(residual, 50.0, 150.0, xtol=0.01, rtol=1e-6, maxiter=100)
        P.g2[(1, 0)] = float(root)
        d_opt, E_min = minimize_1d(lambda d: energy_total(Geometry(2, d), P)[0], lo=d_range[0], hi=d_range[1])
        return float(root), d_opt, E_min
    except Exception:
        d_opt, E_min = minimize_1d(lambda d: energy_total(Geometry(2, d), P)[0], lo=d_range[0], hi=d_range[1])
        return P.g2[(1, 0)], d_opt, E_min

# -----------------------------------------------------------------------------
# Scan mode
# -----------------------------------------------------------------------------

def solve_g2_g2r_closed_form(d: float, lam: float, lam_r: float):
    try:
        eL = math.exp(-d/lam) / d
        eR = math.exp(-d/lam_r) / d
        A = -((-math.exp(-d/lam)/lam)/d - math.exp(-d/lam)/d**2)
        B = (+(-math.exp(-d/lam_r)/lam_r)/d - math.exp(-d/lam_r)/d**2)
        C = -2 * (HBARC**2 / (2*MU_N)) / d**3
        RHS1 = -C
        RHS2 = TARGETS["D"] - (HBARC**2 / (2*MU_N)) / d**2
        det = A*eR - B*(-eL)
        if abs(det) < 1e-12:
            return None, None
        g2 = (RHS1*eR - B*RHS2) / det
        g2r = (A*RHS2 - RHS1*(-eL)) / det
        return g2, g2r
    except Exception:
        return None, None

def run_scan(lam_vals: np.ndarray, d_vals: np.ndarray, lam_r: float = 0.5, rc_pp: float = 1.10, 
             delta_nn: float = 0.03, delta_pp: float = 0.05) -> pd.DataFrame:
    rows = []
    for lam in lam_vals:
        for d in d_vals:
            g2, g2r = solve_g2_g2r_closed_form(d, lam, lam_r)
            if g2 is None or g2r is None or g2 <= 0 or g2r <= 0:
                continue
            P = ModelParams(lam=lam, lam_r=lam_r,
                            g2={(1,0): g2, (0,1): g2*0.75, (1,1): g2*0.60, (0,0): g2*0.45},
                            g2r_all=g2r, rc_pp=rc_pp, 
                            delta_nn=delta_nn, delta_pp=delta_pp,
                            three_body_enable=True, W=12.0, Lam3=lam, Wr=0.0, Lam3r=0.7,
                            tensor_enable=True, eta_T=0.0, phase_enable=False)
            a0, E0 = minimize_1d(lambda a: energy_total(Geometry(4, a), P)[0], lo=0.8, hi=2.5)
            h = math.sqrt(2.0/3.0) * a0
            face_factor = 4.0 * math.exp(-h / P.Lam3) / h
            W = (E0 - TARGETS["4He"]) / (-face_factor) if abs(face_factor) > 1e-12 else 0.0
            P.W = W
            a3H, E3H = minimize_1d(lambda a: energy_total(Geometry(3, a, Z=1), P)[0], lo=0.8, hi=2.5)
            a3He, E3He = minimize_1d(lambda a: energy_total(Geometry(3, a, Z=2), P)[0], lo=0.8, hi=2.5)
            rows.append({
                "lambda_fm": lam,
                "d*_fm": d,
                "rc_pp_fm": rc_pp,
                "delta_nn": delta_nn,
                "delta_pp": delta_pp,
                "g2_MeVfm": g2,
                "g2r_MeVfm": g2r,
                "He4_a*_fm": a0,
                "He4_E_MeV": TARGETS["4He"],
                "W_MeVfm": W,
                "a3H_fm": a3H, "E3H_MeV": E3H,
                "a3He_fm": a3He, "E3He_MeV": E3He,
                "He3_minus_H3_MeV": E3He - E3H,
            })
    return pd.DataFrame(rows)

# -----------------------------------------------------------------------------
# Optimize mode
# -----------------------------------------------------------------------------

def objective(theta: Dict[str, float], base: ModelParams):
    P = ModelParams(**{**base.__dict__})
    P.g2 = dict(P.g2)
    P.g2[(0,1)] = theta.get("g2_01", P.g2[(0,1)])
    P.g2[(1,1)] = theta.get("g2_11", P.g2[(1,1)])
    P.g2[(0,0)] = theta.get("g2_00", P.g2[(0,0)])
    P.W      = theta.get("W",      P.W)
    P.Lam3   = theta.get("Lam3",   P.Lam3)
    P.Wr     = theta.get("Wr",     P.Wr)
    P.c3     = theta.get("c3",     P.c3)
    P.rc_pp  = theta.get("rc_pp",  P.rc_pp)
    P.delta_nn = theta.get("delta_nn", P.delta_nn)
    P.delta_pp = theta.get("delta_pp", P.delta_pp)

    # Exact deuteron anchoring
    g2_10, d_star, E_d = solve_deuteron_g2(TARGETS["D"], (1.2, 1.9), P)

    # Ground-state minima
    a3H,  E_3H  = minimize_1d(lambda a: energy_total(Geometry(3, a, Z=1), P)[0], lo=0.8, hi=2.5)
    a3He, E_3He = minimize_1d(lambda a: energy_total(Geometry(3, a, Z=2), P)[0], lo=0.8, hi=2.5)
    a4,   E_4He = minimize_1d(lambda a: energy_total(Geometry(4, a),       P)[0], lo=0.8, hi=2.5)
    split = E_3He - E_3H

    # Weights
    w = {"D":0.01, "4He":10.0, "3H":1.0, "3He":1.0, "split":5.0}

    loss = (
        w["D"]*(E_d   - TARGETS["D"])**2
      + w["4He"]*(E_4He - TARGETS["4He"])**2
      + w["3H"]*(E_3H - TARGETS["3H"])**2
      + w["3He"]*(E_3He - TARGETS["3He"])**2
      + w["split"]*(split - SPLIT_EXP)**2
    )

    res = {
        "d_opt": d_star, "E_D": E_d,
        "a3H_opt": a3H, "E_3H": E_3H,
        "a3He_opt": a3He, "E_3He": E_3He,
        "a4_opt": a4, "E_4He": E_4He,
        "split": split,
        "g2_10": g2_10, "rc_pp": P.rc_pp, 
        "delta_nn": P.delta_nn, "delta_pp": P.delta_pp,
    }
    return loss, res, P

def optimize(base: ModelParams, max_iter: int = 150):
    theta = {
        "g2_01": base.g2[(0,1)],
        "g2_11": base.g2[(1,1)],
        "g2_00": base.g2[(0,0)],
        "W": base.W, "Lam3": base.Lam3, "Wr": base.Wr,
        "c3": base.c3,
        "rc_pp": base.rc_pp,
        "delta_nn": base.delta_nn,
        "delta_pp": base.delta_pp,
    }
    scales = {"g2_01":5.0, "g2_11":5.0, "g2_00":5.0, "W":1.0, "Lam3":0.03, "Wr":0.4,
              "c3":0.01, "rc_pp":0.04, "delta_nn":0.005, "delta_pp":0.005}
    bounds = {"g2_01":(40,100), "g2_11":(30,80), "g2_00":(20,60),
              "W":(8,18), "Lam3":(1.20,1.60), "Wr":(0.5,4.0),
              "c3":(0.82,0.92),
              "rc_pp":(1.0,1.6), 
              "delta_nn":(0.01,0.10), "delta_pp":(0.01,0.10)}
    
    best_loss, best_res, best_P = objective(theta, base)
    
    print(f"Initial: Loss={best_loss:.4f}, Split={best_res['split']:.3f} MeV")
    
    for iter_num in range(max_iter):
        improved = False
        for k in list(theta.keys()):
            for sign in (+1, -1):
                trial = dict(theta)
                lo, hi = bounds[k]
                trial[k] = float(np.clip(trial[k] + scales[k]*sign, lo, hi))
                loss, res, Ptrial = objective(trial, base)
                if loss < best_loss:
                    best_loss, best_res, best_P = loss, res, Ptrial
                    theta = trial
                    improved = True
        
        if not improved:
            print(f"Converged at iteration {iter_num}")
            break
        
        if (iter_num + 1) % 20 == 0:
            print(f"Iter {iter_num+1}: Loss={best_loss:.4f}, Split={best_res['split']:.3f}")
    
    print(f"Final: Loss={best_loss:.4f}, Split={best_res['split']:.3f} MeV")
    
    return best_P, best_res

# -----------------------------------------------------------------------------
# Visualization helpers (mostly unchanged)
# -----------------------------------------------------------------------------

def plot_scan_heatmaps(df: pd.DataFrame, best_row: pd.Series, out_png: str):
    lam_grid = np.linspace(df['lambda_fm'].min(), df['lambda_fm'].max(), 100)
    d_grid = np.linspace(df['d*_fm'].min(), df['d*_fm'].max(), 100)
    L, D = np.meshgrid(lam_grid, d_grid)
    quantities = {
        'W_MeVfm': 'W (MeV·fm)',
        'He4_a*_fm': 'He-4 Edge Length (fm)',
        'He3_minus_H3_MeV': '³He-³H Split (MeV)',
        'g2_MeVfm': 'g² Attractive (MeV·fm)',
        'g2r_MeVfm': 'g²ᵣ Repulsive (MeV·fm)'
    }
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('λ–d Parameter Space (v3.6)')
    for idx, (key, title) in enumerate(quantities.items()):
        ax = axes.flat[idx]
        Z = griddata((df['lambda_fm'], df['d*_fm']), df[key], (L, D), method='cubic')
        if np.isnan(Z).any():
            Z = griddata((df['lambda_fm'], df['d*_fm']), df[key], (L, D), method='linear')
        im = ax.contourf(L, D, Z, levels=20)
        ax.contour(L, D, Z, levels=10, colors='white', alpha=0.3, linewidths=0.5)
        ax.plot(best_row['lambda_fm'], best_row['d*_fm'], '*', markersize=12)
        ax.set_xlabel('λ (fm)'); ax.set_ylabel('d* (fm)'); ax.set_title(title)
        plt.colorbar(im, ax=ax)
        ax.grid(True, alpha=0.2)
    axes.flat[-1].axis('off')
    plt.tight_layout()
    plt.savefig(out_png, dpi=150, bbox_inches='tight')
    plt.close(fig)

def plot_complete(optP: ModelParams, res: Dict[str, float], out_png: str):
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # Plot 1: Energy curves
    ax1 = fig.add_subplot(gs[0, :2])
    a_range = np.linspace(0.8, 2.5, 200)
    curves = {}
    curves['D'] = [energy_total(Geometry(2, a), optP)[0] for a in a_range]
    curves['3H'] = [energy_total(Geometry(3, a, Z=1), optP)[0] for a in a_range]
    curves['3He'] = [energy_total(Geometry(3, a, Z=2), optP)[0] for a in a_range]
    curves['4He'] = [energy_total(Geometry(4, a), optP)[0] for a in a_range]
    for k, y in curves.items():
        ax1.plot(a_range, y, linewidth=2, label=k)
    ax1.axhline(y=0.0)
    ax1.set_xlabel('Edge length (fm)'); ax1.set_ylabel('Total Energy (MeV)')
    ax1.set_title('Binding Energy Curves')
    ax1.legend(); ax1.grid(True, alpha=0.3)

    # Plot 2: Exp vs Calc
    ax2 = fig.add_subplot(gs[0, 2])
    nuclei = ['D', '³H', '³He', '⁴He']
    exp_vals = [TARGETS["D"], TARGETS["3H"], TARGETS["3He"], TARGETS["4He"]]
    calc_vals = [res['E_D'], res['E_3H'], res['E_3He'], res['E_4He']]
    x = np.arange(len(nuclei))
    width = 0.35
    ax2.bar(x - width/2, exp_vals, width, label='Exp')
    ax2.bar(x + width/2, calc_vals, width, label='Calc')
    ax2.set_ylabel('Binding (MeV)'); ax2.set_title('Exp vs Calc'); ax2.set_xticks(x); ax2.set_xticklabels(nuclei)
    ax2.legend(); ax2.grid(True, axis='y', alpha=0.3)

    # Plot 3: A=3 Geometry info
    ax3 = fig.add_subplot(gs[1, 0])
    info_text = f"""A=3 Isosceles Parameters:
    
³H:  a_base = {res['a3H_opt']:.3f} fm
     nn edge = {res['a3H_opt'] * (1 - optP.delta_nn):.3f} fm
     δ_nn = {optP.delta_nn:.3f}
     
³He: a_base = {res['a3He_opt']:.3f} fm  
     pp edge = {res['a3He_opt'] * (1 + optP.delta_pp):.3f} fm
     δ_pp = {optP.delta_pp:.3f}
     
Split = {res['split']:.3f} MeV
(Exp = {SPLIT_EXP:.3f} MeV)
"""
    ax3.text(0.1, 0.5, info_text, transform=ax3.transAxes, 
            fontsize=10, verticalalignment='center', fontfamily='monospace')
    ax3.axis('off')
    ax3.set_title('Isosceles Geometry')

    # Plot 4: He-4 components
    ax4 = fig.add_subplot(gs[1, 1])
    a_he4 = np.linspace(0.8, 2.5, 100)
    pairs, three, kin, tot = [], [], [], []
    for a in a_he4:
        _, comp = energy_total(Geometry(4, a), optP)
        pairs.append(comp['pairs']); three.append(comp['three_body']); kin.append(comp['kinetic']); tot.append(comp['total'])
    ax4.plot(a_he4, pairs, linewidth=2, linestyle='--', label='Pairs')
    ax4.plot(a_he4, three, linewidth=2, linestyle=':', label='3-body')
    ax4.plot(a_he4, kin, linewidth=2, linestyle='-.', label='Kinetic')
    ax4.plot(a_he4, tot, linewidth=3, label='Total')
    ax4.axhline(y=TARGETS["4He"])
    ax4.set_xlabel('Edge length (fm)'); ax4.set_ylabel('Energy (MeV)'); ax4.set_title('⁴He Components')
    ax4.legend(); ax4.grid(True, alpha=0.3)

    # Plot 5: Split vs a
    ax5 = fig.add_subplot(gs[1, 2])
    a_scan = np.linspace(1.0, 2.0, 50)
    splits = []
    for a in a_scan:
        E3H = energy_total(Geometry(3, a, Z=1), optP)[0]
        E3He = energy_total(Geometry(3, a, Z=2), optP)[0]
        splits.append(E3He - E3H)
    ax5.plot(a_scan, splits, linewidth=2, label='³He-³H')
    ax5.axhline(y=SPLIT_EXP)
    ax5.set_xlabel('Base edge length (fm)'); ax5.set_ylabel('Split (MeV)')
    ax5.set_title('Coulomb Split (Isosceles)')
    ax5.legend(); ax5.grid(True, alpha=0.3)

    # Plot 6: Potentials
    ax6 = fig.add_subplot(gs[2, :])
    r_range = np.linspace(0.3, 3.0, 300)
    for (S, T) in [(1,0), (0,1), (1,1), (0,0)]:
        V = [pair_potential_central(r, S, T, False, optP) for r in r_range]
        ax6.plot(r_range, V, linewidth=2, label=f'({S},{T})')
    ax6.axhline(y=0.0); ax6.set_xlabel('r (fm)'); ax6.set_ylabel('V(r) (MeV)')
    ax6.set_title('Channel Potentials'); ax6.legend(); ax6.grid(True, alpha=0.3)

    fig.suptitle('Unified Nuclear Binding Model v3.6 - Simple Isosceles')
    plt.tight_layout()
    plt.savefig(out_png, dpi=150, bbox_inches='tight')
    plt.close(fig)

# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Unified Nuclear Binding Model v3.6")
    ap.add_argument("--mode", choices=["scan", "optimize"], default="scan")
    # Scan options
    ap.add_argument("--lam-min", type=float, default=1.30)
    ap.add_argument("--lam-max", type=float, default=1.38)
    ap.add_argument("--lam-steps", type=int, default=25)
    ap.add_argument("--d-min", type=float, default=1.2)
    ap.add_argument("--d-max", type=float, default=2.4)
    ap.add_argument("--d-steps", type=int, default=31)
    ap.add_argument("--rc-pp", type=float, default=1.10)
    ap.add_argument("--delta-nn", type=float, default=0.03)
    ap.add_argument("--delta-pp", type=float, default=0.05)
    # Optimize options
    ap.add_argument("--iters", type=int, default=100)
    args = ap.parse_args()

    if args.mode == "scan":
        print("="*60)
        print("SCAN MODE - Simple Isosceles A=3")
        print("="*60)
        lam_vals = np.linspace(args.lam_min, args.lam_max, args.lam_steps)
        d_vals = np.linspace(args.d_min, args.d_max, args.d_steps)
        print(f"Scanning λ ∈ [{args.lam_min}, {args.lam_max}] with {args.lam_steps} steps")
        print(f"Scanning d* ∈ [{args.d_min}, {args.d_max}] with {args.d_steps} steps")
        print(f"Using rc_pp = {args.rc_pp} fm")
        print(f"Using delta_nn = {args.delta_nn}, delta_pp = {args.delta_pp}\n")
        
        df = run_scan(lam_vals, d_vals, lam_r=0.5, rc_pp=args.rc_pp, 
                      delta_nn=args.delta_nn, delta_pp=args.delta_pp)
        df.to_csv("v3_scan.csv", index=False)
        
        # Score & pick top
        df['W_abs'] = df['W_MeVfm'].abs()
        df['He4_a_deviation'] = (df['He4_a*_fm'] - 1.4).abs()
        df['split_error'] = (df['He3_minus_H3_MeV'] - SPLIT_EXP).abs()
        
        def normcol(x):
            span = float(x.max() - x.min()) if len(x) else 0.0
            return (x - x.min()) / span if span > 0 else 0.0
        
        df['W_abs_norm'] = normcol(df['W_abs'])
        df['He4_a_deviation_norm'] = normcol(df['He4_a_deviation'])
        df['split_error_norm'] = normcol(df['split_error'])
        df['score'] = 0.4*df['W_abs_norm'] + 0.3*df['He4_a_deviation_norm'] + 0.3*df['split_error_norm']
        
        top = df.nsmallest(20, 'score')
        top.to_csv("v3_top_candidates.csv", index=False)
        plot_scan_heatmaps(df, top.iloc[0], "v3_heatmaps.png")
        
        print("\nScan complete.")
        print(f"Saved: v3_scan.csv, v3_top_candidates.csv, v3_heatmaps.png")
        print("\nBest candidate:")
        print(top.iloc[0][['lambda_fm','d*_fm','rc_pp_fm','delta_nn','delta_pp','W_MeVfm','He4_a*_fm','He3_minus_H3_MeV']])
        
    else:  # optimize mode
        print("="*60)
        print("OPTIMIZE MODE - Simple Isosceles A=3")
        print("="*60)
        base = ModelParams(rc_pp=args.rc_pp)
        optP, res = optimize(base, max_iter=args.iters)
        
        ok_D = abs(res['E_D'] - TARGETS["D"]) < 0.1
        ok_He4 = abs(res['E_4He'] - TARGETS["4He"]) < 0.1
        ok_3H = abs(res['E_3H'] - TARGETS["3H"]) / abs(TARGETS["3H"]) < 0.12
        ok_3He = abs(res['E_3He'] - TARGETS["3He"]) / abs(TARGETS["3He"]) < 0.12
        ok_split = 0.70 <= res['split'] <= 0.85

        results_df = pd.DataFrame({
            "Nucleus": ["D","³H","³He","⁴He"],
            "E_exp_MeV": [TARGETS["D"], TARGETS["3H"], TARGETS["3He"], TARGETS["4He"]],
            "E_calc_MeV": [res['E_D'], res['E_3H'], res['E_3He'], res['E_4He']],
            "a_opt_fm": [res['d_opt'], res['a3H_opt'], res['a3He_opt'], res['a4_opt']],
        })
        results_df.to_csv("v3_results.csv", index=False)
        
        with open("v3_params.json","w") as f:
            json.dump({
                "lambda": optP.lam, "lambda_r": optP.lam_r, "rc_pp": optP.rc_pp,
                "delta_nn": optP.delta_nn, "delta_pp": optP.delta_pp,
                "g2": {str(k): v for k,v in optP.g2.items()}, "g2r_all": optP.g2r_all,
                "W": optP.W, "Lam3": optP.Lam3, "Wr": optP.Wr, "Lam3r": optP.Lam3r,
                "c2": optP.c2, "c3": optP.c3, "c4": optP.c4,
            }, f, indent=2)
        
        plot_complete(optP, res, "v3_complete.png")
        
        print("\nOptimization complete.")
        print("Pass criteria:",
              {"D": ok_D, "He4": ok_He4, "3H": ok_3H, "3He": ok_3He, "split": ok_split})
        print("\nSaved: v3_results.csv, v3_params.json, v3_complete.png")
        print(f"\nBest parameters:")
        print(f"  rc_pp: {res['rc_pp']:.3f} fm")
        print(f"  delta_nn: {res['delta_nn']:.3f} (³H nn contraction)")
        print(f"  delta_pp: {res['delta_pp']:.3f} (³He pp expansion)")
        print(f"\nGeometry check:")
        print(f"  ³H:  nn edge = {res['a3H_opt'] * (1 - res['delta_nn']):.3f} fm < {res['a3H_opt']:.3f} fm (pn)")
        print(f"  ³He: pp edge = {res['a3He_opt'] * (1 + res['delta_pp']):.3f} fm > {res['a3He_opt']:.3f} fm (pn)")

if __name__ == "__main__":
    main()
