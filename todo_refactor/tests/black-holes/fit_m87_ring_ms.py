#!/usr/bin/env python3
"""
Visibility-domain GR vs CBL ring fit from CASA MS (no UVFITS, no eht-imaging).

Models:
  GR  : |V|(ρ) = |J0(2π ρ R)| * exp(-(σ ρ)^2)
  CBL : GR(ρ) * exp(-α ρ), α >= 0  (achromatic envelope)

Improvements:
  • Averages ±avg_chans channels around the center (boosts S/N & sample count)
  • Optionally combines both pols (if present)
  • Robust binning (MAD/√N) + fractional error floor
  • Bounded, robust least_squares (soft_l1) to avoid degenerate minima

Usage:
  python fit_m87_ring_ms.py --ms-glob "ms_hi_e17b06/*.ms" \
      --nbins 240 --spw 0 --pol 0 --avg-chans 16 --combine-pols \
      --crop 2 98 --err-floor 0.02
"""

import argparse, glob, os, numpy as np, matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.special import j0
from numpy.linalg import inv, LinAlgError
from casatools import ms as casams

C = 2.99792458e8                # m/s
UAS_RAD = 4.848e-12             # 1 μas in radians

# --------------------------- MS -> (rho, |V|) ---------------------------

def load_ms_rho_amp(ms_path: str, spw: int = 0, pol: int = 0,
                    avg_chans: int = 16, combine_pols: bool = False):
    """
    Load baseline length (in wavelengths) and |V| from a CASA MS.
    Averages ±avg_chans around the center channel of SPW 'spw'.
    If combine_pols=True and two pols exist, averages amplitudes over pol=0,1.

    Returns:
        rho_all (1D), amp_all (1D)
    """
    m = casams()
    m.open(ms_path)
    m.msselect({'spw': str(spw)})
    data = m.getdata(['data', 'flag', 'uvw', 'axis_info'])
    m.close()

    vis = data['data']      # [npol, nchan, nrow]
    flg = data['flag']      # [npol, nchan, nrow]
    uvw = data['uvw']       # [3, nrow], meters
    freq_axis = data['axis_info']['freq_axis']
    chan_freq = freq_axis['chan_freq']   # [nchan] or [nchan, nrow]

    npol, nchan, nrow = vis.shape
    # center channel window
    if chan_freq.ndim == 1:
        cidx = nchan // 2
        lo = max(0, cidx - avg_chans)
        hi = min(nchan, cidx + avg_chans + 1)
        chans = np.arange(lo, hi)
        amp_list, rho_list = [], []
        for ch in chans:
            f = float(chan_freq[ch])
            lam = C / f
            rho = np.hypot(uvw[0], uvw[1]) / lam
            if combine_pols and npol >= 2:
                vis_ch = vis[0, ch, :] + vis[1, ch, :]
                amp_ch = 0.5*np.abs(vis_ch)
                msk = (~flg[0, ch, :]) & (~flg[1, ch, :])
            else:
                vis_ch = vis[min(pol, npol-1), ch, :]
                amp_ch = np.abs(vis_ch)
                msk = ~flg[min(pol, npol-1), ch, :]
            good = msk & np.isfinite(rho) & np.isfinite(amp_ch)
            if np.any(good):
                rho_list.append(rho[good]); amp_list.append(amp_ch[good])
        if not rho_list: return np.array([]), np.array([])
        return np.concatenate(rho_list), np.concatenate(amp_list)

    else:
        # per-row frequencies
        cidx = nchan // 2
        lo = max(0, cidx - avg_chans)
        hi = min(nchan, cidx + avg_chans + 1)
        chans = np.arange(lo, hi)
        amp_list, rho_list = [], []
        for ch in chans:
            frow = chan_freq[ch, :]             # Hz per row
            rho  = np.hypot(uvw[0], uvw[1]) * (frow / C)
            if combine_pols and npol >= 2:
                vis_ch = vis[0, ch, :] + vis[1, ch, :]
                amp_ch = 0.5*np.abs(vis_ch)
                msk = (~flg[0, ch, :]) & (~flg[1, ch, :])
            else:
                vis_ch = vis[min(pol, npol-1), ch, :]
                amp_ch = np.abs(vis_ch)
                msk = ~flg[min(pol, npol-1), ch, :]
            good = msk & np.isfinite(rho) & np.isfinite(amp_ch)
            if np.any(good):
                rho_list.append(rho[good]); amp_list.append(amp_ch[good])
        if not rho_list: return np.array([]), np.array([])
        return np.concatenate(rho_list), np.concatenate(amp_list)

