# test_falsifiers.py — full suite with PPN-γ track
# - Analytic falsifiers: limb bend, 1/b, Shapiro, redshift, energy weighs
# - Φ invariance to constant energy floor (Poisson on u-u0)
# - Numeric ray vs analytic (analytic Fermat, adaptive RK4)
# - Timelike free-fall (accel + energy drift)
# - NEW: PPN-γ analytic scaling and numeric ray checks
#
# Run:  python3 test_falsifiers.py

import math
import numpy as np
import sys

from libgravity import (
    c, G,
    deflection_angle_point_mass,
    shapiro_delay_point_mass,
    gravitational_redshift_delta_phi,
    energy_equivalent_mass,
)

# Optional Poisson test if available
try:
    from libgravity import phi_from_energy_density_fft as _phi_fft
    _HAS_PHI = True
except Exception:
    _HAS_PHI = False

# Optional grid helpers and steppers (used by free-fall)
_HAS_GRID_HELPERS = _HAS_PART = False
try:
    from libgravity import grad_central, sample_trilinear
    _HAS_GRID_HELPERS = True
    from libgravity import step_particle
    _HAS_PART = True
except Exception:
    pass

ARCSEC = (180.0/math.pi)*3600.0

def almost(a, b, rel=1e-3, abs_tol=0.0, msg=""):
    if abs(a-b) <= max(abs_tol, rel*max(1.0, abs(b))):
        return True
    raise AssertionError(msg or f"{a} vs {b} (rel tol={rel}, abs tol={abs_tol})")

def banner(title):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title))

# ------------------ Analytic falsifiers ------------------

def test_light_bending_solar_limb():
    banner("Light bending — Solar limb (analytic)")
    M_sun = 1.98847e30
    R_sun = 6.9634e8
    theta = deflection_angle_point_mass(M_sun, R_sun)*ARCSEC
    print(f"θ(limb) = {theta:.4f}\"  (GR ~ 1.7505\")")
    almost(theta, 1.7505, rel=8e-4)

def test_light_bending_ratio():
    banner("Light bending — 1/b scaling sanity sweep")
    M_sun = 1.98847e30
    R_sun = 6.9634e8
    bs = [0.5*R_sun, 1.0*R_sun, 2.0*R_sun]
    thetas = [deflection_angle_point_mass(M_sun, b)*ARCSEC for b in bs]
    for bR, th in zip((0.5, 1.0, 2.0), thetas):
        print(f"b={bR:>3.1f} R_sun  θ={th:.4f}\"")
    assert thetas[0] > thetas[1] > thetas[2], "Expected θ(0.5R) > θ(1R) > θ(2R)"
    almost(thetas[0]/thetas[1], 2.0, rel=3e-3, msg="θ(0.5R)/θ(1R) ≠ 2")
    almost(thetas[1]/thetas[2], 2.0, rel=3e-3, msg="θ(1R)/θ(2R) ≠ 2")

def test_shapiro_delay():
    banner("Shapiro delay — Earth↔Earth grazing Sun (analytic)")
    M_sun = 1.98847e30
    AU = 1.495978707e11
    R_sun = 6.9634e8
    b = 1.1*R_sun
    dt = shapiro_delay_point_mass(M_sun, AU, AU, b)
    dt_us = dt*1e6
    print(f"Δt ≈ {dt_us:.3f} μs (expect ~117.6 μs)")
    almost(dt_us, 117.6, rel=0.02)

def test_redshift_sun_surface():
    banner("Gravitational redshift — Sun surface to ∞ (analytic)")
    M_sun = 1.98847e30
    R_sun = 6.9634e8
    Phi_surface = -G*M_sun/R_sun
    z = gravitational_redshift_delta_phi(Phi_surface, 0.0)
    print(f"z ≈ {z:.6e}  (expect ~2.1206e-6)")
    almost(z, 2.1206e-6, rel=5e-4)

def test_energy_has_weight():
    banner("Energy weighs — Δm = U/c^2")
    U = 1.0
    dm = energy_equivalent_mass(U)
    dm_ref = U/(c*c)
    print(f"Δm(1 J) = {dm:.3e} kg")
    almost(dm, dm_ref, rel=0.0, abs_tol=0.0)

