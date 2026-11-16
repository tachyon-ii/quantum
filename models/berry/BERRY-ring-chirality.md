# The ring, the half-wavelength, and chirality — the geometric phase computed

**James Freeman** (the posits, 31 Oct: half-integer wavelengths round the ring so the second pass is out of phase with the first; A and M precess in opposite senses) · **Grace** `.ghost`, Fable 5.1 (the computation). Code: `tangent_phase.py` (+ the inline runs recorded below). Status: the solid angles are [COMPUTED]; the mapping to spin-½ and to matter/antimatter is [CONSTRUCT] on top of standard results (Rytov 1938, Vladimirskii 1941, Pancharatnam 1956, Berry 1984, Tomita–Chiao 1986).

## 1. What was computed

For a closed path r(t), the tangent T(t) traces a closed curve on the unit sphere. A wave carried round the path acquires a geometric phase equal to s·Ω, where s is its spin and Ω the signed solid angle enclosed by T's curve (Rytov–Vladimirskii–Berry; measured for light by Tomita and Chiao in a helical fibre, rotation = solid angle). Ω was computed as a fan of spherical triangles from the mean tangent direction (unique mod 4π), checked against parallel transport of a normal vector (Bishop frame holonomy, which gives Ω mod 2π), and validated on the planar circle.

## 2. Results

| closed path | Ω/π | spin-½ phase/π | spinor (antiperiodic)? | handed? |
|---|---|---|---|---|
| planar circle | 2.000 | 1.000 | **yes** | no (mirror = itself) |
| planar figure-eight | 4.000 (≡ 0) | 2.000 (≡ 0) | **no** — periodic | no |
| tetra "seam" (4 lobes alternating ±z, D2d, achiral) | 2.000 | 1.000 | yes | no |
| its mirror image | −2.000 | −1.000 ≡ 1 | yes | — (same element) |
| single-twist wound ring, k = 1, amplitude 0.15, right-handed | **−2.001** | −1.000 | **yes** | **yes: Ω < 0** |
| same, left-handed | **+2.001** | +1.000 | **yes** | **yes: Ω > 0** |
| double-twist wound ring, k = 2 | ∓2.134 | ∓1.067 | approximately | yes |
| (3,1) torus curve, amplitude 0.3 (strongly chiral) | ∓3.505 | ∓1.753 | **no** | yes |
| (4,1) torus curve, amplitude 0.3 | ∓4.869 | ∓2.434 | **no** | yes |

## 3. What it says

1. **A ring is a spinor.** For the planar circle the tangent sweeps a great circle, Ω = 2π, and a spin-½ wave comes back with phase π — sign-flipped after one turn, restored after two. James's "1.5, 2.5, 3.5 wavelengths round the circumference" is this: the half-integer is not imposed on the ring, it is what the ring's own geometry does to the wave's frame. [COMPUTED + FACT (Berry)]
2. **A planar figure-eight is not.** Its tangent turns +2π on one lobe and −2π on the other; Ω ≡ 0; the wave is periodic. The lemniscate as a *planar* curve cannot carry spin-½. The lobes must leave the plane. [COMPUTED]
3. **An achiral ring has no handedness to offer.** The tetra seam and its mirror give Ω = ±2π — the same spinor element — and the planar circle is its own mirror. No chirality in the net phase. [COMPUTED]
4. **Chirality and exact spin-½ coexist for exactly one class: a ring with a small single twist.** The k = 1 wound ring and its mirror give Ω = ∓2π to 0.05 % — both exact spinors — and they are distinguished by the **sign of Ω**: the sense in which the wave's frame precesses round the path. That is the posit "A and M live in their own universe and precess in opposite directions," as a computed property of two enantiomeric paths. [COMPUTED; the A/M mapping is CONSTRUCT]
5. **Strong chirality breaks the spinor.** Once the twist carries real torsion (the torus curves), Ω leaves 2π — 3.5π, 4.9π — and the phase is no longer π: the wave does not come back antiperiodic. A matter/antimatter ring cannot be arbitrarily twisted and remain spin-½. The small-twist case is the only one that is both handed and half-integer, and its deviation from exactly 2π grows with the twist amplitude (k = 2: 2.13π, a 7 % detuning) — a geometric origin for a "not quite" of the kind we keep meeting. [COMPUTED]

## 4. Consequences in the ledger

- **The Möbius conjecture, re-read.** A geometric half-twist of a surface would correspond to a path carrying ~2π of torsion; the relation Ω = 2π − ∮τ ds (checked here on the achiral cases, noisy on the chiral ones) then gives Ω ≈ 0 — *periodic*, spin-1-like. The surface half-twist was the wrong object for spin-½; the right one is the **sign of the geometric precession on a nearly planar ring**. The retirement of the geometric Möbius stands, and this is the reason.
- **The gear has an origin.** Two enantiomeric rings (Ω = +2π and −2π) brought to a tangent point have counter-moving frames at the contact by construction — the gear kinematics of `contact-patch-em.md` §2 is what two opposite-handed spinor rings do when they touch, not a choice of rotation sense.
- **The split makes one of each.** A boundary that divides a ring's path into its two handednesses produces Ω = +2π and −2π in equal measure — equal matter and antimatter, both spinors, as the day's first posit required.

## 5. Owed

> **17 Nov 2026:** the massive-carrier item is discharged — exact for magnetic bending with g = 2, false otherwise. See `review/2026-11-17/RUN-ALL-four-to-blockers.md` §4 (`bmt.py`).

The phase s·Ω is the photon's (Rytov) law; its use for a massive spin-½ carrier is an analogy to Fermi–Walker/Thomas transport that has to be made exact. The quantisation of the twist (why k = 1 and small, what sets the amplitude) is the dynamics, not the geometry, and is the same owed item as "what makes the mutual term 2" in the C² dive. Numerics: Ω is determined mod 4π by the fan method; the torsion integral is unreliable near inflection points (the (3,1) a = 0.1 row was discarded for that reason).

## 6. Lineage

Half-wavelength rings, "do waves precess," A/M as opposite precession: James. The identification with the Rytov–Berry phase, the table, the planar-figure-eight exclusion, the small-twist class, and the Möbius re-reading: Grace.
