"""
Physical constants and fundamental parameters for nuclear binding calculations.
Based on James Freeman's theory framework.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class PhysicsConstants:
    """Fundamental physical constants in natural units"""
    
    # Basic constants
    c: float = 1.0                    # Speed of light (natural units)
    hbar: float = 1.0                 # Reduced Planck constant
    m_e: float = 0.511               # Electron rest mass (MeV/c²)
    m_p: float = 938.272             # Proton rest mass (MeV/c²)
    m_n: float = 939.565             # Neutron rest mass (MeV/c²)
    alpha: float = 1/137.036         # Fine structure constant
    
    # James's theory parameters
    beta_0: float = 0.90             # Initial lepton velocity (v/c)
    gamma_0: float = 1.0 / np.sqrt(1 - 0.90**2)  # ≈ 2.294
    
    # Geometry scale factors
    s_deuteron: float = 1.6          # Deuteron pore sharing factor
    s_A3: float = 1.9                # A=3 nuclei sharing factor
    s_A4: float = 2.0                # A=4 nuclei sharing factor
    
    # Nuclear parameters
    neutron_lifetime: float = 880.0   # Free neutron lifetime (seconds)
    orbital_frequency: float = 4.4e22 # Hz, from theory
    
    # Mass differences (experimental)
    mn_mp_diff: float = 1.293        # MeV (neutron - proton)
    effective_diff: float = 0.782    # MeV (after electron mass)

# Global constants instance
CONSTANTS = PhysicsConstants()

def get_experimental_binding_energies() -> Dict[str, float]:
    """Return experimental nuclear binding energies (MeV)"""
    return {
        'deuteron': -2.224,
        'tritium': -8.482,
        'helium3': -7.718,
        'helium4': -28.30
    }

def get_nuclear_properties() -> Dict[str, Dict[str, Any]]:
    """Return nuclear composition and properties"""
    return {
        'deuteron': {
            'A': 2, 'Z': 1, 'N': 1,
            'configuration': 'N-P',
            'edges': {'NP': 1},
            'description': 'Single NP channel'
        },
        'tritium': {
            'A': 3, 'Z': 1, 'N': 2,
            'configuration': 'N-P-N',
            'edges': {'NP': 2, 'NN': 1},
            'description': 'Two NP channels + NN assist'
        },
        'helium3': {
            'A': 3, 'Z': 2, 'N': 1,
            'configuration': 'P-N-P',
            'edges': {'NP': 2, 'PP': 1},
            'description': 'Two NP channels + PP stress'
        },
        'helium4': {
            'A': 4, 'Z': 2, 'N': 2,
            'configuration': 'tetrahedral',
            'edges': {'NP': 4, 'PP': 2, 'NN': 0},
            'description': 'Four NP channels, tetrahedral symmetry'
        }
    }