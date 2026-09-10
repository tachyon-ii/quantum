#!/usr/bin/env python3
"""
mobius_annulus_scalar.py  (updated)
-----------------------------------
Thin-shell scalar surrogate (polar annulus) with a Möbius seam and flexible
radial boundary conditions. Confirms:
  • Anti-periodic seam (π) on a closed shell,
  • Clear core/surface split (with BC or asymmetric wells),
  • Area-weighted localization (inner vs outer),
  • A simple “outer flux” proxy to mimic external-field coupling.

PDE (scalar surrogate):  ( -Δ + V(r) ) ψ = λ ψ  on r∈[R-h, R], θ∈[0,2π),
BCs:
  • Möbius seam: ψ(r, θ+2π) = -ψ(r, θ)
  • Radial BCs:  inner/outer = Neumann (default) or Dirichlet (penalized)

Run (strong surface split):
  python mobius_annulus_scalar.py --nr 96 --nt 256 --R 1.0 --h 0.12 --k 4 \
      --inner-bc dirichlet --outer-bc neumann --no-V
Or (asymmetric wells only):
  python mobius_annulus_scalar.py --inner-bc neumann --outer-bc neumann \
      --depth-out 24 --depth-in 16 --sig-out 0.015 --sig-in 0.025
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

def make_potential(r, r_min, r_max, use_V=True,
                   depth_out=20.0, depth_in=20.0, sig_out=0.02, sig_in=0.02):
    if not use_V:
        def V(_): return 0.0
        return V
    rin  = r_min + 2.0*sig_in
    rout = r_max - 2.0*sig_out
    def V(r_):
        return (-depth_in  * np.exp(-0.5*((r_ - rin )/sig_in )**2)
                -depth_out * np.exp(-0.5*((r_ - rout)/sig_out)**2))
    return V

def assemble_operator(r, theta, dr, dth, V, seam_sign=-1.0,
                      inner_bc="neumann", outer_bc="neumann",
                      bc_penalty=1e8):
    """
    Assemble A ≈ ( -Δ + V ) with Möbius seam and chosen radial BCs.
    Radial BCs: 'neumann' (mirror) or 'dirichlet' (penalty on boundary nodes).
    """
    nr, nt = len(r), len(theta)
    N = nr * nt
    def idx(ir, it): return ir*nt + it

    rows, cols, vals = [], [], []

    for ir in range(nr):
        ri = r[ir]
        for it in range(nt):
            p = idx(ir, it)
            diag = 0.0
            Vloc = V(ri)

            # --- radial second derivative (polar Laplacian) ---
            # inward neighbor (ir-1)
            if ir > 0:
                w_im = (ri - dr/2.0) / (ri * dr*dr)
                rows += [p]; cols += [idx(ir-1, it)]; vals += [-w_im]
                diag += w_im
            else:
                # inner wall
                if inner_bc.lower().startswith('d'):  # Dirichlet (penalty)
                    diag += bc_penalty
                else:  # Neumann (mirror): weak consistent penalty to keep SPD
                    diag += 1.0 / (ri * dr) * (1.0 / dr)

            # outward neighbor (ir+1)
            if ir < nr-1:
                w_ip = (ri + dr/2.0) / (ri * dr*dr)
                rows += [p]; cols += [idx(ir+1, it)]; vals += [-w_ip]
                diag += w_ip
            else:
                # outer wall
                if outer_bc.lower().startswith('d'):
                    diag += bc_penalty
                else:
                    diag += 1.0 / (ri * dr) * (1.0 / dr)

            # --- angular second derivative with Möbius seam ---
            it_l = it-1 if it-1 >= 0 else nt-1
            s_l = 1.0 if it-1 >= 0 else seam_sign
            rows += [p]; cols += [idx(ir, it_l)]; vals += [- s_l / (ri*ri*dth*dth)]
            it_r = it+1 if it+1 < nt else 0
            s_r = 1.0 if it+1 < nt else seam_sign
            rows += [p]; cols += [idx(ir, it_r)]; vals += [- s_r / (ri*ri*dth*dth)]
            diag += 2.0 / (ri*ri*dth*dth)

            rows += [p]; cols += [p]; vals += [diag + Vloc]

    A = sp.coo_matrix((vals, (rows, cols)), shape=(N, N)).tocsr()
    return A

def area_weighted_localization(evec, r, nt):
    """Compute inner vs outer area-weighted energy fractions."""
    nr = len(r)
    psi = evec.reshape(nr, nt)
    w = (psi*psi.conj()).real
    # area weight r dr dθ  ~  r
    rw = (w * r[:,None])
    total = rw.sum()
    if total <= 0: return 0.5, 0.5
    i_mid = np.argmin(np.abs(r - 0.5*(r[0]+r[-1])))
    inner = rw[:i_mid,:].sum() / total
    outer = rw[i_mid:,:].sum() / total
    return float(inner), float(outer)

def seam_correlation(evec, nt):
    """Mean correlation ψ(θ=0) ≈ -ψ(θ=2π). 1.0 = perfect anti-phase."""
    nr = evec.size // nt
    psi = evec.reshape(nr, nt)
    left = psi[:, 0]; right = psi[:, -1]
    num = np.vdot(left, -right).real
    den = np.sqrt((np.vdot(left,left).real)*(np.vdot(right,right).real)) + 1e-18
    return float(num/den)

def outer_flux_proxy(evec, r, dr, nt):
    """
    Surrogate 'external flux': integral of ∂ψ/∂r at the outer wall.
    For Dirichlet inner / Neumann outer this grows in the surface-like mode.
    """
    nr = len(r)
    psi = evec.reshape(nr, nt)
    # one-sided radial derivative at outer boundary
    dpsi_dr = (psi[-1,:] - psi[-2,:]) / dr
    # integrate with area weight r dθ (use r_out)
    r_out = r[-1]
    return float(r_out * dpsi_dr.sum() * (2*np.pi/nt))

def to_img(evec, r, nt):
    nr = len(r)
    psi = evec.reshape(nr, nt)
    mag = np.abs(psi); mag /= mag.max() + 1e-18
    return mag

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--R',  type=float, default=1.0)
    ap.add_argument('--h',  type=float, default=0.12)
    ap.add_argument('--nr', type=int,   default=96)
    ap.add_argument('--nt', type=int,   default=256)
    ap.add_argument('--k',  type=int,   default=4, help='number of eigenpairs')
    ap.add_argument('--inner-bc', default='neumann', choices=['neumann','dirichlet'])
    ap.add_argument('--outer-bc', default='neumann', choices=['neumann','dirichlet'])
    ap.add_argument('--no-V', action='store_true', help='disable radial wells')
    # asymmetric well params (used unless --no-V)
    ap.add_argument('--depth-out', type=float, default=20.0)
    ap.add_argument('--depth-in',  type=float, default=20.0)
    ap.add_argument('--sig-out',   type=float, default=0.02)
    ap.add_argument('--sig-in',    type=float, default=0.02)
    args = ap.parse_args()

    r, theta, dr, dth = build_polar_grid(R=args.R, h=args.h, nr=args.nr, nt=args.nt)
    V = make_potential(r, r_min=r[0], r_max=r[-1], use_V=not args.no_V,
                       depth_out=args.depth_out, depth_in=args.depth_in,
                       sig_out=args.sig_out,   sig_in=args.sig_in)

    A = assemble_operator(r, theta, dr, dth, V=V, seam_sign=-1.0,
                          inner_bc=args.inner_bc, outer_bc=args.outer_bc)

    k = min(args.k, A.shape[0]-2)
    vals, vecs = spla.eigsh(A, k=k, which='SM')
    idx = np.argsort(vals); vals, vecs = vals[idx], vecs[:, idx]
    print("Eigenvalues (smallest):", vals[:k])

    # Classify & report
    for m in range(min(k, 4)):
        inner, outer = area_weighted_localization(vecs[:, m], r, args.nt)
        corr = seam_correlation(vecs[:, m], args.nt)
        flux = outer_flux_proxy(vecs[:, m], r, dr, args.nt)
        tag = "surface-like" if outer>inner else "core-like"
        print(f"Mode {m}: {tag:12s} | inner={inner:.3f}, outer={outer:.3f}, "
              f"seam anti-phase={corr:.3f}, flux_out≈{flux:.3e}")

    # Plot first two modes
    fig, axes = plt.subplots(1, 2, figsize=(10,4), constrained_layout=True)
    for ax, m in zip(axes, [0,1]):
        mag = to_img(vecs[:,m], r, args.nt)
        im = ax.imshow(mag, aspect='auto', cmap='magma',
                       extent=[0, 2*np.pi, r[0], r[-1]], origin='lower')
        ax.set_title(f"Mode {m} |ψ|")
        ax.set_xlabel("θ"); ax.set_ylabel("r")
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.suptitle("Thin-shell scalar surrogate with Möbius seam\n(r vertical, θ horizontal)")
    plt.show()

if __name__ == "__main__":
    main()

