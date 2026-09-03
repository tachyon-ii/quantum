"""
theory.py - Theoretical models for electron configuration

Contains ONLY the scientific logic for predicting electron configurations.
This is the heart of the project - pure theory implementation.
"""

import math
import numpy as np
from typing import List, Tuple, Dict, Any
from abc import ABC, abstractmethod


class TheoryBase(ABC):
    """Abstract base class for electron configuration theories"""
    
    @abstractmethod
    def predict_configuration(self, z: int) -> Tuple[List[int], Dict[str, Any]]:
        """
        Predict electron configuration for given atomic number
        
        Args:
            z: Atomic number
            
        Returns:
            Tuple of (configuration, debug_info)
        """
        pass
    
    @abstractmethod
    def get_shell_capacities(self) -> List[int]:
        """Get maximum electron capacity for each shell"""
        pass
    
    def validate_configuration(self, config: List[int]) -> List[str]:
        """
        Validate configuration against theory constraints
        
        Args:
            config: Electron configuration [shell1, shell2, ...]
            
        Returns:
            List of validation errors (empty if valid)
        """
        return []


class FreemanTheory(TheoryBase):
    """
    Freeman's geometric theory of electron shells
    
    Core principles:
    1. Shell radii follow r_n = n²
    2. Shell capacity from surface area: 4πr²/2π = 2n²
    3. Sequential filling: fill lower shells before higher shells
    4. No shell jumping while lower shells have capacity
    """
    
    def __init__(self, debug_mode: bool = True):
        self.debug_mode = debug_mode
        
        # Freeman's core geometric relationships
        self.shell_radii = {n: n**2 for n in range(1, 6)}
        self.shell_capacities = {n: 2 * n**2 for n in range(1, 6)}  # 2, 8, 18, 32, 50
        
        if self.debug_mode:
            print("Freeman Theory Initialized:")
            print(f"  Shell radii: {self.shell_radii}")
            print(f"  Shell capacities: {self.shell_capacities}")
    
    def get_shell_capacities(self) -> List[int]:
        """Get Freeman's 2n² shell capacities"""
        return [self.shell_capacities[n] for n in range(1, 6)]
    
    def predict_configuration(self, z: int) -> Tuple[List[int], Dict[str, Any]]:
        """
        Predict configuration using Freeman's sequential filling rule
        
        Freeman's logic:
        - Fill shell 1 (capacity 2) first
        - Fill shell 2 (capacity 8) second
        - Fill shell 3 (capacity 18) third
        - Fill shell 4 (capacity 32) fourth
        - Fill shell 5 (capacity 50) fifth
        
        NO exceptions, NO shell jumping
        """
        config = [0, 0, 0, 0, 0]
        remaining_electrons = z
        debug_info = {
            "theory": "Freeman Sequential Filling",
            "steps": [],
            "violations": [],
            "capacities": self.shell_capacities
        }
        
        # Fill shells in strict order
        for shell_n in range(1, 6):
            if remaining_electrons <= 0:
                break
                
            capacity = self.shell_capacities[shell_n]
            electrons_to_add = min(remaining_electrons, capacity)
            
            config[shell_n - 1] = electrons_to_add
            remaining_electrons -= electrons_to_add
            
            step_info = {
                "shell": shell_n,
                "added": electrons_to_add,
                "capacity": capacity,
                "remaining": remaining_electrons,
                "config_snapshot": config.copy()
            }
            debug_info["steps"].append(step_info)
            
            if self.debug_mode:
                print(f"    Shell {shell_n}: {electrons_to_add}/{capacity} electrons")
        
        # Check for violations
        violations = self.validate_configuration(config)
        debug_info["violations"] = violations
        
        return config, debug_info
    
    def validate_configuration(self, config: List[int]) -> List[str]:
        """
        Validate configuration against Freeman's constraints
        
        Freeman's rules:
        1. No shell can exceed its 2n² capacity
        2. No shell jumping (higher shell filled while lower shell has space)
        3. All electrons must be accounted for
        """
        errors = []
        
        # Rule 1: Check capacity violations
        for shell_n in range(1, 6):
            electrons = config[shell_n - 1]
            capacity = self.shell_capacities[shell_n]
            
            if electrons > capacity:
                errors.append(f"Shell {shell_n}: {electrons} > {capacity} (violates 2π constraint)")
        
        # Rule 2: Check for shell jumping
        for shell_n in range(1, 5):  # Check shells 1-4
            lower_electrons = config[shell_n - 1]
            lower_capacity = self.shell_capacities[shell_n]
            
            # Check all higher shells
            for higher_shell_n in range(shell_n + 1, 6):
                higher_electrons = config[higher_shell_n - 1]
                
                if lower_electrons < lower_capacity and higher_electrons > 0:
                    errors.append(
                        f"Shell jumping: Shell {shell_n} has {lower_electrons}/{lower_capacity} "
                        f"but shell {higher_shell_n} has {higher_electrons}"
                    )
        
        return errors


