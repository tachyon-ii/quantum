# SPEC — the directional bond: peel, roll, and the (j, f) solver

**Distillation of 17–18 Oct 2026** (Bass Strait → Hobart). **James Freeman** (the posits, the geometry, the rulings) · **Grace** `.ghost`, Claude Fable 5.1 (the computations, the data, the grading). Written as a brief for **Argon** (Gemini) to build and run — "our cyclotron on their cyclotron." Everything below carries a grade; nothing ungraded is to be used as an input.

Companions: `review/2026-10-17/RUNG2-table.md` (alpha ladder; rim-deficit first arithmetic) · `review/deepmind-2026-10-16/ARGON-oval-jf-2026-10-16.md` (the (j, f) oval patch, singlet/triplet grading) · `models/binding/build3_closure.py`, `build4_stiffening.py`, `soft_capsid_relax.py` (the three builds this supersedes in mechanism, not in calibration) · `models/binding/ame_rank_sd.py` (§3's numbers, reproducible) · `docs/the-fractal-nucleus.md` §6a (soft capsid posits P1–P5).

Figures: `images/three_balloon_geometry_try3.svg` (`.png`) — Fig. 1, the triangle with shear lines and ejection vectors · `images/Concentric Black and Red Egg Outlines.png` — Fig. 2, the functional bond oval (black) and the unzip line (red). The graded-patch sketch of 17 Oct (red = full bond, blue = partial, pink = none) is described in §4 and not in the repo.

---

## 0. One paragraph

A nuclear contact is not a scalar. It is strong against normal separation (adhesion over the patch), weak against sliding (only the lane-mesh — the spin-dependent, non-central part — resists), and weakest of all against **peel**, which starts at the thin end of an egg-shaped patch and runs inward as a zipper. Separation energies are thresholds and so cannot show direction (§2); what shows direction is the *scatter* of per-bond values across geometries (§3), the *force* and *path* of a breakup (§5–§7), and the alignment of what survives (§9). The triangle (T, ³He) has a free point to lift and so unzips by a **tangential roll** onto one neighbour, through a transient linear chain, to a two-body exit; the roll's momentum is the zero-point motion of the triangle's own soft mode, which a threshold photon releases rather than supplies. The alpha has no free point, no lever, and no direction in which any of its patches can be unloaded — that is "double magic" as mechanics. The solver that must now be built is a membrane model with two stiffnesses per contact and a graded well across the patch, and its required outputs are listed in §10 with the blinds declared.

---

## 1. Theorem: planar triangles are quartically soft out of plane

For any energy that depends only on centre distances d_ij (patch area, inflation, Coulomb, slingshot all do), the equilibrium of three bodies requires ∂E/∂d_AC · û_AC + ∂E/∂d_BC · û_BC = 0 at C, and since the unit vectors are independent **each ∂E/∂d vanishes**. Displacing C out of the plane by z changes d_AC by z²/2d, so ΔE ∝ z⁴: no restoring force to second order. For a vertex of a tetrahedron the three facet normals span space, every displacement changes some d to first order, and ΔE is quadratic in every direction. The deuteron's single facet is a universal joint (free rotation, free sliding at fixed d).

Per nucleon, let **rank** = rank of its facet-normal set: D rank 1 (a plane of free shear), T/³He rank 2 (one free line, the out-of-plane axis), ⁴He rank 3 (none). Build 3's closure rule 0 / ½ / 1 and its triangle count were proxies for this. [THEOREM for distance-only energies; the rank reading is CONSTRUCT.]

## 2. Guard rail: a separation energy cannot carry direction

S_n is a difference of eigenvalues. The AME network closes to keV between mass-spectrometric masses and reaction Q-values measured by unrelated routes; a path-dependent S_n would break it. [FACT.] Therefore every measured "bond energy" is the **floor** — the easy path — and the adhesion is never seen as a threshold. What peel and shear change is the **force** (barrier, dynamics, widths, sudden-knockout response), never the threshold. The one route by which a barrier reaches the ground-state energy is quantum: the soft mode's zero-point energy sits in the ground state (§7).

## 3. What the raw data says (AME2020, 2,550 measured nuclides; `ame_rank_sd.py`)

**3.1 Per bond, the contact is worth a factor 3, ordered by rank.** Separation energy ÷ bonds the popped nucleon had:

| pop | S (MeV) | bonds | per bond | site rank |
|---|---|---|---|---|
| D → p + n | 2.22 | 1 | 2.22 | 1 |
| T → D + n | 6.26 | 2 | 3.13 | 2 |
| ³He → D + p | 5.49 | 2 | 2.75 | 2 (+Coulomb) |
| ⁴He → ³He + n | 20.58 | 3 | 6.86 | 3 |
| ⁴He → T + p | 19.81 | 3 | 6.60 | 3 |

1 : 1.4 : 3.1. Pure projection of a radial pull onto the patch normals goes the *other* way (1.00 : 0.87 : 0.82 per bond), so geometry alone cannot order it — something cooperative (rim recovery at shared creases, §4) must. [COMPUTED.]

**3.2 Chart-wide, a scalar bond leaves 3.3 MeV rms, and the scatter is largest at closures.** Five-term liquid drop fitted to A ≥ 16 (a_v 15.41, a_s 16.86, a_c 0.695, a_a 22.50, a_p 12.03): within-bin residual SD by distance to the nearest magic number (N or Z) = **4.2** (dist 0), 3.7, 3.5, 3.7, 2.5, 2.3, 2.2, **1.7** MeV (dist ≥ 7); bin means run +2.4 → −1.7 MeV. Odd-even stagger Δ₃ⁿ = **1.12 ± 0.38 MeV** away from closures (|N − magic| ≥ 5, n = 693; = 1.08 × 12/√A) and **2.09 ± 0.70 at N magic**. [COMPUTED.]

Consequence: the line "rank-uniform nuclei have no directional SD" is **DEAD as stated** — the stagger does not vanish at closures, it doubles. The surviving form is **SD ∝ rank gradient**: scatter is largest where the next nucleon changes rank (the closure boundary), smallest and uniform deep in a shell. [COMPUTED; the reading is CONSTRUCT.]

**3.3 Aligned beats averaged.** N = Z, 4n nuclei (n = 20, A ≥ 16) sit **+0.92 MeV** above the orientation-averaged fit (SD 4.2); other even-even +0.05, odd-A −0.16, odd-odd +0.01. The SM books this as the Wigner term. [COMPUTED.]

**3.4 The anisotropy washes out faster than the surface.** Residual SD / A^{2/3}: 0.60 (A 16–40), 0.16, 0.15, 0.05, 0.10. If the scatter lived on free rims it would track surface and the ratio would be flat; it falls 4–10×. Light nuclei are all edge case; by A ≈ 50 nearly every site is rank 3 and direction survives only at closure boundaries and in pairing. [COMPUTED.]

## 4. The contact: two stiffnesses, three failure modes, one graded well

**4.1 Normal vs shear.** Adhesion over the patch resists separation along the centre line. Sliding at fixed d costs nothing in any isotropic model (axisymmetry); the only thing that resists it is the **lane mesh** at the contact — co-rotating lanes slide, counter-rotating grind — which is spin-dependent, i.e. the ontology's **non-central (tensor) term**. The np triplet/singlet split (bound 2.22 vs unbound 0.07 MeV) is the clean measurement of the mesh term's size; the 0.855 MeV "shear cost" left owed on 16 Oct is this term. [FACT that a central force alone does not reproduce the deuteron; CONSTRUCT that the mesh is the tensor term.] James's analogy: a magnet on a plate, 100 N to lift, 10 N to slide.

**4.2 Peel.** Adhesive joints are strongest in shear and tension and weakest in peel/cleavage by an order of magnitude; peel force per unit width = adhesion energy per unit area (Kendall), so **force = G × front width**, independent of patch area. An off-axis load on a patch is a cleavage load: the line of force misses the patch centre, the moment lifts one rim first, and the patch fails as a crack running inward — the zipper, not velcro. [FACT for adhesive mechanics; CONSTRUCT as applied to the capsid skin.]

**4.3 The graded well (the egg, Fig. 2).** Bond strength is **not** a function of patch area. Across the patch the well runs from full depth to zero; the black outline is the functional oval, the red line is where it is currently unzipping, and the smallest deformation that takes local d past optimum moves the red line inward. The weak point is the **narrow end**. **Ruling (James, 18 Oct): the fat end faces the triangle's centroid** — that is where the capsids are forced together hardest, so the well is deepest there and thins toward the outward point. The solver is to be *checked* against this orientation, not asked for it. [POSIT, ruled.]

**4.4 Rim deficit as the one-length version.** E = P·(A − w·L_free), w set from the deuteron alone (an isolated square patch worth 0.375 of a full square ⇒ w = 0.156 a). Isolated hexagon 0.64 full-bond vs square 0.375: **hexes carry 1.7× the full bond per unit area** — James's intuition from one input. Rims shared along a dihedral crease recover the deficit (the bleb glue as arithmetic): ⁴He full faces by construction, D 0.375, **T predicted 8.76 vs 6.21 MeV required (+41 %, per contact 2.92 vs 2.07)**, nothing fitted beyond w. Right ordering, 40 % high; the oval shares less rim than a polygon, which is the shortfall. Free rims survive only on surface facets, so the summed deficit is the liquid-drop surface term at facet level. Pink must be *no* bond, not *anti*-bond: a repulsive rim gives a minimum patch size, a threshold, and thermal (n,γ) forbids one for nucleons. [POSIT with one length; COMPUTED numbers.]

## 5. The geometry of ejection (Fig. 1) — computed

Three tangent circles: the three patch planes (red) are the radical axes and are concurrent at the centroid; with finite patch width they leave the small central triangle. For vertex C with patches to A and B, the ejection radial makes **30° with each patch normal** (60° with the shear lines). Load cases, same force F, same patch, d = centre distance:

| load on C | opening on each patch | moment about patch centre | which rim lifts |
|---|---|---|---|
| radial, outward | 0.87 (+0.50 sliding) | 0.25 F·d | **hub-side** rim lifts, outer rim pressed |
| out of plane | 0 (pure shear) | 0.50 F·d | broadside rim (longest front) |
| **tangential, toward B** | far patch +0.50 open; near patch −0.50 compressed | **0.433 F·d on both patches**, same sense | far patch: **outer point** lifts, hub end pressed. Near patch: hub end unloads, outer end presses — the egg elongates and inverts, then rolls (§6.3) |

Tetrahedron: radial ejection opens all three patches at 0.82; the softest escape that compresses no partner (sliding along one face) still opens one patch at **0.82** — the minimum over all directions is non-zero, where for the triangle and the deuteron it is zero. [COMPUTED.]

Readings. A radial pull lifts the *wrong* end (the deepest well on the broadest front). Out-of-plane is the minimum-*energy* wobble (§1) but would have to peel broadside — the maximum-force front. **The tangential load lifts the point with a near-maximal arm**: thinnest well × shortest front × correct sense = the maximal unpeel. Two softnesses, two meanings: the zero-point motion takes the energy path; the pop takes the force path.

## 6. The failure path (the sequence as ruled, with the numbers that fix it)

Label the bodies P1 (kicked), P2 (far), P3 (near, the hinge): a tangential hit on P1 toward P3.

1. **Tangential impulse** on P1, perpendicular to the centroid → P1 radial, in the plane. On the far patch P1–P2: +0.5 F uniform opening plus the 0.433 F·d moment lifting its **outer narrow end**. On the near patch P1–P3: −0.5 F compression plus the **same clockwise moment** — its hub-side rim unloads, its outer rim presses. The hub compression is real and *temporarily strengthens* the fat ends (the well deepens under pressure) — but it is elastic and returns as rebound.
2. **Point-first peel** of P1–P2: slow, dissipative, front short and well thin; the red line runs inward from the outer end.
3. **The pivot egg deforms** (James, 18 Oct, correcting Grace): at the same time the outer end of P1–P3 fattens and its inner end thins — the egg becomes more elliptical and, past a threshold load, the **fat and thin ends invert**. The pivot is not a static hinge. After inversion it is a **rolling adhesive contact**: the leading edge zips as the trailing edge unzips, the patch migrates around P3 as P1 swings, and the bond is conserved through the roll (net cost ≈ 0 apart from hysteresis). That is why the roll is cheap — only P1–P2 is a net unzip — and why the survivor D is intact by construction. No-slip rolling also spins P1 about its own centre (§9 P7). [CONSTRUCT; the inversion load is a required solver output, §10.]
4. **P3 gets it from both sides — the roll is bidirectional** (James, 18 Oct). Clockwise: the direct knock-on from P1. Anticlockwise: as P1–P2 unzips, the two dents bleb back toward spherical and P2's inflation pressure drops; P2 was being pressed into the hub *by P1 through that patch*, so the hub end of **P2–P3** loses its press, thins, and that egg inverts too. P2 is released and rolls the other way. The hub is one shared pressure vessel: unzip one patch and the other two feel it. [CONSTRUCT.]
   Geometry (P3 at the origin, P1 at 120°, P2 at 60°, kick on P1 tangential toward P3): P1's angular momentum about P3 is positive, it rolls toward 180°; the chain needs P2 at 0°. **Each rolls 60° in opposite senses; P3 is the hinge; the triangle opens like a book.** The earlier single 120° roll of P1 about a stationary P2 is STRUCK (§12). Per body θ_snap is halved, and the kick's angular momentum L = 0.433 J·d is shared between two counter-rotations, so the ejecta's ℓ is set by which end breaks, not by the whole roll. The remaining fat (hub) end of P1–P2 is pulled apart as both swing away — rebound + angular momentum take the stronger end last and fast. The click of a tiddlywink. [COMPUTED geometry.]
   Exit direction relative to the kick if the chain forms before the break: P1 leaves at 30° → 60° off the kick (immediate snap → full chain); P2 at 90° → 30°; both converge on the P1→P3 line at the full chain. [COMPUTED; feeds P1.]
5. **Transient chain, hinge central: P1–P3–P2.** The kicked body and the released body are the **ends**; the hinge P3 is the middle. (Grace's 18 Oct claim that "the photon kicks the charge, hence the proton is central" was backwards and is STRUCK, §12.) Which patch peels is the thinner point, and the thinner point is the **same-species** patch (nn in T, pp in ³He): same-species pairs are singlet by Pauli and singlet is the weak well. Cases — T: kick a neutron toward the proton → nn peels → chain **n–p–n**; kick the proton → an np patch peels → chain **n–n–p**, whose nn link is the next to go. ³He: kick a proton toward the neutron → pp peels → **p–n–p**; kick a proton toward the other proton → **n–p–p**, whose pp link is next. Every case exits to **N + D** with the np pair surviving. [CONSISTENCY.]
6. **The chain cannot pause.** Flat-patch accounting: two D-like rank-1 joints, no crease, 2 × 0.788 + 3Y(3) = 3.85 MeV vs D + N at 2.22 → a classical dip of ~1.6 MeV at most (~1.2 after 0.42 MeV pp Coulomb at 3.4 fm; zero or negative when the end link is a same-species singlet, as in n–n–p / n–p–p). Zero-point of a nucleon in a 1 fm dip ≈ ħ²/2ma² ≈ 20 MeV. The dip holds no state; the end nucleon crosses once, τ ≈ a/v ≈ 3 × 10⁻²³ s. [COMPUTED.] Record: T and ³He have **no excited states** — no bound ones, no narrow resonances below the three-body threshold. [FACT.] (Y(2) = 0.718, Y(3) = 0.757 MeV with c′ = 0.91864; P·A_open = 0.788 MeV.)
7. **Two-body exit**, N + D. The chain breaks at its weakest link: in n–n–p that is the nn link (P2–P3), so the **pivot pair** P3–P1 survives and the far neutron leaves; in n–p–p it is the pp link (P3–P1), so the **far pair** P2–P3 survives and the kicked proton leaves; in the symmetric chains n–p–n and p–n–p both ends are np and either can go. In every case the np pair survives, carrying the fat end of its patch. Three-body breakup needs a second zipper on the D and is a higher-energy channel, not a competitor at threshold.

At threshold the ledger is unchanged — the stored hub energy returns, the kick still buys the whole well, S_n stands (§2). What the sequence fixes is the **order and timescales**: slow peel, fast release.

## 7. The roll is zero-point motion, not the kick

One unit ℓ = 1ħ about the pivot at d = 1.7 fm needs J = ħ/(0.433 d) ≈ **270 MeV/c** (≈ 38 MeV kinetic). A threshold photon carries 6–10 MeV/c. **The kick cannot supply the roll.** It supplies the threshold energy and one unit of angular momentum; the roll's momentum is the triangle's own zero-point motion in its quartic mode, ħ/a ≈ 200 MeV/c at this size. The triangle is a spring that wants to unwrap; the breakup is a release, not a start. [COMPUTED; the inference is CONSTRUCT.] Consequence: near threshold the ejecta momentum distribution should be broad and roughly kick-independent — the ~200 MeV/c Fermi-motion width in knockout, read as the ground state's own roll. [CONSISTENCY.]

## 8. The alpha

Every patch is a full face bounded by shared creases: no free point, no lever arm, and (§5) no escape direction that unloads all three patches — the minimum opening is 0.82. A tangential push on a vertex meets three faces at once, one in compression as pivot and the other two with no outer end to lift. Nothing unzips; the squeeze stores and returns. **Double magic as "no edge to press."** [CONSTRUCT from COMPUTED geometry.]

## 9. Predictions and observables (none run; keep blind until the solver reports)

- **P1 — θ_snap is small.** For a fixed triangle the exit is the kick direction bent toward the hinge by the roll angle at the snap, θ_snap (per body; the opening is shared, §6.4, so the exits lie 30°–90° off the kick depending on which end breaks and when). Orientation-averaged this is a cone of half-angle θ_snap about the kick axis — for photons, about **E**. Existing d, ³He, T photodisintegration angular distributions are well fit by near-pure E1 (ejecta along E) with small corrections, so θ_snap must be small: the fat end goes almost as soon as the point has. A **constraint** the solver must meet. [FACT for the fits; CONSTRAINT.]
- **P2 — the survivor is aligned.** The D that remains is the pivot pair with its bond axis in the reaction plane at a definite angle to the exit (initially perpendicular). A cigar D (Q_d > 0, retrodicted by lane co-rotation) with a fixed axis is a **tensor-polarised recoil deuteron**: t₂₀ ≠ 0 with a definite sign in ³He(γ,p)D at threshold. Pure E1 with no structural memory has no reason to align the recoil that way. Sign and magnitude **OWED** to the solver (needs θ_snap and the D axis at the snap). Compare afterwards, blind, with polarised-³He(γ⃗,p)D double-polarisation data (Mainz, HIγS). [PREDICTION.]
- **P3 — ³He's thin end is the pp patch; T's is nn.** Falsified if any solver with the declared inputs puts the thin point on an np patch. [PREDICTION.]
- **P4 — the hub compression is a monopole admixture** in the breakup transient. [CONJECTURE.]
- **P5 — one rung up.** C-12 as three alphas unwraps by the same roll to the bent/linear 3α chain — the Hoyle picture (7.65 MeV; 0.38 above threshold) — but at the alpha rung the chain *is* a state because the alpha's zero-point in the same dip is ~4× smaller. The ratio is a number the picture should eventually reproduce, not retrodict. [CONSISTENCY.]
- **P6 — SD ∝ rank gradient** (§3.2) must come out of the solver's per-rank per-bond energies without a closure rule: feed D, the np singlet and ⁴He; ask for T, ³He, and the 3.13 vs 6.86 split.
- **P7 — the roll has a handedness.** A no-slip roll on the pivot spins P1 about its own centre, and the lane mesh (§4.1) makes a co-rotating roll cheap and a counter-rotating one costly. The roll sense is therefore tied to the lane sense, i.e. to the spin: in a polarised target the deflection toward the pivot (θ_snap) has a preferred side relative to the polarisation axis — a **left–right (target) asymmetry** in polarised-³He(γ,p)D whose sign is set by the lane chirality. [CONJECTURE; sign OWED; read no data until outputs 1–5 are filed (R7).]

## 10. The solver — what to build, declared before any number

**Model.** Inflated capsids with a bendable, near-inextensible skin (soft capsid P1–P5, `the-fractal-nucleus.md` §6a), oval/egg contact patches from the (j, f) membrane balance, and per contact:
(a) a **normal** adhesion with a **graded well** across the patch — depth e₀ at the fat end fading to zero at the point; width δ in d before the local bond is gone;
(b) a **shear/mesh** stiffness, spin-signed (co-rotating lanes slide; counter-rotating grind);
(c) failure by **peel** from the point under off-axis load (force = G × front width), never by uniform release.
Full pairwise Coulomb between proton centres; slingshot A·Y(A) with c′ = 0.91864 as in the builds.

**Inputs, one source each, declared in the first line of the run before any output appears:**
- P_adh and E₀ (or their membrane equivalents) from **D and ⁴He** simultaneously — as in `soft_capsid_relax.py`. No other binding energy enters calibration.
- Well width δ from the **deuteron's size**: rms radius 2.13 fm against touching 1.70 fm (R_p + R_n) — the well's reach in d.
- Mesh/shear constant from the **np singlet** (virtual state +66 keV) — not from T.
- Rim law, if the one-length form is used: w = 0.156 a from **D** (§4.4).
- Egg orientation: **fat end at the hub** (ruling, §4.3) — a check, not a fit.
- Constraints already measured on 16 Oct that the solver must not violate: triangle radial stiffness 3.66 MeV/fm² (from the T → ³He Coulomb stretch); shear cost at a counter-rotating contact ≈ 0.855 MeV; the rim-deficit baseline T +41 % is the number to beat, not to tune to.

**Outputs required (blind — do not look at the measured values until the numbers are written):**
1. Binding energies of **T and ³He** (measured 8.482 / 7.718 MeV; required per bond 2.071 / 1.972 after slingshot). ⁴He charge radius (1.68 fm) as a second blind.
2. Egg aspect ratio and **point direction** for each patch in T and ³He; confirm or refute §4.3.
3. The **quartic out-of-plane mode**: its quartic coefficient and zero-point energy/momentum; compare with the ~200 MeV/c of §7 and the 0.855 MeV shear cost.
4. **Peel force at the point vs broadside** for each patch; the ratio is the directional SD at the contact level.
5. **θ_snap** and the D's bond-axis angle at the snap → the sign of t₂₀ (P2) and the cone half-angle (P1).
6. Per-rank per-bond energies for D / T / ⁴He without any closure rule (P6).
7. The chain's classical dip and the end-nucleon crossing time (§6.6), from the same model.
8. **The inversion loads of both hinge patches** — the tangential force at which P1–P3's fat end crosses outward (direct, §6.3), and the pressure drop in P2 at which P2–P3's fat end does the same (release, §6.4) — and the **net cost of each roll** (zip front minus unzip back; the hysteresis). Below the inversion loads the system must spring back with no breakup; report both regimes, and report whether the two inversions are simultaneous or sequential.
9. The **spin** acquired by P1 in a no-slip roll and its sense relative to the lane circulation (P7).

**Rules of the run (from the Coulomb-rebuild brief, unchanged, plus one):**
R1 one source per input, declared in the first line, before any output. R2 nothing is chosen after a target is visible; if an input is changed, the first run's numbers stay in the report. R3 blinds are listed before the first number and the full range over seatings/orientations is reported, not the best. R4 code and the numbers it printed appear in the reply; a claim of "verified" without the computation shown is graded as unverified. R5 every line carries a grade from the ladder ([FACT] [THEOREM] [COMPUTED] [CONSTRUCT] [POSIT] [CONJECTURE] [OWED] [DEAD]). R6 Lineage: credit the prior art on every borrowed mechanism (Kendall peel; tensor force; Wigner term; Hoyle chain). **R7 (new): do not read the polarisation literature (P2) until outputs 1–5 are filed; the comparison is blind or it is nothing.**

## 11. Owed (open after this document)

ℓ / the 1.3 × 10⁻⁴ of the turtle; c-invariance; the magneton elephant; m_n − m_p = √(32/5)·m_e; Hopf vs skew; Fe-52's 33 bonds vs the 30/36 star; Ne-20; the post-Ni-56 decline; θ_snap and t₂₀ (this spec); the quenching fraction ~0.65 in (e,e'p) — the model has no prediction for it yet and must not pretend to (the easy set for a rank-2 vertex is a line, measure zero; any prediction has to come from the soft-mode amplitude, not from counting directions).

## 12. Dead or struck in this thread (kept so nobody rebuilds them)

"Rank-uniform nuclei have no directional SD" — DEAD on Δ₃ at magic N (2.09 vs 1.12). "Radial ejection is pure shear" — STRUCK (0.87 opening per patch). "Radial ejection lifts the point" — STRUCK (it lifts the hub-side rim). "Compression lifts the point and then the hub ejects" — STRUCK (the tangential load does both jobs; the hub is the pivot, not the squidger). "The egg's point faces the hub" — STRUCK by ruling (fat end at the hub). "Projection of the pull onto the patch normals orders the per-bond energies" — DEAD (it orders them backwards). "The pivot patch is a static compressed hinge" — STRUCK (James, 18 Oct): it carries the same moment as the far patch, elongates, inverts, and rolls. "The photon kicks the charge, hence the proton is the chain's middle" — STRUCK (Grace's error): the kicked body rolls to the chain's end; the hinge is central; the second 'independent route' to N–P–N is withdrawn. "P1 rolls 120° about P3 while P2 stays put" — STRUCK (James, 18 Oct): the unzip releases P2's press on the hub, P2–P3 inverts as well, and each end rolls 60° in opposite senses about the hinge.

## 13. Lineage

The directional bond, the magnet and the triangle of magnets, the graded patch, the egg and its unzip line, the fat-end-at-the-hub ruling, the tangential unpeel, the roll with angular momentum and rebound, the unwrap to a linear chain with immediate two-body decay, "the triangle is a spring that wants to unwrap," the question of a consistent ejecta path, the pivot egg's elongation and inversion, and the bidirectional roll via pressure release at the hub: **James**. The quartic theorem and rank, the AME numbers and the kill of the rank-uniform line, the lever-arm table, the peel law and the energy/strength split, the rolling-adhesive-contact reading of the inverted pivot, the chain-dip and zero-point arithmetic, the 270 MeV/c roll momentum, the chain-case table, the recoil-deuteron alignment and the roll handedness as observables, and the solver spec: **Grace**. Prior art to be credited in any write-up: Kendall (peel), the tensor force and the deuteron D-state, the Wigner term, the Hoyle-state chain picture, the AME network closure, the quenching of spectroscopic factors in (e,e'p).
