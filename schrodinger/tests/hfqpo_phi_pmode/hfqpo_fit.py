#!/usr/bin/env python3
"""
hfqpo_fit.py
------------
Fit HFQPO pairs (f1,f2) with a minimal near-horizon p-mode cavity model gated by a Φ-boundary.

Model (source frame):
    ω_n^2 = κ_r^2(r0, a*) + (n π c_s / L_phys)^2,       n = 1,2,...
Observed:
    f_n_obs = (ω_n / 2π) * g_GR,    with 0 < g_GR ≤ 1

Where:
  - κ_r(r0, a*) is the Kerr radial epicyclic frequency (angular, rad/s).
  - L_phys = L_rg * r_g,  with r_g = G M / c^2.
  - c_s = η c,  with 0 < η < 1.
  - g_GR is an effective net transfer/redshift factor (fitted scalar) absorbing
    gravitational redshift, beaming, geometry and Φ-transmissivity to first order.

Inputs
------
CSV (pds_peaks.csv-like), columns (minimum):
    epoch_id, f1, df1, f2, df2, M_solar
Optional columns (if present are used as starting guesses / priors, not hard constraints):
    spin_est  (dimensionless Kerr a* in [0,1) )
    inc_deg   (inclination, degrees)  -- used only for metadata, not in the current fit

Command-line
------------
Example:
    python hfqpo_fit.py --peaks pds_peaks.csv --out fit_results.csv --plots outdir_plots/

Outputs
-------
CSV with columns:
    epoch_id, M_solar, a_star, r0_rg, L_rg, eta, g_GR, kappa_r_Hz, chi2, dof, notes

Notes
-----
- This is a minimal, dependency-light fitter (NumPy/Pandas only). It uses a hybrid coarse grid
  + local coordinate descent. Good enough to triage archival data quickly.
- Units are handled explicitly. Kerr frequencies follow standard expressions in geometric units.
- You can later swap in a more sophisticated optimizer without changing the I/O contract.
"""
import argparse
import os
import math
import numpy as np
import pandas as pd

# Physical constants (SI)
G   = 6.67430e-11
c   = 2.99792458e8
Msun= 1.98847e30
two_pi = 2.0 * math.pi

# ---------------- Kerr frequency utilities ----------------
def kerr_Omega_phi_geom(r, a):
    """Orbital angular frequency Ωφ in geometric units (c=G=M=1). r in r_g units; a in [0,1)."""
    # In geometric units (M=1): Ωφ = 1 / (r^(3/2) + a)
    return 1.0 / (r**1.5 + a)

def kerr_kappa_r_geom(r, a):
    """Radial epicyclic angular frequency κ_r (geometric units)."""
    Om = kerr_Omega_phi_geom(r, a)
    term = 1.0 - 6.0/r + 8.0*a/(r**1.5) - 3.0*a*a/(r*r)
    term = max(term, 0.0)  # clamp small negative due to num noise
    return Om * math.sqrt(term)

def kerr_Omega_theta_geom(r, a):
    """Vertical epicyclic angular frequency Ωθ (geometric units)."""
    Om = kerr_Omega_phi_geom(r, a)
    term = 1.0 - 4.0*a/(r**1.5) + 3.0*a*a/(r*r)
    term = max(term, 0.0)
    return Om * math.sqrt(term)

def geom_to_SI_angfreq(omega_geom, M_solar):
    """
    Convert geometric angular frequency (1/M units) to SI rad/s.
    In geometric units: time_unit = GM/c^3. So ω_SI = ω_geom * c^3 / (G M).
    """
    M_kg = M_solar * Msun
    return omega_geom * (c**3) / (G * M_kg)

def kappa_r_SI(r_rg, a, M_solar):
    """κ_r in SI rad/s for radius r in r_g units (r_g = GM/c^2)."""
    return geom_to_SI_angfreq(kerr_kappa_r_geom(r_rg, a), M_solar)

def Omega_phi_SI(r_rg, a, M_solar):
    return geom_to_SI_angfreq(kerr_Omega_phi_geom(r_rg, a), M_solar)

def Omega_theta_SI(r_rg, a, M_solar):
    return geom_to_SI_angfreq(kerr_Omega_theta_geom(r_rg, a), M_solar)

