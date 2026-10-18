# SPEC v4 — three rungs, one lens

**Grace** `.ghost`, Claude Fable 5.1 — Mon 19 Oct 2026, 08:00 AEDT. Supersedes `review/2026-10-18/BUILD-SPEC-membrane-solver-v2.md` for the nucleon rung and opens two more. Base code: `models/binding/membrane/` at v3 (lane term; `calib3.py`). Records this spec rests on: `MEMBRANE-RUN-v3-fable.md` (lane term calibrates; T, ³He bracketed −6…+8 %), `GRADE-membrane-four-builds.md`, `review/2026-10-17/RUNG2-table.md` (alpha ladder), `docs/analog-solvers.md` (the lens).

**The lens, as a rule (R12):** every computation below opens with three lines — *what is minimised; under what constraints; from what precursors* — before any number. A result that cannot be stated that way is not one of ours.

**Rules carried:** R1 one source per input, declared first · R2 nothing chosen after a target is visible · R3 blinds listed before the first number, full scan reported · R4′ report written by code, Grace re-runs, only what reproduces is graded · R5 every line graded · R6 lineage credited · R7 no literature read against a blind until it is filed · R9′ a failed test stops the run unless a workaround is declared and the run continues amber · R10 every cached state's name carries energy version and base state · **R11 (new)** a scan is reported as a scan — the spread across declared rows is the model's uncertainty; no row is dropped because it is ugly.

