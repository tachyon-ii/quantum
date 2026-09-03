"""
Crossed Möbius implementation for Freeman's geometric theory.

This module implements two Möbius strips crossed to form a tetrahedral configuration,
which serves as the fundamental unit for crystal assembly in James Freeman's theory.
The crossing geometry determines interaction properties and charge characteristics.
"""

import numpy as np
from typing import Tuple, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

from .geometric_mobius import GeometricMobius, HelicityType, EnergyConfiguration

logger = logging.getLogger(__name__)

class CrossingType(Enum):
    """Types of Möbius strip crossings."""
    ORTHOGONAL = "orthogonal"      # 90° crossing (tetrahedral)
    PARALLEL = "parallel"          # Parallel alignment (unstable)
    ANTIPARALLEL = "antiparallel"  # Anti-parallel alignment
    OBLIQUE = "oblique"            # General angle crossing

class BindingState(Enum):
    """Binding states between crossed Möbius strips."""
    UNBOUND = "unbound"            # No binding interaction
    WEAKLY_BOUND = "weakly_bound"  # Weak attractive interaction
    STRONGLY_BOUND = "strongly_bound"  # Strong binding (stable)
    REPULSIVE = "repulsive"        # Repulsive interaction (unstable)

@dataclass
class CrossingGeometry:
    """Geometric properties of the Möbius crossing."""
    crossing_point: np.ndarray     # 3D position where strips cross
    crossing_angle: float          # Angle between strips at crossing (radians)
    separation_distance: float     # Minimum separation between strips (m)
    overlap_volume: float          # Volume of geometric overlap (m³)
    
    # Tetrahedral properties
    tetrahedral_vertices: List[np.ndarray]  # Four vertices of tetrahedron
    tetrahedral_edge_length: float          # Characteristic edge length
    tetrahedral_volume: float               # Volume of tetrahedron

@dataclass
class InteractionEnergy:
    """Energy components of crossed Möbius interaction."""
    binding_energy: float          # Total binding energy (J)
    coulomb_energy: float         # Coulomb interaction energy (J)
    exchange_energy: float        # Exchange interaction energy (J)
    geometric_stress_energy: float # Energy from geometric deformation (J)
    topological_energy: float     # Energy from topological constraints (J)

@dataclass
class ChargeDistribution:
    """Charge distribution in crossed Möbius system."""
    net_charge: float             # Total charge in units of e
    charge_separation: float      # Separation between charge centers (m)
    dipole_moment: float         # Electric dipole moment (C⋅m)
    quadrupole_moment: float     # Electric quadrupole moment (C⋅m²)

