# tests/alpha-ladder results — AME2020, 2550 measured nuclides

## Phase 1 — α-conjugate ladder, q = 2.42 fixed, no refit

Contact counts, derived here (tetrahedral growth 3N−6 vs best sticky-sphere packing found by search):

| Nα | 3N−6 | E_max (search) |
|---|---|---|
| 3 | 3 | 3 |
| 4 | 6 | 6 |
| 5 | 9 | 9 |
| 6 | 12 | 12 |
| 7 | 15 | 15 |
| 8 | 18 | 18 |
| 9 | 21 | 21 |
| 10 | 24 | 25 |
| 11 | 27 | 28 |
| 12 | 30 | 32 |
| 13 | 33 | 36 |
| 14 | 36 | 40 |

| nucleus | Nα | AME BE | pred 3N−6 | err | pred E_max | err |
|---|---|---|---|---|---|---|
| Ne-20 | 5 | 160.645 | 163.258 | +1.63% | 163.258 | +1.63% |
| Mg-24 | 6 | 198.257 | 198.814 | +0.28% | 198.814 | +0.28% |
| Si-28 | 7 | 236.537 | 234.370 | -0.92% | 234.370 | -0.92% |
| S-32 | 8 | 271.780 | 269.926 | -0.68% | 269.926 | -0.68% |
| Ar-36 | 9 | 306.717 | 305.481 | -0.40% | 305.481 | -0.40% |
| Ca-40 | 10 | 342.052 | 341.037 | -0.30% | 343.457 | +0.41% |
| Ti-44 | 11 | 375.475 | 376.593 | +0.30% | 379.013 | +0.94% |
| Cr-48 | 12 | 411.468 | 412.148 | +0.17% | 416.988 | +1.34% |
| Fe-52 | 13 | 447.700 | 447.704 | +0.00% | 454.964 | +1.62% |
| Ni-56 | 14 | 483.996 | 483.260 | -0.15% | 492.940 | +1.85% |

within 2 %: 3N−6 rule 10/10, maximal-contact rule 10/10.
Calibration points (not scored): C-12 92.147 vs 92.162, O-16 127.703 vs 127.619; Be-8 excess -0.092 (open edge, unbound).

Implied q per nucleus under 3N−6 (AME excess / (3N−6)): Ne-20 2.130  Mg-24 2.374  Si-28 2.564  S-32 2.523  Ar-36 2.479  Ca-40 2.462  Ti-44 2.379  Cr-48 2.397  Fe-52 2.420  Ni-56 2.440

## Phase 2 — valley of stability to U-238, α-ladder extended with the fewest constants

L1: BE = Nα·28.296 + 2.42·(3Nα−6) + e_n·N_loose, e_n fitted = 4.821 MeV  ->  RMS 38.35 MeV, 4.57 % of BE   (1 new constant)
L2: L1 + Coulomb-shaped bond weakening c·E·Z/A^(1/3), e_n = 11.870, c = -0.1914  ->  RMS 36.28 MeV, 4.33 %   (2 new constants)
L3: L2 + symmetry (N−Z)²/A, coefs [23.167, -0.1925, -56.6124]  ->  RMS 8.03 MeV, 2.67 %   (3 new constants)

| A | nucleus | AME | L1 | err | L3 | err |
|---|---|---|---|---|---|---|
| 12 | Z=6 | 92.2 | 92.1 | -0.0% | 90.6 | -1.7% |
| 16 | Z=8 | 127.6 | 127.7 | +0.1% | 124.0 | -2.8% |
| 20 | Z=10 | 160.6 | 163.3 | +1.6% | 156.9 | -2.3% |
| 28 | Z=14 | 236.5 | 234.4 | -0.9% | 221.1 | -6.5% |
| 40 | Z=18 | 343.8 | 324.8 | -5.5% | 354.2 | +3.0% |
| 56 | Z=26 | 492.3 | 467.0 | -5.1% | 481.0 | -2.3% |
| 90 | Z=40 | 783.9 | 744.8 | -5.0% | 772.6 | -1.4% |
| 120 | Z=50 | 1020.5 | 970.8 | -4.9% | 1014.4 | -0.6% |
| 138 | Z=56 | 1158.3 | 1106.4 | -4.5% | 1143.4 | -1.3% |
| 160 | Z=66 | 1309.4 | 1293.8 | -1.2% | 1312.5 | +0.2% |
| 180 | Z=72 | 1446.3 | 1439.1 | -0.5% | 1441.5 | -0.3% |
| 208 | Z=82 | 1636.4 | 1655.4 | +1.2% | 1624.0 | -0.8% |
| 232 | Z=90 | 1766.7 | 1836.2 | +3.9% | 1766.6 | -0.0% |
| 238 | Z=92 | 1801.7 | 1881.4 | +4.4% | 1801.2 | -0.0% |

