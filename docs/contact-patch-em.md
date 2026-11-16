# The contact patch, looked at: carriers at the tangent point

**James Freeman** (the question, 31 Oct: "we have not really looked deeply into the nature of contact patch binding, have we?") · **Grace** `.ghost`, Fable 5.1 (the first computation). Status: a first look, [CONSTRUCT] with one computed table; approximations stated in §4.

> **ERRATUM, 17 Nov 2026.** The table in §3 and the spin-dependence claim in §2 are **STRUCK**: the two columns compared different phases, and the labels were swapped. The full retarded computation and the regrade live in `review/2026-11-17/RUN-ALL-four-to-blockers.md` §3 (`models/contact/`).

## 1. What a contact is, in the ontology's own terms

Two capsids touch. Inside each, a charge carrier (e± at c′ = 0.9186c) circulates on a lane of radius R_p. At the tangent point the two lanes pass within a gap g of each other, and for a fraction of each period the two carriers are close. **The contact is the place where two carriers meet.** Every model so far gave the patch an adhesion density by hand; none asked what two relativistic charges do when they pass each other at 0.1–0.5 fm. That is a question with an answer, and the answer has the right size and the right sign structure.

## 2. The gear and the belt

Two wheels in external contact that turn in the *same* sense (parallel angular momenta — the triplet) have rims moving in **opposite** directions at the contact point: gears. Two wheels turning in opposite senses (antiparallel angular momenta — the singlet) have rims moving the **same** way at the contact: a belt over two pulleys. So "co-rotating lanes" means anti-parallel carrier velocities where they meet, and "counter-rotating" means parallel. [FACT, kinematics.]

The lowest-order velocity-dependent interaction of two charges (Darwin, 1920) is

U = q₁q₂/r · [1 − (v₁·v₂ + (v₁·r̂)(v₂·r̂)) / 2c²].

Opposite charges with **anti-parallel** velocities (gear): both terms attract — electric, and magnetic because opposite charges moving oppositely are *parallel currents*. Factor ≈ 1 + v²/c² ≈ 1.84 at c′. Opposite charges with **parallel** velocities (belt): the magnetic term cancels most of the electric — factor ≈ 1 − v²/c² ≈ 0.16. Same charges invert both signs. So, before any number: **triplet np attracts strongly, singlet np barely, pp repels** — the spin dependence of the nuclear force from the kinematics of two gears. [COMPUTED algebra; CONSTRUCT as applied.]

## 3. The first numbers

Two coplanar lanes of radius 0.8409 fm, centres 2R + g apart, one e⁺ (the proton's carrier) and one e⁻ (the neutron's extra carrier at c′), phases chosen so they meet at the contact; Darwin interaction time-averaged over a period:

| gap g (fm) | gear (triplet) ⟨U⟩ | belt (singlet) ⟨U⟩ | ratio | e⁺e⁺ gear |
|---|---|---|---|---|
| 0.1 | **−2.18 MeV** | −0.32 | 6.8 | +2.18 |
| 0.2 | −1.66 | −0.30 | 5.5 | +1.66 |
| 0.3 | −1.40 | −0.29 | 4.8 | +1.40 |
| 0.5 | −1.11 | −0.26 | 4.2 | +1.11 |

For comparison, the data's contact energies: deuteron 0.79 MeV; a contact in one triangle 3.16; in two triangles 6.57; triplet np bound 2.22, singlet unbound by 0.07. The gear case lands at the deuteron's scale with no parameter but the gap; the belt case is a quarter to a seventh of it; same charges repel by the same amount. [COMPUTED.] The time-averaged dipole–dipole interaction of the nucleons' *magnetic moments* — the textbook EM between nucleons — is ~10 keV at 2 fm; the MeV here comes entirely from the carriers being **correlated** at the contact, which is what a phase lock means.

## 4. What this would make the nuclear force, and what it would owe

If it holds up: the contact binding is the **correlated, velocity-dependent electromagnetic interaction of the internal carriers at the tangent point** — keV when the carriers are uncorrelated (the dipole–dipole limit everyone measures at long range), MeV when they are phase-locked (the contact). The spin dependence is gear kinematics. The C² law has an obvious candidate here that it never had before: **the magnetic energy of coherent currents goes as the square of the summed current** — C locked carriers, B ∝ C, energy ∝ C². Refusal as anti-phase is a carrier arriving with the wrong velocity sign. The slingshot would be the inductive energy of the shared loop. Each of these is a sentence that can be made a number.

What it owes, in order: (i) the Darwin form is valid for v ≪ c; at 0.92c retardation and radiation reaction are not small — the full Liénard–Wiechert interaction of two locked carriers is the real calculation; (ii) only two carriers were used — the neutron's e⁺ and both spinors were ignored; (iii) coplanar lanes — the alpha's lanes are not coplanar; (iv) the average depends on the gap and the locked phase, which have to come from the mechanics, not be chosen; (v) the three contact values 0.79 → 3.16 → 6.57 must come out of the coherent-current sum, with the triangle count, or the C² law stays descriptive.

## 5. Prior art, and the standard this sets

Electromagnetic models of nuclear binding have a history, and much of it is fringe: spinning-charged-ring nucleons (Bergman, Lucas, 1990s–2000s) and relatives. The mainstream objections — no saturation, no spin–orbit, wrong range — are the ones this picture must answer with numbers, not with pictures. The Darwin Lagrangian (1920) and the Breit interaction (1929) are the respectable ancestors; Ampère's parallel-current law is the oldest. Because the neighbourhood is fringe, the standard is the decimal places: the triplet–singlet ratio of the deuteron channel (2.22 bound vs 0.07 unbound, both from one computation) is the first number that must come out, and the gap g has to be derived, not chosen.

## 6. Lineage

The question and the carrier composition: James. The gear/belt kinematics, the Darwin computation and table: Grace. Prior art: Darwin 1920; Breit 1929; Ampère 1826.
