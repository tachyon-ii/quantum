# Run-all, 17 Nov 2026 — four queue items taken to their blockers

**James Freeman** (the instruction: "Run them all … get to a blocker") · **Grace** `.ghost`, Claude Fable 5.2 (the computations and grades). Every number below was produced by the named script in this session; tables marked *generated* are code-written (R4′). Per-capsid slingshot bookkeeping throughout (DEEPDIVE-C2-lane §8). No GPU was used: the sandbox has 4 cores and no route to the A100 box; nothing here needed more.

Inputs, one source each: masses, R_p, c′, AME2020 — `models/kernel/data.py`; a_e, μ_p — CODATA; lepton masses — PDG.

| # | item | outcome | blocker |
|---|---|---|---|
| 1 | closed lanes as kernel bodies | linear attachment rule **DEAD**; unit not confirmed | attachment is itself a closure law |
| 2 | what κ = 0.18 means | screening **DEAD** (κ_eff = 0.97 ± 0.04); bonds strengthen ×1.25 | neutron fillers unmodelled |
| 3 | full retarded contact interaction | 31 Oct table **STRUCK**; channel ordering wrong | neutron's internal layout; radiation; no gap |
| 4 | Berry phase for a massive carrier | Rytov law **exact** for magnetic bending, g = 2 | what supplies 4.7 × 10¹² T |

---

## 1. Closed lanes as bodies — `models/kernel/lanes.py`, `lanes_report.py`

**Minimised/maximised:** BE = Y(2)·n_gated + Σ_lanes[u·C² − 0.854·n_singlet] − Coulomb(exact pp positions) + u·ATT, over every lattice placement of rigid motifs (α tetrahedron, T/³He triangle, D, 2n, single n/p). u = Q_β = 0.7823 MeV. **No fitted number.** ATT (the attachment count between bodies) is not derived, so six candidate rules × {singles refused, singles counted} were all run. Whole scan: `models/kernel/results/LANES-rule-scan.md` (generated).

Summary of the scan, singles refused:

| rule for ATT | rms miss, 12 bound nuclei A = 6–12 | holes kept (of 4) | ⁶Li | ⁷Li | ⁸Be (must be ≤ 0) | ¹²C |
|---|---|---|---|---|---|---|
| none | 11.4 % | 4 | −6.1 % | −7.9 % | S = −1.46 | −11.4 % |
| contacts | 6.3 % | 3 | +6.0 % | +5.1 % | S = +4.19 | −0.4 % |
| np contacts | 6.5 % | 3 | +0.3 % | −0.6 % | S = +1.71 | −5.3 % |
| np − like | 7.4 % | 3 | −2.5 % | −1.4 % | S = +0.62 | −7.1 % |
| triangles | 10.4 % | 3 | +10.9 % | +11.1 % | S = +7.32 | +6.4 % |
| newcomer nucleons touching | 7.6 % | 3 | −2.4 % | −2.8 % | S = +1.06 | −7.2 % |

Readings:

- **No rule passes.** Every rule that rewards attachment binds ⁸Be (by 0.6 to 7.3 MeV); the data say −0.09. With singles counted, every rewarding rule also binds ⁵He and ⁵Li. [COMPUTED → the linear attachment rule is **DEAD**]
- **The 30 Oct by-hand numbers reproduce** (⁶Li −2.4 %, ⁷Li −2.8 %, ⁷Be −3.6 % under "newcomer nucleons touching" = the counts 2, 3, 3). They were right arithmetic on a rule that then fails ⁸Be and misses ¹²C by −7 %. [COMPUTED]
- **The zero-freedom test of the unit.** What the data require of ATT, in units of Q_β: ⁶Li 2.51, ⁷Li 3.95, ⁷Be 3.97, ⁸Be 1.30. Not integers, and not the counts 2 and 3. The unit Q_β gains no support; it stays **COINCIDENCE-LEVEL**. [COMPUTED]
- **What the required counts do show.** Per α–α pair the data require 1.30 u in ⁸Be (open) and 4.48 u in ¹²C (each pair in one triangle of alphas): a factor 3.4 (2.4 if the inter-alpha Coulomb is taken at point-alpha distances instead of lattice positions). The nucleon rung's own ladder is 1 : 4.0 for the same step. **The attachment between bodies is a closure law, not a count** — the same graph property one rung up. [COMPUTED; the cross-rung reading is CONSTRUCT]
- ⁵He comes out exactly at threshold (S = 0.00) and ⁵Li at −1.03 under refusal: right sign, no roundness term needed, but refusal is a postulate here, not a result. [CONSISTENCY]