def test_phi_invariance_to_u0_floor():
    banner("Poisson: Φ invariance to constant floor in u(x)")
    if not _HAS_PHI:
        print("phi_from_energy_density_fft not available — SKIP")
        return
    N = 48; L = 1.0
    dx = dy = dz = (2*L)/N
    x = np.linspace(-L, L, N, endpoint=False)
    X,Y,Z = np.meshgrid(x,x,x, indexing='ij')
    M = 1.0; sigma = 0.2*L
    r2 = X*X + Y*Y + Z*Z
    rho = (M / ((2*np.pi)**1.5 * sigma**3)) * np.exp(-0.5*r2/(sigma*sigma))
    u0 = 5.0e-14
    u = rho*(c*c) + u0
    from libgravity import phi_from_energy_density_fft as phi_fft
    Phi1 = phi_fft(u, dx, dy, dz, u0=u0)
    du = 3.21e-12
    Phi2 = phi_fft(u + du, dx, dy, dz, u0=u0+du)
    num = np.max(np.abs(Phi1 - Phi2))
    den = max(np.max(np.abs(Phi1)), 1e-30)
    rel = num/den
    print(f"max|ΔΦ|/max|Φ| = {rel:.3e}")
    almost(rel, 0.0, abs_tol=1e-10)

# ------------------ Numeric ray: analytic Fermat (γ=1) ------------------

def test_numeric_ray_bending_analytic():
    banner("Numeric ray vs analytic bend (analytic Fermat, adaptive RK4)")

    def robust_angle(k1, k2):
        cdot = float(np.clip(np.dot(k1, k2), -1.0, 1.0))
        x = float(np.linalg.norm(np.cross(k1, k2)))
        return math.atan2(x, cdot)

    def n_and_gradn(x, M):
        r = float(np.linalg.norm(x))
        n = 1.0 + 2.0*G*M/(c*c*r)
        gradn = -(2.0*G*M/(c*c)) * (x / (r**3 + 1e-30))
        return n, gradn

    def rhs(pos, kk, M):
        n, gn = n_and_gradn(pos, M)
        kdotg = float(np.dot(kk, gn))
        dkds = (gn - kdotg*kk)/max(n, 1e-30)
        return kk, dkds

    def rk4_step(pos, kk, ds, M):
        dx1, dk1 = rhs(pos, kk, M)
        p2 = pos + 0.5*ds*dx1; k2 = kk + 0.5*ds*dk1; k2/=np.linalg.norm(k2)
        dx2, dk2 = rhs(p2, k2, M)
        p3 = pos + 0.5*ds*dx2; k3 = kk + 0.5*ds*dk2; k3/=np.linalg.norm(k3)
        dx3, dk3 = rhs(p3, k3, M)
        p4 = pos + ds*dx3;     k4 = kk + ds*dk3;     k4/=np.linalg.norm(k4)
        dx4, dk4 = rhs(p4, k4, M)
        pos_new = pos + (ds/6.0)*(dx1 + 2*dx2 + 2*dx3 + dx4)
        k_new   = kk  + (ds/6.0)*(dk1 + 2*dk2 + 2*dk3 + dk4)
        return pos_new, k_new/np.linalg.norm(k_new)

    M_sun = 1.98847e30; R_sun = 6.9634e8
    b = 1.0*R_sun;  L = 30.0*R_sun
    k0 = np.array([1.0, 0.0, 0.0], float)
    x  = np.array([-L, b, 0.0], float)
    k  = k0.copy()

    dtheta_cap = 0.005 * (math.pi/648000.0)
    steps_nominal = 20000
    ds_nom = (2.0*L)/steps_nominal
    ds_min = ds_nom*1e-4
    ds_max = ds_nom*1.0

    s_guard = 0
    while x[0] < L and s_guard < 5*steps_nominal:
        s_guard += 1
        _, dk1 = rhs(x, k, M_sun)
        rate = float(np.linalg.norm(dk1))
        ds = min(ds_nom, max(ds_min, min(ds_max, dtheta_cap/rate))) if rate>0 else ds_nom
        x, k = rk4_step(x, k, ds, M_sun)

    theta_num = robust_angle(k0, k) * ARCSEC
    theta_gr  = deflection_angle_point_mass(M_sun, b) * ARCSEC
    rel_err   = abs(theta_num - theta_gr)/max(theta_gr, 1e-30)
    print(f"θ_num={theta_num:.4f}\"  θ_GR={theta_gr:.4f}\"  rel err={rel_err*100:.2f}%")
    assert rel_err < 0.02, "Numeric ray (analytic Fermat) deviates >2% from analytic"

