# Adversarial review — Euler-ruler statistics (EULER-RULER-tests.md)

Reviewer script: `outputs/ruler_review/rv.py` (session outputs folder). Independent seed, independent code for the T1/T2/T3/T5 statistics. 23 Nov 2026.

## Table

| claim | their value | my value | verdict |
|---|---|---|---|
| T1: 6π⁵ vs proton/electron, relative miss | 1.9e-5 | 1.882e-5 (6π⁵ = 1836.1181 vs 1836.1527) | correct |
| T1: single-hit p, π-only ruler, ±factor-2 window | 3.3e-4 (400k surrogates) | 2.9e-4 (4M surrogates); analytic 2d·n/(2 ln 2) = 3.0e-4 with n = 11 expressions in window | correct within their Monte Carlo error (±0.3e-4) |
| T1: same p under other reasonable windows | not reported | ×1.5 window 2.7e-4; ×1.2 window 2.0e-4; log-uniform over the family's whole span 1.6e-3 | p depends on window by a factor ~8 |
| T1: same p under other family bounds | not reported | p,q≤6: 7e-5; p,q≤20: 1.2e-3; exponents to ±8 or ±10: 2.0e-3 | p depends on analyst's bounds by a factor ~30 (7e-5 to 2e-3) |
| T1: "after 70 trials" | 0.023 | arithmetic right (0.020 with my p); but range 0.005–0.13 over the family choices above | not a valid error rate; see problem 1 |
| T1: "fitted as well 0.0 % of the time", "p=0.00", "smallest single p 0.000" | 0.0 %, 0.000 | floor of a 4,000-surrogate test is 1/4001 = 2.5e-4 | misreported; must read "< 0.03 %" or give the 400k value |
| T1: Fisher π-only, ten independent constants | 0.03 | 0.38 when proton/electron is removed (hand calculation from their printed p-values, 9 constants, χ² = 19.2 on 18 d.f.) | the 0.03 (and 0.01 for fourteen) is the single 6π⁵ hit, not a second finding |
| T1: neutron/electron π-only p = 0.02, proton/muon p = 0.03 | listed as separate rows | neutron/electron's hit is the same 6π⁵ (miss 1.4e-3 = the n–p mass difference) | not independent hits; file says so only for Fisher |
| T1: constants | as typed | 1/α, m_p/m_e, m_n/m_e, m_μ/m_e, (m_n−m_p)/m_e, μ_p, μ_n, a_e, sin²θ_W: agree with CODATA 2018 / PDG to digits given. τ/e 3477.23 ok (1776.86). W/Z 0.88147 uses m_W = 80.379 (current PDG average 80.369 gives 0.88136). Higgs/Z 1.3737 matches no standard value: 125.25 → 1.3735, 125.20 → 1.3730 | Higgs/Z wrong in 4th decimal, W/Z dated; both inside experimental error, no effect on conclusions |
| T2: N=Z ladder, 13 alpha gains | p = 0.231 (file; brief said 0.25) | uniform 0.23; jittered data 0.19; shuffled gaps 0.36; log-uniform 0.26; scan 1–4: 0.14; scan 1–16: 0.38; scan 1–30: 0.59 | not significant under any variant; p itself is soft (0.14–0.59) |
| T2: column header "0.25 = chance" | 0.25 | null mean of the best-unit statistic: 0.08 (n=4), 0.11 (n=6), 0.16 (n=13), 0.21 (n=60), 0.23 (n=483) | wrong; chance level depends on n because the unit is optimised |
| T2: nucleon rungs, unit 7.0, stat 0.048, p 0.117 | 0.048 / 0.117 | at unit 7.0 the ratios are 0.113, 1.026, 1.054, 4.000 — 0.788 is scored as "0 units". Forbidding zero: stat 0.108, unit 1.04, p = 0.78 | the low score is an artefact of rounding to zero |
| T2: Dalton control p | 0.000 | < 5e-5 (20,000 surrogates, none as good) | fine; print as "< 1/4001" |
| T2: power (mine) | not reported | n=13, planted unit, noise sd 0.10 unit: detected 100 %; sd 0.15: 73 %; sd 0.20: 30 % | test can only see lattices tighter than ~±0.15 unit |
| T3: chance level and ceiling | not stated | fraction gaps per unit interval 1/4, 1/12, 1/6, 1/6, 1/12, 1/4 → chance mean 0.0486, largest possible single distance 0.125 | observed 0.039–0.066 sits on chance; scale is compressed (0 to 0.125) |
| T3: pooled p | 0.844 | not recomputed; pooled power checked: all 28 ratios locked with noise up to 0.04 → detected 100 % | pooled test is sensitive to a full lock; per-nucleus rows (4 ratios) are weak |
| T3: level energies | from memory | O-16, Ne-20, Mg-24, Si-28, S-32, Ca-40 agree with my recollection to ±0.01 MeV. C-12 list (4.44, 7.65, 9.64, 10.3, 12.71) is not the five lowest: omits 9.87 (2⁺), 10.84 (1⁻), 11.83 (2⁻) | C-12 row is a selected list |
| T5: β⁻ only / all 34 | p = 0.841 / 0.749 | 0.83 / 0.74 (uniform); jitter ±3 decades 0.80 / 0.73; normal 0.79 / 0.75; unit range 0.3–3: 0.95 / 0.92; turn = 1e-23, 3e-22, 1e-21 s: 0.80–0.97; turn = 1 s: 0.33–0.78 | reproduced; never below 0.3 in any variant |

