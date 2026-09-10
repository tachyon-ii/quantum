# Three-term binding — can constructs with no fudge constants reach 2, 7, 8, 28?

**James Freeman (posits) · Neyman (quantum) (tables, grades), 2026-09-08. §8–§9 rebuilt by Grace `.ghost` 2026-09-08 (surgery below).** Generator: `models/three_term_binding.py` — every numeric table below is its output; the script is the artefact, this file is the reading. Status: **[CONSTRUCT — un-promoted shelf]**. Nothing here crosses the wall.

> **Surgery, 2026-09-08 (witnessed).** The old §8–§12 — a least-squares three-term solve, a per-lane/per-patch fit, and a ten-column enumeration — were **deleted**. Three constants on four points is not a test; that machinery was the Standard-Model reflex (fit to the magic numbers) the wall exists to refuse. §0–§7 stand. §8 is the honest forward model that replaces them: one free scale, geometry does the rest, no `lstsq` in the generator. **Second pass 2026-09-09 (Fable, reviewing the Opus-hat first pass):** the first pass held the round patch to one size and so declared a "structural" gap at T/He3 — an SM-shaped conclusion. Under the trough (not surface tension — §8b) the patch is not one size: it grows with the number of neighbours pressing the balloon. That fixes T/He3 inside 1% with no new integer (§8c). It also retired James's de-spin term unilaterally; that is undone — held, not retired. Field-orthogonality notation unified to **V ⊥ M** (see §4).

## 0. The ontology — read Φ first, it is not repeated here

The chain this document rests on — Ω → Φ{μ,i} → {m,l,s} → {E,F} → V⊥M →
Universe — with Ω, μ, i and the antecedents m, l, s, is stated **once**, in
`Φ-a-minimal-ontology-of-an-emergent-universe.md` §1–§3. This file used to
restate it; that copy was cut 2026-09-10 (DRY — two copies drift, one is
canon). Read Φ §1–§3, then start at §4 below. Symbols used from here on are in
the nomenclature.

## 4. Nomenclature

