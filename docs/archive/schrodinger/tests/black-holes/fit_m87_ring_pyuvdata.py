#!/usr/bin/env python3
"""
Fit M87* ring in the visibility domain using pyuvdata (no eht-imaging required).

Models:
  GR   : |V|(rho) = |J0(2π rho R)| * exp(-(sigma*rho)^2)
  CBL  : GR_model * exp(-alpha * rho), alpha >= 0

Usage:
  python3 fit_m87_ring_pyuvdata.py --fits-glob "/Users/.../e17b06-7-hi-m87-M87.fits/E17B06.[0-3].bin0000.source0000.FITS" --nbins 60

Requires:
  pip install pyuvdata astropy numpy scipy matplotlib
"""

import argparse, glob, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import j0
from pyuvdata import UVData

C = 2.99792458e8
UAS_RAD = 4.848e-12  # 1 μas in radians

def load_rho_amp_from_fitsidi(paths, spw=0, pol=0):
    """
    Load baseline lengths (in wavelengths) and visibility amplitudes from FITS-IDI files.
    Uses the center frequency channel of the given spw.
      paths: list of FITS-IDI filenames
      spw  : spectral window index to use (default 0)
      pol  : polarization index to use (default 0)
    Returns:
      rho_all (wavelengths), amp_all (same units as data amplitude)
    """
    rhos, amps = [], []
    for p in paths:
        uvd = UVData()
        uvd.read_fitsidi(p)  # data_array: (Nblts, Nspws, Nfreqs, Npols)
        # frequency array [Nspws, Nfreqs]
        freq_hz = uvd.freq_array
        if spw >= freq_hz.shape[0]:
            print(f"[WARN] {p}: spw {spw} out of range; skipping.")
            continue
        # pick center frequency channel within spw
        nfreq = freq_hz.shape[1]
        fidx = nfreq // 2
        f = float(freq_hz[spw, fidx])
        lam = C / f

        # select that spw,freq,pol
        # uvw in meters => wavelengths by dividing by lambda
        uvw = uvd.uvw_array  # meters, shape (Nblts, 3)
        u = uvw[:,0] / lam; v = uvw[:,1] / lam
        rho = np.hypot(u, v)

        # extract data & flags
        if uvd.data_array.ndim != 4:
            print(f"[WARN] {p}: unexpected data_array shape {uvd.data_array.shape}; skipping.")
            continue
        if pol >= uvd.data_array.shape[-1]:
            print(f"[WARN] {p}: pol {pol} out of range; skipping.")
            continue

        vis = uvd.data_array[:, spw, fidx, pol]
        flg = uvd.flag_array[:, spw, fidx, pol]
        m = (~flg) & np.isfinite(rho) & np.isfinite(vis.real) & np.isfinite(vis.imag)
        if not np.any(m):
            print(f"[WARN] {p}: no valid points after flagging.")
            continue

        rhos.append(rho[m])
        amps.append(np.abs(vis[m]))

    if not rhos:
        raise RuntimeError("No valid visibilities collected; check paths/spw/pol.")
    return np.concatenate(rhos), np.concatenate(amps)

def az_bin(rho, amp, nbins=60):
    """Azimuthal (radial) binning in log-ρ; returns (ρc, |V|, SE)."""
    rho = np.asarray(rho); amp = np.asarray(amp)
    # robust range
    rmin, rmax = np.percentile(rho, [1, 99.5])
    rmin = max(rmin, 1e3)  # avoid ρ≈0
    edges = np.geomspace(rmin, rmax, nbins+1)
    rc, av, se = [], [], []
    for i in range(nbins):
        m = (rho >= edges[i]) & (rho < edges[i+1])
        if m.sum() < 10:  # need enough points
            continue
        vals = amp[m]
        rc.append(np.sqrt(edges[i]*edges[i+1]))
        av.append(np.mean(vals))
        # standard error of mean
        se.append(np.std(vals, ddof=1) / np.sqrt(vals.size))
    return np.array(rc), np.array(av), np.array(se)

# Visibility-domain models
def V_ring(rho, R, sigma):
    return np.abs(j0(2.0*np.pi*rho*R)) * np.exp(-(sigma*rho)**2)

