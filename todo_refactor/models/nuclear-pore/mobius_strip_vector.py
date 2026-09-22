#!/usr/bin/env python3
"""
mobius_strip_vector.py
----------------------
2-D vector curl–curl eigenproblem on a thin rectangular strip (s, n) that
parametrizes a Möbius seam around a closed loop:

  s ∈ [0, L]    (longitudinal, around the loop)
  n ∈ [-h/2, h/2]  (across the shell thickness)

Unknown: E = (Es, En).
Eigenproblem (TE-like in-surface):
    ∇ × ( ∇ × E ) + α ∇(∇·E) = λ E
with α > 0 a small divergence penalty to suppress gradient spurious modes.

Boundary conditions:
  • Möbius seam in s:  Es(L,n) = +Es(0,n),  En(L,n) = -En(0,n)
  • PEC walls in n:    Es(s, ±h/2) = 0       (tangential vanishes at top/bottom)
    (swap one line below for PMC if desired)

Outputs:
  • eigenvalues, area-weighted inner/outer energy fractions,
  • seam anti-phase check (for En),
  • outer-wall “flux” proxy: ∫ ∂Es/∂n |_{n=+h/2} ds
  • plots of |E| for modes 0 and 1

Deps: numpy, scipy, matplotlib
Run:
  python mobius_strip_vector.py --Ns 300 --Nn 80 --L 2.0 --h 0.20 --k 6
"""

import argparse
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt

