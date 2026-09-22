#!/usr/bin/env python3
"""
CBL (Critical Boundary Layer) visualizer for BH rings.

- Exterior metric: Schwarzschild (GR), so ring diameter b_crit stays GR-like.
- Boundary/halo: finite-thickness, partially absorbing shell at r_b=(1+eps)*2 r_g
  with a long-tailed kernel so it can attenuate rays whose closest approach is
  near the photon sphere (r_min ~ 3 r_g).

   tau_eff(b) = tau0 * K( (r_min(b) - r_b) / ell )

  Kernels:
    "exp"     : tau0 * exp( -|dr|/ell )          (default, good halo)
    "gauss"   : tau0 * exp( -(dr/ell)^2 )        (narrow tail)
    "lorentz" : tau0 / (1 + (dr/ell)^2 )         (very long tail)
    "power"   : tau0 / (1 + (|dr|/ell)**p )

- Intensity profile (screen model):
    I(b) = exp( - tau_eff(b) )

Outputs
-------
1) Prints: r_g, b_crit (GR), ring diameter, and the shadow-edge thickness
   (10%→90% of outer brightness) in r_g and as a fraction of b_crit.
2) Saves:
   - cbl_ring_intensity.png   (I vs b/b_crit)
   - cbl_ring_attenuation.png (1 - I vs b/b_crit)
"""

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------- constants -------------------------------

C = 2.99792458e8     # m/s
G = 6.67430e-11      # m^3 kg^-1 s^-2
M_SUN = 1.98847e30   # kg

# ------------------------------- utilities -------------------------------

def rg_of_mass(M_solar):
    """Gravitational radius r_g = GM/c^2."""
    M = M_solar * M_SUN
    return G*M / (C*C)

def A_schw(r, r_g):
    """Schwarzschild A(r) = 1 - 2 r_g / r (g_tt = -A c^2)."""
    return 1.0 - 2.0*r_g/r

def b_crit_gr(r_g):
    """GR critical impact parameter (shadow radius): b_crit = sqrt(27) r_g."""
    return np.sqrt(27.0) * r_g

def r_photon_sphere(r_g):
    """Photon sphere radius in Schwarzschild: 3 r_g."""
    return 3.0 * r_g

def closest_approach_from_b(b, r_g, tol=1e-12, maxit=80):
    """
    For a given impact parameter b >= b_crit, solve for the turning radius r_min
    from the algebraic condition:
        b^2 = r^2 / A(r)  with A(r) = 1 - 2 r_g / r
    In Schwarzschild, r_min is the outer positive root > r_ph.
    """
    r_ph = r_photon_sphere(r_g)
    r_low = r_ph * (1.0 + 1e-9)   # just above photon sphere
    r_high = max(10.0*r_g, 1.5*b) # safe upper bracket

    def f(r):
        A = A_schw(r, r_g)
        return b*b - (r*r)/A

    f_low = f(r_low)
    f_high = f(r_high)
    # ensure opposite signs
    it_guard = 0
    while f_high > 0 and it_guard < 20:
        r_high *= 1.5
        f_high = f(r_high)
        it_guard += 1
    if f_low <= 0 or f_high >= 0:
        return np.nan

    a, fa = r_low, f_low
    c, fc = r_high, f_high
    for _ in range(maxit):
        m = 0.5*(a+c)
        fm = f(m)
        if abs(fm) < tol*(1.0 + b*b):
            return m
        if np.sign(fm) == np.sign(fa):
            a, fa = m, fm
        else:
            c, fc = m, fm
    return 0.5*(a+c)

# ------------------------------- CBL model -------------------------------

def tau_eff(r_min, r_b, ell, tau0, kernel="exp", p=2.0):
    """
    Effective optical depth of the boundary/halo at closest approach r_min.
    dr = max(0, r_min - r_b): we only attenuate rays outside the boundary.
    """
    dr = np.maximum(0.0, r_min - r_b)
    if kernel == "gauss":
        return tau0 * np.exp(-(dr/ell)**2)
    elif kernel == "exp":
        return tau0 * np.exp(-dr/ell)
    elif kernel == "lorentz":
        return tau0 / (1.0 + (dr/ell)**2)
    elif kernel == "power":
        return tau0 / (1.0 + (np.abs(dr)/ell)**p)
    return tau0 * np.exp(-dr/ell)  # default

def intensity_profile(M_solar, eps=0.0, ell_over_rg=0.8, tau0=0.8,
                      b_max_factor=2.0, n_b=2000, kernel="exp", p=2.0):
    """
    Compute I(b)=exp(-tau_eff) with a halo kernel that reaches r_ph≈3 r_g.
    Defaults (ell_over_rg≈0.8, tau0≈0.8, kernel="exp") yield ~few–10% attenuation
    near the ring while keeping the diameter GR-like (eps=0).
    """
    r_g = rg_of_mass(M_solar)
    bcrit = b_crit_gr(r_g)
    r_b = (1.0 + eps) * 2.0 * r_g
    ell = ell_over_rg * r_g

    b = np.linspace(bcrit*(1.000001), bcrit*b_max_factor, n_b)
    rmin = np.array([closest_approach_from_b(bi, r_g) for bi in b])

    tau = tau_eff(rmin, r_b, ell, tau0, kernel=kernel, p=p)
    I = np.exp(-tau)
    return b, I, rmin, r_g, bcrit, r_b, ell

