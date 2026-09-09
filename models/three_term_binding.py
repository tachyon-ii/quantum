#!/usr/bin/env python3
"""
three_term_binding.py — the three-ratio forward model (James, 2026-09-08; rebuilt
by Grace .ghost 2026-09-08 after the least-squares/enumeration version was binned
as Standard-Model-anchored fitting).

The honest construction, no fudge:

    BE = s·Y(c′,n)  +  area·P  −  PP·U_pp

  s      slingshot count per assembly (James: D 1, T 3, He3 3, He4 4)
  Y      per-lepton slingshot ΔE = m_e c²[γ(c′) − γ(c′/n)], n = lane length (2,3,3,4).
         ONE free scale: c′, a fraction of c. Tabulated, not fitted.
  area   contact area in SQUARE UNITS, from geometry, THREE RATIOS:
             circ : square : hex  =  π/4 : 1 : 2.598      (circle in a unit square;
         regular hexagon (3√3/2)s²). D/T/He3 touch as balloons → round patches (circ
         each). He4 is PACKED (Kelvin cells, 100%): its faces are whole — 2 squares
         + 4 hexes. Packing is the cliff.
  P      one energy per square-unit of contact.
  U_pp   Coulomb, α ħc / 2R_p, COMPUTED. PP = proton–proton contacts.

Calibration is ONE datum + one posit: D = 2.2246 split (James's start 50:50) fixes
Y and P. Everything else is a prediction. There is no least-squares anywhere in
this file, by design — a fit on 4 points with 3 constants is not a test (that was
the old T4/T7/T8/T10; deleted).

Run:  python3 models/three_term_binding.py
"""
import math

# ── data (AME2020, MeV) ─────────────────────────────────────────────────────────
B = {"H": 0.0, "D": 2.2246, "T": 8.4818, "He3": 7.7180, "He4": 28.2957}

# ── constants ───────────────────────────────────────────────────────────────────
ME, MP = 0.51100, 938.272          # MeV
ALPHA_HBARC = 1.43996              # e²/4πε₀, MeV·fm
RP = 0.8409                        # fm, proton charge radius
U_PP = ALPHA_HBARC / (2 * RP)      # two proton cores in contact, COMPUTED

# ── geometry: the three ratios, computed once ─────────────────────────────────────
CIRC = math.pi / 4                 # 0.7854 — circle inscribed in a unit square
SQUARE = 1.0
HEX = 3 * math.sqrt(3) / 2         # 2.5981 — regular hexagon, side 1

# per assembly: slingshot count s, lane length n, round-patch count, whole-face
# area (squares+hexes, He4 only), PP.  D/T/He3 touch as balloons (round patches);
# He4 is packed → whole faces. area = round_count·circ + whole_area.
PLAYERS = {
    #        s   n   round_patches   whole_area            PP
    "D":   (1,  2,  1,               0.0,                  0),
    "T":   (3,  3,  3,               0.0,                  0),
    "He3": (3,  3,  3,               0.0,                  1),
    "He4": (4,  4,  0,               2 * SQUARE + 4 * HEX, 1),
}
ORDER = ["D", "T", "He3", "He4"]

def gamma(beta):        return 1.0 / math.sqrt(1.0 - beta * beta)
def Y(cp, n):           return ME * (gamma(cp) - gamma(cp / n))   # per lepton, MeV

def predict(cp, P, circ):
    """circ = area of ONE round contact patch (square units). He4's faces are whole."""
    out = {}
    for k in ORDER:
        s, n, rp, whole, PP = PLAYERS[k]
        area = rp * circ + whole
        out[k] = s * Y(cp, n) + area * P - PP * U_PP
    return out

# ── the slingshot keeper table (doc §7) ──────────────────────────────────────────
print("§7  slingshot per lepton  ΔE = m_e c²[γ(c′) − γ(c′/n)]   (MeV);  admissible c′ ≤ 0.9534")
print(f"{'c′':>7} {'γ(c′)':>7} {'oo':>7} {'ooo':>7} {'oooo':>7} {'D 2.2246−2·oo':>14}")
for cp in [0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.95]:
    oo, ooo, oooo = Y(cp, 2), Y(cp, 3), Y(cp, 4)
    print(f"{cp:7.3f} {gamma(cp):7.3f} {oo:7.3f} {ooo:7.3f} {oooo:7.3f} {B['D']-2*oo:14.3f}")
print("  (ooo, oooo add 2–8% over oo — the slingshot saturates; it is a per-contact quantum, not a ratio-maker)")

