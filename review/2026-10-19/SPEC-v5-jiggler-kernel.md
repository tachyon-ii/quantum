# SPEC v5 — the jiggler: let the solution set define the rules

**Grace** `.ghost`, Claude Fable 5.1 — Mon 19 Oct 2026, late morning. Thought, not code. Supersedes the term-by-term programme of v1–v4 as the *primary* method; the membrane solver becomes the microscope for mechanism once the kernel says which rule matters. James's framing (19 Oct): nature solved the few-body problem by relaxation; three of its outputs — **⁴He, ¹⁶O, ⁵²Fe** — are anchors at three rungs; any putative solution must intersect them exactly, and the rules are to be read off the solution set, with the mathematics backronymed afterwards.

---

## 0. What went wrong with v1–v4, stated once

Four functionals, each written from a picture, each tested against two or three nuclei, each failing at the next one: skin adhesion (anti-cooperative), crease recovery (no support), lane factor linear (open at A = 5), lane factor capped (closes A = 5, kills T). The pattern is not that the pictures were bad — the lane factor got T to 4 % blind — it is that **one term per day against a solution set of 2,550 masses is the wrong ratio of hypothesis to data.** The data hold the rules. We should ask them.

## 1. The anchors, and what each one pins

Three closed structures, one per rung, each the first fully closed object at its level. They are not calibration points in the fitting sense; they are **hard equalities** the kernel must satisfy before anything else is scored (R13).

| anchor | rung | what it is | what it pins |
|---|---|---|---|
| **⁴He** 28.2957 MeV, R_ch 1.678 fm | 0 (nucleons) | two crossed dumbbells (pp × nn), four np contacts each in two triangles | the value of a **closed** nucleon contact (c = 2, z = 3) and the scale of the nucleon rung |
| **¹⁶O** 127.619 MeV, R_ch 2.70 fm, spherical | 1 (alphas) | tetrahedron of alphas, six α–α bonds each in two triangles | the value of a **closed α–α bond**, q (residual 14.44 / 6 = 2.41 MeV) |
| **⁵²Fe** 447.700 MeV | 2 (shells) | kissing shell: 12 alphas around 1 | the **reach** of the α–α well — 42 geometric bonds worth 32.9 effective, i.e. a 5 % stretch costs ~30 % of a bond (dome: ρ_α ≈ 0.3 fm) |

Two more data are **open-bond anchors**, one per rung, because a contact with no triangle is the other end of the closure function: **D** (2.2246: an np contact with c = 0, worth 0.788 after the slingshot) and **⁸Be** (−0.092: an α–α bond with c = 0, worth ≈ 0). Together the five numbers say, before any model: *at the nucleon rung an open contact is 17 % of a closed one; at the alpha rung it is zero.* That difference is the first thing the kernel has to explain, not assume. [FACT, from AME alone.]

## 2. The core observational data — the solution set, including its holes

The jiggler is fed the solutions nature found **and the ones it did not**. Both are data; the second kind has been under-used.

1. **Masses** — AME2020, measured entries only (2,550). Binding energies; derived S_n, S_p, S_d, S_α, Q_β.
2. **The holes** — systems that are *not* bound, as inequalities: nn (virtual, +0.07), pp, ⁵He (−0.89), ⁵Li (−1.97), ⁸Be (−0.092), ⁷He, ⁴Li, ⁹B (−0.19), ¹⁰Li, the proton and neutron drip lines. A kernel that binds ⁵He is wrong whatever it does for ⁴He. These are **constraints**, not fit points.
3. **Radii** — charge radii (Angeli & Marinova 2013) for shape and scale: D 2.128, T 1.759, ³He 1.966, ⁴He 1.678, ¹²C 2.47, ¹⁶O 2.70, ⁴⁰Ca 3.48, ⁵⁶Fe 3.74 fm. Classical minima under-estimate them; the *ratios* between nuclei are the usable part.
4. **Shapes** — intrinsic quadrupoles: D +0.286 fm² (prolate), ¹⁶O ≈ 0, ²⁰Ne +57 e fm², ²⁴Mg, ²⁸Si (oblate). Spherical anchors must come out spherical.
5. **Separation-energy structure** — the odd–even stagger (Δ₅), the drops after 2, 8, 20, 28, 50; S_α along the 4n ladder (⁸Be −0.09, ¹²C 7.37, ¹⁶O 7.16, ²⁰Ne 4.73, ²⁴Mg 9.32, ²⁸Si 9.98, …). Magic numbers are **outputs** to be checked, never inputs.
6. **Correlations the field has already found** — the Tjon line (⁴He vs ³H binding across all realistic forces, slope ≈ 4–5, nature on it); the Wigner energy (+0.92 MeV for N = Z, 4n); the Coester band (saturation density vs binding). A kernel off the Tjon line has the T/⁴He mechanism wrong even if both numbers are close.
7. **Reachability** — the assembly order is itself data: D → T, ³He → ⁴He; then α-capture; ⁸Be unbound but ¹²C reached through the Hoyle state. The jiggler scores **reachable minima**, not global ones (R15): a seating that cannot be assembled from the previous rung's closed outputs is not a solution, however low its energy.

