# BUILD SPEC v2 — the membrane solver with rim recovery and the pull-off peel

**Grace** `.ghost`, Claude Fable 5.1 — 18 Oct 2026 (evening). Supersedes `BUILD-SPEC-membrane-solver.md` (v1). Base code: the Opus build in `models/binding/membrane/` — **v2 is that code with the changes in §1 and §3 and nothing else**; a fresh implementer may rebuild from scratch but must reproduce the Opus v1 fallback-A triton (BE 4.156 MeV at δ = 0.0841 fm, κ = 0.3 E₀, r = 3) before changing anything, as the handshake. Rulings by James, 18 Oct: slingshot at /2; rim recovery first; the well is smooth (bonding is interference, not velcro). Graded record of v1: `GRADE-membrane-four-builds.md`.

**R4′** stands: the report is written by the code; Grace re-runs; only what reproduces is graded. **R9′ (new):** a failed acceptance test stops the run *unless* the implementer declares a workaround in the report's "added" table and continues under an amber flag. Stopping silently is not compliance; stopping loudly without a workaround is a result only if no workaround exists.

---

## 1. Fixes to v1 (all six found by the four builds; see GRADE §3)

| # | v1 | v2 |
|---|---|---|
| F1 | E_inflate = E₀(V₀/V − 1): not stationary at rest | **E_inflate = E₀ (V₀/V + V/V₀ − 2)** — stationary at V₀, curvature 2E₀/V₀², still 1/V-hard under compression. Energy zero is then the rest capsid exactly; Opus's A1 is retired. |
| F2 | gap = signed distance to nearest face plane; candidate radius 3 mean edges | **gap = Gaussian blend (width 0.4 rest edge) of signed plane distances to the 24 nearest faces, floored by (nearest-centroid distance − 1 rest edge)** (Opus A2); candidate pre-screen radius **in fm**: partner bounding radius + δ + 0.1 fm. |
| F3 | K_BEND = 0 primary, 0.01 E₀ variant: wrapping instability | **K_BEND = 0.2 E₀ primary; 0.3 E₀ variant.** Report the fraction of engulfed states; any engulfed state (closest centroids < 1.3 fm or any skin point > 1.2 fm from its centroid) is excluded from calibration and flagged. |
| F4 | E_MESH = E_patch(D) − E_SINGLET with slingshot on every connected graph: singlet np comes out bound | **Ruling: a singlet pair fuses no lane** (mesh term and lane fusion are one mechanism). Slingshot counts only capsids that have at least one **triplet** contact; the singlet np alone has none → BE_singlet = E_patch − E_MESH = −0.066 by construction (acceptance test 8). In T, ³He, ⁴He every capsid has a triplet contact, so A·Y applies in full; **He-4's nn and pp singlet pairs do not reduce it** — declared, and He-4 is where this is tested. |
| F5 | acceptance 9.1 |V−V₀|/V₀ < 10⁻⁴; 9.2 aspect 1 ± 0.02 | 9.1: sphericity (radius std/mean) < 0.5 % and E_total(isolated) < 10⁻⁴ E₀ (now achievable with F1); 9.2: aspect < 1.10 at SUBDIV 3, < 1.05 at SUBDIV 4. |
| F6 | "pin the system centroid" — rigid rotation is a zero mode | Load paths tether P2 and P3 centroids (k = 2000 MeV/fm², declared; stands for their inertia). Report the tether forces at every step so the suppression of P2's counter-roll is visible. |

**Slingshot (ruling):** E_sling = −A·Y(2) for every connected nucleus with at least one triplet contact per capsid; Y(2) = 0.718059 MeV. Y(3), Y(4) are not used. If He-4 lands outside ±2 % with /2 and inside with 4·Y(4), that is a result to report, not a knob to turn.

## 2. Constants (changes only; the rest as v1 §2)

```
K_BEND_FAC   = 0.2        # primary (variant 0.3)
E1_COOP      = calibrated  # §3, MeV/fm^2 — the ONLY new physical constant
SLING_N      = 2          # ruling: Y(2) everywhere
GAP_K_NEAR, GAP_H, GAP_MARGIN_FM = 24, 0.4, 0.10
TETHER_K     = 2000.0     # MeV/fm^2, load paths only
R_GRID       = [1, 2, 3, 5, 10]   # e0*A0p/E0 scan (A0p = 4 pi RP^2)
DELTA_GRID   = [0.10, 0.20, 0.30] * RP
```
`targets.py` unchanged; importable only by `compare.py`; assert in `run_all.py`.

## 3. The one new term — rim recovery (the cooperative term)

Physics (SPEC-peel-and-roll §4.4): a patch's rim is a deficit only where it is *free*; where two patches on the same capsid meet along a dihedral crease the deficit is recovered. In the membrane this is skin of capsid i that is within the well of **two** partners at once.

**E_coop,i = −E1 · Σ_v A_v · Σ_{j<k} s(g_v^j/δ) · s(g_v^k/δ)**

summed over vertices v of capsid i and unordered partner pairs (j, k) both in contact with i. It is zero for the deuteron by construction (one partner), non-zero for every capsid in T, ³He, ⁴He. Gradient: product rule on the two gap terms, same machinery as E_adh. This is the whole change to the energy; no other term is touched.

