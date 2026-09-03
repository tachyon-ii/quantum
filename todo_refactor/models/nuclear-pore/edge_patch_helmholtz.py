#!/usr/bin/env python3
"""
edge_patch_helmholtz.py
-----------------------
2D finite-difference Helmholtz/Laplacian eigenproblem on a periodic cell with a
single hexagonal pore (Dirichlet on pore boundary). Lowest eigenmodes localize
on the pore edge -> "rails on edges".

Solve:  -Δψ = λ ψ  on Ω \\ H,   ψ=0 on H,   periodic BC on ∂Ω.
We use a 5-point stencil and assemble a sparse matrix with periodic wraps.

Dependencies: numpy, scipy, matplotlib
Run: python edge_patch_helmholtz.py --nx 160 --ny 160 --k 6
"""

import argparse
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt

def hex_mask(nx, ny, cx, cy, radius):
    """
    Return a boolean mask of a regular hexagon centered at (cx,cy) in index coords,
    with circumradius 'radius' (in grid steps). Uses distance to 6 half-planes.
    """
    y, x = np.indices((ny, nx))
    # shift to center
    X = (x - cx)
    Y = (y - cy)
    # rotate coordinate by 0,60,120 deg and take |proj| <= radius
    mask = np.ones((ny, nx), dtype=bool)
    angles = np.deg2rad([0, 60, 120])
    for a in angles:
        ca, sa = np.cos(a), np.sin(a)
        u =  ca*X + sa*Y
        v = -sa*X + ca*Y
        # hex inequality: |u| + |v|/np.sqrt(3) <= radius  (approx regular hex)
        mask &= (np.abs(u) + np.abs(v)/np.sqrt(3.0) <= radius + 1e-9)
    return mask

def assemble_laplacian_periodic(nx, ny, pore_mask, h=1.0):
    """
    Build sparse -Δ with periodic wraps on the rectangle, Dirichlet (remove)
    on pore cells. Return matrix A and a map from (i,j) -> DOF index.
    """
    N = nx*ny
    # DOF map: -1 for pore cells (Dirichlet), else assigned sequential ID
    dof = -np.ones((ny, nx), dtype=int)
    count = 0
    for j in range(ny):
        for i in range(nx):
            if pore_mask[j, i]:
                dof[j, i] = -1
            else:
                dof[j, i] = count
                count += 1

    rows, cols, vals = [], [], []
    def add(i, j, ii, jj, val):
        rows.append(dof[j, i]); cols.append(dof[jj, ii]); vals.append(val)

    for j in range(ny):
        for i in range(nx):
            p = dof[j, i]
            if p < 0:  # pore
                continue
            # 5-point stencil with periodic wraps
            # center
            rows.append(p); cols.append(p); vals.append(4.0 / h**2)
            # neighbors (wrap)
            inb = (i+1) % nx; jnb = j
            if dof[jnb, inb] >= 0:
                add(i, j, inb, jnb, -1.0 / h**2)
            # left
            inb = (i-1) % nx; jnb = j
            if dof[jnb, inb] >= 0:
                add(i, j, inb, jnb, -1.0 / h**2)
            # up
            inb = i; jnb = (j+1) % ny
            if dof[jnb, inb] >= 0:
                add(i, j, inb, jnb, -1.0 / h**2)
            # down
            inb = i; jnb = (j-1) % ny
            if dof[jnb, inb] >= 0:
                add(i, j, inb, jnb, -1.0 / h**2)

    A = sp.coo_matrix((vals, (rows, cols)), shape=(count, count)).tocsr()
    return A, dof, count

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nx', type=int, default=140)
    ap.add_argument('--ny', type=int, default=140)
    ap.add_argument('--k',  type=int, default=6, help='# of smallest eigenpairs')
    ap.add_argument('--radius', type=float, default=35.0, help='hex circumradius in cells')
    args = ap.parse_args()

    nx, ny = args.nx, args.ny
    cx, cy = (nx-1)/2.0, (ny-1)/2.0

    # Hex pore mask (False=solid shell, True=pore) -> we want Dirichlet on pore cells
    hex_bool = hex_mask(nx, ny, cx, cy, args.radius)
    # Mark pore as True => Dirichlet => remove those DOFs
    pore_mask = hex_bool.copy()

    A, dof, ndof = assemble_laplacian_periodic(nx, ny, pore_mask)
    print(f"Grid {nx}x{ny}, DOFs (after Dirichlet pore) = {ndof}")

    # Compute k smallest eigenvalues/vectors of -Δ
    vals, vecs = spla.eigsh(A, k=min(args.k, ndof-2), which='SM')
    idx = np.argsort(vals)
    vals, vecs = vals[idx], vecs[:, idx]
    print("Eigenvalues (smallest):", vals[:min(6,len(vals))])

    # Reconstruct field on grid and plot |ψ| of the ground mode
    ground = np.zeros((ny, nx))
    gvec = vecs[:, 0]
    for j in range(ny):
        for i in range(nx):
            p = dof[j, i]
            if p >= 0:
                ground[j, i] = gvec[p]
            else:
                ground[j, i] = 0.0

    mag = np.abs(ground)
    mag /= mag.max() + 1e-12

    plt.figure(figsize=(6,5))
    plt.imshow(mag, origin='lower', cmap='magma', extent=[0,1,0,1])
    plt.colorbar(label='|ψ| / max')
    plt.title('Lowest eigenmode |ψ|: edge-localized along hex pore')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

