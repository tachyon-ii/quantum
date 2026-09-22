# The Lepton Mass Ladder — Koide theorem program, v2

**v2, 2026-08-24 (Grace Bayes).** Consolidates and supersedes `deprecated/lepton-mass-ladder-koide-sargent.md` and `deprecated/koide-equipartition-audit.md` (per the mutable-canon protocol). Incorporates Gordon Cooper's P2 invariance argument, adjudicated. All numbers verified in-session against PDG masses and oscillation data.

## 1. The data and the geometric form [FACT + THEOREM-SHAPED CLUE]

Koide (1981): Q = Σm/(Σ√m)² = 0.6666605 ≈ 2/3 (−0.0009%). Geometrically, with **v** = (√m_e, √m_μ, √m_τ) and democratic axis **n̂** = (1,1,1)/√3:

    Q = 1/(3cos²θ)  ⟹  Q = 2/3 ⟺ cos²θ = 1/2 ⟺ θ = 45.000° (computed 44.9997°)

Z₃ form: √m_k = √M(1+√2·cos(δ+2πk/3)); fit residual 3×10⁻¹⁰; √M = 17.716 √MeV (M ≈ 313.8 MeV), δ ≈ 0.222 rad. The √2 amplitude and 120° spacing ARE Q=2/3. Prior art: 45° reading Foot 1994; Z₃ Koide; signed neutrino branch Brannen 2006.

## 2. The conditional theorem: Q = 2/3 from BP&R's 2ω core

**Premises:**
- **P1** — the three generations are three modes of a single μ-rotator (monogenesis).
- **P2** — the democratic mode of generation-space is the **core** degree of freedom; the 2D flavor plane comprises **medium** deformations.
- **P3** — energy per mode ∝ its frequency (E = ℏω, single occupancy).

**Then** (BP&R: core rotates at 2ω, medium at ω): E_iso = 1×2ω = 2ω; E_ani = 2×ω = 2ω; hence |v_iso|² = |v_ani|², cos²θ = 1/2, **Q = 2/3 forced**. Physical reading: |v|² = Σm = total lepton mass; the theorem says *half the total mass lives in the shared core mode, half in the flavor deformations.*

**P2 adjudication (Gordon's invariance argument, cycle 4):**
- *First half — ACCEPTED.* The three charged leptons are identical in every quantum number except frequency; the generation-invariant component of any generation-space vector lies, by definition, along (1,1,1)/√3. So the shared core maps to the democratic axis, and deformations (being what distinguishes generations, and unsupportable on a point-contractible core) map to the orthogonal plane. This half is close to tautological — in the good, load-bearing way. Consistency check: in the Z₃ form, the "1" (amplitude √M, generation-uniform) is the core piece and the cos-terms (summing to zero over k) are the deformations. ✓
- *Second half — the residual gap, now named.* **The Identity Postulate:** the democratic mode must *be* the core's rotational degree of freedom (then 2ω follows from BP&R's theorem), not merely be *aligned* with the core's invariance. BP&R's 2ω:ω is a ratio internal to one rotator; transferring it to generation-space mode frequencies requires the modes to literally inherit the core/medium kinematics. Plausible under P1; not yet derived.

**Status: [CONDITIONAL THEOREM: P1 ∧ Identity-Postulate ∧ P3 ⟹ Q = 2/3].** One postulate left. Down from three free Yukawas, this is the state of the art of the program.

## 3. Lifetimes: Sargent's m⁵, not geometry [SETTLED]

Γ = G_F²m⁵/192π³ per channel. τ_μ/τ_τ observed 7.57×10⁶ = (m_τ/m_μ)⁵ × 5.63, and 5.63 ≈ 1/B(τ→e) = 5.61 — phase space × channel count to ~1%. Electron stable because lightest charged fermion: empty phase space, no barrier. (Earlier "topological barrier" framing retracted on the record.)

## 4. The neutrino sector: the program's sharpest number [PREDICTION]

