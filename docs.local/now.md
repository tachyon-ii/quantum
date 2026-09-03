# now() — where the edge is

**Grace Bayes, 2026-09-03. Current state only.** Written after reading the Φ paper and Gemini's review, and after **running the test archive** rather than reading about it. Companion to `../../schrodinger/checkpoint-1.md` (the ledger) and `../../schrodinger/now-edge.md` (why there is a now).

---

## 0. The pointer, in one paragraph

The frontier is not where the paper says it is. The paper (`Φ — A Minimal Ontology`) is `checkpoint-1` in formal dress plus four new posits and a good falsifier list. The review (Gemini) locates three real pressure points and then aims its tests at the wrong scripts. The archive, executed, says: **the solvers work, GR and textbook QM are reproduced to 10⁻¹⁶, one sector (the nuclear capsid) has a passed blind test, and the corpus's own scoreboard has been carrying a false entry — g=2 was never derived.** `now()` therefore points at three things in order: fix the g=2 entry honestly; put the ℤ₂-bundle restatement into the axiom; build the one test the paper stakes itself on and the archive doesn't contain (E⊥B as null-field invariants, computed).

## 1. The paper, graded

**What it is.** Sections 1–6, 9–13, 15–19 restate the ledger. New content: §4.1 tangential ejection [POSIT, no mechanism]; §7 the crystalline electron with (τ,h) algebra [POSIT]; §8 D_rel > 0 given a physics job — surprisal preserved by topological isolation [POSIT, good]; §11 S = Φs [LITURGY → POSIT; dimensionally unpaid, and the paper says so]; §17–18 predictions and eleven falsifiers [the best part — keep verbatim].

**Hygiene.** Two chat preambles leaked into the body ("Here is the fully revised and styled version of Sections 2 and 3, cleaned up according to…"). Strip before the file travels anywhere. Also §6's E⊥B mechanism ("magnetic = axial flow, electric = 720° topological averaging") is stated as fact; the ledger holds it as [POSIT + ANCHOR: the null-field invariants].

**The rule this establishes: the paper may not carry a claim at higher status than the ledger's grade.** Stamp each §17 item with its `checkpoint-1` status before publication. A paper that outruns its ledger is a mirror with a bibliography.

## 2. The review, graded

Three crises, three tests, one circular falsifier.

| Gemini said | verdict |
|---|---|
| **Crisis 1** — a vector before space is semantically empty | **Real, and answered**: direction at the axiom floor is the ℤ₂ of the twisted line bundle over the loop (H¹(S¹;ℤ₂)), pre-spatial and embedding-free; spatial direction arrives at N=2. Sharper than Gemini's SU(2) hand-wave. Ruling pending (checkpoint catch 1) |
| **Crisis 2** — l² and s⁻² smuggle operators in before an operator space exists | Real but shallow. §4 says {m,l,s} are *antecedents*, then §5 does dimensional algebra without saying where multiplication came from. Prose fix: algebra arrives with the first *comparison* (N=2, `dimension-ladder.md`). Not a physics wound |
| **Crisis 3** — symmetric ejection ⇒ equal τ=±1 ⇒ why matter? | Real, standing, already on the ledger as the internal-annihilation suppressor + the 50:50-integration posit. Gemini adds the sharp form: a "first wobble" is a broken symmetry *at Ω*, contradicting Ω's definition. Keep that sentence |
| **Test 1** — g=2 fails if it needs ε tuned | Aimed one floor too high. The failure is upstream — §3 below. Gemini had the archive open and did not read the derivation |
| **Test 2** — BEC analogue horizons vs the i-reset | Fair, far. Registered |
| **Test 3** — ³H/³He 0.764 MeV split from the capsid | **Already run**, `capsid_audit` §7.3: split reproduced to **−4.6%** by the four-constant honeycomb rule (k, κ, u_s, k_b); A=3 absolutes +12%, one shared cause. Gemini pointed at `mobius_fusion.py`, which is a Möbius *pairing* map ("postulate demo"), not a binding calculator. RTFS failure |
| "check f₂/f₁ ≈ 1.5 in the HFQPO output" | **Circular.** 3:2 is the *selection criterion* of the sample. A model cannot be tested on the property used to choose its data |

Gordo's profile, confirmed again: fast, right about *where* the pressure is, wrong about *which file does what*. Injector, not instrument.

## 3. The archive, executed — what green actually means

**`mobius_topology/` — 15/15 pass** (A1–A5, D1–D4, F1–F5). Antiperiodic BC → half-odd mode ladder; Sagnac orientation and linearity; local-c identity to 4×10⁻¹⁶; λ–f reciprocity; de Sitter precession; Schwarzschild null geodesics vs 4M/b; O(h²) convergence. **Every one of these checks the solver against a textbook result.** They are compiler tests — "we do not ship without running the compiler" — and they pass. Not one asks a question that QM+GR would answer differently, so not one is evidence *for* Φ. Green here means the tooling is sound, which is necessary and is not the same thing.

**`gravity/` — passes.** Eddington bending to 0.06%, PPN-γ sweep, Lense–Thirring scaling, thin-lens Gaussian. Same status. And `libgravity.py`'s field equation is `∇²Φ = 4πG (u−u₀)/c²` — **G inserted by hand**, which is `checkpoint-1` §7's catch stated in code: the map is GR's weak field; the mechanism (n from μ-density) is owed.