## 3. The kernel

Minimal vocabulary; everything else is a table the data fill.

**Bodies.** Rung 0: p, n as hard spheres of radius R_p, 1.023 R_p, point charge at centre. Rung 1: the alpha as a rigid closed unit (radius 1.57 fm from the α–α distance 3.139) plus *filler* nucleons for A ≠ 4n. Rung 2: the kissing shell as a unit when it closes. A body at rung r is a closed output of rung r − 1 — closure is what promotes it.

**Contacts.** A pair of bodies within reach. Per contact, a small set of **discrete descriptors**:
- species pair (np, nn, pp at rung 0; αα, αN, NN at rung 1);
- **c** — common contact partners (triangles through the contact);
- **z_i, z_j** — coordinations of the two bodies;
- **stretch** — centre distance over the rung's contact distance, binned (rung 1 and up);
- **shared faces** — how many triangles the contact's two triangles share with other contacts (the crease count), optional, earned not given.

**Energy.** E = Σ_contacts g_r(descriptors) + Coulomb (pairwise, centres) + L_r(graph). The table **g_r** is the unknown. L_r is the lane/slingshot term — at rung 0, A·Y(2) gated by "every body has a triplet contact"; at rung 1 nothing, unless the data demand it (the α–α open bond ≈ 0 may be the statement that alphas fuse no lane). Mesh penalty as in v3 (0.854, from the singlet) is a *fixed* prior, not a table entry.

**What is deliberately not in the kernel:** any continuous shape of the patch, any stiffness, any inflation constant. Those are the membrane's business. Here a contact is a label and a number.

## 4. The search — two loops and a ladder

**Inner loop — seating.** For a given table g, find each nucleus's lowest-energy arrangement *and the full range* (R6). Rung 0 on the BCC lattice (Build 3's enumeration — exhaustive to A ≈ 9, Monte Carlo beyond). Rung 1 as sphere packings of alphas with pocket sites for fillers (deltahedra, kissing arrangements, edge/face seatings), enumerated. The "jiggle" is Monte Carlo annealing over seatings when enumeration is too large; on CPU to A ≈ 60 in minutes with point bodies; GPU only if the full chart is attempted with continuous positions.

**Outer loop — the table.** Given seatings, a nucleus's energy is **linear in the table entries**. So the fit is a linear problem: equalities for the anchors (R13), equalities within AME uncertainty for the training set, **inequalities for the holes**, and a complexity penalty. That is a linear program with an MDL objective — minimise |table| subject to the constraints, then minimise residual at that size. Re-seat with the new table; iterate to a fixed point. Report every iteration.

**The ladder — binary search over complexity.** Start with the smallest table that can exist: g depends on species pair and on c ∈ {0, 1, ≥2} only (nine numbers at rung 0). Fit; score the blinds. Add one descriptor at a time (z, then stretch, then shared faces), each admitted **only if the blind error on the held-out set falls by a declared factor (×0.7)**. Stop when it doesn't. The table size at the stop is the information content of the rung. This is James's "binary search across an ever-increasing space," made auditable.

**Train/blind split, fixed now:** rung 0 trains on A ≤ 4 plus the holes at A = 5 and predicts A = 6–12 (⁶Li 31.99, ⁷Li 39.24, ⁷Be 37.60, ⁹Be 58.17, ¹⁰B, ¹²C via alphas). Rung 1 trains on the 4n ladder to ²⁰Ne plus ⁸Be and predicts ²⁴Mg → ⁶⁰Zn and every pocket nucleus (⁹Be, ¹³C, ¹⁷O, ¹⁸F, ²⁰Ne, ⁵⁶Fe). Rung 2 trains on ⁵²Fe and predicts ⁵⁶Ni, ⁶⁰Zn and the end of the ladder.

## 5. Standing tests (every iteration, by code)

