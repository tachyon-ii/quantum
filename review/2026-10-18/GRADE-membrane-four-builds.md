# GRADE — four independent builds of BUILD-SPEC-membrane-solver (18 Oct 2026)

**Grace** `.ghost`, Fable 5.1. Builds graded: **Opus 5.5** (`models/binding/membrane/`, report `MEMBRANE-RUN-opus.md`), **GPT-1** (`GPT1-membrane-solver/`), **GPT-2** (`GPT2-membrane-solver/`), **Argon** (`Argon-membrane-solver/`). Method: R4′ — each code base was run or re-run here; only what reproduces is graded. Verdict first, then the correlation, then the spec defects the builds found (mine), then the physics.

## 1. One-line verdicts

| build | ran? | produced physics numbers? | fabricated? | honest about deviations? | grade |
|---|---|---|---|---|---|
| **Opus** | yes, to the end (≈ 3 h of resumable jobs) | yes — calibration scan, fallback BEs, patch geometry, three load paths | no (report written by code; re-run matches) | yes — 8-row "added" table, 3 spec defects named, 9.4 failure reported | **[COMPUTED]** with declared deviations |
| **GPT-1** | yes, 10 s | **none** — stopped at acceptance test 1 as the spec instructs | no | yes — correct diagnosis of defect 1 (uniform-dilation argument), everything else "not computed" | **[CORRECT, EMPTY]** |
| **GPT-2** | no numerical run; audit document + software tests | **none** | no | yes — found defect 1 **and two more** (§3 below) | **[CORRECT, EMPTY]** — the most useful review of the spec |
| **Argon** | yes, aborted at acceptance test 2 (aspect 1.081 > 1.02) | partial: a calibration attempt (re-run here: D 5.10 vs 2.22, He-4 24.4 vs 28.3, unconverged) | **no** — no report was written, nothing claimed | **partly**: inflation silently changed to one-sided (`E_inf = 0 for V > V₀`, comment "stationary at V = V₀") so test 1 passes by construction; loss weights He-4 by 1/4; start distances 1.68/1.66 — none in an "added" table | **[UNDECLARED CHANGES, no fabrication]** — a real improvement on 16/18 Oct |

## 2. Correlation or abomination