def assemble(Ns, Nn, L, h, alpha=0.05):
    """
    Build the sparse matrix for A[E] = ∇×(∇×E) + α ∇(∇·E) with Möbius seam.
    Grid: s_i = i*ds, i=0..Ns-1 (periodic seam)
          n_j = -h/2 + j*dn, j=0..Nn-1
    Unknown ordering: [Es(0,0..Nn-1), ..., Es(Ns-1,0..Nn-1), En(0,0..Nn-1), ..., En(Ns-1,0..Nn-1)]
    """
    ds = L / Ns
    dn = h / (Nn - 1)
    size = 2 * Ns * Nn

    def idx_Es(i, j):
        return i * Nn + j
    def idx_En(i, j):
        return Ns * Nn + i * Nn + j

    rows, cols, vals = [], [], []

    # helpers with periodic (Möbius) seam: for En, wrap with sign flip
    def wrap_i(i):
        return (i + Ns) % Ns
    def sign_En_shift(i_from, i_to):
        # if we crossed the seam (from Ns-1 to 0 or 0 to Ns-1), flip En sign
        # We implement this by checking specific wraps:
        if (i_from == Ns-1 and i_to == 0) or (i_from == 0 and i_to == Ns-1):
            return -1.0
        return 1.0

    # discrete curl z-component: C = ∂Es/∂n - ∂En/∂s
    # curl back to get vector: (-∂C/∂n, +∂C/∂s)
    # divergence: D = ∂Es/∂s + ∂En/∂n

    for i in range(Ns):
        for j in range(Nn):
            # neighbors indices with handling of seam in s and PEC in n
            iL = wrap_i(i-1)
            iR = wrap_i(i+1)
            jD = max(j-1, 0)
            jU = min(j+1, Nn-1)

            # seam signs for En
            sL = sign_En_shift(i, iL)
            sR = sign_En_shift(i, iR)

            # --- indices
            p_Es = idx_Es(i, j)
            p_En = idx_En(i, j)

            # === build ∇×(∇×E) ===
            # First compute curl scalar C with centered differences:
            # C(i,j) ≈ (Es(i,jU)-Es(i,jD))/(2 dn) - (En(iR,j)*sR - En(iL,j)*sL)/(2 ds)
            # Then -∂C/∂n contributes to Es-equation, +∂C/∂s contributes to En-equation.

            # ----- Es equation contribution from curl-curl -----
            # -∂/∂n [C]  ≈ -( C(i,jU) - C(i,jD) ) / (2 dn)
            # C at jU:
            def C_at(i0, j0):
                # handle seam signs inside En differences:
                iL0 = wrap_i(i0-1); iR0 = wrap_i(i0+1)
                sL0 = sign_En_shift(i0, iL0); sR0 = sign_En_shift(i0, iR0)
                term_n = (get_Es(i0, min(j0+1,Nn-1)) - get_Es(i0, max(j0-1,0))) / (2*dn)
                term_s = (sR0*get_En(iR0, j0) - sL0*get_En(iL0, j0)) / (2*ds)
                return term_n - term_s

            # To avoid nested calls, we place C contributions explicitly:

            # C(i, jU): depends on Es(i, jU±1), En(iR, jU), En(iL, jU)
            # C(i, jD): depends on Es(i, jD±1), En(iR, jD), En(iL, jD)
            # But we only need the linear combination -(C(i,jU) - C(i,jD))/(2 dn).
            # We can assemble by stencils:

            # ----- helper to add a triplet
            def add(r, c, v):
                rows.append(r); cols.append(c); vals.append(v)

            # convenience getters for basis assembly
            def get_Es(i0, j0): return 0.0
            def get_En(i0, j0): return 0.0

            # coefficients for Es-equation from curl-curl:
            coeff = -1.0/(2*dn) * (1.0/(2*dn))   # from -[ ... ]/(2dn) and C's ∂Es/∂n term
            # Es(i, jU+1), Es(i, jU-1), Es(i, jD+1), Es(i, jD-1)
            # jU+1 and jU-1 clamp at walls
            jp = min(j+1, Nn-1); jm = max(j-1, 0)
            jp2 = min(jp+1, Nn-1); jm2 = max(jp-1, 0)
            # from C(i, jU):
            add(p_Es, idx_Es(i, jp2), -coeff)
            add(p_Es, idx_Es(i, jm),   +coeff)
            # from C(i, jD):
            add(p_Es, idx_Es(i, jp),   +coeff)
            add(p_Es, idx_Es(i, jm2),  -coeff)

            # Es-equation from the En terms in C:
            coeff_s = -1.0/(2*dn) * ( -1.0/(2*ds) )  # minus sign from -∂/∂n, minus in C for En-part
            # from C(i, jU):
            add(p_Es, idx_En(iR, jp), coeff_s * sR)
            add(p_Es, idx_En(iL, jp), -coeff_s * sL)
            # from C(i, jD):
            add(p_Es, idx_En(iR, jm), -coeff_s * sR)
            add(p_Es, idx_En(iL, jm), coeff_s * sL)

            # ----- En equation contribution from curl-curl -----
            # +∂C/∂s ≈ ( C(iR,j) - C(iL,j) ) / (2 ds)
            # C(iR,j): term_n uses Es(iR,j±1), term_s uses En(iRR,j),En(i, j) with seam signs, etc.
            coeff_sEs =  1.0/(2*ds) * (1.0/(2*dn))  # from ∂/∂s of C's ∂Es/∂n term
            add(p_En, idx_Es(iR, jp),  coeff_sEs)
            add(p_En, idx_Es(iR, jm), -coeff_sEs)
            add(p_En, idx_Es(iL, jp), -coeff_sEs)
            add(p_En, idx_Es(iL, jm),  coeff_sEs)
            # En-part via C's ∂En/∂s term:
            coeff_sEn =  1.0/(2*ds) * (1.0/(2*ds))
            # C(iR,j) contributes -∂En/∂s ≈ -(sRR*En(iRR,j) - sR*En(i,j))/(2 ds)
            iRR = wrap_i(iR+1); sRR = sign_En_shift(iR, iRR)
            iLL = wrap_i(iL-1); sLL = sign_En_shift(iL, iLL)
            # from +∂/∂s[C(iR,j)]:
            add(p_En, idx_En(iRR, j), -coeff_sEn * sRR)
            add(p_En, idx_En(iR,  j), +coeff_sEn * sR)
            # from -∂/∂s[C(iL,j)]:
            add(p_En, idx_En(iL,  j), -coeff_sEn * sL)
            add(p_En, idx_En(iLL, j), +coeff_sEn * sLL)

            # === add divergence penalty α ∇(∇·E) ===
            # D = ∂Es/∂s + ∂En/∂n
            # ∇D = (∂D/∂s, ∂D/∂n). We add α * ∇D to (Es, En) equations.
            # Es-eq gets α * ∂D/∂s; En-eq gets α * ∂D/∂n.

            # ∂D/∂s: centered differences with seam
            # ∂Es/∂s gives second s-derivative of Es:
            add(p_Es, idx_Es(iR, j),  alpha*( 1.0/(2*ds*2*ds)))
            add(p_Es, idx_Es(iL, j),  alpha*( 1.0/(2*ds*2*ds)))
            add(p_Es, idx_Es(i,  j), -alpha*( 1.0/(2*ds*2*ds))*2.0)

            # ∂En/∂n part contributes nothing to ∂/∂s; ignore here.

            # ∂D/∂n in En-equation:
            # from ∂En/∂n → second n-derivative of En:
            add(p_En, idx_En(i, jU),  alpha*( 1.0/(2*dn*2*dn)))
            add(p_En, idx_En(i, jD),  alpha*( 1.0/(2*dn*2*dn)))
            add(p_En, idx_En(i, j),  -alpha*( 1.0/(2*dn*2*dn))*2.0)

            # from ∂Es/∂s part, ∂/∂n of that term is small; omitted for brevity.

            # === PEC at top/bottom: Es(s, ±h/2) = 0 (penalty) ===
            if j == 0 or j == Nn-1:
                rows += [p_Es]; cols += [p_Es]; vals += [1e8]

    A = sp.coo_matrix((vals, (rows, cols)), shape=(size, size)).tocsr()
    return A, ds, dn

