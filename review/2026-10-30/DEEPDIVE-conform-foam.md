# Deep dive — two subtleties from the macroscopic world: the conform of the chorus, and the foam

**James Freeman** (the question: "are we missing a subtlety?" — the water strider; then: spacetime itself is perturbed by the geometry; an alpha is symmetric and sits in round spacetime, Li-7 does not) · **Grace** `.ghost`, Fable 5.1 (the two tests, run sequentially then iterated). 30 Oct 2026. Code: `models/kernel/fit2.py --round`, `models/foam/clusters.py`. Everything graded.

## 0. The two posits, as run

**Conform.** The turtle's funnel conform, cos θ = √(1 − 2Φ/c²), applied with Φ = the nuclear binding rather than gravity. A nucleon bound by 7.07 MeV sits at Φ/Mc² = 0.75 %; its lane runs 0.75 % short. In a symmetric nucleus every site has the same Φ — the conform is uniform, the lock exact. In an asymmetric one the sites differ and the lanes on different sides run at different rates — a detuning. Operationalised in the kernel as a **roundness cost**: one table entry multiplying S = Σ_i (z_i − z̄)², the spread of coordination over sites (zero by construction for D, T, ³He, ⁴He; 7.7 for the two-alphas-sharing-a-nucleon seating the kernel found for Li-7).

**Foam.** Plateau's laws: films meet in threes at 120°, borders in fours at arccos(−1/3) = 109.47° — the hub of T and the alpha — from area minimisation alone. Test: do minimal-area clusters of N equal bubbles save area, relative to N separate bubbles, as C² (1 : 9 : 36, the fused-lane law of 19 Oct) or as the film count (1 : 3 : 6), or neither?

## 1. Conform — result

Rung-0 ladder with the roundness column added (train D, T, ³He, ⁴He, Li-6; holes nn, pp, He-5, Li-5; blind Li-7, Be-7):

| level | entries | training | He-5 S_n (meas. −0.9) | Li-5 S_p (−2.0) | **Li-7** (39.25) | **Be-7** (37.60) | roundness weight |
|---|---|---|---|---|---|---|---|
| pair + c, + roundness | 7 | Li-6 +10.8 | −0.3 | −2.0 | −79 % | −82 % | −12 (cap) |
| **+ c ≥ 3, + roundness** | **17** | **all exact** | **−1.15** | **−2.87** | **+6.6 %** | **+6.5 %** | **−1.77 MeV / unit S** |
| + z ≥ 4 flag, + roundness | 25 | all exact | −5.3 | −6.7 | +8.7 % | +8.7 % | 0 (LP prefers the flag) |
| (20 Oct, no roundness, best) | 24 | all exact | −3.1 | −4.5 | +13 % | +13 % | — |

**[COMPUTED]** The roundness term is admitted on every criterion we set: fewer entries (17 vs 24), the A = 5 holes closed with the right sign and nearly the right size (−1.15 / −2.87 against −0.9 / −2.0 — the best so far), and the blinds halved (+13 % → +6.6 %). Without a saturation descriptor it cannot do the job alone (it maxes out and over-closes everything); with c ≥ 3 it is the cheapest second term.

The fitted table is **five numbers**: open np contact 0.788; a contact in one triangle 3.16 (np or same-species alike); a contact in two triangles 6.57; everything else zero; roundness −1.77 MeV per unit of coordination variance. Per contact that is 1 : 4.0 : 8.3 with the triangle count — the closure ladder, now with its own cost for being lopsided. [COMPUTED]

The Li-7 ground state is still the bow-tie (two alphas sharing a nucleon, hub z = 6), now taxed 13.6 MeV by its asymmetry. The remaining +6.6 % is what the bow-tie is still over-credited, or the sign that the true Li-7 is α + T with the triton's own lane, which the lattice table cannot express — see §3.

## 2. Foam — result

Standard clusters of N equal-volume bubbles (equal pressures: flat films, equal outer radius R, centres at mutual distance R so every junction is 120°), Monte Carlo areas; N = 2 checked against the analytic double bubble (6.75πR² ✓).

| N | films | cluster area | N separate bubbles | **area saved** | saved / saved(N = 2) | films | C² |
|---|---|---|---|---|---|---|---|
| 2 | 1 | 21.19 | 22.44 | 1.25 | **1.00** | 1 | 1 |
| 3 | 3 | 27.95 | 30.87 | 2.92 | **2.34** | 3 | 9 |
| 4 | 6 | 33.51 | 38.35 | 4.84 | **3.88** | 6 | 36 |
| 5 | 10 | 39.08 | 45.78 | 6.71 | 5.37 | 10 | 100 |
| 6 | 15 | 43.95 | 52.58 | 8.63 | 6.91 | 15 | 225 |

