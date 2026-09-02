
#!/usr/bin/env python3
"""
make_hera_theory.py  (dependency-free helper)

Builds a HERA_theory.csv with columns: Q2, x_num, sigma_theory
on the same (Q2, x) grid as your data.

Two modes:
  --mode spline
      Compute a smooth baseline per Q2 slice using a cubic spline over x,
      and call that 'sigma_theory'. This is a quick-look surrogate (not QCD).

  --mode passthrough --theory-csv THEORY.csv --theory-col sigma_theory
      Merge a user-supplied theory CSV (same grid) that already contains
      the reduced cross-section prediction in column THEORY_COL.

Usage examples:
  python make_hera_theory.py --data HERA_full.csv --out HERA_theory.csv --mode spline
  python make_hera_theory.py --data HERA_full.csv --out HERA_theory.csv \
         --mode passthrough --theory-csv HERAPDF_prediction.csv --theory-col sigma_theory
"""

import argparse, re, numpy as np, pandas as pd
from scipy.interpolate import UnivariateSpline

def parse_xbj_str(s):
    if pd.isna(s): return np.nan
    t = str(s).strip()
    t = re.sub(r'\s*([0-9.]+)\s*x10\s*([+-]?\d+)\s*', r'\1e\2', t)
    try: return float(t)
    except ValueError: return np.nan

def build_spline_baseline(df):
    """Return a DataFrame with columns Q2, x_num, sigma_theory built by cubic spline per Q2."""
    rows = []
    for q2, sl in df.groupby('Q2'):
        sl = sl.sort_values('x_num')
        x = sl['x_num'].to_numpy()
        y = sl['sigma'].to_numpy()
        # Drop nan
        m = np.isfinite(x) & np.isfinite(y)
        x, y = x[m], y[m]
        if len(x) < 5:
            # too few points; just copy sigma
            for xv, yv in zip(x, y):
                rows.append((q2, xv, yv))
            continue
        # Weak smoothing spline as baseline
        s_param = 0.001 * len(x)
        spline = UnivariateSpline(x, y, s=s_param, k=3)
        yhat = spline(x)
        for xv, yh in zip(x, yhat):
            rows.append((q2, xv, float(yh)))
    return pd.DataFrame(rows, columns=['Q2','x_num','sigma_theory'])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', required=True, help='HERA_full.csv path')
    ap.add_argument('--out',  required=True, help='HERA_theory.csv path to write')
    ap.add_argument('--mode', choices=['spline','passthrough'], default='spline')
    ap.add_argument('--theory-csv', default=None, help='CSV with theory column (passthrough mode)')
    ap.add_argument('--theory-col', default='sigma_theory', help='Column name in theory CSV')
    args = ap.parse_args()

    df = pd.read_csv(args.data)
    if 'Q2' not in df.columns or 'xBj' not in df.columns or 'sigma' not in df.columns:
        raise RuntimeError("Expected columns 'Q2', 'xBj', 'sigma' in --data CSV.")
    # Parse x
    df['x_num'] = df['xBj'].map(parse_xbj_str)
    df['Q2'] = pd.to_numeric(df['Q2'], errors='coerce')
    df['sigma'] = pd.to_numeric(df['sigma'], errors='coerce')
    df = df[np.isfinite(df['Q2']) & np.isfinite(df['x_num']) & np.isfinite(df['sigma'])].copy()

    if args.mode == 'spline':
        out = build_spline_baseline(df)
    else:
        if not args.theory_csv:
            raise RuntimeError("passthrough mode requires --theory-csv")
        th = pd.read_csv(args.theory_csv)
        # normalize theory columns
        cols = {c.lower(): c for c in th.columns}
        q2_th = cols.get('q2', None)
        x_th  = cols.get('x_num', None) or cols.get('xbj', None) or cols.get('x', None)
        if x_th and x_th.lower() in ('xbj','x'):
            # parse if given as string
            th['x_num'] = th[x_th].map(parse_xbj_str)
            x_th = 'x_num'
        thcol = args.theory_col if args.theory_col in th.columns else None
        if not (q2_th and x_th and thcol):
            raise RuntimeError("Theory CSV must contain Q2, x_num (or xBj/x), and the given --theory-col.")
        # merge
        d = df[['Q2','x_num']].copy()
        # round x to avoid float merge issues
        d['_xr'] = d['x_num'].round(12); th['_xr'] = th[x_th].round(12)
        m = pd.merge(d, th[[q2_th,'_xr',thcol]], left_on=['Q2','_xr'], right_on=[q2_th,'_xr'], how='inner')
        out = m[['Q2','_xr',thcol]].rename(columns={'_xr':'x_num', thcol:'sigma_theory'})

    out.to_csv(args.out, index=False)
    print("Wrote:", args.out)

if __name__ == '__main__':
    main()
