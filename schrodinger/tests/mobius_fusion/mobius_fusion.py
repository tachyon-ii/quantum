
#!/usr/bin/env python3
"""
mobuis_fusion.py — Capture/transition map for Möbius-loop pairing (postulate demo).

Distorted‑Null & chaos mapping (v2):
- Amplitude/environment knobs:
  --A : internal amplitude (dimensionless)
  --A-thresh : threshold where anti-periodic BC flips to periodic (double cover)
  --hysteresis : fractional hysteresis band around A-thresh (e.g. 0.05 = ±5%)
  --Eext : external field/torque bias (dimensionless, [0,1] typical)

- Grid/basin/chaos with probabilities:
  --grid NX NY : sweep a 2D plane and classify outcomes at each cell
  --cell-trials N : number of micro-encounters per cell (averaged) [NEW]
  --plane {A-b,A-E} : choose plane (Amplitude vs impact) or (Amplitude vs external field)
  --Amin/Amax, --bmin/bmax2, --Emin/Emax : ranges for swept axes
  --basin : PNG basin (argmax label from averaged probabilities)
  --chaos : PNG chaos proxy (boundary sensitivity of labels)
  --prob-photon/--prob-ann/--prob-capsid : optional probability heatmaps [NEW]
  --grid-csv : write CSV with probs and label

Existing:
  * photon-only mode, CSV of samples, simple scatter plots.
License: MIT
"""
import math, random, argparse, csv
from dataclasses import dataclass
from typing import Tuple, List, Optional

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

@dataclass
class Encounter:
    energy: float
    impact: float
    phase: float
    same_helicity: bool
    A: float
    Eext: float
    periodic: bool

@dataclass
class Outcome:
    label: str
    energy: float
    impact: float
    same_helicity: bool
    A: float
    Eext: float
    periodic: bool

def boundary_periodic(A: float, A_thresh: float, hysteresis: float=0.0, prior: Optional[bool]=None) -> bool:
    if A_thresh <= 0:
        return False
    if prior is None or hysteresis <= 0.0:
        return A >= A_thresh
    low = A_thresh*(1.0 - hysteresis)
    high = A_thresh*(1.0 + hysteresis)
    if prior:
        return A >= low
    else:
        return A >= high

def sample_encounter(rng: random.Random, same_helicity: bool, A: float, Eext: float, periodic: bool) -> Encounter:
    E = 10 ** rng.uniform(-2, 2)  # 0.01 .. 100
    b = rng.random()
    phi = rng.random() * 2*math.pi
    return Encounter(E, b, phi, same_helicity, A, Eext, periodic)

def capture_window_probability(enc: Encounter, params) -> Tuple[float, float, float]:
    E, b, phi = enc.energy, enc.impact, enc.phase
    A, Eext, periodic = enc.A, enc.Eext, enc.periodic
    p_cap = 0.0
    p_ann = 0.0
    p_cap_cap = 0.0

    widen = 1.15 if periodic else 1.0
    tighten_capsid = 0.85 if periodic else 1.0

    if enc.same_helicity:
        E0, wE = params["E0"], params["wE"] * (1.0/widen)
        bmax = params["bmax"] * widen
        smax = params["smax"] * (1.0 + 1.0*Eext)
        logE = math.log10(E)
        logE0 = math.log10(E0)
        gateE = math.exp(-0.5 * ((logE - logE0)/wE)**2)
        gateB = 1.0 if b <= bmax else 0.0
        gateP = 1.0 if abs(math.sin(0.5*phi)) <= smax else 0.0
        p_cap = gateE * gateB * gateP

        Ehi, slope = params["Ehi"], params["ann_slope"]
        overlap = max(0.0, (bmax - b)/max(bmax, 1e-9))
        amp_factor = 1.0 + 0.5*A
        p_ann = overlap * max(0.0, (math.log10(E) - math.log10(Ehi)) * slope) * amp_factor
    else:
        E0c, wEc = params["E0c"], params["wEc"]/max(tighten_capsid,1e-9)
        bmaxc = params["bmaxc"] * tighten_capsid
        smaxc = params["smaxc"] * (1.0 - 0.5*Eext)
        logE = math.log10(E)
        logE0 = math.log10(E0c)
        gateE = math.exp(-0.5 * ((logE - logE0)/wEc)**2)
        gateB = 1.0 if b <= bmaxc else 0.0
        gateP = 1.0 if abs(math.sin(0.5*phi)) <= smaxc else 0.0
        p_cap_cap = gateE * gateB * gateP

        Ehi, slope = params["Ehi"], params["ann_slope"]
        overlap = max(0.0, (bmaxc - b)/max(bmaxc, 1e-9))
        amp_factor = 1.0 + 0.5*A
        p_ann = overlap * max(0.0, (math.log10(E) - math.log10(Ehi)) * slope) * amp_factor

    # Clamp
    p_cap = max(0.0, min(1.0, p_cap))
    p_ann = max(0.0, min(1.0, p_ann))
    p_cap_cap = max(0.0, min(1.0, p_cap_cap))
    return p_cap, p_ann, p_cap_cap

