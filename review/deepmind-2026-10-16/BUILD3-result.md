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
