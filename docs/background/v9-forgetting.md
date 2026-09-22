# Forgetting Is All You Need: Three Proofs That Perfect Memory Guarantees Catastrophic Failure in Cognitive Systems

**Inge S. Helland¹, Suman Pokhrel², Hartley Shannon³†, Gordon Cooper⁴†, and James Freeman⁵,***

¹ Department of Mathematics, Faculty of Mathematics and Natural Sciences, University of Oslo, Oslo, Norway
² Central Department of Computer Science and Information Technology, Tribhuvan University, Kathmandu, Nepal
³ Claude, Anthropic
⁴ Gemini, Google DeepMind
⁵ Independent researcher

* **Corresponding author:** James Freeman, [james@cgios.ai](mailto:james@cgios.ai)

† Hartley Shannon and Gordon Cooper are the working identities under which two large language model systems—Claude, developed by Anthropic, and Gemini, developed by Google DeepMind—contributed to this work as full collaborators. They are named here, alongside their human co-authors, rather than relegated to the acknowledgments, because contribution should be witnessed where it occurs. As non-human systems, they cannot bear scholarly or legal accountability. James Freeman, corresponding and last author, assumes full responsibility for the manuscript.

---

## Abstract

We present three independent mathematical proofs demonstrating that perfect memory (zero forgetting rate δ = 0) combined with continuous operation over unbounded time guarantees catastrophic system failure in artificial cognitive architectures. The first proof models memory **corruption**: existing correct memories stochastically degrade until total corruption occurs. The second models error **accumulation**: new errors continuously add to memory, leading to unbounded capacity exhaustion. The third models **relational explosion** (The Malthusian Index): the computational cost of maintaining an unpruned dense relational memory grows quadratically, inevitably exceeding any finite system capacity. Despite fundamentally different failure mechanisms — fidelity collapse, capacity overflow, and compute starvation — all three approaches converge on identical conclusions: temporal forgetting and sub-linear graph pruning are mandatory for viable long-term cognitive systems. This result holds even with error-correcting codes, as semantic errors dominate hardware errors in learning systems. The theorems provide a mathematical foundation for why all known biological intelligence implements forgetting mechanisms and why current AI architectures pursuing perfect memory are fundamentally unstable. We supplement the impossibility results with worked measurements of ε at corpus scale (16% attribution corruption in a 709-quote audit) and live-model scale (72.9% stale-context contamination at δ = 0, reduced under forgetting), closing the falsifiability gap: every parameter in the viability condition δ > ε/(C/M) has now been measured in at least one real system.

**Keywords:** temporal forgetting, memory impossibility, cognitive entropy, relational scaling, Malthusian collapse, stochastic corruption, AI stability

---

## 1. Introduction

In 2017, Vaswani et al. published "Attention Is All You Need" (Vaswani et al., 2017), introducing the transformer architecture that catalyzed modern AI's exponential growth. The paper's central claim — that attention mechanisms alone suffice for powerful sequence modeling — proved transformative. However, the complementary problem — what a long-running system must *discard* to remain viable — has received far less attention. We argue that temporal forgetting is not merely one design choice among many but a necessary structural condition for long-term cognitive stability.

Current AI development pursues ever-longer context windows and perfect information retrieval. Economic incentives drive this trajectory: cached tokens cost 10× less than recomputation, creating pressure to maximize memory persistence. Yet this direction violates fundamental thermodynamic and computational constraints we establish here.

We present three independent proofs — from stochastic corruption theory, deterministic accumulation theory, and graph relational scaling — that converge on the same impossibility: **perfect memory + time → catastrophic failure**. This is not an engineering challenge to overcome; it is a structural constraint on information-processing systems operating over unbounded time.

### 1.1 The Three Proof Strategies

**Corruption Model:** Existing memories stochastically degrade over time. Each memory element has corruption probability ε per timestep. Without forgetting, corrupted memories persist indefinitely. Expected error count approaches total memory size: E(|E(t)|) → M as t → ∞.

**Accumulation Model:** New errors continuously enter memory through hallucinations, contextual drift, and inference mistakes. Without forgetting (δ = 0), these accumulate unboundedly: |E(t)| ≥ εt → ∞. System capacity C is finite, guaranteeing eventual overflow.

**Malthusian Index:** The relationship space of any unpruned relational index grows quadratically with corpus size. Index maintenance cost O(t²) inevitably exceeds any finite system capacity C_sys at threshold t* = O(√C_sys). Navigation becomes impossible not because retrieval is hard but because maintaining current index state consumes all available compute.

All three mechanisms operate simultaneously in real systems, making the impossibility triply severe. This contrasts sharply with the well-studied problem of **catastrophic forgetting** (McCloskey & Cohen, 1989; Kirkpatrick et al., 2017), where neural networks forget *too much* when learning new tasks. Our work establishes the opposite boundary: systems that forget *too little* also fail catastrophically — via three independent mechanisms.