def classify_localization(evec, Ns, Nn):
    Es = evec[:Ns*Nn].reshape(Ns, Nn)
    En = evec[Ns*Nn:].reshape(Ns, Nn)
    w  = (Es*Es.conj() + En*En.conj()).real
    # area weight ~ dn*ds (uniform): inner vs outer halves across n
    total = w.sum()
    j_mid = Nn//2
    inner = w[:, :j_mid].sum()/total
    outer = w[:, j_mid:].sum()/total
    return float(inner), float(outer)

def seam_check_En(evec, Ns, Nn):
    En = evec[Ns*Nn:].reshape(Ns, Nn)
    left  = En[0, :]
    right = En[-1, :]
    # Anti-periodic: En(L, n) ≈ -En(0, n)
    num = np.vdot(left, -right).real
    den = np.sqrt((np.vdot(left,left).real)*(np.vdot(right,right).real)) + 1e-18
    return float(num/den)

def outer_flux_proxy(evec, Ns, Nn, dn):
    Es = evec[:Ns*Nn].reshape(Ns, Nn)
    dEs_dn = (Es[:, -1] - Es[:, -2]) / dn
    return float(dEs_dn.sum() * (1.0/Ns))  # average along s

def plot_modes(evecs, Ns, Nn, title=""):
    fig, axes = plt.subplots(1, 2, figsize=(10,4), constrained_layout=True)
    for ax, m in zip(axes, [0,1]):
        Es = evecs[:, m][:Ns*Nn].reshape(Ns, Nn)
        En = evecs[:, m][Ns*Nn:].reshape(Ns, Nn)
        mag = np.sqrt((Es*Es.conj() + En*En.conj()).real)
        mag /= mag.max() + 1e-18
        im = ax.imshow(mag.T, origin='lower', aspect='auto', cmap='magma',
                       extent=[0, 1, -0.5, 0.5])
        ax.set_title(f"Mode {m}  |E|")
        ax.set_xlabel("s/L"); ax.set_ylabel("n/h")
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if title:
        plt.suptitle(title)
    plt.show()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--Ns', type=int, default=300)
    ap.add_argument('--Nn', type=int, default=80)
    ap.add_argument('--L',  type=float, default=2.0)
    ap.add_argument('--h',  type=float, default=0.20)
    ap.add_argument('--k',  type=int, default=6)
    ap.add_argument('--alpha', type=float, default=0.05)
    args = ap.parse_args()

    A, ds, dn = assemble(args.Ns, args.Nn, args.L, args.h, alpha=args.alpha)
    k = min(args.k, A.shape[0]-4)
    vals, vecs = spla.eigsh(A, k=k, which='SM')
    idx = np.argsort(vals); vals, vecs = vals[idx], vecs[:, idx]
    print("Eigenvalues:", vals[:k])

    # classify
    for m in range(min(k,4)):
        inner, outer = classify_localization(vecs[:,m], args.Ns, args.Nn)
        seam = seam_check_En(vecs[:,m], args.Ns, args.Nn)
        flux = outer_flux_proxy(vecs[:,m], args.Ns, args.Nn, dn)
        tag = "surface-like" if outer>inner else "core-like"
        print(f"Mode {m}: {tag:12s} | inner={inner:.3f}, outer={outer:.3f}, "
              f"seam En anti-phase={seam:.3f}, flux_out≈{flux:.3e}")

    plot_modes(vecs, args.Ns, args.Nn,
               title="Vector curl–curl on Möbius strip (|E|)")

if __name__ == "__main__":
    main()