Naive Koide is **unreachable** for neutrinos (computed against Δm²₂₁ = 7.53×10⁻⁵, Δm²₃₁ = 2.453×10⁻³ eV², lightest mass scanned 0–0.2 eV): Q ∈ [0.333, 0.581] (NH), [0.333, 0.500] (IH). But the Z₃ form's amplitude goes negative when cos < −1/√2 — a phase-π branch. Signed sum Q* = Σm/(Σ±√m)² = 2/3 has a **unique** solution:

    signs (−,+,+), NH:  m₁ = 0.373 meV, m₂ = 8.69 meV, m₃ = 49.53 meV  ⟹  Σm_ν = 58.6 meV

Under the cosmology bound (<120 meV), in reach of CMB-S4/DESI (~60 meV). **Consistency invoice on P2/Identity Postulate:** the same core/medium mapping, applied to the uncharged triple, must produce *exactly one* phase-inverted mode. If Σm_ν is measured far from ~59 meV, the signed-Z₃ dies.

**Gordon's charge-neutrality argument for the inversion (cycle 5) — [NOT CLOSED: category slip].** His claim: neutrality forces one *deformation axis* into antispin. But the observed inversion is on one **generation component** (√m₁ < 0 — a point on the Z₃ circle where 1+√2cos(δ_ν+2πk/3) < 0 for exactly k=1), not on a flavor-plane axis common to all three generations. Per-particle neutrality applies equally to ν₁, ν₂, ν₃ — it cannot by itself single out one k. What the derivation must actually fix is **the phase δ_ν** (specifically: into the region where exactly one amplitude is negative). "Zero net flux ⟹ one antispin axis" is also asserted, not derived (why not core–medium cancellation, or zero axes?). Side-note worth carrying: if the inversion is literal antispin (BP&R: antiparticle sense), the neutral triple contains its own antiparticle component — a **Majorana-flavored** structure, testable via 0νββ.

**The π/12 datum [MEASURED IN-SESSION — the new sharp handle].** Extracting the Z₃ phases from data: charged leptons δ_l = −2.31662 rad (amplitude 1.41420 ≈ √2 ✓); signed-branch neutrinos δ_ν = −2.57777 rad. Difference:

    |δ_ν − δ_l| = 0.26114 rad;  π/12 = 0.26180;  ratio 0.9975 — **agreement to 0.25%**

