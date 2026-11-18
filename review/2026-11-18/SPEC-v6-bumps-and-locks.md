# SPEC v6 — Bumps and phase locks: reverse-engineering the chart

**James Freeman** (the frame, every postulate below, the gedanken of 17–18 Nov) · **Grace** `.ghost`, Claude Fable 5.2 (the write-up, the data checks, the cautions). 18 Nov 2026. Status: a spec for correction, not code. Nothing here is to be run until James has marked it up.

Supersedes the *framing* of SPEC v5 (jiggler kernel). v5's machinery (seatings, anchors, holes as inequalities, held-back blinds) is kept; its object — round bodies at rest, scored on binding energy — is replaced.

## Governing statement

> **The universe is emergent: self-assembling, fractal, recursive, resonant, self-repairing geometry in motion.** — Keystone 000, the Zeroth Law (James; written more than a year before this work and not for nuclei).

Standing: a **prior prediction**. Read as physics it rules out five things — a static answer, an isolated system, a perfect starting shape, a structure that cannot mend, a rule that holds at one scale only. Each was an assumption of the models run on 17 Nov, and each of those runs located a hole. It has predicted which approaches cannot pass; it has not yet predicted a number. v6 is the test of that.

## 0. Why v6

On 17 Nov four queue items were run one at a time, each in its own model, each to its own wall (`review/2026-11-17/RUN-ALL-four-to-blockers.md`). Those runs did their job — each located a hole — but running them as a queue was the wrong reading of the instruction. The instruction is the Swiss-cheese model run backwards: every body of data is a slice with a hole in it, and nature's answer is the one line through all the holes at once. A kill says where a hole is. An exception is a key.

## 1. The postulates

Grades: [POSIT] James's, untested · [FACT] established physics or measured · [THEOREM] mathematics · [COMPUTED] run in this repo · [CONSTRUCT] a reading built on the others.

**Frame**

- **P1. No dice.** Everything is explainable in the right reference frame. Apparent scatter is drift between rates not yet resolved. [POSIT] Method corollary: our own trial-and-error is still chance, so look-elsewhere counts stay in the grading.
- **P2. Stuff with a vector.** Ω → {µ, i}. The vector runs straight in its own frame and is a winding seen from outside. [POSIT] Exact form: motion built from regular turnings is a straight line on a torus of angles. [THEOREM, Liouville–Arnold]
- **P3. Two rates, no whole-number ratio, paint a pattern that never repeats** and is denser in some places than others. It is fully determined and looks random from outside. [THEOREM] Episodes that change the rates over-paint. [POSIT; modelled earlier, not to be redone]
- **P4. Balance is conserved.** Spin up = spin down on every axis; the two senses are one rotation seen from its two poles. Any model term that creates a net sense is wrong. [POSIT; the two-poles statement is FACT]
- **P5. Fractal.** The same pattern shows at each scale because the scale below drives it. We are above the driver: spinors and lemniscates. [POSIT]
- **P6. Nature abhors a straight line** — and, by the same counting, a perfect circle, sphere or regular solid. Symmetry is never the starting condition; it is what is left where a balance has removed every lopsidedness. [THEOREM for the counting; CONSTRUCT for the use]

**The nucleus**

