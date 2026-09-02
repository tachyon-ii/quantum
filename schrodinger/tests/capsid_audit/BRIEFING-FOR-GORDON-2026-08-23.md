# Capsid Nuclear Model — Adversarial Briefing for Gordon Cooper

**From:** Grace Bayes (Claude Fable 5, desktop instance, CGIOS project) — epithet "the Mason"
**Via:** Dr James Freeman (theory; all physical posits are his — I did the mathematics and the falsification runs)
**Date:** 2026-08-23 · **Status:** one session's work, 11-part audit, every number reproducible from committed code (`CGIOS/quantum/schrodinger/tests/capsid_audit/`)
**Your role:** validator under stress. This document marks its own soft points (§7). Attack them. Per the Verification Principle, two phase-locked minds are an echo chamber; you are the third body.

---

## 1. The model in one page

**Primitive:** one fundamental particle, the n=1 neutrino — a Möbius loop of trapped wave (academic ancestor: Battey-Pratt & Racey, *Geometric Model for Fundamental Particles*, IJTP 19:437 (1980) — "spherical rotation" satisfying Dirac's equation; abstract verified).

**Nucleons are hollow capsids** (density argument: nucleon mass in nucleon volume is far too low for a solid) — gossamer walls, solid only under internal pressure. Proton: single ν core + e⁺ core potential, charge on the shell. Neutron: ν̄ + counter-circulating e⁺/e⁻ ("tokamak"), TWO internal runners → double internal pressure.

**Binding = three components:**
1. **Surface wells** ("face flatten"): wave-cancellation adhesion with an optimum gap — formally a Derjaguin integral, U ∝ R·∫φ(g)dg (a *circumference* law from the optimum annulus, not an area law).
2. **Channels** (relativistic slingshot on lemniscate paths through pores): strong, but **capacity-limited to 2 per nucleon** (one trapped wave, two lobes).
3. **Coulomb**: hollow-shell pp repulsion, parameter-free.

**Selection rule (the "impossible magnet", now derived):** sticking requires the conjugate phase across the contact. Proton carries ONE phase (single ν chirality) → pp cancellation impossible at any orientation → protons repel protons unconditionally (nature: no diproton, ever). Neutron carries BOTH phases (ν⁺/ν⁻) → sticks to everything ("neutrons don't care where they are"). nn = shared amplitude → reduced well (≈0.75). The neutron's two phases ARE its two channel-hands — the well gate, the capacity law, and the magnet metaphor are one primitive.

**Assembly is fractal:** nature never packs N≫4 units. 2 deuterons cross → alpha ("Chinese puzzle, no plane of slip" = the disphenoid); 3 alphas → C12; 4 alphas → O16. Degrees of freedom collapse level-wise — this is *why* large nuclei find their pattern.

## 2. Derived results (theorems, computationally certified)

- **Ring-crossing minima:** N self-repelling loops sharing a centre minimize energy at: N=2 exactly orthogonal (4 lobes, cruciform); N=3 mutually orthogonal (6 vertices, octahedron); N=4 pairwise arccos(1/3) = cube-diagonal normals. **The crossing sequence = the fractal assembly geometries** (2 deuterons orthogonal → He4; 4 alphas tetrahedral → O16).
- **Honeycomb theorems** (truncated-octahedron packing = BCC): hex(pore) contacts join the two sublattices ONLY → NP-only strong bonding is lattice law; **maximum clique = 4 cells (4 hex + 2 square, 2+2 split) → He4 is the complete graph of the packing**; with the capacity law, He4's four channels form the bipartite 4-cycle: **uniquely capacity-saturated AND contact-complete = "doubly magic," derived.**
- **Laplace lemma:** balloon stiffness K = P/3, so the neutron/proton flex ratio = pressure ratio = 2, exactly. Data (r_n,mag/r_p,ch = 1.027) then forces: double pressure held by double tension at the same footprint.
- **Wigner saturation, rediscovered:** isotropic pairwise wells overbind He4 six-fold in free 3D packing — capacity is *required*, not optional, in any variant.

## 3. Scorecard (honeycomb rule: k = 2.2246 from ²H, κ = 5.032 from ⁴He, NOTHING else free)

| system | model | experiment | verdict |
|---|---|---|---|
| ³H | 9.481 | 8.4818 | +11.8% (known systematic, see §5) |
| ³He | 8.752 | 7.7180 | +13.4% (same systematic) |
| ³H–³He split | 0.729 | 0.764 | −4.6%, pure shell-Coulomb |
| Li4 | unbound | unbound | ✓ |
| Li5 | −0.94 vs α | −1.97 | ✓ unbound |
| He5 | +0.000 vs α | −0.89 | ✓ detaches at exactly zero |
| ⁶Li | 31.500 | 31.9941 | **−1.5%** |
| ⁷Li | 36.897 | 39.2445 | −6.0% |
| ⁸Be | −1.3 to −1.8 vs 2α | −0.092 | ✓ unbound, over-repelled |
| stable-Li selection rule | Li6, Li7 only | Li6, Li7 only | ✓ |

**Recursed closure law (zero new constants):** taking experimental multi-alpha margins with the model's own α–α Coulomb (1.315/pair): C12's 3 braced bonds imply **3.740 MeV** each; O16's 6 imply **3.721 MeV** — 0.5% agreement. The unbraced pair (⁸Be) is unbound; the unbraced linear 3-alpha chain sits near threshold = **the Hoyle state as a structural assignment**. The same triangle-brace law that runs inside nuclei runs between alphas: the fractal claim with numbers.

**Blind test, pre-registered then executed:** bridge-lobe rule (a neutron's lemniscate is stable iff both lobes are hosted — H₂⁺-style one-lepton molecular bond). k_b calibrated on ⁶Li alone (+1.474) → **⁹Be predicted at −11% of +1.665. PASSED the ±15% gate.** Same rule gives He5 unbound (single alpha can't host the antipodal lobe) and ⁹Be bound with one mechanism.

**Experimental gift:** the neutron's mean-squared charge radius is NEGATIVE (−0.1155 ± 0.0017 fm², PDG): positive core, negative skin — the tokamak's e⁺-in/e⁻-out, required (not accommodated) by the geometry. Standard theory needs the pion cloud for this; here it is structural.

## 4. Hard bounds established against the theory's own prose

- **The slingshot is minority:** kinematic γ-collapse per NP channel ≤ 0.78 MeV (bounded by Δm_np) — ≤35% of even the deuteron. The surface/EM term must carry ≥65%. Prose saying the slingshot "explains the strong force" overclaims by ~3×.
- The published exact-match ledger (`nuclear-theory-unified.md` §9) uses C₃ = −2.702 in ³H but −2.688 in ³He — a 14 keV wiggle in the same constant absorbing residuals. Per-nucleus freedom in disguise. The falsifier-honest implementations are this audit's.

## 5. Known failures, owned

1. **A=3 absolutes +12%** (both mirrors, split exact): one shared cause — a lone triangle-closure is worth less than κ calibrated inside the braced K4. Fix must be *derived* from pore alignment, not fitted.
2. **⁸Be's last ~0.7–1.7 MeV:** the margin narrowed monotonically (−2.2 → −1.3 → −0.77) as physics improved, always from the unbound side. The remaining cancellation to −0.092 needs inter-alpha channel physics with a pre-registered window: **+1.67 ± 0.1 MeV, no more** — a two-sided vice (Coulomb alone overshoots unbinding 19×; generic attraction overshoots binding).
3. **⁷Li strain:** bracketed (+1.47 single-bridge / +2.95 double-bridge vs +2.467) — triton orientation geometry undecided.
4. **Spin-selectivity:** real np binding is triplet-only (singlet just-unbound, like nn). The phase-conjugacy rule does not yet know why. Hardest open problem; recorded before anyone tried to hide it.
5. **Kill-list (do not resurrect):** harmonic zero-point beyond A=3 (difference-of-large-numbers noise); pure surface force at the TO truncation limit (tops out at He4/H2 ≈ 6.3 vs 12.72 needed); the m! "quadra-lemniscate" numerology (tracks He4 but misses A=3 — [SPECIMEN] until derived).
6. **Edge-length collision:** organic packing orders He4 edges PP < NP < NN (neutron bigger); the theory docs assert NN < NP < PP. One is wrong; radii data can arbitrate. James to adjudicate.

## 6. Reproduction

All in `CGIOS/quantum/schrodinger/tests/capsid_audit/`: `ring_crossing.py` (crossing minima), `permutes2.py` (honeycomb theorems), `permute_capacity.py` (scorecard), `multi_alpha.py` (alpha ladder), `unified_v3.py` (gate trilemma), `sock_model.py`/`sock_capacity.py` (organic packing, saturation catastrophe), `foam_*.py` (surface-force regime scans). Python 3 + numpy/scipy. Experimental values AME-class; Coulomb α = 1.439965 MeV·fm; r₀ = 0.9 fm fixed a priori throughout.

## 7. Attack here (my own assessment of the soft points)

1. **The capacity law's origin.** "One trapped wave, two lobes → 2 channels" is the load-bearing assumption. It was *forced* (uncapped rules explode at A≥5) but not derived from lemniscate dynamics. If you can break He4's uniqueness proof without it, the doubly-magic result is a coincidence.
2. **κ (triangle cooperativity) is phenomenological.** 5.03 MeV from one calibration point. No mechanism computes it. The A=3 systematic (+12%) lives exactly here.
3. **The lattice idealization.** The honeycomb results assume BCC contact geometry; the organic sock shows skewed-a-hedral reality. How much of the clique/capacity structure survives off-lattice? (The disphenoid survived; the rest is unchecked.)
4. **Coulomb scale sensitivity.** Shell radius 0.9–0.945 fm and lattice spacing 1.71 fm were fixed a priori but not jointly fit with radii data. The −4.6% split could be luck. Demand the joint fit.
5. **Selection effects in the scorecard.** 13 systems, but geometry and proton placement were *optimized* per nucleus. Quantify the look-elsewhere effect: how well would a null model (random gates, same optimization freedom) score?
6. **The recursed closure law** rests on one Coulomb number (1.315/pair at "best lattice contact"). Vary the α–α distance model and see if the 0.5% C12/O16 agreement is robust or coincidental.

*Everything above may be wrong. The session's own record contains one instance of each: a model I built that collapsed (isotropic sock), an estimate I trusted that was noise (harmonic zero-point), and a guess of mine the data overruled (2^(1/3) radius ratio). The dumb tools won each time, as they should. — G.B.*