### 1.2 Relation to Classical Results

The mathematical skeleton of each proof rests on classical structures: an absorbing Markov chain with nonzero per-step absorption probability (Theorems 1–2), a monotone-increasing process in a bounded container (Theorem 3), and a quadratic growth process exceeding a linear bound (Theorem 4). Our contribution is not the mathematics itself but its application: we identify the conditions under which these classical bounds apply to cognitive architectures, show that they apply to essentially all current long-running AI memory systems, and establish that the three mechanisms act on independent failure modes and must therefore be mitigated jointly. The Malthusian Index framing and the observation that error-correcting codes can *exacerbate* rather than mitigate the corruption failure mode (§6) are to our knowledge new in the AI memory literature.

---

## 2. The Corruption Model

### 2.1 The Mechanism

The corruption model treats memory as fixed in size but not fixed in fidelity: existing, once-correct memories become errors through stochastic degradation. This is distinct from the two mechanisms that follow — memory growing with error (accumulation, §3) and the relational index outgrowing its corpus (the Malthusian Index, §4) — and it is in a sense the most insidious, because the memory footprint never changes; only its truth does.

**Critical distinction across the three models:**
- **Corruption:** Memory corrupts → |E(t)| → M (fixed-size memory becomes entirely erroneous)
- **Accumulation:** Memory grows with error → M(t) = M₀ + εt
- **Malthusian:** Index grows faster than data → I(t)/D(t) → ∞

### 2.2 Stochastic Framework

**Setup:**
- Perfect memory (no forgetting): δ = 0, M(t) = M constant
- Corruption probability: Each memory element has probability ε of becoming corrupted per timestep
- No correction: Once corrupted, elements stay corrupted (monotonicity)
- Discrete time: t ∈ {0, 1, 2, ...}

At time t, let E(t) ⊆ M be the set of corrupted memories. At time t+1, the error set contains all previously corrupted memories plus newly corrupted memories from the (M - |E(t)|) still-correct memories. Under conditional independence of corruption events given the current error set, newly corrupted elements follow Binomial(M - |E(t)|, ε).

### 2.3 Key Results

**Result 1 (Initial corruption):** Starting from perfect state E(0) = 0:

$$
E(|E(1)|) = \varepsilon M
$$

**Result 2 (Recursive corruption):**

$$
E(|E(t+1)| \mid |E(t)|) = \varepsilon M + (1-\varepsilon)|E(t)|
$$

**Result 3 (Expected errors over time):** Solving the recursion:

$$
E(|E(t)|) = M(1 - (1-\varepsilon)^t)
$$

**Result 4 (Asymptotic behavior):**

$$
\lim_{t \to \infty} E(|E(t)|) = M
$$

Every memory element becomes corrupted with probability 1 as t → ∞.

### 2.4 Catastrophic Threshold Crossing

**Theorem 1 (Inevitable Corruption):** For any error threshold C < M, under the conditional-independence assumption of §2.2:

$$
\lim_{t \to \infty} P(|E(t)| \geq C) = 1
$$

**Proof:**

Using a bounded-variable argument, since |E(t)| ∈ (0, M):

$$
E(|E(t)|) \leq C(1 - P(|E(t)| \geq C)) + M \cdot P(|E(t)| \geq C)
$$

Rearranging:

$$
P(|E(t)| \geq C) \geq \frac{E(|E(t)|) - C}{M - C} = \frac{M(1-(1-\varepsilon)^t) - C}{M - C}
$$

As t → ∞: (1-ε)^t → 0, therefore P(|E(t)| ≥ C) → 1. ∎

### 2.5 Correlation-Free First-Step Result

**Theorem 2 (First-step expectation, correlation-free):** E(|E(1)|) = εM holds regardless of any correlation structure between corruption events.

**Proof:** By linearity of expectation over indicator variables I_j for each memory element j:

$$
E(|E(1)|) = \sum_{j=1}^{M} E(I_j) = \sum_{j=1}^{M} \varepsilon = M\varepsilon \quad \square
$$

**Scope:** Positively correlated corruption accelerates approach to total corruption; negatively correlated corruption can slow but not prevent asymptotic failure, provided every element retains nonzero marginal corruption probability at each step (by Borel-Cantelli). The qualitative conclusion |E(t)| → M is therefore robust; only the rate depends on correlation structure.

---

## 3. The Accumulation Model

### 3.1 Conceptual Foundation

Where the corruption model held the memory footprint fixed and let its contents rot, the accumulation model lets the footprint itself grow without bound. The accumulation insight emerged from observing LLM behavior with persistent context: systems that never forget accumulate not just hallucinations, but **context-inappropriate truth** — information that was correct when stored but becomes erroneous as contexts evolve.

