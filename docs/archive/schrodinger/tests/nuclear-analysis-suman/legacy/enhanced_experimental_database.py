#!/usr/bin/env python3
"""
Advanced Nuclear Database - Enhanced Format Parser
Handles the new comprehensive nuclear data format with uncertainties and decay data

This is the complete "Database of Ground Truths" that James Freeman specified
"""

import os
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AdvancedNuclearData:
    """Complete nuclear data structure with uncertainties"""
    N: int  # Neutrons
    Z: int  # Protons  
    A: int  # Mass number
    element: str  # Element symbol
    mass_excess_kev: float  # Mass excess in keV
    mass_excess_uncertainty: float  # Uncertainty in keV
    binding_energy_kev: float  # Total binding energy in keV
    binding_energy_uncertainty: float  # Uncertainty in keV
    decay_mode: str  # Decay mode (B-, B+, EC, α, etc.)
    decay_energy_kev: float  # Q-value for decay in keV
    decay_uncertainty: float  # Uncertainty in decay energy
    atomic_mass_u: float  # Atomic mass in atomic mass units
    atomic_mass_uncertainty: float  # Uncertainty in atomic mass
    
    # Derived properties
    binding_energy_mev: float = None
    binding_energy_per_nucleon: float = None
    is_stable: bool = None
    separation_energy_n: float = None  # Neutron separation energy
    separation_energy_p: float = None  # Proton separation energy
    
    def __post_init__(self):
        # Convert to MeV
        self.binding_energy_mev = self.binding_energy_kev / 1000.0
        
        # Calculate binding energy per nucleon
        if self.A > 0:
            self.binding_energy_per_nucleon = self.binding_energy_mev / self.A
        
        # Determine stability (simplified)
        self.is_stable = self.decay_mode == '*' or self.decay_energy_kev == 0
        
    def get_nuclear_radius_fm(self) -> float:
        """Estimate nuclear radius using empirical formula"""
        return 1.2 * (self.A**(1/3))
    
    def get_q_value_mev(self) -> float:
        """Get decay Q-value in MeV"""
        return self.decay_energy_kev / 1000.0 if self.decay_energy_kev > 0 else 0.0