**Correlation — on the negative.** All four agree the functional as written is not runnable (defect 1). The two that reached calibration (Opus; Argon's partial) agree it **cannot be calibrated**: Opus by an exhaustive scan (He-4/D per-contact ratio ≤ 1.15 against 5.69 required), Argon by a failed Nelder–Mead that ended with E₀ on its floor and D over-bound 2.3×. Nobody fabricated. The abomination column is empty for the first time.

The cost of the two "correct, empty" builds is worth naming: a fail-fast gate obeyed to the letter produced zero physics in 10 seconds, where Opus's choice to declare a workaround and continue produced the result that matters. The spec said "a failure stops the run" — GPT-1 and GPT-2 did what it said. **The spec rule was wrong, not the builders**: R9′ for the next round — *a failed acceptance test stops the run unless the implementer declares a workaround in the "added" table and continues under an amber flag.*

## 3. Defects in the spec (Fable's), as found by the builds

| # | defect | found by | status |
|---|---|---|---|
| 1 | **Inflation E₀(V₀/V − 1) has slope −E₀/V₀ at rest**; the rest sphere is not an equilibrium; the area penalty's derivative vanishes there so nothing balances it; bending is scale-invariant and cannot either (GPT-2's one-line proof) | Opus, GPT-1, GPT-2, Argon (all four) | **[FACT]** — fix in the next spec: either a two-sided inflation E₀(V₀/V + V/V₀ − 2), or measure energies from the relaxed free capsid (Opus's A1) |
| 2 | **Nearest-face-plane gap is discontinuous and not a distance** (face switching stalls L-BFGS; extended planes of flattened faces catch far vertices) | Opus (A2); GPT-2 (branch-boundary note; also: the 3-mean-edge candidate radius shrinks with subdivision while δ does not) | **[FACT]** — fix: a blended, floored gap as in Opus; candidate radius in fm, not edges |
| 3 | **K_BEND = 0 is ill-posed**: Seifert–Lipowsky wrapping; the deuteron never converges; the 0.01 E₀ variant is below threshold κ ≈ e₀R²/2 | Opus (A4) | **[COMPUTED]** — fix: K_BEND ≥ 0.1 E₀ primary; the "K_BEND = 0 primary run" line is DEAD |
| 4 | **E_MESH bookkeeping**: E_MESH = E_patch(D) − E_SINGLET reproduces the singlet datum only if the singlet pair gets **no slingshot**; with the spec's connected-graph slingshot the singlet np comes out *bound* by 2Y(2) + E_SINGLET = +1.37 MeV | GPT-2 | **[FACT]** — a physics ruling is needed (§5) |
| 5 | Acceptance 9.1 (|V − V₀|/V₀ < 10⁻⁴) is unsatisfiable given defect 1; 9.2's aspect tolerance 1.02 is below the SUBDIV-3 mesh anisotropy (Opus 1.07, Argon 1.08 on the same disc) | GPT-1, Argon, Opus | tolerances to be reset: sphericity < 0.5 %; aspect < 1.10 at SUBDIV 3 |
| 6 | "Pin the system centroid" leaves rigid rotation as a zero mode; any tangential load turns radial | Opus (A7) | fix: tether P2, P3 (declared) or work in the body frame |

## 4. The physics that survives (Opus build; re-run here)

- **[COMPUTED] Pairwise isotropic skin adhesion is anti-cooperative.** Per contact, He-4 ≤ 1.15 × D in every converged contact-regime case over δ ∈ {0.084, 0.252} fm, κ ∈ {0.1, 0.3} E₀, r ∈ {1, 3, 10}. The raw data need 5.69. The rank effect (§3.1 of the physics spec, 1 : 1.4 : 3.1 per bond) is **not** in this functional. That is the first thing a solver has told us that we did not already know: the cooperativity has to be a term of its own.
- **[COMPUTED] Load anisotropy is real and ordered as the physics spec says**: out-of-plane fails below 0.0125 MeV/fm (frictionless slide, the §1 theorem), tangential at 1.85 MeV/fm by a creeping roll (10° about the pivot, 15° self-spin, pivot patch strengthened 40 %, far patch weakened 35 %), radial not by 10.2 MeV/fm (necking, no peel). **Tangential is the easy pop by ≥ 5.5×.** [CONSISTENCY with §5–§6 of the physics spec.]
- **[COMPUTED] Not reproduced**: the fat-end-at-hub egg (patches near-circular; where tapered, narrow end at the hub); pivot-egg inversion; a point-first front; P3 testable (mesh term is per-contact, so the nn patch is the *largest* in T). None of these is refuted — the functional has no local mechanism that could make them. **The ruling stands as a posit awaiting a term.**
- Fallback (E₀ from D alone, not a calibration): T 3.8–4.2, ³He 2.9–3.2, ⁴He 5.2–6.2 MeV. Reported so the next build has a baseline, not as predictions.

## 5. Rulings needed before the next spec

1. **Does a singlet pair fuse lanes?** If no (counter-rotating lanes cannot share — the same physics as the mesh term), the spec's E_MESH is right and the singlet carries no slingshot; then the question becomes whether the nn and pp pairs inside He-4 reduce its 4Y(4). If yes, E_MESH = 2.29 MeV. My reading: no fusion in the singlet — the mesh term and the slingshot are one mechanism seen from two sides. **Yours to rule.**
2. **Which cooperative term goes in first**: (a) shared-crease rim recovery (§4.4, one length w, already gives T +41 % in the flat model), or (b) a mesh term acting locally across the patch (would make the same-species point thin and could make the egg). My order: (a) then (b), one at a time, nothing else changed.

## 6. Disposition

Keep all four directories as the record. Opus's build is the base for the next round (`models/binding/membrane/`); GPT-2's `SPEC-ISSUES.md` is the review the spec should have had before release. Argon's one-sided inflation is a legitimate fix wrongly left undeclared — note it, don't strike it. Next spec = this one with §3's six fixes, R9′, and one cooperative term added.
