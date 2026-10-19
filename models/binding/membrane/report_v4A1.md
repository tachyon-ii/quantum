# v4 A1/A2 — He-5 / Li-5 / Li-6 blind under three lane forms (generated from results/calib4.json)

Row r = 0.3, δ = 0.1682 fm, κ = 0.2 E₀; E₀ = 41.079 MeV from D (v4 energy: smooth floor + smooth max, continuous contact graph w = tanh(2W/0.30)). λ recalibrated on ⁴He per form.

| form | λ | ⁴He (cal.) | T (8.482) | ³He (7.718) | He-5 S_n (meas −0.89) | He-5 on pnn face | Li-5 S_p (meas −1.97) | Li-6 stacked: S_d (meas +1.47) |
|---|---|---|---|---|---|---|---|---|
| linear | — | multi-stable: [(2.301, 29.692), (2.301, 29.688), (2.3, 29.686)] | — | — | — | — | — | — |
| sat | 3.598 | 28.295 | 7.002 (-17 %) | 6.105 (-21 %) | +11.38 | +5.64 | +6.87 | +13.88 |
| cap3 | 3.410 | 28.314 | 6.808 (-20 %) | 5.915 (-23 %) | -7.51 | -10.88 | -8.96 | -8.05 |

Forms: **linear** f = 1 + λc; **sat** f = 1 + λ·min(c,2)/2; **cap3** = sat × min(1, 3/z_i, 3/z_j) with z the continuous coordination (a nucleon's lane threads at most three boosted contacts).

Readings (Grace, 19 Oct):
- **A1 as predicted: without saturation the alpha is not closed.** Under the linear form at the v3 energy He-5 came out bound by 43 MeV (the fifth nucleon raised the alpha's own triangle counts from 2 to 3); under the sat form (c capped at 2) He-5 is still bound by 11 MeV, Li-5 by 7, and the stacked deuteron by 14 (measured −0.9, −2.0, +1.5). **Dead as built.**
- **cap3 closes the alpha — too hard.** He-5 unbound by 7.5, Li-5 by 9.0, Li-6 by 8.0 against measured −0.9, −2.0, +1.5. The sign is right everywhere; the cost of a fifth nucleon is ~7 MeV too large because a hard capacity at z = 3 taxes the alpha's own bonds the moment anything touches it.
- The truth sits between sat and cap3, and the four data (He-5, Li-5, Li-6, Be-8) bracket the shape of the saturation. That shape is the next declared scan — not a fit to He-5.
- **Cost of the energy-version change:** the smooth floor shifted ⁴He by −9 % at fixed λ; after recalibration T and ³He under sat/cap3 are −17…−23 %, worse than v3-linear's −4…−6 %. The linear form at the new energy shows ⁴He hysteresis (two states, 25.0 and 29.7 MeV, at λ = 2.30) and could not be calibrated by secant; to be redone with multi-start.

