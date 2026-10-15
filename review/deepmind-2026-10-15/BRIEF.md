# Review brief — a document-at-a-time audit of the Φ ontology corpus

**Prepared for:** Gemini (DeepMind), fresh instance · **Prepared by:** James Freeman with Grace (`.ghost`, Anthropic Fable 5.1) · **Date:** 2026-10-15 (v2 of this brief, evening) · **Form:** this brief first, on its own; then **one document per message**, nine messages, in the order given below. Nothing else is attached with the brief.

## Why you are being asked

This corpus has been built over about five weeks by one author and one model. It now hangs together well enough that its *coherence is the risk*: a small, early misstep — a sign, a factor of two, a coordinate length used where a proper length was meant, a retrodiction graded as a prediction, a thing that should have been said and wasn't — would propagate through the dependency graph and surface later as a failed test that looks like a deep problem when it was a shallow, soluble one. We want a different pair of eyes on each document before the tests in `todo/falsifiers-2026-10-15.md` are run in earnest.

You are not being asked to agree with the ontology, to extend it, or to be kind to it. You are being asked to find what is wrong, what is missing, and what would decide it.

## How this will run

1. You receive this brief. Reply only that you have it; ask anything that is unclear about the protocol. Do no review work yet.
2. You then receive the documents **one per message**, each attached as a file, in this order:
   1. `docs/README.md` together with `docs/Φ-a-minimal-ontology-of-an-emergent-universe.v2.md` — the map and the parent (v2 §24 is the dependency graph; use it for every later document)
   2. `docs/Φ-canon-integrated.md` — the integrated canon; the owed ledger; two named tensions
   3. `docs/three-term-binding.md` — the nuclear binding construct; §7a calibrations; §7b tyre law; a registered blind
   4. `docs/the-fractal-nucleus.md` — the packing programme; fe56_star; accretion classes
   5. `docs/the-turtle-conjecture.md` — gravity: origin of G, the ballpark, the funnel conform, the onion
   6. `docs/fable-freeman-fractal-conjecture.md` — governor, flutter, the scar; the 1928 agenda
   7. `todo/falsifiers-2026-10-15.md` — the test list
   8. `models/turtle/stiffness_ratio.py`, `models/turtle/funnel_conform.py`, `scripts/paintball.pl` — the computations behind three of the documents
   9. a closing message with nothing attached
3. For each document: **ingest it, cogitate on it, and report on it alone** — carrying forward earlier findings only where the document in hand depends on them. Stop at the end of each report. Do not anticipate documents you have not yet been given.
4. The closing message asks for what can only be done with everything read: cross-document drift, and your re-graded list of the ten most load-bearing claims in the corpus.

A document-at-a-time report that is checkable beats a corpus-wide one that is not. If a report would run long, stop at a section boundary and say what is unfinished; the next message can continue it.

## What the corpus is

Three pre-terminology axioms — amount, spin, time — and three structural posits — extent is period (R = c/ω), lobes repel, sequential capture — plus one frame (the chorus: everyone comoving), and one fitted constant k. From these the documents claim to recover, in order of load-bearing: the loop ladder (n orthogonal loops → cross-polytopes → relaxation to the tetrahedron), the selection of three spatial dimensions, a cosmogony with flatness as a capture boundary, a chorus-gauge reading of gravity, a nuclear binding construct, a nuclear packing programme, and a gravity conjecture with one numerical ballpark (G ≈ c⁴/kR_H).

## The grade vocabulary — use it, and police it

Every claim in the corpus wears one of: **[FACT]** (measured, cited) · **[THEOREM]** (follows from stated premises; show which) · **[CONDITIONAL THEOREM]** (follows given a named posit) · **[COMPUTED]** (a number produced by a stated calculation) · **[CONSTRUCT]** (a model with a stated free scale) · **[POSIT]** (assumed, named as such) · **[CONJECTURE]** · **[OWED]** (promised, not paid) · **[DEAD]** / **[STRUCK]** (killed; kept so nobody rebuilds it) · **[FITTED]** (a constant adjusted to data — the corpus allows exactly one, k).