class AdvancedNuclearDatabase:
    """
    Complete experimental nuclear database
    Handles the advanced format with uncertainties and decay data
    """
    
    def __init__(self, data_file: str = "binding-energy.txt"):
        self.nuclei: Dict[str, AdvancedNuclearData] = {}
        self.separation_energies: Dict[str, Dict[str, float]] = {}
        self.load_nuclear_data(data_file)
        self.calculate_separation_energies()
    
    def load_nuclear_data(self, data_file: str):
        """Load comprehensive nuclear dataset"""
        
        if os.path.exists(data_file):
            logger.info(f"Loading advanced nuclear data from {data_file}")
            self._parse_advanced_format(data_file)
        else:
            logger.warning(f"Advanced data file {data_file} not found, using fallback")
            self._load_fallback_data()
        
        logger.info(f"Loaded {len(self.nuclei)} nuclear data points with uncertainties")
    
    def _parse_advanced_format(self, filename: str):
        """Parse the advanced nuclear data format"""
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            # Skip header line
            for line in lines[1:]:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                try:
                    parts = line.split()
                    if len(parts) < 10:
                        continue
                    
                    # Parse fields
                    N = int(parts[0])
                    Z = int(parts[1]) 
                    A = int(parts[2])
                    element = parts[3].strip()
                    
                    # Mass excess and uncertainty
                    mass_excess = self._parse_value_with_uncertainty(parts[4])
                    mass_uncertainty = self._parse_value_with_uncertainty(parts[5])
                    
                    # Binding energy and uncertainty
                    binding_energy = self._parse_value_with_uncertainty(parts[6])
                    binding_uncertainty = self._parse_value_with_uncertainty(parts[7])
                    
                    # Decay information
                    decay_mode = parts[8].strip() if len(parts) > 8 else '*'
                    decay_energy = self._parse_value_with_uncertainty(parts[9]) if len(parts) > 9 else 0
                    decay_unc = self._parse_value_with_uncertainty(parts[10]) if len(parts) > 10 else 0
                    
                    # Atomic mass
                    atomic_mass = self._parse_value_with_uncertainty(parts[12]) if len(parts) > 12 else 0
                    atomic_mass_unc = self._parse_value_with_uncertainty(parts[13]) if len(parts) > 13 else 0
                    
                    # Create nucleus data
                    nucleus = AdvancedNuclearData(
                        N=N, Z=Z, A=A, element=element,
                        mass_excess_kev=mass_excess,
                        mass_excess_uncertainty=mass_uncertainty,
                        binding_energy_kev=binding_energy,
                        binding_energy_uncertainty=binding_uncertainty,
                        decay_mode=decay_mode,
                        decay_energy_kev=decay_energy,
                        decay_uncertainty=decay_unc,
                        atomic_mass_u=atomic_mass,
                        atomic_mass_uncertainty=atomic_mass_unc
                    )
                    
                    # Store with multiple lookup keys
                    self._store_nucleus(nucleus)
                    
                except (ValueError, IndexError) as e:
                    logger.debug(f"Could not parse line: {line[:50]}... - {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error reading {filename}: {e}")
            self._load_fallback_data()
    
    def _parse_value_with_uncertainty(self, value_str: str) -> float:
        """Parse values that may have # markers or uncertainties"""
        if not value_str or value_str == '*':
            return 0.0
        
        # Remove # markers (experimental estimates)
        clean_str = value_str.replace('#', '').strip()
        
        try:
            return float(clean_str)
        except ValueError:
            return 0.0
    
    def _store_nucleus(self, nucleus: AdvancedNuclearData):
        """Store nucleus with multiple lookup keys"""
        keys = [
            f"{nucleus.Z}_{nucleus.A}",
            f"{nucleus.Z}p_{nucleus.N}n", 
            f"{nucleus.element}-{nucleus.A}",
            f"{nucleus.element}{nucleus.A}"
        ]
        
        for key in keys:
            self.nuclei[key] = nucleus
    
    def _load_fallback_data(self):
        """Fallback data based on the first dataset"""
        fallback_nuclei = [
            (1, 1, 2, "H", 13135.7, 0.0, 1112.28, 0.0, "B-", 0, 0),
            (2, 2, 4, "He", 2424.9, 0.0, 7073.92, 0.0, "*", 0, 0),
            (4, 3, 7, "Li", 14907.1, 0.0, 5606.44, 0.0, "B-", 0, 0),
            (4, 4, 8, "Be", 4941.7, 0.0, 7062.44, 0.0, "B-", 0, 0),
            (6, 6, 12, "C", 0, 0.0, 7680.14, 0.0, "*", 0, 0),
            (8, 8, 16, "O", 0, 0.0, 7052.28, 0.0, "*", 0, 0),
        ]
        
        for N, Z, A, element, mass_excess, mass_unc, binding, bind_unc, decay, decay_E, decay_unc in fallback_nuclei:
            nucleus = AdvancedNuclearData(
                N=N, Z=Z, A=A, element=element,
                mass_excess_kev=mass_excess,
                mass_excess_uncertainty=mass_unc,
                binding_energy_kev=binding,
                binding_energy_uncertainty=bind_unc,
                decay_mode=decay,
                decay_energy_kev=decay_E,
                decay_uncertainty=decay_unc,
                atomic_mass_u=A,  # Approximation
                atomic_mass_uncertainty=0.0
            )
            self._store_nucleus(nucleus)
    
    def calculate_separation_energies(self):
        """Calculate neutron and proton separation energies"""
        
        for key, nucleus in self.nuclei.items():
            if '_' not in key:
                continue
                
            Z, A = nucleus.Z, nucleus.A
            N = nucleus.N
            
            # Neutron separation energy S_n = BE(Z,N) - BE(Z,N-1)
            if N > 0:
                parent_key = f"{Z}_{A-1}"
                if parent_key in self.nuclei:
                    parent = self.nuclei[parent_key]
                    s_n = nucleus.binding_energy_mev - parent.binding_energy_mev
                    nucleus.separation_energy_n = s_n
            
            # Proton separation energy S_p = BE(Z,N) - BE(Z-1,N)
            if Z > 0:
                parent_key = f"{Z-1}_{A-1}"
                if parent_key in self.nuclei:
                    parent = self.nuclei[parent_key]
                    s_p = nucleus.binding_energy_mev - parent.binding_energy_mev
                    nucleus.separation_energy_p = s_p
    
    def get_nucleus(self, protons: int, neutrons: int) -> Optional[AdvancedNuclearData]:
        """Get nucleus by protons and neutrons"""
        key = f"{protons}p_{neutrons}n"
        return self.nuclei.get(key)
    
    def get_nucleus_by_z_a(self, Z: int, A: int) -> Optional[AdvancedNuclearData]:
        """Get nucleus by Z and A"""
        key = f"{Z}_{A}"
        return self.nuclei.get(key)
    
    def get_all_stable_nuclei(self) -> List[AdvancedNuclearData]:
        """Get all stable nuclei in the database"""
        stable_nuclei = []
        seen = set()
        for nucleus in self.nuclei.values():
            key = f"{nucleus.Z}_{nucleus.A}"
            if key not in seen and nucleus.is_stable:
                stable_nuclei.append(nucleus)
                seen.add(key)
        return stable_nuclei