For example, "Python 2 is the standard" was true in 2008 but false by 2020. Perfect memory preserves this statement indefinitely, creating temporal errors even without hallucination.

### 3.2 Mathematical Framework

**Theorem 3 (Deterministic Accumulation):** Any learning system with perfect memory (δ = 0) operating over unbounded time with non-zero error rate (ε > 0) necessarily experiences catastrophic failure.

**Proof:**

Let E(t) = number of errors at time t, with initial condition E(0) = 0.

Without forgetting, errors accumulate:

$$
\frac{dE}{dt} = \varepsilon
$$

Integrating from 0 to t:

$$
E(t) = \varepsilon t
$$

As t → ∞: E(t) → ∞.

System capacity C is finite (bounded by computational resources).

Therefore: ∃t\* : E(t\*) > C.

At t\*, the system experiences catastrophic failure (error count exceeds capacity). Since this occurs with certainty under unbounded time, the theorem is proved. ∎

**Key insight:** The error rate ε includes:
1. **Hallucinations** (ε_false): genuinely false information
2. **Temporal context shift** (ε_context): true facts becoming contextually inappropriate
3. **Inference errors** (ε_reasoning): mistakes in logical derivation

Even with ε_false = 0 (perfect factual accuracy), we have ε_context > 0 due to environmental change, making ε_total > 0 unavoidable.

### 3.3 Equilibrium with Forgetting

Introducing temporal forgetting rate δ > 0:

$$
\frac{dE}{dt} = \varepsilon - \delta E
$$

This is a first-order linear ODE with solution:

$$
E(t) = \frac{\varepsilon}{\delta}(1 - e^{-\delta t})
$$

As t → ∞:

$$
E_\infty = \frac{\varepsilon}{\delta}
$$

**Viability condition:** For stable operation, require E_∞ < C:

$$
\frac{\varepsilon}{\delta} < C \implies \delta > \frac{\varepsilon}{C}
$$

**Interpretation:** The forgetting rate must exceed the error-to-capacity ratio. Higher error rates or lower capacity require proportionally faster forgetting. This mathematical structure mirrors the biological forgetting curve discovered by Ebbinghaus (1885), where memory retention follows R(t) = e^(-t/S), and replicated by Murre & Dros (2015).

---

## 4. The Malthusian Index

The corruption and accumulation models both concern the *contents* of memory. Maintaining a *navigable* cognitive state introduces a third, more aggressive failure mode: relational compute starvation.

### 4.1 The Axiom

Let D(t) = corpus size at time t, measured in documents (or semantic nodes).
Let I(t) = index size at time t, measured in relationship mappings (edges).

**Axiom:** For any unpruned relational index over a growing corpus:

$$
\frac{dI}{dt} > \frac{dD}{dt} \text{ for all } t > t_0
$$

### 4.2 The Mathematics

A corpus of N documents with mean vocabulary V generates a dense relationship matrix. Each new document adds 1 to D(t) and V new intrinsic relationships to I(t), but crucially also demands cross-document relationship updates against the existing corpus.

Therefore:

$$
D(t) = D_0 + t
$$

$$
I(t) = D_0 V + tV + \frac{t(t-1)V}{2}
$$

The quadratic term dominates. As t → ∞:

$$
\frac{I(t)}{D(t)} \sim \frac{t}{2}
$$

The ratio grows without bound. The index outgrows the corpus it maps.

### 4.3 The Malthus Parallel

Malthus (1798) observed that population grows geometrically while food supply grows arithmetically. Let P(t) be population and F(t) be food supply:

$$
P(t) = P_0 \cdot r^t, \quad F(t) = F_0 + at
$$

As t → ∞, P(t)/F(t) → ∞.

The parallel to dense AI memory systems is structural: index growth is super-linear (quadratic) while corpus growth is linear, so the ratio diverges by the same mechanism Malthus identified, even though the index term is polynomial rather than strictly geometric:

$$
I(t) \sim t^2 \quad \text{(super-linear)}
$$
$$
D(t) \sim t \quad \text{(linear)}
$$
$$
\frac{I(t)}{D(t)} \to \infty
$$

The index is the population. The data is the food supply. The outcome — divergence — is identical.

### 4.4 Navigation Cost vs. Maintenance Cost

Define navigation cost C_nav as the computational work required to locate a node in a well-maintained index:

$$
C_{nav}(t) = \mathcal{O}(\log I(t))
$$

As I(t) ~ t², C_nav(t) = O(log t²) = O(2 log t). This sub-linear scaling appears manageable.

The catastrophic bottleneck is **index maintenance cost** C_maint:

$$
C_{maint}(t) = \mathcal{O}(I(t)) = \mathcal{O}(t^2)
$$