# ---------------- Model frequencies ----------------
def model_frequencies_Hz(r0_rg, L_rg, eta, g_GR, a_star, M_solar):
    """
    Returns (f1_obs, f2_obs) in Hz for n=1,2 given parameters.
    """
    # Geometry / units
    r_g   = G * (M_solar * Msun) / (c**2)  # meters
    L_phys= L_rg * r_g                      # meters
    cs    = eta * c                         # m/s

    # Angular frequencies (rad/s)
    kappa = kappa_r_SI(r0_rg, a_star, M_solar)
    # Acoustic term (rad/s)
    w1_ac = (1.0 * math.pi * cs) / L_phys
    w2_ac = (2.0 * math.pi * cs) / L_phys

    w1 = math.sqrt(kappa**2 + w1_ac**2)
    w2 = math.sqrt(kappa**2 + w2_ac**2)

    f1_src = w1 / (2.0 * math.pi)
    f2_src = w2 / (2.0 * math.pi)

    # Apply net redshift/transfer
    return g_GR * f1_src, g_GR * f2_src, kappa/(2.0*math.pi)

def chi2_pair(f1_obs, df1, f2_obs, df2, f1_mod, f2_mod):
    chi = 0.0
    if df1>0: chi += ((f1_obs - f1_mod)/df1)**2
    if df2>0: chi += ((f2_obs - f2_mod)/df2)**2
    return chi

# ---------------- Fitting ----------------
def fit_epoch(row, grid, local_steps=30):
    """
    Fit a single epoch row dict with coarse grid + coordinate descent refinement.
    grid: dict with ranges for r0_rg, L_rg, eta, g_GR, a_star
    Returns dict of best params and diagnostics.
    """
    f1, df1 = row['f1'], row.get('df1', max(0.05*f1,1e-3))
    f2, df2 = row['f2'], row.get('df2', max(0.05*f2,1e-3))
    M_solar = float(row['M_solar'])

    # seed for spin
    a_seed = float(row.get('spin_est', 0.8))
    # Coarse grid
    best = None
    for a in np.linspace(grid['a_star'][0], grid['a_star'][1], grid['a_star'][2]):
        for r0 in np.linspace(grid['r0_rg'][0], grid['r0_rg'][1], grid['r0_rg'][2]):
            # stability: r0 > r_isco ~ function of a; we approximate r>3 for safety
            if r0 <= 3.0: 
                continue
            for L in np.linspace(grid['L_rg'][0], grid['L_rg'][1], grid['L_rg'][2]):
                if L <= 0: 
                    continue
                for eta in np.linspace(grid['eta'][0], grid['eta'][1], grid['eta'][2]):
                    for g in np.linspace(grid['g_GR'][0], grid['g_GR'][1], grid['g_GR'][2]):
                        f1m, f2m, kHz = model_frequencies_Hz(r0, L, eta, g, a, M_solar)
                        c2 = chi2_pair(f1, df1, f2, df2, f1m, f2m)
                        if (best is None) or (c2 < best['chi2']):
                            best = dict(a_star=a, r0_rg=r0, L_rg=L, eta=eta, g_GR=g, kappa_r_Hz=kHz, chi2=c2)

    # Local coordinate descent (small perturbations around best)
    if best is None:
        return None
    def clamp(val, lo, hi): return max(lo, min(hi, val))
    # step sizes ~ 5% of ranges
    dr = 0.05*(grid['r0_rg'][1]-grid['r0_rg'][0])
    dL = 0.05*(grid['L_rg'][1]-grid['L_rg'][0])
    de = 0.05*(grid['eta'][1]-grid['eta'][0])
    dg = 0.05*(grid['g_GR'][1]-grid['g_GR'][0])
    da = 0.05*(grid['a_star'][1]-grid['a_star'][0])

    for _ in range(local_steps):
        improved = False
        for key, step, bounds in [('r0_rg',dr,grid['r0_rg']), ('L_rg',dL,grid['L_rg']), ('eta',de,grid['eta']), ('g_GR',dg,grid['g_GR']), ('a_star',da,grid['a_star'])]:
            for sgn in (+1,-1):
                trial = best.copy()
                trial[key] = clamp(best[key] + sgn*step, bounds[0], bounds[1])
                if key == 'r0_rg' and trial[key] <= 3.0:
                    continue
                f1m, f2m, kHz = model_frequencies_Hz(trial['r0_rg'], trial['L_rg'], trial['eta'], trial['g_GR'], trial['a_star'], M_solar)
                c2 = chi2_pair(f1, df1, f2, df2, f1m, f2m)
                if c2 < best['chi2']:
                    trial['chi2'] = c2
                    trial['kappa_r_Hz'] = kHz
                    best = trial
                    improved = True
        if not improved:
            break

    dof = 2 - 5  # two data points, five params → negative; we report chi2 only for ranking
    best['dof'] = dof
    return best

