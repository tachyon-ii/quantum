# HFQPO Φ‑Boundary Toolkit

Minimal, dependency‑light tools to test the **Φ‑boundary–gated p‑mode** interpretation of
high‑frequency quasi‑periodic oscillations (HFQPOs) in black‑hole binaries.

This implements the pipeline we discussed:

1) Fit HFQPO pairs with a near‑horizon cavity (slender torus) ladder:
   \[ \omega_n^2 = \kappa_r^2(r_0,a_\ast) + (n\pi c_s/L)^2, \quad f_n^{\rm obs}=\frac{\omega_n}{2\pi}\,g_{\rm GR} \]
2) Check **energy dependence**: overtone hardening and **lag‑sign flip** (Φ‑gate transmissivity).
3) Search **Lense‑Thirring sidebands** at \(f_n \pm f_{\rm LT}\).

All scripts are pure NumPy/Pandas; matplotlib is optional for quick‑look plots.

---

## File layout

```
tests/hfqpo_phi_pmode/
  hfqpo_fit.py          # fits (f1,f2) to get r0,L,eta,g_GR (and reports κ_r)
  hfqpo_energy_lags.py  # energy‑dependent RMS/lag checks (overtone hardening; lag flip)
  hfqpo_sidebands.py    # searches for sidebands at ±f_LT using PDS + fit
  README.md             # this file
```

---

## 1) Fitting the ladder: `hfqpo_fit.py`

**Input CSV** (`--peaks`): minimal columns
- `epoch_id` (string/int)
- `f1, df1` — lower HFQPO frequency (Hz) and uncertainty
- `f2, df2` — upper HFQPO frequency (Hz) and uncertainty
- `M_solar` — BH mass in solar masses

**Optional columns**
- `spin_est` — seed spin \(a_\ast\) in [0,1)
- `inc_deg` — inclination (metadata only in this version)

**Usage**
```bash
python hfqpo_fit.py \
  --peaks pds_peaks.csv \
  --out fit_results.csv \
  --plots plots_fit/ \
  --r0 3.5,10,30 --L 0.2,5,30 --eta 0.01,0.5,20 --g 0.5,1.0,12 --spin 0.0,0.99,12
```

**Output CSV** (`fit_results.csv`)
- `epoch_id, M_solar, a_star, r0_rg, L_rg, eta, g_GR, kappa_r_Hz, f1_obs, f1_mod, f2_obs, f2_mod, chi2, dof, notes`

> Notes: `r0_rg` and `L_rg` are in gravitational radii \(r_g=GM/c^2\). `eta` is \(c_s/c\). `g_GR` is an
> effective factor absorbing gravitational/Doppler/Φ‑gate transfer to first order.

---

## 2) Energy dependence: `hfqpo_energy_lags.py`

**Input CSV** (`--lags`): per epoch **and energy band**
- `epoch_id`
- `band_lo_keV, band_hi_keV`
- `rms_n1, rms_n2` — fractional RMS (or power) at \(n=1,2\)
- `lag_n1_ms, lag_n2_ms` — phase lags (ms) for \(n=1,2\)

**Usage**
```bash
python hfqpo_energy_lags.py \
  --lags lags_rms.csv \
  --out energy_lag_tests.csv \
  --plots plots_energy/
```

**Output CSV**
- `epoch_id, slope_rms_n1, slope_rms_n2, overtone_hardens, lag_flip, notes`

**Pass criteria (model‑distinctive):**
- Overtone \(n=2\) RMS increases with energy faster than \(n=1\).
- Lag sign flips between \(n=1\) and \(n=2\) at hard energies (or exhibits a crossing).

---

## 3) Sidebands: `hfqpo_sidebands.py`

**Inputs**
- `--pds` PDS CSV with `epoch_id, freq_Hz, power`
- `--fit` results from `hfqpo_fit.py` (gives \(r_0, a_\ast\))
- `--peaks` CSV with `epoch_id, f1, f2` (observed peak centers)

**Usage**
```bash
python hfqpo_sidebands.py \
  --pds pds.csv \
  --fit fit_results.csv \
  --peaks pds_peaks.csv \
  --out sidebands.csv \
  --plots plots_sidebands/ \
  --win 0.1       # window half‑width as fraction of f_LT
```

**Output CSV**
- `epoch_id, f_LT_Hz, snr_f1_minus, snr_f1_plus, snr_f2_minus, snr_f2_plus, detected_any, notes`

Detection metric: simple robust SNR against a local‑median background in windows around
\(f_1 \pm f_{\rm LT}\) and \(f_2 \pm f_{\rm LT}\). A refined search (e.g., matched filters) can be
dropped in later without changing I/O.

---

## Data contracts (CSV schemas)

**pds_peaks.csv**
```
epoch_id,f1,df1,f2,df2,M_solar[,spin_est,inc_deg]
XTEJ1550_01,184,5,276,5,9.1,0.8,70
...
```

**fit_results.csv** (produced)
```
epoch_id,M_solar,a_star,r0_rg,L_rg,eta,g_GR,kappa_r_Hz,f1_obs,f1_mod,f2_obs,f2_mod,chi2,dof,notes
...
```

**lags_rms.csv**
```
epoch_id,band_lo_keV,band_hi_keV,rms_n1,rms_n2,lag_n1_ms,lag_n2_ms
XTEJ1550_01,2,4,0.06,0.08,-0.5,0.3
...
```

**pds.csv**
```
epoch_id,freq_Hz,power
XTEJ1550_01,100,1.2
...
```

---

## Pass / Fail (for verifiers)

- **3:2 preserved under jitter**: ratio stable while absolute \(f\) drifts (fit explains via \(ΔL\)).
- **Overtone hardens + lag flip**: energy‑dependent signatures present.
- **Sidebands at \(±f_{\rm LT}\)**: detectable in good S/N; scale as \(a_\ast/M\).
- **Mass scaling**: across sources of similar spin, \(f\propto 1/M\).

Failures in multiple good datasets falsify the Φ‑boundary–gated p‑mode interpretation.

---

## Notes and limitations

- This is a **minimal** implementation to get results from archival data quickly.
- The factor `g_GR` is currently a scalar; a more complete model would compute it from
  transfer functions (ray tracing) and Φ‑boundary transmissivity \(T(ω,Φ)\).
- You can substitute a better optimizer (e.g., SciPy) without changing inputs/outputs.