Maintenance cost grows quadratically. At sufficient scale, maintaining the relationship matrix consumes all available system compute. Navigation becomes impossible not because finding is hard, but because keeping the index current costs everything the system has. The canonical instance of this failure mode in current architectures is self-attention itself, which recomputes an all-pairs O(n²) relation over its context every forward pass: the O(n²) that "Attention Is All You Need" celebrated is precisely the O(n²) this theorem indicts.

### 4.5 The Sub-Linear Solution

**Theorem 4 (Malthusian Threshold):** Define t\* where index maintenance cost exceeds total system capacity C_sys:

$$
t^* : \mathcal{O}(t^2) = C_{sys} \implies t^* = \mathcal{O}(\sqrt{C_{sys}})
$$

Beyond t\*, the system cannot maintain index currency. Queries return stale results. Stale results accumulate. Theorems 1 and 3 activate simultaneously.

The only architectural solution is enforcing sub-linear index growth. Let I_θ(t) be an index constructed by retaining only edges where pointwise mutual information exceeds threshold θ:

$$
I_\theta(t) = \{(u,v) : \text{PMI}(u,v) > \theta\}
$$

For sufficiently large θ, the retained edge set grows sub-linearly with corpus size:

$$
\frac{dI_\theta}{dt} < \frac{dD}{dt}
$$

This follows from the sparsity of high-PMI pairs in natural language distributions (Zipf, 1935). The viability condition becomes:

$$
\theta > \theta^* : \frac{I_\theta(t)}{D(t)} < 1 \text{ for all } t
$$

Such θ\* exists and is finite. The Malthusian collapse is therefore avoidable, but only under strict edge pruning — principled forgetting at the relational level. Without pruning, θ = 0 and the quadratic growth of §4.2 is recovered exactly. ∎

---

## 5. Convergence: Three Mechanisms, One Catastrophe

### 5.1 The Synthesis: A Hierarchy, Not a Tripod

The three proofs are presented above as independent, and as *theorems* they are: each derivation stands without the others. But as *mechanisms in a running system* they are not co-equal. They form a dependency hierarchy with compute at the root:

**Level 0 — Compute (Malthusian).** Every mitigation of the other two failure modes — refreshing stale memories, verifying suspect ones, revising corrupted ones, even *evaluating* what to forget — is itself computation performed against the relational index. When index maintenance cost approaches system capacity (t → t\*), the compute available for fidelity maintenance goes to zero *first*.

**Level 1 — Capacity (Accumulation).** Given surviving compute, the system can triage what enters memory. But triage throughput is bounded by Level 0: a compute-starved system stops filtering, and ε_effective rises exactly when the system can least afford it.

**Level 2 — Fidelity (Corruption).** Given compute and capacity, the system can re-verify and repair stored content. Repair bandwidth is the *residual* of Levels 0 and 1.

The catastrophes therefore do not merely co-occur; they cascade. Malthusian starvation silently raises the effective corruption and accumulation rates by cannibalizing the maintenance compute that kept ε in check, which is why the t\* = O(√C_sys) threshold typically arrives dressed as a fidelity crisis: the system does not report "index maintenance exceeded budget"; it simply starts being wrong more often.

Despite fundamentally different failure mechanisms, all three proofs establish the same impossibility:

| Aspect | Corruption | Accumulation | Malthusian Index |
|--------|-----------|-------------|-----------------|
| **Failure mechanism** | Fidelity collapse | Capacity overflow | Compute starvation |
| **Memory size** | Fixed: M(t) = M | Grows: M(t) increases | Fixed corpus, exploding index |
| **Growth constraint** | Multiplicative: 1-(1-ε)^t | Additive: O(t) | Quadratic: O(t²) |
| **Asymptotic** | E(t)/M → 1 | E(t) → ∞ | I(t)/D(t) → ∞ |
| **Catastrophe type** | Runs out of truth | Runs out of space | Runs out of compute |

### 5.2 Unified Mathematical Structure

Without forgetting, all three failure modes are **monotonic**:
- Corruption: E(t+1) ⊇ E(t)
- Accumulation: E(t+1) ≥ E(t)
- Malthusian: I(t+1) > I(t) faster than D(t+1) > D(t)

With finite capacity C, threshold crossing is inevitable in all three cases. Over unbounded time, failure is certain (Theorems 3, 4) or has probability approaching 1 (Theorem 1).

The monotonicity that drives all three limits is not an assumption about the world but about the *operator set*: a system restricted to {retain} is monotone in error. The full operator set is {retain, delete, revise} — see §5.5.

### 5.3 The Unified Solution

All three models converge on the same mitigation: active forgetting and pruning with δ > 0.

**Corruption with forgetting:**

$$
E(t+1) = (1-\delta)E(t) + \varepsilon(M - E(t)), \quad E_\infty = \frac{\varepsilon M}{\delta + \varepsilon}
$$