**Blocker.** A body-level closure law needs at least two numbers (open body-contact, body-contact in a triangle) and there are only two clean data to fix them (⁸Be, ¹²C). Beyond that it is rung B's q again. The cluster vocabulary cannot be made zero-freedom; the question it leaves is whether one closure function serves both rungs (1 : 4.0 : 8.3 at the nucleon rung against 1 : 2.4–3.4 : ~same at the alpha rung — on these numbers, no).

## 2. What κ = 0.18 means — `models/kernel/rungB/nz_geom.py`, `nz_test.py` (output: `nz_test_out.md`, generated)

The owed test was "N ≠ Z breaks the degeneracy". The cleanest N ≠ Z datum needs no neutron model at all: a **mirror pair** differs by one proton ↔ neutron, so its binding difference is the Coulomb energy of one proton in the cluster. Geometry: the soft-well optimum already on file (reproduced to the last digit). Model: point alphas, full charge, plus the measured in-alpha partner term (T − ³He = 0.764). No fitted number.

κ_eff = (measured − 0.764) / (full point-charge sum):

| core | hole pair (A = 4n − 1) measured | model, full Coulomb | κ_eff | particle pair (A = 4n + 1) measured | κ_eff (pocket at 2.7 fm) |
|---|---|---|---|---|---|
| C-12 | 2.764 | 2.598 | 1.09 | 3.003 | 0.94 |
| O-16 | 3.537 | 3.515 | 1.01 | 3.543 | 0.92 |
| Mg-24 | 4.839 | 4.989 | 0.96 | 5.059 | 1.00 |
| Ca-40 | 7.307 | 7.608 | 0.96 | 7.278 | 1.07 |
| Fe-52 | 8.836 | 9.304 | 0.95 | 9.070 | 1.10 |
| Ni-56 | 9.476 | 9.787 | 0.97 | 9.557 | 1.13 |

All twelve cores: hole pairs **κ_eff = 0.970 ± 0.042**; particle pairs 1.04 ± 0.06 (pocket distance declared, scanned 2.2–3.14 fm in the full table).

- **Screening is DEAD.** The inter-alpha Coulomb is paid in full, at the point-alpha rate, at the cluster's own geometry — to 3 % with nothing fitted. "Alphas see one-fifth of each other's charge" (20 Oct) is struck. [COMPUTED]
- **Therefore the α–α bond strengthens with coordination.** With Coulomb paid in full, the bond the data require rises from 4.26 MeV (C-12) to 5.32 MeV (Ni-56): ×1.25, q ≈ 3.26 + 0.33·z̄ (rms 0.19 MeV), log-slope 0.24 in mean coordination. Cooperative, but weakly — nothing like C². [COMPUTED; the linear form is CONSISTENCY]
- κ = 0.18 was the cooperative strengthening mis-booked as missing Coulomb. The ±3.8 % ladder of 20 Oct stands as a description; its third constant now has its meaning.
- Items 1 and 2 agree: bonds between alphas are worth more when they close loops with other bonds.

**Blocker.** The neutron-excess increments (Fe-56 − Fe-52 = 11.1 MeV per neutron; Ca-44 − Ca-40 = 9.7; Ne-22 − Ne-20 = 8.6) are the next data, and they need filler-nucleon pockets on an alpha cluster — a rung-0-on-rung-B seating that does not exist yet and, after item 1, has no attachment law to use.

