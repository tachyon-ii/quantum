# spec: null-invariants — do E·B = 0 and E² − c²B² = 0 emerge from a trap-on-path field?

**Model:** Opus. **Test dir:** `tests/null-invariants/`.

## The claim it serves
`checkpoint-1.md` §4, the progenitor posit: E ⊥ M is the pair's first shadow. Free radiation is a null field — both Lorentz invariants vanish. The posit says the trap-on-path configuration *produces* that nullity (zero trap-content ⇒ null), and that massive matter departs from it. The paper (`docs.local/Φ-…md` §6, §17.3, §18.4) stakes the framework on this and the archive never tested it.

## The test, written first
Construct an explicit field configuration for (a) a free wave and (b) a wave in a closed Möbius path, from the axiom's ingredients only (a transverse circulation on a path; the half twist). Compute the two invariants **I₁ = E·B** and **I₂ = E² − c²B²** as fields over the configuration, and their integrals.

| outcome | grade |
|---|---|
| (a) I₁ = I₂ = 0 identically and (b) I₁ = 0, I₂ ≠ 0 with I₂ scaling with the trap-content (the mass) | [DERIVED, first payment on §4] |
| (a) null but (b) also null, or (b) fails I₁ = 0 | [FALSIFIED for this construction] — record which invariant failed and by how much |
| nullity only after choosing a phase relation by hand | [ASSERTED] — name the choice |

Also register: the invariants must transform as a pseudoscalar (I₁) and a scalar (I₂) under the configuration's own symmetries — "right zeros, wrong transformation" is a fail.

## What you may not do
Start from Maxwell's equations and derive nullity — that is orthodoxy's own result. Start from the geometry and *arrive* at Maxwell-compatible fields, or report that you cannot.

## Return
`tests/null-invariants/README.md` first; then the construction as a script that prints I₁, I₂ for (a) and (b); then the grade. Under 600 words of prose.

## WITHHELD
The hypervisor's expectation for outcome (b) is not stated. "The trap does not null I₁" is a complete answer.