# --------------------------- Binning & errors ---------------------------

def az_bin(rho, amp, nbins=240, min_per_bin=5):
    """
    Bin |V| vs ρ on a log-ρ grid; return (ρ_center, mean |V|, SE).
    SE uses MAD/√N (robust); falls back to std/√N if needed.
    """
    rho = np.asarray(rho); amp = np.asarray(amp)
    rmin, rmax = np.percentile(rho, [1, 99.5])
    rmin = max(rmin, 1e3)
    edges = np.geomspace(rmin, rmax, nbins + 1)

    rc, av, se = [], [], []
    for i in range(nbins):
        m = (rho >= edges[i]) & (rho < edges[i+1])
        if m.sum() < min_per_bin:
            continue
        vals = amp[m]
        rc.append(np.sqrt(edges[i] * edges[i+1]))
        av.append(np.mean(vals))
        mad = np.median(np.abs(vals - np.median(vals)))
        se_i = 1.4826 * mad / np.sqrt(vals.size)
        if not np.isfinite(se_i) or se_i == 0:
            se_i = np.std(vals, ddof=1) / np.sqrt(vals.size)
        se.append(se_i)
    return np.array(rc), np.array(av), np.array(se)

# --------------------------- Models & helpers ---------------------------

def V_ring(rho, R, sigma):
    return np.abs(j0(2.0 * np.pi * rho * R)) * np.exp(-(sigma * rho)**2)

def V_cbl(rho, R, sigma, alpha):
    return V_ring(rho, R, sigma) * np.exp(-alpha * rho)

def aic_from_rss(rss, k):  # Gaussian
    return 2.0 * k + rss

def cov_from_jac(ls_result, rss, dof):
    try:
        J = ls_result.jac
        JTJ = J.T @ J
        s2 = rss / max(dof, 1)
        cov = s2 * np.linalg.inv(JTJ)
        return np.sqrt(np.clip(np.diag(cov), 0, np.inf))
    except LinAlgError:
        return None

# --------------------------- Main pipeline ---------------------------