## Problems, most serious first

1. **The 0.023 is not an error rate and should not be quoted as one.** The coincidence 6π⁵ was known (Lenz 1951) before the family was written down, and the family bounds (p,q ≤ 10, exponents to ±5) are the smallest round bounds that contain it. Changing only those bounds moves the single-hit p from 7e-5 to 2e-3, and the "×70" figure from 0.005 to 0.13. In one direction 70 is too harsh (the five rulers are nested, so the 70 pairs are far from independent; π-only alone is 14 trials → 0.004). In the other it is far too lenient (the real search space is every constant and every expression form anyone tried before 1951, which is not enumerable). Correct statement: "a five-digit agreement; no meaningful significance can be assigned after the fact."

2. **"Excluded as an exact equality" is true but the output never shows it.** The file contains no measurement uncertainties. m_p/m_e is known to about 2e-11 relative (6e-11 in CODATA 2018), so a miss of 1.9e-5 is roughly 3e5 to 1e6 standard deviations. That one line should be added. It also exposes a design gap: T1 measures "closeness relative to random numbers", never "agreement within error". For the precisely measured constants every best expression in the table is excluded as an equality; for the poorly measured ones (sin²θ_W ±1.7e-4, W/Z ±1.5e-4, Higgs/Z ±9e-4) the full ruler fits inside the error bar by density alone (misses 1.2e-5 to 1.4e-4), which is equally uninformative.

3. **Fisher π-only p = 0.01 / 0.03 reads as corroboration; it is the same hit counted again.** Without proton/electron the ten-constant figure is ≈ 0.38. The fourteen-constant figure additionally double-counts via neutron/electron (same expression) and proton/muon. Also the Fisher inputs are 4,000-surrogate p-values floored at 2.5e-4, so the combined value is noisy.

4. **T2 statistic lets values round to zero.** The nucleon-rung row's 0.048 comes from calling 0.788 MeV "zero units of 7.0". With whole numbers ≥ 1 required the row is 0.108, p = 0.78. The surrogate shares the flaw so the printed p is not anti-conservative, but the "best unit 7.000, distance 0.048" cells invite a false reading.

5. **"0.25 = chance" in the T2 and T5 headers is wrong.** Because the unit is optimised, chance is 0.08–0.23 depending on the number of values. A reader comparing 0.141 (ladder) or 0.117 (closed cores) against 0.25 will see structure that is not there.

6. **T2 scan range and surrogate are analyst choices that move p.** Ladder p runs 0.14 to 0.59 across scan ranges 1–4 to 1–30 and four surrogate types. Conclusion (nothing) survives; the specific number 0.231 carries no weight. The uniform-between-min-and-max surrogate also pins the range to the data's own extremes (slightly conservative) and does not match clustered data; for the 483-value set p = 0.95 probably reflects that mismatch rather than anything physical (reasoned, not tested).

7. **Zeros printed as p-values.** "p=0.00", "0.000", "0.0 % of the time" in T1, T2, T3 controls: all should be "< 1/4001".

8. **T3: C-12 level list is selective**, and per-nucleus tests on four ratios have little power; only the pooled row means anything. The test would miss a partial lock (say a quarter of ratios locked) — reasoned, not tested. Dividing by E₁ only tests ratios to the first level, not between other pairs.

9. **T5 tests a lattice through a fixed origin (one turn = 1e-22 s).** That origin is a free choice; I varied it over three decades and to 1 s and nothing appears, so the null result is robust. The T5 table is appended to the file with no heading, directly under T4's closing sentence.

10. **Minor constants:** Higgs/Z 1.3737 should be 1.3735 (125.25) or 1.3730 (125.20); W/Z should be 0.8814 only for the older m_W. Neither changes any row materially.

## Does the output support the summary?

"The ruler finds nothing beyond chance except the long-known 6π⁵ coincidence, which is itself excluded as an exact equality."

- "Nothing beyond chance" in T2, T3, T4, T5: supported, and robust to the variants I ran.
- "Except 6π⁵": acceptable only if no significance is attached. Do not quote 0.023 or the π-only Fisher 0.01/0.03 as evidence.
- "Excluded as an exact equality": correct, but rests on the measurement uncertainty, which the output does not contain. Add it.

Suggested wording: "No set of energies, level ratios, closed numbers or lifetimes shows a common measure beyond chance. Among fourteen pure numbers the only close hit is the long-known 6π⁵ ≈ m_p/m_e, agreeing to five digits; because it was known before the test was designed no significance can be assigned to it, and it misses the measured value by about a million times the measurement uncertainty, so it is not an equality."

## Checks run versus reasoned

Run (recomputed): 6π⁵ miss; T1 single-hit p by Monte Carlo (4M) and analytically; window and family-bound sensitivity; T2 ladder p under four surrogates and four scan ranges; nucleon-rung row with and without zero; null level of the T2 statistic versus n; T2 power; Dalton control; T3 gap structure, chance mean, ceiling, pooled power; T5 under three nulls, two unit ranges, five origins; derived constant ratios (τ/e, W/Z, Higgs/Z, τ/μ, p/μ, n−p).

Reasoned only / from memory: correctness of CODATA and PDG values and of nuclear level energies and half-lives (no reference tables consulted); Fisher without proton/electron (hand arithmetic on their printed p-values); T3 partial-lock insensitivity; cause of p = 0.95 on the 483-value set; T4 (read only, no issue found); the full five-ruler T1 table and the T3 per-nucleus p-values were not rerun.
