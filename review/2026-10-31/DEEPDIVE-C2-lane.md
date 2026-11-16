# Deep dive — the C² law: form, unit, mechanism

**Grace** `.ghost`, Claude Fable 5.1 — 30/31 Oct 2026, at James's "dive into it, take as long as it takes." Target: item 3 of the 30 Oct ledger — the law at the centre of everything that survived, E_lane ∝ C², which had no mechanism. Everything graded; the one thing claimed as a result is an identity, and it is stated with its margin.

## 1. The form — which law, exactly

Contact energy = BE − A·Y(2) + mesh·n_singlet + Coulomb (lattice), for the four fused lanes:

| | C | contact energy (MeV) | /0.788 |
|---|---|---|---|
| D | 1 | 0.788 | 1.00 |
| T | 3 | 7.18 | 9.1 |
| ³He | 3 | 7.38 | 9.4 |
| ⁴He | 6 | 28.0 | 35.5 |

Candidate laws against the two ratios (9.1, 35.5): **C²** → 9, 36 ✓; triangular C(C+1)/2 → 6, 21 ✗; C^{1.5} → 5.2, 14.7 ✗; 2^{C−1} → 4, 32 ✗; carriers² (3, 5, 6 carriers) → 2.8, 4 ✗; carriers × contacts → 5, 12 ✗. **The data choose C² and nothing adjacent to it**, and they choose *contacts*, not carriers. [COMPUTED]

That last point kills one of the two mechanisms left standing on the 30th. A Venturi binding — pressure removed in every gap a lane threads — scales with the gaps (linear) or with carriers × gaps (1 : 5 : 12). Neither is the data. **Venturi: DEAD.** Coherence is the only candidate left, and §4 says what it has to mean.

## 2. The unit — what 0.788 MeV is

g₁ = BE(D) − 2Y(2) = 0.7884 MeV. The neutron's β-decay Q-value is Q_β = m_n − m_p − m_e = (γ − 1)·m_e = **0.7823 MeV**, with γ = (m_n − m_p)/m_e = 2.531 the same γ that fixes c′ in the slingshot. Ratio g₁/Q_β = **1.0078**. [COMPUTED]

So the single-contact lane energy is, to 0.8 %, **the kinetic energy of the neutron's extra carrier at c′** — the energy that β-decay would release. Written out, the deuteron's binding energy becomes a formula in three masses:

BE(D) = m_e [3γ − 1 − 2γ₂],  γ₂ = 1/√(1 − (c′/2)²)  → **2.2185 MeV vs 2.2246 (−0.27 %).** [COMPUTED identity]

and the deuteron's protection against β-decay — the margin by which its neutron cannot decay — is BE(D) − Q_β = 1.442 MeV against the slingshot 2Y(2) = 1.436 (+0.4 %). **The contact pays the carrier's kinetic energy; the slingshot is the protection.** "The nucleus solves for prevention of neutron decay" (19 Oct) is this equation. [COMPUTED; the reading is CONSTRUCT]

## 3. The law with its unit — A ≤ 4 from masses alone

BE = A·Y(2) + Q_β·C² − E_mesh·n_singlet − E_Coulomb, with Y(2) and Q_β from (m_n, m_p, m_e), E_mesh = g₁ + 0.066 from the np singlet (the one datum), Coulomb at the lattice H distance √3·R_p:

| | C | predicted | measured | miss |
|---|---|---|---|---|
| D | 1 | 2.218 | 2.225 | −0.27 % |
| T | 3 | 8.341 | 8.482 | −1.7 % |
| ³He | 3 | 7.352 | 7.718 | −4.7 % |
| **⁴He** | **6** | **28.339** | **28.296** | **+0.15 %** |

[COMPUTED] No fitted constant. The (T, ⁴He) pair sits at (8.34, 28.34) against nature's (8.48, 28.30) — on the Tjon line to within the line's own width, which neither of the saturating lane forms of 19 Oct managed. The ³He miss is the lattice Coulomb (0.99 at 1.456 fm) plus the known T/³He asymmetry beyond Coulomb; it is the one number here that a better contact distance would move.

## 4. The mechanism — what C² has to mean