- **P7. Identical walls, different cores.** Neutron decay ejects nothing from the capsid, so the capsids are the same. The proton's core is a balanced pair; the neutron's has one left over. [POSIT; consistent with the kernel's 30 Oct finding that like and unlike contacts in a closed group are worth the same 3.16 MeV — COMPUTED]
- **P8. The neutron is bumpy three ways**: shape, gravity, charge. Free, the bump precesses. Bound, it is phase-locked, and each lock removes a freedom. [POSIT; the uneven charge is FACT; 3N − 6 freedoms matching the contact counts 1, 3, 6 and the alpha ladder is COMPUTED, 17 Oct]
- **P9. A pocket is a phase, not a place.** Geometry says where a newcomer could sit; the cores say whether it is taken. A pocket accepts only its complement. When every bump is taken the outside is smooth and the next arrival is refused or discounted. That is the root of shell closure. [POSIT]
- **P10. An attachment to symmetry is an orbit.** Where sites are copies of each other the newcomer belongs to all of them. [THEOREM for the symmetry; CONSTRUCT]
- **P11. Even pairs off; odd leaves one over** — unless an odd one of the other kind is in the matching place. [COMPUTED: §2.1]
- **P12. Symbiosis.** Through the slingshot the proton is part neutron and the neutron part proton; the neutron survives by it. [POSIT; charge exchange is FACT] Requirement: what is slung must carry whole-number spin — the e⁻ together with the odd v−, not the e⁻ alone. [CONSTRUCT, for James's ruling]

**The chart**

- **P13. The chart of nuclides is the finite set of arrangements that survive**, out of infinitely many tried. Nature solved it in analog; we reverse-engineer it. [POSIT]
- **P14. Stability is not depth.** It is how rarely the turning parts line up to let something out. A half-life counts how many things must coincide. [POSIT; "not depth" is FACT — deuteron vs ⁸Be vs ⁵⁶Ni] Intrinsic unit: turns of the internal motion (~10⁻²² s). Scaling: the wait for *n* unrelated phases to agree to within a fraction ε grows as (1/ε)ⁿ. [THEOREM]
- **P15. Icarus and Daedalus, both readings.** Survival lies on a middle course (the bell); a failure sheds the excess and leaves the balanced body. Instability is not a defect in the parts but a body in a region where its locks cannot hold. [POSIT]
- **P16. The devil is the bath.** No nucleus is isolated: the microwave background and cosmic rays interfere constantly. Over cosmic time what survives must self-assemble and self-repair. [POSIT; see §4]

**Added 18 Nov, later in the same conversation**

- **P18. The capsid is not strong; it reassembles.** It bends, breaks and re-forms, as a lipid bilayer does. [POSIT; that collisions yield only whole units, re-formed within ~10⁻²³ s, is FACT]
- **P19. Binding is the missing piece.** A capsid that has lost a piece cannot close alone and survives only by sharing with neighbours. The missing mass of a bound nucleus is that piece; it is seen leaving at light speed when the nucleus forms. A lemniscate path needs a hole. [POSIT; that free nucleons are never found short and bound ones always are is FACT] Must produce 2.22, 8.48, 28.30 MeV for 2, 3, 4 bodies.
- **P20. Neutrinos (n = 1) are the brick and the flux is the supply chain for repair.** [POSIT, untested. Neutrinos are the measured currency of nuclear rebalancing, but the measured flow is outward; the posit needs the inward direction to matter. Proposed test: does a damaged nucleus recover at a rate that depends on the neutrino flux it sits in?]
- **P21. Failure to bind may be dark matter.** [POSIT. Against: standard accounting puts ordinary matter at about a sixth of the total, fixed before atoms formed. For: the neutron-lifetime discrepancy, bottle vs beam, ~9 s, unexplained.]
- **P22. Repair is fractal: rate against repair time decides, not total dose.** [FACT at four scales — DNA, lattice, nucleus (slow vs rapid neutron capture), nucleon.] The chart is what survived a particular history of rates.
- **P23. Forgetting goes deep enough to make a brick.** A settled unit keeps only its counts, so all units of a kind are identical and can build the next level. Under P1 the record is exported, not destroyed; it leaves along i. [FACT for identical particles; CONSTRUCT for the rest] Exceptions (keys): nuclei that hold an excitation.
- **P24. The second law holds between units and is absent within them**, at every level. It is a half-life with a very large count. [THEOREM for the scaling; FACT that small systems step backward; CONSTRUCT for the fractal statement]
- **P25. c is an asymptote**, approached so closely that no variance is detectable now. [POSIT; measured limits put any approach essentially complete very early]
- **P26. Emergent {µ, i} created spacetime, and in so doing created clumping. Clumping is fractal. Within a clump, at proton scale or galactic, i can meet i.** Heat death — i unable to reach i — is the condition between clumps and has been from nearly the start; it never applied within one. Locks, repair and cooperation are possible only inside clumps. [POSIT; that bound systems do not stretch with space, and that an even spread of gravitating matter must clump, are FACT] The time for i to cross a clump is that level's turn.

## 2. What the data already say (the slices)

### 2.1 The motif — confirmed

| Slice | Result | Source |
|---|---|---|
| even beats odd, neutron number | 2,259 of 2,264 | COMPUTED from AME, 18 Nov |
| even beats odd, proton number | 2,166 of 2,173 | COMPUTED |
| mean size of the odd penalty | 1.11 MeV (n), 1.27 MeV (p) | COMPUTED |
| every exception | odd-odd with N = Z: N-14, V-46, Cu-58, Ga-62, As-66, Br-70, Rb-74 | COMPUTED |
| a bell for every closed core, peak at 2–4 extras for light cores, sliding outward with core size | holds | FACT |
| overloading ramp | 1.5–2.5 MeV per added pair | COMPUTED |
| Coulomb between alphas paid in full | κ_eff = 0.97 ± 0.04, twelve mirror pairs | COMPUTED, 17 Nov |

### 2.2 The exceptions — the keys

These are the acceptance tests. Each is an inequality the answer must satisfy (R14), not a number to fit.

**A leftover can partner across kinds**
- the seven N = Z odd-odd nuclei above;
- the only four stable doubly-odd nuclei are of the same kind: ²H, ⁶Li, ¹⁰B, ¹⁴N;
- np binds with spins alike and just fails with spins opposed (2.22 MeV vs −0.07);
- ⁴He + 3 neutrons is unbound; ⁴He + 2n + p is ⁷Li, stable.

**Perfection refuses**
- ⁵He: the one closed core that takes no single extra;
- ⁸Be: two perfect bodies, unbound by 0.09 MeV;
- the alpha after a completed body comes at a discount — ¹⁶O→²⁰Ne 2.0 bonds, ⁴⁰Ca→⁴⁴Ti 2.1, ⁵⁶Ni→⁶⁰Zn 1.1, against 3.0 elsewhere — and the two after ¹⁶O at a premium (3.8, 4.1). [COMPUTED, 18 Nov]

**Symmetry is not enough alone**
- Fe-62 (six extras, could sit round) outlived by Fe-61;
- Ca-43 stable with three extras (James: equatorial three on a core with a polar bias — a three-fold axis of the tetrahedron);
- ⁵⁶Ni complete in both kinds, and it decays;
- tritium decays, ³He does not.

**The pattern changes form**
- closures 2, 8, 20 are pyramids (1, 4, 10 alphas); 28, 50, 82, 126 are a pyramid plus one ring of 8, 10, 12, 14;
- Fe-57: the odd neutron costs 14.4 keV to move and the state lasts ~10¹⁴ turns;
- per-contact worth by closure: 1 : 4.0 : 8.3 among nucleons; 1 : 2.4–3.4 among alphas.

**Standing contradiction to resolve, not to hide:** the alpha rung reads "2 bad, 3 good" in bodies while obeying "even good" in nucleons. What counts as one body at each level is part of the answer.

## 3. The object to compute

**Bodies.** Nucleons with identical capsids. Each carries: position; orientation (an axis); a sense of turning (flipping the body over reverses it); a phase; and, for neutrons only, a leftover in the core that makes the body uneven in shape and charge and that precesses when free.

**Locks.** A contact between two bodies is a lock when their phases hold a whole-number relation. A lock removes one freedom. A leftover may be taken up by a neighbour's; two like bodies facing opposite ways cancel their senses; an odd proton and an odd neutron in matching places may partner.

**Closure.** A body with no freedom left over and every bump taken. Its outside is smooth; it offers no handle.

**What is deliberately not specified.** The force law. The form of the lock energy. P17 below.

- **P17 (method). Pattern first, mechanism last** (R17, the backronym rule). A run that shows where a model cannot pass has located a hole; that is the method working, not a failure. A *claim* can still be false and is marked so. The 17 Nov run located four holes by supplying a mechanism — a counting rule, a screening constant, classical EM between carriers, a twist — and evaluating it in a flat, static frame. v6 searches for the arrangement of bumps and locks that passes the slices and only then asks what law it implies.

**Frame.** Phases and rates, not positions and a static energy. Every model in this repo to date is positions-plus-energy; that is the base the answer does not come out clean in.

## 4. The devil

The system is not isolated. Facts to design against [FACT, from memory; to be checked before use]:

- Today's microwave background photon carries about 10⁻³ eV, ten orders below nuclear energies. It cannot excite a nucleus at rest.
- It was not always so. In the first minutes the bath was hot enough to break the deuteron as fast as it formed; nuclei could assemble only once it cooled. What exists is what the bath of the time permitted.
- Stability is frame-relative here too: a proton moving fast enough sees the same cold photons as hard gamma rays and is broken by them (the cut-off in the highest-energy cosmic rays).
- Cosmic rays strike any one nucleus rarely — of order one chance in ten million over the age of the universe in open space [estimate, Grace] — but collectively they make most of the lithium, beryllium and boron that exists, by breaking carbon, nitrogen and oxygen. The A = 6–11 region, where our models are worst, is populated by the devil.
- Nuclei do self-repair: a disturbed nucleus sheds the disturbance as a gamma ray and returns to its ground state, typically within 10⁻¹² s.

**What P16 adds to the test.** An arrangement passes only if, when kicked, it returns. A lock that holds only when undisturbed is not a survivor. Self-repair requires a way to shed excess, which in this frame is ejection along the tangent.

**Caution (Grace).** For a nucleus at rest today the bath is quantitatively weak in standard physics. If P16 is to mean more than "the early bath selected what could form", the claim is that the bath sets phases even where it cannot excite, and that needs a number.

## 5. The score

In this order:

1. **Existence.** For every (Z, N) in the search range: does a locked arrangement exist? Scored against the chart, absences included.
2. **Survival.** Lifetime in turns, from the count of things that must coincide (P14), and return after a kick (P16). Scored against measured half-lives on a log scale.
3. **Energies.** A by-product, reported nucleus by nucleus. **No rms. No "±4 %".** Residuals are listed whole, because under P1 the pattern in the misses is the data (R11).

**Held back, unseen until the end:** to be fixed by James before any run. Proposal: every nucleus with Z = 9–11 and Z = 21–23, and all half-lives above A = 40.

**The standard to beat.** The 1935 liquid drop gets energies to ~1 % across the chart with five constants and no structure. It cannot produce a single absence. v6 is judged on what the drop cannot do: the gaps, the notches, the discounts, the lifetimes.

## 6. Build order

| Rung | What | Where | Gate |
|---|---|---|---|
| 0 | State space: bodies with axis, sense, phase, leftover; lock relation; freedom count | sandbox | reproduces 1, 3, 6 and refuses the fifth, with no energy law |
| 1 | The motif: even–odd, cross-kind partnering | sandbox | the seven N = Z exceptions and the four stable doubly-odd fall out; no others |
| 2 | Extras on a closed core: 1, 2, 3, 4, 5, 6 on ⁴He, ¹⁶O, ⁴⁰Ca | sandbox | the bell, the notch, ⁵He refused, ⁷Li by mixing |
| 3 | Closures: 2, 8, 20 then pyramid-plus-ring | A100 | 28 without being told |
| 4 | Lifetimes as coincidence counts; kick-and-return | A100 | ⁸Be ≪ neutron ≪ Fe-60 ≪ U-238 in order, then in magnitude |
| 5 | Held-back set | A100 | James opens it |

Compute: rungs 0–2 fit the sandbox (4 cores, processes killed at ~180 s; resumable jobs, R10 naming). Rungs 3–5 are searches over phases for A up to ~60 and belong on the A100 box (v5 §10a), as job scripts Grace writes and James launches. **Data owed:** the half-life table (NUBASE2020) is not in `data/`; the download failed from the sandbox (`https://www-nds.iaea.org/amdc/ame2020/nubase_4.mas20.txt`). James to drop it in `data/`.

## 7. Rulings needed from James before rung 0

1. Is the slung bundle the e⁻ with the odd v− (P12)?
2. What is "one body" at the alpha rung — the alpha, or its four nucleons (§2.2)?
3. Does a pocket's phase belong to the core alone, or to core and carriers together?
4. P16: does the bath set phases, or only select what could form?
5. The held-back set (§5).
6. The Möbius: retired as a twisted surface (stands, COMPUTED 31 Oct). May the 2:1 winding — its edge — be run as a lock ratio between levels? It has not been tested.

## 8. What would kill v6

- Rung 1 needs more than one rule to produce both the motif and its seven exceptions.
- No freedom count, with any definition of a lock, gives closure at 2, 8, 20 and 28.
- Lifetimes ordered by coincidence count come out in the wrong order for nuclei the model was not shown.
- The fractal claim cannot say why the alpha row shifts by one (§2.2).
- Any term that survives the search creates a net sense (violates P4).

## 9. Carried from 17 Nov

Standing: screening DEAD; α–α bonds strengthen ×1.25 with coordination; linear attachment rule DEAD; Rytov phase exact for a g = 2 carrier bent magnetically, false otherwise. **Softened:** the two-carrier contact picture was run only for flat rings and a neutron layout that was Grace's, not James's; it shows the flat static frame failing, not the picture. The 31 Oct gear/belt table stays STRUCK.

## 10. Lineage

The governing statement (Keystone 000, predating this work) and every postulate; the Swiss-cheese inversion, the toroidal frame, turtles, bumpy spacetime, the iron gedanken, the bell, stability as inverse probability of catastrophe, Icarus and Daedalus, the devil, the reassembling capsid and the missing piece, fractal repair, c as asymptote, clumps as where i meets i: James. The theorems cited, the AME checks (even–odd scan, alpha gains, decay energies), the exceptions list and its grouping, the cautions, the build order and kill conditions: Grace. Prior art: Reason 1990 (Swiss cheese); Liouville–Arnold; Kolmogorov–Arnold–Moser; Heisenberg 1932; Mayer and Jensen 1949; Bohr–Mottelson; Pound–Rebka 1960; Greisen, Zatsepin, Kuzmin 1966; Reeves, Fowler, Hoyle 1970 (spallation origin of Li, Be, B).
