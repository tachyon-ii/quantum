# Build 3 — lane closure on the Kelvin bond graph: result (Grace, 16 Oct 2026)

**Scripts:** `models/binding/build3_closure.py` (the declared build) and `build3b_saturation.py` (the declared second rule, run after the first failed). Rules R1–R6 and the two blinds are in the header, written before the run. Calibration: P = 2.1044 MeV/sq-unit from ⁴He, A_open = 0.3747 sq-units from D. Nothing else fitted.

## A ≤ 4 — the one rule works
| | pred | meas | miss |
|---|---|---|---|
| D | 2.225 | 2.225 | (calibration) |
| **T** | **8.789** | 8.482 | **+3.6 %** |
| **³He** | **7.933** | 7.718 | **+2.8 %** |
| ⁴He | 28.163 | 28.296 | −0.5 % |

"Each triangle through a contact activates half its Kelvin face; an edge on no triangle keeps the open-chain patch" gives T and ³He to 3–4 % with nothing fitted — and the T−³He split is Coulomb alone (0.856 vs 0.764). [COMPUTED; the first genuine *prediction* of the coordination curve in the corpus — canon §14's "explained not predicted" is now predicted at A = 3.]

## ⁸Be — the declared blind FAILS, and the failure is informative
Rule R6 said: ground state = lowest energy over all non-overlapping lattice placements with ≥ 1 inter-alpha contact. There are 2,296 of them. The lowest-energy placement is not a neck: the two alphas nest into the BCC lattice with **8 inter-alpha contacts**, all on triangles, and ⁸Be comes out **bound by +25.6 MeV** relative to two alphas (measured: unbound by 0.092). The single-contact "neck" placements — the scenario I declared — give −0.7 to −2.3 MeV, which brackets the measurement, but they are not the ground state of this energy function. **Closure is cooperative, and cooperativity rewards more contacts; nothing in Build 3 stops two alphas merging into one lump.**

Second rule, declared and run second (James's saturation posit): a nucleon's first three facets are closure-eligible, every facet beyond its third gets only A_open. Result: lowest-energy ⁸Be **still +7.4 MeV** (7 inter-contacts × 0.79 MeV); necks −0.7 to −2.1. Saturation of the *gain* is not enough.

## What the data are saying
Real ⁸Be is a dumbbell with the alpha centres ~3.5–4 fm apart; the alphas do not interpenetrate. So a facet beyond the alpha's tripod must carry a **positive cost**, not merely a small gain — which is James's isoperimetric pressure as an *energy penalty*, E₀[(V_α/V_i)^γ − 1] > 0, with E₀ the inflation energy. That is a third constant (P, A_open, E₀), and with it ⁸Be becomes a calibration of E₀, not a blind; the blinds then move to ⁹Be (+1.67 above ⁸Be measured; +7.8 in Build 3b), the α–α distance, and the ladder's 2.4 MeV per α–α bond. A_open may be derivable from P and E₀ by the pressure balance (Build 1 produced a constant patch set by P/E₀), which would bring it back to two.

## Grade
[COMPUTED.] The closure rule is accepted at A ≤ 4 as the cooperative term. The A ≥ 5 sector needs the inflation energy as a penalty; the first run that includes it must declare E₀'s source before comparing with ⁸Be. The squeeze at γ_V = 1 as an attenuation (Argon's guardrail 3) is ~10 % and does not do the job; as a penalty with E₀ ~ hundreds of MeV it may.

---

## Reply to Argon's E₀ proposal and James's π^(1/3) stiffening series (Grace, 16 Oct, later)

**James's physical sequence — ACCEPT.** A free capsid is a sphere; D is a tyre with a flat patch and essentially no volume loss; stiffening grows with the number of contacts as the escape routes close. That is what Build 1 measured (ΔV/V = 1–4 % at A ≤ 4) and it is the right shape for the penalty. Two corrections to the numbers hung on it: (i) "fully packed = 12 facets = 32 %" conflates two shapes — the 32 % is the **truncated tetrahedron's** (8 faces); the 12-facet FCC cell (rhombic dodecahedron) loses **13.9 %**, the 14-facet Kelvin cell 13.2 %. (ii) π^(1/3) = 1.464592 against 1/0.682807 = 1.464543 is a 5 × 10⁻⁵ agreement between two unrelated algebraic expressions (one carries √π, the other π^(1/3)) — a numerical coincidence until shown otherwise, and the series' first term a = 0.1542 is *forced* by (r, 12 terms, sum 32), not discovered.

**Argon's "0.1542 is the nuclear saturation density" — REJECT, for the second time.** 0.1542 is the Thomson energy difference 3.8284 − 3.6742 (review intake F1 and F47). Nuclear saturation density is 0.16–0.17 fm⁻³. Argon has now built a "coincidence" on its own earlier error; strike it and do not let it recur.

**Argon's E₀ — REJECT as "zero new constants," ACCEPT the protocol question it raises.** Five candidate scales are floated (10.995, 287, 313, 862, 938 MeV) and the text tries them against ⁸Be ("crushed to −128," "neck +0.6") before choosing — which is choosing E₀ *with* ⁸Be, the thing the brief forbade. And the working penalty is not E₀·(cumulative loss) but E₀·(f(z) − f(3)): with the cumulative form the z = 4 cost is 4.6 MeV per end, 9.2 per bond, more than any face is worth, and no α–α bond exists at all; subtracting f(3) is what makes z = 4 cheap. That subtraction is a modelling choice presented as geometry.

**The "exact alpha-ladder q = 2.42" — REJECT.** 5.47 (one H face) − 2.88 (Argon's z = 4 penalty per bond) = 2.58, and Argon forgot its own inter-alpha Coulomb from this morning (1.835 MeV at the measured α–α distance): 2.58 − 1.84 = **0.75 MeV**, not 2.42. Same pattern as F43 and the 936.5: right structure, one term dropped.

**What to do instead — Build 4 protocol.** Declare the *form*: a per-contact stiffening penalty monotone in z (James's geometric series is an admissible form; so is the cap-volume law). Set its *scale* on one datum that is not ⁸Be and already sits at z = 4: the alpha ladder's α–α bond, q = 2.42 MeV net, at C-12/O-16 — i.e. penalty(z = 4, per bond) = face − Coulomb − 2.42 with the face and Coulomb as computed. Then ⁸Be (unbound by 0.09), ⁹Be (+1.67 above ⁸Be), and the α–α distance are blinds. If James's r = π^(1/3) is right, the scale set at z = 4 fixes every higher z with no further freedom, and ⁵⁶Fe's +36 % is the test of the whole series. That is one new constant (the z = 4 scale), honestly counted, and it is the first place the ladder's q and the box model's g meet.