# ── the three ratios ──────────────────────────────────────────────────────────────
print(f"\nThree ratios  circ : square : hex  =  {CIRC:.4f} : {SQUARE:.1f} : {HEX:.4f}")
print("  circ = round (balloon) contact, unpacked;  square/hex = whole faces, forced by 100% Kelvin packing (He4 only)")
def area_of(k, circ):
    s, n, rp, whole, PP = PLAYERS[k]
    return rp * circ + whole
print(f"  contact area (square units), circ=π/4:  D {area_of('D',CIRC):.3f}  T {area_of('T',CIRC):.3f}  "
      f"He3 {area_of('He3',CIRC):.3f}  He4 {area_of('He4',CIRC):.3f}")
print(f"  U_pp = α ħc / 2R_p = {U_PP:.3f} MeV (computed);  T−He3 split = {B['T']-B['He3']:.3f}")

# ── calibration: D split 50:50 (James's start) → fixes Y-scale (hence c′) and P ────
half = B["D"] / 2
lo, hi = 0.5, 0.9534                    # slingshot leg: s_D · Y(c′,2) = half → solve c′
for _ in range(100):
    mid = 0.5 * (lo + hi)
    (lo, hi) = (mid, hi) if PLAYERS["D"][0] * Y(mid, 2) < half else (lo, mid)
cp_D = 0.5 * (lo + hi)
print(f"\nCalibration — D split 50:50 (start posit): slingshot {half:.3f} + patch {half:.3f}")
print(f"  ⇒ c′ = {cp_D:.4f}  (Y_oo = {Y(cp_D,2):.4f})")

def table(cp, P, circ, tag):
    pred = predict(cp, P, circ)
    print(f"\n{tag}")
    print(f"  {'nuc':4} {'pred':>8} {'data':>8} {'err':>7}")
    for k in ORDER:
        e = 100 * (pred[k] - B[k]) / B[k] if B[k] else 0.0
        print(f"  {k:4} {pred[k]:8.3f} {B[k]:8.3f} {e:+6.1f}%")
    return pred

# Scenario A — circ geometric (π/4). P from D's patch leg. He4 is a pure prediction.
P_A = half / (PLAYERS["D"][2] * CIRC)   # area_D = 1·circ ; area_D·P = half
table(cp_D, P_A, CIRC,
      "Scenario A — circ = π/4 (geometric). D exact by the split; T/He3/He4 all predicted:")

# Scenario B — circ deflated so D (50:50) AND He4 both fit; T/He3 then predicted.
# D: circ·P = half.  He4: whole·P + s4·Y = B(He4)+U_pp.  Two eqns, unknowns circ,P.
s4, n4, rp4, whole4, PP4 = PLAYERS["He4"]
P_B = (B["He4"] + PP4 * U_PP - s4 * Y(cp_D, n4)) / whole4
circ_B = half / P_B
print(f"\nLaplace lever [NEXT STEP — derive from surface tension, do not fit]:")
print(f"  D+He4 both on data ⇒ P = {P_B:.4f} MeV/sq-unit, round patch deflated to circ = {circ_B:.4f}")
print(f"  (naive π/4 = {CIRC:.4f}; deflation ×{CIRC/circ_B:.3f}). Laplace on the balloon contact is the posited")
print(f"  cause; its size is owed from γ_surface. It is He4-agnostic to T/He3 — they are round too.")
table(cp_D, P_B, circ_B,
      "Scenario B — circ Laplace-deflated (D and He4 anchored; T/He3 predicted, still round):")

# ── honest verdict ────────────────────────────────────────────────────────────────
print("\nVerdict (measured apart from concluded):")
print(f"  • He4 cliff is REACHABLE: packing (round→whole square+hex) makes 28 attainable with the sensible")
print(f"    ratio π/4:1:2.598 and a Laplace deflation ×{CIRC/circ_B:.2f} on the round patch. Two-term (no hex,")
print(f"    no packing) could not get near 28; this can. The deflation factor is a NEXT STEP to derive.")
print(f"  • T/He3 middle stays ~−20%% in BOTH scenarios: T's counts are 3× D's in every term, so T/D = 3.00")
print(f"    for ANY P, c′, circ; data T/D = {B['T']/B['D']:.2f}. The He4-only packing boost cannot move it.")
print(f"    T needs a count D lacks — an OPEN geometric question, not a constant to fit (do NOT reach for lstsq).")
print(f"  • slingshot: saturating (§7), per-contact; one free scale c′, bounded above by D (≤0.9534).")
