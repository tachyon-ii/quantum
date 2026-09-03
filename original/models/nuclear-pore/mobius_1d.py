#!/usr/bin/env python3
"""
mobius_1d.py
------------
1D loop eigenproblem illustrating periodic vs anti-periodic (Möbius) boundary.
We solve -ψ'' = λ ψ on [0,L] with either ψ(0)=ψ(L) (periodic) or ψ(0)=-ψ(L)
(anti-periodic). The spectra differ by a half-integer shift.

Run:
  python mobius_1d.py --L 1.0 --N 400         # periodic
  python mobius_1d.py --L 1.0 --N 400 --anti  # anti-periodic
"""

import argparse
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def assemble_1d(N, L, anti=False):
    """FD Laplacian on a ring with periodic or anti-periodic closure."""
    h = L/N
    main = 2*np.ones(N)/h**2
    off  = -1*np.ones(N-1)/h**2
    A = sp.diags([off, main, off], [-1,0,1], shape=(N,N)).tolil()
    # wrap: +1 for periodic, -1 for anti-periodic in the off-diagonals
    sgn = 1.0 if not anti else -1.0
    A[0, -1] = -sgn/h**2
    A[-1, 0] = -sgn/h**2
    return A.tocsr()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--L', type=float, default=1.0)
    ap.add_argument('--N', type=int, default=400)
    ap.add_argument('--anti', action='store_true', help='use anti-periodic (Möbius) closure')
    ap.add_argument('--k', type=int, default=6)
    args = ap.parse_args()

    A = assemble_1d(args.N, args.L, anti=args.anti)
    vals, _ = spla.eigsh(A, k=args.k, which='SM')
    vals = np.sort(vals)
    print(("Anti" if args.anti else "Periodic") + " eigenvalues (lowest):")
    print(vals)

    # Analytic comparison: periodic -> (2πn/L)^2 ; anti -> ((2n+1)π/L)^2
    n = np.arange(args.k, dtype=float)
    if args.anti:
        ana = (( (2*n+1)*np.pi/args.L )**2)
    else:
        ana = (( (2*n)*np.pi/args.L )**2)
    print("Analytic approx:", ana)

if __name__ == '__main__':
    main()

