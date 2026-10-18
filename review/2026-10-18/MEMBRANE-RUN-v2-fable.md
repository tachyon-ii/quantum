# Membrane solver v2 — build, run, grade

**Grace** `.ghost`, Claude Fable 5.1 — 18 Oct 2026, 16:00–18:00 AEDT. Code: `models/binding/membrane/` (v2 on the Opus v1 base; `energy_v1.py`, `constants_v1.py` kept). Report written by code: `models/binding/membrane/report_v2.md`. Spec: `BUILD-SPEC-membrane-solver-v2.md`. This is the base for the Argon/GPT runs; the handshake number is the v2 live-row triton, **BE(T) = 3.652 MeV** at r = 1, δ = 0.2523 fm, κ = 0.2 E₀, E1 = e₀.

## 1. Headline

**[COMPUTED] Rim recovery, implemented as skin inside two wells at once, does not exist at membrane contact sizes, and where it exists it is unstable.** Patches subtend 19–27° of a capsid; two patches 60° apart do not meet until each exceeds 30°. Cooperative support is zero at δ ≤ 0.17 fm and ≤ 0.3 fm² (of 8.9 fm² skin) at δ = 0.25 fm. There E1 = e₀ adds 0.06 MeV to ⁴He against the 23 MeV missing; reaching ⁴He would need E1 ≈ 400 e₀. One row reports a root at E1 = 1.84 e₀ and it is spurious: ⁴He has collapsed to an engulfed ball (closest centroids 0.49 fm, skin out to 2.08 fm), because the term is positive feedback — overlap makes coop, coop makes overlap — with a first-order jump from BE 4.0 to 58.7 MeV between E1 = 0.52 and 1.55 MeV/fm². **No calibration. The v2 §3 term is DEAD in this form.**

**My on-record prediction (v2 §3) fails**, as I said I would say: E1/e₀ is not 1–3 (no finite value works); the hub-half fraction in T is 0.48–0.51, not > 0.55. The fat end at the hub does not come from a crease term in a skin model.

## 2. What the run established that is positive

- **[COMPUTED] The well is the dome, not the band.** Pull-off profiles F(s) = front width × line energy on T and ⁴He patches: axisymmetric peak at 0.54–0.63 of the patch radius, stable ("tinkle") fraction 0.31–0.47. Dome prediction 0.58 / 0.44; cone 0.50 / 0.50; v1 rim band 0.84 / 0.16. **James's smooth-well ruling is what the membrane produces** — about half the patch energy goes in tinkles, half in the bang.
- **[COMPUTED] The load-path snap is the pull-off peak.** On the v2 triton the tangential path loses equilibrium between 1.40 and 1.45 MeV/fm applied; the far patch's tangential F_max is 0.61 MeV/fm; the opening component 0.5 × F_snap = 0.70 → ratio 1.15. On the v1 triton: 0.93 vs 0.98 → 0.94. Two independent computations on the same states agree to the lever-arm projection. **"Peak strength then BANG" is the mechanics of the snap; crack propagation was the wrong picture** (mine), and the one-dimensional F(s) calculation predicts the snap force without running a load path.
- **[COMPUTED] Seventh spec defect (mine):** the Helfrich form Σ(1 − cos θ) charges the icosphere its own curvature; the rest capsid is not stationary (E = 1.5 E₀, |∇E| 0.57) even after F1. Fixed by measuring bending from the rest dihedral; the rest capsid is then exactly stationary (|∇E| 4 × 10⁻¹⁴). All seven defects were in Fable's spec; all were found by building it.
- **Fallback F2 numbers** at the live row (E1 = e₀ declared, not calibrated): T 3.65, ³He 2.75, ⁴He 4.97 MeV; classical radii 1.25 / 1.26 / 1.31 fm. The coop term moves these by 15–50 keV. Baseline for the next term.

## 3. Bookkeeping that matters for the bees

- v1 and v2 load paths collided on job file names; the first v2 tangential path silently reused v1's relaxed states and was discarded (`results/paths_v2_contaminated/`). Fixed: job names carry the base state. **R10 for the next spec: every cached state's name carries the energy version and the base state.** A reused cache is a fabrication nobody intended.
- Engulfment criterion (closest centroids < 1.3 fm or skin > 1.2 fm from centroid) kills every r ≥ 3 row at κ = 0.2; at κ = 0.3, r = 3 survives in D (d_min 1.30–1.34) and collapses in ⁴He once the coop term is on. The contact regime in this model is **r ≈ 1, κ ≥ 0.2** — adhesion weak relative to inflation. That is itself a statement about what the capsid can be: a skin that wraps at r = 3 cannot also be a nucleon that touches.

## 4. Where this leaves the physics

Three terms have now been tried for the factor 5.7 between a rank-3 and a rank-1 contact: pairwise adhesion (v1: anti-cooperative, ≤ 1.15×), crease recovery as skin-sharing (v2: no support / runaway). What has *not* been tried is the mesh term acting on the patch rather than per contact — James's option (b) — and the geometric fact behind the flat-model success (closure by triangles, Build 3: 0 / ½ / 1 per contact, T within 3.6 %) has not yet been given a continuum form that survives in a skin. My reading, graded [CONSTRUCT]: the cooperativity is in the **lanes**, not the skin — a contact is strengthened when the carrier lane threading it also threads the neighbour's contact, which is a graph property (triangles) and not a geometric overlap. The skin model will keep saying no until that is put in as what it is: a bond-graph term with the triangle count, i.e. Build 3's rule derived rather than assumed.

## 5. Disposition

`report_v2.md` and this grade are the v2 record. Code is the base for Argon/GPT; the handshake is BE(T) = 3.652 at the live row. Recommend the bees are asked to **reproduce** v2 (handshake, pull-off table, path snap) and then to **propose and test one lane/graph cooperative term each**, declared in their first line — rather than to re-run a term that has just been shown dead.
