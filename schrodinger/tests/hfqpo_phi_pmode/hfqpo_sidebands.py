#!/usr/bin/env python3
"""
hfqpo_sidebands.py
------------------
Search for Lense-Thirring sidebands around HFQPO peaks using archival PDS and fitted (r0,a*) results.

Inputs
------
1) PDS CSV with columns: epoch_id, freq_Hz, power   (Leahy or fractional; we treat relatively)
   - Provide one file per energy band or a merged file with epoch ids.
2) Fit CSV from hfqpo_fit.py with columns: epoch_id, M_solar, a_star, r0_rg, ...

Usage:
    python hfqpo_sidebands.py --pds pds.csv --fit fit_results.csv --peaks pds_peaks.csv \
        --out sidebands.csv --plots outdir/

The pds_peaks.csv provides f1,f2 (observed) per epoch to center the search windows.

Method (quick triage):
- Compute Kerr frequencies at fitted (r0,a*): Ωφ, Ωθ → f_LT = (Ωφ - Ωθ) / (2π).
- Define windows around f1±f_LT, f2±f_LT (±W, default W = 0.1 f_LT).
- Estimate local background via median in annulus; compute simple SNR.
- Output per-epoch detection flags and SNRs.

Outputs
-------
CSV: epoch_id, f_LT_Hz, snr_f1_minus, snr_f1_plus, snr_f2_minus, snr_f2_plus, detected_any, notes
"""
import argparse, os, numpy as np, pandas as pd, math

# Physical constants
G   = 6.67430e-11
c   = 2.99792458e8
Msun= 1.98847e30
two_pi = 2.0 * math.pi

def kerr_Omega_phi_geom(r, a):
    return 1.0 / (r**1.5 + a)

def kerr_Omega_theta_geom(r, a):
    Om = kerr_Omega_phi_geom(r, a)
    term = 1.0 - 4.0*a/(r**1.5) + 3.0*a*a/(r*r)
    term = max(term, 0.0)
    return Om * math.sqrt(term)

def geom_to_SI_angfreq(omega_geom, M_solar):
    M_kg = M_solar * Msun
    return omega_geom * (c**3) / (G * M_kg)

def f_LT_Hz(r_rg, a, M_solar):
    Om = geom_to_SI_angfreq(kerr_Omega_phi_geom(r_rg, a), M_solar)
    Oth= geom_to_SI_angfreq(kerr_Omega_theta_geom(r_rg, a), M_solar)
    return (Om - Oth) / (2.0*math.pi)

def window_snr(freq, power, f_center, width):
    # Simple box SNR: mean inside window minus median in side annulus, normalized by MAD.
    m = (freq >= f_center-width) & (freq <= f_center+width)
    if not np.any(m): return 0.0
    inside = power[m]
    # side annulus: [1.5W, 3W]
    a = (np.abs(freq - f_center) >= 1.5*width) & (np.abs(freq - f_center) <= 3.0*width)
    bg = power[a]
    if len(bg) < 10:
        # fallback: global median
        bg = power
    med = np.median(bg)
    mad = np.median(np.abs(bg - med)) + 1e-12
    snr = (np.mean(inside) - med) / (1.4826*mad)
    return float(snr)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pds', required=True, help='CSV with epoch_id,freq_Hz,power')
    ap.add_argument('--fit', required=True, help='CSV from hfqpo_fit.py')
    ap.add_argument('--peaks', required=True, help='CSV with epoch_id,f1,f2 (observed)')
    ap.add_argument('--out', required=True, help='Output CSV summary')
    ap.add_argument('--plots', default='', help='Optional directory for quick-look plots')
    ap.add_argument('--win', type=float, default=0.1, help='Window half-width as fraction of f_LT (default 0.1)')
    args = ap.parse_args()

    pds = pd.read_csv(args.pds)
    fit = pd.read_csv(args.fit).set_index('epoch_id')
    pk  = pd.read_csv(args.peaks).set_index('epoch_id')

    rows = []
    if args.plots:
        os.makedirs(args.plots, exist_ok=True)

    for epoch_id, grp in pds.groupby('epoch_id'):
        if epoch_id not in fit.index or epoch_id not in pk.index:
            continue
        r0 = fit.loc[epoch_id, 'r0_rg']
        a  = fit.loc[epoch_id, 'a_star']
        M  = fit.loc[epoch_id, 'M_solar']
        fLT= f_LT_Hz(r0, a, M)
        width = max(args.win * fLT, 1e-3)

        f1 = pk.loc[epoch_id, 'f1']
        f2 = pk.loc[epoch_id, 'f2']

        freq = grp['freq_Hz'].values
        power= grp['power'].values

        s1m = window_snr(freq, power, f1 - fLT, width)
        s1p = window_snr(freq, power, f1 + fLT, width)
        s2m = window_snr(freq, power, f2 - fLT, width)
        s2p = window_snr(freq, power, f2 + fLT, width)
        detected = any([s>4.0 for s in (s1m,s1p,s2m,s2p)])

        rows.append(dict(epoch_id=epoch_id, f_LT_Hz=fLT, snr_f1_minus=s1m, snr_f1_plus=s1p,
                         snr_f2_minus=s2m, snr_f2_plus=s2p, detected_any=bool(detected), notes='ok'))

        if args.plots:
            try:
                import matplotlib.pyplot as plt
                fig,ax=plt.subplots(figsize=(6.5,3.2))
                ax.plot(freq, power, lw=0.8)
                for fc in [f1-fLT, f1+fLT, f2-fLT, f2+fLT]:
                    ax.axvspan(fc-width, fc+width, color='orange', alpha=0.25)
                ax.set_xlabel('Frequency (Hz)'); ax.set_ylabel('Power (arb)')
                ax.set_title(f'epoch {epoch_id}  f_LT ~ {fLT:.2f} Hz')
                fig.tight_layout()
                path = os.path.join(args.plots, f"sidebands_epoch_{epoch_id}.png")
                fig.savefig(path, dpi=150)
                plt.close(fig)
                print("Saved plot:", path)
            except Exception as e:
                print("Plotting failed:", e)

    out = pd.DataFrame(rows)
    out.to_csv(args.out, index=False)
    print("Wrote sideband summary:", args.out)

if __name__ == '__main__':
    main()
