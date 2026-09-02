# Chirality Note — when handedness survives in the capsid–compression model

**Scope.** Truncated-tetra (TT) capsids with equal edges; contacts are **H–T** (backbone), rare **V–V** pins (locks), with belts routed on tokamak-like flux surfaces. We ask: *when does a cluster have two mirror-related minima (L/R) separated by a real barrier*, i.e., when is chirality a **stable** feature and not washed out by parity mixing?

> **Chirality survives when a TT cluster has two mirror-related H–T assemblies separated by a real barrier.** D₂ provides the unique seed; He-4 is a chiral 4-cycle geometrically but parity-mixes; larger α clusters can lock L/R folds if the H–T network and lemniscate routing raise the barrier above local mode scales.

---

## 1) Order parameter (handedness in one line)

Pick three non-coplanar **H–T** face normals that define the fold, e.g. around a ring or a 3-D hinge:

$$
\chi \;=\; \operatorname{sign}\!\big(\, \mathbf{n}_1 \cdot (\mathbf{n}_2 \times \mathbf{n}_3 ) \,\big)\;\in\;\{-1,+1\}
$$

* $\chi=+1$: right-handed (R) configuration; $\chi=-1$: left-handed (L).
* $|\chi|=0$ only at a *saddle* (degenerate/planar) — useful for locating the barrier top.

**Handedness survives** if the energy landscape has **two minima** at $\chi=\pm1$ separated by a **finite barrier** $\Delta E_b>0$. Without a barrier the ground state parity-mixes (achiral).

---

## 2) The seeds: D₂ and He₄

### D₂ (p + n): unique H–T dimer (up to symmetry)

* **Backbone:** one **coaxial H–T**: `H:0(p) ↔ T:0(n)`
* **Registry:** a 60° twist DOF about the common normal yields two local “registries” (co-rotating / counter-rotating); energy equivalent in isolation.
* **Use:** the *only* dimer that smoothly feeds belts and tilings; treat as the “stud” that α builds from.

### He₄ (p + n + p + n): **closed H–T 4-cycle → two enantiomers**

* Build two D₂ seeds; close the ring with two more **H–T** joints on the `:1` ports.
* Apply a **±60°** twist about that axis on one dimer → **He-4(L)** and **He-4(R)**.
* The ring is **chiral geometrically**, but for A=4 the tunneling barrier is effectively zero (J$^{\pi}$=0⁺); the physical ground state parity-mixes.
* **Key virtue:** every TT keeps **two unused H∥T ports**, giving clean sockets for α-polymer growth.

**Why 60° shows up.** The inner triangular “window” of a TT hex repeats every 60°. H–T docking fixes a common normal but leaves this registry free; a 4-cycle cannot keep all windows in phase, forcing a $\pm\pi/3$ misalignment (the *hex aperture* you observed).

---

## 3) Bonding & routing recap (for energy/counting)

* **Face radii:** centroid → hex plane $r_H$; centroid → tri plane $r_T=\tfrac{5}{3}r_H$.
* **Bi-lemniscate length (same lobe count k):** $L\propto kR$. For $k=2$, $L_{HH}:L_{HT}:L_{TT}=1:\tfrac{4}{3}:\tfrac{5}{3}$.
* **Bond index (continuity-limited):**

  $$
  \mathcal B(k,R)\propto \frac{v(k)^2}{L(k,R)},\qquad 
  v(k)\approx v_2\left(\frac{2}{k}\right)^{\alpha},\ \alpha\in[1,2]
  $$

  ⇒ for fixed $k$, $\mathcal B\propto L^{-(2\alpha+1)}$: **short & smooth beats long & tight**.
* **Grammar:** H–T as backbone (**strong**; k=2 preferred), V–V pins are **locks** (no belt), H–H/T–T are **bridges** (use sparingly).

---

## 4) Minimal energy functional (with chirality)

$$
E \;=\; -\sum_{\text{H–T bonds}} J_{HT}\,\mathcal B_{HT}
\;-\; J_{\text{pin}}N_{VV}
\;+\; E_{\text{Coul}}(Z)
\;+\; E_{\text{curv}}(A)
\;-\; \epsilon\,\chi
$$

