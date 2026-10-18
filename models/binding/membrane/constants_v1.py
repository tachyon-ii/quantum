"""constants.py — every number used by the membrane solver. BUILD-SPEC-membrane-solver.md §2.
Implementer: Grace (Claude Opus 5.5), 18 Oct 2026."""
from math import sqrt
HC      = 197.3269804     # MeV fm            CODATA 2018
AHC     = 1.439964547     # alpha*hbar*c      CODATA 2018
ME      = 0.510998950     # MeV               CODATA 2018
MP      = 938.2720882     # MeV               CODATA 2018
MN      = 939.5654205     # MeV               CODATA 2018
RP      = 0.8409          # fm  proton charge radius  CODATA 2018
RN      = 1.023 * RP      # fm  posit P1 (the-fractal-nucleus.md §6a)
BE_D    = 2.224566        # MeV AME2020  CALIBRATION
BE_HE4  = 28.29566        # MeV AME2020  CALIBRATION
E_SINGLET = -0.0660       # MeV np virtual state  CALIBRATION of mesh term
CPRIME  = sqrt(1 - (ME/(MN-MP))**2)
def Y(n): return ME*((MN-MP)/ME - 1/sqrt(1-(CPRIME/n)**2)) if n > 1 else 0.0
# --- numerical / mesh (declared, not physical) ---
SUBDIV     = 3
K_AREA_FAC = 50.0         # K_AREA = 50 E0 / A0
K_PEN_FAC  = 10.0         # K_PEN  = 10 e0 / (0.05 RP)^2
K_BEND_FAC = 0.0          # primary run; variant 0.01
DELTA_GRID = [0.05*RP, 0.10*RP, 0.20*RP, 0.30*RP]
FADE       = 'linear'     # 'linear' primary; 'quad' variant
# --- ADDED at build time (not in spec) — listed in report 'added' table ---
GAP_MARGIN   = 0.10       # fm: vertex pre-screen radius beyond partner bound + delta (pure speed; no physics)
TETHER_K     = 2000.0     # MeV/fm^2: centroid tether for P2,P3 in load paths (rotation gauge / inertial anvil), §6
F_STEP_COARSE= 0.20       # MeV/fm coarse load step; bracket then bisect to 0.02 (spec §6 resolution)
F_STEP_FINE  = 0.02
K_NEAR       = 24         # faces blended in the gap
GAP_H        = 0.4        # Gaussian blend width, in rest mean edge lengths
FADE_EPS     = 0.05       # softplus rounding of the fade corners, in units of delta
CONTACT_FRAC = 0.5        # a pair is 'in contact' if any vertex has g < 0.5 delta
