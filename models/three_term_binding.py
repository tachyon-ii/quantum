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

# Scenario B — the round patch is NOT one number. Under Laplace a balloon pressed by
# two neighbours (T, He3: coordination 2) has a bigger contact than one pressed by one
# (D: coordination 1); packed (He4: coordination 3) the face is whole. Anchor P and the
# coordination-1 patch on D+He4; then ask what patch T and He3 each REQUIRE. They are
# independent data (He3 carries computed Coulomb) — their agreement is the check.
s4, n4, rp4, whole4, PP4 = PLAYERS["He4"]
P_B   = (B["He4"] + PP4 * U_PP - s4 * Y(cp_D, n4)) / whole4    # He4 whole faces → P
c1    = half / P_B                                             # D: one contact, coordination 1
c2_T  = (B["T"]   - 3 * Y(cp_D, 3)) / (3 * P_B)                # T:   coordination 2, required
c2_H  = (B["He3"] + U_PP - 3 * Y(cp_D, 3)) / (3 * P_B)         # He3: coordination 2, required
print(f"\nScenario B — patch area by COORDINATION (Laplace: more neighbours, bigger patch, whole when packed)")
print(f"  P = {P_B:.4f} MeV/sq-unit (from He4's whole faces, D's split)")
print(f"  coordination 1  (D)          patch {c1:.3f}     [π/4 would be {CIRC:.3f}; deflated ×{CIRC/c1:.2f}]")
print(f"  coordination 2  (T)          patch {c2_T:.3f}   required by T")
print(f"  coordination 2  (He3)        patch {c2_H:.3f}   required by He3 — same geometry, differs by computed Coulomb; agree to {100*abs(c2_T-c2_H)/c2_T:.1f}%")
print(f"  coordination 3  (He4)        square 1.000, hex {HEX:.3f}  — whole faces, packed")
print(f"  monotone: {c1:.2f} → {0.5*(c2_T+c2_H):.2f} → 1.00 as neighbours 1 → 2 → 3; ratio to coord-1: ×{0.5*(c2_T+c2_H)/c1:.2f}, ×{1/c1:.2f}")
pred_B = {"D": B["D"], "He4": B["He4"],
          "T":   3 * Y(cp_D, 3) + 3 * 0.5*(c2_T+c2_H) * P_B,
          "He3": 3 * Y(cp_D, 3) + 3 * 0.5*(c2_T+c2_H) * P_B - U_PP}
print(f"  with ONE coordination-2 patch = {0.5*(c2_T+c2_H):.3f}:  T {pred_B['T']:.3f} ({100*(pred_B['T']/B['T']-1):+.1f}%)  He3 {pred_B['He3']:.3f} ({100*(pred_B['He3']/B['He3']-1):+.1f}%)")

# ── honest verdict ────────────────────────────────────────────────────────────────
print("\nVerdict (measured apart from concluded):")
print(f"  • MEASURED: the round patch T requires and the one He3 requires agree to {100*abs(c2_T-c2_H)/c2_T:.1f}% —")
print(f"    which is the T−He3 = {B['T']-B['He3']:.3f} vs U_pp = {U_PP:.3f} split ({U_PP-(B['T']-B['He3']):.3f} MeV) spread over 3 patches:")
print(f"    the same Coulomb check as before, restated (Neyman 2026-09-09). NOT independent evidence for coordination.")
print(f"  • MEASURED: patch area is monotone in coordination number: {c1:.2f} (1 nbr) → {0.5*(c2_T+c2_H):.2f} (2) → 1.00 (3, packed).")
print(f"  • CONCLUDED [POSIT, untested until A≥5]: the patch mechanism is ONE mechanism — contact area grows with how many")
print(f"    neighbours squeeze the balloon, saturating at the whole face when packed. There is no missing")
print(f"    integer at A≤4. The old 'T/D=3 structural' claim assumed one patch size for every round contact;")
print(f"    that assumption, not the geometry, was wrong.")
print(f"  • OWED [NEXT STEP]: derive the trough (interference at the smurf distance, James 2026-09-09 — not surface")
print(f"    tension) and the patch of a balloon held there under 1/2/3 neighbours; it must reproduce the curve")
print(f"    {c1:.2f} → {0.5*(c2_T+c2_H):.2f} → 1.00 with no free knob. It fixes the ATTRIBUTION; the geometry stands either way.")
print(f"  • CAUTION: the 50:50 split pins c′ at its ceiling ({cp_D:.4f}). A lighter slingshot share lowers c′ and")
print(f"    raises P; the coordination curve rescales but keeps its shape. c′ is one honest free scale, at a boundary.")
print(f"  • NOT YET a prediction of a new nucleus: 3 unknowns (P, patch₁, patch₂) on 4 points = the one check above.")
print(f"    Prediction starts at A≥5, where coordination mixes within one nucleus.")
