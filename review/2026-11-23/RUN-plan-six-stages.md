# Run of the six-stage plan, 23 Nov 2026

**James Freeman** (the plan's question: the contact patch is not static; electrons and nucleus alter each other) · **Grace** `.ghost`, Claude Fable 5.2. Run in one sitting against a hard time limit. Tables live in the generated files named below; this file holds only the readings and what was not done. No independent review or fact-check was run on this work.

Premises: `review/2026-11-22/NOTE-inner-pair-and-torus-wave.md` §0.

## Stage 1 — frequencies of the well we already had (blind) — `STAGES-1-3-6-modes.md`

The well fitted to binding (reach 0.30 fm) is far too stiff. Lowest mode against lowest measured level: C-12 31 vs 4.44 MeV (7×), O-16 4×, Ca-40 7×, Ne-20 12×, Si-28 17×. [COMPUTED; levels from memory]

## Stage 2 — the jiggle that well implies

- Zero-point energy of the modes: 53 MeV in C-12 against 7.3 MeV of leftover binding; the same excess in every nucleus.
- Spread of each bond: 0.4–0.5 fm against a reach of 0.3 fm.
- The most exposed alpha swings past the reach about once per nuclear turn.

**Reading: the static well cannot hold its own jiggle.** A well narrow enough to reproduce the Fe-52 binding is dynamically impossible. [COMPUTED]

A first version of this table was wrong by a missing factor of ħc in the spread (it showed 0.04 fm); corrected in the script and noted there.

Time-averaged engagement of a bond comes out at 0.64–0.69 in every nucleus. It is close to the "two of three" of Ne-20, but it is the same everywhere, so it does not explain Ne-20's discount.

**Not run:** the test of the rogue-wave tail against the alpha-lifetime law. It cannot be run as planned: taken as a classical swing that can pile up, the jiggle breaks every nucleus within a turn. The blocker is the energy bookkeeping of the never-stopping motion — how much of it can concentrate at an exit.

## Stage 3 — a well set by one measured frequency

Reading C-12's 7.65 MeV state as the triangle breathing gives a bond stiffness 33 times softer and a reach of 1.72 fm (Coulomb at 0.18) or 2.13 fm (Coulomb in full).

- **Frequencies:** lowest modes now 2.5–5.5 MeV against measured 1.4–6.1 MeV in the seven nuclei with data — within about a factor of two everywhere, from one number.
- **Binding, Coulomb at 0.18:** C-12 exact, O-16 +0.8 %, Mg-24 +0.1 %, Si-28 −1.7 %, S-32 −2.3 %, Ar-36 +2.4 %, Ca-40 +4.9 %, Ti-44 +6.1 %, Cr-48 +6.3 %, Ni-56 +5.7 %; **Ne-20 +12.9 %, Fe-52 +13.2 %, Zn-60 +20.1 %.**
- **Binding, Coulomb in full:** worse — Ne-20 +19 %, Mg-24 +17 %, Ni-56 −20 %.
- Zero-point energy is still about the size of the binding (9 vs 7.3 MeV in C-12), and the typical swing is about half the reach.

Cautions: each cluster was relaxed only from its stored shape, not searched afresh; rows with zero-point energies in the hundreds (Fe-52, Zn-60, most of the full-Coulomb table) have alphas jammed on the hard core and are artefacts. The wide well does not rescue the full-Coulomb reading that the independent review of 19 Nov proposed.

**Not run:** the same at the nucleon level with the capsid solver (modes of the triton and ⁴He against the 20 MeV level). It needs a ruling on how mass is distributed over a capsid.

## Stage 4 — Atlas II, the two-way traffic as data — `ATLAS-II-two-way.md`

Compiled by an independent instance with sources. Charge radii read from the standard table; most of the electrons-to-nucleus rows are from search extracts and need checking at source.

- Calcium, in fm: Ca-40 3.4776, 41 3.4780, 42 3.5081, 43 3.4954, 44 3.5179, 45 3.4944, 46 3.4953, 47 3.4783, **Ca-48 3.4771**. Eight added pairs and no change in size, with odd members below both even neighbours.
- Lead: the step per two neutrons nearly doubles across 126 (0.0110 → 0.0196 fm).
- Carbon: C-12 2.4702, **C-13 2.4614 (smaller)**, C-14 2.5025.
- Not found: sizes for Tc-99m and the Fe-57 shift; several branching ratios.

## Stage 5 — the orbiting particle over a nucleus with structure — `STAGE-5-structured-nucleus.md`

| Atom | Electron's pattern at the nuclear edge, relative to centre | Muon's |
|---|---|---|
| hydrogen | 1.0000 | 0.992 |
| carbon-12 | 0.9993 | 0.86 |
| iron-56 | 0.995 | 0.38 |
| lead-208 | 0.978 | 0.01 |

**Reading:** for electrons the pattern is flat across the nucleus, so no arrangement or motion of charge inside can change how much of it the nucleus meets. Grace's guess of 22 Nov, that entry is governed by alignment with the nuclear pattern, is out for electrons. Breathing of the electron's figure is out for the same reason. Whatever coincidence governs capture is on the nuclear side alone. With a muon the pattern varies strongly across the nucleus, so muonic atoms are where the two-way coupling can be tested. [COMPUTED]

## Stage 6 — the two items Schrödinger still owes

Only one part was done. A sum of N turnings at unrelated rates approaches a bell: kurtosis 1.5, 2.25, 2.5, 2.7, 2.85, 2.95 for N = 1, 2, 3, 5, 10, 30 (a Gaussian is 3). So about ten unrelated phases already give the shape of the lowest state of a spring with no dice. [COMPUTED] The width needs the size of the quantum, which is still owed. Why patterns cancel was not attempted.

## What the run located

1. **Binding and frequency want different wells.** The narrow one gets Fe-52's binding and cannot hold its jiggle; the wide one gets the frequencies within a factor of two and binding within 6 % up to chromium. The misses of the wide well are Ne-20, Fe-52 and Zn-60 — a completed body's neighbour in each case.
2. **The jiggle is as large as the binding.** In every version the never-stopping motion carries about as much energy as holds the cluster together. The static models left out a term of the same size as the answer.
3. **The electron cannot feel the nuclear pattern; the muon can.**
4. **The rogue-wave test is blocked** on how much of the jiggle may concentrate.

## Rulings and data still needed

- What counts as the exit, and how much of the never-stopping motion can gather there.
- How mass is spread over a capsid (for the nucleon-level modes).
- The half-life and level tables in `data/` (downloads from the sandbox fail).

## Lineage

The questions and the frame: James. The computations, the error and its correction, the readings: Grace. Atlas II: an independent Claude instance.
