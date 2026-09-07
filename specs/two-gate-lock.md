# spec: two-gate lock — does annihilation probability rise or fall with relative velocity?

**Model:** Opus. **Test dir:** `tests/annihilation-velocity-gate/`. **Drafted:** Neyman (quantum), 2026-09-07, from the crack registered in `checkpoint-1.md` §8 and `docs.local/now.md` §2a.

## The claim it serves
`todo_refactor/docs/annihilation.md` Part IV: e⁺e⁻ annihilation requires *both* the E and the M loop to reinforce in phase **and** a relativistic relative velocity — "too slow → they bounce off." Part III supplies the machinery: `dE/dt = (κA² − Γ)E`, threshold `∫₀^τ_coh (κA² − Γ) dt > ln(E_bind/E(0))`. The bee's objection (2026-09-07): higher velocity raises frequency and packet volatility, so it should raise alignment probability, not gate it. The model owes the sign of `dP/dv`.

## The test, written first
From Part III's symbols and **nothing added**, derive how each of κ, A, Γ, τ_coh depends on the relative velocity v of an e⁺e⁻ pair, and hence P_ann(v), the probability the threshold integral is met. Report `dP/dv` sign at low v (β ≪ 1) and at high v.

**Referents the result is compared against** (measured, not ours):

- Dirac 1930 / PDG: the e⁺e⁻ → γγ cross-section at low velocity goes as **σ ≈ π r_e² / β** — it *rises* as the pair slows.
- Positronium annihilates **at rest**: p-Ps 125 ps, o-Ps 142 ns. PET works because positrons thermalise *then* annihilate.

**Pass/fail, registered before any physics is written:**

| outcome | grade |
|---|---|
| P_ann(v) from Part III's own threshold integral gives dP/dv < 0 at low v (matches 1/β and Ps-at-rest) with no new constant; the "velocity gate" of Part IV re-reads as a different quantity and the spec names it | [DERIVED] — Part IV rewritten; Part III survives |
| dP/dv < 0 only after adding a parameter or a dependence Part III does not contain | [ASSERTED] — name the addition |
| Part III's symbols yield dP/dv > 0 (Part IV as written) | [FALSIFIED against the referents] — Part IV goes to `_condemned/` with the number; Part III's threshold is [OPEN] pending a mechanism that turns the sign |
| the symbols do not determine a sign | [OWED] — Part IV downgraded to [POSIT, contradicted by data] on the ledger |

Register the sign *before* the fit. A curve that matches σ ∝ 1/β only after κ(v) is tuned is the ε-fit of `now.md` §3 again — record it as [ASSERTED], not as agreement.

**What green means:** the parametric-pump picture has a velocity dependence with the right sign, unforced. What it does not mean: the 2-γ/3-γ branching, the 125 ps number, or anything about neutrinos — Part IV's neutrino-sea argument rests on "e⁺ in protons," a separate posit, out of scope here.

## What you may not do
- Import QED's cross-section and call the sign derived; QED is the referent, not the picture.
- Treat "critical velocity crunch" as a fact to be explained. It is the claim under test.
- Widen to neutrinos. One pair, one sign.

## Return
`tests/annihilation-velocity-gate/README.md` (this test, first commit), then a script that prints P_ann(β) for β ∈ {0.001, 0.01, 0.1, 0.5, 0.9} with the dependence it assumed for each symbol, then the grade. Under 600 words of prose. Measured separately from concluded.

## WITHHELD
The hypervisor has a view on which of Part III's four symbols carries the sign and is not stating it. "The symbols do not determine a sign" is a complete, valuable answer.
