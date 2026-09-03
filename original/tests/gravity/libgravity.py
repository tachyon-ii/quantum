
# libgravity.py
# Minimal gravity-from-Δt library (weak-field) for the Φ/CMB framework.
# Equations follow:
#   ∇²Φ = 4πG * ((u - u0)/c²)
#   alpha(x) = sqrt(1 + 2Φ/c²)
#   n(x) = 1 - 2Φ/c²
#   Timelike: ẋ = v, ṗ = m a with a = -∇Φ  (mass-independent acceleration)
#   Null rays: d/ds (n k) = ∇n  (Fermat principle in inhomogeneous index)
#
# Fits the ontology: photons are waves OF Φ (n), matter is resonators IN Φ (α). 
# This operationalizes gravity as a gradient in proper time (Δt).
#
# References to user's scrolls:
# - Möbius + photon-as-Φ-wave ontology: turn0file0
# - Electron shells / nuclear geometry energy ledger (for u): turn0file1
# - Nuclear binding energy density as source term u: turn0file2
# - Seven Pillars (gravity from energy-density over CMB floor): turn0file3
#
# Author: Erwin (for James)
# License: MIT

import numpy as np

# -----------------------------
# Physical constants (SI)
# -----------------------------
c = 2.99792458e8          # m/s
G = 6.67430e-11           # m^3 kg^-1 s^-2
sigma_SB = 5.670374419e-8 # W m^-2 K^-4

# Typical CMB energy density ~ a T^4 with a = 4σ/c
a_rad = 4.0 * sigma_SB / c
u0_CMB_2p725K = a_rad * (2.725)**4  # ≈ 4.18e-14 J/m^3

# -----------------------------
# Core field relations
# -----------------------------
def alpha_from_phi(Phi, cval=c):
    """Local clock-rate for v=0 observers: alpha = dτ/dt = sqrt(1 + 2Φ/c^2)."""
    return np.sqrt(1.0 + 2.0*Phi/(cval*cval))

def n_from_phi(Phi, cval=c):
    """Refractive index for null rays in the optical metric: n = 1 - 2Φ/c^2."""
    return 1.0 - 2.0*Phi/(cval*cval)

# -----------------------------
# Poisson solver (FFT, periodic)
# -----------------------------
def phi_from_energy_density_fft(u, dx, dy, dz, u0=u0_CMB_2p725K, Gval=G, cval=c):
    """
    Solve ∇²Φ = 4πG * ((u - u0)/c²) on a uniform periodic grid via FFT.
    For isolated systems, place the mass well inside the domain and pad generously.
    Inputs:
      u: 3D ndarray of energy density [J/m^3]
      dx,dy,dz: cell sizes [m]
    Returns:
      Φ: 3D ndarray of gravitational potential [m^2/s^2]
    """
    rho_eff = (u - u0) / (cval*cval)  # effective mass density [kg/m^3]
    rhs = 4.0*np.pi*Gval * rho_eff

    nx, ny, nz = u.shape
    kx = 2.0*np.pi * np.fft.fftfreq(nx, d=dx)
    ky = 2.0*np.pi * np.fft.fftfreq(ny, d=dy)
    kz = 2.0*np.pi * np.fft.fftfreq(nz, d=dz)
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2

    rhs_hat = np.fft.fftn(rhs)
    Phi_hat = np.zeros_like(rhs_hat, dtype=np.complex128)

    # Avoid division by zero at k=0 by enforcing zero-mean Φ (gauge)
    mask = K2 != 0
    Phi_hat[mask] = - rhs_hat[mask] / K2[mask]
    Phi_hat[~mask] = 0.0 + 0.0j

    Phi = np.fft.ifftn(Phi_hat).real
    return Phi

# -----------------------------
# Finite-difference helpers
# -----------------------------
def grad_central(field, dx, dy, dz):
    """Compute gradient of scalar field with central differences and periodic boundaries."""
    dfdx = (np.roll(field, -1, 0) - np.roll(field, 1, 0)) / (2.0*dx)
    dfdy = (np.roll(field, -1, 1) - np.roll(field, 1, 1)) / (2.0*dy)
    dfdz = (np.roll(field, -1, 2) - np.roll(field, 1, 2)) / (2.0*dz)
    return dfdx, dfdy, dfdz

