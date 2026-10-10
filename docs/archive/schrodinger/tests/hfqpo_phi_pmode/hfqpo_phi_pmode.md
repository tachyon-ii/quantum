## HFQPOs → Φ‑boundary–gated p‑modes: test plan

### Core model (what we’ll fit)

Near‑horizon cavity (slender torus) at radius $r_0$, half‑extent $L$, comoving sound speed $c_s=\eta c$.

Mode ladder (source frame):

$$
\omega_n^2 \;=\; \kappa_r^2(r_0,a_\ast)\;+\;\Big(\frac{n\pi c_s}{L}\Big)^2,\qquad n=1,2,3,\ldots
$$

Observed:

$$
f_n^{\rm obs} \;=\; \frac{\omega_n}{2\pi}\; g_{\rm GR}(r_0,a_\ast,i).
$$

**Key predictions to test**

1. **3:2 pairs with preserved ratio during jitter**
   $\Delta(f_2/f_1)\ll \Delta f_1/f_1$.
   *Why distinctive:* many resonance models struggle to keep the ratio fixed while both peaks drift.

2. **Hard‑band enhancement of the overtone**
   Overtone $n=2$ is stronger in harder X‑ray bands due to energy‑dependent transmissivity $T(\omega,\Phi)$ at the Φ boundary.
   *Why distinctive:* ties the geometry (Φ‑gate) to energy‑dependent RMS/phase lags.

3. **Sidebands at the local LT frequency**
   Weak shoulders at $f_n \pm m f_{\rm LT}(r_0,a_\ast)$ (with $m=1,2$), scaling $\propto a_\ast/M$.

4. **Mass scaling across sources**
   For similar spins, $f\propto 1/M$ to first order.

5. **Jitter–size relation**
   $\Delta f_n/f_n \approx -\frac{(n\pi c_s/L)^2}{\kappa_r^2+(n\pi c_s/L)^2}\,(\Delta L/L)$.
   *Check:* epochs with larger $f$ correspond to smaller fitted $L$, ratio $f_2/f_1$ \~ constant.

### Data & sources (archival, immediately usable)

* **BH binaries with 3:2 HFQPOs:** GRO J1655‑40, XTE J1550‑564, GRS 1915+105, H1743‑322 (RXTE PCA; also NICER, NuSTAR where available).
* **Products:** power density spectra (PDS) in multiple energy bands; cross‑spectra for phase lags; epoch stacks.

### Analysis pipeline (minimal)

1. **PDS extraction per energy band**, identify $f_1,f_2$ and Q factors; estimate errors via Monte‑Carlo (scrambling or bootstrap).
2. **Fit the ladder**: unknowns $(r_0,L,\eta,\kappa_r,g_{\rm GR})$ with priors on $M,a_\ast,i$ (wide if needed).

   * Start with $\kappa_r$ set by GR Kerr at $r_0$, or treat as a small floor parameter.
   * Use both peaks simultaneously; require $f_2/f_1$ ≈ 3/2 within the fitted model.
3. **Energy dependence**: measure RMS and phase lag vs energy for $n=1,2$; check hard‑band enhancement of $n=2$ and **lag‑sign flip** between $n=1$ and $n=2$.
4. **Sideband search**: look for shoulders at $\pm f_{\rm LT}(r_0,a_\ast)$ around $f_n$; significance via matched filters or likelihood ratio.
5. **Jitter epochs**: across multi‑epoch data, verify $f$-drift explained by $\Delta L$ with near‑constant $f_2/f_1$.
6. **Cross‑source scaling**: compare $f_1$ vs $1/M$ slope across sources (expect \~‑1 within uncertainties).

### Pass/Fail (explicit)

* **PASS if** (i) the 3:2 ladder fits with one $(r_0,L,\eta)$ per epoch and a stable ratio, (ii) overtone dominance grows with energy and lag sign flips between $n=1$ and $n=2$, (iii) sidebands consistent with $f_{\rm LT}$ are present when S/N permits, and (iv) mass scaling holds across sources.
* **FAIL if** any of the following consistently occur across good datasets:
  a) ratio wanders widely while both peaks drift;
  b) overtone is not harder (or lag signatures contradict the Φ‑gate energy dependence);
  c) no sidebands when S/N is ample and spin is high;
  d) cross‑source mass scaling is inconsistent with $f\propto 1/M$.

---

## Where to put this in the repo

```
tests/hfqpo_phi_pmode/
  hfqpo_fit.py          # fits (f1,f2) with the ladder; outputs best (r0,L,eta,kappa_r,g_GR)
  hfqpo_energy_lags.py  # measures RMS, phase lags vs energy; tests overtone-hard enhancement & lag flip
  hfqpo_sidebands.py    # searches for f_LT sidebands around f1,f2
  README.md             # how to run; expected CSV schemas; pass/fail criteria
```

**CSV in/out (suggestion):**

* **input\_events.csv:** time, energy\_channel (or keV), source\_id, epoch\_id
* **pds\_peaks.csv:** epoch\_id, band\_keV, f1, df1, Q1, f2, df2, Q2
* **fit\_results.csv:** epoch\_id, r0\_rg, L\_rg, eta, kappa\_r\_Hz, g\_GR, chi2\_dof
* **lags\_rms.csv:** epoch\_id, band\_keV, rms\_n1, rms\_n2, lag\_n1\_ms, lag\_n2\_ms

---

## Patch snippets to wire it into docs

**veracifiers.md** (add under Black Hole tests)

```diff
+ **HFQPO Φ‑boundary–gated p‑modes**
+ - **Prediction:** HFQPO pairs are the p‑mode ladder of a near‑horizon cavity with Φ‑dependent transmissivity. Expect (i) ~3:2 ratio with jitter but preserved ratio, (ii) hard‑band enhancement of the overtone and a lag‑sign flip between n=1 and n=2, (iii) sidebands at ±f_LT(r0,a*), and (iv) f ∝ 1/M across sources of similar spin.
+ - **Method:** Fit f1,f2 with ω_n^2 = κ_r^2 + (nπ c_s/L)^2 times redshift g_GR; test RMS/lag vs energy; search sidebands; check mass scaling.
+ - **Falsifier:** Failure of any item (i)–(iv) across good S/N datasets.
+ - **Code:** tests/hfqpo_phi_pmode/ (fit, energy‑lags, sidebands).
```

**black-holes.md** (append under HFQPOs section)

```diff
+ #### HFQPOs as Φ‑boundary–gated p‑modes
+ A small inner cavity near r0 supports inertial–acoustic modes with
+   ω_n^2 = κ_r^2(r0,a*) + (nπ c_s/L)^2;
+ observed f_n = ω_n/(2π) · g_GR. The Φ‑boundary’s transmissivity T(ω,Φ)
+ imprints energy dependence: overtone (n=2) strengthens in hard bands;
+ phase lags flip sign between n=1 and n=2. Frame‑dragging adds sidebands at ±f_LT.
+ See veracifiers.md for pass/fail criteria and tests/hfqpo_phi_pmode/ for code.
```

---

## Why this is a strong test

* Uses **archival data now** (no new telescope time needed).
* Produces **numerical outputs** ($r_0,L,\eta$, sideband spacing, lag signatures) you can compare across sources.
* Separates our model from competing pictures via **energy‑dependent overtone behaviour** and **lag flips**, which come naturally from a transmissivity gate but aren’t generic to pure‑GR discoseismology.

If you want, I can also sketch the CLI for `hfqpo_fit.py` (args, outputs) so you can drop in your usual workflow.

