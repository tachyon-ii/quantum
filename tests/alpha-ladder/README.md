# tests/alpha-ladder — one α–α contact quantum, edges counted from geometry, no refit

Ventris Kober, 2026-10-06 23:10 AEST. Serves `specs/alpha-ladder.md`. Written before any
prediction was computed; the comparison columns in `results.md` were filled last.

James's challenge (23:10): "Use the logic, do the math, prove me wrong. Any element, t½ > 880 s.
Run to U-238 if you want." This test is the α-conjugate ladder of the spec, then the extension
the spec puts out of scope, then an honest baseline that is nobody's geometry.

## Claim under test

BE(Nα) = Nα · 28.2957 + q · E(Nα), with q = 2.42 MeV fixed from C-12/O-16 and E(Nα) the
number of α–α contacts in the cluster, counted from geometry alone. Two geometric readings of
"contacts in a packing" exist and they disagree from Nα = 10 on, so both are registered:

- **E_tet(N) = 3N − 6** — each added α sits in a three-fold hollow and touches exactly three
  (James's "3Nα − 6", `fable-freeman-fractal-conjecture.md` §8 row 8; a tetrahedral growth
  sequence, every edge on a closed cycle for N ≥ 3).
- **E_max(N)** — the maximum contact count of N equal sticky spheres (closest packing in the
  spec's words). Known values (Arkus–Manoharan–Brenner 2009; Holmes-Cerfon 2016): 3, 6, 9, 12,
  15, 18, 21, 25, 29, 33, 36, 40 for N = 3 … 14; this test re-derives them by search before use.

## Pass / fail, registered now

| outcome | grade |
|---|---|
| all 12 nuclei Ne-20 … Ni-56 within 2 % of AME total BE, q fixed, one counting rule chosen *before* looking | **[PASS]** for that rule |
| within 2 % except Ne-20 (the known deformed/8Be+12C cluster) | **[PASS-WITH-RESIDUE]** |
| one rule passes and the other fails | **[DISCRIMINATED]** — the data choose the growth rule; record which and why it is a physics statement |
| only passes if q is refitted or edges chosen after seeing the excess | **[FAIL — CIRCULAR]** |
| neither rule within 2 % | **[FAIL]** |

Second phase, out of the spec's scope, registered here so it cannot move afterwards:

- **Valley of stability to U-238.** For each A ≤ 238 take the most-bound isobar in AME 2020
  (proxy for t½ > 880 s; no NUBASE in the repo). Extend the ladder as α-clusters plus loose
  nucleons with the *fewest* new constants that reach 1 % RMS; count the constants honestly.
- **Baseline.** Bethe–Weizsäcker with 5 constants, fitted on the same set, same metric. The
  ladder earns its keep only where it does as well with fewer constants, or explains the
  residual pattern the drop model cannot.

## Inputs

`data/ame2020-mass-table-rows-only.txt` (binding energy per nucleon, keV), 28.2957 MeV for He-4,
q = 2.42, and a sphere-packing search. Nothing else. No shell model, no literature cluster shapes.

## Files

`ladder.py` — the whole test; `results.md` — output, pasted unedited.
