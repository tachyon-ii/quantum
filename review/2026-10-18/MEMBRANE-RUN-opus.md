# Membrane solver — first build and run, graded

**Grace** `.ghost`, Claude Opus 5.5 — 18 Oct 2026. Code: `models/binding/membrane/` (every number in `report.md` is written by `run_all.py` from `results/`). Spec: `BUILD-SPEC-membrane-solver.md`. This is the Opus implementation of the three-way build; Argon and GPT have not yet run.

## Headline

**[COMPUTED] The spec's functional cannot be calibrated.** A rank-3 (He-4) contact has to be worth **5.69×** a rank-1 (deuteron) contact. In this functional it is worth **0.85–1.15×** in every converged contact-regime case (δ = 0.084 and 0.252 fm; κ = 0.1 and 0.3 E₀; r = 1–10). Three patches on one capsid compete for one skin and one volume, so adhesion here is *anti*-cooperative. Hub skin within δ of two partners does not rescue it. This is the isotropic-adhesion version of the §3.1 raw-data fact: geometry alone orders the per-bond energies backwards. The cooperative term has to come from something the functional does not contain.

## Three defects in the spec (Fable's, found by building it)

1. **[COMPUTED] Inflation has non-zero slope at rest** (E₀(V₀/V − 1)), so an isolated capsid is not at equilibrium. Fixed by taking the relaxed isolated capsid as the energy zero.
2. **[COMPUTED] The nearest-face-plane gap is discontinuous and not a distance.** Optimiser line searches failed. A vertex near the *extended* plane of a flattened face got adhesion from 0.23 fm away. Fixed with a blended, floored gap.
3. **[COMPUTED] K_BEND = 0 is ill-posed.** Without bending rigidity the deuteron's skins wrap each other and never stop: the Seifert–Lipowsky wrapping instability. The spec's 0.01 E₀ variant is also below the threshold κ ≈ e₀R²/2. Even at κ = 0.1–0.3 E₀, 11 of 23 grid points are engulfed, with one capsid inside another.

## Fallback: E₀ from the deuteron alone (declared; not a calibration)

At two settings, both in the contact regime:

- **Binding:** T 4.16 / 3.82 MeV (8.48 measured); ³He 3.24 / 2.93 (7.72); ⁴He 6.16 / 5.19 (28.30). [COMPUTED]
- **The egg [COMPUTED; the ruling not reproduced].** Patches come out near-circular (aspect 1.04–1.25), with the geometric centroid *outward* of the pair midpoint by 0.01–0.07 fm. The energy-weighted offset is ±0.016 fm with no consistent sign. Where there is a taper (setting A, T), the narrow end is at the hub. A pairwise isotropic adhesion does not make the fat-end-at-hub egg. The ruling stands as a posit that needs a local mechanism this functional lacks.
- **P3 untestable here.** The mesh term is a per-contact constant, so the nn patch in T is geometrically the *largest* (−0.90 vs −0.57 / −0.71 MeV). Testing "thin point on the same-species patch" needs a spin-signed term that acts locally across the patch.

## Load paths on the fallback triton (P1 = proton, tangential toward pivot P3)

| path | first instability | how it fails |
|---|---|---|
| out of plane | **< 0.0125 MeV/fm** | P1 slides over both patches with both contacts kept. No resistance, exactly as the §1 theorem requires when there is no friction/mesh term. [COMPUTED] |
| tangential | **1.85–1.86 MeV/fm** | Creeping roll about P3: 10.3° roll and 14.6° P1 spin at the last stable step. The pivot patch strengthens under compression (−0.70 → −0.98 MeV) while the far patch loses 35 % (−0.57 → −0.37). Both contacts are kept at the snap. [COMPUTED] |
| radial | **> 10.2 MeV/fm** (capped) | No peel. The skin necks: P1 is drawn 0.60 fm and the patches retain 27 % of their energy. [COMPUTED] |

**Tangential is the easy pop, ≥ 5.5× softer than radial.** The pivot compresses and the far patch weakens, as the picture says [CONSISTENCY]. **Not seen:**

- pivot-egg inversion (the offsets stay at ±0.006 fm, against a 0.11 fm mesh edge);
- a point-first unzip front;
- any clean hub-side lift under radial load (hub-half fraction 0.37–0.65, noisy).

The P2 counter-roll is suppressed by the tethers (declared A7), so "simultaneous vs sequential" was not testable.

## Tests

- Gradients exact to 2 × 10⁻⁸. Isolated capsid is spherical to 0.3 %. Two-capsid patch is a disc. **pass**
- **9.4 fails:** T's two np patches differ by 19 % at setting A. The triangle's relaxed state breaks its own symmetry, so ground states are not unique at this resolution.
- Not run (no calibrated state to scale them): SUBDIV 4, K_AREA×2, rotation, quartic E(z), chain, quadratic fade.

## What this means for the three-way build

When Argon and GPT run the same spec, they should hit the same three defects. Watch for that in their reports: if either "calibrates" this functional, it changed the functional without saying so, or it used the rms distances. The physics conclusion I'd carry forward: **the rank effect is not in pairwise skin adhesion.** It needs one of two things:

- an explicitly cooperative term (shared-crease rim recovery, §4.4 of the physics spec), or
- a mesh term that acts on the patch, not per contact.

The natural next build is this code with one of those added and nothing else changed.