def V_cbl(rho, R, sigma, alpha):
    return V_ring(rho, R, sigma) * np.exp(-alpha*rho)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fits-glob", required=True, help="glob of FITS-IDI files to load")
    ap.add_argument("--nbins", type=int, default=60, help="number of radial bins")
    ap.add_argument("--spw", type=int, default=0, help="spectral window index to use")
    ap.add_argument("--pol", type=int, default=0, help="polarization index to use")
    args = ap.parse_args()

    paths = sorted(glob.glob(args.fits_glob))
    if not paths:
        raise SystemExit(f"No files matched: {args.fits_glob}")
    print(f"[INFO] loading {len(paths)} FITS-IDI files...")

    rho, amp = load_rho_amp_from_fitsidi(paths, spw=args.spw, pol=args.pol)
    rho_b, amp_b, se_b = az_bin(rho, amp, nbins=args.nbins)
    if rho_b.size < 10:
        raise SystemExit("Not enough binned points; try increasing nbins or adding more files.")

    # Normalize amplitude to the median of first bins (reduce absolute flux sensitivity)
    A0 = np.nanmedian(amp_b[: max(3, rho_b.size//20) ])
    amp_n = amp_b / A0
    se_n  = se_b / A0

    # Initial guesses
    R0    = 20.0 * UAS_RAD   # ~20 μas radius in radians
    sigma0= 1e-11            # width scale in (wavelength)^-1 units
    alpha0= 0.0

    # Fit GR ring
    p_gr, c_gr = curve_fit(V_ring, rho_b, amp_n, p0=[R0, sigma0],
                           sigma=se_n, absolute_sigma=True, maxfev=30000)
    R_gr, sig_gr = p_gr
    model_gr = V_ring(rho_b, *p_gr)
    resid_gr = (amp_n - model_gr) / se_n
    rss_gr = np.sum(resid_gr**2); k_gr = 2
    AIC_gr = 2*k_gr + rss_gr

    # Fit CBL ring
    p_cbl, c_cbl = curve_fit(V_cbl, rho_b, amp_n, p0=[R0, sigma0, alpha0],
                             bounds=([0, 0, 0],[np.inf, np.inf, np.inf]),
                             sigma=se_n, absolute_sigma=True, maxfev=30000)
    R_cbl, sig_cbl, a_cbl = p_cbl
    model_cbl = V_cbl(rho_b, *p_cbl)
    resid_cbl = (amp_n - model_cbl) / se_n
    rss_cbl = np.sum(resid_cbl**2); k_cbl = 3
    AIC_cbl = 2*k_cbl + rss_cbl
    dAIC = AIC_gr - AIC_cbl

    # Report
    print("\n=== VIS RING FIT (pyuvdata) ===")
    print(f"Data points (binned): {rho_b.size}")
    print(f"GR  : R = {R_gr/UAS_RAD:6.2f} μas  (diameter ~ {2*R_gr/UAS_RAD:6.2f} μas),  sigma = {sig_gr:.3e}")
    print(f"CBL : R = {R_cbl/UAS_RAD:6.2f} μas  (diameter ~ {2*R_cbl/UAS_RAD:6.2f} μas),  sigma = {sig_cbl:.3e},  alpha = {a_cbl:.3e}")
    print(f"AIC : GR = {AIC_gr:.1f},  CBL = {AIC_cbl:.1f},  ΔAIC = {dAIC:.1f}  (positive favors CBL)")

    # Plot
    plt.figure(figsize=(8.0,5.2))
    plt.errorbar(rho_b, amp_n, yerr=se_n, fmt='k.', alpha=0.6, label='Data (binned |V|)')
    plt.plot(rho_b, model_gr,  lw=2, color='tab:blue', label='GR ring')
    plt.plot(rho_b, model_cbl, lw=2, ls='--', color='tab:red', label='CBL ring = GR × exp(-αρ)')
    plt.xscale('log'); plt.ylim(0, 1.2*np.nanmax(amp_n))
    plt.xlabel(r"Baseline length $\rho = \sqrt{u^2+v^2}$ (wavelengths)")
    plt.ylabel(r"Normalized $|V|$")
    plt.title("M87* vis amplitudes: GR vs CBL envelope (pyuvdata)")
    plt.legend(); plt.grid(alpha=0.2)
    plt.tight_layout(); plt.savefig("m87_visfit_gr_vs_cbl_pyuv.png", dpi=140)
    print("Saved: m87_visfit_gr_vs_cbl_pyuv.png\n")

if __name__ == "__main__":
    main()