def sample_trilinear(field, x, y, z, origin, spacing):
    """
    Trilinear sampling with periodic wrap. 
    origin: (x0,y0,z0), spacing: (dx,dy,dz)
    """
    nx, ny, nz = field.shape
    x0, y0, z0 = origin
    dx, dy, dz = spacing

    # fractional indices
    fx = (x - x0) / dx
    fy = (y - y0) / dy
    fz = (z - z0) / dz

    i0 = np.floor(fx).astype(int) % nx
    j0 = np.floor(fy).astype(int) % ny
    k0 = np.floor(fz).astype(int) % nz
    i1 = (i0 + 1) % nx
    j1 = (j0 + 1) % ny
    k1 = (k0 + 1) % nz

    tx = fx - np.floor(fx)
    ty = fy - np.floor(fy)
    tz = fz - np.floor(fz)

    c000 = field[i0, j0, k0]
    c100 = field[i1, j0, k0]
    c010 = field[i0, j1, k0]
    c110 = field[i1, j1, k0]
    c001 = field[i0, j0, k1]
    c101 = field[i1, j0, k1]
    c011 = field[i0, j1, k1]
    c111 = field[i1, j1, k1]

    c00 = c000*(1-tx) + c100*tx
    c10 = c010*(1-tx) + c110*tx
    c01 = c001*(1-tx) + c101*tx
    c11 = c011*(1-tx) + c111*tx

    c0 = c00*(1-ty) + c10*ty
    c1 = c01*(1-ty) + c11*ty

    c = c0*(1-tz) + c1*tz
    return c

# -----------------------------
# Integrators
# -----------------------------
def step_particle(x, v, Phi, origin, spacing, dt):
    """
    Advance a test particle using a = -∇Φ (mass-independent).
    x, v: 3-vectors (numpy arrays)
    Phi: 3D potential grid
    Returns updated (x, v).
    """
    dx, dy, dz = spacing
    # Compute grad at grid; use trilinear to sample each component of grad
    dPhidx, dPhidy, dPhidz = grad_central(Phi, dx, dy, dz)

    gx = sample_trilinear(dPhidx, x[0], x[1], x[2], origin, spacing)
    gy = sample_trilinear(dPhidy, x[0], x[1], x[2], origin, spacing)
    gz = sample_trilinear(dPhidz, x[0], x[1], x[2], origin, spacing)

    a = -np.array([gx, gy, gz])

    v_new = v + a * dt
    x_new = x + v_new * dt
    return x_new, v_new

def step_ray(x, k, Phi, origin, spacing, ds, cval=c):
    """
    Advance a null ray using Fermat with physical arc length ds (meters):
        d/ds (n k) = ∇n,  with n = 1 - 2Φ/c^2.
    The local speed of light is v_opt = c/n; the time step is dt = ds / v_opt.
    Position update: x <- x + k * v_opt * dt = x + k * ds.
    """
    dx, dy, dz = spacing

    # Sample ∇Φ via central differences and n at current x
    dPhidx, dPhidy, dPhidz = grad_central(Phi, dx, dy, dz)

    # trilinear samples
    nloc = 1.0 - 2.0*sample_trilinear(Phi, x[0], x[1], x[2], origin, spacing)/(cval*cval)
    gPx = sample_trilinear(dPhidx, x[0], x[1], x[2], origin, spacing)
    gPy = sample_trilinear(dPhidy, x[0], x[1], x[2], origin, spacing)
    gPz = sample_trilinear(dPhidz, x[0], x[1], x[2], origin, spacing)
    gradn = -2.0*np.array([gPx, gPy, gPz])/(cval*cval)

    kdotg = float(np.dot(k, gradn))
    dk = (gradn - kdotg*k) / max(nloc, 1e-30) * ds  # consistent with d(nk)/ds = ∇n

    # Update k and re-normalize to unity
    k_new = k + dk 
    k_new = k_new / np.linalg.norm(k_new)

    # Local speed of light from refractive index n
    v_opt = cval / max(nloc, 1e-30)
    # Convert pathlength ds to time via ds/c and advance
    x_new = x + k_new * v_opt * (ds / cval)
    return x_new, k_new

# -----------------------------
# Analytic utilities (point mass)
# -----------------------------
def phi_point_mass(x, y, z, M, center=(0.0,0.0,0.0), Gval=G):
    """Analytic Newtonian potential for point mass: Φ = -GM/r."""
    cx, cy, cz = center
    rx = x - cx
    ry = y - cy
    rz = z - cz
    r = np.sqrt(rx*rx + ry*ry + rz*rz)
    # avoid r=0
    return -Gval*M/np.maximum(r, 1e-30)

