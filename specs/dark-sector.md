# spec: dark-sector — commit to a w(z) before DESI DR3, and check the EHT chromaticity

**Model:** Sonnet 4.6, WebSearch-armed. **Test dir:** `tests/dark-energy-w/` and `tests/eht-chromaticity/`.

## The claims they serve
`todo_refactor/docs/now-edge.md` §4–§5: dark energy as the bulk's pressure on the now-surface (no {μ,i} in the bulk ⇒ EM-invisible by construction); the deficiency hierarchy (DE = no pair, DM = μ without the EM lock). And `todo_refactor/tests/black-holes/README-testing.md`: the CBL model predicts a **5–10 % chromatic ring-size shift 230 → 345 GHz** versus achromatic GR.

## Test 1 — the equation of state, registered before the data
Derive **one** w(z) from the balloon's Laplace wall mechanics (tension vs radius as the surface inflates). The menu is known — w = −1 (uniform tension), w = −2/3 (wall-like scaling), w < −1 (tension growing with inflation) — and **a menu scores zero**. Commit to one, with the derivation, in `tests/dark-energy-w/README.md`, then compare to DESI DR2's w₀wₐ contours (currently w₀ ≈ −0.44 … −0.81 by dataset combination, wₐ < 0, 2.8–4.2 σ from Λ). Register the pass/fail against DR3 before DR3 is published; that is the entire point.

| outcome | grade |
|---|---|
| a single w(z) derived, inside DR2's band, and DR3 lands on it | [CONFRONTED — pass] |
| a single w(z) derived, outside the band | [FALSIFIED] — say so first, then look for what was wrong |
| the mechanics only yields the menu | [UNDERDETERMINED] — record which extra assumption picks each branch |

Also register the DGP kinship: state where this model's growth-of-structure prediction differs from DGP self-acceleration (which was killed by growth data), or inherit its grave.

## Test 2 — EHT chromaticity (cheapest kill in the estate)
Literature check, not a computation: has a 345 GHz ring size for M87* or Sgr A* been published? If the ring is achromatic to better than 5 %, the CBL T(ω,Φ) prediction is dead; file it as [FALSIFIED] with the citation. If not yet measured, file [REGISTERED, awaiting data] with the prediction and the date.

## What you may not do
Pick the w from the menu that best fits DR2 and call it derived. Read `system/keystones/013` and `docs/now.md` §2 on why.

## Return
Two test READMEs (first commits), the derivation, the citations. Under 800 words of prose. Measured apart from concluded.

## WITHHELD
The hypervisor's expectation for w(z) is not stated.
