#!/usr/bin/env python3
# compute_closure_ms_streaming.py
# Stream rows from an MS in chunks; build per-(scan, spw, timebin) *phase* and *amplitude* accumulators
# per baseline; then compute CP/LCA and flush. Uses casatools (bundled with CASA), not python-casacore.

import argparse, os, glob, math, cmath, itertools
import numpy as np
import pandas as pd
from collections import defaultdict
from casatools import table as tbtool

# ---------- helpers ----------

def unique_tris(ants):
    ants = sorted(ants)
    return [(a, b, c) for a, b, c in itertools.combinations(ants, 3)]

def unique_quads(ants):
    ants = sorted(ants)
    return [(a, b, c, d) for a, b, c, d in itertools.combinations(ants, 4)]

def chan_avg(v, f, w=None):
    """
    v: (npol, nchan) complex
    f: (npol, nchan) bool
    w: (npol, nchan) float or None
    Returns:
      vavg  (npol complex)  - weighted complex average
      wsum  (npol float)    - effective weight
      aavg  (npol float)    - weighted amplitude average
      pavg  (npol complex)  - weighted *unit phasor* average (phase-only)
    """
    good = ~f
    if w is None:
        ww = good.astype(float)
    else:
        ww = w * good.astype(float)

    # complex vis weighted average
    wsum = ww.sum(axis=1) + 1e-12
    vavg = (v * ww).sum(axis=1) / wsum

    # amplitude weighted average
    a = np.abs(v)
    aavg = (a * ww).sum(axis=1) / wsum

    # unit phasor per channel (avoid /0)
    ph = v / np.maximum(a, 1e-20)
    pavg = (ph * ww).sum(axis=1) / wsum  # complex unit-ish (phasor mean)

    return vavg, wsum, aavg, pavg

def fetch_oriented_complex(a, b, store, conj_ok=True):
    """
    Fetch complex vector per-pol for baseline (a,b) from a dict keyed by (min,max).
    If reversed, optionally conjugate.
    Returns (vec or None)
    """
    if a <= b:
        bl = (a, b); conj = False
    else:
        bl = (b, a); conj = True
    if bl not in store:
        return None
    vec = store[bl]
    if conj and conj_ok:
        vec = np.conjugate(vec)
    return vec

def fetch_oriented_real(a, b, store):
    """
    Fetch real (per-pol) vector (e.g., amplitudes) from dict keyed by (min,max).
    Orientation does not change amplitudes.
    """
    if a <= b: bl = (a, b)
    else:      bl = (b, a)
    return store.get(bl, None)

# ---------- CP / LCA from averaged phasors & amplitudes ----------

def cp_for_triangle(i, j, k, phasor_by_bl, w_by_bl):
    """
    Use phase-only averaged phasors per baseline to compute closure phase.
    phasor_by_bl[(i,j)] is (npol complex phasor mean)
    w_by_bl[(i,j)]      is (npol float weight)
    Returns (cp_deg, wsum)
    """
    V12 = fetch_oriented_complex(i, j, phasor_by_bl, conj_ok=True)
    V23 = fetch_oriented_complex(j, k, phasor_by_bl, conj_ok=True)
    V31 = fetch_oriented_complex(k, i, phasor_by_bl, conj_ok=True)
    if any(x is None for x in (V12, V23, V31)):
        return None, 0.0

    W12 = fetch_oriented_real(i, j, w_by_bl)
    W23 = fetch_oriented_real(j, k, w_by_bl)
    W31 = fetch_oriented_real(k, i, w_by_bl)
    if any(x is None for x in (W12, W23, W31)):
        return None, 0.0

    Tsum = 0.0 + 0.0j
    wsum = 0.0
    npol = len(V12)
    for pol in range(npol):
        # triple product of *phasors* (unit-ish complex)
        T = V12[pol] * V23[pol] * V31[pol]
        # geometric mean weight
        w = (W12[pol] * W23[pol] * W31[pol]) ** (1.0 / 3.0)
        Tsum += w * T
        wsum += w
    if wsum <= 0:
        return None, 0.0
    return math.degrees(cmath.phase(Tsum / wsum)), wsum

