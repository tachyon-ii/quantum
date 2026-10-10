#!/usr/bin/env python3
"""
HERA residual oscillation fit (patched)

- Reads HERA Table-10–style CSV (Q2, xBj, sigma, d tot,…).
- Parses xBj strings like "0.502x10-5".
- Optional theory CSV (same grid) for sigma_theory to build residual = data/theory - 1.
- Otherwise uses a smooth spline baseline (quick-look only).
- y cut, Q^2 window, optional x window, min # of x per slice.
- Fits ε * cos(2π x / Δx + φ) * exp(-α(1-x)).
  * --fix-alpha  : hold α = 0
  * --delta-x    : fix Δx; if omitted, fit (free)
- Writes per-Q^2 CSV + PNG plots and χ²/ndf per slice.

Examples:
  python hera_residual_fit.py --data HERA_full.csv --q2-min 8 --q2-max 18 --y-max 0.7 --min-nx 10 --outdir hera_out_quick
  python hera_residual_fit.py --data HERA_full.csv --theory HERA_theory.csv --theory-col sigma_theory --q2-min 8 --q2-max 18 --y-max 0.7 --min-nx 10 --outdir hera_out_theory
  python hera_residual_fit.py --data HERA_full.csv --theory HERA_theory.csv --theory-col sigma_theory --delta-x 0.073 --fix-alpha --q2-min 8 --q2-max 18 --outdir hera_out_fixedDx_alpha0
"""
import argparse, re
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
from pathlib import Path

def parse_xbj_str(s):
    if pd.isna(s): return np.nan
    t = str(s).strip()
    t = re.sub(r'\s*([0-9.]+)\s*x10\s*([+-]?\d+)\s*', r'\1e\2', t)
    try: return float(t)
    except ValueError: return np.nan

def resid_model_full(x, eps, inv_delta_x, phi, alpha):
    return eps * np.cos(2*np.pi*x*inv_delta_x + phi) * np.exp(-alpha*(1.0 - x))

def resid_model_alpha0(x, eps, inv_delta_x, phi):
    return eps * np.cos(2*np.pi*x*inv_delta_x + phi)

def smooth_baseline(x, y, s_fac=0.0):
    order = np.argsort(x); xs, ys = x[order], y[order]
    s_param = s_fac if s_fac > 0 else 0.001 * len(xs)
    return UnivariateSpline(xs, ys, s=s_param, k=3)

def load_table(csv_path):
    df = pd.read_csv(csv_path)
    cols = {c.lower(): c for c in df.columns}
    q2col   = cols.get('q2', None)
    xcol_raw= cols.get('xbj', None) or cols.get('x', None) or cols.get('x_num', None)
    # accept several plausible names for the measured reduced cross section
    sigcol  = (cols.get('sigma', None) or cols.get('sigma_r', None) or
               cols.get('sigma_r,nc', None) or cols.get('sigma_theory', None))
    utot    = cols.get('d tot', None) or cols.get('delta_tot', None) or cols.get('total_uncertainty_%', None)
    if not (q2col and xcol_raw and sigcol):
        raise RuntimeError(f"Missing required columns (Q2/xBj/sigma). Found: {list(df.columns)}")
    # parse x
    if xcol_raw.lower() in ('xbj','x'):
        df['x_num'] = df[xcol_raw].map(parse_xbj_str)
        xcol = 'x_num'
    else:
        xcol = xcol_raw
        df[xcol] = pd.to_numeric(df[xcol], errors='coerce')
    # numerics
    for c in [q2col, sigcol]:
        if df[c].dtype == object: df[c] = df[c].astype(str).str.replace('%','', regex=False)
        df[c] = pd.to_numeric(df[c], errors='coerce')
    if utot:
        if df[utot].dtype == object: df[utot] = df[utot].astype(str).str.replace('%','', regex=False)
        df[utot] = pd.to_numeric(df[utot], errors='coerce')
    return df, q2col, xcol, sigcol, utot