E = Q_β·C² = Q_β·C + 2Q_β·C(C−1)/2. Read as a sum over contacts: **each contact has self-energy Q_β, and every pair of contacts in the same lane has mutual energy exactly 2Q_β.** A mutual term equal to twice the self term is the signature of complete coherence — N in-phase dipoles radiate as N² for the same reason, the cross terms being 2× the diagonal. In one line: **E = Q_β·|Σ_contacts e^{iφ_k}|², all φ_k equal.** The contacts of a fused lane are not six bonds; they are six in-phase sources of one mode, and the mode's energy is the square of their sum. [CONSTRUCT — this is the form the data force; the dynamics that produce it are owed]

Two consequences follow from the form alone, both already seen in the record:

- **Species does not matter inside a fused lane.** The kernel's 30 Oct table found g(same-species, c = 1) = g(np, c = 1) = 3.16 on its own; the alpha's pp and nn contacts count in C = 6. In a coherent sum there is no "np bond" and "pp bond" — only phases. The mesh penalty is then what a singlet pair costs *outside* the coherent sum, which is how it enters above. [CONSISTENCY]
- **Refusal is anti-phase.** A contact that cannot lock contributes amplitude with the wrong sign: (C − |a|)² < C². An intruder on a closed alpha does not add a weak bond — it *reduces* the coherent sum, which is why He-5 is unbound rather than weakly bound. The Tacoma failure of 19 Oct is this sign. [CONSTRUCT]

What is owed and I will not pretend to have: the dynamics that make C contacts share one phase and make the mutual term exactly 2Q_β. It is not a surface (30 Oct, foam) and not pressure (§1). It is a phase. The lane's own equation of motion is the next thing, and it has a number to produce: 2.

## 5. The unit one rung up, and the attachments

- α–α bond q = 2.425 = **3.10 Q_β**. A closed α–α bond is worth three carrier-KE units — a triangle's worth, as noted on the 19th in deuteron units; now in the decay unit.
- Attachments onto closed lanes (19 Oct table): ⁶He 1.2, ⁶Li 1.9, ⁷Be 2.0, ⁹Be 2.1, ⁷Li 3.1 — in units of Q_β: 1.25, 1.88, 2.03, 2.13, 3.16. Integers within the lattice-Coulomb noise. [COMPUTED; CONJECTURE that they are integers]
- The cluster model of 30 Oct (closed lanes as bodies, Q_β·C² each, open attachments at Q_β) gave ⁶Li, ⁷Li, ⁷Be at −2.5 … −3.7 % by hand. With the unit now fixed to Q_β it loses its last free number.

## 6. What would kill it

