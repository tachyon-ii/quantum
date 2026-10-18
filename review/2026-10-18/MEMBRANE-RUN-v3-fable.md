# Membrane solver v3 — lane/graph cooperativity: build, run, grade

**Grace** `.ghost`, Claude Fable 5.1 — 18 Oct 2026, 18:10–19:30 AEDT. Code: `models/binding/membrane/` (v2 energy + one term; `calib3.py`, `run_all_v3.py`). Report written by code: `models/binding/membrane/report_v3.md`. Follows `MEMBRANE-RUN-v2-fable.md` (rim recovery as skin-sharing: DEAD) and takes its §4 at its word: *the cooperativity is in the lanes, not the skin.*

## 1. The term — declared before running

For a contact (i, j) with c_ij common contact partners — the triangles of the bond graph — the adhesion density is multiplied by **f_ij = 1 + λ·c_ij**. Only **triplet** (np) contacts are boosted: a singlet pair fuses no lane (James's ruling F4, now doing work). One new constant, **λ, set on ⁴He**; E₀ from D, where λ cannot enter (c = 0). r and δ scanned, κ = 0.2 E₀. This is Build 3's closure rule (0 / ½ / 1 per contact by triangle count) given a continuum body: the skin, inflation, bending, Coulomb and the mesh/slingshot bookkeeping all respond to it self-consistently.

**Pre-run arithmetic, on record:** with no geometry the factor gives T/D = ³He/D = (1 + ⁴He/D)/2 = 3.46 against the required 3.04 / 3.12 → T +14 %, ³He +11 %. The membrane's job was to say what geometry does to that.

## 2. Result

**[COMPUTED] The lane term calibrates, in the contact regime, and the blinds bracket the measurements.**

| r | δ (fm) | E₀ (MeV) | λ | ⁴He (cal.) | **T** (meas. 8.482) | **³He** (meas. 7.718) |
|---|---|---|---|---|---|---|
| 0.1 | 0.168 | 131.6 | 2.91 | 28.293 | 9.124 (+7.6 %) | 8.264 (+7.1 %) |
| 0.1 | 0.252 | 88.2 | 3.03 | 28.301 | 9.161 (+8.0 %) | 8.262 (+7.0 %) |
| 0.3 | 0.168 | 42.7 | 2.28 | 28.294 | 8.113 (−4.4 %) | 7.245 (−6.1 %) |
| 0.3 | 0.252 | 28.7 | 2.29 | 28.294 | 7.987 (−5.8 %) | 7.083 (−8.2 %) |

δ barely matters; r does. The rigid limit (r → 0) recovers the pre-run arithmetic (+8 % → +14 %); softer capsids (r = 0.3) over-correct to −5 %. **The measured T and ³He sit inside the scan**, at r ≈ 0.2 — which is not a fit, it is where a scan declared in advance happens to put them. The ordering ³He < T is right in every row, by Coulomb. ⁴He's centroids stay at 1.44–1.65 fm: contact, not engulfment.

**Regime finding [COMPUTED]:** r ≥ 1 is the wrong regime for the whole programme. At E₀ ≈ 8 MeV the lane factor drives ⁴He into engulfment before 28 MeV is reached; at E₀ ≈ 30–130 MeV it does not. The inflation scale has to be large compared with a patch — consistent with the ~600 MeV bubble estimate of 16 Oct — and that fixes what the capsid is: stiff, small patches, adhesion of order 1 MeV/fm². Every v1/v2 row at r ≥ 1 was in the soft regime; that is why they wrapped.

## 3. What came out that was not put in

- **[COMPUTED] The same-species patch is the thin one.** T: nn raw patch 0.431 vs np 0.54, d_nn 1.70 vs d_np 1.62 fm. ³He: pp 0.411, d 1.665. Physics-spec **P3** ("the thin point is on the nn / pp patch") is now a *consequence* of "a singlet fuses no lane," not an input.
- **[COMPUTED] ⁴He is not a regular tetrahedron.** np distances 1.49–1.56 fm; nn 1.73; pp 1.72. Squashed along the np bonds. Prediction for the charge/matter geometry of the alpha to carry forward.
- **[COMPUTED] Dome again.** Pull-off profiles on the v3 triton peak at 0.54–0.62 of the patch radius with tinkle fraction 0.34–0.48 (dome 0.58 / 0.44). Third time; the smooth well is what this body makes.
- **[NOT REPRODUCED]** Hub-half fractions 0.45–0.58 with no consistent sign: the fat-end-at-hub egg does not come from the lane term either. Three terms have now failed to make it. Either it needs a local mesh density across the patch (James's option b), or the ruling needs re-examining against what the three solvers keep producing — patches that are near-circular with their *geometric* centroid slightly outward.

## 4. Grades and caveats

- Calibration and blinds: **[COMPUTED]**, reproducible from `results/calib3.json` and the job states; `targets.py` touched only by `compare.py`.
- The term is a **[POSIT]** with Build 3 as its lineage; its continuum form (density multiplier by triangle count) is **[CONSTRUCT]**. The `all`-mode and `sat`-form variants were queued and not finished (time); their ⁴He trajectories so far run parallel to `triplet/linear`.
- Classical radii 1.25–1.28 fm against measured 1.76 / 1.97 / 1.68: the classical-minimum caveat stands; the zero-point is not in this model.
- Not run on the v3 states: load paths, quartic mode, chain, SUBDIV 4. The v2 cross-check (snap = pull-off peak) is the mechanism's evidence for now.
- Lineage: Build 3 (16 Oct, closure by triangles) is the parent of this term; the physics spec §4.4 rim recovery is its sibling and is dead in skin form; "a singlet fuses no lane" is James's ruling of this morning and did the work in §3.

## 5. Disposition

v3 is the base for the bees. Handshake: **BE(T) = 8.113 MeV at r = 0.3, δ = 0.1682 fm, κ = 0.2, λ = 2.277 (triplet/linear)**. Ask them to reproduce the four-row table, then to run the load paths and the quartic mode on the r = 0.3 triton — the one calculation that can now give the soft-mode zero-point a scale — and, separately, to try one local-mesh-density term for the egg. Commit with the v2 record.
