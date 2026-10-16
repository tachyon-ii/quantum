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

---

## The lateral bleb (James, after Build 4) — graded

**James.** The bleb matters more than a 2 % radius stretch: displaced volume rolls laterally into a collar around the facet and *increases the contact patch at each of the 4–6 neighbouring edges*. **Argon:** ΔA/A ≈ 2δr/r on every bordering interface; neighbour 3 sits on the bleb of the 1–2 contact, so the bleb is the mechanical actuator of Build 3's closure jump; two regimes — pockets self-tighten (z = 2–4), full occupation makes blebs collide into the stiffening wall (z ≥ 6); predicts Build 4 would *under*-bind pocket nuclei.

**Grace.**
- *As mechanism:* ACCEPT as the continuum-mechanics face of lane closure. "The third capsid lands on the meniscus of the first contact" and "a closed ring of lanes is a standing wave" are one posit in two languages, and the bleb version is the one a relaxer could actually compute. It adds nothing new at A ≤ 4 beyond Build 3 (same cooperativity, now with a reason); its own prediction is the pocket self-tightening at z = 3–4, testable later in ⁵⁶Fe's four pockets.
- *As the cure for ⁸Be:* NO — it points the wrong way. Build 4 failed by **over**-binding compact placements, not by under-binding pockets; Argon predicted the opposite residual. More nucleon-level cooperativity makes merging *more* favourable. The bleb cannot rescue the α–α sector.
- *Why the lattice merged the alphas, in one number.* Nucleon–nucleon contact on the Kelvin lattice is at 1.46–1.68 fm (centre to centre). The α–α centre distance from the measured radii of ¹²C and ⁴He is **3.14 fm**, and an alpha's nucleons sit 0.94 fm from its centre — so neighbouring alphas' surface nucleons are ~**1.3 fm apart surface-to-surface**, i.e. *not in facet contact at all*. Real alphas never approach to nucleon contact; every "merged" placement I enumerated is a configuration nature does not visit. The α–α bond is a longer-range contact between two *alpha* capsids — the trough at the alpha rung — which is the two-rung conclusion of the Build 4 page, now with the distance that forces it.

---

## Build 5 (two rungs) — Argon's sketch graded, and what must be declared before it runs (Grace, 16 Oct)

**Accepted:** the architecture. Rung 1 = nucleons → D, T, ³He, ⁴He by closure (done, locked). Rung 2 = alphas as closed capsids (R_α ≈ 1.57 fm, contact at d_αα = 3.14 fm, only one way for two spheres to touch — no lumps) plus loose nucleons; inter-alpha Coulomb U_αα = 1.835 MeV at that distance. Argon's reading of `loose cannons = 0` at ⁴He as the reason an alpha's lanes do not open to a neighbour is the ontology's own statement and is the right one.