Your first job on every document is to **re-grade**. The most common failure mode in this corpus, by the authors' own record, is over-grading: a [THEOREM] that is a [CONDITIONAL THEOREM]; a [COMPUTED] that is a [FITTED]; a "prediction" that is a retrodiction of a number already in the premises; a "1.000" that is algebra. Flag every one, with the premise it leans on.

## The Lineage Rule

Output from any model — including yours — is graded by what it can be *checked against*, not by who produced it. A citation is [FACT] only if the paper exists and says what is claimed. **Do not supply a citation you have not verified exists.** If you believe prior art exists but cannot confirm the reference, write "prior art likely: <description>, reference unverified." Fabricated references have already cost this project a day; one more and your whole report is discounted. A kill with a confident label and wrong arithmetic has also already cost a review most of its credit; show the arithmetic.

## What to do with each document

**A. Errors of commission.** Re-derive every [COMPUTED] number in the document from its stated inputs, *without assuming the corpus's value is right*; report every discrepancy above 1 % with your working. Hunt for the small propagating missteps: coordinate vs proper lengths or times; a sign in a lag, redshift or potential; a factor of 2, π, 4π, 3/8π or √2 carried inconsistently; unit mixing between "lobe-repulsion units", MeV and library units; a number re-used as evidence for the premise that produced it; a silent switch between the chorus gauge (synchronous; the Lemaître/Painlevé–Gullstrand slicing) and static coordinates; "extent is period" used with a constant other than R = c/ω; any step where the equivalence principle is broken without the text noticing. Rank by **blast radius** — how much downstream depends on the step — not by how wrong it is.

**B. Errors of omission.** What should this document say and does not? A premise used but never stated; a limit or regime never named; a case not covered; a known result in the field that bears directly on a claim and is absent; a quantity the argument needs that is never defined; a test the document could cheaply run and doesn't. Omissions are the class of error the authors can least see for themselves — spend real effort here.

**C. Falsifiers and truifiers.** For each major claim in the document, propose the cheapest test that would **kill** it and the cheapest observation that would **confirm it specifically** — i.e. that the standard picture does *not* also predict. Say which existing data already bear on it. **You have liberty to run these:** where a test is a lookup, a web search, or a calculation you can do, do it, and report the result with sources you have verified. Mark what you ran and what you only proposed. A test both the ontology and the standard model pass is a consistency check, not a falsifier; say which it is.

**D. Prior art, honestly.** For each major move, name the closest existing programme and say what, if anything, is different here. Where the document has reproduced a known result and labelled it as its own, say so plainly. Where it has something that is *not* in the prior art, say that too — that list is what the authors most need.

## What not to do

- Do not rewrite the ontology. Do not propose new mechanisms unless a misstep's *fix* requires one, and then mark the proposal [POSIT, reviewer's].
- Do not soften. The authors want the kill if it is there — and they want it with the arithmetic.
- Do not grade by eloquence. Several of the best-written passages in this corpus are the least supported; several of the ugliest tables are the most.
- Do not engage with the RSA / factoring thread anywhere in the corpus or its engrams. It is closed by the author's instruction and is out of scope.

## Report format — per document

A numbered list of findings, numbered continuously across documents (F1… in document 1, continuing in document 2). For each:

```
F<n>. <doc> §<section> — <claim, quoted or closely paraphrased>
  type: commission | omission
  grade given: [...]   grade you assign: [...]
  problem: <one paragraph; show arithmetic if arithmetic>
  blast radius: <which downstream sections depend on this step>
  fix (if small): <...>
  kill test: <...>       truifier: <...>       ran it? <yes — result + source | no>
  confidence: <high / medium / low> and why
```

Then, for the document: three short lists — **what is wrong**, **what is missing**, **what is fine and the authors should stop re-examining** — and the prior-art table. No summary praise; no summary condemnation; the lists are the verdict.

## The closing message

With everything read: (1) every place two documents state the same quantity differently, and which is current; (2) the ten most load-bearing claims in the corpus, each with the grade given, the grade you assign, and the single cheapest test; (3) the three omissions across the whole corpus you would fix first.