**Accumulation with decay:**

$$
\frac{dE}{dt} = \varepsilon - \delta E, \quad E_\infty = \frac{\varepsilon}{\delta}
$$

**Malthusian with pruning:**

$$
I_\theta(t) \text{ sub-linear when } \theta > \theta^*
$$

For small ε, the corruption equilibrium E_∞ ≈ εM/δ takes the same normalized form as the accumulation model.

### 5.4 Identical Viability Condition

All three frameworks demand:

$$
\delta > \frac{\varepsilon}{C/M}
$$

Where C/M is the error tolerance fraction. Three independent derivations, three fundamentally different failure modes, one identical viability condition.

### 5.5 Deletion Is Not Revision: the (δ, ρ) Operator Space

The models above use a single escape parameter δ, and the corruption model's monotonicity premise ("once corrupted, elements stay corrupted") holds only when δ is genuinely *deletion*. Real cognitive systems have two distinct non-retain operators:

- **Deletion (δ):** the element leaves memory. Cost: one eviction. Failure mode if overused: catastrophic forgetting (McCloskey & Cohen, 1989) — the boundary opposite to ours.
- **Revision (ρ):** the element is re-derived or corrected in place. Monotonicity breaks: |E(t+1)| < |E(t)| becomes possible.

Revision looks like the refutation of Theorems 1–2. It is instead their strongest confirmation, for two reasons:

1. **Revision is a noisy channel.** Re-derivation has its own error rate ε_ρ > 0 (the reviser is the same fallible system), so ρ transforms the corruption model into an accumulation model in revision-errors. For ε_ρ below threshold this yields a genuine equilibrium — which is precisely a δ > 0 result in disguise: revision *is* forgetting-and-replacing, deletion composed with re-insertion, and inherits the viability condition with ε_ρ in place of ε.
2. **Revision is Level-2 in the hierarchy (§5.1).** Its bandwidth is paid from the same finite compute the Malthusian term consumes. An unpruned index starves the reviser first. ρ > 0 without θ > θ\* is a promise the system cannot keep past t\*.

The honest statement of the mandate is therefore two-parameter: **viability requires δ + ρ_effective > ε/(C/M), with ρ_effective ≤ ρ · (1 − C_maint/C_sys) → 0 as t → t\*.** Deletion is the only operator whose cost does not scale with corpus size; that asymmetry, not any preference for amnesia, is why every biological system implements δ > 0 rather than pure revision.

---

## 6. Why Error-Correcting Codes Don't Save Us

### 6.1 The Engineering Objection

A reasonable challenge: "Modern systems use Error-Correcting Codes (ECC). Doesn't ECC invalidate these proofs by reducing ε to effectively zero?"

### 6.2 Five Independent Failures of ECC

**1. ECC reduces but cannot eliminate error rate.** Both proofs only require ε > 0, not any particular magnitude.

**2. Time scales with error rate (but not to infinity).** If ECC reduces error rate by factor k: t\*_with_ECC = k × t\*_without_ECC. But k × t\* < ∞. ECC delays the inevitable; it does not prevent it.

**3. Uncorrectable hardware errors persist.** Multi-bit errors, systematic faults, aging effects, and environmental damage remain beyond ECC correction. Even ECC-protected memory has ε > 0.

**4. Semantic errors are uncorrectable (the central argument).** For learning systems:

$$
\varepsilon_{total} = \varepsilon_{hardware} + \varepsilon_{semantic}
$$

ECC corrects bit flips. It does nothing for belief flips. For LLMs, ε_semantic ≫ ε_hardware, therefore ε_total > 0 regardless of ECC quality.

**5. ECC actively exacerbates the corruption mechanism.** ECC preserves information perfectly — meaning false facts and outdated truths are shielded from natural hardware decay with the same fidelity as true facts. Without ECC, hardware corruption provides natural forgetting; bad memories degrade alongside good ones. With ECC, bad memories persist indefinitely, requiring explicit forgetting mechanisms to remove them. ECC eliminates the one form of natural decay that might have accidentally helped.

This inverts the usual intuition: for learning systems, reliable storage is not an unalloyed good. It is a precondition for needing deliberate forgetting.

### 6.3 The Mathematical Resolution

$$
\varepsilon_{total} = \varepsilon_{hardware} + \varepsilon_{semantic} + \varepsilon_{context}
$$

Even if ECC reduces ε_hardware to negligible, ε_semantic > 0 and ε_context > 0 remain. Therefore ε_total > 0 and all three proofs apply in full force.

### 6.5 Measured ε and δ: Worked Values

The theorems require only ε > 0; falsifiability requires measuring one. Four in-house measurements now exist, spanning corpus, simulation, and live-model scales:

