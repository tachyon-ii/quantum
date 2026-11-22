# Adversarial recomputation of `review/2026-11-17/RUN-ALL-four-to-blockers.md`

Independent reviewer (Claude Fable 5.2, sub-agent). All "recomputed" values come from my own scripts in the session outputs folder, `feynman/` (`a_mirror.py`, `b_lw.py`, `c_bmt.py`, `d_lanes.py`); none of the note's scripts was re-run. Inputs shared with the note: AME2020 via `models/kernel/data.py`, and the saved cluster geometries `nz_geom_kappa*.json` (read, not regenerated).

Counts (35 rows): 22 confirmed · 1 wrong · 7 over-claimed · 2 unsupported · 3 not checked. Two of the confirmed rows carry a wording or last-digit error (28, 35).

## Table

| # | claim | their value | recomputed | verdict |
|---|---|---|---|---|
| **§1** | | | | |
| 1 | Be-8, all six rules, singles refused (BE and S) | S = −1.46 / +4.19 / +1.71 / +0.62 / +7.32 / +1.06 | identical to 2 d.p., own enumerator, no translation box, all six proton placements | confirmed |
| 2 | C-12, all six rules | 81.64 / 91.78 / 87.27 / 85.61 / 98.04 / 85.52 | identical | confirmed |
| 3 | Enumeration cannot miss the maximum (box, anchoring, species) | implied | box-free search gives the same optima; widest optimum (C-12 "none", a linear chain) spans 10 lattice units, inside ±8 from the first body | confirmed |
| 4 | "Every rewarding rule binds Be-8" → "the linear attachment rule is DEAD" | DEAD | true for the five rules run. One count per touching body pair gives S(Be-8) = −1.46 + 0.78 = −0.68 (unbound). A count of loops through three bodies is linear, is zero for Be-8, and was not run | over-claimed (scope: five rules, not "the linear rule") |
| 5 | Required ATT: Li-6 2.51, Li-7 3.95, Be-7 3.97, Be-8 1.30 u | as stated | arithmetic reproduces. With measured body energies instead of model bodies (model α is +0.18 MeV, T −0.14, ³He −0.24): 2.73, 4.00, 3.89, 1.75 u. Be-8 at the compact (8-contact) geometry: 2.07 u | arithmetic confirmed; "not integers" over-claimed for Li-7 and Be-7 (4.0 and 3.9 at the test's own ±0.3–0.5 u resolution) |
| 6 | Per α–α pair: 1.30 u (Be-8) vs 4.48 u (C-12, "each pair in one triangle"), factor 3.4 | 3.4 | 13.45 u is measured against the "none" optimum, which is a **linear chain**: 2 touching pairs, no triangle, Coulomb 3.77 MeV. Divided by 3 triangle pairs it is a mixed number. Consistent versions: compact/compact 16.49 u ÷ 3 = 5.50 vs 2.07 → **2.66**; chain/chain 13.45 ÷ 2 = 6.72 vs 1.30 → 5.2; point alphas at 3.139 fm → 2.44 | wrong (3.4 is an inconsistent mix) |
| 7 | Cross-rung reading: "1 : 4.0 at the nucleon rung, same step" | CONSTRUCT | consistent alpha-rung ratio is 2.4–2.7, not 3.4; ratio > 1 itself is just S(Be-8) = −0.09 vs 7.27/3 = 2.42 MeV per pair | unsupported as a match; "ratio ≠ 1" confirmed |
| 8 | He-5 "exactly at threshold (S = 0.00) … right sign" [CONSISTENCY] | S = 0.00 | zero by construction: a refused neutron contributes no term at all. Data −0.89. Report counts S ≤ 1e-9 as "hole kept", so He-5 is a free pass; the same refusal leaves Be-9 and Li-8 at S = 0.00 (measured +1.66, +2.03) | over-claimed (tautology, not a consistency) |
| 9 | Triangle count, gating, Coulomb sum | — | ordered sums halved correctly; my counts match (12 for Be-8, 24 for C-12). Latent bug: the `tris` split for a non-single body added after a single counts a triangle with one single vertex as 0.5 and ignores the two-new-one-single term; no decomposition in `NUC` reaches that branch | confirmed (bug latent, no effect on the table) |
| 10 | 30 Oct by-hand numbers reproduce (−2.4, −2.8, −3.6 %) | as stated | read off the generated scan only | not checked independently |
| **§2** | | | | |
| 11 | Mirror differences (B/C-11, N/O-15, K/Ca-39, Co/Ni-55, Ca/Sc-41, C/N-13, O/F-17); T − ³He | 2.764, 3.537, 7.307, 9.476, 7.278, 3.003, 3.543; 0.764 | identical | confirmed |
| 12 | κ_eff = 0.970 ± 0.042, hole pairs | 0.970, sd 0.042 | 0.970, sd 0.042 (κ = 1 geometry: 0.971; Gaussian finite-size alphas: 0.986) | confirmed |
| 13 | "to 3 % with nothing fitted" | 3 % | ±0.042 is scatter with a trend (1.09 at C-12 → 0.94 at Ti/Cr, r = −0.58). The mean over alphas hides the choice of which alpha holds the hole: per-nucleus range 0.75–1.11 (Fe-52: 0.75–1.06). Model rms charge radii run low (Ca-40: 3.28 vs 3.478 fm, −5.7 %), which by itself accounts for κ_eff < 1. d0 = 3.139 comes from the C-12 radius and ρ = 0.30 from Fe-52 | over-claimed (precision), result not affected |
| 14 | Screening DEAD (κ ≠ 0.18) | DEAD | uniform sphere, R = √(5/3)·r_ch(exp): measured/model = 1.00–1.02 for A = 11–39; with r0 = 1.2 A^⅓: 0.83–0.93. Not circular: geometry at κ = 0.18 and κ = 1 give 0.970 and 0.971 | confirmed |
| 15 | T − ³He as the in-alpha term | 0.764 | reasonable to about 0.1 MeV (pp spacing in ⁴He vs ³He; charge-symmetry breaking); shifts κ_eff by 5 % at C-12, 1 % at Ni-56 | confirmed (reasoned) |
| 16 | q_needed 4.26 → 5.32, ×1.25, 3.26 + 0.33 z̄, log-slope 0.24 | as stated | 4.26 → 5.32, ratio 1.249; sequence starts 4.26, 4.24, 4.09 (falls before it rises). κ in 0.90–1.05 moves the ratio 1.23–1.26 | arithmetic confirmed |
| 17 | "**Therefore** the α–α bond strengthens with coordination" [COMPUTED] | forced | not forced. Same data, same number of parameters, fit to resid + E_C over 13 nuclei: q(z̄) linear, rms 2.80 MeV; **constant q = 4.24 MeV + 0.92 MeV per second-shell pair (d0+ρ < d < 2.2 d0), rms 1.30 MeV**; constant q + Yukawa tail, rms 1.71. z̄ and Nα are collinear, so coordination is not isolated. Also omitted: non-rigid alphas, bond count b being geometry-defined | over-claimed |
| 18 | "κ = 0.18 was the cooperative strengthening mis-booked" | stated as fact | follows only if #17 is the unique reading | unsupported |
| 19 | Neutron increments 11.1 / 9.7 / 8.6 MeV per neutron | as stated | 11.14 / 9.73 / 8.56 | confirmed |
| **§3** | | | | |
| 20 | Same-sense rotation → anti-parallel velocities at contact | yes | v1 = (0, +0.9186), v2 = (0, −0.9186) at t = 0, s2 = +1 | confirmed |
| 21 | Full retarded e⁺/e⁻, phase 0: gap 0.1, 0.3, 0.5 | −1.80/−2.29, −1.21/−1.45, −0.91/−1.03 | −1.795/−2.290, −1.206/−1.446, −0.912/−1.026 (retarded = advanced to 3 d.p.) | confirmed |
| 22 | Darwin at 0.1 fm, phase 0 | −2.20 vs −2.18 | −2.203 vs −2.183 | confirmed |
| 23 | Erratum: old "gear" = Darwin counter-sense φ = 0; "belt" ≈ same-sense φ = π → STRUCK | −2.18; ≈ −0.32 | −2.183; −0.297 (7 % off the old −0.32) | confirmed |
| 24 | Channel table, 0.3 fm: pn −0.41/−0.83, nn −0.83/−1.67, pp +0.77/+0.61 | as stated | −0.414/−0.837, −0.829/−1.675, +0.770/+0.608 | numbers confirmed |
| 25 | "only the correlation energy survives"; "nn binds twice as deep as pn" [COMPUTED] | finding | nn(φ) ≡ −2·pn(φ) and pn(φ+π) = −pn(φ) algebraically for the antipodal layout, so the factor 2 is an identity, not a result. The pp row is not a correlation energy: phase means are +0.88/+0.78, so pp correlation is −0.11/−0.17 (attractive) | over-claimed / mislabelled |
| 26 | Ordering wrong → contact picture DEAD "as declared" | DEAD | holds for this layout only (and this layout has zero net current, hence μ_n = 0); the note's qualifier is accurate | confirmed as scoped |
| 27 | "Scale: right" (0.4–1.7 vs 0.79 MeV) | COMPUTED | e²/R_p = 1.71 MeV fixes the scale dimensionally; the gap is unset by the note's own finding and e⁺e⁻ alone runs −0.9 to −2.3 over 0.1–0.5 fm | over-claimed |
| 28 | Larmor 39.7 MeV per fm/c, 50× KE | "two charges … radiate 39.7" | 39.67 **per charge** (79.3 for two); ratio to KE 0.782 MeV = 50.7 | confirmed, wording wrong (per charge) |
| 29 | Force ~1/g to 0.03 fm; W(g) oscillates to 60 fm | COMPUTED | — | not checked |
| **§4** | | | | |
| 30 | λ_M = 1 + aγ; λ_E = 1 − 1/γ + aγβ²; λ_T = −(γ − 1) | as stated | derived by hand from Jackson 11.170 with dβ/dt from the Lorentz force; own RK4 integration of orbit + spin agrees to 6 d.p. at γ = 1.05, 2, 2.531, 10, a = 0 and a_e. Signs correct | confirmed |
| 31 | Table at c′: 1.002935, 0.605, −1.531; returns −0.999957, −0.32, +0.10 | as stated | 1.002935, 0.604897, −1.530988; −0.999957, −0.3236, +0.0972 | confirmed |
| 32 | B = 4.71 × 10¹² T; loop-centre field of μ_p 4.74 × 10¹²; ratio 0.993; μ_p ≈ ½γβ e c R_p²/r_e | as stated | 4.713e12; 4.745e12; 0.9933; 1.4012e-26 vs 1.4106e-26 J/T | confirmed |
| 33 | Look-elsewhere ≈ 8 % | 8 % | eight trials span a factor 7.35; P(±1 %) = 8.0 %, P(±0.7 %, the actual miss) = 5.6 %. Trial family (which radius, centre vs equatorial vs on-orbit field, which momentum) was chosen after the hit, so 8 % is a floor on chance | confirmed for the declared family |
| 34 | Twist does not cancel the anomaly detuning → DEAD | DEAD | — | not checked |
| 35 | Koide Q, δ, m_τ, DC/AC | 0.666665; 0.222239; 1776.97; 0.999993 | 0.6666645 (rounds to 0.666664); 0.222239; 1776.969; 0.999993 | confirmed (last digit of Q off by one) |

## Most serious problems, in order

1. **The factor 3.4 (item 6) is not a like-for-like number.** The C-12 baseline is a linear chain (Coulomb 3.77 MeV, two touching pairs) but is divided by three triangle pairs. Like-for-like it is 2.66 (compact) or 2.44 (point alphas); the alpha-rung range is 2.4–2.7, not 2.4–3.4. The comparison with the nucleon rung's 1 : 4.0 loses its only near-match. Strike "3.4".
2. **"Therefore the bond strengthens with coordination" is one reading of two (item 17).** A constant bond of 4.24 MeV plus 0.92 MeV per second-shell pair fits the same 13 residuals at rms 1.30 MeV against 2.80 MeV for q(z̄). The ledger entry "COMPUTED: ×1.25" and the closing line "cooperation is the common finding at both rungs" should be downgraded to an alternative; "κ = 0.18 was cooperative strengthening mis-booked" goes with it.
3. **"Linear attachment rule DEAD" is wider than the test (item 4).** Five counts were run. A per-body-pair count leaves Be-8 unbound (S = −0.68 MeV), and the note's own conclusion (loops through three bodies) is itself a linear count that was never scanned. Correct grade: the five tested rules are dead.
4. **Required-ATT table depends on unstated baselines (item 5).** Model body errors of 0.14–0.24 MeV (0.2–0.3 u) and the stretched-geometry Coulomb move Be-8 from 1.30 to 1.75–2.07 u and put Li-7 and Be-7 at 4.0 and 3.9 u. "Not integers" is shown by Li-6 and Be-8 only.
5. **Two "results" are identities.** He-5 S = 0.00 under refusal (item 8) and nn = 2 × pn (item 25) are fixed by the declarations; neither should carry COMPUTED or CONSISTENCY. The pp row is on a different footing from pn and nn (mean Coulomb +0.88/+0.78 MeV included).
6. **κ_eff precision (item 13).** 0.97 ± 0.04 is scatter about a trend; which alpha holds the hole spans 0.75–1.11; the 3–4 % deficit matches the model's 5.7 % radius shortfall at Ca-40. Screening at 0.18 is dead regardless.
7. **"Scale: right" (item 27)** is e²/R_p with a hand-picked gap. Minor: Larmor figure is per charge; Koide Q last digit.

Nothing graded DEAD or STRUCK needs reviving beyond the narrowing in problem 3. Standing items that should be struck or downgraded: the 3.4 factor and the 1 : 4.0 comparison; ledger line "α–α bond strengthens with coordination — COMPUTED"; He-5 [CONSISTENCY]; "Scale: right [COMPUTED]".

## What was run and what was only reasoned

Run (own code): mirror differences and κ_eff under four Coulomb models, model vs experimental charge radii, q_needed and five alternative two-parameter fits; Liénard–Wiechert energies (root-bracketed retarded and advanced times), Darwin values, contact velocities, 24-point phase scan and the three channel combinations at 0.3 fm, Larmor power; T-BMT orbit + spin integration, field and moment figures, look-elsewhere arithmetic, Koide; box-free enumeration of α+α and α+α+α under all six rules with features and Coulomb.

Reasoned only: legitimacy of T − ³He (item 15); the latent `tris` bug and singles handling in `lanes.py` (read, not exercised); generality of the channel ordering; trial-family size for the coincidence.

Not checked: nuclei other than Be-8 and C-12 in the rule scan (including the 30 Oct reproductions and the rms-miss row); particle-pair pockets; force law and W(g) out to 60 fm; channel table at gaps other than 0.3 fm; twisted-ring holonomies; regeneration of the cluster geometries.