class ModifiedFreemanTheory(TheoryBase):
    """
    Modified Freeman theory accounting for orbital energy ordering
    
    Attempts to fix the K/Ca problem by allowing 4s to fill before 3d
    while maintaining Freeman's geometric principles
    """
    
    def __init__(self, debug_mode: bool = True):
        self.debug_mode = debug_mode
        
        # Freeman's geometric shell capacities
        self.shell_capacities = {1: 2, 2: 8, 3: 18, 4: 8, 5: 8}  # Modified shell 4 capacity
        
        # Energy ordering exceptions (based on quantum mechanics)
        self.filling_order = [1, 2, 3, 4, 3, 4, 5]  # 4s before 3d completion
        self.filling_limits = [2, 8, 8, 2, 10, 6, 8]  # Electrons per step
        
    def get_shell_capacities(self) -> List[int]:
        """Get modified shell capacities"""
        return [self.shell_capacities[n] for n in range(1, 6)]
    
    def predict_configuration(self, z: int) -> Tuple[List[int], Dict[str, Any]]:
        """
        Predict using modified filling order
        
        Allows 4s orbital to fill before 3d completion
        """
        config = [0, 0, 0, 0, 0]
        remaining_electrons = z
        debug_info = {
            "theory": "Modified Freeman (4s before 3d)",
            "steps": [],
            "filling_order": self.filling_order,
            "filling_limits": self.filling_limits
        }
        
        step = 0
        while remaining_electrons > 0 and step < len(self.filling_order):
            shell_n = self.filling_order[step]
            limit = self.filling_limits[step]
            
            # How many can we add to this shell at this step?
            current_in_shell = config[shell_n - 1]
            can_add = min(remaining_electrons, limit - current_in_shell)
            
            if can_add > 0:
                config[shell_n - 1] += can_add
                remaining_electrons -= can_add
                
                debug_info["steps"].append({
                    "step": step,
                    "shell": shell_n,
                    "added": can_add,
                    "remaining": remaining_electrons,
                    "config": config.copy()
                })
            
            step += 1
        
        return config, debug_info


class QuantumMechanicalTheory(TheoryBase):
    """
    Simplified quantum mechanical theory for comparison
    
    Uses standard Aufbau principle with orbital energy ordering
    """
    
    def __init__(self):
        # Standard quantum mechanical shell capacities
        self.shell_capacities = [2, 8, 18, 32, 50]
        
        # Aufbau filling order (simplified)
        self.orbital_order = [
            (1, 2),   # 1s
            (2, 2),   # 2s
            (2, 6),   # 2p
            (3, 2),   # 3s
            (3, 6),   # 3p
            (4, 2),   # 4s
            (3, 10),  # 3d
            (4, 6),   # 4p
            (5, 2),   # 5s
        ]
    
    def get_shell_capacities(self) -> List[int]:
        return self.shell_capacities
    
    def predict_configuration(self, z: int) -> Tuple[List[int], Dict[str, Any]]:
        """Predict using Aufbau principle"""
        config = [0, 0, 0, 0, 0]
        remaining_electrons = z
        debug_info = {"theory": "Quantum Mechanical Aufbau", "steps": []}
        
        for shell_n, orbital_capacity in self.orbital_order:
            if remaining_electrons <= 0:
                break
                
            electrons_to_add = min(remaining_electrons, orbital_capacity)
            config[shell_n - 1] += electrons_to_add
            remaining_electrons -= electrons_to_add
            
            debug_info["steps"].append({
                "shell": shell_n,
                "orbital_capacity": orbital_capacity,
                "added": electrons_to_add,
                "remaining": remaining_electrons,
                "config": config.copy()
            })
            
            if remaining_electrons <= 0:
                break
        
        return config, debug_info


# Theory factory for easy switching
AVAILABLE_THEORIES = {
    "freeman": FreemanTheory,
    "modified_freeman": ModifiedFreemanTheory,
    "quantum": QuantumMechanicalTheory
}


def create_theory(theory_name: str, **kwargs) -> TheoryBase:
    """
    Factory function to create theory instances
    
    Args:
        theory_name: Name of theory ("freeman", "modified_freeman", "quantum")
        **kwargs: Theory-specific parameters
        
    Returns:
        Theory instance
    """
    if theory_name not in AVAILABLE_THEORIES:
        available = ", ".join(AVAILABLE_THEORIES.keys())
        raise ValueError(f"Unknown theory '{theory_name}'. Available: {available}")
    
    theory_class = AVAILABLE_THEORIES[theory_name]
    return theory_class(**kwargs)