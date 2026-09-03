#!/usr/bin/env python3
# fit_kappa.py — OLS estimator for κ in Δf/f = κ·(ΔU/c^2) + nuisances + noise
# Modes:
#   --mode orbit : CSV columns t[s], y[s/s], r[m], v[m/s]
#   --mode tide  : CSV columns t[s], y[s/s], U_tide[J/kg]
#
# Usage:
#   python3 fit_kappa.py --make-synth --csv synth_orbit.csv --mode orbit
#   python3 fit_kappa.py --csv synth_orbit.csv --mode orbit --poly 2

import argparse, math
import numpy as np

C = 2.99792458e8
G_DEF = 6.67430e-11
M_EARTH_DEF = 5.972e24

# ---------- template builders ----------

def build_orbit_template(t, r, v, G, M_earth):
    """
    Orbit relativity template:
      s(t) = (ΔU/c^2) - v^2/(2c^2), zero-meaned term-by-term
    """
    U  = -G*M_earth/np.maximum(r, 1e-6)
    sU = U - U.mean()
    vv = v*v
    sSR = -(0.5*(vv - vv.mean()))
    s = (sU + sSR)/(C*C)
    if np.std(s) < 1e-20:
        raise ValueError("Orbit template nearly flat; use an eccentric synthetic or reduce --poly.")
    return s

def build_tide_template(U_tide):
    return (U_tide - np.mean(U_tide))/(C*C)

# ---------- OLS core (stable; no extra matmuls) ----------

def fit_kappa_ols(y, s, H=None):
    """
    Ordinary least squares on y = [s H] [kappa; a] + ε
    Returns: k_hat, sigma_k
    """
    y = np.asarray(y, dtype=np.float64).reshape(-1)
    s = np.asarray(s, dtype=np.float64).reshape(-1)
    T = len(y)

    if H is None or H.size == 0:
        X = s.reshape(-1,1)
    else:
        H = np.asarray(H, dtype=np.float64)
        if H.ndim == 1:
            H = H.reshape(-1,1)
        X = np.column_stack([s, H])

    # Solve by least squares
    beta, residuals, rank, svals = np.linalg.lstsq(X, y, rcond=None)
    k_hat = float(beta[0])

    # Residual variance (RSS/dof)
    if residuals.size > 0:
        RSS = float(residuals[0])
    else:
        # full-rank case without residuals returned (rare); recompute safely
        RSS = float(np.sum((y - X @ beta)**2))
    dof = max(T - X.shape[1], 1)
    sigma2 = RSS / dof

    # Covariance from (X^T X)^{-1}
    XtX = X.T @ X
    cov = sigma2 * np.linalg.pinv(XtX)    # pinv is robust if columns are mildly collinear
    sigma_k = float(np.sqrt(cov[0,0]))

    return k_hat, sigma_k

# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description="Fit κ in Δf/f = κ·(ΔU/c^2) via OLS (stable)")
    ap.add_argument("--csv", required=True, help="Input CSV path")
    ap.add_argument("--mode", choices=["orbit","tide"], default="orbit")
    ap.add_argument("--G", type=float, default=G_DEF)
    ap.add_argument("--M_earth", type=float, default=M_EARTH_DEF)
    ap.add_argument("--poly", type=int, default=2, choices=[0,1,2,3],
                    help="Polynomial drift degree included in H (0..3)")

    # Synthetic generator (optional)
    ap.add_argument("--make-synth", action="store_true")
    ap.add_argument("--T", type=float, default=86400.0)
    ap.add_argument("--dt", type=float, default=30.0)
    ap.add_argument("--kappa-synth", type=float, default=1.0)
    ap.add_argument("--noise", type=float, default=5e-13)
    ap.add_argument("--ecc", type=float, default=0.01)
    args = ap.parse_args()

    # Synthesize if asked
    if args.make_synth:
        t = np.arange(0.0, args.T, args.dt, dtype=np.float64)
        a = 2.656e7               # ~GPS semi-major axis [m] (toy)
        e = float(args.ecc)
        n = math.sqrt(args.G*args.M_earth/a**3)
        r = a*(1.0 - e*np.cos(n*t))
        v = np.sqrt(args.G*args.M_earth*(2.0/r - 1.0/a))
        U = -args.G*args.M_earth/np.maximum(r,1e-6)
        s = (U - U.mean())/(C*C) - 0.5*((v*v)-(v*v).mean())/(C*C)
        y = args.kappa_synth*s + args.noise*np.random.randn(t.size)
        np.savetxt(args.csv, np.c_[t,y,r,v], delimiter=",", fmt="%.9e")
        print(f"[synth] wrote {args.csv} with κ={args.kappa_synth}, e={e}, noise σ={args.noise:.2e}")

    # Load CSV
    data = np.loadtxt(args.csv, delimiter=",", ndmin=2)
    if args.mode == "orbit" and data.shape[1] < 4:
        raise ValueError("orbit mode needs CSV columns: t, y, r, v")
    if args.mode == "tide" and data.shape[1] < 3:
        raise ValueError("tide mode needs CSV columns: t, y, U_tide")

    t = data[:,0].astype(np.float64)
    y = data[:,1].astype(np.float64)

    # Build H on normalized time x in [-1,1] (well-conditioned drift columns)
    H = None
    if args.poly > 0:
        tmin, tmax = float(t.min()), float(t.max())
        scale = max(tmax - tmin, 1.0)
        x = 2.0*(t - 0.5*(tmin + tmax))/scale
        cols = [np.ones_like(x)]
        if args.poly >= 1: cols.append(x)
        if args.poly >= 2: cols.append(x**2)
        if args.poly >= 3: cols.append(x**3)
        H = np.column_stack(cols)

    # Template
    if args.mode == "orbit":
        r = data[:,2].astype(np.float64)
        v = data[:,3].astype(np.float64)
        s = build_orbit_template(t, r, v, args.G, args.M_earth)
    else:
        U_tide = data[:,2].astype(np.float64)
        s = build_tide_template(U_tide)

    # Fit
    k_hat, sigma_k = fit_kappa_ols(y, s, H=H)

    # Report χ_t = c^4/(4π κ G)
    chi_t = C**4/(4.0*np.pi*args.G*k_hat)
    print(f"kappa = {k_hat:.6e} ± {sigma_k:.6e}")
    print(f"chi_t = {chi_t:.6e}  (SI units)")

if __name__ == "__main__":
    main()