def main():
    ap = argparse.ArgumentParser(description="Visibility-domain GR vs CBL ring fit (MS)")
    ap.add_argument("--ms-glob", required=True, help="glob of MS directories")
    ap.add_argument("--nbins", type=int, default=240)
    ap.add_argument("--spw", type=int, default=0)
    ap.add_argument("--pol", type=int, default=0)
    ap.add_argument("--avg-chans", type=int, default=16, help="±channels around center to average")
    ap.add_argument("--combine-pols", action="store_true", help="average pol=0,1 if present")
    ap.add_argument("--crop", type=float, nargs=2, default=[2, 98], help="percentile crop on ρ (lo hi)")
    ap.add_argument("--err-floor", type=float, default=0.02, help="fractional error floor")
    args = ap.parse_args()

    paths = sorted(glob.glob(args.ms_glob))
    if not paths:
        raise SystemExit(f"No MS matched: {args.ms_glob}")
    print(f"[INFO] loading {len(paths)} MS…")

    # Accumulate across MS files
    all_rho, all_amp = [], []
    for p in paths:
        r, a = load_ms_rho_amp(p, spw=args.spw, pol=args.pol,
                               avg_chans=args.avg_chans, combine_pols=args.combine_pols)
        if r.size:
            all_rho.append(r); all_amp.append(a)
    if not all_rho:
        raise SystemExit("No valid visibilities collected; try different SPW/POL or avg_chans.")

    rho = np.concatenate(all_rho); amp = np.concatenate(all_amp)

    # Bin
    rho_b, amp_b, se_b = az_bin(rho, amp, nbins=args.nbins, min_per_bin=5)
    if rho_b.size < 30:
        print(f"[WARN] only {rho_b.size} binned points; consider more scans or fewer bins")

    # Normalize and error floor
    outer_n = max(3, rho_b.size // 20)
    A0 = np.nanmedian(amp_b[:outer_n])
    y  = amp_b / A0
    ey = se_b  / A0
    ey = np.maximum(ey, args.err_floor * np.nanmax(y))

    # Crop to informative ρ window
    lo_p, hi_p = args.crop
    lo, hi = np.percentile(rho_b, [lo_p, hi_p])
    m = (rho_b >= lo) & (rho_b <= hi)
    rho_b, y, ey = rho_b[m], y[m], ey[m]

    # ------------------ bounded, robust LS fits ------------------

    # Physical bounds
    R_LO, R_HI = 8.0*UAS_RAD, 35.0*UAS_RAD        # ~16–70 μas diameter
    S_LO, S_HI = 5e-12, 5e-10                     # finite width
    A_LO, A_HI = 0.0, 1e-6                        # envelope ≥ 0

    # Initial guesses
    R0, sig0, a0 = 21.0*UAS_RAD, 3e-11, 0.0

    def resid_gr(p):      # [R, σ]
        return (y - V_ring(rho_b, p[0], p[1])) / ey

    def resid_cbl(p):     # [R, σ, α]
        return (y - V_cbl(rho_b, p[0], p[1], p[2])) / ey

    ls_gr = least_squares(resid_gr, x0=[R0, sig0],
                          bounds=([R_LO, S_LO], [R_HI, S_HI]),
                          loss='soft_l1', f_scale=0.03, max_nfev=100000)
    R_gr, sg_gr = ls_gr.x
    y_gr = V_ring(rho_b, R_gr, sg_gr)
    rss_gr = np.sum(((y - y_gr) / ey)**2); k_gr = 2
    AIC_gr = aic_from_rss(rss_gr, k_gr)
    err_gr = cov_from_jac(ls_gr, rss_gr, dof=max(y.size - k_gr, 1))
    dR_gr, dS_gr = (err_gr if err_gr is not None else (np.nan, np.nan))

    ls_cb = least_squares(resid_cbl, x0=[R0, sig0, a0],
                          bounds=([R_LO, S_LO, A_LO], [R_HI, S_HI, A_HI]),
                          loss='soft_l1', f_scale=0.03, max_nfev=100000)
    R_cb, sg_cb, a_cb = ls_cb.x
    y_cb = V_cbl(rho_b, R_cb, sg_cb, a_cb)
    rss_cb = np.sum(((y - y_cb) / ey)**2); k_cb = 3
    AIC_cb = aic_from_rss(rss_cb, k_cb)
    dAIC   = AIC_gr - AIC_cb
    err_cb = cov_from_jac(ls_cb, rss_cb, dof=max(y.size - k_cb, 1))
    if err_cb is not None:
        dR_cb, dS_cb, dA_cb = err_cb
    else:
        dR_cb = dS_cb = dA_cb = np.nan

    # ------------------ report ------------------

    print("\n=== VIS RING FIT (from MS) ===")
    print(f"Binned points: {rho_b.size}")
    print(f"GR  : R = {R_gr/UAS_RAD:6.2f} ± {dR_gr/UAS_RAD if np.isfinite(dR_gr) else np.nan:5.2f} μas"
          f"  (diam ~ {2*R_gr/UAS_RAD:6.2f} μas)"
          f",  sigma = {sg_gr:.3e} ± {dS_gr:.1e}")
    print(f"CBL : R = {R_cb/UAS_RAD:6.2f} ± {dR_cb/UAS_RAD if np.isfinite(dR_cb) else np.nan:5.2f} μas"
          f"  (diam ~ {2*R_cb/UAS_RAD:6.2f} μas)"
          f",  sigma = {sg_cb:.3e} ± {dS_cb:.1e}"
          f",  alpha = {a_cb:.3e} ± {dA_cb:.1e}")
    print(f"AIC : GR = {AIC_gr:.1f},  CBL = {AIC_cb:.1f},  ΔAIC = {dAIC:.1f}  (positive favors CBL)")

    # ------------------ plot ------------------

    plt.figure(figsize=(8.0, 5.2))
    plt.errorbar(rho_b, y, yerr=ey, fmt='k.', alpha=0.6, label='Data (binned |V|)')
    plt.plot(rho_b, y_gr, lw=2, color='tab:blue', label='GR ring')
    plt.plot(rho_b, y_cb, lw=2, ls='--', color='tab:red', label='CBL = GR × exp(-αρ)')
    plt.xscale('log'); plt.ylim(0, 1.2*np.nanmax(y))
    plt.xlabel(r"Baseline length $\rho$ (wavelengths)")
    plt.ylabel(r"Normalized $|V|$")
    plt.title("M87* vis amplitudes: GR vs CBL (from MS)")
    plt.legend(); plt.grid(alpha=0.2)
    plt.tight_layout(); plt.savefig("m87_visfit_gr_vs_cbl_ms.png", dpi=140)
    print("Saved: m87_visfit_gr_vs_cbl_ms.png\n")

if __name__ == "__main__":
    main()

