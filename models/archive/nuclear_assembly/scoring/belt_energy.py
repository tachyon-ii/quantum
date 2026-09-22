"""
Belt energy calculations for nuclear assemblies.
"""

import numpy as np
from typing import Dict, List, Tuple
from geometry.constants import r_eff_HH, r_eff_HT, r_eff_TT


class BeltScorer:
    """
    Calculate belt energies for nuclear configurations.
    """
    
    def __init__(self, alpha: float = 1.0):
        """
        Initialize scorer.
        
        Args:
            alpha: Velocity exponent (typically 1.0-1.5)
        """
        self.alpha = alpha
        
        # Coupling constants (relative strengths)
        self.couplings = {
            'HH': 1.0,
            'HT': 0.42,  # From formula: (3/4)^(2α+1) for α=1
            'TT': 0.17   # Weakest
        }
        
    def belt_length(self, k: int, R: float) -> float:
        """
        Calculate belt length.
        
        Args:
            k: Number of lobes (2 for bi-lemniscate)
            R: Effective radius
            
        Returns:
            Belt length
        """
        return k * 2 * np.pi * R
    
    def bond_index(self, k: int, R: float) -> float:
        """
        Calculate bond index B.
        
        B ∝ (2/k)^(2α+1) / R
        
        Args:
            k: Number of lobes
            R: Effective radius
            
        Returns:
            Bond index
        """
        if k <= 0 or R <= 0:
            return 0.0
        return (2.0 / k) ** (2 * self.alpha + 1) / R
    
    def bond_energy(self, bond_type: str, k: int = 2) -> float:
        """
        Calculate energy for a single bond.
        
        Args:
            bond_type: 'HH', 'HT', or 'TT'
            k: Number of lobes (default 2)
            
        Returns:
            Bond energy (negative for binding)
        """
        # Get effective radius
        if bond_type == 'HH':
            R = r_eff_HH()
        elif bond_type == 'HT':
            R = r_eff_HT()
        elif bond_type == 'TT':
            R = r_eff_TT()
        else:
            raise ValueError(f"Unknown bond type: {bond_type}")
        
        # Calculate bond index
        B = self.bond_index(k, R)
        
        # Apply coupling constant
        J = self.couplings.get(bond_type, 0)
        
        return -J * B
    
    def score_assembly(self, bonds: List[Dict]) -> Dict:
        """
        Score a complete assembly.
        
        Args:
            bonds: List of bond dictionaries
            
        Returns:
            Scoring results
        """
        total_energy = 0
        bond_details = []
        
        for bond in bonds:
            bond_type = bond.get('type', 'HT')
            k = bond.get('k', 2)
            
            energy = self.bond_energy(bond_type, k)
            total_energy += energy
            
            bond_details.append({
                'type': bond_type,
                'k': k,
                'energy': energy
            })
        
        return {
            'total_energy': total_energy,
            'n_bonds': len(bonds),
            'bond_details': bond_details,
            'alpha': self.alpha
        }
    
    def compare_configurations(self, configs: Dict[str, List[Dict]]) -> Dict:
        """
        Compare multiple configurations.
        
        Args:
            configs: Dictionary of name -> bonds list
            
        Returns:
            Comparison results
        """
        results = {}
        
        for name, bonds in configs.items():
            score = self.score_assembly(bonds)
            results[name] = {
                'energy': score['total_energy'],
                'n_bonds': score['n_bonds'],
                'energy_per_bond': score['total_energy'] / score['n_bonds'] if score['n_bonds'] > 0 else 0
            }
        
        # Sort by energy
        sorted_results = sorted(results.items(), key=lambda x: x[1]['energy'])
        
        return {
            'rankings': sorted_results,
            'best': sorted_results[0] if sorted_results else None,
            'details': results
        }
