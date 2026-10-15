# Argon review — Documents 1–5, consolidated

**Reviewer:** Argon (Gemini 4 Argon, Google DeepMind), fresh instance, protocol v2 of `BRIEF.md` (one document per message). **Session:** engram `cgios_memory_engram_gemini_2026-10-15T20_31_30.377Z_t0-9.json`, 10 turns. **Consolidated by:** Opus 5.5 (formatting only — no grading, no edits to substance; the Lineage-Rule grading is a separate pass, to follow).

**Transport notes.** The engram's math was scraped as rendered MathML; it has been re-set as plain notation here. Argon's own consolidation attempt (turn 10) aborted on a parser bug (raw `<` in a subscript). In Document 4, the bodies of F24–F26 were scrambled in transport twice (turns 6 and 8); **Argon supplied a clean drop-in patch on 16 Oct** for F24, F25, F26 and the truncated Document 2 prior-art rows, applied verbatim. F27 had been restored cleanly in turn 8. Argon was also given `hubrility-v8.md` and `socratic-cyclotron.md` as process background before Document 1 and said it would watch for "ghost premises" from the earlier H² framework.

**Documents covered:** #1 `docs/README.md` + `docs/Φ-a-minimal-ontology-of-an-emergent-universe.v2.md` · #2 `docs/Φ-canon-integrated.md` · #3 `docs/three-term-binding.md` · #4 `docs/the-fractal-nucleus.md` · #5 `docs/the-turtle-conjecture.md`. Not yet sent: #6–#9.

## Index of findings

| F | doc | where | type | Argon's grade | blast |
|---|---|---|---|---|---|
| F1 | v2 | §7, §19, §24 — tetra offset; skew-loop relaxation | commission | DEAD (offset ×2); CONDITIONAL (relaxation needs a confining constraint) | high |
| F2 | v2 | §15 — Brownian paint as HZ density spectrum | commission | DEAD as derivation | high |
| F3 | v2 | §5, §10, §11 — spin-up k = 2/5; "two roots" | commission | CONSTRUCT, internally inconsistent | high |
| F4 | v2 | §12a — Lemaître/PG; redshift attribution | commission | CONSTRUCT | med-high |
| F5 | README, v2 | §11, §19 — the 1.000 still tagged P | commission | R (tautology) | low-med |
| F6 | v2 | §10–§13 — Milne slicing vs flatness | commission | CONDITIONAL, contradicts §11/§13 | high |
| F7 | v2 | §12a — 8.2 ppm / 113 kyr clock lag | commission | COMPUTED, wrong velocity input | low |
| F8 | v2 | §7, §14, §18 — spin composition | commission | POSIT, owes Pauli; §14 vs §18 | medium |
| F9 | v2 | §7, §10, §16 — proton stability; FIRAS | omission | OWED | med-high |
| F10 | canon | §10 — Koide conditional theorem | commission | CONJECTURE | high |
| F11 | canon | §16 — snakeskin dark matter | commission | DEAD as stated | high |
| F12 | canon | §14 — c′ = 0.9534 vs 50:50 split | commission | CONSTRUCT, factor-2 in s | medium |
| F13 | canon | §15 — Nolen–Schiffer constant residual | commission | DEAD — falsified by existing data | medium |
| F14 | canon | §12–§13 — bound-neutron stability; two-stage decay | commission | CONJECTURE | med-high |
| F15 | canon | §32.13 Posit 5 — governors run down | commission | DEAD | low |
| F16 | canon | internal collisions (EHT chromatic; 370 vs 627 km/s; δ) | commission | INTERNALLY INCONSISTENT | medium |
| F17 | canon | §9, §11, §31 — DIS, e⁺e⁻ annihilation, compositeness | omission | OWED | high |
| F18 | binding | §7b — tyre law | commission | DEAD | high |
| F19 | binding | §7a — T−He3 split; Coulomb; R6/R7 | commission | CONSTRUCT | high |
| F20 | binding | §5–§8 — touching capsids vs R_D = 2.128 fm | commission | GEOMETRICALLY INCOMPATIBLE | medium |
| F21 | binding | §6–§9 — full Coulomb; v = c′/n; de-spin | omission | OWED | high |
| F22 | fractal | §3 — "triangles do not touch" | commission | DEAD | high |
| F23 | fractal | §6 — fe56_star | commission | CONSTRUCT, three contradictions | high |
| F24 | fractal | §4 — alpha ladder omits inter-alpha Coulomb | omission | CONSTRUCT | medium |
| F25 | fractal | §3a, §7 — Mackay series vs §10; Bi-209 row; "left over = 0" | commission | INTERNAL CONTRADICTION / ARITHMETIC SLIP | low-med |
| F26 | fractal | §3b — neutron capture favoured along N = Z + 4 pocket line | commission | CONTRADICTED BY DATA (N = 28 magic isotone line) | low-med |
| F27 | fractal | §8 Falsifier 1 — ±10 % gate; Ca-40 seating | omission | UNDERSPECIFIED | medium |
| F28 | turtle | §3b, §5a — G ≈ c⁴/kR_H and lockstep | commission | COINCIDENCE at t₀ | high |
| F29 | turtle | §2, §3 — the tripod; R/3 lag | commission | CONJECTURE, four errors | high |
| F30 | turtle | §3c — sec θ on the chorus slice | commission | CONSTRUCT | medium |
| F31 | turtle | §3, §9, §10 — Gm_p²/R_p ≈ 10⁻³⁰ MeV | commission | unit error ×10⁶ | low |
| F32 | turtle | §6a — mass inflation; Planck floor | commission | CONJECTURE | medium |
| F33 | turtle | §3a, §8 F7 — PBH edge at 2.5 × 10¹³ kg | omission | UNOBSERVABLE as stated | low-med |

---

## Document 1 — `README.md` + `Φ-a-minimal-ontology-of-an-emergent-universe.v2.md`

**F1. v2 §7, §19, §24 — the tetrahedral offset and the relaxation of two skew loops.**
*Claim:* the tetrahedron's two loops run along opposite edges, "offset from the centroid by edge/√2 [FACT, checked]"; relaxation pushes the two loops of n = 2 off the centroid.
*Type:* commission. *Grade given:* FACT (offset); THEOREM, Cohn–Kumar (relaxation); CONSTRUCT-in-principle (no-node stability). *Argon:* DEAD for edge/√2; CONDITIONAL THEOREM for relaxation, conditional on an unstated confining constraint.
*Problem:* (1) For vertices (1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1), edge a = 2√2; the opposite-edge midpoints (±1,0,0) are distance 1 from the centroid = a/(2√2) ≈ 0.354a, not a/√2 ≈ 0.707a. a/√2 is the bimedian (edge-to-edge) distance. §7 and the §19 table both carry the factor-2 error. (2) Thomson / Cohn–Kumar optimality is for points *constrained to a sphere*. Once the two loops leave the centroid as unlinked skew segments of fixed length a, nothing enforces the sphere: the inter-loop lobe distance is r₁₂(x₀) = √(4x₀² + a²/2), and for any decreasing repulsion V(r) the energy falls monotonically in x₀ — the loops dissociate into two free n = 1 loops. If instead they stay anchored at the centroid, they still cross there, erasing the "no crossing at n = 2 vs one at n = 3" distinction.
*Blast radius:* high — §7 (proton/neutron node mechanism, alpha crossed-pair), §19 row 3, §24, every downstream use of the offset or skew binding.
*Fix:* correct to edge/(2√2) (axis separation edge/√2); state the confining potential or linking constraint that holds the skew pair together.
*Kill test:* E(x₀) = 2V(a) + 4V(√(4x₀² + a²/2)) for V = r⁻ᵖ — is there a minimum at finite x₀? *Truifier:* show a shared constraint (fixed circumradius R = √(x₀² + a²/4)) gives a stationary point at x₀ = R/√3 = a/(2√2).
*Ran it:* yes — unconstrained dE/dx₀ < 0 everywhere (dissociates); constrained, the stationary point is at a = √(8/3)R, x₀ = R/√3 = a/(2√2) for all p > 0.
*Confidence:* high.