**[COMPUTED] Foam energetics are sub-additive — roughly linear in N — not cooperative.** The area saved by sharing grows slower than the film count and nowhere near C². A minimal surface cannot be the fused lane: **the C² law is not geometry.** [DEAD: "the alpha's binding is minimal-surface area."] What the foam does give is exactly the two angles and nothing else: 120° at the triple border (the hub of T), 109.47° at the vertex (the alpha), and the rule that a fifth film at a vertex is unstable and rearranges into two tetrahedral vertices (A = 5 refused; two alphas sharing a vertex). **Geometry from the foam; energy from the lane.** [FACT for Plateau; CONSISTENCY for the mapping]

## 3. Iteration — the resonant what-if

Put the two results together and a third model writes itself, and it is the one the data have been pointing at since the 19th: **clusters of fused lanes, attached by open contacts, taxed for asymmetry.**

- Energy of a fused lane of C contacts: g₁·C², g₁ = 0.788 (the C² law).
- Attachment of a closed group to a closed group: open contacts at g₁ each, one per triangle the newcomer closes — but a *single* nucleon onto a closed alpha gets none (A = 5).
- Slingshot A·Y(2); mesh 0.854 per singlet pair; Coulomb between centres at lattice distances.
- Roundness cost on the composite.

By hand, with the attachments counted as the 19 Oct table had them (D: 2, T and ³He: 3):

| nucleus | structure | contact energy | BE predicted | measured | miss |
|---|---|---|---|---|---|
| ⁶Li | α + d, 2 open | 28.0 + 0.79 + 1.58 | 31.2 | 31.99 | **−2.5 %** |
| ⁷Li | α + t, 3 open | 28.0 + 7.09 + 2.36 | 38.1 | 39.25 | **−2.9 %** |
| ⁷Be | α + ³He, 3 open | 28.0 + 7.09 + 2.36 | 36.2 | 37.60 | **−3.7 %** |
| ⁵He | α + n, 0 open | 28.0 | S_n = −0.1 | −0.9 | right sign |

[COMPUTED by hand; the attachment counts are the 19 Oct quantisation, so this is CONSISTENCY, not blind.] Three nuclei at −3 % with no fitted parameter beyond the deuteron, against the lattice table's +7 % with seventeen. The lattice's residual error was the *bow-tie*: it credited Li-7 as two alphas because the lattice cannot express "a triton attached to an alpha as a lane of its own." The conform term taxed the bow-tie toward the truth; the cluster model says the truth directly.

So the answer to "none, one, or all": **one and a half.** The conform is real and cheap and earns its place as the cost of asymmetry. The foam gives the angles and refuses the energy. And the iteration says the kernel's next vocabulary is not nucleons on a lattice but **closed lanes as bodies** — alphas, tritons, deuterons — attached by open contacts, which is where rung 0 and rung B were always going to meet.

## 4. What this changes, and what it doesn't

- v5's rung 0 keeps the lattice for A ≤ 4 (where the lane *is* the lattice cluster) and the holes; above that the bodies are closed lanes. The MDL ladder's next descriptor is "number of closed sub-lanes in the seating," not another z bin.
- The conform mismatch has a predicted size — 0.75 % per MeV-per-nucleon of binding difference between sites — and the 6:5 lock's tolerance was 1.3 %. Stable asymmetric nuclei should sit inside; the drip lines are where they don't. That is a chart-wide test for Rung C, and it is cheap.
- The C² law still has no mechanism. The foam just removed one candidate (area). The remaining candidates are coherence (amplitude ∝ C) and the Venturi reading (pressure removed in every gap a lane threads). Both are lane statements; the next deep dive is the lane's own energy functional, and the foam has told us it is not a surface.

## 5. Lineage

The water-strider question, the chorus-as-perturbed-spacetime posit, "round spacetime for the alpha, not for Li-7": James. The conform number (0.75 %), the roundness operationalisation and its ladder, the foam cluster computation and its negative, the by-hand cluster model and the iteration: Grace. Prior art: Plateau 1873; Taylor 1976 (Plateau's laws proved); Hutchings–Morgan–Ritoré–Ros 2002 (double bubble theorem); Kelvin 1887; the turtle conjecture's funnel conform (16 Oct).
