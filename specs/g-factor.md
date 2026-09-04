# spec: g-factor — does the double loop give μ/S = q/m from topology alone?

**Model:** Opus (a derivation where regression to the mean is the failure mode). **Test dir:** `tests/g-factor/`.

## The claim it serves
`checkpoint-1.md` §1–§4: the electron is a wave of energy E = mc² on a closed path that returns to itself only after 720°; charge is a topological residue of the whole configuration, not a density riding the path. The scoreboard entry for g=2 was corrected on 2026-09-03 from [DERIVED] to [ASSERTED] — see `docs.local/now.md` §3 for why the old two-mode note fails (it doubles μ while holding S fixed; the classical gyromagnetic theorem forbids that for co-moving charge and mass).

## The test, written first
Compute the ratio **μ/S** for a closed double-loop wave configuration with these and *only* these inputs:
- total energy E = mc² (m the electron mass);
- the path closes after 720°, i.e. the configuration is a ℤ₂-twisted bundle over the loop (`checkpoint-1` catch 1);
- total charge e, entered **once**, as a property of the whole configuration;
- c and ℏ as unit conversions.

**Pass/fail, registered before any physics is written:**

| outcome | grade |
|---|---|
| μ/S = e/m (g=2) falls out with no chosen radius ratio, no fitted ε, no second loop | [DERIVED] |
| μ/S = e/m only if a ratio between the charge's effective circuit and the momentum's is *chosen* to be 2 | [ASSERTED] — say so; record the ratio that was needed |
| μ/S = e/2m (g=1) | [FALSIFIED for this construction] — the theorem wins; record why the topology did not evade it |
| anything else | record the number; do not round toward 2 |

**What green means:** that the ℤ₂ double cover shows up as a measurable ratio. What it does not mean: agreement with QED's 2.0023… — that is the α-invoice, out of scope.

## What you may not do
- Import Dirac's equation and call it a derivation. Dirac is the answer to be *matched*, from a picture, not the picture.
- Use the archived toolkit (`todo_refactor/tests/g_equals_2_mobius/`) except as a specimen of what not to do.
- Add a second charged loop. Two loops of co-moving charge give g=1 by theorem. If you find yourself doing that, stop and write down why.

## Precedents to read (on the shelf, `papers/quantum/md/`)
Battey-Pratt & Racey 1980 (`-READING-NOTES` first); the Physics Detective guidance notes (`docs.local/`); Williamson & van der Mark 1997 once fetched — their charge came out **0.91e**, which is what an honest miss looks like.

## Return
`tests/g-factor/README.md` (the test, first commit), then the computation as a script that prints μ/S and the inputs it used, then the grade. Under 600 words of prose. Measured separately from concluded.

## WITHHELD
The hypervisor has a view on which of the four outcomes this reaches and is not stating it. "I ran it and got g=1" is a complete, valuable answer.