| symbol | name | what it is | grade |
|---|---|---|---|
| **Ω** | the singularity | undifferentiated potential; no distinction, no information | posit |
| **Φ** | | the first distinction: something localised going somewhere; Φ = {μ, i} | posit |
| **μ** | the agent of capture | a Möbius loop: closed, one-sided, captures one discrete unit of what Ω delivers | conjecture 0 |
| **i** | direction | a literal *this way* vector; information's minimal unit is its pairing with μ | posit |
| **m, l, s** | mass, length, time | ontological antecedents, not units: localisation, displacement, change | derived from Φ |
| **E, F** | energy, force | E = mc², F = ma — definable only once {m,l,s} exist | derived |
| **V ⊥ M** | orthogonal fields | electric ⊥ magnetic, always. **V** (not E) names the electric field so E stays free for energy in E=mc²; **M** (not B) is house style. This is the canon's E⊥B. | fact |
| | | …and are two shadows of one Möbius trap | conjecture 0 |
| **spacetime** | | Ω → time ⊥ space | james |
| **now** | | processing i in space | james |
| **CoCi** | the front — *Coordination Curve i*, pronounced "cocky" (the boss rooster; the pastoral holder of the now) | where the past intersects the now to create the future recursion back to now. It *is* the UPU. Ruled 2026-09-09 | james — RULED |
| **UPU** | Universal Processing Unit, U³ | a massive, distributed, in-memory analog computer: takes the last universe as input, outputs the next, recursively. Operates in the now; manages the past → now → future recursion loop. Neo's matrix, realised as fractal recursive physics | james — RULED |
| **Universe** | | the printout | — |
| **c′** | the orbital fraction | the fraction of c at which a free lepton circulates inside its capsid. **One number for the universe**, unknown; tabulated, not fitted | geometry |
| **lane** | | a shared lepton path threading n capsids; an n-lemniscate, written `oo`, `ooo`, `oooo` | geometry |
| **Y, Yₙ** | slingshot | energy a lepton sheds slowing from c′ to c′/n on an n-lane: Yₙ = mₑc²[γ(c′) − γ(c′/n)] | conjecture 1 |
| **y** | | lepton count in lanes: p = e⁺, n = e⁺e⁻ ⇒ y = p + 2n | integer |
| **patch** | | one capsid–capsid contact face | geometry |
| **round patch** | | an *unpacked* contact: balloons touching, area π/4 of a square. Packed (He4, 100% Kelvin packing) the contact is the whole square and the hexes are hexes | geometry |
| **A** | patch quantum | binding per patch, "squish and stick", posited flat-and-perfect with Zipf-like fall-off beyond contact | conjecture 2 |
| **a** | | patch count = edges of the bond graph | integer |
| **leg** | | a capsid vertex off the plane of the first three (He-4 has one; the "tyre spike") | geometry |
| **Q** | leg quantum / capsid spin | energy released when a capsid's spin is locked by the cluster (Newton III on the lepton–capsid pair) | conjecture 3 |
| **q** | | count for the Q term. **Three readings tried:** bonded baryons; out-of-plane legs; dimension | integer |
| **loose cannon** | | an unpaired e⁺ in circulation (all others in e⁺e⁻ pairs): **H 1, D 1, T 1, He3 2, He4 0** — He-4's two balance each other. **Bounded by the T/He3 split:** T − He3 = 0.764 = U_pp + c ⇒ c = 0.764 − U_pp ≈ 0 for a point-charge Coulomb; < 0.2 MeV for any spread charge | james; bounded |
| **inflation** | | carriers in circulation inflate the capsid; the second carrier costs m_n − m_p − m_e = 0.782 MeV | fact |
| **loop** | | a closed bond cycle (triangle, tetrahedron; not a line): 0, 1, 1, 1. The one integer T has and D lacks | geometry |
| **U_pp** | Coulomb | e²/(4πε₀·2R_p), two proton cores in contact; **computed, not fitted** | fact |

Lane order by geometry (ruled 2026-09-08): D = `oo`; T, He3 = `ooo`; He4 = `oooo` — a tetrahedron is four-lobed and from any lobe the world looks the same.

## 5. Meet the players

Composition per the capsid model (`lepton-theory-v4`): a central antineutrino spinor, the charge carriers, and a capsid. Masses, radii and spins are CODATA/AME (fact). Contacts are what `models/nuclear_to_assembly` finds by automatic bond discovery when the capsids are truncated octahedra (Kelvin cells, 14 faces: 6 squares S, 8 hexagons H); anything unbound is a sphere.

| player | spinor | e⁺ | e⁻ | capsids | mass MeV | radius fm | spin | contacts (S-S, H-H) | lanes |
|---|---|---|---|---|---|---|---|---|---|
| **p** | 1 | 1 | 0 | 1 | 938.272 | 0.8409 | ½ | 0 | — |
| **n** | 1 | 1 | 1 | 1 | 939.565 | 0.86 (magnetic; charge r² < 0) | ½ | 0 | — |
| **D** | 2 | 2 | 1 | 2 | 1875.61 | 2.128 | 1 | 1 (1, 0) | oo |
| **T** | 3 | 3 | 2 | 3 | 2808.92 | 1.759 | ½ | line 2 (2, 0) · triangle 3 (1, 2) | ooo |
| **He3** | 3 | 3 | 1 | 3 | 2808.39 | 1.966 | ½ | line 2 (2, 0) · triangle 3 (1, 2) | ooo |
| **He4** | 4 | 4 | 2 | 4 | 3727.38 | 1.678 | 0 | cross 6 (2, 4) · ring 4 | oooo |

### 5a. Bond data, generated (`models/nuclear_to_assembly/gen_players.sh` → `players/`)

