"""
fixed_deflection.py - Replace the placeholder deflection function with proper physics
"""

from math import exp, sin, cos, radians, sqrt
from typing import Tuple

def deflection_energy_and_force(r: float, edge_type: str,
                                theta_max_deg: float = 35.0,
                                scale: float = 1.0,
                                r0_hint: float = None) -> Tuple[float, float]:
    """
    Angular deflection model: converts Coulomb repulsion into angular momentum
    through neutron-provided scroll electron fields.
    
    The deflection reduces the effective radial Coulomb force and creates
    binding through angular momentum stabilization.
    """
    
    # Get characteristic distance for this edge type
    if r0_hint is None:
        r0_hint = {"NN": 1.6, "NP": 1.8, "PP": 2.0}.get(edge_type, 1.8)
    
    # Edge-specific deflection efficiency
    # PP edges need maximum deflection (no neutron present)
    # NP edges have partial deflection (one neutron)
    # NN edges have no Coulomb to deflect but can have scroll coupling
    if edge_type == "PP":
        base_efficiency = 0.0  # PP has no neutron for deflection!
    elif edge_type == "NP":
        base_efficiency = 0.8  # One neutron provides deflection
    else:  # NN
        base_efficiency = 0.5  # Scroll-scroll coupling
    
    # Distance-dependent deflection angle
    # Maximum deflection at r0, decreases with distance
    width = 0.3  # Range of deflection effect
    distance_factor = exp(-((r - r0_hint) ** 2) / (2 * width**2))
    
    # Actual deflection angle (in radians)
    theta_max_rad = radians(theta_max_deg)
    theta_actual = theta_max_rad * base_efficiency * distance_factor
    
    # The deflection creates an effective attractive potential
    # by converting radial repulsion into angular momentum
    deflection_depth = -scale * base_efficiency * sin(theta_actual)
    
    # Energy contribution
    U = deflection_depth * distance_factor
    
    # Force (negative gradient)
    dU_dr = deflection_depth * (-(r - r0_hint) / (width**2)) * distance_factor
    F = -dU_dr
    
    return U, F


def coulomb_with_deflection(r: float, edge_type: str, q1: float, q2: float,
                           theta_max_deg: float = 35.0,
                           deflection_scale: float = 1.0,
                           k_e: float = 0.05) -> Tuple[float, float]:
    """
    Combined Coulomb + angular deflection.
    
    The deflection reduces the effective radial Coulomb force by
    redirecting it into angular momentum.
    """
    
    # Raw Coulomb
    r_safe = max(r, 1e-6)
    U_coulomb = k_e * q1 * q2 / r_safe
    F_coulomb = -k_e * q1 * q2 / (r_safe**2)
    
    # Get deflection effect
    U_deflect, F_deflect = deflection_energy_and_force(
        r, edge_type, theta_max_deg, deflection_scale
    )
    
    # Deflection reduces the effective Coulomb
    # (converts radial force to angular)
    deflection_factor = 1.0 + U_deflect  # U_deflect is negative, so this reduces
    
    U_effective = U_coulomb * max(0, deflection_factor) + U_deflect
    F_effective = F_coulomb * max(0, deflection_factor) + F_deflect
    
    return U_effective, F_effective


# Test the new functions
if __name__ == "__main__":
    print("Testing corrected deflection physics")
    print("=" * 60)
    
    # Test deflection alone
    print("\nDeflection energy for different edge types at r=1.8:")
    for edge in ["NN", "NP", "PP"]:
        U, F = deflection_energy_and_force(1.8, edge, theta_max_deg=35, scale=1.0)
        print(f"  {edge}: U={U:8.5f}, F={F:8.5f}")
    
    print("\nDeflection vs distance for NP edge:")
    for r in [1.4, 1.6, 1.8, 2.0, 2.2]:
        U, F = deflection_energy_and_force(r, "NP", theta_max_deg=35, scale=1.0)
        print(f"  r={r}: U={U:8.5f}, F={F:8.5f}")
    
    print("\nEffect of theta_max_deg on NP edge at r=1.8:")
    for theta in [0, 20, 35, 50, 80]:
        U, F = deflection_energy_and_force(1.8, "NP", theta_max_deg=theta, scale=1.0)
        print(f"  theta={theta}°: U={U:8.5f}, F={F:8.5f}")
    
    print("\n" + "=" * 60)
    print("This should be integrated into nuclear_solver.py")
    print("to replace the placeholder deflection function.")