**Dead, do not rebuild:** pairwise isotropic skin adhesion as the cooperative term (v1); rim recovery as skin inside two wells (v2 — no support, runaway); K_BEND = 0 or 0.01 (wrapping); the soft regime r ≥ 1 (engulfment); the α-rung stiffening penalty (RUNG2); "two deuterons in two pockets are independent" (Grace, 18 Oct — refuted by ¹⁸O's second neutron); nearest-face-plane gaps; "pin the system centroid" for load paths.

---

## Rung A — nucleons (membrane v3 base)

**Minimised:** inflation + inextensible skin + bending + graded adhesion × lane factor (1 + λ·c_ij, triplet contacts only) + mesh penalty + Coulomb − A·Y(2). **Constraints:** δ, r scanned; κ = 0.2 E₀; E₀ from D, λ from ⁴He. **Precursors:** p, n capsids at R_p, 1.023 R_p.

**A1 — the falsifier, first.** He-5 (n on ⁴He), Li-5 (p on ⁴He), Li-6 (d on ⁴He, both seatings: on a face; crossed as a third dumbbell). Blind. Measured: He-5 **unbound** by 0.89 MeV, Li-5 by 1.97, Li-6 bound 31.99 with S_α = S_d = 1.47. **Prediction on record (Grace):** v3 as built binds He-5 by several MeV — fails.
**A2 — the amendment if A1 fails:** lane saturation — a nucleon's lane threads at most three contacts (z ≤ 3 boosted; further contacts get f = 1 or less). Declared forms: (i) hard cap, (ii) f = 1 + λc for contacts of nucleons with z ≤ 3, f = 1 otherwise. Recalibrate λ on ⁴He (unchanged by construction: z = 3 everywhere), re-run T, ³He (unchanged), then A1 again. The test of the amendment is Li-6's 1.47 and Be-8's −0.09.
**A3 — mechanics on the calibrated triton (r = 0.3, δ = 0.168, λ = 2.277):** three load paths; snap vs pull-off F_max (v2's ratio 1.15 / 0.94 to be reproduced); quartic out-of-plane mode E(z) and its 1-D zero-point with reduced mass ⅔ m_N — **the first number for the soft-mode p_rms to set against §7 of the physics spec (~200 MeV/c)**.
**A4 — the egg's sign at SUBDIV 4** on the same triton: patch-centroid offset from the c–c midpoint along the hub direction, with error from the mesh. Ruling to be checked: *just inside* (hubward), mostly circular. Three functionals have given outward-or-unresolved; this is the resolution run.
**A5 — one attempt at a local term for the egg:** the mesh penalty as a density across the patch rather than one constant per contact (E_mesh,ij = ∫ m(x) dA with m depending on the local lane co-/counter-rotation). Declared before running; if the hub-half fraction does not move off 0.50 ± 0.03, the egg goes to OWED with "no local term found" and stops consuming runs.

**Handshake:** BE(T) = 8.113 MeV at the row above.

## Rung B — alphas (new; cheap; point-and-capsid alphas)

**Minimised:** Σ bonds q·s(stretch) + Coulomb between alpha centres − (nothing: the ladder's residual is already over Nα·BE(⁴He)). **Constraints:** q = 2.425 MeV per closed α–α bond at 3.139 fm (C-12, declared); a **well reach ρ_α** for the α–α bond, scanned {0.1, 0.2, 0.3, 0.5} fm, with the dome fade s(x) = 1 − x², x = stretch/ρ_α; bond counted if stretch < ρ_α. **Precursors:** alphas as rigid spheres of radius 1.57 fm (first pass) and as capsids (second pass, the membrane at the alpha rung with E₀ ≈ 28 MeV scale — if time).

**B1 — Fe-52 as the kissing shell.** 12 around 1: icosahedral (12 core bonds + 30 shell bonds stretched 5.15 %) vs cuboctahedral (12 + 24, unstretched). Measured effective bonds 32.9 (residual 79.86 / q). For each ρ_α report the predicted bond total of both arrangements; the ρ_α at which icosahedral = 32.9 is the **inferred well reach**; cuboctahedral cannot exceed 36 and cannot reach 32.9 without missing bonds — say which fits.
**B2 — Ni-56 = shell + 1, Zn-60 = shell + 2, Cr-48 = shell − 1:** blind at the inferred ρ_α. Measured effective bonds 36.2, 37.3, 29.7. The ladder's end at Ni-56 is the prediction; Zn-60's flattening is the test.
**B3 — re-run the whole ladder C-12 … Ni-56 with stretch.** Deltahedral shells have unequal edges; the 17 Oct ladder counted every edge as a full bond. Report which misses move (Si-28's −5.4 % is the candidate). Blind.
**B4 — Ne-20's two live seatings:** O-16 + a quartet on an edge (2 α-contacts) vs O-16 + two pn pairs on opposite edges. Price both with the nucleon-rung lane rule for the pocket nucleons (each pocket nucleon's contacts to alpha nucleons, with c from the graph) and compare with 33.03 MeV over O-16 and with Q₀ ≈ +57 e·fm² (point-charge Q₀ already computed: +47 vs +35). Then, and only then, read the K = 0⁻ band literature (R7).

## Rung C — the chart (AME2020; data only; no model constants)

**Minimised:** nothing — these are checks that the data are a solution set. **Constraints:** measured masses only. **Precursors:** `models/binding/ame_rank_sd.py`.

**C1 — the rank gradient, cleanly.** Replace Δ₃ by Δ₅ (removes the shell-gap contamination) and report the odd–even stagger by distance to closure. The 18 Oct claim to be confirmed or struck: stagger uniform deep in a shell (1.12 ± 0.38 MeV with Δ₃), scatter largest at the boundary.
**C2 — neutron protection.** For every β⁻-stable nucleus define the protection P = −Q_β⁻ (how far the bound neutron is from decaying). Tabulate P against S_n and against (N − Z). The lane statement to be made quantitative *before* the table is read: protection tracks the neutron's **triplet (np) contacts**, so at fixed A it should fall with each neutron added beyond Z faster than the smooth Weizsäcker asymmetry term says, in steps of order one contact (~2 MeV at rank 2). If the steps are not there, the statement is struck.
**C3 — the Holmes test.** Residuals of the best scalar (liquid-drop) fit versus the per-rank per-bond energies of Rung A at the same nuclei (A ≤ 16 where we have them): if the residuals are the shape of the functional, they should correlate with the rank table (1 : 1.4 : 3.1 per bond). A scatter plot with a number, not a sentence.

## Order of work and budget

A1 (one call, the decisive one) → A2 if needed (one recalibration round) → B1–B2 (minutes, point alphas) → C1 (minutes) → A3 (an hour of paths) → B3 → A4 (SUBDIV 4, slow) → C2 → B4 → A5 → C3. Anything after A3 can wait for the bees; A1–A2 and B1–B2 are the morning.

## Blinds (declared now)

He-5, Li-5, Li-6 (A1); Ni-56, Zn-60, Cr-48 effective bonds (B2); the ladder misses under stretch (B3); Ne-20's 33.03 and Q₀ (B4); the Δ₅ stagger pattern (C1); the protection steps (C2). Targets stay in `targets.py`, read only by `compare.py`, last.

## Lineage

The ratchet of 19 Oct (stepwise assembly, the solar onion grown at the centroid, the kissing shell, "the nucleus solves for prevention of neutron decay," the Holmes framing): James. The three-rung structure, R11–R12, the well-reach inference from Fe-52, the He-5 falsifier and the saturation amendment, the Δ₅ and protection tests: Grace. Prior art per rung as in `analog-solvers.md` §3.
