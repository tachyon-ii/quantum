# ∆t Gravity — Minimal Stack

**Idea in one line:** gravity is a **spatial gradient in proper time** (∆t).  
Local clock-rate:  
\[
\alpha(\mathbf x)=\frac{d\tau}{dt}\Big|_{v=0}=\sqrt{-g_{00}(\mathbf x)}\!,
\quad
g_{00}\approx-\Big(1+\frac{2\Phi}{c^2}\Big),\;
g_{ij}\approx\Big(1-\frac{2\Phi}{c^2}\Big)\delta_{ij}.
\]
Matter lowers \(\alpha\) (captured Φ-energy), creating a gradient; geodesics are “follow the fastest clock.”

**Field/source (weak field):**
\[
\nabla^2\Phi = 4\pi G\,\frac{u(\mathbf x)-u_0}{c^2},\qquad
\alpha(\mathbf x)=\sqrt{1+\tfrac{2\Phi}{c^2}},\qquad
n(\mathbf x)=1-\frac{2\Phi(\mathbf x)}{c^2}.
\]

**Equations of motion:**
- Timelike (slow): \(\dot{\mathbf v}=-\nabla\Phi\).
- Null (Fermat): \(\dfrac{d}{ds}(n\mathbf k)=\nabla n\) (Eddington bending emerges when combined with the spatial factor).

**This repo (minimal):**
- `libgravity.py` — source of truth (Φ from energy density, \(\alpha,n\), steppers, analytic helpers).  
- `test_falsifiers.py` — the full weak-field test suite (GR, PPN-γ, extended lens, free-fall, and invariances).  
- `visualize_lensing.py` — a **single visualizer** that uses `libgravity.ray_trace_point_analytic(...)` to sweep impact parameters \(b\) and compare **numeric** vs **analytic** bending (with optional PPN-γ).

---

## Quickstart

```bash
# 0) (Optional) venv & deps
python3 -m venv .venv && source .venv/bin/activate
python -m pip install numpy matplotlib

# 1) Run the falsifiers (should all pass)
python3 test_falsifiers.py

# 2) Visualize point-mass lensing (numeric vs analytic)
python3 visualize_lensing.py --M-solar --L 20Rsun \
  --b "0.5Rsun,1Rsun,2Rsun,3Rsun,5Rsun" \
  --gamma 1.0 --steps 20000 --out lens_point