**Corrected before anyone codes it:**
1. **"The same law one rung up" is already false in one detail.** At rung 1, one triangle through an edge gives *half* a face and two give the full face (that is what predicted T and ³He). At rung 2 that rule fails at once: calibrating the half-bond on ¹²C (c = 1) makes the full bond 8.52 MeV and ¹⁶O's residual 40.1 MeV against 14.44 measured. The ladder's constant q says **at the alpha rung, c = 1 and c = 2 bonds are equal**; the only distinction is open (c = 0) vs closed (c ≥ 1). Different cooperativity at different rungs — which is itself a result about the turtle, and should be written as one.
2. **⁸Be at the declared distance is −0.225 MeV, not −0.092.** Argon's −0.092 uses d_αα = 3.38 fm, chosen after the fact; at the declared 3.139 fm the open bridge gives 0.378 × 4.260 − 1.835 = **−0.225 MeV**. Right sign, unbound, magnitude 2.4× — that is the honest blind result and it is good. Do not retrofit the distance.
3. **⁹Be is not a blind until the nucleon–alpha contact law is declared.** Argon's "+1.55 to +1.67" is assembled from two open nucleon patches, a slingshot upgrade and a "1/4-scale mass weight" invented in the sentence. Declare what a single nucleon touching an alpha capsid is worth, then run it.
4. **Ne-20 is the first rung-2 blind already on the books, and the closure law fails it.** Nine closed α–α bonds give 21.8 MeV vs 19.17 measured (+13.9 % — the ladder's known sore thumb). If James's stiffening belongs at the alpha rung (Argon's "native habitat"), Ne-20's three equatorial alphas at z_α = 4 are where it first bites: closing the gap needs **0.88 MeV per z_α = 4 alpha**. That sets the rung-2 stiffening scale on Ne-20; then Mg-24, Si-28 … Ni-56 and the ⁵²Fe star (core alpha at z_α = 12) are the blinds for the π^(1/3) series — and the per-bond ladder (2.37, 2.56, 2.52, 2.48, 2.46 … flat to Ni-56) is a hard test of it, because a monotone penalty must not make the ladder sag where the data don't.

**So Build 5 = the alpha ladder + three declared additions:** the open-bridge fraction (⁸Be → −0.225), a nucleon–alpha contact law (⁹Be, ⁷Li, ⁷Be), and a rung-2 stiffening scale set on Ne-20 (then Mg → Ni as blinds). Pencil before code: most of it is a table.

---

## James's reframing — circular patches sized by centroid proximity — and Argon's d⁻³ table, checked (Grace, 16 Oct)

**James [RULING-grade reframing, ACCEPT]:** the squares and hexagons were a shortcut and they are wrong; k calibrated on Kelvin faces is contaminated by that choice; the measured inter-centroid distances of D, T, ³He, ⁴He are data the model should be using; the alpha's double magic is more and larger patches plus maximal slingshot; assume spherical capsids and circular patches whose size follows centroid proximity.

**The distances, done once and consistently** (d from the measured charge radii with the proton's own radius unfolded: d = 2r for the pair, √3 r for the triangle, √(8/3) r for the tetrahedron, r = √(R_ch² − R_p²)):

| | d (fm) | Coulomb at d | required energy per bond |
|---|---|---|---|
| D | 3.910 | 0 | 0.788 MeV |
| T | 2.676 | 0 | 2.071 |
| ³He | 3.078 | 0.468 | 1.972 |
| ⁴He | 2.371 | 0.607 | 4.305 |

Two immediate gains, independent of any law: the ⁴He pp Coulomb at the *measured* separation is 0.61 MeV, not the lattice's 0.86, so P recalibrates slightly; and the T−³He split at the measured separations is 0.47 MeV of Coulomb plus 0.30 MeV of smaller patch in the Coulomb-puffed ³He — the A = 3 Nolen–Schiffer residual as geometry, which is the right shape of answer and is accepted.

**Argon's d⁻³ proximity law — REJECT as run; the table was assembled from mixed distances.** Argon derives the exact distances above and then, in the "final table," uses d(⁴He) = 2.10, d(T) = 2.68, d(³He) = 2.72, d(D) = 3.76 — four numbers from four different sources, chosen where each fits. With the one consistent set: **D +7.7 %, T +32.7 %, ³He −0.1 %, ⁴He calibration.** The cleanest test is the mirror pair, parameter-free: measured E₁(T)/E₁(³He) = 1.05; a d⁻³ law predicts (d_He3/d_T)³ = **1.52**. It over-predicts the mirror difference tenfold. The lens law π(R_eff² − d²/4) with R_eff fitted on the T/D ratio (2.25 fm) gets the ³He/T ratio to 0.82 (measured 0.95) and the ⁴He/T ratio to 1.12 against a measured 2.08 — proximity alone does not make the cliff; the factor two from T to ⁴He is still the closure (two triangles per edge), as Argon itself notes in passing. Its ⁸Be "−0.048 MeV" counts one inter-alpha attraction against four Coulomb pairs: a pairwise d⁻³ law has to sum all sixteen inter-alpha pairs, and then ⁸Be is heavily bound. Struck.

**What stands.** The currency changes: circular patches, measured d as input, Coulomb at the measured d. The cooperative term stays: closure (open / one triangle / two triangles). The honest statement of the A ≤ 4 sector is now three numbers in one law — the patch for an open contact, for a contact on one triangle, for a contact on two — read off D, T, ⁴He at their measured separations, with ³He then *predicted* (the T−³He split from Coulomb at 3.08 fm plus the 5 % patch shrink). That is the same content as Build 3 in a better currency, and it makes k's calibration honest: k = E₁/A_circle with A_circle the measured lens, not a Kelvin face. Grace will redo `stiffness_ratio.py` on that basis; the comparison with c⁴/(G R_Λ) is re-opened on the new k, not pre-judged.
