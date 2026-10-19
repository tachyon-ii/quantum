# Rung 0 — first complexity ladder (generated from results/rung0_ladder.json)

Train: D, T, He-3, He-4 (D and He-4 as anchors). Holes (inequalities, every seating): nn, pp unbound; He-5, Li-5 ≤ BE(He-4). Blind: Li-6 (52,040 seatings on the BCC lattice, 2,602 clusters × 20 species assignments). LP: L1 residual + 0.02·Σ|g|, |g| ≤ 12 MeV. Slingshot A·Y(2) gated on connectivity and a triplet contact per body; Coulomb at lattice distances.

| level | entries | D | T | He-3 | He-4 | He-5 max (≤ 28.30) | Li-5 max | **Li-6 blind** (31.99) |
|---|---|---|---|---|---|---|---|---|
| L0 pair2+c3 | 6 | +0.00 | +0.00 | -0.09 | **-9.41** | 28.30 | 26.58 | **39.69 (+24 %)** |
| L1 +type | 12 | +0.00 | +0.00 | -0.09 | **-9.24** | 28.30 | 26.83 | **36.07 (+13 %)** |
| L2 +nn/pp | 18 | +0.00 | +0.00 | +0.00 | **-8.75** | 28.30 | 28.30 | **37.05 (+16 %)** |
| L3 +c>=3 | 24 | -0.79 | +0.00 | +0.00 | **-0.72** | 28.30 | 27.26 | **40.33 (+26 %)** |
| L4 +zmax>=4 flag | 42 | +0.00 | +0.00 | +0.00 | **+0.00** | 16.85 | 15.70 | **18.72 (-41 %)** |

Reading (Grace, 19 Oct, 12:20):
- **Without a saturation descriptor the anchors and the holes are inconsistent.** L0–L2 cannot bind He-4 (−9 MeV) because every He-5 seating must stay below He-4 and, with the same label on the fifth nucleon's contacts as on the alpha's, that pins the closed-contact value near zero. The lattice says, independently of the membrane: **the alpha closes only if contacts know about coordination.**
- **With a hard coordination flag (L4) everything in training fits exactly and the holes are respected — but Li-6 blind is 18.7 vs 32.0 (−41 %).** He-5 comes out unbound by 11 MeV instead of 0.9. Same over-closure as the membrane's cap3 this morning (−8 MeV on Li-6). Two methods, one answer: **the saturation is graded, and A ≤ 4 plus the holes cannot determine its shape** — they only bracket it (L2: Li-6 +16 %; L4: −41 %).
- Consequence for the split (declared now, before any A = 7 number is seen): **Li-6 moves into training**; the blind set becomes Li-7, Be-7, Be-9, B-10, B-11, C-12. A = 7 seatings (~30 k clusters × 35 assignments) are feasible here; A = 9 and up go to the box.
- The ladder's admission rule worked as designed: L1 (contact type) improved the blind by ×0.5 and is admitted; L2 (nn/pp split) did not (+12.7 → +15.8 %) and is not; L3 is unstable (D lost); L4 is admitted on the holes alone.