def lca_for_quad(i, j, k, l, amp_by_bl, w_by_bl):
    """
    LCA using *amplitude* means per baseline.
    We try two standard pairings and use the first valid:
      (i,j)(k,l) / (i,k)(j,l)
      (i,k)(j,l) / (i,l)(j,k)
    Returns (lca, wsum) or (None,0).
    """
    def try_pairing(legs):
        (a,b),(c,d),(e,f),(g,h) = legs
        Aab = fetch_oriented_real(a,b,amp_by_bl)
        Acd = fetch_oriented_real(c,d,amp_by_bl)
        Aef = fetch_oriented_real(e,f,amp_by_bl)
        Agh = fetch_oriented_real(g,h,amp_by_bl)
        if any(x is None for x in (Aab,Acd,Aef,Agh)):
            return None, 0.0

        Wab = fetch_oriented_real(a,b,w_by_bl)
        Wcd = fetch_oriented_real(c,d,w_by_bl)
        Wef = fetch_oriented_real(e,f,w_by_bl)
        Wgh = fetch_oriented_real(g,h,w_by_bl)
        if any(x is None for x in (Wab,Wcd,Wef,Wgh)):
            return None, 0.0

        num = 0.0; wsum = 0.0
        npol = len(Aab)
        for pol in range(npol):
            n = (Aab[pol]) * (Acd[pol])
            d = (Aef[pol]) * (Agh[pol])
            if n <= 0 or d <= 0:
                continue
            val = math.log(n / d)
            w = (Wab[pol] * Wcd[pol] * Wef[pol] * Wgh[pol]) ** 0.25
            num += w * val
            wsum += w
        if wsum <= 0:
            return None, 0.0
        return num / wsum, wsum

    # two candidate pairings
    out = try_pairing(((i,j),(k,l),(i,k),(j,l)))
    if out[0] is not None:
        return out
    return try_pairing(((i,k),(j,l),(i,l),(j,k)))

# ---------- flush per-bin ----------

def flush_bin(msname, scan, spw, tbin_mid, accum, rows_cp, rows_lca):
    """
    accum: dict[(min(i,j), max(i,j))] -> [sum_w_phasor(npol complex), sum_w_amp(npol float), sum_w(npol float)]
       where:
         sum_w_phasor stores *weighted sum of per-channel unit phasors*
         sum_w_amp    stores *weighted sum of amplitudes*
         sum_w        stores total weights per pol
    Convert to means, then compute CP/LCA and push rows.
    """
    if not accum:
        return

    ants_present = set()

    # Build per-baseline means
    phasor_by_bl = {}
    amp_by_bl    = {}
    w_by_bl      = {}

    for (i, j), (sum_p, sum_a, sum_w) in accum.items():
        ants_present.add(i); ants_present.add(j)
        # averaged phasor (complex), averaged amplitude (real), and weights
        pmean = sum_p / (sum_w + 1e-12)
        amean = sum_a / (sum_w + 1e-12)
        phasor_by_bl[(i,j)] = pmean
        amp_by_bl[(i,j)]    = amean
        w_by_bl[(i,j)]      = sum_w

    # Triangles → CP
    for (i, j, k) in unique_tris(ants_present):
        cp_deg, w = cp_for_triangle(i, j, k, phasor_by_bl, w_by_bl)
        if cp_deg is None:
            continue
        rows_cp.append(dict(ms=msname, scan=scan, spw=spw,
                            tbin_mid=tbin_mid, ant_i=i, ant_j=j, ant_k=k,
                            cp_deg=cp_deg, w=w))

    # Quads → LCA
    for (i, j, k, l) in unique_quads(ants_present):
        lca, w = lca_for_quad(i, j, k, l, amp_by_bl, w_by_bl)
        if lca is None:
            continue
        rows_lca.append(dict(ms=msname, scan=scan, spw=spw,
                             tbin_mid=tbin_mid, ant_i=i, ant_j=j, ant_k=k, ant_l=l,
                             lca=lca, w=w))