**Calibration (declared order):**
1. For each (r, δ) on the grid: relax D; set the energy scale **E₀(r, δ)** so that BE(D) = BE_D exactly (D has no cooperative term, so E1 does not enter).
2. At that E₀, relax ⁴He and set **E1(r, δ)** so that BE(⁴He) = BE_HE4 (one-dimensional root; report E1/e₀ — the cooperative strength relative to the plain adhesion).
3. **r and δ are scanned, not fitted.** Report every (r, δ) row; T and ³He are blind at every row; the spread across the grid *is* the model's uncertainty and is reported as such.

If E1(r, δ) has no root for some row (⁴He cannot be reached), say so in the row — that is a result. If E1 must be negative, the row is dead.

**Prediction before running (Grace, so it is on record):** E1/e₀ will come out between 1 and 3; T and ³He will land within −10 % … +20 % of measurement with the ordering ³He < T preserved by Coulomb; the hub-half fraction of patch energy in T will exceed 0.55 (the fat end at the hub appears because the cooperative term lives at the hub). If the hub-half fraction stays at 0.50 ± 0.03, the egg ruling needs a different mechanism and I will say so.

## 4. The smooth well and the pull-off peel (replaces v1 §7.4)

**Ruling:** bonding is interference; the well across a patch is smooth, no band. In the membrane the fade is s(x) with x = g/δ; the well profile in the patch plane, e(ρ), is an **output**: for two spheres the gap grows as ρ²/R_eff so a linear fade in g gives a parabolic dome in ρ. Report e(ρ) as measured (binned, outer → hub, along the lift axis) — not assumed.

**Peel = pull-off instability.** For a front at position s across the patch along the lift direction, with front width b(s) (chord of the contact outline) and line energy G(s) = e(s) (Kendall), **F(s) = b(s) · G(s)**. Report for each patch of T and ³He, for the tangential-lift axis (point → hub) and for the axisymmetric case (b = 2πρ):
- F(s) tabulated; **F_max** and **s\*** (the peak);
- the **stable-branch energy fraction** (patch energy outside s\*): the "tinkle" share; the remainder is released in one event (the "bang");
- for reference, the analytic values at the measured dome: for e ∝ (1 − ρ²/a²) the axisymmetric peak is at ρ\*/a = 1/√3 and the stable fraction is 4/9 ≈ 0.44; for a cone 0.50; for the v1 rim-band (w = 0.156a) 0.16. The measured number decides which world we are in.

**Snap** on a load path is where the applied force exceeds F_max of the far patch: report both the path's last stable F (as in v1) and the F_max from the profile, and their ratio. They should agree within the load step; if they do not, the front is not where the profile assumes.

## 5. Outputs (v1 §7, amended)

7.1 BE and classical radii for D, T, ³He, ⁴He at every (r, δ) row; per-bond energies after slingshot and Coulomb.
7.2 Patch geometry as v1, plus the **hub-half energy fraction** and the **cooperative energy per capsid** (E_coop,i) and its share of the capsid's total adhesion.
7.3 Quartic mode on T: E(z) fit, k₂, k₄, 1-D Schrödinger E_zp and p_rms with reduced mass ⅔·m_N (now meaningful — there is a calibration).
7.4 Pull-off peel as §4.
7.5 Load paths as v1 (tangential, radial, out-of-plane on T; tethers reported). θ_snap, β_D, P1 spin.
7.6 Chain: P1–P3–P2 collinear, P3 pinned; energy vs D + N.
7.7 **Rank table**: per-bond energy D : T : ⁴He from the model (compare.py puts 2.22 : 3.13 : 6.86 beside it, last).
7.8 Convergence: SUBDIV 4 on D and T at the central row (r = 3, δ = 0.2 RP); K_AREA doubled; rotated start.

## 6. Acceptance (v1 §9 with F5, plus)

8. **Singlet deuteron is unbound by 66 keV** at every calibrated row (by construction; an assert that the mesh/slingshot bookkeeping is as ruled).
9. E_coop(D) = 0 exactly.
10. T's two np patches equal to 2 % (v1's 0.5 % failed at 19 %; if 2 % also fails, report the two minima and their energies — the triangle may have two seatings).

## 7. Added-table discipline

Every constant not in this document goes in the report's first table with a reason. Argon's v1 one-sided inflation was a legitimate fix wrongly undeclared; GPT-1/2's stop-at-gate was compliance with a bad rule. Under R9′ both are now in the open: declare and continue.

## 8. Lineage

Rim recovery as the cooperative term, the smooth well, slingshot at /2, "the singlet fuses no lane," the peak-strength picture of peel ("a few tinkles then BANG") and the question that produced it: **James**. The pull-off formulation F(s) = b·G, the stable-fraction numbers, the six fixes and R9′, the membrane form of the cooperative term and its calibration order, the on-record prediction: **Grace**. Defects found by the v1 builds credited in `GRADE-membrane-four-builds.md` §3 (Opus, GPT-1, GPT-2, Argon). Prior art: Seifert–Lipowsky 1990; Kendall 1971; Johnson–Kendall–Roberts 1971 (pull-off instability); Helfrich 1973.
