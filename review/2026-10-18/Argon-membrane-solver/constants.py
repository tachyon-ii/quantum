# models/binding/membrane/constants.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import math

# Physical constants — one source each (CODATA 2018 / AME2020 / corpus §2)
HC        = 197.3269804                  # MeV fm            CODATA 2018
AHC       = 1.439964547                  # alpha*hbar*c, MeV fm   CODATA 2018
ME        = 0.510998950                  # MeV               CODATA 2018
MP        = 938.2720882                  # MeV               CODATA 2018
MN        = 939.5654205                  # MeV               CODATA 2018
RP        = 0.8409                       # fm, proton charge radius   CODATA 2018
RN        = 1.023 * RP                   # fm, neutron capsid radius  posit P1
BE_D      = 2.224566                     # MeV   AME2020   — CALIBRATION
BE_HE4    = 28.29566                     # MeV   AME2020   — CALIBRATION
E_SINGLET = -0.0660                      # MeV   np virtual state — CALIBRATION of mesh term
CPRIME    = math.sqrt(1.0 - (ME / (MN - MP))**2)  # 0.91864   three-term-binding.md §7a

def Y(n):
    """Slingshot per capsid, lane length n = A."""
    return ME * ((MN - MP) / ME - 1.0 / math.sqrt(1.0 - (CPRIME / n)**2)) if n > 1 else 0.0

# Closed-form mesh shear constant (§4.2)
E_PATCH_D = BE_D - 2.0 * Y(2)            # 0.788624 MeV
E_MESH    = E_PATCH_D - E_SINGLET        # 0.854624 MeV

# Numerical/mesh constants (§2, §3, §6)
SUBDIV        = 3                        # icosphere subdivision (642 verts, 1280 faces)
SUBDIV_CONV   = 4                        # convergence check subdivision (2562 verts, 5120 faces)
DELTA_GRID    = [0.05 * RP, 0.10 * RP, 0.20 * RP, 0.30 * RP]  # fm, scanned not fitted
K_AREA_MULT   = 50.0                     # K_AREA = 50 * E0 / A_i^0
K_PEN_MULT    = 10.0                     # K_PEN  = 10 * e0 / (0.05 * RP)^2
K_PEN_SCALE   = 0.05 * RP
K_BEND_PRI    = 0.0                      # Primary run K_BEND = 0
K_BEND_VAR    = 0.01                     # Variant K_BEND = 0.01 * E0
D_INIT        = 1.70                     # fm, starting centre separation (§5)
GTOL          = 1e-8                     # L-BFGS-B gtol (§4.1)
F_STEP        = 0.02                     # MeV/fm load path step (§6)
Z_DISPL_GRID  = [0.0, 0.05, -0.05, 0.10, -0.10, 0.20, -0.20, 0.30, -0.30]  # fm (§7.3)

# Any numerical regularizer not in §2 is logged here for the report header (§4.3, §10)
UNDECLARED_NUMERIC = {
    'EPS_NORM': (1e-12, 'Safe denominator floor for vector norms in analytic gradients'),
    'MAX_ITER_RELAX': (600, 'Maximum L-BFGS-B iterations per quasi-static relaxation call'),
    'F_MAX_STEPS': (150, 'Maximum force steps (3.0 MeV/fm ceiling) on load path before halt'),
}