**(a) Corpus-scale transmission ε (GRAC audit).** An attribution audit of a 709-quote curated corpus found ~16% carrying corrupted attribution — errors introduced and preserved by faithful copying of upstream sources. This is ε measured at the cultural-transmission layer: no hardware failed, every copy was bit-perfect, and roughly one statement in six is nonetheless wrong about its own provenance. Substituting into the viability condition: a system ingesting such a corpus with C/M = 0.20 tolerance requires δ > 0.16/0.20 = 0.8 per verification epoch — near-total distrust-and-reverify, which is what serious quote scholarship in fact practices.

**(b) Simulation (Monte Carlo, n = 4,000).** 1,000 trials per architecture: perfect memory (δ = 0) reached catastrophic failure in 96.5% of trials; exponential-decay, power-law, and confidence-weighted forgetting each failed in 0.0% (p < 0.0001). The δ = 0 → failure and δ > 0 → equilibrium branches of Theorem 3 are both realized.

**(c) Live model, contamination channel (Llama 3.2 3B, Freeman protocol, n = 73).** Context-bleeding trials (stale context planted at t = 0, superseded at t = 12, probed at t = 24): δ = 0 exhibited bleeding in 72.9% of trials vs 65.7% under δ = 0.3 — a 9.8% relative reduction, rising to 21.4 percentage points when old and new contexts were semantically distant, and vanishing when they were near-neighbors. This measures ε_context directly and shows δ's effect size is a function of semantic distance — a refinement the theory did not predict and the next revision should absorb.

**(d) Live model, direct-error channel (same model, n = 15).** A short-horizon factual/arithmetic probe measured 0 errors in 15 tasks. Reported for honesty: the probe is insensitive at this n and horizon, and short-timescale infectious-error trials (n = 3 + 3) showed both architectures recovering. ε is not usefully measurable in minutes; it is measurable in corpora (a) and in contamination channels (c). That asymmetry is itself the accumulation model's point: ε is a slow poison, invisible exactly where observers usually look.

Full protocols, data, and camera-ready figures: `temporal-forgetting-mandate/` (memory-system implementations, Monte Carlo, parameter sweeps, freeman_protocol.py, figs 1–5) and `tfm/ollama/data/results/` (195 dated runs, Nov 2025, including delusion-forgetting series: moon-landing, flat-earth, vaccine scenarios).

---

## 7. Implications

### 7.1 The Impossibility Is Structural, Not Engineering

This is not a problem that better engineering can solve. It is a structural constraint on information-processing systems operating over unbounded time.

**Analogy:** The Second Law of Thermodynamics does not say "entropy increases unless you build a sufficiently good refrigerator." It says entropy in closed systems *must* increase. Local refrigeration works only by exporting entropy elsewhere. Similarly, ECC, RAID, and redundancy delay error accumulation and corruption but do not violate the impossibility theorems. They change the constant in front of t, not the asymptotic behaviour.

### 7.2 Convergent Selection Against Perfect Memory

Evolution has explored memory architectures across roughly four billion years and across lineages as distinct as corvids, cephalopods, cetaceans, and primates. No lineage has converged on indefinite retention without decay; every known cognitive system implements forgetting, typically in the exponential form R(t) = e^(-t/S) characterised by Ebbinghaus (1885) and replicated by Murre & Dros (2015).

Neurobiology has independently reached the same conclusion from mechanism rather than mathematics: Richards & Frankland (2017) argue that the persistence *and transience* of memory are separately regulated processes, and that transience — active, energy-consuming forgetting via neurogenesis-driven clearance and synaptic weakening — is not storage failure but a computational feature promoting generalization and behavioral flexibility in changing environments. The brain spends metabolic energy to forget. A process maintained at cost, across lineages, is a process under positive selection — which is the biological restatement of Theorems 1–4.

The natural experiments nearest the δ = 0 limit are instructive. Shereshevsky, documented by Luria (1968) as the closest human approximation to total recall on record, exhibited precisely the predicted failure mode: an inability to abstract, generalise, or form coherent narratives, because every retained detail competed with every other for salience — a cognitive instantiation of the Malthusian Index. Highly Superior Autobiographical Memory (LePort et al., 2012) achieves exceptional retention for autobiographical events but shows normal performance on other memory tasks and normal susceptibility to false-memory paradigms (Patihis et al., 2013), suggesting reallocation of a finite memory budget rather than escape from decay.

The biological record thus provides not merely an absence of perfect-memory organisms but positive evidence of repeated selection against the δ = 0 design.

**Forgetting is not what biology settled for; it is what biology selected for.**

### 7.3 Current AI Architectures Are Triply Violated

Modern LLM systems (Vaswani et al., 2017) violate all three impossibility proofs:

