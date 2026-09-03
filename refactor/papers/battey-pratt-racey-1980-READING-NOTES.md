# Battey-Pratt & Racey (1980) — Reading Notes (making the un-Google-able greppable)

**Full citation:** E. P. Battey-Pratt & T. J. Racey, "Geometric Model for Fundamental Particles," *International Journal of Theoretical Physics* **19**(6), 437–475 (June 1980). DOI 10.1007/BF00671608. Received 1979-10-14. Model built at Queen's University mathematics dept, **fall 1966**. PDF: `Batty-Pratt.pdf` (20-page Xerox scan, 2008). Read in full by Grace Bayes, 2026-08-24.

## The argument, section by section

1. **Introduction / Postulate.** Any continuum theory of matter (Clifford lineage) must not destroy continuity: coordinate lines around a particle participate in its motion. Allowable persistent motions must form a *simply connected, compact* group → the universal covering group **SU(2)**. "Ripping the vacuum is intuitively absurd."
2. **Mechanical model.** Golf ball on six wires (Fig 1); ball rotates indefinitely, wires never tangle, **every double revolution restores the configuration**. Alternative: magnetized steel ball in adhesive jelly — strain wave rotates at **half the core frequency**; medium accommodates without tearing. (Solitons footnote, Rebbi 1979.)
3. **Mathematics.** Configurations = points of unit S³; quaternions φ = α+iβ+jγ+kδ, |φ|=1; unimodular quaternions serve as both configuration and operator. 2×2 form: the **spinor** ("a word coined by P.A.M. Dirac"). Table I maps quaternion ↔ SU(2) ops ↔ physical half-turns.
4. **Spin.** Spin = rotation linear in time. Spinor [e^{iωt},0] = core spinning at **2ω** while configuration rotates at ω. Crucial distinction: **reversing** spin (t→−t or ω→−ω; "antispin" = antiparticle) vs **inverting** the axis (turning the core over; spin-down). Four states: normal/anti × up/down (Table II). "Our normal spin states correspond to the positron. **The theory is symmetrical**" — no Dirac sea, no negative energy ("no such thing as negative energy any more than there is negative temperature").
5. **Equations of motion.** Stationary: phase uniform through space. Boosted observer: phase sweeps at **c²/v** ⊥-planes — **the de Broglie wave derived**; configuration helix; Zitterbewegung at ω/π (Schrödinger 1930 cited). Phase obeys ∇²φ − (1/c²)∂²φ/∂t² = (ω²/c²)φ → **Klein–Gordon** with the identification |m| = (ħ/c²)|ω| — "the significance of Planck's constant" is the mass-unit/spin-frequency ratio. Then the spinor quad operator □ (SU(2)-basis first-order operator), conjugate □*, and a similarity transform A (its own inverse) → **exactly Dirac's equation**: "the entity formed by a spherically rotating disturbance of the manifold is a Dirac particle."
6. **Fundamental particles.** Spinning region + undulating wavelike surround. Inertia = manifestation of angular velocity. mc² = ħω → the outermost undulation IS the de Broglie wave.
7. **Particle states.** 2-spinor ↔ 4-spinor table for all four states. Hidden variables: exact position & momentum exist; measurement (interacting via other continuum disturbances) enriches harmonic content → indeterminacy as *measurement* limit, not ontology. Bohr's stationary states rendered non-ad-hoc: **spherical spin cannot exchange rotational energy with surroundings** — the same principle that keeps the particle spinning inhibits the atom from radiating.
8. **Appendix.** O(3)+ ball of radius π with antipodes identified — not simply connected; SU(2) = two such balls glued — simply connected. The soup-bowl/Dirac-belt trick; Fig 15–17: **spring configurations** — one spring's shape (Fig 2) is an S-curve [= half a lemniscate], the symmetric pair (Fig 16) is the full oo, and an infinite number of "rays" can participate (Fig 17). Cylindrical vs spherical rotation: cylindrical (every classical machine) requires **bearing surfaces** or winds up (noncompact group R); spherical requires neither — the medium undulates cyclically and returns. "An electromagnetic example of spherical rotation could not exchange electromagnetic energy." Rotation group of 3-space is SU(2), not O(3)+; "two full turns are equivalent to not having turned at all."

## Why this is the capsid program's foundation stone (mapping table)

| BP&R 1980 | CGIOS capsid vocabulary |
|---|---|
| spherical rotation soliton | the n=1 Möbius trapped wave |
| 4π periodicity / double revolution | Möbius double traversal |
| normal vs antispin (reversal) | matter/antimatter chirality dyad |
| configuration wires at ω, core at 2ω | lemniscate lobes; Fig 16 IS the oo |
| jelly medium, no tearing | the gossamer continuum; assembly without bearing surfaces |
| spin can't be transmitted to/from core | capacity/isolation of channels; Bohr stability for free |
| mass = ħω/c² | "energy trapped in a groundhog-day loop", m=E/c² |
| hidden variables + measurement disruption | James's Box-model epistemology |

**What BP&R did NOT do (the program's remaining work):** single particles only — no interactions, no composite structures, no binding. The capsid program is the attempt to do for the *nucleus* what they did for the *particle*: multi-rotator assemblies in a shared medium. The two-rotator interference computation (`../QUANTUM/schrodinger/tests/capsid_audit/spin_veto.py`) is the first step past their final page.