def deflection_angle_point_mass(M, b, cval=c):
    """GR/Eddington light deflection for impact parameter b: θ = 4GM/(c^2 b) [radians]."""
    return 4.0 * G * M / (cval*cval * b)

def shapiro_delay_point_mass(M, r1, r2, b, cval=c):
    """
    Shapiro time delay for a superior-conjunction path grazing a point mass.
    Approximate formula (r1,r2 >> b): Δt ≈ (2GM/c^3) * ln(4 r1 r2 / b^2).
    """
    return (2.0 * G * M / (cval**3)) * np.log(4.0 * r1 * r2 / (b*b))

def gravitational_redshift_delta_phi(Phi_emitter, Phi_receiver, cval=c):
    """
    Redshift from potential difference (weak field): z ≈ (Φ_receiver - Φ_emitter)/c^2.
    For emission at potential Φ_e and observation at Φ_r (Φ→0 at infinity),
    z ≈ -Φ_e / c^2 if receiver is at infinity.
    """
    return (Phi_receiver - Phi_emitter) / (cval*cval)

def energy_equivalent_mass(U, cval=c):
    """Δm = U / c²."""
    return U / (cval*cval)

def build_orbit_template_series(t, r, v, G=G):   # uses global G by default
    U = -G * 5.972e24 / np.maximum(r,1e-6)  # Earth mass default; pass G*M if needed
    c2 = (2.99792458e8)**2
    return (U - np.mean(U))/c2 - 0.5*(v*v)/c2

def build_tide_template_series(U_tide):
    c2 = (2.99792458e8)**2
    return (U_tide - np.mean(U_tide))/c2


# -----------------------------
# Fermat ray tracer (point mass), PPN-γ
# -----------------------------
def ray_trace_point_analytic(M, b, L, steps=20000, gamma=1.0):
    """
    Analytic Fermat ray tracer for a point mass with PPN-γ.
    Returns total deflection (radians).
    """
    import numpy as np, math

    def n_and_gradn_gamma(pos):
        r = float(np.linalg.norm(pos))
        r = max(r, 1e-30)  # avoid r=0
        Phi = -G*M/r
        n   = 1.0 - (1.0+gamma)*Phi/(c*c)
        gradPhi = (G*M/(r**3)) * pos          # OUTWARD ∇Φ
        gradn   = -(1.0+gamma)*gradPhi/(c*c)  # INWARD ∇n
        return n, gradn

    def rhs(pos, kk):
        # Fermat: d/ds (n k) = ∇n  ⇒  n dk/ds = ∇n − (k·∇n)k
        n, gn = n_and_gradn_gamma(pos)
        kdotg = float(np.dot(kk, gn))
        dkds  = (gn - kdotg*kk) / max(n, 1e-30)
        return kk, dkds

    def rk4(pos, kk, ds):
        # RK4 on arc length with unit-renormalization per stage
        dx1, dk1 = rhs(pos, kk)
        p2 = pos + 0.5*ds*dx1; k2 = kk + 0.5*ds*dk1; k2 /= np.linalg.norm(k2)
        dx2, dk2 = rhs(p2, k2)
        p3 = pos + 0.5*ds*dx2; k3 = kk + 0.5*ds*dk2; k3 /= np.linalg.norm(k3)
        dx3, dk3 = rhs(p3, k3)
        p4 = pos + ds*dx3;     k4 = kk + ds*dk3;     k4 /= np.linalg.norm(k4)
        dx4, dk4 = rhs(p4, k4)                     # ← missing line fixed

        pos_new = pos + (ds/6.0)*(dx1 + 2*dx2 + 2*dx3 + dx4)
        k_new   = kk  + (ds/6.0)*(dk1 + 2*dk2 + 2*dk3 + dk4)
        k_new  /= np.linalg.norm(k_new)
        return pos_new, k_new

    # Integrate from x=-L to +L
    x  = np.array([-L, b, 0.0], float)
    k0 = np.array([ 1.0, 0.0, 0.0], float)
    k  = k0.copy()
    ds = (2.0*L)/max(steps, 1)

    for _ in range(steps):
        x, k = rk4(x, k, ds)
        if x[0] >= L:
            break

    # Robust small angle between k0 and k
    dot  = float(np.clip(np.dot(k0, k), -1.0, 1.0))
    cross= float(np.linalg.norm(np.cross(k0, k)))
    theta = math.atan2(cross, dot)  # radians
    return theta

