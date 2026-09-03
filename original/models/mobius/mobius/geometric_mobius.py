"""
Geometric Möbius implementation for Freeman's physical theory.

This module implements the Möbius strip as a physical energy configuration
in the CMB/Φ-field, following James Freeman's geometric theory where:
- Mass = captured energy in stable geometric configurations
- Möbius strips are physical defects in spacetime, not mathematical surfaces
- Energy density creates local Φ-field gradients (following gravity theory)
- Helicity at crossing points determines matter/antimatter classification
"""

import numpy as np
from typing import Tuple, Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class HelicityType(Enum):
    """Helicity classification at Möbius crossing point."""
    LEFT = -1   # Left-handed helicity (antimatter)
    RIGHT = 1   # Right-handed helicity (matter)
    UNDEFINED = 0  # Undetermined or mixed

class PoleType(Enum):
    """Pole types in Möbius configuration."""
    NORTH = "N"   # North magnetic pole at vertex
    SOUTH = "S"   # South magnetic pole at vertex  
    EAST_PLUS = "E+"   # East positive at centroid
    WEST_MINUS = "W-"  # West negative at centroid

@dataclass
class EnergyConfiguration:
    """Energy distribution parameters for Möbius strip."""
    total_captured_energy: float  # Total energy captured from CMB/Φ-field (Joules)
    peak_energy_density: float    # Peak energy density (J/m³)
    energy_decay_length: float    # Characteristic decay length (m)
    binding_energy: float         # Energy required to maintain configuration (J)
    capture_efficiency: float     # Efficiency of CMB energy capture (0-1)
    
@dataclass
class GeometricProperties:
    """Geometric properties of the physical Möbius strip."""
    characteristic_length: float  # Characteristic size scale (m)
    twist_energy: float           # Energy associated with π twist (J)
    topological_charge: float     # Topological invariant
    stability_index: float        # Measure of configuration stability (0-1)
    
@dataclass
class PoleConfiguration:
    """Configuration of magnetic/electric poles in Möbius strip."""
    north_position: np.ndarray    # 3D position of north pole
    south_position: np.ndarray    # 3D position of south pole
    east_position: np.ndarray     # 3D position of east pole
    west_position: np.ndarray     # 3D position of west pole
    
    magnetic_moment: float        # Magnetic dipole moment
    electric_moment: float        # Electric dipole moment
    
