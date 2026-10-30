# Rung B — Fe-52 as the kissing shell: the α–α well reach, and Ni-56 / Zn-60 / Cr-48 blind (generated from kissing_results.json)

Minimised: Σ_pairs q·s(stretch), dome s = 1 − x², x = (d − 3.139)/ρ_α, counted while x < 1. Constraints: rigid alphas, contact 3.139 fm; q = 2.425 MeV from C-12 (ladder convention, Coulomb implicit); ρ_α scanned, inferred from Fe-52 (residual over 13 × 28.296 = 79.86 MeV); Cr-48, Ni-56, Zn-60 blind at that ρ_α. Precursors: alphas. Icosahedral shell: 12 core bonds + 30 shell bonds stretched 5.15 %; cuboctahedral: 12 + 24 unstretched. Ni-56 = shell + one alpha in the best three-contact face pocket; Zn-60 = two non-touching pockets; Cr-48 = shell minus one vertex.


### (a) ladder convention|ico

| ρ_α (fm) | Cr-48 (71.92) | **Fe-52 (79.86)** | Ni-56 (87.86) | Zn-60 (90.55) |
|---|---|---|---|---|
| 0.10 | 26.67 (-62.9 %) | **29.10 (-63.6 %)** | 36.37 (-58.6 %) | 43.65 (-51.8 %) |
| 0.15 | 26.67 (-62.9 %) | **29.10 (-63.6 %)** | 36.37 (-58.6 %) | 43.65 (-51.8 %) |
| 0.20 | 47.75 (-33.6 %) | **54.39 (-31.9 %)** | 61.66 (-29.8 %) | 68.94 (-23.9 %) |
| 0.25 | 61.99 (-13.8 %) | **71.47 (-10.5 %)** | 78.75 (-10.4 %) | 86.02 (-5.0 %) |
| 0.30 | 69.72 (-3.1 %) | **80.75 (+1.1 %)** | 88.03 (+0.2 %) | 95.30 (+5.3 %) |
| 0.35 | 74.38 (+3.4 %) | **86.35 (+8.1 %)** | 93.62 (+6.6 %) | 100.90 (+11.4 %) |
| 0.40 | 77.41 (+7.6 %) | **89.98 (+12.7 %)** | 97.26 (+10.7 %) | 104.53 (+15.4 %) |
| 0.50 | 80.97 (+12.6 %) | **94.25 (+18.0 %)** | 101.53 (+15.6 %) | 109.51 (+20.9 %) |
| 0.70 | 84.07 (+16.9 %) | **97.97 (+22.7 %)** | 105.25 (+19.8 %) | 114.07 (+26.0 %) |

### (a) ladder convention|cub

| ρ_α (fm) | Cr-48 (71.92) | **Fe-52 (79.86)** | Ni-56 (87.86) | Zn-60 (90.55) |
|---|---|---|---|---|
| 0.10 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |
| 0.15 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |
| 0.20 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |
| 0.25 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |
| 0.30 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |
| 0.35 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |
| 0.40 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |
| 0.50 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |
| 0.70 | 75.17 (+4.5 %) | **87.30 (+9.3 %)** | 94.57 (+7.6 %) | 101.85 (+12.5 %) |

### Reading (Grace, 20 Oct)

- **The shell is icosahedral and the well reach is ρ_α ≈ 0.30 fm.** At ρ_α = 0.30 the 30 stretched shell bonds are each worth 1 − (0.162/0.30)² = 0.71 of a full bond: Fe-52 comes out +1.1 %. The cuboctahedral shell has no stretched bonds, is ρ-independent, and misses Fe-52 by +9.3 % with no knob to turn. [COMPUTED]
- **Blind at ρ_α = 0.30:** Cr-48 −3.1 %, **Ni-56 +0.2 %**, Zn-60 +5.3 %. Three nuclei not used to set anything, two inside the ladder's ±5 %, the third the first to fall outside — and it is the one the kissing picture says should: the 15th alpha's measured increment over Ni-56 is 2.69 MeV, about one bond, while two face pockets offer three. **The ladder ends at Ni-56 because the shell is full**, as a number rather than a sentence. [COMPUTED; blind]
- **Explicit pairwise Coulomb between alpha centres fails outright** (convention (b): q recalibrated to 4.26 on C-12, then Fe-52 at −63 % and worse). The constant-q ladder works to ±5 % only with Coulomb implicit in q. Since pairwise point-charge Coulomb grows as Nα^{5/3} and bonds as Nα, the data are saying that the inter-alpha Coulomb is **not paid at the point-charge rate between alpha centres**. That is either screening by shared lanes or a statement about where the alpha's charge sits — and it may be the same fact as the lane-charge partition question in `docs/slac-reimagined.md` §6. [COMPUTED; the reading is CONJECTURE]
- The reach 0.30 fm at the alpha rung sits beside the nucleon-rung δ scan (0.08–0.25 fm) and the pull-off peel's dome: same shape of well, same order of reach, one rung up.


## B3 — the whole 4n ladder as soft-well clusters (`ladder_stretch.py`; generated)