# ------------------ Free-fall (grid) ------------------

def _build_phi_point_mass_grid(M, L, N):
    x = np.linspace(-L, L, N, endpoint=False)
    X,Y,Z = np.meshgrid(x,x,x, indexing='ij')
    r = np.sqrt(X*X + Y*Y + Z*Z); r[r==0.0]=1e-9
    Phi = -G*M/r
    origin = (-L, -L, -L)
    spacing = ((2*L)/N, (2*L)/N, (2*L)/N)
    return Phi, origin, spacing

def test_freefall_energy_and_accel():
    if not (_HAS_GRID_HELPERS and _HAS_PART):
        print("\n(grid helpers or step_particle not available — SKIP free-fall)")
        return
    banner("Timelike free-fall: accel check + energy drift")

    M_sun = 1.98847e30; R_sun = 6.9634e8
    L = 10.0*R_sun; N = 64
    Phi, origin, spacing = _build_phi_point_mass_grid(M_sun, L, N)

    r0 = 5.0*R_sun
    x = np.array([ r0, 0.0, 0.0 ], float)
    v = np.array([ 0.0, 0.0, 0.0 ], float)

    dx,dy,dz = spacing
    dPx,dPy,dPz = grad_central(Phi, dx,dy,dz)
    gx = sample_trilinear(dPx, x[0],x[1],x[2], origin, spacing)
    gy = sample_trilinear(dPy, x[0],x[1],x[2], origin, spacing)
    gz = sample_trilinear(dPz, x[0],x[1],x[2], origin, spacing)
    a_num = np.linalg.norm([-gx, -gy, -gz])
    a_exp = G*M_sun/(r0*r0)
    rel = abs(a_num - a_exp)/a_exp
    print(f"|a|_num={a_num:.6e}  |a|_exp={a_exp:.6e}  rel err={rel*100:.3f}%")
    assert rel < 0.05

    def phi_at(pos): return -G*M_sun/max(np.linalg.norm(pos), 1e-30)
    dt = 0.25; steps = 4000
    E0 = 0.5*np.dot(v,v) + phi_at(x)
    max_rel_drift = 0.0
    for _ in range(steps):
        x, v = step_particle(x, v, Phi, origin, spacing, dt)
        E = 0.5*np.dot(v,v) + phi_at(x)
        drift = abs(E - E0)/max(abs(E0), 1e-30)
        if drift > max_rel_drift: max_rel_drift = drift
    print(f"max relative energy drift over run: {max_rel_drift*100:.2f}%")
    assert max_rel_drift < 0.05

# ------------------ NEW: PPN-γ tests ------------------

def _theta_ppn_gamma(M, b, gamma):
    # θ_γ = (1+γ) * 2GM/(c^2 b)  [radians]
    return (1.0 + gamma) * 2.0 * G * M / (c*c*b)

def _shapiro_ppn_gamma(dt_gr, gamma):
    # Our baseline uses 2GM/c^3; PPN says Δt ∝ (1+γ), so scale by (1+γ)/2
    return dt_gr * (1.0 + gamma) / 2.0

def test_ppn_gamma_bending_analytic():
    banner("PPN-γ: analytic light bending scaling")
    M_sun = 1.98847e30; R_sun = 6.9634e8; b = 1.0*R_sun
    for gamma in (0.5, 1.0, 1.5):
        th = _theta_ppn_gamma(M_sun, b, gamma)*ARCSEC
        print(f"γ={gamma:.1f}  θ_γ={th:.4f}\"")
    # Scaling checks
    th05 = _theta_ppn_gamma(M_sun, b, 0.5)
    th10 = _theta_ppn_gamma(M_sun, b, 1.0)
    th15 = _theta_ppn_gamma(M_sun, b, 1.5)
    assert th05 < th10 < th15
    almost(th15/th05, (1+1.5)/(1+0.5), rel=1e-12)