class GeometricMobius:
    """
    Physical Möbius strip as energy configuration in CMB/Φ-field.
    
    Based on James Freeman's theory where:
    - Möbius strips are stable energy configurations, not mathematical surfaces
    - They capture energy from the CMB/Φ-field medium
    - Create local spacetime curvature through energy density
    - Have definite helicity that determines matter/antimatter classification
    - Poles located at vertices (N-S) and centroid (E+/-)
    """
    
    # Physical constants from James's gravity theory
    CMB_ENERGY_DENSITY = 4.17e-14  # J/m³ (approximate CMB energy density)
    PHI_FIELD_COUPLING = 1.0       # Coupling strength to Φ-field
    PLANCK_LENGTH = 1.616e-35      # m
    PLANCK_ENERGY = 1.956e9        # J
    
    def __init__(self, characteristic_size: float = 1e-15):
        """
        Initialize geometric Möbius strip.
        
        Args:
            characteristic_size: Characteristic length scale in meters
        """
        self.characteristic_size = characteristic_size
        
        # Energy configuration
        self.energy_config = None
        self.geometric_props = None
        self.pole_config = None
        
        # Helicity properties
        self.helicity = HelicityType.UNDEFINED
        self.crossing_point = np.zeros(3)
        
        # Φ-field properties (following James's gravity theory)
        self.phi_field_strength = 0.0
        self.local_time_dilation = 1.0  # α(x) factor from gravity theory
        
        # Energy density distribution
        self.energy_density_field = None
        self.phi_gradient_field = None
        
        # Stability and dynamics
        self.is_stable = False
        self.decay_rate = 0.0
        self.self_repair_rate = 0.0
        
        logger.info(f"Initialized geometric Möbius with size scale {characteristic_size:.2e} m")
    
    def initialize_energy_configuration(self, captured_energy: float) -> None:
        """
        Initialize energy configuration based on captured CMB energy.
        
        Args:
            captured_energy: Total energy captured from CMB/Φ-field (J)
        """
        # Calculate energy parameters
        volume_scale = self.characteristic_size**3
        peak_density = captured_energy / volume_scale
        decay_length = self.characteristic_size * 0.5  # Energy spreads over half the structure
        
        # Binding energy from topological constraint (π twist energy cost)
        twist_energy = self._calculate_twist_energy()
        binding_energy = twist_energy * 1.2  # 20% overhead for maintaining twist
        
        # Capture efficiency depends on size (smaller = more efficient)
        capture_efficiency = min(1.0, (self.PLANCK_LENGTH / self.characteristic_size)**0.5)
        
        self.energy_config = EnergyConfiguration(
            total_captured_energy=captured_energy,
            peak_energy_density=peak_density,
            energy_decay_length=decay_length,
            binding_energy=binding_energy,
            capture_efficiency=capture_efficiency
        )
        
        logger.info(f"Energy configuration: {captured_energy:.2e} J captured, "
                   f"efficiency {capture_efficiency:.3f}")
    
    def _calculate_twist_energy(self) -> float:
        """Calculate energy cost of maintaining π twist in Möbius topology."""
        # Energy cost scales with curvature and size
        # Based on elastic energy in twisted ribbon
        
        # Twist energy density (J/m³)
        twist_density = self.PHI_FIELD_COUPLING / (self.characteristic_size**2)
        
        # Total twist energy over Möbius volume
        volume = np.pi * self.characteristic_size**3  # Approximate Möbius volume
        twist_energy = twist_density * volume
        
        return twist_energy
    
    def calculate_energy_distribution(self, resolution: int = 1000) -> np.ndarray:
        """
        Calculate energy density distribution along Möbius path.
        
        Args:
            resolution: Number of points along path
            
        Returns:
            Array of energy densities along path
        """
        if self.energy_config is None:
            raise ValueError("Energy configuration not initialized")
        
        # Parametric coordinate along Möbius path (0 to 4π)
        u = np.linspace(0, 4 * np.pi, resolution)
        
        # Energy distribution has specific structure
        # Peak at crossing point, decay along path
        crossing_position = 2 * np.pi  # Middle of 4π path
        
        # Distance from crossing point (with periodic boundary)
        dist_from_crossing = np.minimum(
            np.abs(u - crossing_position),
            4 * np.pi - np.abs(u - crossing_position)
        )
        
        # Exponential decay from crossing point
        energy_density = (self.energy_config.peak_energy_density * 
                         np.exp(-dist_from_crossing / self.energy_config.energy_decay_length))
        
        # Add topological enhancement at crossing
        crossing_enhancement = 1 + 0.5 * np.exp(-(dist_from_crossing / (0.1 * self.energy_config.energy_decay_length))**2)
        energy_density *= crossing_enhancement
        
        self.energy_density_field = energy_density
        
        logger.info(f"Energy distribution calculated: peak {np.max(energy_density):.2e} J/m³")
        
        return energy_density
    
    def determine_helicity(self) -> HelicityType:
        """
        Determine left/right helicity at crossing point.
        
        Based on the geometric orientation of the Möbius twist.
        In James's theory: left helicity = antimatter, right helicity = matter.
        
        Returns:
            HelicityType indicating left (-1) or right (+1) helicity
        """
        if self.energy_config is None:
            raise ValueError("Energy configuration required for helicity determination")
        
        # Calculate crossing point geometry
        crossing_point = self._calculate_crossing_point()
        
        # Analyze twist direction at crossing
        # This is where the Möbius strip crosses itself after π rotation
        
        # Get tangent vectors before and after crossing
        epsilon = 0.01  # Small offset for numerical derivatives
        
        # Positions slightly before and after crossing
        pos_before = self._get_position_at_parameter(2 * np.pi - epsilon)
        pos_after = self._get_position_at_parameter(2 * np.pi + epsilon)
        
        # Tangent vectors
        tangent_before = pos_before / np.linalg.norm(pos_before)
        tangent_after = pos_after / np.linalg.norm(pos_after)
        
        # Cross product gives twist direction
        cross_product = np.cross(tangent_before, tangent_after)
        
        # Z-component determines helicity
        if cross_product[2] > 0:
            self.helicity = HelicityType.RIGHT  # Right-handed = matter
        elif cross_product[2] < 0:
            self.helicity = HelicityType.LEFT   # Left-handed = antimatter
        else:
            self.helicity = HelicityType.UNDEFINED
        
        logger.info(f"Helicity determined: {self.helicity.name}")
        
        return self.helicity
    
    def _calculate_crossing_point(self) -> np.ndarray:
        """Calculate 3D position of Möbius crossing point."""
        # Crossing occurs at u = 2π in the 4π path
        crossing_pos = self._get_position_at_parameter(2 * np.pi)
        self.crossing_point = crossing_pos
        return crossing_pos
    
    def _get_position_at_parameter(self, u: float) -> np.ndarray:
        """
        Get 3D position at parameter u along Möbius path.
        
        Args:
            u: Parameter value (0 to 4π)
            
        Returns:
            3D position vector
        """
        # Use lemniscate parametrization for figure-8 centerline
        t = np.mod(u, 2 * np.pi)  # Map to centerline parameter
        
        # Lemniscate with characteristic size scaling
        a = self.characteristic_size * np.sqrt(2)
        denominator = 1 + np.sin(t)**2
        
        x = a * np.cos(t) / denominator
        y = a * np.sin(t) * np.cos(t) / denominator
        z = 0  # Base lemniscate in xy-plane
        
        return np.array([x, y, z])
    
    def initialize_pole_configuration(self) -> None:
        """Initialize magnetic and electric pole positions."""
        if self.energy_config is None:
            raise ValueError("Energy configuration required for pole initialization")
        
        # Calculate pole positions based on Möbius geometry
        # N-S poles at vertices, E+/- at centroid
        
        # Find vertices (extreme points of lemniscate)
        vertices = self._find_lemniscate_vertices()
        
        # Find centroid
        centroid = self._calculate_centroid()
        
        # Magnetic moment from energy and size
        magnetic_moment = (self.energy_config.total_captured_energy * 
                          self.characteristic_size / (2 * 3e8))  # Rough estimate
        
        # Electric moment from charge separation
        electric_moment = magnetic_moment * 3e8  # Related by c
        
        self.pole_config = PoleConfiguration(
            north_position=vertices[0],
            south_position=vertices[1], 
            east_position=centroid + np.array([self.characteristic_size/10, 0, 0]),
            west_position=centroid - np.array([self.characteristic_size/10, 0, 0]),
            magnetic_moment=magnetic_moment,
            electric_moment=electric_moment
        )
        
        logger.info(f"Pole configuration initialized: magnetic moment {magnetic_moment:.2e} A⋅m²")
    
    def _find_lemniscate_vertices(self) -> List[np.ndarray]:
        """Find the extreme vertices of the lemniscate."""
        # For lemniscate, vertices occur at t = 0 and t = π
        vertex_params = [0, np.pi]
        vertices = []
        
        for t in vertex_params:
            pos = self._get_position_at_parameter(t)
            vertices.append(pos)
        
        return vertices
    
    def _calculate_centroid(self) -> np.ndarray:
        """Calculate geometric centroid of Möbius strip."""
        # Sample positions along path and average
        u_samples = np.linspace(0, 4 * np.pi, 100)
        positions = [self._get_position_at_parameter(u) for u in u_samples]
        centroid = np.mean(positions, axis=0)
        
        return centroid
    
    def calculate_phi_field_gradient(self) -> np.ndarray:
        """
        Calculate Φ-field gradient created by captured energy.
        
        Following James's gravity theory: ∇²Φ = 4πG(u-u₀)/c²
        where u is energy density and u₀ is CMB background.
        
        Returns:
            Φ-field strength at characteristic distance
        """
        if self.energy_config is None:
            raise ValueError("Energy configuration required for field calculation")
        
        # Gravitational constant and speed of light
        G = 6.674e-11  # m³/kg⋅s²
        c = 2.998e8    # m/s
        
        # Excess energy density above CMB background
        excess_density = self.energy_config.peak_energy_density - self.CMB_ENERGY_DENSITY
        
        # Φ-field strength at characteristic distance
        # Simplified as point source: Φ ≈ -GM/r where M = total_energy/c²
        equivalent_mass = self.energy_config.total_captured_energy / (c**2)
        phi_strength = -G * equivalent_mass / self.characteristic_size
        
        self.phi_field_strength = phi_strength
        
        # Local time dilation factor α = √(1 + 2Φ/c²)
        self.local_time_dilation = np.sqrt(1 + 2 * phi_strength / (c**2))
        
        logger.info(f"Φ-field calculated: strength {phi_strength:.2e} J/kg, "
                   f"time dilation factor {self.local_time_dilation:.6f}")
        
        return phi_strength
    
    def calculate_stability_metrics(self) -> Dict[str, float]:
        """
        Calculate stability metrics for the Möbius configuration.
        
        Returns:
            Dictionary of stability metrics
        """
        if self.energy_config is None:
            raise ValueError("Energy configuration required for stability calculation")
        
        # Energy balance: captured vs binding energy
        energy_surplus = (self.energy_config.total_captured_energy - 
                         self.energy_config.binding_energy)
        
        # Stability index (0 = unstable, 1 = perfectly stable)
        if self.energy_config.binding_energy > 0:
            stability_index = max(0.0, min(1.0, energy_surplus / self.energy_config.binding_energy))
        else:
            stability_index = 0.0
        
        # Decay rate (how fast configuration would dissolve)
        if energy_surplus > 0:
            decay_rate = 0.0  # Stable configuration
        else:
            # Exponential decay with time scale related to Planck time
            planck_time = 5.39e-44  # s
            decay_rate = abs(energy_surplus) / (self.energy_config.total_captured_energy * planck_time)
        
        # Self-repair rate (ability to maintain configuration)
        repair_rate = (self.energy_config.capture_efficiency * 
                      self.CMB_ENERGY_DENSITY / self.energy_config.binding_energy)
        
        self.is_stable = stability_index > 0.5
        self.decay_rate = decay_rate
        self.self_repair_rate = repair_rate
        
        metrics = {
            'stability_index': stability_index,
            'energy_surplus': energy_surplus,
            'decay_rate': decay_rate,
            'self_repair_rate': repair_rate,
            'is_stable': self.is_stable,
            'topological_protection': 1.0  # Möbius topology provides protection
        }
        
        logger.info(f"Stability analysis: index {stability_index:.3f}, "
                   f"stable = {self.is_stable}")
        
        return metrics
    
    def get_matter_antimatter_classification(self) -> str:
        """
        Get matter/antimatter classification based on helicity.
        
        Returns:
            String classification: 'matter', 'antimatter', or 'undefined'
        """
        if self.helicity == HelicityType.RIGHT:
            return 'matter'
        elif self.helicity == HelicityType.LEFT:
            return 'antimatter'
        else:
            return 'undefined'
    
    def calculate_charge_contribution(self) -> float:
        """
        Calculate expected charge contribution from this Möbius unit.
        
        In James's theory: right helicity → +e, left helicity → -e
        
        Returns:
            Charge contribution in units of elementary charge
        """
        if self.helicity == HelicityType.RIGHT:
            return +1.0  # +e (matter)
        elif self.helicity == HelicityType.LEFT:
            return -1.0  # -e (antimatter)
        else:
            return 0.0   # No net charge
    
    def evolve_configuration(self, time_step: float) -> None:
        """
        Evolve the Möbius configuration over a time step.
        
        Args:
            time_step: Evolution time step (s)
        """
        if not self.is_stable:
            # Decay the configuration
            decay_factor = np.exp(-self.decay_rate * time_step)
            self.energy_config.total_captured_energy *= decay_factor
            
            # Recalculate dependent properties
            if self.energy_config.total_captured_energy < self.energy_config.binding_energy * 0.1:
                logger.warning("Configuration becoming critically unstable")
        
        # Self-repair from CMB absorption
        repair_energy = self.self_repair_rate * time_step
        self.energy_config.total_captured_energy += repair_energy
        
        # Update Φ-field gradient
        self.calculate_phi_field_gradient()
    
    def get_diagnostic_info(self) -> Dict[str, any]:
        """Get comprehensive diagnostic information."""
        diagnostics = {
            'characteristic_size': self.characteristic_size,
            'helicity': self.helicity.name,
            'matter_antimatter': self.get_matter_antimatter_classification(),
            'charge_contribution': self.calculate_charge_contribution(),
            'phi_field_strength': self.phi_field_strength,
            'time_dilation_factor': self.local_time_dilation,
            'is_stable': self.is_stable,
            'decay_rate': self.decay_rate,
            'self_repair_rate': self.self_repair_rate
        }
        
        if self.energy_config:
            diagnostics.update({
                'total_energy': self.energy_config.total_captured_energy,
                'binding_energy': self.energy_config.binding_energy,
                'capture_efficiency': self.energy_config.capture_efficiency,
                'peak_density': self.energy_config.peak_energy_density
            })
        
        if self.pole_config:
            diagnostics.update({
                'magnetic_moment': self.pole_config.magnetic_moment,
                'electric_moment': self.pole_config.electric_moment
            })
        
        return diagnostics