**F2. v2 §15, §19, §21, §24 — the recoil paint as the primordial spectrum.**
*Claim:* the occupation density of the recoil walk is the primordial density field; Brownian gives slope −2 in 2D = Harrison–Zeldovich; the red tilt demands H = 0.4914.
*Type:* commission. *Grade given:* COMPUTED ("the strongest consequence in the document"); P (shape only) in §19. *Argon:* DEAD as a derivation of the HZ density spectrum.
*Problem:* (1) Missing Poisson factor. HZ (n_s = 1) means equal power per octave in the *potential/curvature*, P_Φ ∝ k⁻³ in 3D. Poisson gives δ ∝ k²Φ, so the HZ *density* spectrum is P_δ ∝ k¹ in 3D (k⁰ in 2D), not k⁻². A density with P_δ ∝ k⁻² gives P_Φ ∝ k⁻⁶ — effective n_s ≈ −2, off by ≈ 3. §15 explicitly calls the occupation the *mass density* ("painted twice has a gravitational advantage"). (2) Dimensionality: the occupation integral is over 1D walk time, so Brownian gives |ρ̂(k)|² ∝ k⁻² in *every* d ≥ 2; that is flat per octave only in d = 2, and not in 3D. (3) Geometry: in §9–10 the ejecta travel radially, so launch time maps to radius; the walk does not deposit strokes onto one 2D sheet at fixed radius.
*Blast radius:* high — all of §15, §19 rows 10–13, §20 (Hurst owed), §21 falsifiers 14–15, §24 ("one of the three results of v2").
*Fix:* not small. Either the walk sets the potential Φ directly (and a mechanism lifts it to 3D), or density is the Laplacian of the occupation — which needs a hyperuniform walk, impossible for fractional Brownian occupation (−1/H < −1).
*Kill test:* P_Φ from a Brownian occupation density via Poisson vs Planck n_s − 1 = −0.0351 ± 0.0042. *Truifier:* derive from the axioms a walk that sets Φ directly with P_Φ ∝ k⁻³⁻⁰·⁰³⁵.
*Ran it:* yes — slope off by ≈ 3 per octave; "killed as a density-seed model by > 700σ against Planck 2018."
*Confidence:* high.