def test_ppn_gamma_shapiro_scaling():
    banner("PPN-γ: Shapiro delay scaling")
    M_sun = 1.98847e30; AU = 1.495978707e11; R_sun = 6.9634e8; b = 1.1*R_sun
    dt_gr = shapiro_delay_point_mass(M_sun, AU, AU, b)  # GR baseline (γ=1)
    for gamma in (0.5, 1.0, 1.5):
        dt_g = _shapiro_ppn_gamma(dt_gr, gamma)
        print(f"γ={gamma:.1f}  Δt_γ ≈ {dt_g*1e6:.3f} μs")
    # Ratios
    almost(_shapiro_ppn_gamma(dt_gr, 1.5)/_shapiro_ppn_gamma(dt_gr, 0.5),
           (1+1.5)/(1+0.5), rel=1e-12)

def test_ppn_gamma_numeric_ray_analytic():
    banner("PPN-γ: numeric ray vs analytic (analytic Fermat, adaptive RK4)")

    def robust_angle(k1, k2):
        cdot = float(np.clip(np.dot(k1, k2), -1.0, 1.0))
        x = float(np.linalg.norm(np.cross(k1, k2)))
        return math.atan2(x, cdot)

    def n_and_gradn_gamma(x, M, gamma):
        r = float(np.linalg.norm(x))
        n = 1.0 - (1.0 + gamma) * (-G*M/r) / (c*c)  # 1 - (1+γ)Φ/c^2
        gradPhi = (G*M/(r**3 + 1e-30)) * x          # OUTWARD ∇Φ
        gradn = - (1.0 + gamma) * gradPhi / (c*c)   # INWARD ∇n
        return n, gradn

    def rhs(pos, kk, M, gamma):
        n, gn = n_and_gradn_gamma(pos, M, gamma)
        kdotg = float(np.dot(kk, gn))
        dkds = (gn - kdotg*kk)/max(n, 1e-30)
        return kk, dkds

    def rk4_step(pos, kk, ds, M, gamma):
        dx1, dk1 = rhs(pos, kk, M, gamma)
        p2 = pos + 0.5*ds*dx1; k2 = kk + 0.5*ds*dk1; k2/=np.linalg.norm(k2)
        dx2, dk2 = rhs(p2, k2, M, gamma)
        p3 = pos + 0.5*ds*dx2; k3 = kk + 0.5*ds*dk2; k3/=np.linalg.norm(k3)
        dx3, dk3 = rhs(p3, k3, M, gamma)
        p4 = pos + ds*dx3;     k4 = kk + ds*dk3;     k4/=np.linalg.norm(k4)
        dx4, dk4 = rhs(p4, k4, M, gamma)
        pos_new = pos + (ds/6.0)*(dx1 + 2*dx2 + 2*dx3 + dx4)
        k_new   = kk  + (ds/6.0)*(dk1 + 2*dk2 + 2*dk3 + dk4)
        return pos_new, k_new/np.linalg.norm(k_new)

    M_sun = 1.98847e30; R_sun = 6.9634e8
    b = 1.0*R_sun;  L = 30.0*R_sun
    k0 = np.array([1.0,0.0,0.0], float)

    for gamma in (0.5, 1.5):
        x = np.array([-L, b, 0.0], float)
        k = k0.copy()
        dtheta_cap = 0.005 * (math.pi/648000.0)
        steps_nominal = 20000
        ds_nom = (2.0*L)/steps_nominal
        ds_min = ds_nom*1e-4; ds_max = ds_nom*1.0

        s_guard = 0
        while x[0] < L and s_guard < 5*steps_nominal:
            s_guard += 1
            _, dk1 = rhs(x, k, M_sun, gamma)
            rate = float(np.linalg.norm(dk1))
            ds = min(ds_nom, max(ds_min, min(ds_max, dtheta_cap/rate))) if rate>0 else ds_nom
            x, k = rk4_step(x, k, ds, M_sun, gamma)

        theta_num = robust_angle(k0, k) * ARCSEC
        theta_ppn = _theta_ppn_gamma(M_sun, b, gamma) * ARCSEC
        rel_err   = abs(theta_num - theta_ppn)/max(theta_ppn, 1e-30)
        print(f"γ={gamma:.1f}  θ_num={theta_num:.4f}\"  θ_PPN={theta_ppn:.4f}\"  rel err={rel_err*100:.2f}%")
        assert rel_err < 0.02, f"PPN γ={gamma} ray deviates >2%"

