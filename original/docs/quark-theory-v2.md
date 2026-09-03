# Geometric Reinterpretation of Deep Inelastic Scattering — v2

**v2, 2026-08-24 (Grace Bayes, with Gordon Cooper's derivations adjudicated).** Supersedes `deprecated/quark-theory.md`. Changes from v1: the thirds lemma (which was algebraically inconsistent — its constraints proved 0=1) replaced by the repaired 2×2 system; Gordon's q²-coupling mechanism adopted with the occupancy/menu conflation fixed; the R-ratio prefactor-3 debt posted; the F₂ oscillation section rewritten after the kernel was shown band-limited (the v1 headline prediction was unobtainable from the v1 formula); frozen-geometry (w,d) computed exactly; structural Koide exemption added. v1's audit trail: `deprecated/quark-rail-audit.md`.

## 1. Core hypothesis (unchanged)

What SLAC identified as point-like partons are **edge-aligned rail currents** on the truncated-octahedron (TO) nucleon capsid. Nucleon: 8 hexagonal + 6 square faces, 24 vertices, 36 edges — **12 hex-hex edges** (all lying in the three coordinate planes, **4 per plane**) and 24 hex-square edges. The three coordinate planes define the **three orthogonal rail families**. Confinement = rails are closed loops with no endpoints. [POSIT]

## 2. The thirds — repaired lemma [THEOREM, conditional on the occupancy posit]

v1's lemma assumed the proton triple was (x,y,y) with x+2y=1 and 2y=−x — jointly inconsistent (0=1), and its "derived" triple (2/3,−1/3,−1/3) sums to 0 (the *neutron* condition). The repair separates the **charge menu** {x,y} from the **occupancy**:

    proton (x,x,y):   2x + y = 1
    neutron (x,y,y):  x + 2y = 0        [isospin = swap ONE family's occupancy x↔y]

Linear, det = 3 ≠ 0 → **unique, parameter-free: x = 2/3, y = −1/3.** No coprimality/minimality axiom needed. The single geometric assumption doing all the work: **isospin acts by swapping one rail family's occupancy** ("two forward one side" ↔ "one forward two side"). That posit is what the capsid geometry must justify.

## 3. Square-law coupling [MECHANISM DERIVED — numbers corrected]

Gordon's derivation, adopted: the virtual photon couples to family a's current linearly in its charge weight, J_a = q_a j(u), so the amplitude M_a ∝ q_a ĵ(x) and the incoherent cross-section gives

    F₂^geom(x) ∝ Σ_a q_a² |ĵ_a(x)|²

— square-law coupling earned, not borrowed. **Two corrections to the v1/Gordon numerics:**

1. **DIS on a proton uses the occupancy, not the menu:** Σq_a² = (2/3)²+(2/3)²+(−1/3)² = **1** (neutron: 2/3). Gordon's Σq² = 2/3 reused the pre-repair triple — the exact menu/occupancy conflation the repair exists to prevent. Naive-parton F₂^p/F₂^n = 3/2 falls out as a free check. Note also the u-rails and d-rail then carry different currents, so ĵ_a are *not* all identical — the cubic-symmetry shortcut holds only per charge class.
2. **The R-ratio needs a second, independent 3.** SM: R = N_color × Σ_flavors e_f² = 3 × 2/3 = 2 below charm — **two different indices multiplied**. The rail model so far has *one* three (families = the flavor-menu axis). Writing "R = 3Σq²" imports the SM prefactor without a geometric origin.

**Gordon's color proposal (cycle 4): color = the 3D spatial orientation of the instantiated TO relative to the probe axis.** Adjudicated [PROMISING POSIT, NOT DERIVED — one free win, two named gaps, one sharp falsifier]:
- *Free win:* a baryon = one TO with three orthogonal families; the antisymmetric combination over three orthogonal axes is the volume form ε_ijk — which is exactly the SM's color-singlet baryon structure ε_abc, and it dissolves the Δ++ spin-statistics problem the way color was invented to. Unasked-for structural agreement; credit it.
- *Gap 1 — discreteness:* an isotropic vacuum permits a **continuous** SO(3) of orientations (mod O_h, still continuous), which integrates to an average, not a ×3 multiplicity. The discrete 3 requires that only axis-aligned instantiations are allowed (resonance/on-shell argument?) — currently asserted.
- *Gap 2 — observability:* spatial orientation is measurable (angular distributions); color is exactly unobservable. Orientation-color needs its own confinement-of-orientation-information mechanism.
- *Falsifier — π⁰→γγ (the coherence test):* the anomaly amplitude is ∝ N_c: rate ∝ N_c² = 9× the single-channel value, Γ = 7.75 eV vs PrimEx 7.80 eV ✓. But "three **equally probable** orientations" is a *classical, incoherent* sum: rate ×3 only ⟹ Γ = 2.58 eV — **excluded by data**. So the orientation triple must sum **coherently in the loop** (a quantum superposed label) — at which point it behaves as an internal quantum number and the classical-instantiation language must go.

*Cycle-5 adjudication of Gordon's coherent upgrade:* **mixture-vs-superposition settled in favour of superposition — accepted.** Three corrections to how it was claimed:
  1. *Normalization:* with his own |Ψ⟩ = (|x⟩+|y⟩+|z⟩)/√3, the sum is M = √3·M₀ and Γ ∝ 3|M₀|², not "3M₀ → 9|M₀|²" — he dropped his own 1/√3. The physical content (coherent ≠ mixture) survives; absolute-rate bookkeeping must also track that the SM's N_c-linear amplitude holds f_π *measured* fixed (f_π itself scales ~√N — 't Hooft), so match ratios, not raw factors.
  2. *Two-way bookkeeping now owed:* the same label must sum **incoherently** in R (final-state multiplicity: rate ×3, not ×9) and **coherently** in the π⁰ loop (bound singlet initial state). A proper internal quantum number does both automatically; the model must state which sums are over final states and which are inside amplitudes — once, in general, not per-process.
  3. *"We derived confinement" — [REJECTED as non sequitur].* Coherence/traced-out-ness of an internal label does not make it unobservable: **spin** is a coherent internal d.o.f. and is measured every day (Stern-Gerlach). QCD confinement = no colored *asymptotic states* — a dynamical statement. What the model actually has is its own confinement *posit* (closed loops, no endpoints — families can't be isolated), which is fine and was already in v1. Status: [COHERENT LABEL ESTABLISHED; CONFINEMENT REMAINS A POSIT].

**Warning standing from the audit:** the model now juggles color-3 (families? prefactor?), generation-3 (Koide Z₃), and menu-vs-occupancy. These are different threes in the SM with severely bounded mixing. No silent fusion.

## 4. Koide exemption [STRUCTURAL]

Quarks fail Koide's Q=2/3 because **there are no quark μ-rotators**: "quark masses" are scheme-dependent parameters of collective rail modes, not trapped-rotation frequencies of free rotators. m = ℏω/c² applies only to free μ-folds — the charged leptons (and, with the signed branch, the neutrinos: Σm_ν ≈ 58.6 meV, see `koide-equipartition-audit` → carried in the Koide scrolls). This supersedes the dynamical flux-tube exemption.

## 5. The F₂ oscillation — v1's headline prediction was unobtainable from v1's own formula [KILLED AND REBUILT]

**The band-limit theorem (fatal to v1 as written):** v1 predicted Δx ∈ [0.06, 0.12] (8–16 cycles across x∈[0,1]) from ĵ(x) = ∫₀¹ j(u) e^{i2πux} du. But with u ∈ [0,1] and x ∈ [0,1], the phase 2πux sweeps at most one cycle — **|ĵ(x)|² cannot oscillate faster than once across the full x range.** Computed on the exact frozen geometry: zero extrema in [0,1], a single monotone lobe. The [0.06, 0.12] numbers (which drifted across v1's drafts: 0.03→0.3→6.7→0.08, never derived) were structurally impossible outputs of the stated kernel. No amount of (w,d) extraction fixes this.

**What the frozen geometry actually gives (computed, exact closed forms):** equatorial rail loop per family = 4 hex-hex edges (length √2) alternating with 4 square traversals (length 2), L = 8+4√2:

    w = 4√2/L = √2 − 1 ≈ 0.41421          (active fraction)
    per-gap d = (2−√2)/4 ≈ 0.14645          (4 gaps, exactly equally spaced by symmetry)

Four equally-spaced segments → spectral content only at loop-harmonics n = 4, 8, 12, …

**The rebuilt prediction requires a winding number.** To place oscillations in observable x, the kernel must be e^{i2πNux} with N = coherent windings of the rail current per interaction (a physical input v1 never named). Dirichlet peaks sit at x = 4k/N, spacing Δx = 4/N. The model's frozen, N-independent content: **any genuine oscillation has 4-fold harmonic structure** — peaks at x = 4k/N only, never 3k/N or 5k/N (the 4 comes from the 4 hex-hex segments and cannot move).

**Gordon's N = 1/(2α) ≈ 68.5 proposal (cycle 4) — adjudicated [REJECTED AS DERIVATION, RETAINED AS SCALING ANSATZ]:**
- *Circularity catch:* the "[33, 67] window" Gordon aimed at was back-derived from v1's Δx ∈ [0.06, 0.12] — numbers this document's own audit showed were walked, never derived. Deriving N to land in a window whose only source is a discredited guess is painting the target around the arrow. **The window is void and is hereby withdrawn**; only Δx = 4/N (geometry) survives as constraint.
- *Arithmetic catch:* 68.5 lies *outside* [33, 67] anyway, and Δx = 8α = 0.0584 falls *below* v1's [0.06, 0.12]. "Precisely at the boundary" was precisely beyond it.
- *What survives:* the physics skeleton is respectable — a closed EM waveguide's coherent-cycle count (Q-factor) scales inversely with its leakage coupling, and in this model the current's environment coupling is electromagnetic, so **N = c/α** with c an O(1) geometric constant is a legitimate ansatz. But c = 1/2 ("half-wave") was chosen post-hoc. Registered form: **Δx = 4α/c** (c=1/2 → 0.0584; c=1 → 0.0292; c=2 → 0.0146), with the α-proportionality itself falsifiable in principle.
- *How to earn c:* v1's own Methods section is the machine — the Helmholtz edge-mode eigenproblem with Im(ε) loss gives the rail mode's actual Q-factor. Run it; c comes out; then the prediction registers. Until then N is an ansatz wearing a constant it hasn't paid for.
- *Gordon's integral definition (cycle 5) — [REJECTED: dimensionally broken].* c = ∫_edge|ψ|²dS / ∮_∂P|∇ψ|²dl has dimensions [ψ²L²]/[ψ²L⁻¹] = **L³** — not dimensionless. An O(1) constant cannot carry units (the C-as-speed error, third appearance). **Corrected protocol, registered:** solve the Bloch eigenproblem with complex ε_pore = ε_p(1 + i·η), η = 1 (unit loss); the lowest edge-localized band gives complex k; the *dimensionless* geometric quality is Q_geom = Re(k)/(2·Im(k)); then **N = Q_geom·(η/α)** — the α enters once, explicitly, as the physical loss amplitude replacing the unit η, and c ≡ Q_geom·η. No integrals assembled by hand; the eigenvalue does the bookkeeping.
- *Spec correction (cycle 7):* Gordon's BVP used w = √2−1 as the dielectric strip *width*. w is the rail-loop **arc fraction** of hex-hex edges — a 1D fraction of loop length, not a wall thickness. The wall thickness t is an independent, unfixed geometric parameter; launder w into that role and the number is wrong by construction. Protocol: scan t, report sensitivity.

**FIRST-PASS SOLVER RUN (cycle 7, in-session; 96² FD grid, square lattice of circular pores — stated approximations: scalar field, Γ-point, first-pass lattice geometry):** scanning t ∈ {0.1, 0.2, 0.3}, ε_shell ∈ {4, 12}, η = 1: the most shell-localized mode gives **Q_geom ∈ [7, 74]** — never lower than ~7 anywhere in the scan. Hence:

    N = Q_geom/α ∈ [~970, ~10 100]      Δx = 4α·Q_geom⁻¹ ∈ [0.0004, 0.004]

**Implication [MAJOR]: the model's own mechanism predicts F₂ oscillations 3–30× finer than any feasible binning (δx ≥ 0.01) — i.e. a NULL observable result at HERA.** A_res = exp[−½(2πσ_x/Δx)²] annihilates structure finer than the bin. The v1 dream of visible per-mille ripples dies under the theory's own Q-factor: an edge-guided mode good enough to be a rail is too coherent to ripple coarsely. This is a *protective* result — it forbids the program from claiming any coarse HERA residual as signal (any structure at Δx ≳ 0.01 would now be evidence AGAINST the model, or of physics outside it). Escapes, for the record: Q_geom < 2 requires a barely-confined mode (contradicts the edge-guiding premise); or a decoherence channel much stronger than EM leakage (foreign to the model). Refinement to honest-second-pass: hex lattice, vector field, k-scan, convergence — expected to move Q by O(1) factors, not orders.

**Kept verbatim from v1 (good falsifier design):** phase φ stable across Q² bins; amplitude monotone ↓ in Q²; fixed period; proton target, Q² ∈ [5,20] GeV², fine binning δx ≤ 0.02. Confront `../models/hera_explorer/` only after N is registered.

## 6. Status ledger

| item | status |
|---|---|
| thirds (2/3, −1/3) unique | [THEOREM] conditional on occupancy-swap posit |
| q² coupling mechanism | [DERIVED] (Gordon), incoherence assumption noted |
| proton Σq² = 1 (occupancy) | [CORRECTED] — menu ≠ occupancy |
| R-ratio prefactor 3 | [PROMISING POSIT] — orientation-color; must go coherent or die on π⁰→γγ |
| confinement = closed loops | [POSIT, natural] |
| Koide quark exemption | [STRUCTURAL] — no quark rotators |
| F₂ oscillation | [FIRST-PASS COMPUTED]: Q_geom ∈ [7,74] ⟹ Δx ∈ [0.0004, 0.004] — **below binning: predicted NULL at HERA**; coarse structure would falsify |
| Callan-Gross (spin-½) | [OWED] — rails must yield 2xF₁=F₂ |
| asymptotic freedom / β-function | [OWED] — the mountain; QCD-as-EFT claim carries it |