| assembly | A | Z | N | contacts | NP | PP | NN | S-S | H-H | orth links | shear | curvature | closed loop | bad phase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| d2 | 2 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0.0 | 0 | 0 |
| h3_linear | 3 | 1 | 2 | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0.0 | 0 | 0 |
| h3_orth | 3 | 1 | 2 | 2 | 2 | 0 | 0 | 2 | 0 | 1 | 0 | 0.0 | 0 | 0 |
| h3_tri | 3 | 1 | 2 | 3 | 2 | 0 | 1 | 1 | 2 | 0 | 0 | 0.3 | 1 | 1 |
| he3_linear | 3 | 2 | 1 | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0.0 | 0 | 0 |
| he3_orth | 3 | 2 | 1 | 2 | 2 | 0 | 0 | 2 | 0 | 1 | 0 | 0.0 | 0 | 0 |
| he3_tri | 3 | 2 | 1 | 3 | 2 | 1 | 0 | 1 | 2 | 0 | 0 | 0.3 | 1 | 1 |
| he4_cross | 4 | 2 | 2 | 6 | 4 | 1 | 1 | 2 | 4 | 1 | 0 | 0.6 | 1 | 3 |
| he4_ring | 4 | 2 | 2 | 4 | 4 | 0 | 0 | 4 | 0 | 4 | 1 | 0.0 | 1 | 1 |

Kelvin-cell contacts are the *a* of the formula. Each nucleus's JSON, PNG and score are in `players/`; regenerate, never hand-edit. (`he4_ring` shipped with a duplicated constraint — `P2:S-X–N2:S-X` — that the discovery step re-added as `S+X`, printing 5 contacts for a 4-ring; fixed in `library.py`.)

**Why He-4 is the cliff, seen not argued (James, 2026-09-08):** two deuterons crossed. In the cross every capsid touches the other three — six faces in contact, four of them hexagons — where two separate deuterons had one square each. The jump from ~16 (T + He3, or 2×8) to 28 is that packing. The truncated octahedron is a rough approximation of the truth; it got very close with a two-term bond model. The real model needs three: an unbonded proton capsid must entrain, must spin, must precess; when it bonds it loses one degree of freedom. That lost freedom is the de-spin term — still fluffy, and written down as such.

**The 4?? — answered by the tool.** `he4_cross` auto-discovers **6 contacts**: 4 NP (2 S-S + 2 H-H), 1 NN (H-H), 1 PP (H-H). Every cell touches every other: the tetrahedron. Your 4 is the NP count; the NN and PP faces are also in contact. The ring variant has 4 (S-S only, no hexagon in contact). For A = 3 the shipped library only had lines (2 contacts); a triangle of Kelvin cells closes around one edge (S-S + H-H + H-H, dihedrals 125.26° + 125.26° + 109.47° = 360°), so I added `h3_tri` and `he3_tri` — 3 contacts each. Triangle or line for A = 3 is now a buildable choice, not an assumption.

Run the visualizer (matplotlib PNG; `viz3d` needs a display and `trimesh`):

```
cd ~/cgios.ai/QUANTUM/models/nuclear_to_assembly
python3 -m nuclear_to_assembly.cli.toasm build he4_cross -o he4_cross.json
python3 -m nuclear_to_assembly.cli.toasm score he4_cross.json
python3 -m nuclear_to_assembly.cli.toasm viz he4_cross.json --out he4_cross.png --title "He-4 cross"
python3 -m nuclear_to_assembly.cli.toasm viz3d he4_cross.json
cd -
```

Nuclei: `d2 h3_linear h3_orth h3_tri he3_linear he3_orth he3_tri he4_cross he4_ring`. (`cli/toasm.py` shipped with an unresolved git merge conflict and would not import; resolved toward the `library`/`builder` side, whose modules exist. `h3_orth` was built P-N-P, i.e. He3 — fixed to N-P-N.)

## 6. The binding formula

$$
\boxed{
\begin{aligned}
&\quad \\
&\bm{\qquad BE = \underbrace{y\,Y_n}_{\text{slingshot}} + \underbrace{a\,A}_{\text{capsid patch}} + \underbrace{q\,Q}_{\text{capsid de-spin}} - \underbrace{PP\,U_{pp}}_{\text{Coulomb}} \qquad} \\
&\quad
\end{aligned}
}
$$