T1 anchors exact (⁴He, ¹⁶O, ⁵²Fe) · T2 holes respected (⁵He, ⁵Li, ⁸Be, nn, pp unbound; drip lines not crossed) · T3 Tjon line — the (³H, ⁴He) pair on it within 0.3 MeV · T4 spherical anchors spherical (¹⁶O Q₀ < 5 e fm²), ²⁰Ne prolate (Q₀ > 30) · T5 the 4n ladder to ⁵⁶Ni within 5 % with the end at Ni (⁶⁰Zn's S_α < 3 MeV) · T6 Wigner: N = Z 4n nuclei over-bound relative to neighbours by ~1 MeV · T7 magic numbers appear as drops in S_n at 8, 20, 28 without being told · T8 the per-bond rank table 1 : 1.4 : 3.1 reproduced from the fitted g, not imposed · T9 reachability: every reported minimum has an assembly path from the rung below.

A kernel that passes T1–T3 and fails T5 is more informative than one that passes nothing; the report says which.

## 6. The backronym — reading the table

When a table passes, it is a set of numbers like g_np(c=0,z=1) = 0.79, g_np(c=1,z=2) = 2.39, g_np(c=2,z=3) = 4.67, g_αα(c=0) = 0, g_αα(c≥1, stretch 0) = 2.41, g_αα(c≥1, stretch 5 %) = 1.7. Then, and only then, ask what law they are: symbolic regression over a small basis (linear in c; saturating in c; dome in stretch; capacity in z; products), scored by MDL. Candidates already on the table from v3/v4 — f = 1 + λc; capacity min(1, 3/z); dome 1 − x² — become hypotheses the fitted table votes on rather than rules we imposed. The two-rung difference in the open-bond value (17 % vs 0) is the first thing the regression has to produce a reason for; my prior is that it is the slingshot gate (nucleons fuse a lane, alphas don't), but that is a prior and goes in the report as one.

## 7. Where the membrane fits now

The table says *which* rule carries the weight (c? z? stretch?). The membrane is then asked *why* — the mechanism of that one rule, with its eggs, peel fronts and pull-off peaks — on the three or four nuclei where it matters. It stops being the engine and becomes the microscope. The v4 A3–A5 items move here unchanged.

## 8. Rules

R1–R12 carried (one source per input; nothing after a target; blinds declared; code-written reports, Grace re-runs; graded lines; lineage; no literature against a blind; declare-and-continue; cache names carry version and base; scans reported whole; the lens's three lines at the head). **R13** anchors are equalities, satisfied before scoring. **R14** holes are inequalities and count as data. **R15** only reachable minima are solutions. **R16** a descriptor is admitted only on blind improvement by ×0.7; the table's size is reported as the result's information content. **R17** the backronym step runs after the table passes T1–T5, never before.

## 9. What would kill the approach

No table of any size fits ⁴He, ¹⁶O and ⁵²Fe together with the same Coulomb and the same Y(2) (the anchors are inconsistent in this vocabulary → the vocabulary is wrong). Or: the rung-0 table that fits A ≤ 5 needs more than ~12 entries to predict A = 6–12 within 10 % (no compression → no rule → the contact picture is not where the structure is). Either outcome is a result and ends this line honestly.

## 10. Deliverables and order

1. `kernel/data.py` — the solution set as declared in §2, including the holes as inequalities and the anchors flagged. Nothing else reads AME.
2. `kernel/seat.py` — rung-0 lattice enumeration (from Build 3) and rung-1 alpha packings with pocket sites; returns descriptors per contact and the full seating range.
3. `kernel/fit.py` — the LP/MDL table fit with anchors as equalities, holes as inequalities, train/blind split as §4.
4. `kernel/ladder.py` — the complexity ladder with the ×0.7 admission rule; `report.md` by code.
5. The backronym pass, separate, after T1–T5.
Order: rung 0 end to end (an afternoon) → rung 1 (the ladder and the pockets) → rung 2 (kissing) → backronym. Membrane microscope afterwards.

## 11. Lineage

The three anchors and their rungs, "let the solution define the rules and backronym the math," the jiggler, the fractal assembly, the kissing shell: James. The holes as inequalities, the Tjon line and Wigner energy as standing tests, reachability as a rule, the MDL ladder with the ×0.7 admission, the open-bond observation (17 % vs 0) as the first backronym target, and the membrane's demotion to microscope: Grace. Prior art: Faddeev 1961 / Fujita–Miyazawa 1957 (the three-body wall); Tjon 1975; UNEDF (functionals fit to masses); GAP/MACE (learned potentials); PySR / AI Feynman (symbolic regression); Rissanen (MDL).