* $J_{HT}$ dominates; $J_{\text{pin}}$ small (rigidity only).
* Coulomb & curvature as in your capsid model (grow with $Z^2/A^{1/3}$, $A^{-2/3}$).
* **New term:** $ -\epsilon\,\chi$ = tiny symmetry-breaking bias (set $\epsilon=0$ for pure SSB). It stands for environmental selection (rotation, surface, flow) at freeze.

---

## 5) Barrier & tunneling recipe (how to decide if chirality survives)

1. **Enumerate** a small, TT-legal configuration family (e.g., α chains/rings/knots with only H–T backbones, sparse V–V pins).
2. **Fix $\chi=+1$**, **minimise $E$** → $E_L$. Reflect to $\chi=-1$ → $E_R=E_L$.
3. **Find the MEP** (minimum energy path) between L and R by stepping a single 60° twist parameter (or do a quick NEB). The maximum is the saddle $E_\ddagger$.
4. **Barrier:** $\Delta E_b=E_\ddagger-E_L$.
5. **Criterion:** if $\Delta E_b \gtrsim \hbar\omega$ of local modes (or the thermal/collective scale at freeze), the system **localises** (chiral); else it **parity-mixes** (achiral).

*He-4:* $\Delta E_b$ ≈ 0 → achiral ground state.
*Cluster targets:* ¹²C (3-α ring/triangle), ¹⁶O (4-α ring/stack), ²⁰Ne (5-α chain + bend) — good candidates for $\Delta E_b>0$.

---

## 6) What to look for (data hooks)

* **Parity doublets / chiral doublet bands** in α-cluster nuclei at moderate spin (cf. known odd–odd chiral bands, but seek cluster analogues).
* **E1 systematics**: E1 suppression/allowance patterns consistent with localised L/R vs parity-mixed states.
* **Reaction selectivity:** transfer/knockout in an oriented/rotating environment (proxy $\epsilon$) yielding enantiomeric excess in population.

---

## 7) Implementation checklist (sim)

* Geometry: **uniform TT** (4 H + 4 T, equal edges).
* Ports: **H∥T pairs** labelled $i=0..3$.
* Dimer: `H:0(p) ↔ T:0(n)`; registry S/M (60°).
* α ring: close with `:1` ports; apply **±60°** twist → L/R.
* Routing: outer flux layer for backbone H–T belts (k=2); inner layer for rare braces; phase-offset belts to avoid crossings.
* Energy: use the functional above; start with $\alpha=1$, $J_{\text{pin}}\approx 0.2J_{HT}$, bias $\epsilon=0$ unless testing selection.

# Nomenclature

Absolutely—baby steps. Here’s a tight, staged plan that keeps us 100% on **nucleons** and turns the truncated-tetra (TT) model into working geometry + numbers without jumping ahead.

---

## Stage 0 — Lock the coordinates & naming (once, reusable)

**Goal:** one unambiguous TT object we can clone for p/n.

* Shape: uniform **truncated tetrahedron** (equal edges).
* Face IDs: **H0..H3** (hexagons), **T0..T3** (triangles) with **Hᵢ ∥ Tᵢ**.
* “Look-at” convention (you proposed): pick **H0** by a reference vector $\hat u$; order **H1→H2→H3** **clockwise**; triangles inherit the index by parallelism.
* Radii (so belts have numbers):
  $r_H=\frac{\sqrt6}{4}a$, $r_T=\frac{5\sqrt6}{12}a$, $\Delta t=r_T-r_H=\frac{\sqrt6}{6}a$.

**Deliverable:** a tiny TT object spec (JSON) with face normals, centroids, and the H∥T pairing.

---

## Stage 1 — D₂ only (one dimer, one number)

**Goal:** choose **one** backbone, compute its belt length & relative strength, then validate visually.

* **Backbone:** **H–T** coaxial contact
  `H:0(p) ↔ T:0(n)` (anti-parallel face normals).
* **Optional stiffener:** *one* V–V pin on a separate layer (rivet; **no belt** through it).
* **Belt length (bi-lemniscate, k=2):**
  $L_{HT}\approx 4\pi\,R_{\mathrm{avg}}$ with $R_{\mathrm{avg}}=r_H+\Delta t/2 = \tfrac{4}{3}r_H$.