# Utility functions for geometric analysis
def create_standard_mobius(size_scale: float = 1e-15, energy_scale: float = 1e-18) -> GeometricMobius:
    """
    Create a standard Möbius configuration for testing.
    
    Args:
        size_scale: Characteristic size (m)
        energy_scale: Captured energy (J)
        
    Returns:
        Configured GeometricMobius instance
    """
    mobius = GeometricMobius(size_scale)
    mobius.initialize_energy_configuration(energy_scale)
    mobius.calculate_energy_distribution()
    mobius.determine_helicity()
    mobius.initialize_pole_configuration()
    mobius.calculate_phi_field_gradient()
    mobius.calculate_stability_metrics()
    
    return mobius

def analyze_mobius_pair(mobius1: GeometricMobius, mobius2: GeometricMobius) -> Dict[str, any]:
    """
    Analyze interaction between two Möbius configurations.
    
    Args:
        mobius1, mobius2: Möbius configurations to analyze
        
    Returns:
        Dictionary of pair analysis results
    """
    # Helicity compatibility
    helicity_compatible = (mobius1.helicity == mobius2.helicity)
    
    # Energy interaction
    total_energy = (mobius1.energy_config.total_captured_energy + 
                   mobius2.energy_config.total_captured_energy)
    
    # Charge analysis
    total_charge = mobius1.calculate_charge_contribution() + mobius2.calculate_charge_contribution()
    
    # Majorana pair detection (opposite helicities)
    is_majorana_pair = (mobius1.helicity == HelicityType.RIGHT and 
                       mobius2.helicity == HelicityType.LEFT) or \
                      (mobius1.helicity == HelicityType.LEFT and 
                       mobius2.helicity == HelicityType.RIGHT)
    
    return {
        'helicity_compatible': helicity_compatible,
        'is_majorana_pair': is_majorana_pair,
        'total_energy': total_energy,
        'total_charge': total_charge,
        'binding_potential': _calculate_binding_potential(mobius1, mobius2)
    }

def _calculate_binding_potential(mobius1: GeometricMobius, mobius2: GeometricMobius) -> float:
    """Calculate potential binding energy between two Möbius configurations."""
    # Simplified calculation based on Φ-field overlap
    distance = mobius1.characteristic_size + mobius2.characteristic_size  # Approximate separation
    
    # Gravitational-like attraction from Φ-field
    G = 6.674e-11
    c = 2.998e8
    
    m1 = mobius1.energy_config.total_captured_energy / (c**2)
    m2 = mobius2.energy_config.total_captured_energy / (c**2)
    
    binding_potential = -G * m1 * m2 / distance
    
    return binding_potential