"""
Physical constants for truncated tetrahedron geometry.
"""

import numpy as np

# Edge length (normalized)
EDGE_LENGTH = 1.0

# Face radii for edge length a
def r_H(a: float = EDGE_LENGTH) -> float:
    """Radius from center to hexagon face center."""
    return (np.sqrt(6) / 4) * a

def r_T(a: float = EDGE_LENGTH) -> float:
    """Radius from center to triangle face center."""
    return (5 * np.sqrt(6) / 12) * a

def delta_t(a: float = EDGE_LENGTH) -> float:
    """Distance between hex and tri face levels."""
    return r_T(a) - r_H(a)

# Belt parameters
def r_eff_HH(a: float = EDGE_LENGTH) -> float:
    """Effective radius for H-H belt."""
    return r_H(a)

def r_eff_HT(a: float = EDGE_LENGTH) -> float:
    """Effective radius for H-T belt."""
    return (r_H(a) + r_T(a)) / 2

def r_eff_TT(a: float = EDGE_LENGTH) -> float:
    """Effective radius for T-T belt."""
    return r_T(a)

# Energy coupling constants (relative)
COUPLING_HH = 1.0
COUPLING_HT = 0.42  # Weaker due to mixed radii
COUPLING_TT = 0.17  # Weakest due to smallest aperture