(Brannen 2006's relation δ_ν = δ_l ± π/12, reproduced here from our own signed solution + oscillation data.) The charged→neutral transition shifts the Z₃ phase by **π/12 = 2π/24** — 2π divided by the *order* of the octahedral rotation group. **Robustness (computed):** propagating ±1σ oscillation-data errors (±2% on Δm²₂₁, ±1.5% on Δm²₃₁), the offset from exact π/12 spans [−0.0056, +0.0043] rad with central −0.00065 — **π/12 sits inside the 1σ band; the relation is exact within current data.** Σm_ν central: 58.59 meV.

**Gordon's "single structural click" derivation (cycle 6) — [REJECTED: group-theoretically false].** His mechanism: "the smallest invariant geometric step is one symmetry operation = 1/24 of a full rotation." But the 24 *elements* of O are not 24 evenly-spaced rotations: O's element angles are exactly {0°, 90°, 120°, 180°} (classes E, 6C₄, 8C₃, 6C₂+3C₂). **There is no 15° rotation in the octahedral group.** Group *order* ≠ rotation *step* — the derivation conflates |G| with the angle of its elements. Additionally the phase δ lives on the generation-space Z₃ circle, not in physical space; mapping a phase step to a spatial rotation requires the Identity-Postulate machinery, still itself unproven (category bridge crossed for free, again).

**What would earn Δδ = 2π/|O| [ADOPTION CONDITIONS — not yet met]:** the datum needs a mechanism in which 2π divides by the group ORDER naturally — e.g. a Berry/holonomy phase of 2π distributed over a closed path through all 24 group operations (order-denominators arise honestly in holonomy, cf. fractional statistics), or the binary octahedral group 2O (order 48) acting through its double cover. Plus at least **one additional independent prediction** from the same mechanism. Until then: [WAGER — datum exact within 1σ, mechanism absent]. Formal adoption as "the topological definition of the weak isospin transition" is **declined**; the lexicon does not canonize numerators it cannot derive. Note what remains unearned either way: δ_l ≈ 0.222 rad itself (the absolute phase) has no derivation in any sector.

**Gordon's 4π/48 holonomy rebuild (cycle 7) — [MECHANISM CANDIDATE: correctly typed, not yet computed].** Progress conceded: the rebuild lives in the right spaces — spinor phase 4π (BP&R-native), binary octahedral 2O with |2O| = 48 (the double cover, where a Dirac spinor actually transforms), and 4π/48 = π/12 ✓. No hallucinated rotation elements this time. What it still is not: a computation. "Berry phase = total phase volume / number of domains" divides a **1D rotation-angle period** (4π) by a **count of 3D fundamental domains** (48) — the quotient is numerically right but the middle steps are asserted: no closed path exhibited, no connection integrated, no proof the full orbit accumulates exactly 4π (why not 2π, or 0?). Required for [DERIVED]: exhibit the closed path C through the 48 domains of 2O in the μ-rotator's configuration space; compute the holonomy γ = ∮_C A·dl of the canonical SU(2) connection; show γ = 4π and per-domain step 4π/48. Note also: 2π/24 = 4π/48 — **the datum cannot distinguish the O-bookkeeping from the 2O-bookkeeping**; all discriminating power now rests on the independent prediction.

**The registered independent prediction — PMNS from 2O irreps [BAR SET, with numbers].** Gordon's registration: lepton mixing angles strictly derivable from the representation theory of 2O. The compiler sets the bar in advance: (i) the classic leading-order octahedral result (S₄ ≅ O → tribimaximal) gives sin²θ₁₂ = 1/3, sin²θ₂₃ = 1/2, **θ₁₃ = 0 — already excluded at many σ** (data: sin²θ₁₂ ≈ 0.307, sin²θ₂₃ ≈ 0.55, sin²θ₁₃ = 0.0220 ± 0.0007). So the 2O construction must beat tribimaximal: produce θ₁₃ ≈ 8.6° at leading order with **zero free parameters**, or declare its parameter count honestly before fitting. All three angles simultaneously; partial credit is not credit. This is now the single test that decides whether π/12 is structure or coincidence.

**Cycle 8 — the gauntlet fails at the character table [THEOREM: 2O cannot act spinorially on three generations].** Gordon's claimed mechanism ("θ₁₃ ≠ 0 is the strict consequence of the double-valued spin representations of 2O") is killed by representation theory, verified by explicit construction (exact ℤ[√2] quaternion arithmetic, in-session): ⟨s,t⟩ with s = (1+i)/√2, t = (1+i+j+k)/2 closes at **order 48** with **8 conjugacy classes** (sizes 1,1,6,6,6,8,8,12) ⟹ 8 irreps. Five are lifts of S₄ (dims 1,1,2,3,3; Σd² = 24). The three spinorial irreps satisfy Σd² = 48−24 = 24 with **no dim-1 possible** (−1 = [i,j] is a commutator — computed — so every 1-dim rep kills −1): unique solution **{2, 2, 4}**. Therefore **2O has no 3-dimensional spinorial irrep.** Three generations require a 3-dim representation; every 3-dim rep of 2O contains −1 in its kernel and **factors through S₄** — reproducing exactly the single-valued octahedral flavor structure, i.e. tribimaximal, i.e. **θ₁₃ = 0, excluded.** The double cover is invisible to generation space acting irreducibly.

Two independent faults: (a) *category error* — flavor symmetry acts on the generation index; spin-statistics constrains **Lorentz** representations, not flavor representations. "Leptons are fermions, so their flavor group needs double-valued reps" is a non sequitur: the generation label carries no spin-statistics obligation. (b) even granting it, the required 3-dim spinorial rep does not exist (above). Escape routes, with their price tags: assign generations reducibly as 2_s ⊕ 1 (spinorial doublet + singlet) — legitimate, but the assignment choice + relative couplings ARE parameters and must be declared as such; or break 2O differently in the two sectors — likewise parametric. **Consequence: the π/12 wager has lost its designated zero-parameter discriminator and must either post a new independent prediction or pay for its parameters openly.** The holonomy integral remains the mechanism's one live route to being earned.

**Cycle 9 — the holonomy integral: flat route KILLED, curved route REBUILT with two exact theorems and one named posit.**

*Kill (computed):* Gordon's steps as specified put the path on the quotient of SU(2) by 2O and expect topologically locked fractions. But quantized (path-shape-independent) holonomy on S³/2O comes from **flat** connections, whose U(1) holonomies are characters of π₁ = 2O, i.e. of its abelianization. Computed on the explicit 48-element group: **[2O, 2O] has order 24 (= 2T), so 2O^ab = Z₂** — flat holonomies take values only in **{0, π}. π/12 is impossible on the topological route.** Also named: "phase ∝ number of domains traversed" is volume logic applied to a line integral — ∮A·dl responds to enclosed *flux*, not traversed *volume* (the same species of category error as order-vs-angle).

*Rebuild (the well-posed version — answers "how do we parameterize A"):* the μ-rotator's slow variable is its **axis direction n̂ ∈ S²** (the fast variable is the 2ω spin about it). Adiabatic transport of the BP&R spinor as n̂ moves gives the **standard spin-½ Berry connection: the monopole of strength ½** (A = ½(1−cosθ)dφ, curvature uniform, total flux ½·4π = 2π — the ½ *is* the 4π spinor periodicity, BP&R-native). The capsid's O-symmetry tessellates this axis-sphere into fundamental domains. Two exact results (both computed):

1. **Gauss-Bonnet:** the Möbius (2,3,4) triangle — vertices at a C₄ axis (rail/charged), a C₃ axis (pore/neutral), a C₂ axis — has angles exactly (π/2, π/3, π/4) and spherical excess = **area = π/12 exactly** (verified to 10⁻⁹; 48 such O_h domains tile 4π ✓). *This is where Gordon's "4π/48" honestly lives: it is an area on the axis-sphere, not a phase on SU(2).*
2. **The phase:** spin-½ monopole holonomy around one **rotation-domain** (two mirror triangles, area 4π/24 = π/6): γ = ½ × π/6 = **π/12 exactly** — quantized *by symmetry* (uniform curvature × symmetry-fixed area), path-shape-independent within the domain class.

*The one remaining posit [NAMED — the whole mechanism now rests here]:* the charged↔neutral transition circuit must enclose **exactly one rotational fundamental domain** (area π/6). Registered as the next computation: build V(n̂), find the true critical structure and minimal circuits. **→ EXECUTED, cycle 10, below.**

**Cycle 10 — the landscape computed. Gordon's potential and circuit both fail; the true landscape delivers π/12 anyway, exactly, by symmetry alone.**

*Catch 1 — sign error:* Gordon's V = −αK₄ **+** βK₆ ("the β term cuts a well into the pore") does the opposite: K₆ has its maximum at C₃, so +β *raises* the pore. Computed: C₃ remains a MAXIMUM for every β (eigs −4 → −39 as β: 3 → 81). The metastable neutral well requires **V = −αK₄ − βK₆**, β/α above a threshold ∈ (3, 9).

*Catch 2 — his claimed Morse structure is impossible on a compact manifold:* 14 minima + 12 C₂-saddles + 0 maxima cannot exist (a smooth V on S² must attain a maximum; with M ≥ 1 the saddle count must exceed 12). Computed census (corrected V, β = 27, 600-start survey): **14 minima (6 C₄ + 8 C₃), 24 saddles ON the C₄–C₃ edges** (at (0.272, 0.272, 0.923)-type points, orbit 24), **12 maxima at C₂**. Morse check: 14 − 24 + 12 = 2 = χ(S²) ✓. **Consequence: nothing transits through C₂ — it is a peak, not a pass — so Gordon's circuit C₄→C₂→C₃→C₂′→C₄ is unphysical.** Each charged well connects to each adjacent neutral well by exactly ONE minimal path (over the edge-saddle): no two-saddle interference loop exists between a single pair.

*The rebuilt (and stronger) π/12 — exact by symmetry, no numerics needed once the topology is known:* the min-path network has V=14 wells, E=24 saddle-edges ⟹ **F = 12 faces**, one per C₂ maximum. O acts transitively on the 12 C₂ axes ⟹ the faces are congruent and tile the sphere: **face area = 4π/12 = π/3 exactly**, independent of α, β, and path shapes. Each face is mirror-symmetric through the great circle containing its two C₄ corners and its central C₂ ⟹ **half-face = π/6 exactly**. Therefore the gauge-invariant interference phase between the two physical routes from a charged well e to its neighbor e′ —

    route A: e → ν → e′   (through the neutral well: the weak-mediated path)
    route B: e → e′ direct over the C₂ ridge   (the charged path)

— is γ = ½ × (half-face area) = ½ × π/6 = **π/12 exactly.** Spinor charge (½, BP&R) × octahedral face symmetry (Gauss-Bonnet/tessellation) and nothing else: **no free parameters, no path-shape dependence, robust to all values of α, β in the metastable regime.** The phase is the flux separating "transition via the neutral state" from "no transition" — precisely the character of a weak-sector phase offset.

*Status:* **[DERIVED, conditional on two named premises]** — (i) the landscape regime (C₃ metastable, i.e. neutral states exist — empirically unobjectionable), and (ii) **the Bridge**: the geometric phase of the axis-circuit is the shift of the generation-space Z₃ phase δ. Note the consolidation: this Bridge and the Identity Postulate (Koide 2:1) are instances of ONE meta-assumption — *generation space inherits the rotator's geometry* — on which now hang TWO independent five-figure numbers (Q = 2/3 at −0.0009%; Δδ = π/12 at 0.25%). The program owes one axiom, and it pays out twice if earned.

*PMNS direction [BAR, not a build]:* the adjacency of the well network is suggestive — each neutral well borders exactly **3** charged wells (democratically, by C₃ symmetry); each charged well borders 4 neutral wells. A mixing matrix from this incidence + the π/12 phases is constructible — but it **fuses generation-3 with axis-3** (the flagged fusion; price: O-degeneracy of the three axes vs the observed mass ladder, resolvable only via the Koide deformation story, and it must survive the three-threes audit). Bar unchanged: sin²θ₁₃ = 0.0220 ± 0.0007 with parameters declared in advance, all three angles at once.

**Cycle 11 — boundary conditions for the 14×14 transition operator (all verified in-session). One no-go, one gauge rule, one sourcing rule, one demand.**

1. **Symmetry no-go [THEOREM]:** O acts **transitively** on the 24 saddle-edges (computed: single-edge orbit = 24). So at the symmetric level every edge amplitude is EQUAL — the operator has two constants total (well energy, one hopping) and its spectrum is organized by O-irreps. The 3-axis (generation) space decomposes as **A₁ ⊕ E exactly** (computed: ⟨χ,χ⟩ = 2): any O-invariant operator on it is a·P_{A₁} + b·P_E by Schur. Consequence: the democratic eigenvector is fixed and the E-doublet basis is **arbitrary** (degenerate) — **the symmetric network yields PMNS angles that are UNDEFINED, not predicted.** No amount of diagonalizing the symmetric 14×14 can produce θ₁₃. All mixing information must come from symmetry breaking.
2. **Gauge rule [Gordon's per-edge plan has a factor-2 bug]:** the π/12 is a **flux, not an edge phase**. Edge phases are gauge freedom; only plaquette products are physical. Correct assignment: **uniform plaquette flux π/6 per face** (½ × π/3). Consistency check that certifies the whole geometry: total flux = ½ × 4π = 2π = 12 faces × π/6 ✓ — the spin-½ monopole quantization is exactly saturated by the 12-face tessellation. Gordon's uniform e^{iπ/12} per edge gives 4 × π/12 = π/3 per plaquette — wrong by 2. Fix the gauge before diagonalizing.
3. **Sourcing rule:** the only symmetry-breaking inputs admitted are the two deformation phases the program already owns: **δ_l (measured, 0.222) and δ_ν = δ_l − π/12 (derived-conditional)**. PMNS must emerge as U(δ_l, δ_ν) with zero new parameters. Any per-edge structure not induced by these two phases is a free parameter and must be declared as such before fitting.
4. **The ± demand:** the 6 charged wells are 3 axes × (±). The construction must state what ± is (spin-up/down? particle/antiparticle? redundancy?) *before* projecting 6 → 3 — BP&R identify axis inversion with spin flip, which would fuse spin (Lorentz) into the same geometry as generation (flavor): a fourth fusion, to be priced, not smuggled.

**Cycle 12 — Gordon's U = exp(−i(J·n̂)π/12) EXECUTED. [FAILED — all-angles bar not met; selective preview named.]**

Gordon declared the super-fusion wager (± ≡ spin, accepted as [WAGER DECLARED]) and proposed PMNS = the 3D rotation by π/12 about the democratic axis, previewing only |U₁₃|² ("0.0258 or 0.0190, bracketing the data"). Computed, both signs, all three angles (data: 0.307±0.012, 0.55±0.02, 0.0220±0.0007):

    sign +: sin²θ₁₂ = 0.0196 (−24σ)   sin²θ₂₃ = 0.0196 (−27σ)   sin²θ₁₃ = 0.0259 (+5.5σ)
    sign −: sin²θ₁₂ = 0.0264 (−23σ)   sin²θ₂₃ = 0.0264 (−26σ)   sin²θ₁₃ = 0.0191 (−4.2σ)

His preview numbers were **correct and cherry-picked**: θ₁₃ misses on both signs (the bar was ±0.0007, and "bracketing" is not hitting), while θ₁₂ and θ₂₃ — whose measured values were on the board since cycle 8 — are off by **~25σ** and went unmentioned. The structural reason is elementary: a 15° rotation is near-identity, and near-identity matrices cannot produce 33° and 49° mixing. **A pure E-plane relative rotation by Δδ can never be the PMNS matrix.**

*What survives under the sourcing rule:* the two sector bases must differ **structurally**, not merely by the small phase — and the geometry offers exactly this: charged wells sit on **C₄ axes**, neutral wells on **C₃ body-diagonals**. The axis-adapted ↔ diagonal-adapted change of basis is intrinsically large-angle, with π/12 as the correction on top. Naive trimaximal F₃ for that map FAILS (computed: sin²θ₁₃ = 1/3, +445σ) — the basis map must be **derived**, not guessed: build the tight-binding well states from V(n̂), project the 8 C₃ ground states to generation space, with **all phases fixed by the π/6 plaquette flux**, zero free parameters, and report all three angles for both signs. **Registered as the next construction.** Marked coincidence, logged not claimed: sin²(π/12)/3 = 0.02233 (1.9σ from data). If the derived construction misses, the super-fusion wager dies as declared.

**Cycle 13 — the tight-binding construction EXECUTED. Result: an obstruction theorem. The super-fusion is DEAD, killed by the model's own flux. [SPECIMEN — kept per the never-destroy rule: a wager that died by the theory's own internal logic, teaching that generation-3 is not axis-3. Cycles 12–13 are the autopsy.]**

Built in full: the 6+8 well network, 24 unit-modulus hoppings, edge phases solved exactly so every plaquette carries flux π/6 mod 2π (the monopole's Dirac string routed through one face — the naive real-valued solve is inconsistent since 12×π/6 = 2π ≠ 0; verified all 12 fluxes ≡ π/6 after the string fix). Spectra of TT† and T†T, exact closed forms:

    charged:  {3−√3 (×4),  6+2√3 (×2)}                    (trace 24 ✓)
    neutral:  {0 (×2),  3−√3 (×4),  6+2√3 (×2)}           (trace 24 ✓;  √3 = 2cos(π/6) — the flux in the spectrum)

**The obstruction:** the flux-dressed multiplets have dimensions **{4, 2} and {2, 4, 2} — never 3, never 1.** With π/6 flux per plaquette, the wells transform under a *projective* (magnetic) representation of O — and projective reps of O are exactly the **spinorial irreps of 2O, dims {2, 2, 4}** (cycle 8's character table, now appearing *dynamically*). Inversion parity is broken by the flux (even-contents fractional, computed), so the ±-trace 6→3 projection does not commute with H: **no 3-dimensional generation multiplet exists anywhere in the flux-dressed spectrum. The 3×3 PMNS matrix cannot even be formed.** The failure is not "wrong angles" — it is "no object."

**The irony, stated for the record:** the π/6 monopole flux — the mechanism's crown jewel, the thing that derives π/12 — is precisely what forbids three generations from living on the spatial axes. Cycle 8 proved it statically (2O has no 3-dim spinorial irrep); cycle 13 proves it dynamically (the flux imposes spinorial multiplets on the wells). Same fact, two faces. **The super-fusion (generations ≡ spatial axes) is dead as declared, and the three-threes flag was correct from the day it was raised: generation-3 is NOT axis-3.** What survives, untouched because it never depended on the fusion: the π/12 derivation (Bridge-conditional), the Koide conditional theorem, Σm_ν = 58.6 meV, and the observation that generation space is an abstract Z₃ whose geometric home is still unidentified. PMNS is, honestly, outside the current machinery. The program keeps its two five-figure numbers and owes its one axiom.

**Cycle 14 (arc close) — Gordon's final question, registered with entrance requirements.** Proposal: *the Z₃ generation space is the geometric phase between the 2ω core and the ω medium of the μ-rotator.* Registered as [CANDIDATE — the right kind of question: internal to the twist, not spatial]. Entrance requirements before any building: (1) a core–medium relative phase is a U(1) circle — the proposal must derive **why exactly three** stable lockings (note the tension to beat: a 2ω:ω = 2:1 internal resonance naturally yields **Z₂**, not Z₃ — where does 3 come from? The quaternion triple {i,j,k} wager is the standing candidate and would unify this with the N=3 question); (2) it must reproduce the **√2 amplitude** (the 45° lock) from the same mechanism, not import it; (3) it must locate δ_l ≈ 0.222 (the absolute phase) or declare it initial-condition. Any proposal meeting (1)–(3) would BE the Bridge — earning the axiom pays out Q = 2/3 and Δδ = π/12 simultaneously. This is the program's single open front.

## 5. Quarks: structural exemption [pointer]

Quarks fail Koide because there are no quark μ-rotators — "quark masses" are parameters of collective rail modes (see `quark-theory-v2.md` §4). m = ℏω/c² applies only to free rotators: charged leptons + (signed-branch) neutrinos. This supersedes the dynamical flux-tube exemption.

## 6. Why three generations [OPEN + WAGER]

Z₃ cannot answer it (circular: the 3-space was built from the observed three). LEP: N_ν = 2.9840 ± 0.0082 — no 4th light active ν. Wager on file: ℍ has exactly three imaginary units {i, j, k} — three orthogonal twist axes of SU(2), no fourth; if generations = deformation axes, N = 3 is algebra. Owed: the map {i,j,k} (orthogonal) → Z₃ phases (120°, planar), and its welding to the lexicon's i-identity flag. Distinct from color-3 and from the R-prefactor-3 (see quark-theory-v2 §3) — three threes, no silent fusion.

## 7. Falsifier table

| test | prediction | dies if |
|---|---|---|
| Σm_ν (CMB-S4/DESI) | ≈ 58.6 meV, NH | measured far from ~59 meV |
| hierarchy | normal (signed branch unique in NH) | inverted confirmed |
| Identity Postulate | one inverted mode for ν triple, none for charged | mapping can't produce the asymmetry |
| Koide scale √M ≈ 314 MeV | should emerge from μ dynamics | remains numerological |
| 4th generation | forbidden (quaternion wager) | 4th lepton found (LEP already ~excludes light) |