where

* $Y_n = m_e c^2\,[\gamma(c') - \gamma(c'/n)]$, per lepton on an $n$-lane; $n$ = capsids threaded (D 2, T/He3 3, He4 4); $c' \le 0.9534$ from §7;
* $y$ = leptons that slow — **open**: one per capsid ($y = A$: 2, 3, 3, 4) or all charge carriers ($y = p + 2n$: 3, 5, 4, 6);
* $A$ = one quantum of binding per contact face, pivoting on how much face is in contact — the patch term is where the energies pivot;
* $a$ = contact *area* in square units: unpacked contacts are round, π/4 each (D 0.785; T, He3 3×0.785); packed He4 is 2 whole squares + 4 hexes (hex = 2.598 by geometry, ≈5 by the envelope);
* $Q$ = capsid de-spin — **TBA**; the one no-fudge candidate is the spin-½ shell rotation $3 m_p c^2/256 = 10.995$ MeV (§7);
* $q$ = its count — **open**: out-of-plane legs (0, 0, 0, 1) is the only reading that survives A ≤ 4 (§9);
* $U_{pp} = \alpha\hbar c / 2R_p = 0.856$ MeV, PP = proton–proton contacts.

| nucleus | lane | y (one/capsid) | y (all) | a (line) | a (tri/tetra) | PP | q (legs) | BE data |
|---|---|---|---|---|---|---|---|---|
| D | oo | 2 | 3 | 1 | 1 | 0 | 0 | 2.2246 |
| T | ooo | 3 | 5 | 2 | 3 | 0 | 0 | 8.4818 |
| He3 | ooo | 3 | 4 | 2 | 3 | 1 | 0 | 7.7180 |
| He4 | oooo | 4 | 6 | — | 6 | 1 | 1 | 28.2957 |

## 6a. Back of the envelope — the two-term first pass (James, 2026-09-08)

One unit for a slingshot, one unit for a square contact, a hex worth 5 squares:

```
D    1 slingshot + 1 square                    =  2
T    3 slingshot + 3 square                    =  6      (He3 the same, less Coulomb)
He4  4 slingshot + 2 square + 4 hex (= 20)     = 26
data 2.2  /  8.5, 7.7  /  28.3
```

Recomputed with the unit taken from D (u = 2.2246 / 2 = 1.112 MeV) and the hex from He-4:

```
D    2u          = 2.225   (fixed)
T    6u          = 6.674   data 8.482   −21%
He3  6u − U_pp   = 5.818   data 7.718   −25%
He4  6u + 4h     = 28.30   ⇒ h = 5.41 = 4.9 u     (the "5×" is exact by construction)
```

With the round-patch correction (§7, T9) — D's contact is π/4 of a square, He-4's squares are whole — the same envelope gives u = 1.246 and He-4 = 19.6 (hex from geometry, 2.598) or 31.5 (hex = 5): the two hex values bracket 28.3, and T/He3 do not move, because they are round too.

What the envelope shows: the *shape* is right with two terms and one unit. What it cannot do: T/D. With T's counts exactly 3× D's, T/D = 3.00 whatever the unit; the data say 3.81. That 21% is not a constant — it is a count T has and D lacks (§10, items 6–8).

## 7. The slingshot chunk — the keeper table

Per lepton, MeV. Release = energy shed = binding contributed. Struck: oo > 2.2246/2, excluded by D (two leptons slow, glue not negative). Admissible **c′ ≤ 0.9534**.

