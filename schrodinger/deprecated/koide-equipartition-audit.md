# Koide "equipartition derivation" — audit, neutrino falsifier run, and the N=3 question

**Grace Bayes (Claude), 2026-08-24.** James-out-of-loop cycle 2. Gordon proposed: Q=2/3 derived from "equipartition" of strain energy between the 1D democratic core and 2D anisotropic plane; quarks exempt via SU(3) flux-tube coupling; asked what forbids a 4th Z₃ phase. All numbers computed in-session. Companion to `lepton-mass-ladder-koide-sargent.md`.

## 1. CATCH — "equipartition" is mislabeled; the derivation assumes its answer

True **per-mode** equipartition (the actual physical principle: equal energy per degree of freedom) over 3 modes (1 democratic + 2 flavor) gives:

    |v_iso|² = ⅓|v|²  →  cos²θ = ⅓  →  Q = 1     [computed]

Gordon's condition |v_iso|² = |v_ani|² is **subspace balance**: the single democratic mode carrying as much energy as *both* flavor modes combined — a **2:1 per-mode weighting** of the democratic mode. That is not equipartition; it is a specific non-equipartition, chosen because it yields 2/3. As stated, the derivation renames the mystery ("why 45°?" becomes "why 2:1?") rather than solving it. **Status: [NOT A DERIVATION — a reformulation].**

## 2. The rescue candidate — and it is native to the corpus [CANDIDATE, underived]

BP&R's rotator is not democratic between core and medium: **the core spins at 2ω, the configuration/medium at ω** — a structural factor of 2, already in the canonical mechanics. If the democratic mode is the *core* mode and the flavor plane is the *medium* deformation, a 2:1 energy weighting is exactly what the 2ω/ω split would supply, and subspace balance follows:

    E_iso : E_per-flavor-mode = 2 : 1  ⟺  |v_iso|² = |v_ani|²  ⟺  Q = 2/3

This upgrade path is real but **owed**: derive (not assert) that the generation-space democratic mode inherits the core's 2ω. Until then, [CANDIDATE].

**Prior art (credit where due):** the cos²θ=1/2 geometric reading is R. Foot (1994, hep-ph/9402242); the Z₃ parametrization is Koide's own; the signed-branch neutrino move (§3) is C. Brannen (2006). We adopt; we did not invent.

## 3. The neutrino falsifier — RUN. Gordon's exemption story fails; the Z₃ form itself survives with a unique prediction

Gordon exempted quarks from Q=2/3 via SU(3) flux-tube coupling: "leptons are the only structures allowed to deform freely." **Then neutrinos — chargeless, colorless, the freest leptons of all — must satisfy Q=2/3.** Computed against oscillation data (Δm²₂₁=7.53×10⁻⁵, Δm²₃₁=2.453×10⁻³ eV²), scanning the lightest mass 0→0.2 eV:

    NH: Q ∈ [0.333, 0.581]  — 2/3 NOT reachable
    IH: Q ∈ [0.333, 0.500]  — 2/3 NOT reachable

**The free-deformation story as stated is falsified by the neutrino sector.** But the Z₃ parametrization √m_k = √M(1+√2cos(δ+2πk/3)) contains its own escape: the amplitude goes **negative** when cos < −1/√2 — a phase-π (antispin?) branch. Testing the signed Koide sum Q* = Σm/(Σ±√m)²:

    signs (−,+,+): unique solution  m₁ = 0.373 meV, m₂ = 8.69 meV, m₃ = 49.53 meV, Σm = 58.6 meV
    signs (+,−,+) and (+,+,−): no solution

**A unique, sharp prediction** (normal hierarchy; matches Brannen 2006): Σm_ν = 58.6 meV — comfortably under the cosmology bound (<120 meV) and *testable* (CMB-S4/DESI will reach ~60 meV sensitivity; also m_β for KATRIN-successors). In the geometric language: **the first-generation neutrino sits on the negative-amplitude branch of the Z₃ circle** — its √-strain is phase-inverted relative to its charged partners. If the fold means anything, it must say *why* exactly one neutrino mode is inverted (antispin on one axis?). If Σm_ν is measured far from ~59 meV, the signed-Z₃ form dies. This is now the program's cleanest falsifier.

## 4. What forbids a fourth generation — the circularity catch, the data, and the quaternion wager

**Catch:** Gordon's question is circular as posed. The 3-space of the Koide construction was *built from* the three observed leptons; Z₃ presupposes N=3, it cannot forbid N=4 (a 4th lepton would simply make it a 4-space with some Z₄/other structure). Nothing in a 2D plane forbids 4 phases at 90° instead of 3 at 120°. The N must come from elsewhere.

**Data bar:** LEP Z-width, N_ν = 2.9840 ± 0.0082 — a 4th light active neutrino is excluded at ~2‰. Any 4th generation must be heavy or sterile; the geometry doesn't get to choose freely.

**The wager worth making [WAGER, underived]:** the quaternion algebra ℍ has **exactly three imaginary units {i, j, k}** — three orthogonal twist generators of SU(2), no fourth. If the three generations are the three *axes* available to the μ-fold's anisotropic deformation, then N=3 is forced by the algebra BP&R already committed to: **there is no 4th imaginary unit for a 4th generation to live on.** Note what this does: it welds the generation count to the `i`-identity flag in `conjecture-lexicon.md §C` — the same i whose triple duty (rotation/information/trajectory) is the lexicon's open item. If generations = {i,j,k}, then "why 3 generations" and "what is i" are one question. Owed: an actual mapping from {i,j,k} to the Z₃ phases (the 120° circle lives in a plane; the three quaternion axes are mutually orthogonal — the map is not trivial and might fail).

## Ledger after this cycle

- Q=2/3 "equipartition derivation": **rejected as stated**; 2:1 weighting must be derived — candidate source: BP&R's 2ω core / ω medium. 
- Quark exemption: qualitative, unproven, and **its own logic forced the neutrino test, which the naive form failed.**
- Signed-Z₃ neutrino prediction: **Σm_ν ≈ 58.6 meV, unique branch (−,+,+)** — the program's sharpest falsifiable number.
- N=3: not explained by Z₃ (circular); LEP bounds any 4th light ν; quaternion {i,j,k} wager filed.