def merge_theory(df_data, df_theory, q2col, xcol, theory_col, tol=1e-9):
    # rename columns to avoid collisions
    d = df_data.rename(columns={'sigma':'sigma_data',
                                'sigma_r':'sigma_data',
                                'sigma_r,nc':'sigma_data',
                                'reduced_cross_section':'sigma_data'}).copy()
    t = df_theory.copy()
    if theory_col not in t.columns:
        raise RuntimeError(f"--theory-col '{theory_col}' not found in theory CSV.")
    t = t.rename(columns={theory_col:'sigma_theory'})
    # ensure numeric x columns exist
    if xcol not in d.columns:
        raise RuntimeError(f"x column '{xcol}' missing in data.")
    if xcol not in t.columns:
        # try to parse theory x from xBj/x
        xraw = next((c for c in t.columns if c.lower() in ('xbj','x','x_num')), None)
        if not xraw: raise RuntimeError("Theory CSV must contain x column (xBj/x/x_num).")
        t[xcol] = t[xraw].apply(parse_xbj_str) if xraw.lower() in ('xbj','x') else pd.to_numeric(t[xraw], errors='coerce')
    # nearest merge per Q2
    out_rows = []
    for q2, dsl in d.groupby(q2col):
        tsl = t[t[q2col]==q2].copy()
        if tsl.empty:
            continue
        dsl = dsl.sort_values(xcol); tsl = tsl.sort_values(xcol)
        # merge_asof with tolerance
        m = pd.merge_asof(dsl, tsl[[xcol,'sigma_theory']], on=xcol, direction='nearest', tolerance=tol)
        m = m.dropna(subset=['sigma_theory'])
        out_rows.append(m)
    if not out_rows:
        # fall back to a coarser rounding if nothing merges
        d['_xr'] = d[xcol].round(8); t['_xr'] = t[xcol].round(8)
        m = pd.merge(d, t[[q2col,'_xr','sigma_theory']], on=[q2col,'_xr'], how='inner')
        return m.drop(columns=['_xr'])
    return pd.concat(out_rows, ignore_index=True)