| c′ | γ(c′) | E @ c′ | E @ c′/2 | oo | ooo | oooo | lim | D 2.224 − 2·oo |
|---|---|---|---|---|---|---|---|---|
| **0.800** | 1.667 | 0.852 | 0.558 | 0.294 | 0.321 | 0.330 | 0.341 | 1.636 |
| **0.820** | 1.747 | 0.893 | 0.560 | 0.333 | 0.362 | 0.371 | 0.382 | 1.560 |
| **0.840** | 1.843 | 0.942 | 0.563 | 0.379 | 0.409 | 0.419 | 0.431 | 1.467 |
| **0.860** | 1.960 | 1.001 | 0.566 | 0.435 | 0.468 | 0.478 | 0.490 | 1.354 |
| **0.880** | 2.105 | 1.076 | 0.569 | 0.507 | 0.541 | 0.552 | 0.565 | 1.211 |
| **0.900** | 2.294 | 1.172 | 0.572 | 0.600 | 0.637 | 0.648 | 0.661 | 1.024 |
| **0.920** | 2.552 | 1.304 | 0.576 | 0.728 | 0.767 | 0.779 | 0.793 | 0.768 |
| **0.940** | 2.931 | 1.498 | 0.579 | 0.919 | 0.960 | 0.972 | 0.987 | 0.387 |
| **0.950** | 3.203 | 1.637 | 0.581 | 1.056 | 1.098 | 1.110 | 1.126 | 0.113 |
| ~~0.960~~ | ~~3.571~~ | ~~1.825~~ | ~~0.582~~ | ~~1.243~~ | ~~1.286~~ | ~~1.299~~ | ~~1.314~~ | ~~−0.260~~ |
| ~~0.980~~ | ~~5.025~~ | ~~2.568~~ | ~~0.586~~ | ~~1.982~~ | ~~2.027~~ | ~~2.041~~ | ~~2.057~~ | ~~−1.739~~ |

**If a single row of this table does not fit T, He3 and He4 near perfectly once the other two terms are in, we have a problem.** That is the test, registered here.

## 8. The three-ratio forward model (rebuilt 2026-09-08; corrected 2026-09-09)

The insight that survives §6a: **one free scale and the rest is geometry.** No
least squares. Two mechanisms plus computed Coulomb carry A ≤ 4 —

