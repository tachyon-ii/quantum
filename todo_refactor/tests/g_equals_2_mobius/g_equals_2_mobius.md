# Möbius Two-Mode g-Factor — Theory

## Overview

This document states the assumptions and derivation of the **g = 2** prediction in the Möbius-locked two-mode internal motion model, and outlines how simple “relativistic-style” adjustments shift that result.

The executable demonstration and variant exploration are in [`g_equals_2_mobius.py`].  
Usage and output details are in the accompanying `README.md`.

---

## Assumptions

We work in a model where a charged particle’s internal dynamics consist of:

- **Two equal, orthogonal, phase-locked circulations** of charge (enforced by Möbius-like topology).
- The two loops’ magnetic moments align to the same spin axis by topology, not chance.
- Motion is treated at **leading order** — non-relativistic, in the particle’s rest frame.
- Any higher-order effects (e.g. radiative/QED corrections to produce a true *g − 2*) are out of scope here.

Notation:

- \(q\) — particle charge.
- \(m\) — mass participating in internal motion.
- \(r\) — radius of each circulation.
- \(\omega\) — angular frequency of each circulation.

---

## Magnetic Moment

For one circular current loop:

- Current:  
  \[
  I = \frac{q \,\omega}{2\pi}
  \]
- Area:  
  \[
  A = \pi r^2
  \]
- Magnetic moment:  
  \[
  \mu_{\text{one}} = I A = \frac{q\,\omega\,r^2}{2}
  \]

In the Möbius model, there are two such loops, orthogonal in space but with moments aligned along the spin axis. The total is:

\[
\mu_{\text{total}} = 2\mu_{\text{one}} = q\,\omega\,r^2.
\]

---

## Spin Angular Momentum

For the same internal motion:

\[
S = m\,r^2\,\omega.
\]

Even with two orthogonal modes, their angular momenta sum vectorially to the same spin axis fixed by the geometry, so the total magnitude remains \( m r^2 \omega\).

---

## Landé g Derivation

By definition:

\[
\mu_{\text{total}} = \frac{g\,q}{2m} \, S.
\]

Substitute \(\mu_{\text{total}} = q \omega r^2\) and \(S = m r^2 \omega\):

\[
q \omega r^2 = \frac{g\,q}{2m} (m r^2 \omega) \quad\Rightarrow\quad g = 2.
\]

**Result:** At leading order in this model, \(g = 2\), independent of \(r\) and \(\omega\).

---

## Why This Differs from the Naïve Classical Loop

A single classical current loop gives \(g = 1\) in this relation.  
The Möbius topology enforces a **two-mode doubling** of the magnetic moment for the same total spin, giving \(g=2\) naturally.

---

## Variants: Simple Relativistic-Style Adjustments

The demo script explores three pedagogical variants by introducing \(\gamma\) factors:

- **`td_current`** — apply time dilation to the circulating current:  
  \(\mu_{\text{total}} \to \mu_{\text{total}}/\gamma\) ⇒ \(g \approx 2/\gamma\)
- **`gamma_S`** — apply relativistic inertia to the spin:  
  \(S \to \gamma S\) ⇒ \(g \approx 2/\gamma\)
- **`combined`** — apply both:  
  \(g \approx 2/\gamma^2\)

Here:
\[
\gamma = \frac{1}{\sqrt{1 - \beta^2}}, \quad \beta = \frac{v}{c}, \quad v = r\,\omega.
\]

These are **illustrative only**; they are not full relativistic or QED calculations.

---

## Scope and Limitations

- This note establishes the **leading-order g = 2** result and variant formulas only.
- Real-world \(g\) values include higher-order contributions; those are deferred to future work.
- The model assumes perfect phase-locking and equal mode amplitudes — no decoherence or asymmetry.

---

## License

MIT License — see repository `LICENSE` file.

---

## Citation

When referencing the result or figures/CSVs from the accompanying script, cite as:

> James, *Möbius Two-Mode g-Factor — Theory*, `g_equals_2_mobius.md`.