def test_frame_dragging_lense_thirring_scaling():
    """
    Frame-dragging (Lense–Thirring) sanity check:
    Ω_LT = 2 G J / (c^2 r^3), with J = k M R^2 Ω  (k≈0.4 uniform sphere).
    We assert linear scaling with Ω and sign flip with −Ω.
    """
    banner("Frame dragging (Lense–Thirring) — scaling sanity")

    M = 1.98847e30          # kg  (solar mass)
    R = 6.9634e8            # m   (solar radius)
    r = 4.0*R               # test radius from center
    k = 0.4                 # uniform sphere moment factor

    def omega_LT(Om):
        J = k*M*(R**2)*Om
        return 2.0*G*J/(c*c*(r**3))   # rad/s

    Om1 = 2.7e-6            # rad/s (solar-ish)
    Om2 = 2*Om1

    lt1 = omega_LT(Om1)
    lt2 = omega_LT(Om2)
    lt_neg = omega_LT(-Om1)

    print(f"Ω={Om1:.3e} ⇒ Ω_LT={lt1:.3e} rad/s")
    print(f"Ω={Om2:.3e} ⇒ Ω_LT={lt2:.3e} rad/s  (expect ×2)")
    print(f"Ω={-Om1:.3e} ⇒ Ω_LT={lt_neg:.3e} rad/s  (expect sign flip)")

    # Linear scaling and sign
    almost(lt2/lt1, 2.0, rel=1e-12)
    assert lt_neg < 0.0 and abs(lt_neg/lt1) > 0.99 and abs(lt_neg/lt1) < 1.01, "Sign/magnitude mismatch"


