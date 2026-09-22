"""
Relativistic mechanics calculations for the ice skater mechanism.
Core physics of James Freeman's nuclear binding theory.
"""

import numpy as np
from typing import Tuple, Dict
from dataclasses import dataclass
from .physics_constants import CONSTANTS

@dataclass
class RelativisticState:
    """Represents a relativistic lepton state"""
    gamma: float
    beta: float
    velocity: float
    kinetic_energy: float
    radius: float

class RelativisticMechanics:
    """
    Implements the core relativistic mechanics for the ice skater mechanism.
    
    When nucleons share pores, lepton orbital radius increases by factor s.
    Angular momentum conservation L = mγvr forces velocity to decrease.
    The collapse in γ releases binding energy.
    """
    
    def __init__(self):
        self.m_e = CONSTANTS.m_e
        self.c = CONSTANTS.c
        self.beta_0 = CONSTANTS.beta_0
        self.gamma_0 = CONSTANTS.gamma_0
    
    def calculate_gamma_from_beta(self, beta: float) -> float:
        """Calculate Lorentz factor from velocity ratio"""
        return 1.0 / np.sqrt(1 - beta**2)
    
    def calculate_beta_from_gamma(self, gamma: float) -> float:
        """Calculate velocity ratio from Lorentz factor"""
        return np.sqrt(1 - 1/gamma**2)
    
    def angular_momentum_conservation(self, s: float) -> Tuple[float, float, float]:
        """
        Apply angular momentum conservation L = mγvr = constant
        when radius changes by factor s.
        
        Args:
            s: Radius expansion factor (r_new = s * r_old)
            
        Returns:
            Tuple of (new_gamma, new_beta, k_parameter)
        """
        # Initial angular momentum factor
        gamma_0_beta_0 = self.gamma_0 * self.beta_0
        
        # After radius expansion: γ₁β₁ = γ₀β₀/s
        k = gamma_0_beta_0 / s
        
        # Solve for new state
        gamma_1 = np.sqrt(1 + k**2)
        beta_1 = k / gamma_1
        
        return gamma_1, beta_1, k
    
    def kinetic_energy_change(self, s: float) -> Tuple[float, RelativisticState, RelativisticState]:
        """
        Calculate kinetic energy change per lepton when radius expands by factor s.
        
        Returns:
            Tuple of (delta_K, initial_state, final_state)
        """
        # Initial state
        initial_state = RelativisticState(
            gamma=self.gamma_0,
            beta=self.beta_0,
            velocity=self.beta_0 * self.c,
            kinetic_energy=(self.gamma_0 - 1) * self.m_e,
            radius=1.0  # Normalized
        )
        
        # Final state after radius expansion
        gamma_1, beta_1, k = self.angular_momentum_conservation(s)
        
        final_state = RelativisticState(
            gamma=gamma_1,
            beta=beta_1,
            velocity=beta_1 * self.c,
            kinetic_energy=(gamma_1 - 1) * self.m_e,
            radius=s
        )
        
        # Energy change (negative for binding)
        delta_K = final_state.kinetic_energy - initial_state.kinetic_energy
        
        return delta_K, initial_state, final_state
    
    def binding_energy_per_lepton(self, s: float) -> float:
        """Calculate binding energy released per lepton"""
        delta_K, _, _ = self.kinetic_energy_change(s)
        return -delta_K  # Positive binding energy
    
    def binding_energy_per_channel(self, s: float, num_leptons: int = 2) -> float:
        """Calculate binding energy per channel (typically 2 leptons)"""
        return self.binding_energy_per_lepton(s) * num_leptons
    
    def analyze_velocity_regime(self, s_values: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Analyze how velocity changes across different expansion factors.
        
        Args:
            s_values: Array of radius expansion factors
            
        Returns:
            Dictionary with analysis results
        """
        results = {
            's_values': s_values,
            'gamma_values': np.zeros_like(s_values),
            'beta_values': np.zeros_like(s_values),
            'velocity_values': np.zeros_like(s_values),
            'kinetic_energies': np.zeros_like(s_values),
            'delta_K_values': np.zeros_like(s_values),
            'binding_energies': np.zeros_like(s_values)
        }
        
        for i, s in enumerate(s_values):
            gamma_1, beta_1, _ = self.angular_momentum_conservation(s)
            delta_K, _, final_state = self.kinetic_energy_change(s)
            
            results['gamma_values'][i] = gamma_1
            results['beta_values'][i] = beta_1
            results['velocity_values'][i] = beta_1
            results['kinetic_energies'][i] = final_state.kinetic_energy
            results['delta_K_values'][i] = delta_K
            results['binding_energies'][i] = -delta_K
            
        return results
    
    def validate_conservation_laws(self, s: float, tolerance: float = 1e-10) -> bool:
        """
        Validate that angular momentum is indeed conserved.
        
        Args:
            s: Radius expansion factor
            tolerance: Numerical tolerance for conservation check
            
        Returns:
            True if conservation laws are satisfied
        """
        gamma_1, beta_1, _ = self.angular_momentum_conservation(s)
        
        # Check L = mγvr conservation
        L_initial = self.gamma_0 * self.beta_0 * 1.0  # r₀ = 1 (normalized)
        L_final = gamma_1 * beta_1 * s
        
        conservation_error = abs(L_final - L_initial)
        
        return conservation_error < tolerance
    
    def get_summary_statistics(self) -> Dict[str, float]:
        """Get summary statistics of the relativistic mechanism"""
        
        # Calculate for typical nuclear scales
        s_values = [CONSTANTS.s_deuteron, CONSTANTS.s_A3, CONSTANTS.s_A4]
        
        stats = {
            'initial_gamma': self.gamma_0,
            'initial_beta': self.beta_0,
            'initial_velocity_fraction': self.beta_0,
            'initial_kinetic_energy': (self.gamma_0 - 1) * self.m_e
        }
        
        for i, (name, s) in enumerate(zip(['deuteron', 'A3', 'A4'], s_values)):
            gamma_1, beta_1, _ = self.angular_momentum_conservation(s)
            delta_K, _, _ = self.kinetic_energy_change(s)
            
            stats[f'{name}_final_gamma'] = gamma_1
            stats[f'{name}_final_beta'] = beta_1
            stats[f'{name}_delta_K_per_lepton'] = delta_K
            stats[f'{name}_binding_per_channel'] = -delta_K * 2
            
        return stats

# Example usage and testing
if __name__ == "__main__":
    mechanics = RelativisticMechanics()
    
    # Test ice skater mechanism
    s = 1.6  # Deuteron scale
    delta_K, initial, final = mechanics.kinetic_energy_change(s)
    
    print(f"Ice Skater Mechanism Analysis (s = {s}):")
    print(f"Initial: γ = {initial.gamma:.3f}, β = {initial.beta:.3f}, v = {initial.velocity:.3f}c")
    print(f"Final:   γ = {final.gamma:.3f}, β = {final.beta:.3f}, v = {final.velocity:.3f}c")
    print(f"ΔK per lepton: {delta_K:.3f} MeV")
    print(f"Binding per channel: {-delta_K * 2:.3f} MeV")
    
    # Validate conservation
    is_conserved = mechanics.validate_conservation_laws(s)
    print(f"Angular momentum conserved: {is_conserved}")