def edge_thickness(b, I, frac_low=0.1, frac_high=0.9):
    """
    Shadow-edge thickness: width in b where intensity rises
    from frac_low to frac_high of its outer plateau.
    """
    top = np.sort(I)[int(0.95*I.size):]
    I_out = np.median(top) if top.size>0 else 1.0
    L = frac_low * I_out
    H = frac_high * I_out
    idxL = np.where(I >= L)[0]
    idxH = np.where(I >= H)[0]
    bL = b[idxL[0]] if idxL.size>0 else np.nan
    bH = b[idxH[0]] if idxH.size>0 else np.nan
    width = (bH - bL) if (np.isfinite(bH) and np.isfinite(bL)) else np.nan
    return I_out, bL, bH, width

# ------------------------------- plotting -------------------------------

def plot_profiles(b, I, bcrit, outbase="cbl_ring", show=False):
    x = b / bcrit
    A = 1.0 - I

    plt.figure(figsize=(7.5,4.8))
    plt.plot(x, I, lw=2, color="tab:blue")
    plt.axvline(1.0, color="k", ls="--", lw=1, alpha=0.7, label=r"$b_{\rm crit}$")
    plt.xlabel(r"$b / b_{\rm crit}$"); plt.ylabel(r"Intensity $I(b)$")
    plt.title("CBL: Intensity Profile (outer brightness normalized)")
    plt.grid(alpha=0.15); plt.legend()
    plt.tight_layout(); plt.savefig(f"{outbase}_intensity.png", dpi=140)
    if show: plt.show(); plt.close()

    plt.figure(figsize=(7.5,4.8))
    plt.plot(x, A, lw=2, color="tab:red")
    plt.axvline(1.0, color="k", ls="--", lw=1, alpha=0.7, label=r"$b_{\rm crit}$")
    plt.xlabel(r"$b / b_{\rm crit}$"); plt.ylabel(r"Attenuation $1 - I(b)$")
    plt.title("CBL: Shadow Edge (attenuation vs. b)")
    plt.grid(alpha=0.15); plt.legend()
    plt.tight_layout(); plt.savefig(f"{outbase}_attenuation.png", dpi=140)
    if show: plt.show(); plt.close()

# ------------------------------- driver -------------------------------

if __name__ == "__main__":
    # Example: Sgr A*
    M_solar = 4.3e6
    # Halo parameters (tune to taste)
    eps = 0.0          # r_b = (1+eps)*2 r_g   (keep ≈0 to preserve diameter)
    ell_over_rg = 0.8  # halo scale-length in units of r_g
    tau0 = 0.8         # peak optical depth at r_b
    kernel = "exp"     # "exp"|"gauss"|"lorentz"|"power"

    # Build profile
    b, I, rmin, r_g, bcrit, r_b, ell = intensity_profile(
        M_solar, eps=eps, ell_over_rg=ell_over_rg, tau0=tau0,
        b_max_factor=2.0, n_b=2500, kernel=kernel
    )

    # Edge metrics
    I_out, bL, bH, width = edge_thickness(b, I, frac_low=0.1, frac_high=0.9)

    print("="*64)
    print("CBL RING SUMMARY (Schwarzschild exterior, absorptive halo)")
    print("="*64)
    print(f"M = {M_solar:.3e} M_sun")
    print(f"r_g = {r_g:.3e} m")
    print(f"GR photon sphere  r_ph  = 3.000 r_g")
    print(f"GR shadow radius  b_crit = {bcrit/r_g:.3f} r_g  (diameter = {2.0*bcrit/r_g:.3f} r_g)")
    print()
    print(f"Halo params: r_b = {r_b/r_g:.3f} r_g  (eps={eps:.3g}),  ell = {ell/r_g:.3f} r_g,  tau0 = {tau0:.3g}, kernel={kernel}")
    print(f"Outer intensity (plateau) ~ {I_out:.3f}")
    if np.isfinite(width):
        print(f"Edge thickness (10%→90%): Δb = {width/r_g:.4f} r_g  = {100.0*width/bcrit:.2f}% of b_crit")
        print(f"At 10% level:  b = {bL/r_g:.4f} r_g  (b/b_crit = {bL/bcrit:.5f})")
        print(f"At 90% level:  b = {bH/r_g:.4f} r_g  (b/b_crit = {bH/bcrit:.5f})")
    else:
        print("Edge thickness could not be determined (profile too flat).")

    plot_profiles(b, I, bcrit, outbase="cbl_ring", show=False)
    print("\nSaved: cbl_ring_intensity.png, cbl_ring_attenuation.png")