Each Nα: global minimum of Σ_pairs [hard core below 3.139 fm; −q(1 − x²) dome, ρ_α = 0.30] by two-stage multi-start (60 starts, seed 0). Column A: q = 2.425 (C-12), no Coulomb (ladder convention). Column B: declared test — inter-alpha Coulomb at κ × point-charge over all pairs, κ = 0.18 (set to the Mg–Ni average excess of column A), q_bare = (7.27 + κ·5.50)/3 = 2.753 so C-12 stays exact. Rigid 17 Oct ladder (3Nα − 6 bonds) for comparison.

| nucleus | Nα | measured residual | rigid ladder | A: soft well, no Coulomb | eff. bonds (A) | B: soft well + κ = 0.18 Coulomb |
|---|---|---|---|---|---|---|
| C12 | | 7.27 | +0.0 % | 7.27 (+0.0 %) | 3.0 (3+0) | 7.27 (-0.1 %) |
| O16 | | 14.44 | +0.8 % | 14.55 (+0.8 %) | 6.0 (6+0) | 14.54 (+0.7 %) |
| Ne20 | | 19.17 | +13.9 % | 21.82 (+13.9 %) | 9.0 (9+0) | 21.61 (+12.7 %) |
| Mg24 | | 28.48 | +2.2 % | 29.10 (+2.2 %) | 12.0 (12+0) | 28.48 (-0.0 %) |
| Si28 | | 38.47 | -5.4 % | 38.55 (+0.2 %) | 15.9 (10+6) | 37.49 (-2.5 %) |
| S32 | | 45.41 | -3.9 % | 45.82 (+0.9 %) | 18.9 (13+6) | 44.00 (-3.1 %) |
| Ar36 | | 52.06 | -2.2 % | 54.88 (+5.4 %) | 22.7 (11+12) | 52.25 (+0.4 %) |
| Ca40 | | 59.10 | -1.5 % | 63.08 (+6.7 %) | 26.2 (12+15) | 59.35 (+0.4 %) |
| Ti44 | | 64.22 | +1.9 % | 71.53 (+11.4 %) | 29.6 (16+14) | 66.66 (+3.8 %) |
| Cr48 | | 71.92 | +1.2 % | 78.80 (+9.6 %) | 32.6 (19+14) | 72.34 (+0.6 %) |
| Fe52 | | 79.86 | +0.2 % | 87.02 (+9.0 %) | 35.9 (21+15) | 78.82 (-1.3 %) |
| Ni56 | | 87.86 | -0.6 % | 97.25 (+10.7 %) | 40.3 (18+23) | 87.73 (-0.1 %) |
| Zn60 | | 90.55 | — | 106.32 (+17.4 %) | 43.9 (27+17) | 94.71 (+4.6 %) |

Readings (Grace, 20 Oct):
- **Stretch fixes the two the rigid ladder missed:** Si-28 −5.4 % → +0.2 %, S-32 −3.9 % → +0.9 % (column A), exactly where the deltahedra have unequal edges. [COMPUTED; blind for Si, S]
- **But the free optimum over-binds from Ar-36 on (+5 … +17 %):** the soft well's global minimum is denser than the icosahedral kissing shell (Fe-52: 21 exact + 15 stretched = 35.9 effective bonds vs the shell's 33.3 and the measured 32.9). Real alphas do not pack as densely as the well alone allows. The excess tracks the extra point-charge Coulomb beyond the per-bond share at a constant **κ ≈ 0.16–0.20** from Mg to Ni. [COMPUTED]
- **Column B: one more constant (κ = 0.18) flattens C-12 → Ni-56 to within ±3.8 %** (eleven nuclei, three constants: q, ρ_α, κ; worst Ti-44 +3.8 %, most within ±1.3 %), with Zn-60 the first past the line (+4.6 %) and Ne-20 the standing structural outlier (+12.7 %: face seating gives 3 contacts, data want 2). [COMPUTED; κ fitted, so this is CONSISTENCY not prediction]
- **What κ = 0.18 means is undecided, and the 4n ladder cannot decide it.** The Weizsäcker Coulomb term says the full Z²/A^{1/3} is paid across the chart, so either the inter-alpha Coulomb is screened to ~1/5 (charges mobile on shared lanes) or it is paid in full and the α–α bonds *strengthen* with coordination to compensate (cooperativity at the alpha rung — a C² law one rung up). Both scale like Nα^{5/3} along N = Z, so they are degenerate here. **N ≠ Z breaks it:** adding neutrons adds bonds without Coulomb (Fe-56 − Fe-52 = 44.56 MeV for four; Ne-22 − Ne-20; Ca-44 − Ca-40). That is the next computation at this rung, and it needs the filler-nucleon pockets from rung 0. [OWED]
- Explicit point-charge Coulomb at full strength (κ = 1) fails by −63 % (B1); κ = 0 over-binds by 9–17 %; the data sit at κ ≈ 0.18. Whatever the alphas are, they see one-fifth of each other's charge at these distances. [COMPUTED]

