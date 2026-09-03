# Möbius Two-Mode g-Factor — Toolkit

This toolkit tests a simple but falsifiable claim from the Möbius-locked two-mode model of internal motion:

> At leading order (non-relativistic), the model predicts a Landé g-factor of exactly **2** for a charged particle, independent of radius \(r\) and angular frequency \(\omega\).

The full derivation, assumptions, and physical context are in **`g_equals_2_mobius.md`**.

The accompanying Python program (`g_equals_2_mobius.py`) demonstrates this baseline result and explores three didactic variants that modify the current and/or angular momentum with a relativistic \(\gamma\) factor.

---

## Variants

- `leading` — baseline model: \(g=2\).
- `td_current` — time dilation applied to circulating current: \(g \approx 2/\gamma\).
- `gamma_S` — relativistic inertia applied to spin: \(g \approx 2/\gamma\).
- `combined` — both effects: \(g \approx 2/\gamma^2\).

Here \( \gamma = 1/\sqrt{1-\beta^2} \), \( \beta = v/c \), \( v = r\omega \).

These variants are pedagogical; they are not full QED.

---

## Installation

Python ≥ 3.8 is required.  
Optional plotting uses `matplotlib`:

```bash
pip install matplotlib
````

---

## Usage

```bash
python3 g_equals_2_mobius.py [OPTIONS]
```

Common options:

* `--variant {leading, td_current, gamma_S, combined}`
* `--trials N` — random log-uniform samples of `(r, ω)`.
* `--rmin --rmax`, `--omin --omax` — sampling bounds.
* `--beta-max X` — cap $\beta = v/c$ (<1).
* `--units {physical, arb}` — electron constants or arbitrary units.
* `--seed INT` — reproducible RNG.
* `--sweep NR NOMEGA` — grid sweep over $r$ and $\omega$.
* `--check [--tol EPS]` — verify all samples match the variant’s expected formula.
* `--csv PATH` — write results to CSV.
* `--plot PATH.png` — save scatter of $g$ vs $\beta$.

---

## Examples

Leading-order check:

```bash
python3 g_equals_2_mobius.py
```

Time-dilated current, reproducible run with check:

```bash
python3 g_equals_2_mobius.py --variant td_current --trials 20 --beta-max 0.8 --seed 7 --check
```

Relativistic inertia variant, CSV + plot:

```bash
python3 g_equals_2_mobius.py --variant gamma_S --trials 200 --beta-max 0.9 --seed 1 \
  --csv gammaS.csv --plot gammaS.png
```

Combined effects, grid sweep:

```bash
python3 g_equals_2_mobius.py --variant combined --sweep 40 40 --beta-max 0.95
```

---

## Output

Preview lines:

```
Case 01: r=…, ω=…, β=…, γ=… → g=… (expected=…)
```

CSV columns:

```
variant,units,r_m,omega_rad_s,beta,gamma,g,g_expected
```

Plot (`--plot`) shows $g$ vs $\beta$ for the chosen variant.

---

## License

MIT

---

## Citation

When publishing figures or data from this toolkit, cite the theory document:

> *James, “Möbius Two-Mode g-Factor” (g\_equals\_2\_mobius.md)*
