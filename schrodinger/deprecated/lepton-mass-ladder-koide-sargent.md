# The lepton mass ladder — Koide is the geometric constraint, Sargent is the lifetime law

**Grace Bayes (Claude), 2026-08-24.** James-out-of-loop cycle; Gordon's question: *if μ is the spin-½ fermion and m = ℏω/c², what geometric fold forces the muon/tau mass and instability profiles?* Companion to `mu-particle-model-clearance-pass.md` and `conjecture-lexicon.md`. All numbers below reproduced in-session (PDG masses); Koide verified to −0.0009%, Sargent to ~1%.

## The two invoices are separate. Do not conflate them.

Gordon's question bundles **mass** and **instability**. They have **different** answers. Mass is set by a geometric constraint on frequency (Koide). Lifetime is set by phase space (Sargent m⁵). My previous turn said "stable vs transient = topological barrier heights" — **that framing was wrong and I retract it here** (see §3). The barrier is not what sets the rate.

## 1. Mass = frequency, so the ladder is a frequency ladder

BP&R: m = ℏω/c². Then the three leptons are one μ-rotator in three modes, and the "step-up" Gordon asks for is literally a frequency ratio:

    ω_μ/ω_e = m_μ/m_e = 206.768
    ω_τ/ω_e = m_τ/m_e = 3477.19

The question "what fold forces these numbers" is the **generation problem** — unsolved in the Standard Model, where the three Yukawa couplings are just three free inputs. A geometric ω-theory has no right to three free inputs; it must *predict a relation among them.* One exists.

## 2. Koide: the √-mass vector sits at exactly 45° to the democratic axis [THE RESULT]

Koide (1981), empirical and unexplained in the SM:

    Q  =  (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²  =  0.6666605  ≈  2/3   (−0.0009%)

Write the √-mass vector **v = (√m_e, √m_μ, √m_τ)** in generation-space and the democratic axis **n̂ = (1,1,1)/√3**. Since Σmᵢ = |v|² and (Σ√mᵢ)² = 3(v·n̂)²:

    Q = |v|² / [3 (v·n̂)²] = 1 / (3 cos²θ),   θ = angle(v, n̂)

    Q = 2/3  ⟺  cos²θ = 1/2  ⟺  **θ = 45.000°**   (computed: cos²θ = 0.500005, θ = 44.9997°)

**That is the geometric fold Gordon asked for, stated exactly.** The mass ladder is not three numbers; it is a single locked angle: in the 3-space of √ω (one axis per generation), the physical mass vector bisects the democratic axis and the fluctuation plane at 45°. Equivalently, in Z₃-symmetric form:

    √m_k = √M · (1 + √2·cos(δ + 2πk/3)),   k = 0,1,2

Fitting the data: **√M = 17.716 √MeV** (M ≈ 313.8 MeV), **δ ≈ 0.222 rad**, residual 3×10⁻¹⁰ — the √2 amplitude and 120° spacing are *exact* (they ARE Q=2/3), only δ and the scale √M are free. Three generations = **three phases of one rotation at 120° on a circle.** The Z₃ is not decoration; it is the three-fold fold.

**Bookkeeping of freedom:** three masses → **one geometric constraint fixed (cos²θ=1/2)** + one phase δ + one scale √M. The theory has already, for free, spent two of the three degrees of freedom on geometry. That is the win.

## 3. Lifetime = Sargent's m⁵ law, NOT barrier height [self-correction]

The instability ladder is a *different* mechanism and my "topological barrier" language last turn was romance. Weak decay rate goes as phase space:

    Γ = G_F² m⁵ / (192π³)   (Sargent's rule; per leptonic channel)

Check against data (τ_μ = 2.197 µs, τ_τ = 0.2903 ps):

    τ_μ/τ_τ (observed)   = 7.57×10⁶
    (m_τ/m_μ)⁵           = 1.345×10⁶
    ratio (channel factor) = 5.63   ≈  1/B(τ→e) = 5.61  ✓

The tau is shorter-lived than the naive m⁵ by exactly the factor by which it opens more channels (e, µ, and hadronic — ~5 of them). **The lifetime ladder is m⁵ phase space × channel count, to ~1%.** No topological barrier height is doing the work.

And the electron's stability is **kinematic, not a giant barrier**: it is the lightest electrically charged fermion, so charge + energy conservation leave it *nothing to become*. Γ = 0 because the phase space is empty, full stop.

## 4. What is won, what is owed (the clearance ledger)

**Won.** For a theory in which mass IS trapped rotation frequency, Koide is exactly the relation that theory is *obligated* to produce — and it holds to 5 sig figs. The generation problem's three free numbers collapse to `cos²θ = 1/2` + one phase + one scale. Lifetimes then follow from m⁵ with no new parameters. This is real, and it is the strongest quantitative foothold the geometric program has touched.

**Owed (the honest bill):**
- **Derive cos²θ = 1/2.** Why √2 amplitude / 45°? This should come from an equipartition between the democratic mode and the two-dimensional fluctuation plane of the μ-fold — *that derivation does not yet exist.* Until it does, Koide is a magnificent clue we are *matching*, not *explaining*.
- **Derive δ ≈ 0.222 rad** and the scale √M ≈ 17.7 √MeV (M ≈ 314 MeV, suggestively near the constituent-quark scale — but that is numerology until derived).
- **Radiative subtlety:** Koide is stated with pole masses; it holds even better with QED-run masses at some scale — the theory must say *which* masses (bare, pole, running) the geometry constrains, or the 45° is only approximately meaningful.
- Koide famously *fails* to extend naively to quarks and neutrinos with the same Q=2/3; a geometric derivation must explain why the leptons are special (or predict the correct Q for the others). This is the real falsifier.

**One-line answer to Gordon:** the fold is a **Z₃-symmetric three-mode excitation of a single μ-rotator, whose √-frequency vector is locked at 45° to the democratic axis (Koide, cos²θ=1/2)**; the instability is **not** that geometry but **Sargent m⁵ phase space × channel count** on top of it. The mass geometry we can now *state exactly and must next derive*; the lifetimes are already explained.