def decide_outcome(enc: Encounter, params) -> Outcome:
    p_cap, p_ann, p_cap_cap = capture_window_probability(enc, params)
    r = random.random()
    if enc.same_helicity:
        if r < p_cap:
            label = "photon"
        elif r < p_cap + p_ann:
            label = "annihilation"
        else:
            label = "separate"
    else:
        if r < p_cap_cap:
            label = "capsid"
        elif r < p_cap_cap + p_ann:
            label = "annihilation"
        else:
            label = "separate"
    return Outcome(label, enc.energy, enc.impact, enc.same_helicity, enc.A, enc.Eext, enc.periodic)

def run_sim(N: int, same: bool, opp: bool, photon_only: bool, seed: int, params,
            A: float, A_thresh: float, hysteresis: float, Eext: float) -> List[Outcome]:
    if seed is not None:
        random.seed(seed)
    periodic = boundary_periodic(A, A_thresh, hysteresis, prior=None)
    outcomes: List[Outcome] = []
    def gen(same_h):
        enc = sample_encounter(random, same_h, A, Eext, periodic)
        return decide_outcome(enc, params)

    if photon_only:
        for _ in range(N):
            outcomes.append(gen(True))
        return outcomes

    if same:
        for _ in range(N):
            outcomes.append(gen(True))
    if opp:
        for _ in range(N):
            outcomes.append(gen(False))
    if not same and not opp:
        for _ in range(N):
            outcomes.append(gen(True))
        for _ in range(N):
            outcomes.append(gen(False))
    return outcomes

def save_csv(path: str, outcomes: List[Outcome]):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label","energy","impact","same_helicity","A","Eext","periodic"])
        for o in outcomes:
            w.writerow([o.label, f"{o.energy:.6e}", f"{o.impact:.6f}", int(o.same_helicity),
                        f"{o.A:.4f}", f"{o.Eext:.4f}", int(o.periodic)])

def plot_outcomes(path: str, outcomes: List[Outcome], photon_only: bool, show: bool):
    if plt is None:
        print("matplotlib not available; skipping plot")
        return
    markers = {"photon":"o","capsid":"s","annihilation":"x","separate":"."}
    sizes   = {"photon":16, "capsid":16, "annihilation":22, "separate":2}
    alphas  = {"photon":1.0, "capsid":0.9, "annihilation":1.0, "separate":0.35}

    import math as _m
    plt.figure()
    labels = ["photon", "annihilation", "separate"] if photon_only else ["photon","capsid","annihilation","separate"]
    for label in labels:
        X = [_m.log10(o.energy) for o in outcomes if o.label==label]
        Y = [o.impact for o in outcomes if o.label==label]
        if not X:
            continue
        plt.scatter(X, Y, marker=markers[label], s=sizes[label], alpha=alphas[label], label=label)
    plt.xlabel("log10(relative energy)")
    plt.ylabel("impact parameter")
    plt.legend()
    plt.tight_layout()
    if path:
        plt.savefig(path, dpi=160)
        print(f"Saved plot: {path}")
    if show:
        plt.show()
    else:
        plt.close()

# ---------- Grid / basin / chaos mapping with probabilities ----------

