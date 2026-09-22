"""
Automated Nuclear Configuration Generator

Systematically generates and evaluates multiple nuclear configurations
to find optimal arrangements for any given A (mass number) and Z (atomic number).
"""

import numpy as np
import itertools
import math
from typing import List, Dict, Tuple, Optional, Iterator
from dataclasses import dataclass

from nuclear_to_assembly.geometry.transforms import I
from nuclear_to_assembly.geometry.pose import NucleonPose, Port
from nuclear_to_assembly.assemblies.builder import Assembly, Bond
from nuclear_to_assembly.geometry.constants import D_SS, D_HH
from nuclear_to_assembly.scoring.brickwork import score_brickwork
from nuclear_to_assembly.scoring.channels import count_channels
from nuclear_to_assembly.scoring.phase_rules import score_phase

@dataclass
class ConfigurationResult:
    """Results from evaluating a nuclear configuration"""
    assembly: Assembly
    brickwork_score: Dict
    channel_count: Dict  
    phase_score: Dict
    total_score: float
    geometry_type: str

class AutomatedGenerator:
    """
    Generates nuclear configurations automatically using systematic approaches.
    
    Strategies:
    1. Linear chains
    2. Ring formations  
    3. Layered structures
    4. Cluster arrangements
    5. Random optimization
    """
    
    def __init__(self, max_attempts: int = 100):
        self.max_attempts = max_attempts
        
    def generate_all_configurations(self, A: int, Z: int, 
                                  name_prefix: str = "Auto") -> List[ConfigurationResult]:
        """
        Generate all viable configurations for nucleus with A nucleons, Z protons.
        
        Args:
            A: Mass number (total nucleons)
            Z: Atomic number (protons)
            name_prefix: Prefix for generated assembly names
            
        Returns:
            List of ConfigurationResult objects, sorted by total score
        """
        N = A - Z  # Number of neutrons
        
        if A <= 0 or Z < 0 or N < 0:
            raise ValueError(f"Invalid nucleus: A={A}, Z={Z}")
        
        print(f"Generating configurations for A={A}, Z={Z} (N={N})")
        
        configurations = []
        
        # Strategy 1: Linear arrangements
        linear_configs = self._generate_linear_configurations(A, Z, N, name_prefix)
        configurations.extend(linear_configs)
        
        # Strategy 2: Ring arrangements (for A >= 3)
        if A >= 3:
            ring_configs = self._generate_ring_configurations(A, Z, N, name_prefix)
            configurations.extend(ring_configs)
        
        # Strategy 3: Layered arrangements (for A >= 6)
        if A >= 6:
            layer_configs = self._generate_layered_configurations(A, Z, N, name_prefix)
            configurations.extend(layer_configs)
        
        # Strategy 4: Known optimal configurations (for specific nuclei)
        known_configs = self._generate_known_configurations(A, Z, N, name_prefix)
        configurations.extend(known_configs)
        
        # Strategy 5: Cluster arrangements (for A >= 8)
        if A >= 8:
            cluster_configs = self._generate_cluster_configurations(A, Z, N, name_prefix)
            configurations.extend(cluster_configs)
        
        # Evaluate all configurations
        results = []
        for config in configurations:
            try:
                result = self._evaluate_configuration(config)
                results.append(result)
            except Exception as e:
                print(f"Error evaluating {config.name}: {e}")
                continue
        
        # Sort by total score (higher is better)
        results.sort(key=lambda x: x.total_score, reverse=True)
        
        return results
    
    def _generate_linear_configurations(self, A: int, Z: int, N: int, 
                                      name_prefix: str) -> List[Assembly]:
        """Generate linear chain configurations"""
        configurations = []
        
        # Try different P/N orderings in linear chains
        nucleon_types = ["proton"] * Z + ["neutron"] * N
        
        # Generate some permutations (not all, as that would be factorial)
        max_permutations = min(20, math.factorial(A))
        permutation_count = 0
        
        for perm in itertools.permutations(nucleon_types):
            if permutation_count >= max_permutations:
                break
                
            config = self._build_linear_assembly(list(perm), f"{name_prefix}_linear_{permutation_count}")
            configurations.append(config)
            permutation_count += 1
        
        return configurations
    
    def _build_linear_assembly(self, nucleon_sequence: List[str], name: str) -> Assembly:
        """Build linear assembly from nucleon type sequence"""
        R = I()
        nucleons = {}
        bonds = []
        
        # Position nucleons along X-axis
        for i, nuc_type in enumerate(nucleon_sequence):
            nuc_id = f"{'P' if nuc_type == 'proton' else 'N'}{i+1}"
            position = np.array([i * D_SS, 0.0, 0.0], dtype=float)
            
            # Phase alternation
            phase = "A" if i % 2 == 0 else "B"
            
            # Port assignment
            ports = {}
            if i > 0:  # Not first nucleon
                ports["S-X"] = Port("S-X", phase)
            if i < len(nucleon_sequence) - 1:  # Not last nucleon
                next_phase = "B" if phase == "A" else "A"
                ports["S+X"] = Port("S+X", next_phase)
            
            nucleons[nuc_id] = NucleonPose(
                id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
            )
            
            # Add bond to next nucleon
            if i < len(nucleon_sequence) - 1:
                next_id = f"{'P' if nucleon_sequence[i+1] == 'proton' else 'N'}{i+2}"
                bonds.append(Bond(nuc_id, "S+X", next_id, "S-X"))
        
        return Assembly(name=name, nucleons=nucleons, bonds=bonds)
    
    def _generate_ring_configurations(self, A: int, Z: int, N: int, 
                                    name_prefix: str) -> List[Assembly]:
        """Generate ring configurations"""
        configurations = []
        
        # Simple ring: all nucleons in circle
        nucleon_types = ["proton"] * Z + ["neutron"] * N
        
        # Try a few different arrangements around the ring
        for arrangement_id in range(min(5, len(nucleon_types))):
            # Rotate the sequence
            rotated = nucleon_types[arrangement_id:] + nucleon_types[:arrangement_id]
            config = self._build_ring_assembly(rotated, f"{name_prefix}_ring_{arrangement_id}")
            configurations.append(config)
        
        return configurations
    
    def _build_ring_assembly(self, nucleon_sequence: List[str], name: str) -> Assembly:
        """Build ring assembly from nucleon sequence"""
        R = I()
        nucleons = {}
        bonds = []
        
        A = len(nucleon_sequence)
        ring_radius = D_SS
        
        # Position nucleons in circle
        for i, nuc_type in enumerate(nucleon_sequence):
            nuc_id = f"{'P' if nuc_type == 'proton' else 'N'}{i+1}"
            angle = 2 * math.pi * i / A
            
            x = ring_radius * math.cos(angle)
            y = ring_radius * math.sin(angle)
            position = np.array([x, y, 0.0], dtype=float)
            
            # Phase alternation
            phase = "A" if i % 2 == 0 else "B"
            
            # Each nucleon connects to neighbors
            ports = {
                "S+Y": Port("S+Y", phase),
                "S-Y": Port("S-Y", "B" if phase == "A" else "A")
            }
            
            nucleons[nuc_id] = NucleonPose(
                id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
            )
            
            # Add bond to next nucleon (wrap around)
            next_i = (i + 1) % A
            next_id = f"{'P' if nucleon_sequence[next_i] == 'proton' else 'N'}{next_i+1}"
            bonds.append(Bond(nuc_id, "S+Y", next_id, "S-Y"))
        
        return Assembly(name=name, nucleons=nucleons, bonds=bonds)
    
    def _generate_layered_configurations(self, A: int, Z: int, N: int, 
                                       name_prefix: str) -> List[Assembly]:
        """Generate layered configurations"""
        configurations = []
        
        # Try different layer arrangements
        if A >= 6:
            # 2-layer arrangement
            config = self._build_layered_assembly(A, Z, N, 2, f"{name_prefix}_2layer")
            configurations.append(config)
            
        if A >= 9:
            # 3-layer arrangement  
            config = self._build_layered_assembly(A, Z, N, 3, f"{name_prefix}_3layer")
            configurations.append(config)
        
        return configurations
    
    def _build_layered_assembly(self, A: int, Z: int, N: int, 
                              num_layers: int, name: str) -> Assembly:
        """Build layered assembly with specified number of layers"""
        R = I()
        nucleons = {}
        bonds = []
        
        # Distribute nucleons across layers
        nucleons_per_layer = A // num_layers
        extra_nucleons = A % num_layers
        
        layer_sizes = [nucleons_per_layer] * num_layers
        for i in range(extra_nucleons):
            layer_sizes[i] += 1
        
        # Distribute P/N across layers (try to balance)
        nucleon_types = ["proton"] * Z + ["neutron"] * N
        nuc_index = 0
        nucleon_counter = {"proton": 1, "neutron": 1}  # Separate counters for P and N
        
        for layer_idx, layer_size in enumerate(layer_sizes):
            z_pos = layer_idx * D_SS
            
            # Arrange nucleons in square/polygonal pattern for this layer
            for pos_idx in range(layer_size):
                if nuc_index < len(nucleon_types):
                    nuc_type = nucleon_types[nuc_index]
                    nuc_index += 1
                else:
                    nuc_type = "neutron"  # Default fallback
                
                # Use separate counters for clear IDs
                nuc_id = f"{'P' if nuc_type == 'proton' else 'N'}{nucleon_counter[nuc_type]}"
                nucleon_counter[nuc_type] += 1
                
                # Position in layer (circular arrangement)
                if layer_size == 1:
                    x, y = 0.0, 0.0
                else:
                    angle = 2 * math.pi * pos_idx / layer_size
                    radius = D_SS * 0.6  # Smaller than inter-layer distance
                    x = radius * math.cos(angle)
                    y = radius * math.sin(angle)
                
                position = np.array([x, y, z_pos], dtype=float)
                
                # Phase alternation
                phase = "A" if (layer_idx + pos_idx) % 2 == 0 else "B"
                
                # Ports for intra-layer and inter-layer connections
                ports = {}
                if layer_idx > 0:  # Not bottom layer
                    ports["S-Z"] = Port("S-Z", "B" if phase == "A" else "A")
                if layer_idx < num_layers - 1:  # Not top layer
                    ports["S+Z"] = Port("S+Z", phase)
                
                # Add some lateral connectivity within layer
                if layer_size > 1:
                    ports["S+X"] = Port("S+X", phase)
                    ports["S-X"] = Port("S-X", "B" if phase == "A" else "A")
                
                nucleons[nuc_id] = NucleonPose(
                    id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
                )
        
        # Instead of the current sparse bonding, create full connectivity
        nuc_list = list(nucleons.keys())

        # Vertical bonds between layers
        layer_starts = [0]
        current = 0
        for size in layer_sizes:
            current += size
            layer_starts.append(current)

        # Connect each nucleon to the one above it in the next layer
        for layer_idx in range(num_layers - 1):
            start_curr = layer_starts[layer_idx] 
            start_next = layer_starts[layer_idx + 1]
            
            # Ensure we don't go out of bounds
            curr_layer_size = layer_sizes[layer_idx]
            next_layer_size = layer_sizes[layer_idx + 1]

            for i in range(curr_layer_size):
                if start_curr + i >= len(nuc_list):
                    break  # Safety check
                    
                curr_nuc = nuc_list[start_curr + i]
                
                # Map current nucleon to next layer nucleon with bounds checking
                next_index = start_next + (i % next_layer_size)
                if next_index >= len(nuc_list):
                    # If we can't find a direct mapping, connect to first nucleon in next layer
                    next_index = start_next
                    
                if next_index < len(nuc_list):
                    next_nuc = nuc_list[next_index]
                    bonds.append(Bond(curr_nuc, "S+Z", next_nuc, "S-Z"))
                else:
                    # Skip this bond if we can't find a valid target
                    continue
        
        return Assembly(name=name, nucleons=nucleons, bonds=bonds)
    
    def _generate_known_configurations(self, A: int, Z: int, N: int, 
                                     name_prefix: str) -> List[Assembly]:
        """Generate known optimal configurations for specific nuclei"""
        configurations = []
        
        # Li-7 (A=7, Z=3): Use our optimized configurations
        if A == 7 and Z == 3:
            try:
                from nuclear_to_assembly.assemblies.li7 import (
                    build_li7_linear, build_li7_compact, build_li7_ring
                )
                
                # Add all Li-7 variants with proper naming
                li7_linear = build_li7_linear(f"{name_prefix}_li7_linear")
                li7_compact = build_li7_compact(f"{name_prefix}_li7_compact") 
                li7_ring = build_li7_ring(f"{name_prefix}_li7_ring")
                
                configurations.extend([li7_linear, li7_compact, li7_ring])
            except ImportError as e:
                print(f"Could not import Li-7 configurations: {e}")
        
        # H-3 (A=3, Z=1): Use optimized configurations
        elif A == 3 and Z == 1:
            try:
                from nuclear_to_assembly.assemblies.h3 import (
                    build_h3_ss_orth, build_h3_ss_linear
                )
                
                h3_orth = build_h3_ss_orth(f"{name_prefix}_h3_orth")
                h3_linear = build_h3_ss_linear(f"{name_prefix}_h3_linear")
                
                configurations.extend([h3_orth, h3_linear])
            except ImportError as e:
                print(f"Could not import H-3 configurations: {e}")
        
        # He-3 (A=3, Z=2): Use optimized configurations  
        elif A == 3 and Z == 2:
            try:
                from nuclear_to_assembly.assemblies.he3 import (
                    build_he3_ss_orth, build_he3_ss_linear
                )
                
                he3_orth = build_he3_ss_orth(f"{name_prefix}_he3_orth")
                he3_linear = build_he3_ss_linear(f"{name_prefix}_he3_linear")
                
                configurations.extend([he3_orth, he3_linear])
            except ImportError as e:
                print(f"Could not import He-3 configurations: {e}")
        
        # He-4 (A=4, Z=2): Use optimized configurations
        elif A == 4 and Z == 2:
            try:
                from nuclear_to_assembly.assemblies.he4 import (
                    build_he4_cross, build_he4_ring
                )
                
                he4_cross = build_he4_cross(f"{name_prefix}_he4_cross")
                he4_ring = build_he4_ring(f"{name_prefix}_he4_ring")
                
                configurations.extend([he4_cross, he4_ring])
            except ImportError as e:
                print(f"Could not import He-4 configurations: {e}")
        
        # D-2 (A=2, Z=1): Use optimized configuration
        elif A == 2 and Z == 1:
            try:
                from nuclear_to_assembly.assemblies.d2 import build_d2_ss
                
                d2 = build_d2_ss(f"{name_prefix}_d2")
                configurations.append(d2)
            except ImportError as e:
                print(f"Could not import D-2 configuration: {e}")
        
        return configurations
    
    def _generate_cluster_configurations(self, A: int, Z: int, N: int, 
                                       name_prefix: str) -> List[Assembly]:
        """Generate cluster-based configurations"""
        configurations = []
        
        # Alpha particle clusters (He-4 units)
        if A >= 8 and A % 4 == 0:  # Multiple of 4
            config = self._build_alpha_cluster_assembly(A, Z, N, f"{name_prefix}_alpha")
            configurations.append(config)
        
        return configurations
    
    def _build_alpha_cluster_assembly(self, A: int, Z: int, N: int, name: str) -> Assembly:
        """Build assembly from alpha particle clusters"""
        R = I()
        nucleons = {}
        bonds = []
        
        num_clusters = A // 4
        cluster_distance = D_SS * 1.5
        
        # Arrange clusters in circle
        for cluster_idx in range(num_clusters):
            angle = 2 * math.pi * cluster_idx / num_clusters
            center_x = cluster_distance * math.cos(angle)
            center_y = cluster_distance * math.sin(angle)
            cluster_center = np.array([center_x, center_y, 0.0], dtype=float)
            
            # Each cluster: 2P + 2N in square formation
            cluster_offset = D_SS * 0.4
            cluster_positions = [
                cluster_center + np.array([cluster_offset, cluster_offset, 0], dtype=float),
                cluster_center + np.array([-cluster_offset, cluster_offset, 0], dtype=float),
                cluster_center + np.array([-cluster_offset, -cluster_offset, 0], dtype=float),
                cluster_center + np.array([cluster_offset, -cluster_offset, 0], dtype=float)
            ]
            
            cluster_types = ["proton", "neutron", "proton", "neutron"]
            
            for pos_idx, (nuc_type, position) in enumerate(zip(cluster_types, cluster_positions)):
                nuc_id = f"{'P' if nuc_type == 'proton' else 'N'}{cluster_idx*4 + pos_idx + 1}"
                phase = "A" if (cluster_idx + pos_idx) % 2 == 0 else "B"
                
                # Basic port assignment for cluster connectivity
                ports = {"S+X": Port("S+X", phase), "S-Y": Port("S-Y", "B" if phase == "A" else "A")}
                
                nucleons[nuc_id] = NucleonPose(
                    id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
                )
        
        # Add some bonds (simplified)
        nuc_list = list(nucleons.keys())
        for i in range(0, len(nuc_list)-1, 2):
            if i+1 < len(nuc_list):
                bonds.append(Bond(nuc_list[i], "S+X", nuc_list[i+1], "S-Y"))
        
        return Assembly(name=name, nucleons=nucleons, bonds=bonds)
    
    def _evaluate_configuration(self, assembly: Assembly) -> ConfigurationResult:
        """Evaluate a configuration and assign total score"""
        
        # Get individual scores
        brickwork = score_brickwork(assembly)
        channels = count_channels(assembly) 
        phase = score_phase(assembly)
        
        # Calculate total score (higher is better)
        total_score = 0.0
        
        # Favor configurations with more orthogonal links
        total_score += brickwork["orthogonal_links"] * 10
        
        # Penalize shear and curvature
        total_score -= brickwork["shear_penalty"] * 5
        total_score -= brickwork["curvature_penalty"] * 3
        
        # Favor NP bonds over PP/NN bonds
        total_score += channels["NP"] * 20
        total_score -= channels["PP"] * 10  
        total_score -= channels["NN"] * 10
        
        # Penalize phase violations
        total_score -= phase["bad_phase_bonds"] * 20 #changed from 50 to 20
        
        # Determine geometry type from assembly name
        geometry_type = "unknown"
        if "linear" in assembly.name.lower():
            geometry_type = "linear"
        elif "ring" in assembly.name.lower():
            geometry_type = "ring"  
        elif "layer" in assembly.name.lower():
            geometry_type = "layered"
        elif "alpha" in assembly.name.lower():
            geometry_type = "cluster"
        
        return ConfigurationResult(
            assembly=assembly,
            brickwork_score=brickwork,
            channel_count=channels,
            phase_score=phase, 
            total_score=total_score,
            geometry_type=geometry_type
        )
    # add distance checking:
    def _validate_bond_distance(self, pos1, pos2, bond_type):
        """Ensure bond distance matches D_SS or D_HH"""
        distance = np.linalg.norm(pos2 - pos1)

        if bond_type == "S-S":
            return abs(distance - D_SS) < 0.001
        elif bond_type == "H-H":  
            return abs(distance - D_HH) < 0.001
        return False

    def find_best_configuration(self, A: int, Z: int) -> Optional[ConfigurationResult]:
        """Find the single best configuration for given nucleus"""
        results = self.generate_all_configurations(A, Z)
        
        if not results:
            return None
            
        best = results[0]  # Already sorted by score
        
        print(f"Best configuration for A={A}, Z={Z}:")
        print(f"  Name: {best.assembly.name}")
        print(f"  Geometry: {best.geometry_type}")
        print(f"  Score: {best.total_score:.2f}")
        print(f"  NP bonds: {best.channel_count['NP']}")
        print(f"  Phase violations: {best.phase_score['bad_phase_bonds']}")
        
        return best