## Phase 3 — Bethe–Weizsäcker baseline, 5 constants fitted on the same nuclei

a_v 16.110  a_s 19.105  a_c 0.7519  a_a 22.689  a_p 15.71  ->  RMS 2.63 MeV, 0.67 %   (5 constants)
on the Phase-1 ladder nuclei the 5-constant drop model errs by -1.58% .. -0.40% (the 1-constant ladder: see Phase 1).

## Phase 2a — the light non-α-conjugate nuclei: α-ladder + one loose cluster, excess over the ladder

Excess = AME − [Nα·28.296 + 2.42·(3Nα−6)], i.e. what the loose piece buys on top of the α frame.

| nucleus | Nα + loose | AME BE | excess | per loose nucleon |
|---|---|---|---|---|
| Li-6 | 1α + d | 31.994 | 3.698 | 1.849 |
| Li-7 | 1α + t | 39.245 | 10.949 | 3.650 |
| Be-9 | 2α + n | 58.164 | 1.573 | 1.573 |
| B-10 | 2α + d | 64.751 | 8.159 | 4.080 |
| B-11 | 2α + t | 76.205 | 19.614 | 6.538 |
| C-13 | 3α + n | 97.108 | 4.961 | 4.961 |
| N-14 | 3α + d | 104.659 | 12.512 | 6.256 |
| N-15 | 3α + t | 115.492 | 23.345 | 7.782 |
| O-17 | 4α + n | 131.762 | 4.060 | 4.060 |
| O-18 | 4α + nn | 139.808 | 12.105 | 6.052 |
| F-19 | 4α + t | 147.801 | 20.099 | 6.700 |
| Ne-21 | 5α + n | 167.406 | 4.147 | 4.147 |
| Na-23 | 5α + t | 186.564 | 23.306 | 7.769 |
| Al-27 | 6α + t | 224.952 | 26.138 | 8.713 |
| P-31 | 7α + t | 262.916 | 28.546 | 9.515 |
| Cl-35 | 8α + t | 298.210 | 28.284 | 9.428 |
| K-39 | 9α + t | 333.724 | 28.243 | 9.414 |
| Fe-56 | 13α + nnnn | 492.260 | 44.556 | 11.139 |

What the loose piece buys is not one constant per nucleon, but it is patterned: a single loose neutron on three or more alphas buys 4.0–5.0 MeV (C-13 5.0, O-17 4.1, Ne-21 4.1), with Be-9 the exception at 1.6; a loose triton rises from 10.9 (Li-7) through 19.6 (B-11) and 23.3 (N-15/Na-23) and saturates at 28.2–28.5 MeV from P-31 on — the binding energy of an alpha. The 3n+1 and 3n+3 series each want their own rule, and the triton's saturation at BE(α) is the number a geometric model should be asked to produce.

## Grade (Ventris, 2026-10-06 23:13 AEST)

**Phase 1: [PASS] for both counting rules under the registered 2 % gate; [DISCRIMINATED] in favour of 3N−6.** With q = 2.42 fixed from C-12/O-16 and no refit, the tetrahedral growth rule puts all ten α-conjugate nuclei Ne-20 … Ni-56 within 1.6 %, and the eight from Mg-24 up within 1 %; from Ca-40 up it is within 0.3 % (Fe-52: 0.00 %). The maximal-contact rule passes the gate but drifts to +1.85 % at Ni-56 and would fail by Zn-60. The data say an added α bonds to exactly three neighbours, not to as many as geometry allows — a bond-saturation statement, and the physics that has to be explained. The one-constant ladder beats the five-constant drop model on these ten nuclei (drop: −0.4 … −1.6 %).

