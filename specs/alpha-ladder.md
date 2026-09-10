# spec: alpha-ladder — is there one α–α contact quantum, and does it pay only in closed loops?

**Model:** Sonnet leaves, one nucleus each, under a Fable hypervisor (Neyman). Sonnet because the work is counting and arithmetic on a fixed geometry; the failure mode to guard is *inventing a parameter*, not regression to the mean. **Test dir:** `tests/alpha-ladder/`. Drafted by Grace `.ghost` 2026-09-10 from James's posit; not yet reviewed (010).

## The claim it serves

`docs/three-term-binding.md` §5–§8: He-4 is the cliff — the only A ≤ 4 assembly that packs (Kelvin cells, whole faces), and the unit everything heavier is built from. James's posit (2026-09-10): above He-4 the binding is **α-clusters in contact**, and an α–α contact pays a fixed quantum **only when the contact is part of a closed loop**. Three points already on the table, from AME masses and nothing else:

| nucleus | Nα | BE − Nα·BE(He4) | α bond graph | per bond |
|---|---|---|---|---|
| Be-8 | 2 | −0.092 MeV | one edge, no loop | ≈ 0 (unbound, 92 keV) |
| C-12 | 3 | 7.274 | triangle, 3 edges | 2.425 |
| O-16 | 4 | 14.435 | tetrahedron, 6 edges | 2.406 |

Two independent closed shapes give the same number to 0.8%. Be-8, the open case, gives zero. That is the whole of the evidence; it is enough to write the test and not enough to believe it.

## The test, written first

For each α-conjugate nucleus from Ne-20 to Ni-56 (Nα = 5 … 14), the leaf must:

1. **Build the α-cluster geometry from packing alone** — spheres of the He-4 radius (1.678 fm) in contact, closest packing, no reference to any binding energy. Record the contact graph: vertices, edges, and which edges lie on a closed cycle.
2. **Predict** BE = Nα·28.296 + (edges in closed cycles)·q, with **q = 2.42 MeV fixed** from C-12/O-16 above. No refit. If the leaf wants to move q, the test has failed, not q.
3. **Compare** to AME (`BE − Nα·28.296` is tabulated below; the leaf does not get to look it up before step 1 — build first, read after).

Measured excess over Nα α's (AME 2020, MeV; the answer column — cover it until step 1 is done):

| nucleus | Nα | excess | | nucleus | Nα | excess |
|---|---|---|---|---|---|---|
| Ne-20 | 5 | 19.165 | | Ar-36 | 9 | 52.053 |
| Mg-24 | 6 | 28.481 | | Ca-40 | 10 | 59.092 |
| Si-28 | 7 | 38.465 | | Ti-44 | 11 | 64.219 |
| S-32 | 8 | 45.413 | | Cr-48 | 12 | 71.910 |
| | | | | Fe-52 | 13 | 79.849 |
| | | | | Ni-56 | 14 | 87.844 |

(Fe-56, the stability peak, is **13α + 4n**, not 14α; Ni-56 is the 14α. Fe-56 is a second-phase question — what four loose neutrons buy — and is out of scope for this spec.)

| outcome | grade |
|---|---|
| every nucleus within 2% with q fixed and edges counted from packing | **[PASS]** — the quantum is real; promote to `three-term-binding.md` §9 and register the test at the wall |
| within 2% except one or two, and those are the known deformed clusters (Ne-20 is the usual suspect) | **[PASS-WITH-RESIDUE]** — write the residue as its own todo line; do not bend q |
| fits only if edges are counted from the answer (e.g. choosing which cycles "count" after seeing the excess) | **[FAIL — CIRCULAR]**; the leaf must say so in its own hand |
| needs q to drift with Nα | **[FAIL]** — no single quantum; the closed-loop rule is a coincidence of two points |

## Inputs the leaf may use

The He-4 mass and radius; the Kelvin-cell/sphere packing library in `models/nuclear_to_assembly/`; q = 2.42; Euler and the geometry of contact graphs. **Nothing else.** No shell model, no Weizsäcker terms, no α-cluster literature values for cluster shapes (the shape must come from the packing, or the test is reading the answer off the back of the book).

## Also owed, same spec, one line each

- **A = 5.** He-4 + one nucleon. Prediction from the closed-loop rule: the fifth capsid makes an open edge onto a closed tetrahedron, pays nothing, and Coulomb/inflation costs — **unbound.** He-5 and Li-5 are both unbound (fact). Trivial, and it is the first prediction the rule makes outside its two calibration points; record it.
- **Li-6, Li-7, Be-9, B-10, B-11.** The non-α-conjugate light nuclei: α + loose nucleons. Not this test — but the leaf should note what the *open* edges cost, since that is the next spec.

## Leaf plan (the Sonnet ritual)

One leaf per nucleus, spawned per `specs/README.md`, each reading this file and `three-term-binding.md` §4–§8 only. Each leaf's first commit is `tests/alpha-ladder/<nucleus>/README.md`: the packing it built, the edge count, the cycle count, then the prediction, then — last — the comparison. Leaves do not see each other's results until all fourteen are in; the hypervisor tabulates. Commits via Alexandria (`010`).
