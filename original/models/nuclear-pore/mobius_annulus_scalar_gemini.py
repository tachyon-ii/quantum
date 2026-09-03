#!/usr/bin/env python3
"""
mobius_annulus_scalar.py
------------------------
Thin-shell scalar surrogate (polar annulus) with a Möbius seam.

We solve the scalar eigenproblem on an annulus r ∈ [R-h, R], θ ∈ [0, 2π):

   ( -Δ + V(r) ) ψ = λ ψ,

with:
  • anti-periodic (Möbius) seam: ψ(r, θ+2π) = -ψ(r, θ)
  • homogeneous Neumann in r (∂ψ/∂r = 0) at both inner/outer walls
  • an asymmetric two-well radial potential V(r) to split the two lowest modes
    into core-localized and surface-localized states.

Dependencies: numpy, scipy, matplotlib
Run:
  python mobius_annulus_scalar.py --nr 80 --nt 256 --R 1.0 --h 0.12 --k 4
"""

import argparse
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt

def build_polar_grid(R=1.0, h=0.12, nr=80, nt=256):
    r_min, r_max = R - h, R
    r = np.linspace(r_min, r_max, nr)
    theta = np.linspace(0.0, 2*np.pi, nt, endpoint=False)
    dr = r[1] - r[0]
    dth = theta[1] - theta[0]
    return r, theta, dr, dth

def assemble_operator(r, theta, dr, dth, V_func=None, seam_sign=-1.0):
    """Assemble sparse matrix A ≈ ( -Δ + V(r) ) with Möbius seam (anti-periodic in θ)."""
    nr, nt = len(r), len(theta)
    N = nr * nt
    def idx(ir, it): return ir*nt + it

    rows, cols, vals = [], [], []

    for ir in range(nr):
        ri = r[ir]
        for it in range(nt):
            p = idx(ir, it)

            Vloc = 0.0 if V_func is None else V_func(ri)
            diag = 0.0

            # --- radial second derivative with Neumann at both ends ---
            if ir > 0:
                w_im = (ri - dr/2.0) / (ri * dr*dr)
                rows.append(p); cols.append(idx(ir-1, it)); vals.append(-w_im)
                diag += w_im
            else:
                w_ip = (ri + dr/2.0) / (ri * dr*dr)
                rows.append(p); cols.append(idx(ir+1, it)); vals.append(-w_ip)
                diag += w_ip

            if ir < nr-1:
                w_ip = (ri + dr/2.0) / (ri * dr*dr)
                rows.append(p); cols.append(idx(ir+1, it)); vals.append(-w_ip)
                diag += w_ip
            else:
                w_im = (ri - dr/2.0) / (ri * dr*dr)
                rows.append(p); cols.append(idx(ir-1, it)); vals.append(-w_im)
                diag += w_im

            # --- angular second derivative with Möbius seam ---
            it_l = (it - 1 + nt) % nt
            s_l = seam_sign if it == 0 else 1.0
            rows.append(p); cols.append(idx(ir, it_l)); vals.append(- s_l / (ri*ri*dth*dth))

            it_r = (it + 1) % nt
            s_r = seam_sign if it == nt - 1 else 1.0
            rows.append(p); cols.append(idx(ir, it_r)); vals.append(- s_r / (ri*ri*dth*dth))
            diag += 2.0 / (ri*ri*dth*dth)

            rows.append(p); cols.append(p); vals.append(diag + Vloc)

    return sp.coo_matrix((vals, (rows, cols)), shape=(N, N)).tocsr()

def asymmetric_two_well_potential(r_grid, depth_out=24.0, depth_in=16.0, sig_out=0.015, sig_in=0.025):
    """Return V(r) function with asymmetric wells near inner and outer walls."""
    r_min, r_max = r_grid[0], r_grid[-1]
    rin  = r_min + 2.0 * sig_in
    rout = r_max - 2.0 * sig_out
    def V(r_val):
        return (-depth_in * np.exp(-0.5*((r_val - rin)/sig_in)**2)
                -depth_out* np.exp(-0.5*((r_val - rout)/sig_out)**2))
    return V

def classify_localization(evec, r, nt):
    """Compute inner vs outer localization fractions for an eigenvector."""
    nr = len(r); psi = evec.reshape(nr, nt)
    w = (psi*psi.conj()).real
    w_sum = w.sum()
    if w_sum <= 1e-12: return 0.5, 0.5
    i_mid = nr // 2
    inner = w[:i_mid, :].sum() / w_sum
    outer = w[i_mid:, :].sum() / w_sum
    return float(inner), float(outer)

def seam_check(evec, nt):
    """Return mean correlation across seam ψ(θ=0) ≈ -ψ(θ=2π)."""
    nr = evec.size // nt
    psi = evec.reshape(nr, nt)
    left = psi[:, 0]
    right= psi[:, -1]
    num = np.vdot(left, -right).real
    den = np.sqrt((np.vdot(left,left).real)*(np.vdot(right,right).real)) + 1e-18
    return float(num/den)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--R',  type=float, default=1.0)
    ap.add_argument('--h',  type=float, default=0.12)
    ap.add_argument('--nr', type=int,   default=80)
    ap.add_argument('--nt', type=int,   default=256)
    ap.add_argument('--k',  type=int,   default=4, help='number of eigenpairs')
    args = ap.parse_args()

    r, theta, dr, dth = build_polar_grid(R=args.R, h=args.h, nr=args.nr, nt=args.nt)
    
    # Use the new asymmetric potential
    V_func = asymmetric_two_well_potential(r)
    
    A = assemble_operator(r, theta, dr, dth, V_func=V_func, seam_sign=-1.0)

    k = min(args.k, A.shape[0]-2)
    vals, vecs = spla.eigsh(A, k=k, which='SM')
    idx = np.argsort(vals); vals, vecs = vals[idx], vecs[:, idx]
    print("Eigenvalues (smallest):", vals[:k])

    nt = args.nt
    for m in range(k):
        inner, outer = classify_localization(vecs[:, m], r, nt)
        corr = seam_check(vecs[:, m], nt)
        tag = "surface-like" if outer > inner else "core-like"
        print(f"Mode {m}: {tag:12s} | inner={inner:.3f}, outer={outer:.3f}, seam anti-phase={corr:.3f}")

    fig, axes = plt.subplots(1, 2, figsize=(10,4), constrained_layout=True)
    def to_image(evec):
        psi = evec.reshape(args.nr, args.nt)
        mag = np.abs(psi); mag /= mag.max()+1e-18
        return mag

    im0 = axes[0].imshow(to_image(vecs[:,0]), aspect='auto', cmap='magma',
                         extent=[0, 2*np.pi, r[0], r[-1]], origin='lower')
    axes[0].set_title("Mode 0 |ψ| (Lowest Energy)")
    axes[0].set_xlabel("θ"); axes[0].set_ylabel("r")
    plt.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    im1 = axes[1].imshow(to_image(vecs[:,1]), aspect='auto', cmap='magma',
                         extent=[0, 2*np.pi, r[0], r[-1]], origin='lower')
    axes[1].set_title("Mode 1 |ψ| (First Excited)")
    axes[1].set_xlabel("θ"); axes[1].set_ylabel("r")
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    
    plt.suptitle("Thin-shell scalar surrogate with Möbius seam\n(Asymmetric Potential)")
    plt.show()

if __name__ == "__main__":
    main()