# ---------- driver ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ms-glob', required=True)
    ap.add_argument('--timebin', default='10s')        # e.g., 10s, 30s
    ap.add_argument('--out', default='closure_out')
    ap.add_argument('--chunk', type=int, default=200000, help='row chunk size')
    ap.add_argument('--spw', type=int, default=None,   help='optional spw filter')
    ap.add_argument('--log-every', type=int, default=100000)
    ap.add_argument('--parquet-only', action='store_true', help='skip CSV to save disk')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    binsec = int(args.timebin.rstrip('s'))

    for ms in sorted(glob.glob(args.ms_glob)):
        msname = os.path.basename(ms)
        print(f'[MS] {msname}')
        rows_cp, rows_lca = [], []

        # open main table
        tb = tbtool(); tb.open(ms)
        nrows = tb.nrows(); colnames = tb.colnames()

        # DATA_DESCRIPTION -> SPW mapping
        tbdd = tbtool(); tbdd.open(ms + '/DATA_DESCRIPTION')
        dd_spw = tbdd.getcol('SPECTRAL_WINDOW_ID'); tbdd.close()

        # Discover unique scans by streaming SCAN_NUMBER
        scans_set = set()
        start_scan = 0
        ch_scans = 500_000
        while start_scan < nrows:
            nr = min(ch_scans, nrows - start_scan)
            scans_chunk = tb.getcol('SCAN_NUMBER', start_scan, nr)
            scans_set.update(scans_chunk.tolist())
            start_scan += nr
        scans = sorted(scans_set)

        # Iterate per scan
        for sc in scans:
            if args.spw is None:
                sub = tb.query(f'SCAN_NUMBER=={sc}')
            else:
                ddids = np.where(dd_spw == args.spw)[0]
                if ddids.size == 0:
                    continue
                ddlist = ','.join(str(int(x)) for x in ddids.tolist())
                sub = tb.query(f'SCAN_NUMBER=={sc} && DATA_DESC_ID in [{ddlist}]')

            if sub.nrows() == 0:
                sub.close(); continue

            accum_bins = defaultdict(dict)   # key=(spw,tbin) -> { (i,j): [sum_p, sum_a, sum_w] }
            t0_map = {}                      # (spw) -> first time in this scan (for bin mid calc)
            processed = 0
            start = 0
            ch = args.chunk

            while start < sub.nrows():
                nr  = min(ch, sub.nrows() - start)
                a1  = sub.getcol('ANTENNA1',      start, nr)
                a2  = sub.getcol('ANTENNA2',      start, nr)
                tim = sub.getcol('TIME',          start, nr)
                dd  = sub.getcol('DATA_DESC_ID',  start, nr)
                # Row axis last for arrays
                dat = sub.getcol('DATA',          start, nr)  # (npol, nchan, nr)
                flg = sub.getcol('FLAG',          start, nr)  # (npol, nchan, nr)
                wt  = sub.getcol('WEIGHT',        start, nr) if 'WEIGHT' in colnames else None

                for r in range(nr):
                    spw_val = int(dd_spw[int(dd[r])])
                    if args.spw is not None and spw_val != args.spw:
                        continue

                    # origin per (spw) inside this scan
                    if spw_val not in t0_map:
                        t0_map[spw_val] = float(tim[r])

                    # time bin index
                    t0 = t0_map[spw_val]
                    tbin_idx = int(((float(tim[r]) - t0) * 86400.0) // binsec)

                    # row cells
                    v_cell = dat[:, :, r]
                    f_cell = flg[:, :, r]

                    if wt is None:
                        w_cell = None
                    else:
                        if   wt.ndim == 3:
                            w_cell = wt[:, :, r]
                        elif wt.ndim == 2:
                            w_cell = np.repeat(wt[:, r][:, None], v_cell.shape[1], axis=1)
                        elif wt.ndim == 1:
                            w_cell = np.repeat(wt[:, None], v_cell.shape[1], axis=1)
                        else:
                            w_cell = None

                    # averages for this row
                    _, wsum, aavg, pavg = chan_avg(v_cell, f_cell, w_cell)  # complex avg not needed here

                    # baseline key (sorted) + orientation
                    i = int(a1[r]); j = int(a2[r])
                    if i <= j:
                        bl_key = (i, j)
                        pstore = pavg
                    else:
                        bl_key = (j, i)
                        pstore = np.conjugate(pavg)   # orientation: V_ji -> conj(V_ij)

                    # accumulate into bin
                    key = (spw_val, tbin_idx)
                    bucket = accum_bins[key].get(bl_key)
                    if bucket is None:
                        # [sum_p (complex npol), sum_a (real npol), sum_w (real npol)]
                        accum_bins[key][bl_key] = [pstore.copy(), aavg.copy(), wsum.copy()]
                    else:
                        bucket[0] += pstore
                        bucket[1] += aavg
                        bucket[2] += wsum

                    processed += 1
                    if (processed % args.log_every) == 0:
                        print(f'  [scan {sc}] rows={processed}/{sub.nrows()} bins={len(accum_bins)}')

                start += nr

            # Flush all bins for this scan
            for (spw_val, tbin_idx), blmap in accum_bins.items():
                t0 = t0_map[spw_val]
                tbin_mid = float(t0 + ((tbin_idx + 0.5) * binsec) / 86400.0)
                flush_bin(msname, sc, spw_val, tbin_mid, blmap, rows_cp, rows_lca)

            sub.close()
            print(f'  [scan {sc}] done: CP+LCA bins={len(rows_cp)+len(rows_lca)}')

        tb.close()

        # Write once per MS
        base = os.path.join(args.out, os.path.basename(ms).replace('.ms', ''))
        dfcp  = pd.DataFrame(rows_cp)
        dflca = pd.DataFrame(rows_lca)

        dfcp.to_parquet(base + '_cp.parquet')
        dflca.to_parquet(base + '_lca.parquet')
        if not args.parquet_only:
            dfcp.to_csv(base + '_cp.csv',   index=False)
            dflca.to_csv(base + '_lca.csv', index=False)

        print(f'[DONE] {msname}: CP rows={len(dfcp)}  LCA rows={len(dflca)} → {args.out}')

if __name__ == '__main__':
    main()