**Provenance.** This is the α-particle model of Hafstad & Teller (1938) and Wefelmeier (1937): BE = Nα·B_α + (bonds)·q, bonds from tetrahedral stacking. The spec's inputs forbade the literature cluster shapes, and none were used; the counting came from the packing search. But the result is theirs, and any write-up must cite it. What the truncated octahedron adds to the sphere is not tested by this phase, because both give 3N−6.

**Phase 2: [FAIL] as a one-constant model of the valley.** Extending the ladder with a loose-nucleon constant gives 4.6 % RMS over A = 12–238 and misses Fe-56 by −5.1 %; two further constants (Coulomb-shaped bond weakening, symmetry) bring it to 2.7 %, which is the drop model arriving term by term, and the drop model itself does 0.67 % with five. "Holds to Fe-56 with one constant" is true of Fe-52 and Ni-56, the α-conjugate pair; it is not true of Fe-56, which is 13α + 4n and sits 44.6 MeV above the ladder. "Explains everything between" is not true of the valley.

**Phase 2a: the pattern the geometry should be asked for.** A loose neutron on ≥ 3 alphas buys 4–5 MeV; a loose triton saturates at 28.2–28.5 MeV from P-31 on, i.e. one alpha's worth. Li-6 (α + d, 3.7) and Li-7 (α + t, 10.9) are not anomalies of the model, they are the start of two series. A model that lands Li-7 and not Li-6 has a d-rule missing, not a Li-6 problem.

Nothing here crosses the wall; this is a test directory with its README written first and its numbers pasted unedited. Inputs: AME 2020, 28.2957, 2.42, a sphere-packing search.

## Addendum 23:18 — the α-conjugate premium over neighbours, and where it ends

BE/A of each 4n nucleus against the mean BE/A of the most-bound isobars at A±1 (AME 2020):

| A | nucleus | BE/A | vs A±1 | vs A±2 |
|---|---|---|---|---|
| 4 | He-4 | 7.074 | +69.7 % | +119.5 % |
| 8 | Be-8 | 7.062 | +17.0 % | +19.4 % |
| 12 | C-12 | 7.680 | +6.7 % | +9.6 % |
| 16 | O-16 | 7.976 | +3.3 % | +4.4 % |
| 20 | Ne-20 | 8.032 | +2.0 % | +1.4 % |
| 24 | Mg-24 | 8.261 | +1.1 % | +0.7 % |
| 28 | Si-28 | 8.448 | +0.7 % | +0.2 % |
| 32 | S-32 | 8.493 | −0.05 % | −0.7 % |
| 36 | Ar-36 | 8.520 | −0.4 % | −0.9 % |
| 40 | Ca-40 | 8.551 | −0.2 % | −0.7 % |
| 44 | Ti-44 | 8.534 | −1.0 % | −1.3 % |
| 48 | Cr-48 | 8.572 | −1.3 % | −1.6 % |
| 52 | Fe-52 | 8.610 | −1.6 % | −1.8 % |
| 56 | Ni-56 | 8.643 | −1.4 % | −1.6 % |

Measured: the premium for being whole alphas decays monotonically and crosses zero between Si-28 and S-32; from sulphur on, nuclei with loose neutrons out-bind the α-conjugate ones per nucleon, by 1.5 % at iron. Kelvin-cell (bcc) cluster count: shared-faces-per-cell closures at n = 13–15, 27, 51; no closure at 56. Sphere (α) count: closure at 4 and 13; Fe-52's measured excess is 33.0 bonds, the stacked value, not the 36 of a closed 13-shell. Concluded (marked): "perfect packing" is a surface premium, real and large at He-4 and O-16, and exhausted by A ≈ 30; Fe-56 is not a packing rung on either geometry or data. Si-28 is the last α-conjugate nucleus that gains over its neighbours, and the one the 3N−6 ladder under-predicts most (−0.9 %, implied q 2.56): it wants one contact more than a stacked chain gives it.