* **Relative strength** (against H–H level if we ever compare):
  $\displaystyle \frac{\mathcal B_{HT}}{\mathcal B_{HH}} \approx \left(\frac{L_{HH}}{L_{HT}}\right)^{2\alpha+1} = \Big(\tfrac{3}{4}\Big)^{2\alpha+1}$.
  (For $\alpha=1$: \~0.42; $\alpha=1.5$: \~0.32)

**Deliverables:** a) the D₂ pose file (p,n transforms + ports used), b) $L_{HT}$, $\mathcal B_{HT}$ number, c) screenshot (what you already showed—bottom-right variant).

---

## Stage 2 — He₄ ring (two enantiomers, one barrier)

**Goal:** build **both** L/R α rings using only H–T joints; compute that the two are **degenerate** in energy at k=2, then confirm there’s a **60°** registry DOF.

* Start with two D₂ seeds:
  `H:0(p1) ↔ T:0(n1)` and `H:0(p2) ↔ T:0(n2)`
* Close the ring:
  `H:1(n1) ↔ T:1(p2)` and `H:1(n2) ↔ T:1(p1)`
* **Twist** one dimer by **±60°** about the `:1` axis → **α(L)** and **α(R)**.
* **Chirality label:** $\chi=\mathrm{sign}\{\mathbf n_{H0}\cdot(\mathbf n_{H1}\times \mathbf n_{H2})\}$.
* **Barrier (first pass):** step the twist from −60°→+60° and evaluate $E$ from the belt term only (no pins) to see if a barrier is visible (it should be tiny for He-4).

**Deliverables:** the two α poses (L/R), their $\chi$, belt map, and a twist-scan plot $E(\theta)$.

---

## Stage 3 — He₃ and H₃ (one layout each)

**Goal:** one geometry each that obeys “no P–P belt” as backbone.

* **He₃ (p+p+n):** central **n**; two **opposed** H∥T channels on n:
  `H:0(n) ↔ T:0(p1)`, `T:0(n) ↔ H:0(p2)` → **two** k=2 P–N belts; p–p pushed apart.
* **H₃ (p+n+n):** central **p**; two **H–T** belts to n₁ and n₂ on non-coplanar ports (`H:0(p)↔T:0(n1)`, `H:1(p)↔T:1(n2)`) → tri-lemniscate around p.

**Deliverables:** the two poses + belt lengths/indices.

---

## Stage 4 — One simple scoring & a sanity table

**Goal:** give the model a single-line score to compare motifs and a tiny table to look for trends.

* **Score (belt-only):**
  $\displaystyle E_{\text{belts}}=-\sum_{\text{H–T bonds}} J_{HT}\,\frac{(2/k)^{2\alpha}}{k\,R_{\text{eff}}}$,
  with $R_{\text{eff}}\in\{r_H,\tfrac{4}{3}r_H,\tfrac{5}{3}r_H\}$ for HH/HT/TT as needed (we only use HT here).
* **Set** $J_{HT}=1$, $\alpha=1$ (baby step).
* **Table:** D₂, He₃, H₃, He₄(L/R): list $N_{\text{belts}}$, $\{R_{\text{eff}}\}$, total $E_{\text{belts}}$.

---

## Stage 5 — Packability (qualitative)

**Goal:** check the immediate sockets left on He₄ (two H∥T per TT) and verify that extending by H–T contacts pushes you toward the **ATT dense phase** (near 207/208). No numbers yet—just verify the geometry has **no new voids**.

---

### What I can hand you next (concrete)

* A **minimal JSON** schema for TT pose + port usage (you can generate from your modeller).
* A tiny **Python stub** that:
  (i) reads two TT poses, verifies H–T coaxiality,
  (ii) computes $R_{\text{eff}}$, $L$, and $\mathcal B$,
  (iii) labels $\chi$ for He₄ and scans the twist.

No changes to leptons; this keeps us laser-focused on **D₂ → He₄** and yields **one number** per baby step so we can course-correct quickly.



