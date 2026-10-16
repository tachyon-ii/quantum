# Build 4 — closure + stiffening penalty, scale set on C-12: result (Grace, 16 Oct 2026)

**Script:** `models/binding/build4_stiffening.py` (calibration state in `build4_state.json`). Protocol as declared: Build 3's closure rule, P and A_open unchanged; one new scale D4 for a per-contact penalty pen(z) = D4·Σ_{k=4}^{z} r^{k−4}, r = π^(1/3) (James's form), pen = 0 for z ≤ 3; D4 set by bisection so that the lowest-energy lattice placement of three alphas reproduces BE(C-12) = 92.162. Seating rule R6 throughout. Blinds declared: ⁸Be unbound (−0.092 vs 2α), ⁹Be +1.666 above ⁸Be.

## Calibration
D4 = **1.107 MeV** (C-12 at 92.15). Implied penalties: pen(5) = 2.73, pen(6) = 5.10, pen(7) = 8.58, pen(12) = 71.5 MeV per nucleon. A ≤ 4 untouched by construction (T +3.6 %, ³He +2.8 %, ⁴He −0.5 %).

## Blinds — both FAIL
| | Build 4 | measured |
|---|---|---|
| ⁸Be vs 2α | **+6.12 MeV** (lowest-energy placement has 6 inter-contacts, z up to 6; penalty 17.9 MeV already paid) | −0.092 |
| ⁹Be above ⁸Be | **+8.72 MeV** (+22.8 % on total) | +1.666 |

## What the failure says — and it is the same thing twice
With or without the penalty, with or without saturation, **the energy function prefers compact arrangements**: closed-triangle half-faces (1.3–2.6 sq-units × 2.1 MeV) outweigh a penalty of a few MeV until z ≥ 6, so two alphas always find a partially merged placement that binds by several MeV. Calibrating D4 on C-12 does not help because C-12's own lowest-energy placement is also compact; the calibration absorbs the compactness and ⁸Be inherits it.

The data say the opposite about alphas: ⁸Be is a dumbbell, the α–α bond is weak (2.4 MeV net, ~1.15 sq-units net, ~2 sq-units gross after Coulomb), and nothing merges. In the ontology's own words: **the alpha is a closed shell — its nucleons' lanes are closed among themselves and do not open new triangles to a neighbouring alpha.** Under that reading inter-alpha contacts are bridges (A_open, 0.79 MeV each), which makes ⁸Be's neck unbound correctly — but then the ladder's 2.4 MeV per α–α bond cannot be reached either (two bridge contacts give 1.58 − 1.84 Coulomb < 0). So the α–α contact is *neither* an open nucleon bridge *nor* a closed nucleon half-face. It needs its own currency, ~2 sq-units gross — which is to say, **the alpha is a capsid in its own right with its own skin and its own patch law: the next rung.** That is exactly what `the-fractal-nucleus.md` posits (q = 2.425 per α–α bond; "the same interactions one rung up") and what the nucleon-level lattice model cannot produce from below.

## Grade
[COMPUTED — negative result, informative.] Builds 3 and 4 establish: (1) lane closure predicts the A ≤ 4 coordination curve with nothing fitted (T +3.6 %, ³He +2.8 %); (2) no nucleon-level facet model with lowest-energy seating produces the α–α sector — it over-binds every cluster of alphas by merging them; (3) the α–α bond must be modelled at the alpha rung. The stiffening series stands as a declared form, untested at z ≥ 7 (⁵⁶Fe not run — pointless until the α rung exists). Nothing is tuned; no number from Build 4 enters any document except this page.

## Next build, if James wants it
A two-rung model: nucleons bind into alphas by closure (Build 3, done); alphas bind as units with a patch law of their own, calibrated once on C-12 (q) — then O-16, Ne-20 (the +14 % sore thumb), ⁸Be (unbound) and ⁹Be (+1.67) are the blinds at that rung, and the Mackay/1+12 counts of the fractal nucleus are its geometry. The nucleon-level penalty then lives *inside* the alpha rung's skin stiffness, which is where James's isoperimetric pressure belongs.
