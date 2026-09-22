#!/usr/bin/env python3
"""
hfqpo_energy_lags.py
--------------------
Evaluate the energy dependence of HFQPO fundamentals/overtone RMS and phase lags.

Input CSV (lags_rms.csv) per epoch and energy band with columns:
    epoch_id, band_lo_keV, band_hi_keV, rms_n1, rms_n2, lag_n1_ms, lag_n2_ms

Where lag sign convention is positive if hard lags soft (or vice versa, but consistent per file!).

Tests produced:
  1) Overtone hardening: RMS_n2 grows with energy more steeply than RMS_n1.
  2) Lag sign flip: sign(lag_n1) != sign(lag_n2) in hard bands, or a clear crossing vs energy.
  3) Summary flags per epoch, plus a small PNG plot per epoch (optional).

Usage:
    python hfqpo_energy_lags.py --lags lags_rms.csv --out energy_lag_tests.csv --plots outdir/

Output CSV:
    epoch_id, slope_rms_n1, slope_rms_n2, overtone_hardens, lag_flip, notes
"""
import argparse, os, numpy as np, pandas as pd

def linear_slope(x, y):
    x = np.asarray(x); y=np.asarray(y)
    if len(x) < 2: return np.nan
    A = np.vstack([x, np.ones_like(x)]).T
    try:
        m, b = np.linalg.lstsq(A, y, rcond=None)[0]
    except Exception:
        return np.nan
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lags', required=True, help='CSV with epoch_id, band_lo_keV, band_hi_keV, rms_n1, rms_n2, lag_n1_ms, lag_n2_ms')
    ap.add_argument('--out', required=True, help='Output CSV summary')
    ap.add_argument('--plots', default='', help='Optional output directory for quick-look plots')
    args = ap.parse_args()

    df = pd.read_csv(args.lags)
    rows = []
    if args.plots:
        os.makedirs(args.plots, exist_ok=True)

    for epoch_id, grp in df.groupby('epoch_id'):
        Ek = 0.5*(grp['band_lo_keV'].values + grp['band_hi_keV'].values)
        rms1 = grp['rms_n1'].values
        rms2 = grp['rms_n2'].values
        lag1 = grp['lag_n1_ms'].values
        lag2 = grp['lag_n2_ms'].values

        s1 = linear_slope(Ek, rms1)
        s2 = linear_slope(Ek, rms2)
        # Overtone hardens if s2 > s1 by a margin
        overtone_hard = (np.isfinite(s1) and np.isfinite(s2) and (s2 > s1 + 1e-6))

        # Lag flip: check sign at high-E end if data sorted
        idx = np.argsort(Ek)
        Ek, lag1s, lag2s = Ek[idx], lag1[idx], lag2[idx]
        lag_flip = (np.sign(lag1s[-1]) != np.sign(lag2s[-1])) if len(Ek)>=1 else False

        rows.append(dict(epoch_id=epoch_id, slope_rms_n1=s1, slope_rms_n2=s2,
                         overtone_hardens=bool(overtone_hard), lag_flip=bool(lag_flip),
                         notes='ok'))

        if args.plots:
            try:
                import matplotlib.pyplot as plt
                fig,(ax1,ax2)=plt.subplots(1,2, figsize=(7.5,3.2))
                ax1.plot(Ek, rms1[idx], 'o-', label='n=1')
                ax1.plot(Ek, rms2[idx], 's-', label='n=2')
                ax1.set_xlabel('Energy (keV)'); ax1.set_ylabel('RMS')
                ax1.set_title(f'RMS vs E (epoch {epoch_id})'); ax1.legend()

                ax2.plot(Ek, lag1s, 'o-', label='n=1')
                ax2.plot(Ek, lag2s, 's-', label='n=2')
                ax2.axhline(0, color='k', lw=0.8)
                ax2.set_xlabel('Energy (keV)'); ax2.set_ylabel('Lag (ms)')
                ax2.set_title('Phase lags vs E'); ax2.legend()

                fig.tight_layout()
                path = os.path.join(args.plots, f"energy_lags_epoch_{epoch_id}.png")
                fig.savefig(path, dpi=150)
                plt.close(fig)
                print("Saved plot:", path)
            except Exception as e:
                print("Plotting failed:", e)

    out = pd.DataFrame(rows)
    out.to_csv(args.out, index=False)
    print("Wrote summary:", args.out)

if __name__ == '__main__':
    main()