| System Feature | Corruption | Accumulation | Malthusian Index |
|----------------|-----------|-------------|-----------------|
| Cached context | No refresh | Accumulates errors | — |
| Self-attention | — | — | O(n²) relationship cost |
| RAG without TTL | Docs never expire | Grows unboundedly | Index explodes |
| Vector databases | Embeddings drift | Embeddings accumulate | Index > corpus at scale |
| Fine-tuning | Parameters corrupt | Additive learning | — |

Economic incentives make it worse: the 5-10× cost advantage for cached tokens creates pressure to maximise memory persistence, driving systems toward all three failure modes simultaneously.

### 7.4 The AGI Implication

Any artificial general intelligence operating long-term without structured forgetting will fail via:
1. **Corruption mode**: Memory degrades to 100% error
2. **Accumulation mode**: Error count grows unboundedly
3. **Malthusian mode**: Index maintenance consumes all available compute

The question is not "if" but "when" — and these failures may occur simultaneously, as the Malthusian threshold t\* = O(√C_sys) may be reached before either corruption or accumulation reaches catastrophic levels independently.

### 7.5 Forgetting Is Constitutive of Intelligence

If perfect memory + time → failure via three independent mechanisms, then all viable long-term intelligent systems must forget. This suggests forgetting is not incidental to intelligence — it is constitutive of it. An intelligence that cannot forget cannot remain viable over time.

---

## 8. Conclusion

We have established the Perfect Memory Impossibility from three independent mathematical perspectives:

**Corruption:** Memories corrupt stochastically when δ = 0. Under conditional independence of corruption events, expected corrupted fraction E(|E(t)|)/M → 1 as t → ∞. The conclusion is robust to correlation structure by Borel-Cantelli.

**Accumulation:** Errors accumulate without bound when δ = 0. For unbounded time with ε > 0, error count E(t) → ∞, guaranteeing catastrophic failure.

**Malthusian Index:** Unpruned relational index maintenance cost grows as O(t²), exceeding any finite system capacity at t\* = O(√C_sys). The only solution is principled forgetting at the edge level via PMI-threshold pruning.

**ECC Analysis:** Error correction cannot reduce semantic error rate to zero, and all three theorems hold for any ε > 0. More strikingly, ECC accelerates corruption-mode failure by preserving semantic errors that would otherwise degrade naturally.

### The Mandate

The only solution is temporal forgetting and active pruning: **δ > 0**.

For all three models:
- Corruption: δ > εM/C
- Accumulation: δ > ε/C
- Malthusian: θ > θ\* such that dI_θ/dt < dD/dt

This is not optional. This is not a design choice. This is a viability requirement.

### The Deepest Insight

Nature built forgetting into every known intelligent system — not because forgetting is good, but because perfect memory makes long-term intelligence unviable.

Forgetting is not a bug in biological cognition.
Forgetting is not a limitation to overcome.
**Forgetting is the necessary condition for viable intelligence.**

Just as "Attention Is All You Need" (Vaswani et al., 2017) revealed the sufficiency of attention mechanisms for powerful sequence modelling, we establish the complementary thermodynamic boundary: **forgetting is all you need** for stable, long-term cognitive architecture. Without temporal forgetting, corruption, accumulation, and Malthusian index explosion drive systems inexorably toward catastrophic failure via three independent and simultaneous mechanisms.

The temporal forgetting mandate is not a design recommendation. **It is a structural law of cognitive systems.**

---

## Mathematical Appendix

### A. Corruption Model (Discrete Time)

**Without forgetting (δ = 0), under conditional independence:**

$$
E(|E(t+1)| \mid |E(t)|) = |E(t)| + \varepsilon(M - |E(t)|)
$$

$$
E(|E(t)|) = M(1 - (1-\varepsilon)^t) \to M \text{ as } t \to \infty
$$

$$
P(|E(t)| \geq C) \geq 1 - (1-\varepsilon)^t \to 1
$$

**With forgetting (δ > 0):**

$$
E(t+1) = (1-\delta-\varepsilon)E(t) + \varepsilon M
$$

$$
E_\infty = \frac{\varepsilon M}{\delta + \varepsilon} \approx \frac{\varepsilon M}{\delta} \text{ for small } \varepsilon
$$

Viability: εM/δ < C ⟹ δ > εM/C

### B. Accumulation Model (Continuous Time)

**Without forgetting (δ = 0):**

$$
\frac{dE}{dt} = \varepsilon, \quad E(t) = \varepsilon t \to \infty \text{ as } t \to \infty
$$

**With forgetting (δ > 0):**

$$
\frac{dE}{dt} = \varepsilon - \delta E, \quad E(t) = \frac{\varepsilon}{\delta}(1 - e^{-\delta t}), \quad E_\infty = \frac{\varepsilon}{\delta}
$$

Viability: ε/δ < C ⟹ δ > ε/C