class CrossedMobiusTetrahedron:
    """
    Two Möbius strips crossed to form tetrahedral configuration.
    
    This is the fundamental unit for crystal assembly in James Freeman's theory:
    - Two strips cross at specific angle to form tetrahedron
    - Helicity combinations determine stability and charge properties
    - Forms building block for larger crystal structures
    - Can exhibit Majorana pair behavior (matter-antimatter pairs)
    """
    
    # Physical constants
    TETRAHEDRAL_ANGLE = np.arccos(-1/3)  # ~109.47° tetrahedral angle
    FINE_STRUCTURE_CONSTANT = 7.297e-3   # α ≈ 1/137
    ELECTRON_CHARGE = 1.602e-19          # Elementary charge (C)
    
    def __init__(self, mobius1: GeometricMobius, mobius2: GeometricMobius):
        """
        Initialize crossed Möbius tetrahedral configuration.
        
        Args:
            mobius1: First Möbius strip
            mobius2: Second Möbius strip
        """
        self.mobius_strips = [mobius1, mobius2]
        self.mobius1 = mobius1
        self.mobius2 = mobius2
        
        # Crossing geometry properties
        self.crossing_geometry = None
        self.crossing_type = CrossingType.ORTHOGONAL  # Default to tetrahedral
        
        # Interaction properties
        self.interaction_energy = None
        self.binding_state = BindingState.UNBOUND
        self.charge_distribution = None
        
        # Combined system properties
        self.net_helicity = HelicityType.UNDEFINED
        self.stability_index = 0.0
        # self.is_majorana_pair = False
        
        # Tetrahedral structure
        self.tetrahedral_vertices = None
        self.tetrahedral_center = None
        
        logger.info(f"Initialized crossed Möbius with helicities: "
                   f"{mobius1.helicity.name} × {mobius2.helicity.name}")
    
    @property
    def is_majorana_pair(self) -> bool:
        """Check if this forms a Majorana pair (opposite helicities)."""
        h1, h2 = self.mobius1.helicity, self.mobius2.helicity
    
        # Majorana pair requires opposite helicities and both must be defined
        return (h1 != HelicityType.UNDEFINED and 
            h2 != HelicityType.UNDEFINED and 
            h1 != h2)

    def calculate_crossing_geometry(self) -> CrossingGeometry:
        """
        Calculate geometric properties at the crossing point.
        
        Determines how the two Möbius strips intersect and the resulting
        tetrahedral structure.
        
        Returns:
            CrossingGeometry with calculated properties
        """
        # Find intersection point of the two strips
        crossing_point = self._find_intersection_point()
        
        # Calculate crossing angle
        crossing_angle = self._calculate_crossing_angle(crossing_point)
        
        # Determine separation distance
        separation_distance = self._calculate_separation_distance()
        
        # Calculate overlap volume
        overlap_volume = self._calculate_overlap_volume()
        
        # Generate tetrahedral structure
        tetrahedral_vertices = self._generate_tetrahedral_vertices(crossing_point)
        
        # Calculate tetrahedral properties
        edge_length = self._calculate_tetrahedral_edge_length(tetrahedral_vertices)
        tetra_volume = self._calculate_tetrahedral_volume(tetrahedral_vertices)
        
        self.crossing_geometry = CrossingGeometry(
            crossing_point=crossing_point,
            crossing_angle=crossing_angle,
            separation_distance=separation_distance,
            overlap_volume=overlap_volume,
            tetrahedral_vertices=tetrahedral_vertices,
            tetrahedral_edge_length=edge_length,
            tetrahedral_volume=tetra_volume
        )
        
        # Store tetrahedral properties
        self.tetrahedral_vertices = tetrahedral_vertices
        self.tetrahedral_center = np.mean(tetrahedral_vertices, axis=0)
        
        logger.info(f"Crossing geometry calculated: angle {np.degrees(crossing_angle):.1f}°, "
                   f"edge length {edge_length:.2e} m")
        
        return self.crossing_geometry
    
    def _find_intersection_point(self) -> np.ndarray:
        """Find the 3D intersection point of the two Möbius strips."""
        # Use the position vectors from the GeometricMobius objects
        if hasattr(self.mobius1, 'position') and hasattr(self.mobius2, 'position'):
            center1 = self.mobius1.position
            center2 = self.mobius2.position
        else:
            # Fallback: use characteristic size to create positions
            size1 = self.mobius1.characteristic_size
            size2 = self.mobius2.characteristic_size
            center1 = np.array([0.0, 0.0, size1])
            center2 = np.array([size2, 0.0, 0.0])
        
        # Average of centers as crossing point
        crossing_point = (center1 + center2) / 2
        
        # Ensure it's a valid 3D point
        if crossing_point is None or len(crossing_point) != 3:
            crossing_point = np.array([0.0, 0.0, 1e-15])
        
        return crossing_point
    
    def _calculate_crossing_angle(self, crossing_point: np.ndarray) -> float:
        """Calculate angle between strips at crossing point."""
        # Get tangent vectors of both strips at crossing point
        # This is simplified - would need actual tangent calculation
        
        # For tetrahedral configuration, enforce ~109.47° angle
        if self.crossing_type == CrossingType.ORTHOGONAL:
            return self.TETRAHEDRAL_ANGLE
        else:
            # Calculate actual angle from geometry
            return np.pi / 2  # Default to 90° for now
    
    def _calculate_separation_distance(self) -> float:
        """Calculate minimum separation between the strips."""
        # Approximate as sum of characteristic sizes
        separation = (self.mobius1.characteristic_size + 
                     self.mobius2.characteristic_size) / 4
        
        return separation
    
    def _calculate_overlap_volume(self) -> float:
        """Calculate volume of geometric overlap between strips."""
        # Simplified calculation based on characteristic sizes
        size1 = self.mobius1.characteristic_size
        size2 = self.mobius2.characteristic_size
        
        # Overlap volume scales as product of cross-sectional areas
        overlap_volume = np.pi * (size1 * size2)**1.5
        
        return overlap_volume
    
    def _generate_tetrahedral_vertices(self, crossing_point: np.ndarray) -> List[np.ndarray]:
        """
        Generate the four vertices of the tetrahedral structure.
        
        The crossed Möbius configuration maps to a tetrahedron with:
        - Crossing point at center
        - Vertices at characteristic distance from center
        - Proper tetrahedral angles
        
        Args:
            crossing_point: Center point of tetrahedron
            
        Returns:
            List of four tetrahedral vertices
        """
        # Characteristic distance from center to vertices
        radius = max(self.mobius1.characteristic_size, self.mobius2.characteristic_size)
        
        # Standard tetrahedral vertices centered at origin
        # Using alternating pattern for proper tetrahedral geometry
        vertices_local = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1]
        ]) * radius / np.sqrt(3)  # Normalize to circumradius
        
        # Translate to crossing point
        vertices = [crossing_point + vertex for vertex in vertices_local]
        
        return vertices
    
    def _calculate_tetrahedral_edge_length(self, vertices: List[np.ndarray]) -> float:
        """Calculate average edge length of tetrahedron."""
        edge_lengths = []
        
        # Calculate all pairwise distances
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                edge_length = np.linalg.norm(vertices[i] - vertices[j])
                edge_lengths.append(edge_length)
        
        return np.mean(edge_lengths)
    
    def _calculate_tetrahedral_volume(self, vertices: List[np.ndarray]) -> float:
        """Calculate volume of tetrahedron."""
        # Use determinant formula for tetrahedral volume
        # V = |det(v1-v0, v2-v0, v3-v0)| / 6
        
        v0, v1, v2, v3 = vertices
        
        # Form matrix of edge vectors
        matrix = np.column_stack([v1 - v0, v2 - v0, v3 - v0])
        
        # Volume is absolute value of determinant / 6
        volume = abs(np.linalg.det(matrix)) / 6
        
        return volume
    
    def calculate_interaction_energy(self) -> InteractionEnergy:
        """
        Calculate energy components of the crossed Möbius interaction.
        
        Returns:
            InteractionEnergy with all energy components
        """
        if self.crossing_geometry is None:
            raise ValueError("Must calculate crossing geometry first")
        
        # Binding energy depends on helicity compatibility
        binding_energy = self._calculate_binding_energy()
        
        # Coulomb interaction between charged regions
        coulomb_energy = self._calculate_coulomb_interaction()
        
        # Exchange interaction (quantum mechanical)
        exchange_energy = self._calculate_exchange_interaction()
        
        # Geometric stress from deformation
        stress_energy = self._calculate_geometric_stress_energy()
        
        # Topological constraints energy
        topological_energy = self._calculate_topological_energy()
        
        self.interaction_energy = InteractionEnergy(
            binding_energy=binding_energy,
            coulomb_energy=coulomb_energy,
            exchange_energy=exchange_energy,
            geometric_stress_energy=stress_energy,
            topological_energy=topological_energy
        )
        
        # Determine binding state
        total_energy = binding_energy + coulomb_energy + exchange_energy
        
        if total_energy < -1e-20:  # Significant attractive energy
            self.binding_state = BindingState.STRONGLY_BOUND
        elif total_energy < 0:
            self.binding_state = BindingState.WEAKLY_BOUND
        elif total_energy > 1e-20:
            self.binding_state = BindingState.REPULSIVE
        else:
            self.binding_state = BindingState.UNBOUND
        
        logger.info(f"Interaction energy calculated: total {total_energy:.2e} J, "
                   f"state {self.binding_state.name}")
        
        return self.interaction_energy
    
    def _calculate_binding_energy(self) -> float:
        """Calculate binding energy between strips."""
        # Binding depends on helicity compatibility
        h1, h2 = self.mobius1.helicity, self.mobius2.helicity
        
        if h1 == h2 and h1 != HelicityType.UNDEFINED:
            # Same helicity - repulsive interaction
            binding_energy = +1e-19  # Positive = repulsive
        elif h1 != h2 and h1 != HelicityType.UNDEFINED and h2 != HelicityType.UNDEFINED:
            # Opposite helicity - attractive (Majorana pair)
            binding_energy = -5e-19  # Negative = attractive
            # self.is_majorana_pair = True
        else:
            # Undefined helicity - weak interaction
            binding_energy = -1e-20
        
        return binding_energy
    
    def _calculate_coulomb_interaction(self) -> float:
        """Calculate Coulomb interaction energy."""
        # Get charges from individual strips
        charge1 = self.mobius1.calculate_charge_contribution() * self.ELECTRON_CHARGE
        charge2 = self.mobius2.calculate_charge_contribution() * self.ELECTRON_CHARGE
        
        # Coulomb interaction: E = k * q1 * q2 / r
        k_coulomb = 8.99e9  # N⋅m²/C²
        separation = self.crossing_geometry.separation_distance
        
        if separation > 0:
            coulomb_energy = k_coulomb * charge1 * charge2 / separation
        else:
            coulomb_energy = 0.0
        
        return coulomb_energy
    
    def _calculate_exchange_interaction(self) -> float:
        """Calculate quantum mechanical exchange interaction."""
        # Simplified exchange interaction
        # Depends on overlap and helicity alignment
        
        overlap_factor = self.crossing_geometry.overlap_volume
        
        # Exchange coupling strength
        J_exchange = 1e-21  # J (simplified)
        
        # Exchange energy depends on helicity correlation
        h1, h2 = self.mobius1.helicity, self.mobius2.helicity
        
        if h1 == h2:
            # Parallel helicities - ferromagnetic coupling
            exchange_energy = -J_exchange * overlap_factor
        else:
            # Antiparallel helicities - antiferromagnetic coupling
            exchange_energy = +J_exchange * overlap_factor
        
        return exchange_energy
    
    def _calculate_geometric_stress_energy(self) -> float:
        """Calculate energy from geometric deformation."""
        # Energy cost of deforming strips to achieve crossing
        
        # Stress energy scales with deformation and elastic modulus
        deformation_energy = 1e-21  # J (simplified)
        
        # Depends on how much strips need to bend
        angle_deviation = abs(self.crossing_geometry.crossing_angle - self.TETRAHEDRAL_ANGLE)
        stress_factor = (angle_deviation / self.TETRAHEDRAL_ANGLE)**2
        
        stress_energy = deformation_energy * stress_factor
        
        return stress_energy
    
    def _calculate_topological_energy(self) -> float:
        """Calculate energy from topological constraints."""
        # Energy associated with topological linking of strips
        
        # Linking energy depends on how strips are intertwined
        linking_energy = 2e-21  # J (base topological energy)
        
        # Bonus for stable tetrahedral configuration
        if abs(self.crossing_geometry.crossing_angle - self.TETRAHEDRAL_ANGLE) < 0.1:
            linking_energy *= 0.8  # 20% energy reduction for optimal geometry
        
        return linking_energy
    
    def determine_tetrahedral_structure(self) -> Dict[str, any]:
        """
        Map crossed strips to tetrahedral vertex arrangement.
        
        Returns:
            Dictionary describing tetrahedral structure
        """
        if self.crossing_geometry is None:
            raise ValueError("Must calculate crossing geometry first")
        
        # Analyze tetrahedral properties
        vertices = self.crossing_geometry.tetrahedral_vertices
        edge_length = self.crossing_geometry.tetrahedral_edge_length
        volume = self.crossing_geometry.tetrahedral_volume
        
        # Calculate angles between edges
        angles = self._calculate_tetrahedral_angles(vertices)
        
        # Determine symmetry properties
        symmetry_quality = self._assess_tetrahedral_symmetry(vertices)
        
        structure_info = {
            'vertices': vertices,
            'center': self.tetrahedral_center,
            'edge_length': edge_length,
            'volume': volume,
            'angles': angles,
            'symmetry_quality': symmetry_quality,
            'is_regular_tetrahedron': symmetry_quality > 0.9,
            'characteristic_size': edge_length,
            'packing_efficiency': self._calculate_packing_efficiency()
        }
        
        logger.info(f"Tetrahedral structure: edge {edge_length:.2e} m, "
                   f"symmetry quality {symmetry_quality:.3f}")
        
        return structure_info
    
    def _calculate_tetrahedral_angles(self, vertices: List[np.ndarray]) -> List[float]:
        """Calculate angles in tetrahedral structure."""
        angles = []
        
        # Calculate angles at each vertex
        for i in range(len(vertices)):
            vertex = vertices[i]
            # Get other three vertices
            others = [vertices[j] for j in range(len(vertices)) if j != i]
            
            # Calculate angles between edges from this vertex
            for j in range(len(others)):
                for k in range(j + 1, len(others)):
                    vec1 = others[j] - vertex
                    vec2 = others[k] - vertex
                    
                    # Angle between vectors
                    cos_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
                    cos_angle = np.clip(cos_angle, -1, 1)  # Handle numerical errors
                    angle = np.arccos(cos_angle)
                    angles.append(angle)
        
        return angles
    
    def _assess_tetrahedral_symmetry(self, vertices: List[np.ndarray]) -> float:
        """Assess how close the structure is to a regular tetrahedron."""
        # Calculate all edge lengths
        edge_lengths = []
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                length = np.linalg.norm(vertices[i] - vertices[j])
                edge_lengths.append(length)
        
        # Regular tetrahedron has all edges equal
        mean_edge = np.mean(edge_lengths)
        edge_std = np.std(edge_lengths)
        
        # Symmetry quality: 1 = perfect, 0 = very asymmetric
        if mean_edge > 0:
            symmetry_quality = 1 - (edge_std / mean_edge)
        else:
            symmetry_quality = 0
        
        return max(0, symmetry_quality)
    
    def _calculate_packing_efficiency(self) -> float:
        """Calculate how efficiently the crossed strips fill tetrahedral space."""
        if self.crossing_geometry is None:
            return 0.0
        
        # Volume occupied by strips
        strip1_volume = self.mobius1.characteristic_size**3
        strip2_volume = self.mobius2.characteristic_size**3
        total_strip_volume = strip1_volume + strip2_volume
        
        # Tetrahedral volume
        tetra_volume = self.crossing_geometry.tetrahedral_volume
        
        # Packing efficiency
        if tetra_volume > 0:
            efficiency = min(1.0, total_strip_volume / tetra_volume)
        else:
            efficiency = 0.0
        
        return efficiency
    
    def analyze_charge_distribution(self) -> ChargeDistribution:
        """
        Analyze charge distribution in the crossed system.
        
        Returns:
            ChargeDistribution with calculated properties
        """
        # Net charge from both strips
        charge1 = self.mobius1.calculate_charge_contribution()
        charge2 = self.mobius2.calculate_charge_contribution()
        net_charge = charge1 + charge2
        
        # Charge separation distance
        if self.crossing_geometry:
            charge_separation = self.crossing_geometry.separation_distance
        else:
            charge_separation = (self.mobius1.characteristic_size + 
                               self.mobius2.characteristic_size) / 2
        
        # Electric dipole moment
        dipole_moment = abs(charge1 - charge2) * self.ELECTRON_CHARGE * charge_separation
        
        # Quadrupole moment (simplified)
        quadrupole_moment = dipole_moment * charge_separation / 2
        
        self.charge_distribution = ChargeDistribution(
            net_charge=net_charge,
            charge_separation=charge_separation,
            dipole_moment=dipole_moment,
            quadrupole_moment=quadrupole_moment
        )
        
        logger.info(f"Charge distribution: net {net_charge:.1f}e, "
                   f"dipole {dipole_moment:.2e} C⋅m")
        
        return self.charge_distribution
    
    def predict_stability(self) -> Dict[str, any]:
        """
        Predict stability of the crossed Möbius configuration.
        
        Returns:
            Dictionary of stability predictions
        """
        if self.interaction_energy is None:
            self.calculate_interaction_energy()
        
        # Overall energy balance
        total_energy = (self.interaction_energy.binding_energy + 
                       self.interaction_energy.coulomb_energy +
                       self.interaction_energy.exchange_energy +
                       self.interaction_energy.geometric_stress_energy +
                       self.interaction_energy.topological_energy)
        
        # Stability metrics
        is_stable = total_energy < 0  # Negative energy = bound state
        
        # Stability index (0-1 scale)
        if total_energy < 0:
            self.stability_index = min(1.0, abs(total_energy) / 1e-19)
        else:
            self.stability_index = 0.0
        
        # Predicted lifetime
        if is_stable:
            lifetime = float('inf')  # Stable configuration
        else:
            # Exponential decay with energy-dependent rate
            planck_time = 5.39e-44  # s
            lifetime = planck_time * np.exp(-total_energy / 1e-20)
        
        stability_analysis = {
            'is_stable': is_stable,
            'stability_index': self.stability_index,
            'total_binding_energy': total_energy,
            'binding_state': self.binding_state.name,
            'predicted_lifetime': lifetime,
            'is_majorana_pair': self.is_majorana_pair,
            'dominant_interaction': self._identify_dominant_interaction(),
            'formation_probability': self._calculate_formation_probability()
        }
        
        logger.info(f"Stability prediction: {'stable' if is_stable else 'unstable'}, "
                   f"index {self.stability_index:.3f}")
        
        return stability_analysis
    
    def _identify_dominant_interaction(self) -> str:
        """Identify which interaction dominates the binding."""
        if self.interaction_energy is None:
            return "unknown"
        
        energies = {
            'binding': abs(self.interaction_energy.binding_energy),
            'coulomb': abs(self.interaction_energy.coulomb_energy),
            'exchange': abs(self.interaction_energy.exchange_energy),
            'stress': abs(self.interaction_energy.geometric_stress_energy),
            'topological': abs(self.interaction_energy.topological_energy)
        }
        
        # Find maximum energy component
        dominant = max(energies.items(), key=lambda x: x[1])
        
        return dominant[0]
    
    def _calculate_formation_probability(self) -> float:
        """Calculate probability of forming this crossed configuration."""
        # Simplified statistical mechanics calculation
        
        if self.interaction_energy is None:
            return 0.0
        
        # Boltzmann factor
        kB = 1.381e-23  # J/K
        T = 300  # Room temperature (K)
        
        total_energy = (self.interaction_energy.binding_energy + 
                       self.interaction_energy.coulomb_energy)
        
        # Formation probability ∝ exp(-E/kBT)
        if total_energy < 0:
            formation_prob = min(1.0, np.exp(-abs(total_energy) / (kB * T)))
        else:
            formation_prob = np.exp(-total_energy / (kB * T))
        
        return formation_prob
    
    def get_diagnostic_summary(self) -> Dict[str, any]:
        """Get comprehensive diagnostic information."""
        summary = {
            'mobius1_helicity': self.mobius1.helicity.name,
            'mobius2_helicity': self.mobius2.helicity.name,
            'net_helicity': self.net_helicity.name,
            'is_majorana_pair': self.is_majorana_pair,
            'crossing_type': self.crossing_type.name,
            'binding_state': self.binding_state.name,
            'stability_index': self.stability_index
        }
        
        if self.crossing_geometry:
            summary.update({
                'crossing_angle_deg': np.degrees(self.crossing_geometry.crossing_angle),
                'tetrahedral_edge_length': self.crossing_geometry.tetrahedral_edge_length,
                'tetrahedral_volume': self.crossing_geometry.tetrahedral_volume
            })
        
        if self.interaction_energy:
            summary.update({
                'total_binding_energy': (self.interaction_energy.binding_energy + 
                                       self.interaction_energy.coulomb_energy),
                'dominant_interaction': self._identify_dominant_interaction()
            })
        
        if self.charge_distribution:
            summary.update({
                'net_charge': self.charge_distribution.net_charge,
                'dipole_moment': self.charge_distribution.dipole_moment
            })
        
        return summary

# Utility functions for crossed Möbius analysis
def create_standard_crossed_tetrahedral(helicity1: HelicityType = HelicityType.RIGHT,
                                      helicity2: HelicityType = HelicityType.LEFT,
                                      size_scale: float = 1e-15) -> CrossedMobiusTetrahedron:
    """
    Create standard crossed Möbius tetrahedral configuration.
    
    Args:
        helicity1: Helicity of first strip
        helicity2: Helicity of second strip  
        size_scale: Characteristic size scale
        
    Returns:
        Configured CrossedMobiusTetrahedron
    """
    from .geometric_mobius import create_standard_mobius
    
    # Create two Möbius strips with specified helicities
    mobius1 = create_standard_mobius(size_scale)
    mobius2 = create_standard_mobius(size_scale)
    
    # Set helicities
    mobius1.helicity = helicity1
    mobius2.helicity = helicity2
    
    # Create crossed configuration
    crossed = CrossedMobiusTetrahedron(mobius1, mobius2)
    
    # Calculate all properties
    crossed.calculate_crossing_geometry()
    crossed.calculate_interaction_energy()
    crossed.analyze_charge_distribution()
    
    return crossed