def main():
    ap = argparse.ArgumentParser(description="HERA residual oscillation fit (patched)")
    ap.add_argument('--data', required=True)
    ap.add_argument('--theory', default=None)
    ap.add_argument('--theory-col', default='sigma_theory')
    ap.add_argument('--q2-min', type=float, default=8.0)
    ap.add_argument('--q2-max', type=float, default=18.0)
    ap.add_argument('--y-max',  type=float, default=0.70)
    ap.add_argument('--sqrts',  type=float, default=318.0)
    ap.add_argument('--min-nx', type=int,   default=10)
    ap.add_argument('--bin-width', type=float, default=0.01)
    ap.add_argument('--delta-x', type=float, default=None)
    ap.add_argument('--fix-alpha', action='store_true', help='Hold alpha = 0')
    ap.add_argument('--x-min', type=float, default=None)
    ap.add_argument('--x-max', type=float, default=None)
    ap.add_argument('--outdir', default='hera_out')
    args = ap.parse_args()

    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)

    df, q2col, xcol, sigcol, utot = load_table(args.data)

    # attach theory if provided
    if args.theory:
        df_th, q2_th, x_th, sig_th, _ = load_table(args.theory)
        df = merge_theory(df, df_th, q2col, xcol, args.theory_col)
        have_theory = True
    else:
        have_theory = False

    # compute y and apply cuts
    s = args.sqrts**2
    df['y'] = df[q2col] / (s * df[xcol])
    if args.y_max > 0: df = df[df['y'] < args.y_max].copy()
    df = df[(df[q2col] >= args.q2_min) & (df[q2col] <= args.q2_max)].copy()
    # optional x window
    if args.x_min is not None: df = df[df[xcol] >= args.x_min].copy()
    if args.x_max is not None: df = df[df[xcol] <= args.x_max].copy()

    # group slices
    counts = df.groupby(q2col)[xcol].count().sort_values(ascending=False)
    good_q2 = [q for q,n in counts.items() if n >= args.min_nx]
    if not good_q2:
        print("No Q2 slices meet min-nx; try relaxing --q2-min/max or --min-nx."); return

    # choose models
    def fit_free(x, r, e):
        # Δx free, α = 0 if requested else free
        if args.fix_alpha:
            p0=[0.002, 12.0, 0.0]; bounds=([0.0, 5.0, -np.pi],[0.05, 60.0, np.pi])
            popt, pcov = curve_fit(resid_model_alpha0, x, r, p0=p0, sigma=e, absolute_sigma=True, bounds=bounds, maxfev=20000)
            perr = np.sqrt(np.diag(pcov)); eps, inv_dx, phi = popt; d_eps, d_inv, d_phi = perr
            alpha, d_alpha = 0.0, 0.0
            npar = 3
            yf = resid_model_alpha0(x, eps, inv_dx, phi)
        else:
            p0=[0.002, 12.0, 0.0, 0.2]; bounds=([0.0, 5.0, -np.pi, 0.0],[0.05, 60.0, np.pi, 5.0])
            popt, pcov = curve_fit(resid_model_full, x, r, p0=p0, sigma=e, absolute_sigma=True, bounds=bounds, maxfev=20000)
            perr = np.sqrt(np.diag(pcov)); eps, inv_dx, phi, alpha = popt; d_eps, d_inv, d_phi, d_alpha = perr
            npar = 4
            yf = resid_model_full(x, eps, inv_dx, phi, alpha)
        Delta_x = 1.0/inv_dx if inv_dx!=0 else np.nan
        Delta_x_err = (d_inv/(inv_dx**2)) if (inv_dx!=0) else 0.0
        chi2 = np.sum(((r - yf)/e)**2); ndf = max(len(x) - npar, 1)
        return dict(eps=eps, d_eps=d_eps, Delta_x=Delta_x, d_Delta_x=Delta_x_err,
                    phi=phi, d_phi=d_phi, alpha=alpha, d_alpha=d_alpha, chi2_ndf=chi2/ndf)

    def fit_fixDx(x, r, e, Delta_x):
        inv_dx = 1.0/Delta_x
        if args.fix_alpha:
            def model(xv, eps, phi): return eps * np.cos(2*np.pi*xv*inv_dx + phi)
            p0=[0.002, 0.0]; bounds=([0.0, -np.pi],[0.05, np.pi])
            popt, pcov = curve_fit(model, x, r, p0=p0, sigma=e, absolute_sigma=True, bounds=bounds, maxfev=20000)
            perr = np.sqrt(np.diag(pcov)); eps, phi = popt; d_eps, d_phi = perr
            alpha, d_alpha = 0.0, 0.0; npar = 2
            yf = model(x, eps, phi)
        else:
            def model(xv, eps, phi, alpha):
                return eps * np.cos(2*np.pi*xv*inv_dx + phi) * np.exp(-alpha*(1.0 - xv))
            p0=[0.002, 0.0, 0.2]; bounds=([0.0, -np.pi, 0.0],[0.05, np.pi, 5.0])
            popt, pcov = curve_fit(model, x, r, p0=p0, sigma=e, absolute_sigma=True, bounds=bounds, maxfev=20000)
            perr = np.sqrt(np.diag(pcov)); eps, phi, alpha = popt; d_eps, d_phi, d_alpha = perr
            npar = 3; yf = model(x, eps, phi, alpha)
        chi2 = np.sum(((r - yf)/e)**2); ndf = max(len(x) - npar, 1)
        return dict(eps=eps, d_eps=d_eps, phi=phi, d_phi=d_phi, alpha=alpha, d_alpha=d_alpha, chi2_ndf=chi2/ndf)

    rows = []
    plots_dir = Path(args.outdir); plots_dir.mkdir(exist_ok=True, parents=True)

    for q2, sl in df.groupby(q2col):
        if q2 not in good_q2: continue
        sl = sl.sort_values(xcol)
        x = sl[xcol].to_numpy()
        # build residual
        if have_theory and 'sigma_theory' in sl.columns:
            sig = sl['sigma'].to_numpy() if 'sigma' in sl.columns else sl.get('sigma_data', np.nan)
            base= sl['sigma_theory'].to_numpy()
            r = sig/base - 1.0
            if utot and utot in sl.columns:
                e = (sl[utot].to_numpy()/100.0) * sig/base
            else:
                e = np.full_like(x, 0.01)
        else:
            sig = sl['sigma'].to_numpy()
            spline = smooth_baseline(x, sig); base = spline(x)
            r = sig/base - 1.0
            if utot and utot in sl.columns:
                e = (sl[utot].to_numpy()/100.0) * sig/base
            else:
                e = np.full_like(x, 0.01)

        m = np.isfinite(x) & np.isfinite(r) & np.isfinite(e)
        x_fit, r_fit, e_fit = x[m], r[m], e[m]
        if len(x_fit) < max(8, args.min_nx//2): continue

        if args.delta_x and args.delta_x > 0:
            res = fit_fixDx(x_fit, r_fit, e_fit, args.delta_x)
            Delta_x, Delta_x_err = args.delta_x, 0.0
        else:
            res = fit_free(x_fit, r_fit, e_fit)
            Delta_x, Delta_x_err = res['Delta_x'], res['d_Delta_x']

        rows.append({
            'Q2': q2, 'N_points': len(x_fit),
            'eps': res['eps'], 'eps_err': res['d_eps'],
            'Delta_x': Delta_x, 'Delta_x_err': Delta_x_err,
            'phi': res['phi'], 'phi_err': res['d_phi'],
            'alpha': res['alpha'], 'alpha_err': res['d_alpha'],
            'chi2_ndf': res['chi2_ndf']
        })

        # plot
        xf = np.linspace(x_fit.min(), x_fit.max(), 600)
        if args.delta_x and args.delta_x > 0:
            invdx = 1.0/args.delta_x
            if args.fix_alpha:
                yf = res['eps'] * np.cos(2*np.pi*xf*invdx + res['phi'])
                fit_label = f"Δx={args.delta_x:.3f}, ε≈{res['eps']:.3g}"
            else:
                yf = res['eps'] * np.cos(2*np.pi*xf*invdx + res['phi']) * np.exp(-res['alpha']*(1.0 - xf))
                fit_label = f"Δx={args.delta_x:.3f}, ε≈{res['eps']:.3g}, α≈{res['alpha']:.2g}"
        else:
            invdx = 1.0/Delta_x if Delta_x else np.nan
            if args.fix_alpha:
                yf = res['eps'] * np.cos(2*np.pi*xf*invdx + res['phi'])
                fit_label = f"Δx≈{Delta_x:.3f}, ε≈{res['eps']:.3g}"
            else:
                yf = res['eps'] * np.cos(2*np.pi*xf*invdx + res['phi']) * np.exp(-res['alpha']*(1.0 - xf))
                fit_label = f"Δx≈{Delta_x:.3f}, ε≈{res['eps']:.3g}, α≈{res['alpha']:.2g}"

        fig, ax = plt.subplots(1,1, figsize=(7,4))
        ax.errorbar(x_fit, r_fit, yerr=e_fit, fmt='o', ms=3, label='Residual')
        ax.plot(xf, yf, '-', lw=2, label=fit_label)
        ax.set_title(f"Residual (data/theory-1) | Q²={q2:.2f} GeV²")
        ax.set_xlabel('x_Bj'); ax.set_ylabel('Res'); ax.legend(loc='best'); fig.tight_layout()
        plt.savefig(plots_dir / f"residual_Q2_{q2:.2f}.png", dpi=150); plt.close(fig)

    pd.DataFrame(rows).sort_values('Q2').to_csv(Path(args.outdir, "residual_fit_summary.csv"), index=False)
    print("Saved:", Path(args.outdir, "residual_fit_summary.csv"))

if __name__ == "__main__":
    main()