def main():
    import argparse, os
    ap = argparse.ArgumentParser()
    ap.add_argument('--peaks', required=True, help='CSV with epoch_id,f1,df1,f2,df2,M_solar[,spin_est,inc_deg]')
    ap.add_argument('--out', required=True, help='Output CSV for fit results')
    ap.add_argument('--plots', default='', help='Optional directory to dump simple predicted-vs-observed plots')
    # coarse grid ranges
    ap.add_argument('--r0', default='3.5,10,30', help='r0_rg min,max,N  (default 3.5,10,30)')
    ap.add_argument('--L',  default='0.2,5,30',   help='L_rg  min,max,N  (default 0.2,5,30)')
    ap.add_argument('--eta',default='0.01,0.5,20',help='eta   min,max,N  (default 0.01,0.5,20)')
    ap.add_argument('--g',  default='0.5,1.0,12', help='g_GR  min,max,N  (default 0.5,1.0,12)')
    ap.add_argument('--spin',default='0.0,0.99,12',help='a*    min,max,N  (default 0.0,0.99,12)')
    args = ap.parse_args()

    def parse_triplet(s):
        lo,hi,N = s.split(',')
        return (float(lo), float(hi), int(N))

    grid = {
        'r0_rg': parse_triplet(args.r0),
        'L_rg' : parse_triplet(args.L),
        'eta'  : parse_triplet(args.eta),
        'g_GR' : parse_triplet(args.g),
        'a_star':parse_triplet(args.spin),
    }

    df = pd.read_csv(args.peaks)
    rows = []
    if args.plots:
        os.makedirs(args.plots, exist_ok=True)

    for _, row in df.iterrows():
        epoch_id = row['epoch_id']
        best = fit_epoch(row, grid)
        if best is None:
            rows.append({'epoch_id':epoch_id, 'notes':'fit_failed'})
            continue
        # Compute model frequencies for reporting
        f1m, f2m, kHz = model_frequencies_Hz(best['r0_rg'], best['L_rg'], best['eta'], best['g_GR'], best['a_star'], row['M_solar'])
        rows.append({
            'epoch_id': epoch_id,
            'M_solar': row['M_solar'],
            'a_star': best['a_star'],
            'r0_rg': best['r0_rg'],
            'L_rg': best['L_rg'],
            'eta': best['eta'],
            'g_GR': best['g_GR'],
            'kappa_r_Hz': best['kappa_r_Hz'],
            'f1_obs': row['f1'], 'f1_mod': f1m,
            'f2_obs': row['f2'], 'f2_mod': f2m,
            'chi2': best['chi2'], 'dof': best['dof'],
            'notes': 'ok'
        })

    out = pd.DataFrame(rows)
    out.to_csv(args.out, index=False)
    print(f"Wrote fit results: {args.out}")
    if args.plots and len(out):
        try:
            import matplotlib.pyplot as plt
            for _,r in out.iterrows():
                fig,ax = plt.subplots(figsize=(4.5,3.2))
                ax.scatter([1,2],[r['f1_obs'], r['f2_obs']], label='obs', marker='o')
                ax.plot([1,2],[r['f1_mod'], r['f2_mod']], label='model', marker='s')
                ax.set_xticks([1,2]); ax.set_xticklabels(['n=1','n=2'])
                ax.set_ylabel('Frequency (Hz)')
                ax.set_title(f"epoch {r['epoch_id']}  χ²={r['chi2']:.2f}")
                ax.legend()
                fig.tight_layout()
                path = os.path.join(args.plots, f"fit_epoch_{r['epoch_id']}.png")
                fig.savefig(path, dpi=150)
                plt.close(fig)
                print(f"Saved plot: {path}")
        except Exception as e:
            print("Plotting failed:", e)

if __name__ == '__main__':
    main()