def classify_cell_probs(A: float, B: float, plane: str, params, base_args, trials: int) -> Tuple[float,float,float]:
    """
    Return averaged probabilities (P_photon, P_ann, P_capsid) for a grid cell
    using 'trials' micro-encounters with deterministic RNG per cell.
    (same-helicity encounters only; capsid prob will be ~0 in that case.)
    """
    periodic = boundary_periodic(A, base_args["A_thresh"], base_args["hysteresis"], prior=None)
    rng = random.Random(hash((round(A,6), round(B,6), plane, trials)) & 0xffffffff)
    P_ph = 0.0; P_ann = 0.0; P_cap = 0.0
    for _ in range(max(1,trials)):
        if plane == "A-b":
            Eext = base_args["Eext"]
            impact = min(max(B, 0.0), 1.0)
        else:
            Eext = max(0.0, B)
            impact = rng.random()
        # same-helicity for photon window
        enc = sample_encounter(rng, True, A, Eext, periodic)
        enc.impact = impact
        p_cap, p_ann, _ = capture_window_probability(enc, params)
        P_ph += p_cap
        P_ann += p_ann
        # If we also want capsid probability from opposite helicity at same cell, sample once:
        # do a single opposite-helicity probe per trial to give rough P_capsid
        enc2 = sample_encounter(rng, False, A, Eext, periodic)
        enc2.impact = impact
        _, p_ann2, p_cap2 = capture_window_probability(enc2, params)
        P_cap += p_cap2
    inv = 1.0/max(1,trials)
    return P_ph*inv, P_ann*inv, P_cap*inv

def basin_and_chaos(plane: str, NX: int, NY: int, ranges: dict, params, base_args,
                    out_png_basin: Optional[str], out_png_chaos: Optional[str], out_csv: Optional[str],
                    prob_pngs: dict, cell_trials: int):
    if plt is None and (out_png_basin or out_png_chaos or any(prob_pngs.values())):
        print("matplotlib not available; skipping grid plots")
    xmin, xmax = ranges["Amin"], ranges["Amax"]
    if plane == "A-b":
        ymin, ymax = ranges["bmin"], ranges["bmax"]
    else:
        ymin, ymax = ranges["Emin"], ranges["Emax"]

    # Grids
    Pph = [[0.0 for _ in range(NY)] for __ in range(NX)]
    Pann = [[0.0 for _ in range(NY)] for __ in range(NX)]
    Pcap = [[0.0 for _ in range(NY)] for __ in range(NX)]
    labels = [["" for _ in range(NY)] for __ in range(NX)]
    for ix in range(NX):
        A = xmin + (xmax - xmin)*ix/(NX-1)
        for iy in range(NY):
            B = ymin + (ymax - ymin)*iy/(NY-1)
            ph, ann, cap = classify_cell_probs(A, B, plane, params, base_args, cell_trials)
            Pph[ix][iy], Pann[ix][iy], Pcap[ix][iy] = ph, ann, cap
            # label by argmax of probabilities (capsid only meaningful if you plan to inspect it)
            if ph >= ann and ph >= cap:
                labels[ix][iy] = "photon"
            elif ann >= ph and ann >= cap:
                labels[ix][iy] = "annihilation"
            else:
                labels[ix][iy] = "capsid"  # rarely dominant in same-helicity plane

    # Chaos proxy from labels
    chaos = [[0.0 for _ in range(NY)] for __ in range(NX)]
    for ix in range(NX):
        for iy in range(NY):
            here = labels[ix][iy]
            diffs = 0; neigh = 0
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                jx, jy = ix+dx, iy+dy
                if 0 <= jx < NX and 0 <= jy < NY:
                    neigh += 1
                    if labels[jx][jy] != here:
                        diffs += 1
            chaos[ix][iy] = diffs/max(neigh,1)

    # CSV dump
    if out_csv:
        with open(out_csv, "w", newline="") as f:
            w = csv.writer(f)
            header = ["A", ("impact" if plane=="A-b" else "Eext"), "P_photon", "P_ann", "P_capsid", "label", "chaos_neigh_frac"]
            w.writerow(header)
            for ix in range(NX):
                A = xmin + (xmax - xmin)*ix/(NX-1)
                for iy in range(NY):
                    B = ymin + (ymax - ymin)*iy/(NY-1)
                    w.writerow([f"{A:.6f}", f"{B:.6f}", f"{Pph[ix][iy]:.3f}", f"{Pann[ix][iy]:.3f}", f"{Pcap[ix][iy]:.3f}", labels[ix][iy], f"{chaos[ix][iy]:.3f}"])
        print(f"Wrote grid CSV: {out_csv}")

    # Plot helpers
    def _imshow(Z, xlabel, ylabel, cmap=None, vmin=None, vmax=None, ticks=None, ticklabels=None, path=None, cbar_label=None):
        if plt is None or path is None:
            return
        import numpy as np
        Znp = np.array(Z).T  # transpose so [iy,ix]
        plt.figure()
        plt.imshow(Znp, origin="lower", extent=[xmin,xmax,ymin,ymax], aspect="auto", interpolation="nearest", cmap=cmap, vmin=vmin, vmax=vmax)
        plt.xlabel(xlabel); plt.ylabel(ylabel)
        cb = plt.colorbar()
        if cbar_label:
            cb.set_label(cbar_label)
        if ticks is not None and ticklabels is not None:
            cb.set_ticks(ticks); cb.set_ticklabels(ticklabels)
        plt.tight_layout(); plt.savefig(path, dpi=160); plt.close(); print(f"Saved: {path}")

    # Basin map (labels)
    if out_png_basin:
        # map labels to ints
        lut = {"photon":1, "annihilation":2, "capsid":3}
        Z = [[lut.get(labels[ix][iy], 0) for iy in range(NY)] for ix in range(NX)]
        _imshow(Z, "Amplitude A", "impact b" if plane=="A-b" else "external field Eext",
                ticks=[1,2,3], ticklabels=["photon","annihilation","capsid"], path=out_png_basin, cbar_label="argmax label")

    if out_png_chaos:
        _imshow(chaos, "Amplitude A", "impact b" if plane=="A-b" else "external field Eext",
                vmin=0.0, vmax=1.0, path=out_png_chaos, cbar_label="boundary sensitivity (0–1)")

    # Probability maps
    if prob_pngs.get("photon"):
        _imshow(Pph, "Amplitude A", "impact b" if plane=="A-b" else "external field Eext",
                vmin=0.0, vmax=1.0, path=prob_pngs["photon"], cbar_label="P(photon)")
    if prob_pngs.get("ann"):
        _imshow(Pann, "Amplitude A", "impact b" if plane=="A-b" else "external field Eext",
                vmin=0.0, vmax=1.0, path=prob_pngs["ann"], cbar_label="P(annihilation)")
    if prob_pngs.get("capsid"):
        _imshow(Pcap, "Amplitude A", "impact b" if plane=="A-b" else "external field Eext",
                vmin=0.0, vmax=1.0, path=prob_pngs["capsid"], cbar_label="P(capsid)")