$$
\boxed{\;\; BE \;=\; \underbrace{s\,Y(c',n)}_{\text{slingshot (\S7)}} \;+\; \underbrace{\text{area}\cdot P}_{\text{contact}} \;-\; \underbrace{PP\cdot U_{pp}}_{\text{Coulomb}} \;\;}
$$

The **de-spin term $qQ$ of §6 is not invoked at A ≤ 4** — it is not needed to
reach the cliff. It is *held, not retired*: James's three-term posit stands (an
unbonded capsid must entrain, spin and precess; bonding removes one degree of
freedom), and A ≥ 5 is where it would first be asked for. What is dropped is
only the old §8's menu-picked $Q^* = 11$ MeV coincidence.

**The three ratios** (the spine James set, 2026-09-08):

$$
\text{circ} : \text{square} : \text{hex} \;=\; \tfrac{\pi}{4} : 1 : \tfrac{3\sqrt3}{2} \;=\; 0.785 : 1 : 2.598
$$

D, T, He3 touch as **balloons** — a *round* contact patch per face. He4 is the
only A ≤ 4 assembly that **packs** (truncated-octahedron Kelvin cells, 100%
space-filling): its faces are forced *whole* — 2 squares + 4 hexes = 12.392
square units. **Packing is the cliff.** Square and hex are arithmetic (hex =
2.598, no freedom). circ is the one geometric unknown — and §8c is about the
fact that it is not one number.

$U_{pp} = \alpha\hbar c / 2R_p = 0.856$ MeV, computed. $c'$ is the one free
scale, tabulated in §7, bounded above by D ($c' \le 0.9534$).

**Calibration — one datum, one posit.** D = 2.2246 split 50:50 (James's start):
slingshot 1.112 + patch 1.112. The slingshot leg fixes $c' = 0.9534$; the patch
leg fixes circ·P for a single contact.

### 8a. Scenario A — one round patch, circ = π/4 for every unpacked contact

| nuc | pred | data | err |
|---|---|---|---|
| D | 2.225 | 2.225 | −0.0% |
| T | 6.801 | 8.482 | **−19.8%** |
| He3 | 5.945 | 7.718 | **−23.0%** |
| He4 | 21.364 | 28.296 | **−24.5%** |

All low, all by about a fifth. Two-term-flat (no hex, no packing) could not get
He4 past ~6; **packing + hexes already carry it from 6 to 21.** What is left is
the assumption that every round patch is the same size.

### 8b. The trough, stated correctly (was "the Laplace lever")

A balloon's contact is not the naive π/4 disc. What sets it is **not surface
tension** (James, 2026-09-09) but an *interference trough*: the capsids are
Majorana matter/antimatter pairings, one minute to midnight from annihilation,
and two of them sit at the one separation where their waves interfere to a
low-energy state. Closer, they annihilate — smurfed with extreme prejudice.
Farther, they are unbound — a neutron has 880 s to live. They oscillate about
that separation; James calls it the *smurf distance* and suspects it is the real
core of the Planck length [POSIT]. The Laplace-like part survives as a
*balance* — a curvature/pressure equilibrium — but the restoring force is
interference, not tension. The contact patch is the region held at the trough,
and it depends on how hard the balloon is pressed — **how many neighbours press it.**
The first pass asked only "what deflation puts He4 on data?" and got ×1.39
(π/4 → 0.563) and called the cause surface tension. That number is right but it answers a narrower question than the
right one. The right question is §8c.

*(Correction, 2026-09-09.)* The first pass wrote: "if the derived deflation is
not ~1.4 the patch mechanism is wrong." **That was mis-aimed.** The patch
mechanism — contact area ∝ binding, whole faces when packed — is constructive
geometry and is not what a Laplace derivation tests. What it tests is the
*attribution*: whether the trough — interference at the smurf distance —
accounts for the sizes below. Fail
that and the sizes are still what the data require; only their cause is open.

### 8c. Scenario B — the patch grows with coordination number

Anchor $P$ on He4's whole faces (with D's split): $P = 1.976$ MeV per square
unit. Then D's single contact — coordination 1 — is **0.563**. Now ask what
round patch T requires, and, *independently*, what He3 requires (He3 carries a
computed Coulomb term T does not):

| coordination | who | patch (sq-units) | how obtained |
|---|---|---|---|
| 1 neighbour | D | **0.563** | D's split, P from He4 |
| 2 neighbours | T | **0.847** | required by T |
| 2 neighbours | He3 | **0.862** | required by He3 — *independent of T* |
| 3 neighbours | He4 | **1.000** square · 2.598 hex | whole faces, packed |

**T and He3 agree to 1.8 %** — and (Neyman, 2026-09-09, correctly) that is *not*
a new check: T and He3 share one geometry and differ only by computed Coulomb,
so the 1.8 % is the old T−He3 = 0.764 vs U_pp = 0.856 split (0.092 MeV) spread
over three patches. Real, consistent, and the same test as before. What is new
is only that the coordination reading *absorbs* it without a fit. Take the one coordination-2 patch
= 0.854 and every nucleus is inside 1 %:

| nuc | pred | data | err |
|---|---|---|---|
| D | 2.225 | 2.225 | 0.0% |
| T | 8.528 | 8.482 | +0.5% |
| He3 | 7.672 | 7.718 | −0.6% |
| He4 | 28.296 | 28.296 | 0.0% |

The sequence is **monotone in coordination: 0.56 → 0.85 → 1.00** as neighbours
go 1 → 2 → 3. A balloon touched by one neighbour barely kisses it; pressed by
two it flattens further; packed by three the face is whole. **One mechanism, no
missing integer.** The first pass's "T/D = 3.00 is structural" held every round
patch to one size; *that assumption*, not the geometry, was the error — and it
was a Standard-Model-shaped error (one fixed quantum per bond).

### 8d. What it says — measured apart from concluded

**Measured.**
- Three unknowns ($P$, patch₁, patch₂) on four points leave one check — and it is
  the T/He3 Coulomb split, restated (1.8 % ≡ 0.09 MeV). Not independent evidence
  for coordination.
- Patch area is monotone in coordination: 0.56, 0.85, 1.00.
- The slingshot is a saturating per-contact quantum (§7); one free scale $c'$;
  the 50:50 split pins it at its ceiling 0.9534.

**Concluded.**
1. **The cliff is packing.** He4 is the one assembly whose faces are whole (12.4
   sq-units vs 0.56 for D's single kiss). No de-spin quantum needed to reach 28.
2. **The middle is coordination, not a count** [POSIT — consistent at A ≤ 4,
   untested]. T and He3 sit where a two-neighbour balloon puts them, and nothing
   is a fit to a magic number — but with three numbers on four points,
   coordination has *explained*, not *predicted*. Its first test is A ≥ 5.
3. **This is not yet a prediction of a new nucleus.** It is a coherent
   description of four with three numbers and one passed check. Prediction starts
   at A ≥ 5, where one nucleus mixes coordination numbers.
5. **Fission and fusion, in this picture** [POSIT, James 2026-09-09]. Both are
   *triggered annihilation*: compression pushes matter/antimatter capsids past
   the trough — either a direct capsid–capsid reaction, or the tokamak rails
   distort and the orbiting e⁺/e⁻ strikes the Majorana core. Not a new force;
   antimatter meeting matter, on cue. Registered here, untested; a leaf's
   question once the trough is derived.
4. **Caution on $c'$.** The 50:50 posit is at the boundary. A lighter slingshot
   share lowers $c'$ and raises $P$; the coordination curve rescales but keeps
   its shape. $c'$ is one honest free scale sitting on a wall, which is a flag,
   not a result.

## 9. Next steps — in order; test registered before the physics

1. **Derive the coordination curve from the trough** [OWED — the front, CoCi]. Not
   surface tension: model two capsid wavefunctions and find the separation at
   which interference is a minimum (closer → annihilation, farther → unbound);
   then the contact area of a balloon held at that separation and pressed by
   1, 2, 3 equal neighbours. Compare to **0.56 → 0.85 → 1.00**.
   Hits with no knob → the attribution is earned. Misses → the sizes stand (they
   are what D, T, He3, He4 require) and the *cause* is open. Either way the patch
   geometry is untouched. `models/trough_patch.py`, test README first. Survivorship framing (James): what
   exists is what sits in the trough; CERN's zoo is the transients that don't.
2. **Move $c'$ off the wall** [OPEN]. The 50:50 split is a start, wrong on purpose.
   Tabulate the split and watch the coordination curve: if 0.56/0.85/1.00 is
   robust across splits, it is geometry; if it moves, it was leaning on $c'$.
3. **First prediction, A = 5–7** [UNBUILT]. Declare bond graphs and coordination
   numbers for ⁶Li, ⁷Li, ⁸Be, ⁹Be from the tool — *before* looking at AME — and
   predict with $P$, patch(coord), U_pp as above. ⁸Be is the cheapest kill: two
   balanced tetrahedra, zero loose cannons, should be over-bound if the loose
   cannon is a cost, and it is **unbound by 92 keV**. Failing run on the record
   first. Leaf model: Sonnet 4.6 (arithmetic on declared integers).
4. **Hold $qQ$** for A ≥ 5. Do not retire James's term on A ≤ 4 evidence.

Ruled by James, 2026-09-09: the front is **CoCi** (§4); A = 3 triangle and A = 4 tetrahedron are *ruled*.

*Grade of this document: [CONSTRUCT]. One datum-fixed scale, one computed
Coulomb, one computed shape ratio (hex), one consistency check that is the T/He3 Coulomb split restated (Neyman's catch, 2026-09-09 — coordination itself is untested until A ≥ 5), and one named-and-owed mechanism (the trough, by coordination) whose
derivation fixes the attribution, not the geometry. No least squares. The cliff
is packing; the middle is coordination; nothing crosses the wall.*