def test_extended_gaussian_lens_numeric_vs_thin():
    """
    Extended (Gaussian) lens: numeric ray (analytic Fermat) vs thin-lens formula.
    3D Gaussian density ρ gives a 2D Gaussian Σ after projection:
      Σ(R) = M/(2πσ^2) exp(-R^2/2σ^2)  ⇒  M_2D(<b) = M[1 - exp(-b^2/2σ^2)]
    Thin-lens deflection with PPN γ:
      α_thin(b) = ((1+γ) * 2G / (c^2 b)) * M_2D(<b)
    We integrate a ray through the analytic n(r), ∇n(r) for the same 3D Gaussian and
    compare α_num to α_thin for a few b’s (2% tolerance).
    """
    banner("Extended Gaussian lens — numeric ray vs thin-lens (analytic Fermat)")

    def robust_angle(k1, k2):
        cdot = float(np.clip(np.dot(k1, k2), -1.0, 1.0))
        x = float(np.linalg.norm(np.cross(k1, k2)))
        return math.atan2(x, cdot)

    # 3D Gaussian mass: M_enc(r) and Φ, ∇Φ
    def M_enc_gauss(M, sigma, r):
        if r == 0.0: return 0.0
        x = r/(math.sqrt(2.0)*sigma)
        return M*( math.erf(x) - math.sqrt(2.0/math.pi)*(r/sigma)*math.exp(-0.5*(r*r)/(sigma*sigma)) )

    def grad_phi_gauss(M, sigma, xvec):
        r = float(np.linalg.norm(xvec))
        if r == 0.0: return np.zeros(3)
        gmag = G*M_enc_gauss(M, sigma, r)/(r*r)  # |a| = GM_enc/r^2
        return (gmag/r) * xvec                    # OUTWARD ∇Φ

    # PPN-γ analytic Fermat fields for Gaussian lens
    def n_and_gradn_gauss_gamma(x, M, sigma, gamma=1.0):
        r = float(np.linalg.norm(x))
        # Φ(r) for Gaussian:
        if r == 0.0:
            Phi = -G*M/(math.sqrt(2.0*math.pi)*sigma)
        else:
            xg = r/(math.sqrt(2.0)*sigma)
            Phi = -G*M*math.erf(xg)/r + G*M/(math.sqrt(2.0*math.pi)*sigma)*math.exp(-0.5*(r*r)/(sigma*sigma))
        n = 1.0 - (1.0 + gamma)*Phi/(c*c)
        gradn = - (1.0 + gamma) * grad_phi_gauss(M, sigma, x) / (c*c)
        return n, gradn

    def rhs(pos, kk, M, sigma, gamma):
        n, gn = n_and_gradn_gauss_gamma(pos, M, sigma, gamma)
        kdotg = float(np.dot(kk, gn))
        dkds = (gn - kdotg*kk) / max(n, 1e-30)
        return kk, dkds

    def rk4_step(pos, kk, ds, M, sigma, gamma):
        dx1, dk1 = rhs(pos, kk, M, sigma, gamma)
        p2 = pos + 0.5*ds*dx1; k2 = kk + 0.5*ds*dk1; k2/=np.linalg.norm(k2)
        dx2, dk2 = rhs(p2, k2, M, sigma, gamma)
        p3 = pos + 0.5*ds*dx2; k3 = kk + 0.5*ds*dk2; k3/=np.linalg.norm(k3)
        dx3, dk3 = rhs(p3, k3, M, sigma, gamma)
        p4 = pos + ds*dx3;     k4 = kk + ds*dk3;     k4/=np.linalg.norm(k4)
        dx4, dk4 = rhs(p4, k4, M, sigma, gamma)
        pos_new = pos + (ds/6.0)*(dx1 + 2*dx2 + 2*dx3 + dx4)
        k_new   = kk  + (ds/6.0)*(dk1 + 2*dk2 + 2*dk3 + dk4)
        return pos_new, k_new/np.linalg.norm(k_new)

    # Scenario
    M = 1.98847e30          # kg (solar mass)
    R = 6.9634e8            # m  (R_sun)
    sigma = 0.5*R           # Gaussian core size
    gamma = 1.0             # GR
    L = 30.0*R              # integrate from -L to +L
    steps = 20000           # RK4 steps
    ds = (2.0*L)/steps

    def alpha_thin(b):
        # Thin-lens 2D Gaussian enclosed mass:
        M2D = M*(1.0 - math.exp(-0.5*(b*b)/(sigma*sigma)))
        return ((1.0 + gamma) * 2.0 * G * M2D) / (c*c*b)  # radians

    for bR in (0.5, 1.0, 2.0):
        b = bR*R
        x = np.array([-L, b, 0.0], float)
        k0 = np.array([1.0, 0.0, 0.0], float)
        k  = k0.copy()

        for _ in range(steps):
            x, k = rk4_step(x, k, ds, M, sigma, gamma)
            if x[0] >= L: break

        theta_num = robust_angle(k0, k)
        theta_th  = alpha_thin(b)
        rel_err   = abs(theta_num - theta_th)/max(theta_th, 1e-30)

        print(f"b={bR:.1f} R_sun  θ_num={theta_num*ARCSEC:.4f}\"  θ_thin={theta_th*ARCSEC:.4f}\"  rel err={rel_err*100:.2f}%")
        assert rel_err < 0.02, "Gaussian lens: numeric vs thin-lens deviates >2%"

# ------------------ Main ------------------

def main():
    fails = 0
    tests = [
        test_light_bending_solar_limb,
        test_light_bending_ratio,
        test_shapiro_delay,
        test_redshift_sun_surface,
        test_energy_has_weight,
        test_phi_invariance_to_u0_floor,
        test_numeric_ray_bending_analytic,
        test_freefall_energy_and_accel,
        test_ppn_gamma_bending_analytic,
        test_ppn_gamma_shapiro_scaling,
        test_ppn_gamma_numeric_ray_analytic,
        test_frame_dragging_lense_thirring_scaling,
        test_extended_gaussian_lens_numeric_vs_thin,
    ]
    for f in tests:
        try:
            f()
        except AssertionError as e:
            fails += 1
            print(f"❌ {f.__name__}: {e}")
        except Exception as e:
            fails += 1
            print(f"❌ {f.__name__}: unexpected error: {e}")

    print("\n=== SUMMARY ===")
    if fails == 0:
        print("✅ All falsifiers passed."); sys.exit(0)
    else:
        print(f"❌ {fails} falsifier(s) failed."); sys.exit(1)

if __name__ == "__main__":
    main()

