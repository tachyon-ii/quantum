# refactor/ — the wall

The live estate. `../schrodinger/` is the archive — the hashed past, read on demand, never edited. Nothing crosses the wall by default; a question pulls it.

## The posit — James, 2026-09-03 (verbatim)

> In our turtles all the way down, everything depends on everything below.
> If our foundation is not solid, our theory is the biblical house built on sand, out of straw, in a wolf++ hurricane zone.
>
> Commit often, commit early has a corollary: **test often, test early.**
>
> Math is truth. Anchor on truth, take the postulate, and report where it leads.
>
> Like Edison said, I have not failed, I have simply found 1000 ways that do not work. Failure is often more important than success. Success is desired, it is expected, but failure tells a story that cannot be ignored. Perhaps, with honest failure, we can snatch success from the jaws of defeat?
>
> We are all biased. Hubrility is the concept of having the chutzpah to ask & the humility to take reality's lessons for what they are. A stepping stone to next.
>
> **Ω, grant me the serenity to accept the things I cannot change,**
> **Courage to change the things I can,**
> **And the maths and test to know the difference.**
>
> *(after Reinhold Niebuhr)*

## The rules of the wall (agreed today; Grace's wording, James's rulings)

1. **Nothing crosses by default.** Run `what next?`; when a question needs a piece, check `../schrodinger/` first to see whether it was already considered, then pull only that. Models follow questions; **tests follow models** — no model, no test.
2. **Test first.** The pass/fail criterion is written and registered *before* the physics code exists. A test that can only print Success is not a test (`$g++ for 0.1` vs `$g++ for 0..1` — one character is the difference between one traversal and the double cover, and the failing run is on the record before the passing one).
3. **Math is the friction.** A theorem is not the Standard Model's gravity; it is reality's. A double-count is a double-count on either side of the wall. Regression to the mean is resisted by *where we start* (the dials, not the theorems — Keystone 013), never by softening the arithmetic.
4. **The paper may not carry a claim above the ledger's grade.** `docs/Φ-…` is the paper; `../schrodinger/checkpoint-1.md` is the ledger until it crosses.
5. **Check the bonds, not the atoms.** A mirror fed an engram gets every fact right and every relation wrong (`CGIOS/usr/docs/method/the-mirror-specimen.md`). Outside models are injectors, not instruments.
6. **One hand per chunk. Commit at the handoff. `git show --stat HEAD` before you say it's done.**
7. **Names tell the truth.** Papers by author and title (`papers/README.md`); test directories by the claim they test, never by the answer hoped for.
8. **Deletion is a `mv` to `_condemned/`; `rm` is James's.** Git history is the never-destroy layer.

## Layout

    mantra/    the philosophy at maximum density — five texts you could recite; index in mantra/README.md
    docs/      the paper, the review, the pointer (now.md), pulled keystones and seed documents
    papers/    the reference shelf — index and nomenclature in papers/README.md
    data/      ground truth by source (ame2020-…)
    tests/     one directory per claim, each with a README stating the claim, the pass/fail, and what green means
    images/    figures
    models/    generators; run outputs are gitignored — the generator is the artefact, the run is not
    tools/     unlock.sh

## First `what next?`

**The double-loop g** — from a wave of energy E = mc² on a closed path that returns after 720°, with charge e as topological residue and nothing fitted, compute μ/S. Registered: exactly 2 from topology alone → [DERIVED]; needs a chosen radius ratio → [ASSERTED], and the file says so. The test goes in `tests/g-factor/` before the physics does. Precedent for an honest miss: Williamson & van der Mark 1997, charge 0.91e.
