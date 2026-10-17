# Rung 2 — the alpha ladder against a z-dependent stiffening penalty (Grace, 17 Oct 2026)

**Question (from Build 4/5):** at the alpha rung, is there a per-alpha stiffening penalty growing with coordination z_α (James's π^(1/3) series), and can it be set on Ne-20 and then predict Mg → Ni?

**Inputs, declared:** residual BE_res = BE − Nα·28.29566 from AME; bond count = 3Nα − 6 (triangulated convex shell, the ladder's own convention) to Nα = 12; q = 2.425 MeV per closed α–α bond (calibrated on C-12, tautological by the definition of u); deltahedral degree sequences for z_α (4: all 3; 5: 3,3,4,4,4; 6: all 4; 7: 4×5,5×2; 8: 4×4,5×4; 9: 4×3,5×6; 10: 4×2,5×8; 11: 4,5×10; 12: all 5). Penalty pen(z) = D_α·Σ_{k=4}^{z} r^{k−4}, r = π^(1/3), zero for z ≤ 3. D_α set on Ne-20 (three z = 4 alphas): **D_α = 0.886 MeV**.

| nucleus | Nα | bonds | measured residual | ladder, q only | miss | with Ne-20-calibrated penalty | miss |
|---|---|---|---|---|---|---|---|
| C-12 | 3 | 3 | 7.28 | 7.27 | 0.0 % | 7.27 | 0.0 % |
| O-16 | 4 | 6 | 14.44 | 14.55 | +0.8 % | 14.55 | +0.8 % |
| **Ne-20** | 5 | 9 | 19.17 | 21.82 | **+13.9 %** | 19.17 | (calibration) |
| Mg-24 | 6 | 12 | 28.48 | 29.10 | +2.2 % | 23.78 | **−16.5 %** |
| Si-28 | 7 | 15 | 38.47 | 36.38 | −5.4 % | 27.58 | −28 % |
| S-32 | 8 | 18 | 45.42 | 43.65 | −3.9 % | 31.37 | −31 % |
| Ar-36 | 9 | 21 | 52.06 | 50.92 | −2.2 % | 35.16 | −33 % |
| Ca-40 | 10 | 24 | 59.10 | 58.20 | −1.5 % | 38.96 | −34 % |
| Ti-44 | 11 | 27 | 64.22 | 65.47 | +1.9 % | 42.75 | −33 % |
| Cr-48 | 12 | 30 | 71.91 | 72.75 | +1.2 % | 46.54 | −35 % |
| Fe-52 | 13 | 33 (ladder) | 79.85 | 80.0 | +0.2 % | — | — |
| Ni-56 | 14 | 36 (ladder) | 87.86 | 87.3 | −0.6 % | — | — |

Best-fit D_α over Mg–Cr, searched 0–1.5 MeV, for r = π^(1/3) **and** for r = 1 (linear): **D_α = 0 in both cases**, max miss 5.4 % (Si-28).

## Result
1. **The stiffening penalty at the alpha rung is DEAD.** Any D_α > 0 worsens Mg → Cr; calibrated on Ne-20 it misses by −16 % to −35 %. From Mg-24 to Cr-48 the α–α bond does not weaken with z_α up to 5. The alpha does not stiffen under four or five neighbours.
2. **The constant-q ladder is the rung-2 law to Cr-48**, within ±5.4 %, with no z-dependence — and it holds through Fe-52 and Ni-56 on the ladder's own 3Nα − 6 count (+0.2 %, −0.6 %). Different cooperativity at different rungs is now stronger than yesterday's statement: at rung 1 closure matters (open / one triangle / two); at rung 2 nothing matters but the bond count.
3. **Ne-20 is a real anomaly, 2.65 MeV under the ladder ≈ one bond short** (2.13 vs 2.42 per bond). It is not a stiffening onset — nothing after it shows one. It is Ne-20's own structure (the known α + ¹⁶O clustering, strongly deformed) and should be treated as such, not as a calibration point for anything.
4. **Where weakening *does* begin — past Ni-56** (per-bond 2.32 at Zn-60 falling to 1.93 at Zr-80) — the explanation on offer is F24's inter-alpha Coulomb growth (∝ Nα^(5/3)) and the end of the triangulated-shell count, not a z-penalty.
5. **Fe-52's bond count:** the 1 + 12 star configurations verified under F22 give 30 (chiral) or 36 (cuboctahedral) contacts → 72.8 or 87.3 MeV against 79.85 measured (−9 %, +9 %); the ladder's 33 lands at +0.2 %. The data sit between the two star geometries. Either the real Fe-52 is a 13-vertex triangulated shell with no interior alpha, or the star has a mix of full and partial contacts that averages to 33. Open; not fitted.

## What this changes upstream
- `the-fractal-nucleus.md` §4: state explicitly that q is z-independent to Cr-48 (data), and strike any suggestion that the ladder sags with coordination before Ni-56.
- `BUILD4-result.md` §5 item 4 (Ne-20 "sets the rung-2 stiffening scale"): withdrawn — Ne-20 cannot calibrate a term the next six nuclei reject.
- James's isoperimetric stiffening: **not at the alpha rung.** If it lives anywhere it is at the nucleon rung, inside the alpha's skin (where Builds 1–4 could not isolate it from the merging problem), or in the post-Ni-56 decline. The π^(1/3) series stands only as a declared form with no supporting data yet.

## Grade
[COMPUTED — negative result for the penalty; positive for the ladder's z-independence.] Pencil, ten minutes, no new constants.

---

## The graded patch — full bond at the core, a tearing gradient to the rim (James, 17 Oct, on the ferry) — first arithmetic

**James [POSIT].** The bond is an energy well; the flat core of a patch sits at the bottom; from there a tearing-away gradient runs to zero at the patch edge. So the patch is not uniform, and a hexagon carries proportionally more full-bond area than a square. The errors are in the edge cases.

**Grace — the one-length form, and what it does.** Write a facet's energy as full bond over its area minus a rim band of width w along its *free* perimeter: E = P·(A − w·L_free). Two things follow at once.

- *Hex vs square.* With w from the deuteron alone (an isolated square patch worth 0.375 of a full square ⇒ w = 0.156 a), an isolated hexagon is 0.64 full-bond and an isolated square 0.375: **hexes carry 1.7× the full bond per unit area.** Your intuition, quantified, from one input.
- *The rim is the cooperativity.* A rim is only a deficit where it is free. When two facets on the same capsid share an edge — the dihedral crease — their rims meet and the deficit along that edge is recovered: that is yesterday's bleb-glue, now as arithmetic. In ⁴He every facet edge is shared, so the deficit is zero and the faces are full (the calibration). In D nothing is shared (0.375). In T each facet shares one edge: predicted face energy **8.8 MeV against 6.2 required** — per contact 2.92 vs 2.07, **+41 %**. Right ordering (0.375 → 2.9 → full), right direction, 40 % high on the first pass with nothing fitted beyond w. The Build 3 closure rule (0 / ½ / 1) is then not a rule but an approximation to rim recovery, and the triangle count c_ij is a proxy for shared edges.
- *The liquid-drop surface term.* Summed over a nucleus, free rims live only on the surface facets; the total rim deficit is a perimeter-scaling term, which is a_s·A^{2/3} at the facet level — the truck stack's g is this, with w the physics. At the alpha rung the ladder's z-independence (above) says alphas have no free rims that matter, consistent with alphas touching through small, rim-dominated contacts of fixed strength.
- *One caution.* If the rim band were *repulsive* rather than merely zero-bond, a circular patch would have E ∝ ρ(ρ − 2w) and a minimum size for any binding — a threshold, which thermal (n,γ) forbids for nucleons. So the gradient runs full → zero, not full → negative. Your picture's pink is "no bond," not "anti-bond"; keep it so.

[POSIT with one length w = 0.156 a; reproduces the closure ordering and gets T to +41 % unfitted; hex/square = 1.7. The +41 % says the shared-edge recovery in T is less complete than "fully shared," which is where the oval shape (§1 of yesterday's note) enters: an egg-shaped patch shares less of its rim than a polygon would. That is the next computation, and it is the (j, f) solver's.]