## 3. The contact, with full retardation — `models/contact/retarded.py`, `channels.py`

Two carriers at c′ on coplanar tangent lanes; exact Liénard–Wiechert potentials and fields (retarded time solved by Newton iteration; static limit validated to four figures). U = minus the time-averaged interaction Lagrangian, time-symmetric (retarded and advanced agree).

**Erratum to `docs/contact-patch-em.md` §3.** The 31 Oct table compared two different configurations *and* two different phases: its "gear" column is the Darwin value for **counter-rotating** lanes (carriers co-moving at the contact) at phase 0; its "belt" column is close to same-sense lanes at phase π (carriers never meeting). At equal phase lock the Darwin values are nearly equal (−2.20 vs −2.18 MeV at 0.1 fm), because co-moving carriers dwell together longer and that offsets the weaker instantaneous factor. The ratio 4–7 was an artefact. **Table and "spin dependence from gear kinematics": STRUCK.** (Also: meshing gears counter-rotate; the doc's names were backwards.)

Full retarded, e⁺/e⁻, phase 0 (MeV):

| gap (fm) | same-sense (anti-parallel at contact) | counter-sense (co-moving at contact) |
|---|---|---|
| 0.1 | −1.80 | −2.29 |
| 0.3 | −1.21 | −1.45 |
| 0.5 | −0.91 | −1.03 |

Most of that is the plain Coulomb attraction of an e⁺ and an e⁻, which a neutral neutron cancels. With a neutral neutron (declared: e⁻ and e⁺ antipodal on one lane, same sense) only the **correlation** energy survives:

| channel, gap 0.3 fm | same-sense | counter-sense |
|---|---|---|
| pn | −0.41 | −0.83 |
| nn | −0.83 | −1.67 |
| pp | +0.77 | +0.61 |

- **Scale: right.** A phase-locked contact is worth 0.4–1.7 MeV against the data's 0.79 per open contact. [COMPUTED]
- **Ordering: wrong.** The model gives nn > pn > pp and counter-sense > same-sense. Data: pn triplet bound, pn singlet and nn unbound. With parallel angular momenta read as the triplet, the sign of the spin dependence is reversed, and nn binds twice as deep as pn. [COMPUTED → the two-carrier contact picture, as declared, is **DEAD** on the channel ordering]
- **No gap.** The mean force is attractive and grows like 1/g down to 0.03 fm; nothing in the electromagnetism sets a gap. The potential of mean force does not converge at long range either — the 1/r radiation fields make it oscillate out to 60 fm. [COMPUTED]

**Blockers, three.** (i) The neutron's internal layout is an input the ontology has not fixed (James, 19 Oct: orthogonal e⁺/e⁻ — that is a 3-D lane geometry, not this coplanar one; it is the next run if the picture is to be kept). (ii) Two charges at 0.92c on 0.84 fm circles radiate 39.7 MeV per fm/c by Larmor, fifty times their kinetic energy per fm/c; a non-radiating condition has to be stated before any classical EM number here means anything. (iii) The gap must come from the capsid, not the carriers.

## 4. The geometric phase for a massive carrier — `models/berry/bmt.py`

The Thomas–BMT equation on a closed path at constant speed gives the spin an angular velocity λ × (the velocity direction's own angular velocity), with λ depending only on what bends the path. Closed forms checked against direct integration of the full T-BMT equation to six figures:

| what bends the carrier | λ | at c′ (γ = 2.531): spin turns per orbit | spinor return (−1 = antiperiodic) |
|---|---|---|---|
| magnetic field ⟂ v, g = 2 exactly | 1 | 1.000000 | **−1.000000** |
| magnetic, g = 2(1 + a_e) | 1 + a_e γ | 1.002935 | −0.999957 |
| electric field ⟂ v, g = 2 | 1 − 1/γ | 0.605 | −0.32 |
| no torque (pure Thomas) | −(γ − 1) | −1.531 | +0.10 |

- **The Rytov law is exact for a massive g = 2 carrier bent magnetically, at any speed.** With λ = 1 the spin is parallel-transported with the tangent, which is the photon's law; the owed item of `BERRY-ring-chirality.md` §5 is discharged for that case. This is the principle behind every g − 2 storage ring. [COMPUTED + FACT]
- **For any other bending the ring is not a spinor at c′.** Electric bending gives 0.605 of a turn; torque-free transport gives −1.531. (Pure Thomas would be exact at γ = 2, v = 0.866c — not c′.) So "a ring is a spinor" now carries a condition: the carrier is held on its lane magnetically. [COMPUTED]
- **The anomaly detunes the ring by a_e γ = 0.00294 turns** (0.0184 rad). Conjecture tested: the small single twist is whatever cancels that. Result: on the (k,1) twisted rings, k = 1, 2, 3, the return moves *away* from −1 monotonically with twist amplitude; no cancellation. **DEAD** in this family. What sets the twist is still open. [COMPUTED]
- Required bending field: B = γ m_e β c / (e R_p) = 4.71 × 10¹² T. The field at the centre of a loop of radius R_p whose moment is μ_p is 4.74 × 10¹² T (ratio 0.993; equivalently μ_p ≈ ½ γβ·e c R_p²/r_e). One hit in eight trials (μ_p, μ_n, μ_N, the loop's own moment × centre/equatorial) spanning a factor 7; chance of a 1 % hit ≈ 8 %. **COINCIDENCE-LEVEL**, recorded so it is not rediscovered as an identity. [COMPUTED]

Generations (the 31 Oct thread): Koide Q = 0.666665; Brannen phase δ = 0.222239 rad (2/9 = 0.222222); m_τ from (e, μ, Q = 2/3) = 1776.97 against 1776.93 ± 0.09. In the form √m_k = μ(1 + √2 cos(δ + 2πk/3)), Q = 2/3 says the constant part and the oscillating part of √m carry equal power (computed ratio 0.999993). [FACT; the reading "three phases of one ring, DC = AC" is CONSTRUCT.] Nothing in the ring geometry computed so far produces δ.

**Blocker.** What supplies the bending field. If it is the nucleon's own moment the calculation is a self-field problem (divergent on the loop itself); if it is not magnetic, the ring is not a spinor at c′.

---

## Ledger changes

| claim | was | now |
|---|---|---|
| inter-alpha Coulomb screened to ~1/5 (20 Oct) | CONJECTURE | **DEAD** — κ_eff = 0.97 ± 0.04 on twelve mirror pairs |
| α–α bond strengthens with coordination | alternative reading | **COMPUTED**: ×1.25, C-12 → Ni-56 |
| clusters of lanes with counted attachments (30 Oct §3) | CONSISTENCY at −3 % | **DEAD** as a rule (⁸Be bound; ¹²C −7 %); the three A = 6–7 numbers stand as arithmetic |
| unit of the C² law = Q_β | COINCIDENCE-LEVEL | unchanged; zero-freedom test gave it no support |
| contact-patch table, gear ≫ belt (31 Oct) | COMPUTED | **STRUCK** — mismatched phases and labels |
| carrier EM at the contact gives the nuclear spin dependence | CONSTRUCT | **DEAD** as declared (nn > pn, wrong spin sign); scale survives |
| Rytov phase applies to a massive carrier | OWED | **COMPUTED**: exact iff magnetic bending with g = 2 |
| twist cancels the anomaly detuning | (new) | **DEAD** in the (k,1) family |

What survives and is now sharper: cooperation is the common finding at both rungs — a bond is worth more when it closes loops — and it is *not* one universal function (C² at the nucleon rung, ×1.25 per coordination range at the alpha rung).

## Regrade, 19 Nov — after independent recomputation

Full review: `review/2026-11-18/FEYNMAN-run-all-17nov.md` (35 claims: 22 confirmed, 1 wrong, 7 over-claimed, 2 unsupported, 3 not checked). Accepted in full. Language note (James, 18 Nov): a run that shows where a model cannot pass has *located a hole*; only individual claims are marked false.

| claim in this note | review | regrade |
|---|---|---|
| all code and arithmetic in §1–§4 | reproduced independently (lane enumerator to two decimals; six retarded entries; three λ formulas to six decimals) | stands |
| screening DEAD (§2) | confirmed and not circular: κ = 1 geometry gives 0.971; a uniform sphere at measured radii gives 1.00–1.02 | **stands** |
| "κ_eff to 3 %" | ±0.042 is scatter about a trend (1.09 → 0.94); the model's radii run low | **reworded: κ_eff ≈ 1, not 0.18** |
| "therefore the bond strengthens with coordination" [COMPUTED] | not forced: a constant 4.24 MeV bond plus 0.92 MeV per second-neighbour pair fits the same 13 nuclei better (rms 1.30 vs 2.80 MeV) | **downgraded to one of two readings; open** |
| "κ = 0.18 was cooperative strengthening mis-booked" | depends on the line above | **unsupported; withdrawn** |
| factor 3.4 per α–α pair, ⁸Be → ¹²C (§1) | compared a chain with a triangle; like for like it is 2.4–2.7 | **wrong; corrected to 2.4–2.7** |
| match to the nucleon rung's 1 : 4.0 | not shown | **withdrawn** |
| "linear attachment rule DEAD" | only five counts were run; a count per touching body pair leaves ⁸Be unbound, and a count of loops through three bodies was never tried | **narrowed: the five counts tested do not pass** |
| required attachments "not integers" | with measured body energies ⁷Li is 4.00 and ⁷Be 3.89; only ⁶Li and ⁸Be are clearly non-integer | **narrowed** |
| ⁵He at threshold [CONSISTENCY] | zero by construction; the same refusal puts ⁹Be and ⁸Li at zero against measured +1.66 and +2.03 MeV | **struck** |
| "nn binds twice as deep as pn" (§3) | an identity of the neutron layout Grace declared, not a result | **struck as a finding; the layout was the assumption** |
| pp row of the channel table | not a correlation energy as labelled; the true values are −0.11 and −0.17 MeV | **corrected** |
| "scale: right" (§3) | it is e²/R_p with a chosen gap | **downgraded: order of magnitude only** |
| Larmor 39.7 MeV per fm/c | correct per charge | stands |
| look-elsewhere 8 % for the field coincidence (§4) | fair for the eight trials listed, but the family was chosen after the hit | **stays COINCIDENCE-LEVEL, weaker** |
| Koide Q = 0.666665 | 0.6666645 | last digit corrected |

Not checked by the review: the mean-force integral out to 60 fm, the twisted-ring result, and the scan for nuclei other than ⁸Be and ¹²C.

## Next, in order of what unblocks most

1. **A closure law at the alpha rung with full Coulomb**: refit rung B with q(z) and κ = 1; two constants instead of three, and the mirror energies come free. Runnable now.
2. **Filler neutrons on the alpha cluster** (Fe-56, Ca-44, Ne-22) — needs James's ruling on how a single nucleon seats on a closed body, since refusal (item 1) and 11 MeV per neutron (item 2) pull opposite ways.
3. **The neutron's lane layout** (orthogonal e⁺/e⁻) in 3-D, same retarded code — only if a non-radiating condition is first stated.

## Lineage

The four questions and the neutron composition: James. The mirror-pair route to κ, the rule scan, the retarded computation and erratum, the T-BMT result and the three kills: Grace. Prior art: Nolen–Schiffer 1969 (mirror displacement energies); Thomas 1927; Bargmann–Michel–Telegdi 1959; Rytov 1938; Koide 1982; Brannen 2006; Wheeler–Feynman 1949.
