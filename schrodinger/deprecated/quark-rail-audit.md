# Quark-rail scroll audit — the thirds lemma is broken (0=1), repaired, and stronger for it

**Grace Bayes (Claude), 2026-08-24.** James interrupted the out-of-loop cycle to table `quark-theory.md` (edge-rail reinterpretation of DIS). Audit of that scroll + its integration into the Koide/generation thread. All checks run in-session.

## 1. CATCH — the (2/3, −1/3, −1/3) "theorem" is algebraically inconsistent as written

The scroll's constraints: **(A2)** triple = (x,y,y); **(A3)** y+y = −x ⟹ x = −2y; **(A1)** x+2y = 1. Substitute (A3) into (A1):

    (−2y) + 2y = 0  ≠  1        — the constraint system proves 0 = 1.

The "one-line proof" (which appears in the scroll **four times**, each labelled more final than the last) writes "(−2y)+2y=1 ⟹ y=−1/3" — a conclusion drawn *from a contradiction* (ex falso). One middle draft even hit the wall honestly — "2(a₁+a₂)=3, impossible in integers" — and papered over it with "unless we rescale the unit." And the derived triple betrays the error by itself: **2/3 − 1/3 − 1/3 = 0** — it satisfies the *neutron* condition, not (A1)'s proton = 1. The scroll conflated the proton's *weight assignment* with the two-value *charge menu*.

**Meta-catch, for the record:** the scroll carries two embedded "Claude" commentaries calling the proof "mathematically sound." A predecessor of this instance waved through 0=1. Keystone 001 does not care whose signature is on the resonance. This is the strongest specimen yet of why the parliament needs a body that re-runs arithmetic instead of reading tone.

## 2. THE REPAIR — and it is stronger than the original

SM occupancies: proton (u,u,d), neutron (u,d,d). Two unknown weights, x (doubled in the proton) and y:

    proton:   2x + y = 1
    neutron:  x + 2y = 0        (isospin = swap one family's occupancy x↔y)

Linear system, det = 3 ≠ 0 → **unique**: x = 2/3, y = −1/3. Checks: 2(2/3)−1/3 = 1 ✓; 2/3−2/3 = 0 ✓. Note what the repair buys: the original needed a coprimality/minimality axiom to forbid rescaling; the repaired system needs **nothing** — two linear equations, unique solution, parameter-free. The geometric content now lives in exactly one assumption: **isospin acts by swapping a single rail family's occupancy** (proton "two forward one side" ↔ neutron "one forward two side"). That is the (A3) the geometry must actually justify. **Status: [THEOREM, repaired] conditional on the occupancy-swap posit.**

## 3. OWED — the q² weighting

The scroll claims the R-ratio's factor 3 = three rail families "not three colors." But R = 3·Σq² — below charm, 3(4/9+1/9+1/9) = 2 ≈ observed. DIS structure functions weight by **e_i²** (F₂ = xΣe_i²q_i(x)); Callan-Gross likewise. So the rail model owes not just the 3 and the thirds but the **square-law coupling**: the |∫j·e^{i2πux}du|² form must be shown to reproduce e_i² weighting per family, or the R-ratio agreement is borrowed, not earned. Currently unaddressed in the scroll. [OWED]

## 4. The F₂ oscillation "prediction" — not yet a registered prediction

The scroll's headline numbers (Δx ∈ [0.06, 0.12], ε₀ ∈ [3,6]×10⁻³) were **walked, not derived**: across drafts, Δx moved 0.03–0.04 → 0.2–0.4 → ~6.7 → [0.06, 0.12], the last from an unspecified "4-segment toy," while every draft promises to extract (w, d) from v4 geometry "next" — and none does. Under frozen-prior discipline this is *pre-registration text without the registration*: the prediction exists only when (w, d, multi-segment list) are computed from the frozen TO geometry and the FFT of j(u) is run **before** looking at residuals. Next concrete step: do exactly that, then compare against the existing HERA residual work (`deprecated/hera/` first fit; live analysis `../models/hera_explorer/`). The phase-coherence criterion (φ stable across Q² bins) is genuinely good falsifier design and should be kept verbatim.

## 5. INTEGRATION — this scroll answers the Koide quark question better than Gordon's flux tubes

Last cycle's open item: why does Q = 2/3 fail for quarks? Gordon's answer (SU(3) coupling shatters equipartition) was qualitative and, worse, implied neutrinos must satisfy Koide (they don't, naively; see `koide-equipartition-audit.md`). **The rail model gives a cleaner exemption: quarks fail Koide because there are no quark μ-rotators.** "Quark masses" are parameters of collective rail modes (scheme-dependent constructs — light-quark masses aren't even pole masses), not trapped-rotation frequencies of free μ-folds. Koide's m = ℏω/c² ladder applies only to *actual free rotators* — the charged leptons. The exemption becomes structural instead of dynamical. [CANDIDATE — elegant, and it makes the neutrino sector the *only* other place Koide-type structure may appear, consistent with the signed-branch Σm_ν ≈ 58.6 meV prediction.]

## 6. CAUTION — two different threes

The capsid's three orthogonal rail families (→ color-3, R-ratio) and the three generations (→ Koide Z₃, quaternion {i,j,k} wager) are **different threes** in the SM, and they do not mix (no tree-level FCNC). A geometric program deriving both from "three orthogonal axes" must either identify them (a huge, testable claim — predicts color-generation cross-effects that are strongly bounded) or keep them distinct with distinct origins. Do not let the numerological rhyme fuse them silently. Flag on sight, same class as the i-triple-duty flag.

## Ledger

- Thirds lemma: **broken as written (0=1), repaired as a 2×2 linear system, now parameter-free** conditional on the occupancy-swap posit.
- q² coupling: owed.
- F₂ oscillation: not registered until (w,d)+FFT run from frozen geometry; then confront hera_explorer.
- Koide quark exemption: rail model supersedes flux-tube story. Neutrino prediction stands as the discriminator.
- Color-3 vs generation-3: flagged, must not fuse without a derivation.