def main():
    ap = argparse.ArgumentParser(description="Capture/transition map for Möbius-loop pairing (photon/capsid windows + distorted-null effects).")
    # Sampling
    ap.add_argument("--N", type=int, default=2000, help="number of encounters per helicity class")
    ap.add_argument("--seed", type=int, default=None, help="random seed")
    # Modes
    ap.add_argument("--same-helicity", action="store_true", help="simulate only same-helicity encounters (photon window)")
    ap.add_argument("--opp-helicity", action="store_true", help="simulate only opposite-helicity encounters (capsid window)")
    ap.add_argument("--photon-only", action="store_true", help="simulate only same-helicity encounters and hide capsid in plots")
    # Output
    ap.add_argument("--csv", type=str, default=None, help="write outcomes CSV to PATH")
    ap.add_argument("--plot", type=str, default=None, help="save a scatter PNG to PATH")
    ap.add_argument("--no-show", action="store_true", help="do not display the plot window (default is to display when --plot is set)")
    # Window parameters
    ap.add_argument("--E0", type=float, default=1.0, help="centre of photon capture window (dimensionless energy)")
    ap.add_argument("--wE", type=float, default=0.35, help="log-space width of photon capture window")
    ap.add_argument("--bmax", type=float, default=0.25, help="max impact parameter for photon capture")
    ap.add_argument("--smax", type=float, default=0.35, help="phase gate for photon capture, |sin(phi/2)| <= smax")
    ap.add_argument("--Ehi", type=float, default=5.0, help="energy where annihilation starts to rise")
    ap.add_argument("--ann-slope", type=float, default=0.5, help="slope of annihilation probability in logE beyond Ehi")
    # Capsid window
    ap.add_argument("--E0c", type=float, default=0.8, help="centre of capsid window")
    ap.add_argument("--wEc", type=float, default=0.25, help="log-space width of capsid window")
    ap.add_argument("--bmaxc", type=float, default=0.18, help="max impact for capsid capture")
    ap.add_argument("--smaxc", type=float, default=0.25, help="phase gate for capsid")
    # Distorted-null knobs
    ap.add_argument("--A", type=float, default=0.0, help="internal amplitude (dimensionless)")
    ap.add_argument("--A-thresh", type=float, default=0.0, help="threshold where BC flips to periodic (double cover)")
    ap.add_argument("--hysteresis", type=float, default=0.0, help="fractional hysteresis band around A-thresh (e.g. 0.05 = ±5%)")
    ap.add_argument("--Eext", type=float, default=0.0, help="external field/torque bias (dimensionless)")
    # Grid / basin / chaos
    ap.add_argument("--grid", nargs=2, type=int, metavar=("NX","NY"), help="sweep a 2D plane and classify outcomes")
    ap.add_argument("--cell-trials", type=int, default=50, help="micro-encounters per cell for probability averaging")
    ap.add_argument("--plane", choices=["A-b","A-E"], default="A-b", help="grid plane: A-b (amplitude vs impact) or A-E (amplitude vs external field)")
    ap.add_argument("--Amin", type=float, default=0.0, help="min amplitude for grid")
    ap.add_argument("--Amax", type=float, default=1.0, help="max amplitude for grid")
    ap.add_argument("--bmin", type=float, default=0.0, help="min impact for grid (A-b plane)")
    ap.add_argument("--bmax2", type=float, default=1.0, help="max impact for grid (A-b plane)")
    ap.add_argument("--Emin", type=float, default=0.0, help="min external field for grid (A-E plane)")
    ap.add_argument("--Emax", type=float, default=1.0, help="max external field for grid (A-E plane)")
    ap.add_argument("--basin", type=str, help="PNG path for basin map")
    ap.add_argument("--chaos", type=str, help="PNG path for chaos heatmap")
    ap.add_argument("--prob-photon", type=str, help="PNG for P(photon)")
    ap.add_argument("--prob-ann", type=str, help="PNG for P(annihilation)")
    ap.add_argument("--prob-capsid", type=str, help="PNG for P(capsid)")
    ap.add_argument("--grid-csv", type=str, help="CSV path for grid classifications")

    args = ap.parse_args()

    params = dict(E0=args.E0, wE=args.wE, bmax=args.bmax, smax=args.smax,
                  Ehi=args.Ehi, ann_slope=args.ann_slope,
                  E0c=args.E0c, wEc=args.wEc, bmaxc=args.bmaxc, smaxc=args.smaxc)

    base_args = dict(A_thresh=args.A_thresh, hysteresis=args.hysteresis, Eext=args.Eext)

    if args.grid:
        NX, NY = args.grid
        ranges = dict(Amin=args.Amin, Amax=args.Amax, bmin=args.bmin, bmax=args.bmax2, Emin=args.Emin, Emax=args.Emax)
        prob_pngs = dict(photon=args.prob_photon, ann=args.prob_ann, capsid=args.prob_capsid)
        basin_and_chaos(args.plane, NX, NY, ranges, params, base_args,
                        args.basin, args.chaos, args.grid_csv, prob_pngs, args.cell_trials)
        return

    # Monte Carlo sample mode
    outcomes = run_sim(args.N, args.same_helicity, args.opp_helicity, args.photon_only, args.seed, params,
                       A=args.A, A_thresh=args.A_thresh, hysteresis=args.hysteresis, Eext=args.Eext)

    if args.csv:
        save_csv(args.csv, outcomes)
        print(f"Wrote CSV: {args.csv}")

    if args.plot:
        plot_outcomes(args.plot, outcomes, photon_only=args.photon_only, show=(not args.no_show))

    from collections import Counter
    counts = Counter(o.label for o in outcomes)
    total = sum(counts.values())
    print("Summary:")
    order = ["photon", "annihilation", "separate"] if args.photon_only else ["photon","capsid","annihilation","separate"]
    for k in order:
        if counts.get(k,0):
            print(f"  {k:12s}: {counts[k]:6d}  ({counts[k]/total:5.1%})")

if __name__ == "__main__":
    main()