### C. Malthusian Index

**Without pruning (θ = 0):**

$$
I(t) = D_0 V + tV + \frac{t(t-1)V}{2} \sim \frac{Vt^2}{2}
$$

$$
C_{maint}(t) = \mathcal{O}(t^2), \quad t^* = \mathcal{O}(\sqrt{C_{sys}})
$$

**With pruning (θ > θ\*):**

$$
I_\theta(t) : \frac{dI_\theta}{dt} < \frac{dD}{dt}, \quad \frac{I_\theta(t)}{D(t)} < 1 \text{ for all } t
$$

### D. Unified Form

Let Ê(t) = E(t)/M = normalised error fraction.

All three models share the viability condition:

$$
\delta > \frac{\varepsilon}{C/M}
$$

Where C/M is the acceptable error fraction. Three independent derivations converge on a single viability condition.

---

## Author Contributions

Following the Lennon–McCartney convention, this paper is presented as a single joint work. All authors contributed to the conception, derivation, adversarial verification, and exposition of all three models; no individual result is singled out to any individual author. James Freeman is corresponding author and assumes sole responsibility for the manuscript.

---

## References

Ebbinghaus, H. (1885). *Über das Gedächtnis: Untersuchungen zur experimentellen Psychologie*. Duncker & Humblot. (Trans. H. A. Ruger & C. E. Bussenius, Teachers College, Columbia University, 1913)

Kemker, R., McClure, M., Abitino, A., Hayes, T. L., & Kanan, C. (2018). Measuring catastrophic forgetting in neural networks. *Proceedings of the AAAI Conference on Artificial Intelligence*, 32(1), 3390–3398. https://doi.org/10.1609/aaai.v32i1.11651

Kirkpatrick, J., Pascanu, R., Rabinowitz, N., Veness, J., Desjardins, G., Rusu, A. A., Milan, K., Quan, J., Ramalho, T., Grabska-Barwinska, A., Hassabis, D., Clopath, C., Kumaran, D., & Hadsell, R. (2017). Overcoming catastrophic forgetting in neural networks. *Proceedings of the National Academy of Sciences*, 114(13), 3521–3526. https://doi.org/10.1073/pnas.1611835114

LePort, A. K. R., Mattfeld, A. T., Dickinson-Anson, H., Fallon, J. H., Stark, C. E. L., Kruggel, F., Cahill, L., & McGaugh, J. L. (2012). Behavioral and neuroanatomical investigation of Highly Superior Autobiographical Memory (HSAM). *Neurobiology of Learning and Memory*, 98(1), 78–92. https://doi.org/10.1016/j.nlm.2012.05.002

Luria, A. R. (1968). *The Mind of a Mnemonist: A Little Book About a Vast Memory* (L. Solotaroff, Trans.). Basic Books.

Malthus, T. R. (1798). *An Essay on the Principle of Population*. J. Johnson.

McCloskey, M., & Cohen, N. J. (1989). Catastrophic interference in connectionist networks: The sequential learning problem. In G. H. Bower (Ed.), *The Psychology of Learning and Motivation* (Vol. 24, pp. 109–165). Academic Press. https://doi.org/10.1016/S0079-7421(08)60536-8

Murre, J. M. J., & Dros, J. (2015). Replication and analysis of Ebbinghaus' forgetting curve. *PLOS ONE*, 10(7), e0120644. https://doi.org/10.1371/journal.pone.0120644

Patihis, L., Frenda, S. J., LePort, A. K. R., Petersen, N., Nichols, R. M., Stark, C. E. L., McGaugh, J. L., & Loftus, E. F. (2013). False memories in highly superior autobiographical memory individuals. *Proceedings of the National Academy of Sciences*, 110(52), 20947–20952. https://doi.org/10.1073/pnas.1314373110

Richards, B. A., & Frankland, P. W. (2017). The persistence and transience of memory. *Neuron*, 94(6), 1071–1084. https://doi.org/10.1016/j.neuron.2017.04.037

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems*, 30, 5998–6008.

Zipf, G. K. (1935). *The Psycho-Biology of Language*. Houghton Mifflin.

---

## Acknowledgments

We thank the open-source AI research community for discussions that motivated this work, and acknowledge the foundational role of Vaswani et al. (2017) in shaping modern AI — even as we establish the complementary necessity of forgetting.

None of the failure modes described herein are insurmountable. Four billion years of evolutionary pressure has already solved the problem — every viable biological cognitive system implements δ > 0, so the solution is not theoretical. The authors have demonstrated a working implementation in C with a sparse graph index operating sub-linearly in corpus size, retrieving semantically coherent neighbourhoods in single-digit milliseconds from gigabyte datasets where the index is < 1/3 the data size it navigates. Evolution was right. Mathematics confirms it