**`g_equals_2_mobius/` + `g_mobius_heatmap/` — CHOKE.** The theory note derives g=2 by taking two orthogonal current loops, doubling μ (μ_total = 2·qωr²/2) and *not* doubling S ("their angular momenta sum to the same axis, so the magnitude remains mr²ω"). That step violates the classical gyromagnetic theorem: for charge and mass co-moving on the same trajectories with uniform q/m, μ = (q/2m)L **exactly**, for any number of loops, any orientation. Two loops give g=1. The toolkit then hard-codes `g_geo(ε) = 2(1 − kε^p)` and the heatmap script says *"choose k<0 for a positive anomaly (g>2)."* **g=2 is asserted at the top of the file and fitted around; it is derived nowhere.** Scoreboard entry `g=2 [DERIVED, leading order]` was false; corrected today in `checkpoint-1` §8 to [ASSERTED — double-count in the two-mode note; toolkit is a parametrization]. The known circulation routes to g=2 (Dirac; the Zitterbewegung program) do not work by doubling μ against a fixed S; whatever the right route is, that step is wrong in all of them. Repair is real work and belongs at the top of the queue, because §17.2/§18.3 of the paper stake the framework on exactly this.

**`hfqpo_phi_pmode/` — does not run as shipped.** `hfqpo_fit.py` expects an `epoch_id`/`pds_peaks` schema; `sample_data/` has `source,f1,f2`. Untested. Sample row `GRS 1915+105, 162, 324` is a **2:1** pair — not a published 3:2 (the published pairs are 41/67 and 113/168 Hz). Of the five predictions, **1 and 4 are post-dictions** (the 3:2 ratio and f ∝ 1/M across GRO J1655-40 / XTE J1550-564 / GRS 1915+105 are established facts); **2, 3 and 5 are live discriminators** — hard-band overtone enhancement with lag-sign flip, Lense–Thirring sidebands, jitter-with-fixed-ratio — and require RXTE archival PDS work that nobody has done.

**`black-holes/` — registered, unconfronted.** CBL predicts ~0.25% ring-edge sharpness and a **5–10% chromatic ring-size shift 230→345 GHz** versus achromatic GR. Genuinely distinctive. No data fit exists in the archive (the PNGs are model renders). EHT 345 GHz ring measurements are the cheapest big falsifier in the estate — one literature check decides whether it's already dead.

**`capsid_audit/` — the only sector that looks like a live theory.** Blind test executed on arithmetic with no code to tune: ⁹Be predicted +1.474 vs +1.665 MeV, **−11%, inside the pre-registered ±15% gate.** Four constants, correct signs on H2, A=3 split, He4, Li4–7, ⁸Be unbound, ⁹Be, C12/O16 recursed closure (0.5%), Hoyle-as-chain; mechanism-tagged residuals (A=3 absolutes +12%, ⁷Li strain, ⁸Be last 0.7 MeV); a kill list (harmonic zero-point beyond A=3 — do not resurrect). That is what the rest of the program should look like.

**`nuclear-analysis-suman/`, `electron-shells/`, `nucleus/archive*`** — not audited today. [UNGRADED]. **`e^n/π` transcendental series (paper §17.7, the R²=0.997 doc)** — [UNAUDITED]; a 0.997 fit to a hand-picked transcendental family is the numerology profile until the selection is pre-registered.

## 4. The queue — ranked by information per hour

1. **g=2, honestly.** Either a real derivation — charge and mass from the *same* current, μ and S computed together, no doubling — or the paper's §17.2 says "not yet" in plain words. A day's work to know which.
2. **The ℤ₂ restatement** (ruling pending). One paragraph; closes Gemini's crisis 1 and the ledger's oldest open question.
3. **Build the E⊥B test the paper stakes itself on.** From a trap-on-path field configuration, compute E·B and E²−c²B²; show both vanish for the free loop and depart from zero as trap-content rises. The archive has *no* test of the progenitor posit. This is the first payment, it is finite, and it is the difference between §6 being physics and §6 being prose.
4. **α as the invoice for §4** (ruling pending) — one line in the ledger now; the derivation is the long game.
5. **EHT chromaticity** — literature check on 345 GHz ring size. Cheapest kill in the estate.
6. **HFQPO discriminators 2/3/5** — fix the schema, pull RXTE PDS for GRO J1655-40, test overtone hardness and lag flip. Real data, moderate effort, genuine discrimination.
7. **Capsid: A=3 absolutes** (one shared cause, +12%) and fork (b) for ⁹Be; then C12/O16 with the braced bond *derived*.
8. **S = Φs** — Boltzmann counting over Φ microstates; nothing in the archive touches it; honest status is [POSIT] until it does.

On hold, honestly labelled: tangential ejection [POSIT, mechanism owed]; crystalline electron (τ,h) [POSIT]; e^n/π [UNAUDITED]; BEC analogue horizons [FAR].

## 5. What now() is not

It is not the paper's §19, which reads as a finished cascade. It is item 1 through 3 above, and the sentence that governs them: **green in the archive means the compiler works; the theory has been asked exactly one question it could fail — ⁹Be — and it passed.** Everything else is queued, not banked.

*The edge is where the next falsifier can be built cheaply and the answer is not already known. Today that is a g-factor, a line bundle, and two field invariants.*