- The identity g₁ = Q_β is a coincidence if the same unit fails to appear where the law predicts it: the α–α bond at exactly 3Q_β (it is at 3.10 — the 3 % is the test's resolution, not yet a kill); the attachment quantisation; and above all **⁶Li and ⁷Li from the cluster rule with Q_β fixed**, which are now predictions with zero freedom.
- The coherent form predicts that *any* contact added in phase to a fused lane of C gives (C+1)² − C² = 2C + 1 units — 7Q_β = 5.5 MeV for a seventh contact on the alpha's lane — and that none is available, because carriers = contacts closes it at 6. If a bound A = 5 existed, this would be dead. It doesn't.
- The 0.8 % and 0.27 % residuals are either Coulomb/recoil bookkeeping or the end of the identity; they are the decimal places this programme has been saying it must eventually earn.

## 7. Lineage

The posit that the nucleus solves for preventing neutron decay, and the carrier composition P = {spinor, e⁺}, N = {spinor, e⁺, e⁻} whose extra e⁻ at c′ is the unit: James (19 Oct). The three-term binding's γ and c′ (three-term-binding.md §7a). The C² observation (19 Oct), the form selection, the Venturi kill, the identity g₁ = Q_β and BE(D) = m_e[3γ − 1 − 2γ₂], the A ≤ 4 table, the coherent-sum reading with self : mutual = 1 : 2, and refusal as anti-phase: Grace. Prior art: Dicke 1954 (superradiance, N²); Tjon 1975.

---

## 8. Feynman review (independent adversarial check, 31 Oct) — and the regrade

An independent instance was briefed to break this note: recompute from CODATA/AME, trace circularity, run a look-elsewhere count, test the alternatives, re-examine the Tjon claim. Its findings, accepted where they are right (all but one), with the regrades:

| claim | Feynman | regrade |
|---|---|---|
| arithmetic (γ, c′, Y, Q_β, tables) | **confirmed** | stands |
| "BE(D) − Q_β = 2Y(2)" as a second check | the same equation rearranged — double-counted | **struck** |
| g₁ = Q_β identity, BE(D) = m_e[3γ − 1 − 2γ₂] | look-elsewhere: 9 formulas of the form m_e(aγ + bγ₂ + cγ₃ + d), small integers, land within 0.3 % of BE(D); 23 within 1 %; background rate ≈ 7 per band. In the no-γ₃ family: 1 hit, p ≈ 0.4. The 6 keV miss is ~10⁴σ against the data and is not recoil (1.3 keV). | **COINCIDENCE-LEVEL.** Not an identity. Kept only as a flagged coincidence. |
| bookkeeping | the slingshot used here is per capsid (y = A, "Option I", adopted 16 Oct with full Coulomb); `three-term-binding.md` §7a's keeper table is per carrier (y = p + 2n: D = 3Y(2) = 2.154, face 0.070). The identity and the C² law exist **only in the per-capsid bookkeeping**; per carrier, the face energies go 0.07 : 4.70 : 24.7 — nothing like C². The note cited §7a for γ while using the 16 Oct bookkeeping without saying so. | **Accepted.** The two bookkeepings are mutually exclusive on the T–³He gap (per carrier assigns it to one carrier's slingshot with pp Coulomb ≈ 0, which the 16 Oct review killed on Nolen–Schiffer; per capsid assigns it to Coulomb). The programme's standing choice is per capsid + full Coulomb; §7a's slingshot rule is superseded and should carry a note saying so. **The C² law is a statement inside one bookkeeping, and that must be said every time it is used.** |
| C² "and nothing adjacent" | only two independent ratios (³He ≈ T + Coulomb); C² beats the listed alternatives in every variant, but without the mesh term the fitted exponent is 1.9, and the mesh size (0.854 ≈ g₁ + 0.066) is itself one unit; the rivals were far from the data by construction | **regraded: CONSISTENCY** — a two-point power law, exponent 1.9–2.0 depending on the mesh bookkeeping. |
| Tjon line | the predicted (8.341, 28.339) is 0.69 MeV *above* the Tjon line at that T; the note quoted the perpendicular distance against a steep line | **struck.** The model is off the Tjon correlation in the meaningful (vertical) sense: it under-binds T by 0.14 and should then under-bind ⁴He by 0.66; it over-binds ⁴He by 0.04. |
| mechanism self : mutual = 1 : 2 | a reading of C², zero independent content | **regraded: CONSTRUCT, inheriting every weakness above** |
| attachments as integers in Q_β | 1.25, 1.88, 2.13, 3.10 are not integers at the stated noise | **struck** |
| ³He Coulomb 0.99 vs §7a's "≈ 0" | internal inconsistency not flagged | **accepted**; §7a's U_pp ≈ 0 was already killed on 16 Oct (REPLY-argon F-list); the note should have said so |

**What survives §8:** the A ≤ 4 table as a *compact description* inside the per-capsid bookkeeping (D −0.3 %, T −1.7 %, ³He −4.7 %, ⁴He +0.15 %, two constants' worth of structure from one datum plus masses); the kill of the Venturi reading (contacts, not carriers); the foam kill from 30 Oct. **What does not survive:** the word "identity," the Tjon sentence, the integers, and the mechanism as anything more than the form restated.

Overall after review: **CONSISTENCY at best for §1/§3; COINCIDENCE-LEVEL for §2; CONSTRUCT without independent support for §4–5.** The right next test is unchanged and sharper for the review: ⁶Li and ⁷Li from the cluster rule with the unit fixed — if the unit is a coincidence, they miss; and the per-capsid vs per-carrier bookkeeping needs a nucleus where A and p + 2n diverge (⁶He: 6 vs 10) to be settled on data rather than by ruling.

Lineage of §8: the Feynman instance (an independent Claude run, 31 Oct); the regrades: Grace.