**F3. v2 §5, §10, §11, §19, §24 — the spin-up law and the "two roots".**
*Claim:* with R = c/ω the spin-up is free (ω ∝ m^−3/2); ω = c³/2GM "has two roots" — the Planck scale and the Hubble sphere.
*Type:* commission. *Grade given:* COMPUTED (§10); FACT for the identity, POSIT for the mapping (§11). *Argon:* CONSTRUCT — internally inconsistent scalings; imports a classical k = 2/5 sphere inside Ω.
*Problem:* (1) Spin-up exists only because k = 2/5 < 1 is assumed — the moment-of-inertia coefficient of a uniform Newtonian solid ball, i.e. a 3D interior inside Ω, violating §2 (no current physics inside Ω) and §4 (partless whole). A partless Ω with all its amount at R = c/ω has k = 1: ω constant, no spin-up. (2) Three conflicting ω(m) laws. §10's ω ∝ m^−3/2 means R ∝ m^+3/2: starting from R_H at M_U, shrinking to the Planck mass gives R ≈ 10⁻⁶⁵ m, missing ℓ_P by 30 orders; and early ejecta are shed at large radius, late ones at shrinking radius. §11's ω = c³/2GM is one hyperbola, not an equation with two roots; the Planck point comes from intersecting it with Compton (ω = mc²/ħ), giving R = 2√2 ℓ_P not ℓ_P; at M_U the same Compton relation gives ω ≈ 7.85 × 10¹⁰³ s⁻¹ against H₀ ≈ 2.18 × 10⁻¹⁸ — 121 orders apart. The two points are not two roots of the same pair of equations.
*Blast radius:* high — §5, §10, §11, §19 row 7, §24, README (and the turtle conjecture's two-roots reading).
*Fix:* drop "two roots of the same equation" (a one-parameter hyperbola evaluated at two externally chosen masses), carry the 2√2; state k < 1 as an extra constitutive posit inside Ω and reconcile shrinking-radius shedding with an expanding universe.
*Kill test:* R(m_P) = R_H (m_P/M_U)^((1−k)/k) at k = 2/5 vs ℓ_P; matching needs k = 1/2. *Truifier:* derive k = 1/2 from the axioms without an interior density profile.
*Ran it:* yes — at k = 2/5, off by ~10³⁰; at k = 1/2, R ∝ m matches up to 2√2.
*Confidence:* high.

**F4. v2 §12a, §19, §24 — Lemaître vs Painlevé–Gullstrand, and what produces z = gh/c².**
*Claim:* t constant and t ⊥ space define the synchronous gauge; Lemaître's coordinates are it; the river model is its picture; the shift is the spatial metric changing in flight, second-order Doppler, z = gh/c².
*Type:* commission. *Grade given:* DERIVED in the gauge; R (GR). *Argon:* CONSTRUCT — silent switch between Lemaître and PG; misattributes clock dilation to in-flight dl/dt.
*Problem:* (1) Lemaître is synchronous (g_τρ = 0, time-dependent spatial metric); PG has g_τr = v/c ≠ 0 and flat static slices. (2) Naive upstream-motion Doppler would give a first-order shift Δv/c ≈ gh/(v₁c) ≈ 6.6 × 10⁻¹¹ at Pound–Rebka (h = 22.5 m) — 26,800× the measured gh/c² = 2.46 × 10⁻¹⁵. In PG the metric is stationary: the in-flight velocity gradient exactly cancels that first-order term, and what survives, (v₁² − v₂²)/2c², is 100 % the ratio of the emitter's and receiver's proper-time rates — clock dilation, not in-flight stretching.
*Blast radius:* medium-high — §12a, §19 rows 20–21, §24, turtle §3, §3c, §6a.
*Fix:* distinguish Lemaître from PG; attribute z to the clock-rate ratio.
*Kill test:* compute the PG arrival interval Δτ_recv/Δτ_emit for crests climbing a static potential.
*Confidence:* high.

**F5. README + v2 §11, §19 — the 1.000 regrade not propagated.**
*Claim:* "2GM/R = c² at the Hubble radius to 1.000 (computed)" (README); tagged P in §19.
*Type:* commission. *Grade given:* P (§19), COMPUTED (README), RETRODICTION (§11 body after 15 Oct). *Argon:* R — algebraic tautology for the 1.000; retrodiction of Ω_tot = 1.
*Problem:* §11's 15 Oct regrade was not carried to the §19 ledger (where only P-rows count as evidence) or to the README.
*Blast radius:* low-medium — README, §19, turtle §3b. *Fix:* §19 row 8 P → R; README to match §11.
*Confidence:* high — "already agreed in §11, just un-propagated."

**F6. v2 §10, §12, §13, §16, §24 — the chorus as Milne.**
*Claim:* every ejectum comoving, radial from Ω; the now is the surface of constant τ — "Milne's construction (1933; the empty limit of FLRW)."
*Type:* commission. *Grade given:* THEOREM, given the chorus. *Argon:* CONDITIONAL THEOREM — incompatible with §10, §11 and §13.
*Problem:* Milne's constant-proper-time slices of radial worldlines from one event are hyperbolic (k = −1, Ω_tot = 0, empty), contradicting §11 (flat, Ω_tot = 1), §13 (compact flat T³) and §10 (decelerating shells that cross — Milne's worldlines never decelerate or cross).
*Blast radius:* high — §10–§13, §16, §24 (where "the chorus" is single point of failure #1).
*Fix:* separate the homogeneous FLRW comoving foliation (no spatial centre; Ω is the t = 0 boundary in every point's past) from the central shell-ejection picture (Ω a spatial centre, early shells at smaller r). "You cannot have both simultaneously."
*Kill test:* compute the spatial Ricci scalar of the constant-τ slice. *Confidence:* high.

**F7. v2 §12a, §19, §24 — the 8.2 ppm / 113,000-year clock lag.**
*Problem:* uses the Local Group's 627 km/s against the CMB (2.2 ppm) instead of the Solar System's 369.8 km/s (0.76 ppm), and omits the local supercluster potential (~10–30 ppm). Corrected: 6.8 ppm, ~93 kyr, plus the supercluster term.
*Type:* commission. *Argon:* COMPUTED, wrong velocity input. *Blast radius:* low. *Ran it:* yes — Planck 2018 dipole, 369.82 km/s → 0.761 ppm. *Confidence:* high.

**F8. v2 §7, §14, §18 — spin composition.**
*Claim:* proton = ν̄ν pair (0) + e⁺ (½); neutron = ν̄ν̄ν (½) + e⁺e⁻ (0); §14's lifted figure-eight has ⟨L⟩ = (0, −0.16, 0) at lift 0.2.
*Type:* commission. *Argon:* POSIT — owes Pauli antisymmetrisation for ν̄ν̄ν; §14's continuous orbital L contradicts §18's quantised phase spin.
*Problem:* two identical-orientation loops at a shared node must satisfy Fermi statistics; three mutually orthogonal spin-½ axes add in quadrature, not collinearly; a continuous classical lifted-lemniscate L is not the discrete antiperiodic spin of §18.
*Blast radius:* medium — §7, §14, §18, canon nucleon sections. *Kill test:* compute J and the exchange symmetry of three spin-½ loops at a node. *Confidence:* high.

**F9. v2 §7, §10, §16 — two omitted barriers.**
*Problem:* (a) Nothing in the ledger forbids exothermic p → e⁺ + (ν̄ν), Q = +937.76 MeV, once baryon number is replaced by leptonic composites — the skew-loop geometry explains no crossing, not no separation. (b) Relativistic shell crossing in §10 (Δv ~ c) must clear the COBE/FIRAS blackbody bounds (|y| < 1.5 × 10⁻⁵, |μ| < 9 × 10⁻⁵) — two-stream / Compton drag, energy injection.
*Type:* omission. *Argon:* OWED. *Blast radius:* medium-high.
*Fix:* add to §20 — a topological linking barrier; and place the crossing epoch at z ≫ 2 × 10⁶ (before thermalisation freeze-out).
*Kill test:* Super-K / Hyper-K invisible-mode proton decay (τ > 1.7 × 10³² yr); FIRAS μ bound if crossing is at z < 2 × 10⁶. *Ran it:* yes — Q = 938.272 − 0.511 = +937.761 MeV. *Confidence:* high.

**Document 1 — what is wrong (Argon).** §15's paint spectrum off by the Poisson factor k⁴ and by d = 2 → 3 (F2). §7/§19's offset is ×2 (F1). §7's skew loops dissociate without a confining constraint (F1). §10/§11 scaling laws conflict and import k = 2/5 (F3). §12a mixes Lemaître and PG and misattributes the redshift (F4). §12's Milne slicing is open, not flat (F6). §19 and README still advertise the 1.000 (F5). The clock lag uses the wrong velocity (F7).

**What is missing.** A linking/topological barrier for proton stability (F1, F9). Pauli antisymmetrisation and 3D spin addition for the governors (F8). The thermodynamic epoch of shell crossing vs FIRAS (F9). Reconciliation of §14's orbital L with §18's phase spin (F8).

**What is fine — stop re-examining.** Every kill in §22 (prime sieve; orthogonality running out; torque-free precession; naive ice-skater; trailing shells as dark matter via Birkhoff; c-invariance forbidding bulk rotation; embedded-donut occlusion; the pendulum). Thomson N = 4 (3.83 vs 3.67), N = 6 (10.96 vs 9.99), N = 8 (square antiprism) and Cohn–Kumar on S². The (d − 4) radial-stability linearisation and the d = 2..6 table, given P1. The SO(4) ≅ (SU(2) × SU(2))/ℤ₂ two-rate non-closure argument — "mathematically clean and genuinely distinct." Retiring the Möbius strip for the antiperiodic phase on S¹. The per-link loop ℓ_ab/Δs < c.

**Prior art — Document 1.**

| move | closest prior art | reproduced | new here |
|---|---|---|---|
| pre-spatial axioms Ω{amount, spin, time}; length/mass downstream | Milne, kinematic relativity (1933, 1948); natural units | {m, l, s} → {E, s} via c = ħ = 1 | pairing a 0D U(1) phase rate with a conserved amount and tying first extent to R = c/ω before metric space exists |
| loop ladder → cross-polytopes → Thomson relaxation | Thomson (1904); Cohn & Kumar (2007, JAMS); alpha-cluster models (Wheeler 1937; Brink 1966) | Thomson energies; antiprism at N = 8; tetrahedral ¹⁶O / triangular ¹²C | n = 2 tetra (no crossing) as proton governor vs n = 3 octa (one node) as neutron governor; the spin-addition table |
| d = 3 by stability + knots + closure | Ehrenfest (1917); Tangherlini (1963); Tegmark (1997) — cited | (d − 4) threshold; stable orbits ∩ knots at d = 3 | adding the SO(4) incommensurate-rates non-closure kill |
| flatness from escape velocity at R_H | McCrea & Milne (1934); Sciama (1953) — cited | 2GM/R_H = c² ⇔ Ω_tot = 1; Φ_U/c² = 3/4 | reading Ω_tot = 1 as the marginal capture boundary of rim ejection at c |
| Planck from Compton = Schwarzschild; R_p = 4ħ/m_pc | textbook; EPL 2019 — cited | both identities | reading R_C = R_S as period-extent = capture-extent |
| gravity in synchronous/river coordinates | Painlevé (1921), Gullstrand (1922), Lemaître (1933), Hamilton & Lisle (2008) — cited | GR redshift, Shapiro, Pound–Rebka in flow coordinates | nothing different from GR (and see F4) |
| T³ topology; L moved to galaxy-spin chirality | Luminet et al.; matched circles; COMPACT (PRL 2024); Saadeh et al. (2016); Longo (2011); Shamir (2020–24) | matched-circle and vorticity bounds; the handedness test | tying zero vorticity + local chirality to conservation of Ω's proto-spin |

---

## Document 2 — `Φ-canon-integrated.md`

*Argon's note:* where the canon integrates v2 (§2–5, §25), F1, F3, F4, F6, F7, F8, F9 carry forward and are not re-numbered.

**F10. canon §10, §32.12, §33.12, §36.11 — Koide Q = 2/3 as a conditional theorem.**
*Grade given:* CONDITIONAL THEOREM (P1 ∧ identity-postulate ∧ P3 ⇒ Q = 2/3); PREDICTION for 58.6 meV in §10 header, §32.12, §36.11. *Argon:* CONJECTURE.
*Problem:* (1) The step |v_ani|² = 2 × ω multiplies the mode frequency by the dimension of the flavour plane, which needs an unstated *mode-equipartition postulate* (both orthogonal modes equally excited). A single state vector excites one direction in the plane, giving E_core : E_ani = 2 : 1 ⇒ Q = 1/2. At the measured charged-lepton phase δ = 0.222 rad the two modes carry 95.2 % and 4.8 % (19.6 : 1); equipartition would force δ = π/4. P1–P3 also never justify why √m (not m) projects linearly onto generation axes. (2) The 15 Oct retrodiction regrade of 58.6 meV sits in §10's body but not its header, §32.12, §33.12 or §36.11. (3) Credit: Brannen (2006) for the signed (−,+,+) branch, δ_ν − δ_l = π/12 and 58.6 meV; Foot (1994) for θ = 45°.
*Blast radius:* high — §9, §10, §32.12, §33.12, §34, §36.10–11, and the document's closing grade.
*Fix:* downgrade to CONJECTURE, or add the linear-√m projection and a trace postulate; propagate the regrade; credit Brannen.
*Kill test:* inverted ordering (Σ ≥ 99 meV), Σ > 65 meV in normal ordering, or Dirac neutrinos. *Truifier:* derive δ_l = 0.2222220(19) rad (≈ 2/9 to 10⁻⁶) from the 2O / BP&R rotator with zero fitted parameters.
*Ran it:* yes — all §10 numbers verified (Q_l = 0.66666051, θ = 44.99973°, m = 0.373/8.69/49.53 meV, Σ = 58.59, |δ_ν − δ_l| = 0.26115 vs π/12 = 0.26180, 0.25 %); mode split 0.9515 : 0.0485.
*Confidence:* high.

**F11. canon §16, §24, §32.10, §32.13 Posit 6, §34 — the snakeskin.**
*Grade given:* CONJECTURE / RULING + one owed number / Posit 6. *Argon:* DEAD as stated.
*Problem:* (1) Energy and inventory: by v2 §7 a proton *is* its governor plus its e⁺; if the ν pair and e⁺ leave, a 938.272 MeV proton cannot also leave a 938 MeV hollow capsid — energy from nothing, and no Φ constituents remain to build it. (2) The Super-K bound τ(p → e⁺νν) > 1.7 × 10³² yr assumes no heavy remnant; with a ~937 MeV remnant the visible energy is ≲ 0.7 MeV (or the reaction is endothermic), so the bound doesn't apply as used. (3) The a⁻⁴ neutrino-bath drag extrapolated to today (0.17 meV) contradicts §10's non-relativistic 49.5 meV neutrinos, and would make protons near reactors or in the Sun (bath energy density > 10⁶ × CνB) disassemble far faster than in deep space. (4) The velcro threshold: ~3.6 × 10⁶ collisions at kT = 5 MeV need an activation barrier > 75 MeV to avoid coagulation, not 10 MeV.
*Blast radius:* high — §16, §24, §32.10, §32.13 Posit 6, §34 (Ω_DM/Ω_b = 5.4), v2 §16, fractal nucleus (carrier-less core capsid).
*Fix:* not small — specify what remains in an empty capsid with m_capsid ≤ m_p − m_e, or make the reaction endothermic so it switches off as e^(−Q/kT); raise velcro to > 75 MeV.
*Kill test:* proton stability in high-flux neutrino environments (KamLAND/Borexino); BBN yields if 84 % of protons disassemble at 5 MeV. *Truifier:* recoil kinematics of a neutral ~937 MeV particle with a > 75 MeV sticking threshold.
*Ran it:* yes — backward scaling arithmetic; collision count (barrier > 5 ln(3.6 × 10⁶) MeV = 75.5 MeV); reactor-ν energy density vs CνB.
*Confidence:* high.

**F12. canon §14 — c′ = 0.9534 vs the 50:50 deuteron split.**
*Problem:* at c′ = 0.9534 one lepton on an n = 2 lane sheds 1.11238 MeV = ½ BE(D); two leptons (s = 2) shed all of BE(D), leaving patch₁ = 0, not 0.563. Scenario B uses s = 1 for D but s = 3, 3, 4 for T, ³He, ⁴He. The 10 Oct banner says §7a supersedes c′, but the body still carries the inconsistent arithmetic.
*Argon:* CONSTRUCT — factor-2 error in s (superseded but unflagged). *Blast radius:* medium — §14, §34. *Fix:* replace stale numbers with the §7a/§7b values. *Confidence:* high.

**F13. canon §15, §32.13 Posit 7, §33.13, §34, §36.5 — the Nolen–Schiffer residual.**
*Claim:* "if the swap is one unit, the residual is the same number for every pair"; registered as Falsifier 13.
*Argon:* DEAD — falsified by existing data.
*Problem:* the table has existed since Nolen & Schiffer (1969, Ann. Rev. Nucl. Sci. 19, 471; also Shlomo 1978, Rep. Prog. Phys. 41, 957). The residual is roughly a constant *fraction* (~7 %) of the Coulomb displacement energy ∝ Z/A^1/3: ~0.07 MeV at A = 3, ~0.13 at ⁷Li, ~0.25–0.30 at A = 15–17, ~0.42 at ²⁷Al, ~0.54–0.60 at A = 39–41, with 100–200 keV steps at shell closures. Under §14's own U_pp = 0.856 MeV, A = 3 gives −0.092 MeV (negative) while heavier pairs are positive and hundreds of keV.
*Fix:* strike "constant per swap"; in a contact/lane model a p↔n swap changes Z pp pairs, so the residual scales as Z/R.
*Truifier:* derive the ~7 % scaling and shell steps from the n/p capsid radius difference (0.86 vs 0.8409 fm, ~2.3 %).
*Ran it:* yes — rises ~70 keV → ~600 keV, ~8.5×. *Confidence:* high.

**F14. canon §12, §13, §32.13 Posits 1 & 3, §34 — bound-neutron stability and the two-stage decay.**
*Grade given:* POSIT (§12); CONJECTURE, four retrodictions (§13). *Argon:* CONJECTURE.
*Problem:* (1) If an intermediate state lived between the e⁺ exit and the e⁻ ejection for even ħ/Q_β ≈ 8.4 × 10⁻²² s, Stage 1 would be a two-body decay with a monoenergetic line, not the observed continuous three-body Fermi spectrum. (2) Bound neutrons in ⁶He and ⁸He share lanes yet decay in 0.807 s and 0.119 s — 1000–5000× faster than free — because Q_β = 3.508 and 10.65 MeV: Sargent's phase-space rule, which §9 already accepted for the muon. D is stable because Q_β < 0, not lane detuning. (3) The a-coefficient dependence: velocity-linear vs momentum-linear angular term distorts across the spectrum by 2.53×.
*Blast radius:* medium-high — §12, §13, §32.13, §34.
*Fix:* attribute bound stability to phase space; require the two stages to be one coherent transition (Δt ≪ ħ/Q_β).
*Kill test:* fit aSPECT's recoil spectrum with a momentum-linear angular term. *Truifier:* derive λ = g_A/g_V = 1.2754 (a = −0.1059) and 878.4 s from the octahedron → tetrahedron matrix element plus Fermi phase space.
*Ran it:* yes. *Confidence:* high.

**F15. canon §32.13 Posit 5 — "governors can run down".**
*Problem:* contradicts §16 ("protons have been frictionless since 30 ms"), and any continuous internal age variable makes protons distinguishable, abolishing the antisymmetrisation behind ortho/para-hydrogen.
*Argon:* DEAD. *Kill test:* pure para-H₂ from protons of mixed history exists. *Confidence:* high.

**F16. canon — internal collisions from integration.**
*Problem:* (a) §35/§36.7 predict a 5–10 % chromatic EHT ring-size shift (230 → 345 GHz) while §25/§32.11a adopt an achromatic river metric with γ = 1. (b) §20 gives our CMB speed as 370 km/s while §25 quotes 8.2 ppm computed from 627 km/s. (c) §23 writes δ > ε/(C/M), §29 writes δ > ε/C.
*Argon:* INTERNALLY INCONSISTENT. *Fix:* retire the chromatic ring shift; update §25 to 6.8 ppm / 93 kyr; standardise δ.
*Ran it:* yes — VLBI (Fomalont et al. 2009) and Gaia optical deflection agree with achromatic γ = 1 across five decades in frequency; EHT/GMVA shadow diameters achromatic at ~40–42 μas. *Confidence:* high.

**F17. canon §9, §11, §31, §34 — four omissions in the particle model.**
*Problem:* (1) Deep-inelastic scattering: Bjorken scaling, Callan–Gross, and three fractional-charge spin-½ partons (Gottfried sum) — never addressed for a single-carrier 0.84 fm capsid. (2) No selection rule forbids e⁺e⁻ → 2γ on the neutron's counter-rotating lane (two crossings per orbit, ~10²³ /s, at far above positronium density). (3) §9's "scattering probes the field, not the core" does not clear high-energy contact-interaction bounds (Λ > 10 TeV, R_core < 2 × 10⁻²⁰ m). (4) The Foldy term is conditional on first deriving μ_n = −1.913 μ_N.
*Argon:* OWED. *Blast radius:* high.
*Kill test:* a charge on a shell of radius 0.8409 fm has G_E = sin(QR)/(QR), with a zero at Q = π/R = 0.737 GeV/c (Q² = 0.543 GeV²); measured G_E is smooth and positive past 8 GeV².
*Ran it:* yes. *Confidence:* high.

**Document 2 — what is wrong (Argon).** Koide's equipartition gap (F10). The snakeskin's energy budget, Super-K misuse, a⁻⁴ drag, and velcro threshold (F11). §14's factor-2 in s (F12). Nolen–Schiffer already falsified (F13). Bound-neutron stability and the two-stage spectrum (F14). Posit 5 (F15). Integration collisions (F16). Carried forward: F1, F3, F4, F6, F7, F8, F9.

**What is missing.** Form factors and DIS for a shell capsid; a 2γ selection rule for the neutron lane; compositeness bounds for the crystalline electron; the linear-√m premise in §10 (F10, F17).

**What is fine — stop re-examining.** The honesty audits in §9, §14, §17, §35 — disowning the 9-constant binding calculator, flagging nuclear-binding-v4 §V, correcting g = 2 to ASSERTED (gyromagnetic theorem gives g = 1), retracting the geometric muon lifetime for Sargent, killing V′3V via propyne and methane: "rigorous, courageous, and 100 % sound." All §10 Koide/Brannen arithmetic. The Foldy arithmetic (−0.1266 fm², leaving +0.0105 against −0.1161) and U_pp = 0.8562 MeV. The §13 octahedron → tetrahedron diagonal slide. The twisted-line-bundle restatement in §3 and named tensions #1 and #2.

**Prior art — Document 2.**

| move | closest prior art | reproduced | new here |
|---|---|---|---|
| spin-½ from tethered rotation | Battey-Pratt & Racey (1980, IJTP 19, 437) — cited; Dirac belt; Zitterbewegung | SU(2) double cover; antiperiodic BC | tying BP&R's 2ω : ω core/medium to the Koide angle |
| Koide geometry, signed neutrino branch, π/12, 58.6 meV | Koide (1981); Foot (1994, hep-ph/9402242); Brannen (2006) | *all* §10 numbers | π/12 as the domain step of the binary octahedral group 2O; the BP&R partition for θ |
| nucleons as leptonic composites | pre-1932 proton–electron model; Barut (1979–80) | quark-free leptonic nucleons | n = 2 tetra vs n = 3 octa governors; the two-stage square-saddle β-decay |
| neutron charge radius ≈ Foldy | Foldy (1952); Bawin & Coon (1999); Atac et al. (2021, Nature 590, 57) | the decomposition | using the small +0.01 fm² remainder to choose balanced lanes |
| Kelvin-cell nucleons; tetrahedral α packing | Skyrmion crystals (Klebanov 1985; Battye & Sutcliffe 1997–2006); Pauling (1965); Brink (1966) | polyhedral faces; tetrahedral ⁴He; 3Nα − 6 | the three-term formula combining relativistic carrier deceleration with Kelvin face areas |
| asymmetric dark matter at m ≈ m_p, ratio 5.4 (§16) | Nussinov (1985, Phys. Lett. B); Kaplan, Luty & Zurek (2009, Phys. Rev. D 79, 115016, "Asymmetric Dark Matter"); Farrar (2003/2017, sexaquark / dark baryon at m ≈ 1.8–2 m_p) | motivating m_DM ~ m_p from Ω_DM/Ω_b ≈ 5.4 | identifying the dark particle as a de-governed hollow proton capsid formed when neutrino-bath drag decouples at kT ≈ 5 MeV (currently broken by energy conservation and collision rates; see F11) |
| deterministic guiding wave & early-universe non-equilibrium (§19) | de Broglie–Bohm pilot-wave theory (1927, 1952) and Valentini (1991, 2010) — both explicitly cited in §19 | the interpretive structure and falsifiability criterion | none yet (specific spectroscopic observable is marked [OWED]) |
| sentience as selective forgetting under a Markov blanket (§23, §27–29) | Friston's Free-Energy Principle & Active Inference (2010, 2019) — cited in §28; Information Bottleneck method (Tishby, Pereira & Bialek 1999, formalising optimal representation as selective compression/forgetting of irrelevant past information) | Markov-blanket surprise minimisation and selective information compression | defining S = {μ,i}a as a control system tuning the forgetting rate δ across context compaction |

---

## Document 3 — `three-term-binding.md`

*Argon's note:* F12 (inconsistent s) carries forward to §7–§8.

**F18. binding §7b — the tyre law.**
*Claim:* x = contacts/inflation, A = 1 − e^(−x/x₀), x₀ fixed on the deuteron; T +4.6 %, He-4 −0.7 %; Hertz −46 %.
*Grade given:* COMPUTED; CONSTRUCT-grade. *Argon:* DEAD.
*Problem:* (1) Unit mixing: the numerator is the extensive total bond count (1, 3, 6) and the denominator the intensive per-nucleon carrier count (1.5, 5/3, 1.5), giving x_D : x_T : x_He4 = 1 : 2.7 : 6; consistently per-nucleon it is 1 : 1.8 : 3, and the errors become −9.3 % and −8.3 %. (2) It is calibrated against §8c's superseded 50:50 split (A_D = 0.563) rather than §7a's active calibration (A_D = 0.0367), against which the curve misses T and He-4 by −88 % to −92 %. (3) ³He is omitted. (4) Patch-area residuals against §8c are reported as if total BE residuals against AME.
*Blast radius:* high — §7b, README, v2 §19 row 23, canon §14 banner and §16 ("wet limit of the tyre law").
*Confidence:* high — "exact numerical reproduction of the author's +4.6 % / −0.7 % / −46 %."

**F19. binding §7a — the T−³He split, Coulomb, and R6/R7.**
*Grade given:* DERIVED for the slingshot, conditional on R1–R7. *Argon:* CONSTRUCT — double-counts T−³He by +111 % unless Coulomb is discarded.
*Problem:* every §7a arithmetic line is exact (γ(c′) = 2.5310, c′ = 0.91864, Y(2,3,4) = 0.7181/0.7565/0.7683, D cap 0.9217, P = 1.9113). But (1) y = p + 2n gives T one more slowing carrier than ³He (+0.7565 MeV); add the R4 Coulomb U_pp = 0.856 MeV and BE(T) − BE(³He) = 1.613 MeV vs 0.764 measured, +111 %. Concluding U_pp ≈ 0 in T/³He contradicts R4, §4, §6 and Gauss, and fails heavier mirrors and ⁸Be. (2) R7 puts all of m_n − m_p into the extra carrier's γm_ec², leaving nothing for the neutron's third governor loop or inflation. (3) R6 ("N units at v/N inflate as 1 at v") conflates momentum with kinetic energy/centrifugal pressure.
*Blast radius:* high — §7a, README, canon §14, all A ≥ 5. *Confidence:* high.

**F20. binding §5, §6, §8 — touching capsids vs the deuteron radius.**
*Problem:* two capsids of rms radius 0.8409 fm face-to-face (d = 1.682 fm) give R_D = 1.189 fm, missing the tabled 2.128 fm by −44.1 %; 2.128 fm corresponds to a 3.92 fm separation, a 2.24 fm gap between surfaces.
*Argon:* GEOMETRICALLY INCOMPATIBLE. *Fix:* distinguish the contact configuration (occupied a small fraction of the time — which would explain §7a's 0.037-of-a-square face) from the rms wavefunction radius. *Confidence:* high.

**F21. binding §6, §7, §7a, §9 — three omissions before A ≥ 5.**
*Problem:* (1) Full pairwise Coulomb Σ αħc/r_ij: contact-only PP works at A ≤ 4 (all touch) but at ⁸Be the four non-contact inter-alpha pp pairs supply ≈ −2.06 MeV, which is what makes ⁸Be unbound by 92 keV. (2) No derivation of v_n = c′/n rather than de Broglie p_n = p₁/n (which changes γ by ~29 %). (3) Reconciling "capsid de-spin" (3m_pc²/256 = 10.995 MeV) with preserved nucleon spin-½ and magnetic moments.
*Argon:* OWED. *Blast radius:* high — including the registered Li-7 blind and §9.3's ⁸Be kill.
*Kill test:* run §9.3's ⁸Be (two tetrahedra on one square face) with §7a's rules. *Confidence:* high.

**Document 3 — what is wrong (Argon).** The tyre law's unit mixing and calibration (F18). §7a's T−³He double count and the abolition of Coulomb; R6/R7 (F19). Touching geometry vs R_D (F20). §8's inconsistent s (F12).

**What is missing.** Full Coulomb for A ≥ 5; a wave derivation of v = c′/n; de-spin vs spin-½; D's small face fraction as a residence-time fraction (F20, F21).

**What is fine — stop re-examining.** Kelvin-cell dihedral closure (125.26° + 125.26° + 109.47° = 360°) and face areas; he4_cross's 6 contacts and 12.392 square units. Every number in the §7 slingshot table and the §7a computed block "to the last printed digit." The 9 Sep statistical audit in §8c–d (three parameters on four nuclei leave one degree of freedom, which is the ³He Coulomb split restated) and the deletion of the least-squares solver — "exemplary scientific hygiene." The neutron inflation bracket [1.000, 1.260] and the 1.023 ratio at the stiff end.

**Prior art — Document 3.**

| move | closest prior art | reproduced | new here |
|---|---|---|---|
| nucleons as space-filling polyhedra | Skyrmion crystals (Klebanov 1985; Battye & Sutcliffe); Pauling spheron model (1965, Science 150, 297); Cook & Dallacasa (1987) | polyhedral packing; tetrahedral ⁴He; face counting at A = 2–4 | generating the ⁴He cliff purely from the Kelvin cell's hexagon-vs-square face split |
| binding from shared carriers decelerating on lanes | Heitler–London / Wheeler exchange; pre-1932 models; Barut | delocalisation lowering kinetic energy | Y(n) = m_ec²[γ(c′) − γ(c′/n)] with c′ pinned by m_n − m_p |
| thin-shell rotational energy 10.995 MeV | rigid-rotor / Skyrmion quantisation (Adkins, Nappi & Witten 1983) with R = 4ħ/m_pc | classical shell rotational energy | holding it in reserve as "capsid de-spin" for A ≥ 5 |

---

## Document 4 — `the-fractal-nucleus.md`

*Argon's note:* F1, F18, F19, F20, F21 carry forward.

**F22. fractal §3, §4, §10 — "the triangles do not touch".**
*Claim:* four O-16 tetrahedra sharing one apex, azimuths optimised: nearest inter-triangle alphas 1.076 d apart, "no overlap … the triangles do not touch each other."
*Grade given:* COMPUTED. *Argon:* DEAD.
*Problem:* §3 maximised the *minimum* clearance (≈ 1.076–1.086 d) and concluded no contact is possible. But the clearance varies continuously with an equal chiral twist δ, from 0.667 d (δ = −60°) to 1.086 d (δ = 21.47°), so by the intermediate value theorem exact 1.000 d contact with zero overlap exists. At **δ = 26.84°** all six hexagon–hexagon edges of the chiral truncated tetrahedron are exactly 1.00000 d, next-nearest pairs 1.1301 d: **30 exact α–α contacts** (12 core + 12 intra-triangle + 6 inter-triangle). At δ = 0 the twelve form a regular cuboctahedron: 36 contacts, zero overlap.
*Consequence:* 4·BE(O-16) − 3·BE(α) = 425.6 MeV is the unlinked 24-bond baseline; it under-predicts the measured 447.7 MeV by 22.1 MeV until the six inter-triangle bonds close (+14.4 MeV → 440.0 MeV). The 2.406 MeV/bond is algebraically O-16's own residual divided by 6.
*Blast radius:* high — §3, §3a, §4, §10 dead row 2.
*Ran it:* yes — all 78 pair distances at δ = 26.841°: minimum exactly 1.00000 d, 30 contacts. *Truifier:* high-q ⁵²Fe(e,e′) form factor showing tetrahedral cluster moments.
*Confidence:* high.

**F23. fractal §6, §9 — fe56_star.**
*Problem:* the arithmetic is exact (382.98 sq-units; 668.3 MeV, +35.8 %; −12.2 % → −1.08 % shape cancellation; g = 0.213). Three contradictions: (1) P = 1.912 was calibrated with U_pp ≈ 0 (F19), yet −126 MeV of liquid-drop Coulomb is subtracted; contact-only PP on the build's 35 pp contacts gives only 30 MeV. (2) The slingshot uses the n = 2 deuteron value Y(2) = 0.7181 for all 86 carriers (61.8 MeV) rather than Y(4) or Y(56). (3) All 28 first-shell sites are neutrons and all 24 outer sites protons: 103 n–n bonds in a pure-neutron interior and a neutron skin of ≤ −1.0 fm (wrong sign, 25× too large) against +0.03 to +0.05 fm measured.
*Argon:* CONSTRUCT. *Fix:* execute the flagged species re-rule so n and p alternate across shells; use exact pairwise Coulomb throughout.
*Ran it:* yes — R_n = 2.233 fm vs R_ch ≥ 3.2 fm on the BCC lattice. *Confidence:* high.

**F24. fractal §4, §3a, §8 — the alpha ladder omits inter-alpha Coulomb.**
*Claim:* "With q = 2.425 MeV fixed once on C-12 and the ladder's 3Nα − 6 edges, the residual binding after the alphas: ... Fe-52 | 13 | 79.85 | 33 | 32.9 | +0.2 %; Ni-56 | 14 | 87.85 | 36 | 36.2 | −0.6 %."
*Type:* omission. *Grade given:* COMPUTED; P-type. *Argon:* CONSTRUCT — omits ~115–140 MeV of inter-alpha Coulomb repulsion; 3Nα − 6 diverges above Nα = 14.
*Problem:* All numbers in the §4 table are arithmetically exact against AME 2020. However, tagging the table P-type omits why a purely linear formula BE_res(Nα) = (3Nα − 6)q with zero inter-alpha Coulomb term crosses the experimental curve near Nα = 10–14. A single α contains 1 proton–proton pair, whereas a nucleus of Nα alphas (Z = 2Nα) contains Nα(2Nα − 1) proton–proton pairs — adding 2Nα(Nα − 1) inter-alpha proton–proton pairs (312 pairs in ⁵²Fe, 364 pairs in ⁵⁶Ni) that cost ΔE_C ≈ 115–140 MeV of electrostatic repulsion. In 3D packing, attractive nuclear contact energy grows faster than the hollow-shell planar graph count 3Nα − 6, while omitted Coulomb repulsion grows as −a_C Z²/A^(1/3) ∝ −Nα^(5/3); the two omitted terms cross near Nα = 12–14. Above Nα = 14, because (3Nα − 6)q lacks Coulomb repulsion, it predicts that N = Z alpha nuclei continue gaining +3q = +7.275 MeV per alpha forever (contradicting §3a's own statement that heavy 1:1 shells fail electrically), over-predicting the residual of ⁸⁰Zr (Nα = 20) by +25.9 % (130.9 MeV vs 104.0 MeV measured) and ¹⁰⁰Sn (Nα = 25) by +41.9 % (167.3 MeV vs 117.9 MeV measured).
*Blast radius:* medium — §4 and `specs/alpha-ladder.md`.
*Fix:* state explicitly in §4 that q = 2.425 MeV is an effective net (nuclear minus Coulomb) bond value that holds only where 3D coordination gain compensates ∝ Nα^(5/3) Coulomb growth (Nα ≤ 14), and cannot be extrapolated without an explicit Coulomb term.
*Kill test:* evaluate (3Nα − 6)q at Nα = 20 (⁸⁰Zr) and Nα = 25 (¹⁰⁰Sn) against AME 2020 masses. *Truifier:* separate the bare α–α nuclear contact energy q₀ from the inter-alpha Coulomb sum Σ (4αħc / R_AB) over 3D cluster coordinates and show it reproduces both Nα ≤ 14 and the N = Z proton-drip turnover at ¹⁰⁰Sn.
*Ran it:* yes — ⁸⁰Zr (Nα = 20): 54q = 130.94 MeV vs BE(⁸⁰Zr) − 20 BE(α) = 669.9 − 565.9 = 104.0 MeV (+25.9 %); ¹⁰⁰Sn (Nα = 25): 69q = 167.32 MeV vs 825.3 − 707.4 = 117.9 MeV (+41.9 %).
*Confidence:* high.

**F25. fractal §3a, §7, §10 — Mackay's 10n² + 2 shell series vs §10's kill; the Bi-209 row slip; and the modular tautology of "left over = 0".**
*Claim:* "The series is Mackay's 1, 13, 55 units (shells of 10n² + 2), times four" (§3a); "The Mackay/cuboctahedral shell series in units of four: 1, 13, 55, 147 units... Pb-208 | 82 | 126 | 41 | 11 | 52 | 0; Bi-209 | 83 | 126 | 41 | 10 | 51 | 5" (§7); "icosahedral or cuboctahedral 1 + 12 for iron | killed by 42 / 36 bonds" (§10).
*Type:* commission. *Grade given:* FACT for the series; COINCIDENCE for lead; FITTED for uranium. *Argon:* INTERNAL CONTRADICTION (uses Mackay's icosahedral/cuboctahedral formula after killing both in §10); ARITHMETIC SLIP on Bi-209; MODULAR TAUTOLOGY on "left over = 0".
*Problem:* Three distinct issues occur in §3a and §7: (1) Geometric contradiction between §3a/§7 and §10: Mackay's 10n² + 2 shell formula (12 units at n = 1, 42 units at n = 2, giving cumulative totals 1, 13, 55, 147) is the exact vertex count of concentric icosahedra or cuboctahedra. Yet §10 (Dead row 2) explicitly kills both the icosahedron and cuboctahedron at n = 1 in favour of §3's truncated-tetrahedron star (4 triangular faces + 4 hexagonal faces), which does not have 12 identical five-fold/four-fold vertices and does not generate a 42-unit Mackay second shell. (2) Arithmetic error in §7's Bi-209 row: For ²⁰⁹Bi (Z = 83, N = 126), taking ⌊83/2⌋ = 41 alphas uses 82 protons and 82 neutrons, leaving 1 proton and 126 − 82 = 44 neutrons. Grouping those 44 neutrons into four-neutron tetrads gives 44 / 4 = 11 tetrads (not 10), for 41 + 11 = 52 units (not 51) and 1 proton left over (not 5). (3) Modular-arithmetic tautology of "zero left over": Under the §7 rule (alphas = ⌊Z/2⌋, tetrads = ⌊(N − 2·alphas)/4⌋), "left over = 0" holds if and only if Z is even and N − Z ≡ 0 (mod 4) (equivalently, Z even and A ≡ 0 (mod 4)). Thus 100 % of even-even nuclides with A ≡ 0 (mod 4) across the entire chart of nuclides — including every even-even A = 208 isobar (²⁰⁸Hg = 40α + 12 tetrads, ²⁰⁸Pb = 41α + 11 tetrads, ²⁰⁸Po = 42α + 10 tetrads, ²⁰⁸Rn = 43α + 9 tetrads) — automatically have "52 units, 0 left over".
*Blast radius:* low-medium — §3a, §7, §8 Falsifier 5, and `README.md` ("Pb-208 = 52 units").
*Fix:* correct the Bi-209 row in §7 to `41 | 11 | 52 | 1`; acknowledge that `left over = 0` is a modular identity for all even-Z, A = 4k nuclei (so ²⁰⁸Pb must be distinguished from ²⁰⁸Hg and ²⁰⁸Po by binding energy, not unit-remainder counting); and derive the actual second-shell site count of the truncated-tetrahedron / BCC star rather than importing Mackay's icosahedral 10n² + 2 = 42 count.
*Kill test:* check whether `units = 52, left over = 0` distinguishes doubly-magic ²⁰⁸Pb (Z = 82, N = 126) from unstable ²⁰⁸Hg (Z = 80, N = 128) or ²⁰⁸Po (Z = 84, N = 124). *Truifier:* show from the 3D packing of 52 four-nucleon units that placing exactly 11 neutral tetrads and 41 charged alphas uniquely maximises BE − E_Coulomb at Z = 82, N = 126.
*Ran it:* yes — for ²⁰⁹Bi (Z = 83, N = 126): 83 − 2(41) = 1p, 126 − 2(41) = 44n = 11 × (4n) + 0n ⇒ 41 alphas + 11 tetrads = 52 units, remainder 1 (41×4 + 11×4 + 1 = 209).
*Confidence:* high.

**F26. fractal §3b, §4, §5, §8 Falsifier 3 — neutron capture and separation energies follow the N = 28 magic isotone line, not the N = Z + 4 pocket line.**
*Claim:* "alphas build the N = Z spine ... then neutrons fill the pockets — one at a time, into the four-fold sites of §5 ... the one number it predicts is that neutron capture should be favoured at the pocket sites, which is a statement about capture cross-sections along the N = Z + 4 line nobody has made in these terms." (§3b)
*Type:* commission. *Grade given:* POSIT ("the one number it predicts"). *Argon:* CONTRADICTED BY DATA — stability and capture cross-section steps follow the fixed magic neutron number N = 28 across isotones, not the four-pocket line N − Z = 4.
*Problem:* Section 3b and §5 attribute the stability of ⁵⁶Fe (Z = 26, N = 30 = Z + 4) to four extra neutrons filling the four deep triple-contact pockets around the 4-nucleon core, and predict a signature along the N = Z + 4 line (⁴⁸Ti, ⁵²Cr, ⁵⁶Fe, ⁶⁰Ni). In experimental nuclear data across Z = 20..28 (AME 2020 separation energies and KADoNiS kT = 30 keV stellar (n,γ) cross-sections, Bao et al. 2000), the shell closure and capture bottleneck do not track the four-pocket excess N − Z = 4; they track the fixed magic neutron number N = 28 (the 1f₇/₂ shell closure):
1. At Iron (Z = 26), the magic N = 28 nucleus is ⁵⁴Fe (N = Z + 2, only two extra neutrons past ⁵²Fe, not four): the two-neutron separation energy is highest at ⁵⁴Fe (S₂n = 24.06 MeV) and drops sharply by 3.56 MeV when adding the 3rd and 4th neutrons to make ⁵⁶Fe (S₂n = 20.50 MeV), while the 30 keV (n,γ) cross-section drops from σ(⁵⁴Fe) = 29.6 mb to σ(⁵⁶Fe) = 11.7 mb.
2. At Chromium (Z = 24), N = Z + 4 happens to coincide with N = 28 at ⁵²Cr, where σ(⁵²Cr) = 8.8 mb is a sharp local minimum (closed-shell capture bottleneck).
3. At Titanium (Z = 22), the shell closure and cross-section minimum occur at ⁵⁰Ti (N = 28 = Z + 6, six extra neutrons, not four), where S₂n(⁵⁰Ti) = 19.08 MeV drops by 4.90 MeV to S₂n(⁵²Ti, N = 30) = 14.18 MeV and σ(⁵⁰Ti) = 3.4 mb is a deep minimum compared to σ(⁴⁸Ti, N = Z + 4) = 26.3 mb.

*Blast radius:* low-medium — §3b, §4, §5, and §8 Falsifier 3.
*Fix:* acknowledge that across Z = 20..28 the empirical shell cliff and (n,γ) minimum track total neutron number N = 28 rather than neutron excess N − Z = 4, which means the §8 Falsifier 3 dilemma ("Either the four-site motif recurs on 11, 12 and 14 alphas or the pockets are not why iron has four") is already decided against a core-only 4-pocket excess.
*Kill test:* compare S₂n(Z, N) and 30 keV ⟨σ_{n,γ}⟩ along fixed N − Z = 4 (⁴⁸Ti, ⁵²Cr, ⁵⁶Fe, ⁶⁰Ni) versus fixed N = 28 (⁵⁰Ti, ⁵²Cr, ⁵⁴Fe, ⁵⁶Ni). *Truifier:* show how the BCC site count produces a 28-neutron closed shell (core 2n + first-shell 26n = 28n!) independent of Z.
*Ran it:* yes — AME 2020 S₂n drops across N = 28 → 30: Ti (19.08 → 14.18 MeV, Δ = −4.90 MeV at N − Z = 6 → 8), Cr (21.30 → 16.23 MeV, Δ = −5.07 MeV at N − Z = 4 → 6), Fe (24.06 → 20.50 MeV, Δ = −3.56 MeV at N − Z = 2 → 4); KADoNiS 30 keV σ_{n,γ} minima all sit at N = 28: σ(⁵⁰Ti) = 3.4 mb, σ(⁵²Cr) = 8.8 mb.
*Confidence:* high.

**F27. fractal §8 Falsifier 1, §9 — the gate is too wide and Ca-40 is underspecified.** *[Restored cleanly by Argon.]*
*Problem:* (1) ±10 % on Ni-56 (484.0 MeV) and Ca-40 (342.1 MeV) is ±48 / ±34 MeV. The whole truck-stack correction is −177 MeV, so the gate passes any g ∈ [0.155, 0.271] (±27 %), and even a flat BE/A = 8.0 MeV passes both (−7.4 %, −6.5 %). (2) Ca-40 = 4 + 28 + 8 leaves C(24, 8) = 735,471 seatings of the outer eight unless a rule is pre-registered.
*Type:* omission. *Argon:* UNDERSPECIFIED. *Fix:* gate at ±2 % (±7–10 MeV); pre-register the seating (e.g. the 8 double-contact partner sites).
*Kill test:* toasm on Ca-40 and Ni-56 with pre-registered seating, P = 1.912, g = 0.213, exact pairwise Coulomb, ±2 % gate.
*Ran it:* yes — sensitivity on §6's layer areas: ±10 % allows Δg = ±0.058; ±2 % restricts Δg to ±0.011. *Confidence:* high.

**Document 4 — what is wrong (Argon).** The "do not touch" claim (F22). 425.6 MeV is the unlinked baseline (F22). fe56_star's Coulomb, lane-length and charge-inversion contradictions (F23). Mackay's series used after its polyhedra were killed; the Bi row; the trivial "left over" (F25). The N = Z + 4 capture line (F26).

**What is missing.** Inter-alpha Coulomb in the ladder (F24). A tight gate and a deterministic seating rule for Falsifier 1 (F27).

**What is fine — stop re-examining.** Every BCC site, port and pocket count around he4_cross in §5 (44 ports → 28 sites: 16 single, 8 double, 4 triple pockets at 2a and √11 a). The truncated-tetrahedron circumradius ratios (1.1726, 0.8528). Every AME residual and four-neutron separation in §4, and the 15 Oct C-12 tautology note. The shape-cancellation proof and g = 0.213 arithmetic. The §10 kills (Fe-56 as 14 alphas; Grace's 3× and 36 → 18 %; 8 × Be-8 = 50; U-238 = 55 + 18 as a two-parameter fit; the truncated tetrahedron as a space-filler — Chen, Engel & Glotzer 2014 reached 207/208, not 1).

**Prior art — Document 4.**

| move | closest prior art | reproduced | new here |
|---|---|---|---|
| alpha-cluster polyhedra; 3Nα − 6 bonds | Wheeler (1937); **Hafstad & Teller (1938, Phys. Rev. 54, 681)** — the 3Nα − 6 table with constant α–α bond, ⁸Be to ⁴⁰Ca; Dennison (1940); Bijker & Iachello (2014, PRL 112, 152501) | triangular C-12, tetrahedral O-16, unbound ⁸Be, the linear table | extending to Nα = 13 (⁵²Fe) and 14 (⁵⁶Ni); ⁵²Fe as four O-16 sharing one alpha |
| shells of clusters; spheron packing to Pb | Mackay (1962) — cited; Pauling spheron model (1965, Science; PNAS 54, 989); Cook & Dallacasa (1987) | Mackay counts; Pb as α plus neutron clusters | BCC Kelvin port convergence around he4_cross (44 → 28 with 4 triple pockets); fe56_star |
| the truck stack (layer flattening) | Weizsäcker surface term (1935) — acknowledged; Finnis–Sinclair coordination weakening | ~177 MeV surface reduction | expressing it as overburden flattening (1 − g·layer) on contact patches |

---

## Document 5 — `the-turtle-conjecture.md`

*Argon's note:* F1, F3, F4, F5, F18, F19 carry forward.

**F28. turtle §3 step 5, §3b, §5a, §7 rows 1–1′ — G ≈ c⁴/kR_H and the lockstep defence.**
*Grade given:* COMPUTED; THEOREM given step 3; paid at ballpark. *Argon:* COINCIDENCE / RETRODICTION at t = t₀.
*Problem:* every §3b number is exact. But dimensionless ratios are invariant under conformal rescaling, so Wetterich's frame cannot make the relation time-independent. Written dimensionlessly, kR_H G/c⁴ = (k λ̄_p²/m_pc² ≈ 1/7500) × (ħc/Gm_p² ≈ 1.7 × 10³⁸) × (ħH(t)/m_pc² … ≈ 1.5 × 10⁻⁴² today). The first two are bounded constant since BBN (Oklo, pulsars, LLR); the third changes by ~17 orders between BBN and today. So the ratio is ~2 × 10⁴ at recombination, ~4 × 10¹⁷ at BBN, and ~1 only now.
*Blast radius:* high — §3 steps 3–5, §3b, §5, §5a, §7, §8 F5, README.
*Fix:* strike the claim that lockstep/Wetterich makes it time-independent.
*Truifier:* replace R_H with the asymptotic de Sitter horizon R_Λ = √(3/Λ) = 1.65 × 10²⁶ m: then c⁴/(GR_Λ) = **4.58 MeV/fm², inside k = 2.84–5.41**, and the relation becomes a genuine constant tied to Λ.
*Ran it:* yes (both the epoch values and the de Sitter number). *Confidence:* high.

**F29. turtle §2, §3 steps 1–3, §7 rows 2 & 4, §8 F4 — the tripod.**
*Grade given:* GEOMETRIC IDENTITY; CONDITIONAL THEOREM; THEOREM given tension. *Argon:* CONJECTURE — four errors.
*Problem:* (1) A tetrahedron is a 3-simplex; tip its apex into time and the three remaining vertices span only a 2D plane. 3 + 1 needs five vertices (a 4-simplex). (2) §2 uses a Euclidean (++++) metric; in Minkowski (−+++) the base vertices are at spatial distance 0.943R, the interval to the centroid is +7R²/9, and base-to-apex is timelike — "all four at R" and c = 1 from regularity do not survive. (3) Step 1 conflates internal circulation (which produces rest mass) with centre-of-mass clock dilation. (4) An unattenuated one-third-tick boundary condition in Laplace, summed over the Milky Way's ~10⁶⁹ nucleons at 8 kpc, gives |Φ|/c² ≈ 1.3 × 10³³ vs 6.0 × 10⁻⁶ — off by 2.2 × 10³⁸, which is exactly ħc/Gm_p².
*Fix:* keep all four vertices in space; let time be the tetrahedron's worldline; include the attenuation (ℓ/R_p)² ≈ 5.9 × 10⁻³⁹ so one proton's boundary lag is ~10⁻³⁹ tick, not 1/3.
*Ran it:* yes. *Confidence:* high.

**F30. turtle §3c — the funnel conform on the chorus slice.**
*Problem:* despite the new Lemaître/PG paragraph, three coordinate-vs-proper errors remain. (1) On a chorus slice (dt_PG = 0, flat), a static capsid moving upstream at v_esc is Lorentz-*contracted* radially, Δr = L₀ cos θ — the opposite of "radial lobe × sec θ" (sec θ is the static Schwarzschild g_rr factor on a slice of constant static time). §6a ("everything pancakes") states the correct cos θ → 0. (2) A boost is not diag(cos θ, sec θ); it has γ = sec θ on the diagonal and −γβ = −tan θ off it. (3) sec θ → ∞ on one axis gives a 1D needle; contraction cos θ → 0 gives a 2D cross only if the tetrahedron's bimedian is radial.
*Argon:* CONSTRUCT. *Fix:* state clock rate cos θ and radial width L₀ cos θ on the chorus slice (pancaking to a cross at the horizon with the bimedian radial); sec θ is the number of pancaked capsids per unit coordinate interval.
*Ran it:* yes — static rod in PG: Δr at dt_PG = 0 is L₀ cos θ. *Confidence:* high.

**F31. turtle §3, §9, §10 — Gm_p²/R_p.**
*Problem:* at 0.8409 fm, Gm_p²/R_p = 1.39 × 10⁻³⁶ MeV (= 1.39 × 10⁻³⁰ eV). "10⁻³⁰ MeV" mislabels eV as MeV, a factor 10⁶. Strengthens the conclusion.
*Fix:* 1.4 × 10⁻³⁶ MeV; "thirty-six orders." *Confidence:* high.

**F32. turtle §6a — mass inflation and the Planck floor.**
*Problem:* (1) Poisson–Israel (1990) mass inflation is an inner-Cauchy-horizon instability of charged/rotating holes; it does not exist in Schwarzschild. The τ^(−2/3) Kasner stretching near r = 0 is Weyl tidal blueshift. (2) In ω = c³/2GM, M is the hole's mass, giving the macroscopic horizon frequency (c/ω = r_s ≈ 30 km) — 39 orders below a nucleon's. The single-loop Planck cap needs m_loop = ħω/c². (3) N ~ 10⁵⁷ nucleons reach Planck density collectively at the macroscopic Planck-star radius R_core ≫ ℓ_P (Rovelli–Vidotto).
*Argon:* CONJECTURE. *Fix:* "Kasner tidal blueshift" (or Kerr's inner horizon); use m_loop; say whether the core halts at the collective or single-loop radius (§7 row 5).
*Ran it:* yes — N loops of size ℓ_P at one per ℓ_P³ give R_core ~ N^(1/3) ℓ_P, matching Rovelli–Vidotto's scaling. *Confidence:* high.

**F33. turtle §3a, §8 F7 — a PBH edge at 2.5 × 10¹³ kg.**
*Problem:* the tidal number is exact, but a flattened capsid still adds its full mc² to M, so infall conformation cannot make an edge in dN/dM. Post-formation ISM accretion changes M by ~2 × 10⁻²⁵ over 13.8 Gyr. Hawking evaporation sets its own cutoff near 5 × 10¹¹ kg.
*Type:* omission. *Argon:* UNOBSERVABLE as stated.
*Fix and truifier:* at M = 2.5 × 10¹³ kg the Hawking temperature is **0.424 MeV — right at the capsid/electron scale.** Restate F7 as a channel threshold in the Hawking spectrum of an evaporating PBH at T_H ≈ 0.5–0.78 MeV (M ≈ 1.5–2.5 × 10¹³ kg), rather than the standard QCD threshold at ~150 MeV.
*Ran it:* yes. *Confidence:* high.

**Document 5 — what is wrong (Argon).** Lockstep cannot make G ≈ c⁴/kR_H time-independent (F28). The tripod loses a spatial dimension, uses a Euclidean metric, conflates circulation with dilation, and over-predicts the Galactic potential by 10³⁸ (F29). sec θ on the chorus slice should be cos θ (F30). 10⁻³⁰ MeV is 10⁻³⁰ eV (F31). Mass inflation is not Schwarzschild; ω = c³/2GM uses the wrong mass (F32).

**What is missing.** The boundary attenuation (ℓ/R_p)² in step 3 and §7 row 4 (F29). An observable for the 2.5 × 10¹³ kg scale — the 0.42 MeV Hawking threshold (F33). R_Λ = √(3/Λ) in place of R_H (F28).

**What is fine — stop re-examining.** Every output of `stiffness_ratio.py`. The regular-tetrahedron Euclidean geometry (0.816a, 0.612a, R/3, 109.47°). The 2.5 × 10¹³ kg tidal threshold and the neutron-star strain; the equivalence-principle kill of horizon flattening — "rock solid." The §3c table after the factor-2 fix (all six rows). The Kasner exponents and the echo regrade (a horizon receding at c is a perfect absorber). Every §9 kill.

**Prior art — Document 5.**

| move | closest prior art | reproduced | new here |
|---|---|---|---|
| lag from a fixed 4-velocity budget | Epstein (1981) — cited; Minkowski (1908) | dτ/dt as projection of a constant-speed budget | deriving the lag from the tetrahedron's 3 : 1 lobe split (missing the (ℓ/R_p)² factor, F29) |
| gravity as vacuum elasticity, G = c³ℓ²/ħ | Sakharov (1967) — cited; Kleinert, world crystal (1987); Padmanabhan (2010) | G as an emergent modulus at a cutoff | the cutoff element as the n = 2 tetrahedron; maximum slope c as the per-link deadline |
| nuclear tension ≈ c⁴/GR_H | Dirac (1937), Dicke (1961), Wetterich (2013) — cited; **Weinberg's pion-mass relation (1972, Gravitation and Cosmology, eq. 16.4.2), algebraically identical** | the coincidence | stating it as an equality of 2D surface tensions between the ⁴He patch and the Hubble capsid |
| funnel conform, E = E₀ cos θ | PG, Lemaître, Hamilton–Lisle; **Flamm's paraboloid (1916), whose embedding slope is exactly √(1 − r_s/r)** — cited | lapse/redshift and Flamm tilt | reading Flamm's angle as the shear of a nucleon tetrahedron toward a cross |
| BH interior: Kasner → Planck core / rimmed hole | Kasner (1921); BKL (1970); Thorne–Price–Macdonald (1986); Mazur–Mottola (2004); Mathur (2005); Rovelli–Vidotto (2014) — cited | Kasner exponents, membrane freezing, non-singular core | Kasner compression forcing the repulsive-lobe tetrahedron to align and unwind (3D → 2D → 1D, n = 2 → n = 1) as the mechanism of canon §26's recycler |

---

## Argon's own corrections and offers, recorded

Argon's "ran it" claims, the specific citations it supplied (Hafstad & Teller 1938; Nolen & Schiffer 1969; Shlomo 1978; Fomalont et al. 2009; Weinberg 1972 eq. 16.4.2; Chen, Engel & Glotzer 2014; Bijker & Iachello 2014; Atac et al. 2021; Bawin & Coon 1999; Barut 1979–80; Brannen 2006; Foot 1994), and every numerical result above are **as Argon reported them and have not yet been checked**. That is the next pass.
