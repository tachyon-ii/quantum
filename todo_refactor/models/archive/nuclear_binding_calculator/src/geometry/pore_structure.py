"""
Pore structure analysis for nuclear binding channels.
Implements the geometric foundation of James Freeman's lepton sharing mechanism.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import cdist
from .sierpinski import SierpinskiGenerator, Triangle, Pore

@dataclass
class LeptonChannel:
    """Represents a channel for lepton sharing between nucleons"""
    pore1: Pore          # Entry pore
    pore2: Pore          # Exit pore  
    path_length: float   # Distance between pores
    cross_section: float # Effective cross-sectional area
    orientation: str     # 'orthogonal', 'parallel', 'diagonal'
    efficiency: float    # Sharing efficiency (0-1)
    channel_type: str    # 'NP', 'NN', 'PP'

class PoreStructureAnalyzer:
    """
    Analyzes pore structures in Sierpinski meshes for nuclear binding.
    
    Core insight: Pores enable orthogonal lepton sharing → angular momentum 
    conservation → γ collapse → nuclear binding.
    """
    
    def __init__(self):
        self.generator = SierpinskiGenerator()
        self.nucleon_meshes = {}  # Store meshes for different nucleons
        self.binding_channels = {}  # Store calculated binding channels
        
    def create_nucleon_mesh(self, nucleon_type: str, position: np.ndarray = None, 
                           orientation: np.ndarray = None) -> Tuple[List[Triangle], List[Pore]]:
        """
        Create a nucleon mesh at specified position and orientation.
        
        Args:
            nucleon_type: 'proton' or 'neutron'
            position: 3D position vector
            orientation: Quaternion or rotation matrix
            
        Returns:
            Tuple of (triangles, pores)
        """
        if position is None:
            position = np.array([0.0, 0.0, 0.0])
        
        # Generate Order 2 Sierpinski mesh (nucleon)
        triangles, pores = self.generator.generate_tetrahedral_sierpinski(order=2, radius=1.0)
        
        # Apply position and orientation transformations
        if orientation is not None:
            triangles, pores = self._transform_mesh(triangles, pores, position, orientation)
        else:
            triangles, pores = self._translate_mesh(triangles, pores, position)
        
        return triangles, pores
    
    def find_binding_channels(self, nucleon1_id: str, nucleon2_id: str, 
                             max_distance: float = 3.0) -> List[LeptonChannel]:
        """
        Find lepton sharing channels between two nucleons.
        
        This is the core of James's nuclear binding theory.
        
        Args:
            nucleon1_id: ID of first nucleon mesh
            nucleon2_id: ID of second nucleon mesh  
            max_distance: Maximum distance for channel formation
            
        Returns:
            List of LeptonChannel objects
        """
        if nucleon1_id not in self.nucleon_meshes or nucleon2_id not in self.nucleon_meshes:
            raise ValueError("Nucleon meshes not found")
        
        mesh1 = self.nucleon_meshes[nucleon1_id]
        mesh2 = self.nucleon_meshes[nucleon2_id]
        
        pores1 = mesh1['pores']
        pores2 = mesh2['pores']
        
        channels = []
        
        # Find pore pairs within binding distance
        for pore1 in pores1:
            for pore2 in pores2:
                distance = np.linalg.norm(pore1.center - pore2.center)
                
                if distance <= max_distance:
                    # Analyze this potential channel
                    channel = self._analyze_pore_pair(pore1, pore2, mesh1['type'], mesh2['type'])
                    if channel and channel.efficiency > 0.1:  # Minimum efficiency threshold
                        channels.append(channel)
        
        # Store channels
        pair_id = f"{nucleon1_id}_{nucleon2_id}"
        self.binding_channels[pair_id] = channels
        
        return channels
    
    def _analyze_pore_pair(self, pore1: Pore, pore2: Pore, type1: str, type2: str) -> Optional[LeptonChannel]:
        """Analyze a pair of pores for lepton sharing potential"""
        
        # Calculate basic geometric properties
        path_vector = pore2.center - pore1.center
        path_length = np.linalg.norm(path_vector)
        path_direction = path_vector / path_length if path_length > 0 else np.array([0, 0, 1])
        
        # Calculate cross-sectional area (minimum of the two pores)
        cross_section = min(pore1.area, pore2.area)
        
        # Determine orientation relative to nucleon surfaces
        orientation = self._classify_channel_orientation(pore1, pore2, path_direction)
        
        # Calculate sharing efficiency based on geometry
        efficiency = self._calculate_sharing_efficiency(pore1, pore2, orientation)
        
        # Determine channel type based on nucleon types
        channel_type = self._determine_channel_type(type1, type2)
        
        # Only create channel if efficiency is reasonable
        if efficiency > 0.05:  # 5% minimum efficiency
            return LeptonChannel(
                pore1=pore1,
                pore2=pore2,
                path_length=path_length,
                cross_section=cross_section,
                orientation=orientation,
                efficiency=efficiency,
                channel_type=channel_type
            )
        
        return None
    
    def _classify_channel_orientation(self, pore1: Pore, pore2: Pore, path_direction: np.ndarray) -> str:
        """Classify the orientation of a lepton sharing channel"""
        
        # Get normal vectors of surfaces near pores
        # For simplicity, use the vector from pore center to nucleon center
        normal1 = -pore1.center / np.linalg.norm(pore1.center)  # Point inward
        normal2 = -pore2.center / np.linalg.norm(pore2.center)
        
        # Calculate angles
        angle1 = np.arccos(np.clip(np.dot(path_direction, normal1), -1, 1))
        angle2 = np.arccos(np.clip(np.dot(path_direction, normal2), -1, 1))
        
        # Classify based on angles
        if abs(angle1 - np.pi/2) < np.pi/6 and abs(angle2 - np.pi/2) < np.pi/6:
            return 'orthogonal'  # Best for James's theory
        elif abs(angle1) < np.pi/6 or abs(angle2) < np.pi/6:
           return 'parallel'    # Less efficient
        else:
           return 'diagonal'    # Intermediate efficiency
   
    def _calculate_sharing_efficiency(self, pore1: Pore, pore2: Pore, orientation: str) -> float:
       """
       Calculate lepton sharing efficiency based on pore geometry and orientation.
       
       James's theory: Orthogonal sharing is most efficient for angular momentum conservation.
       """
       # Base efficiency from pore sizes
       size_factor = min(pore1.diameter, pore2.diameter) / max(pore1.diameter, pore2.diameter)
       
       # Orientation efficiency
       orientation_factors = {
           'orthogonal': 1.0,    # Maximum efficiency - James's optimal case
           'diagonal': 0.7,      # Moderate efficiency  
           'parallel': 0.3       # Low efficiency
       }
       orientation_factor = orientation_factors.get(orientation, 0.5)
       
       # Distance penalty (closer is better)
       path_length = np.linalg.norm(pore1.center - pore2.center)
       distance_factor = np.exp(-path_length / 2.0)  # Exponential decay
       
       # Pore alignment (how well pores line up)
       alignment_factor = self._calculate_pore_alignment(pore1, pore2)
       
       # Combined efficiency
       efficiency = size_factor * orientation_factor * distance_factor * alignment_factor
       
       return min(efficiency, 1.0)
   
    def _calculate_pore_alignment(self, pore1: Pore, pore2: Pore) -> float:
       """Calculate how well two pores are aligned for lepton transfer"""
       
       # Vector between pore centers
       connection_vector = pore2.center - pore1.center
       connection_length = np.linalg.norm(connection_vector)
       
       if connection_length < 1e-6:
           return 0.0
       
       connection_direction = connection_vector / connection_length
       
       # Check if pores face each other
       # Use surface normals pointing outward from nucleon centers
       normal1 = pore1.center / np.linalg.norm(pore1.center)
       normal2 = pore2.center / np.linalg.norm(pore2.center)
       
       # Calculate alignment scores
       alignment1 = abs(np.dot(connection_direction, normal1))
       alignment2 = abs(np.dot(-connection_direction, normal2))
       
       # Average alignment (both pores should face the connection)
       return (alignment1 + alignment2) / 2.0
   
    def _determine_channel_type(self, type1: str, type2: str) -> str:
       """Determine the type of binding channel based on nucleon types"""
       if type1 == type2:
           if type1 == 'neutron':
               return 'NN'  # Neutron-neutron
           else:
               return 'PP'  # Proton-proton
       else:
           return 'NP'      # Neutron-proton
   
    def _transform_mesh(self, triangles: List[Triangle], pores: List[Pore], 
                      position: np.ndarray, orientation: np.ndarray) -> Tuple[List[Triangle], List[Pore]]:
       """Apply position and orientation transformation to mesh"""
       # For simplicity, implement translation only
       # Full rotation implementation would require quaternion math
       return self._translate_mesh(triangles, pores, position)
   
    def _translate_mesh(self, triangles: List[Triangle], pores: List[Pore], 
                      translation: np.ndarray) -> Tuple[List[Triangle], List[Pore]]:
       """Translate mesh by given vector"""
       
       # Translate triangles
       translated_triangles = []
       for tri in triangles:
           new_tri = Triangle(
               vertices=tri.vertices + translation,
               center=tri.center + translation,
               area=tri.area,
               normal=tri.normal,  # Normal doesn't change with translation
               id=tri.id,
               level=tri.level,
               chirality=tri.chirality
           )
           translated_triangles.append(new_tri)
       
       # Translate pores
       translated_pores = []
       for pore in pores:
           new_vertices = [v + translation for v in pore.vertices]
           new_pore = Pore(
               center=pore.center + translation,
               vertices=new_vertices,
               area=pore.area,
               diameter=pore.diameter,
               connectivity=pore.connectivity,
               pore_type=pore.pore_type
           )
           translated_pores.append(new_pore)
       
       return translated_triangles, translated_pores
   
    def analyze_nuclear_configuration(self, nucleon_positions: List[Tuple[str, np.ndarray]]) -> Dict[str, any]:
       """
       Analyze a complete nuclear configuration (e.g., deuteron, tritium, helium).
       
       Args:
           nucleon_positions: List of (nucleon_type, position) tuples
           
       Returns:
           Dictionary with complete binding analysis
       """
       # Create nucleon meshes
       nucleon_ids = []
       for i, (nucleon_type, position) in enumerate(nucleon_positions):
           mesh_id = f"{nucleon_type}_{i}"
           triangles, pores = self.create_nucleon_mesh(nucleon_type, position)
           # Override the auto-generated ID with our intended ID
           self.nucleon_meshes[mesh_id] = {
               'type': nucleon_type,
               'position': position,
               'triangles': triangles,
               'pores': pores
           }
           nucleon_ids.append(mesh_id)
       
       # Find all binding channels
       all_channels = []
       channel_pairs = []
       
       for i in range(len(nucleon_ids)):
           for j in range(i + 1, len(nucleon_ids)):
               channels = self.find_binding_channels(nucleon_ids[i], nucleon_ids[j])
               all_channels.extend(channels)
               channel_pairs.append((nucleon_ids[i], nucleon_ids[j], channels))
       
       # Analyze channel statistics
       channel_stats = self._analyze_channel_statistics(all_channels)
       
       # Calculate total binding potential
       total_binding_potential = sum(ch.efficiency * ch.cross_section for ch in all_channels)
       
       # Classify nuclear configuration
       config_type = self._classify_nuclear_configuration(nucleon_positions)
       
       return {
           'configuration_type': config_type,
           'nucleon_count': len(nucleon_positions),
           'total_channels': len(all_channels),
           'channel_pairs': channel_pairs,
           'channel_statistics': channel_stats,
           'total_binding_potential': total_binding_potential,
           'nucleon_meshes': {nid: self.nucleon_meshes[nid] for nid in nucleon_ids},
           'geometric_efficiency': self._calculate_geometric_efficiency(all_channels)
       }
   
    def _analyze_channel_statistics(self, channels: List[LeptonChannel]) -> Dict[str, any]:
       """Analyze statistics of binding channels"""
       if not channels:
           return {'total': 0}
       
       # Group by channel type
       by_type = {'NN': [], 'NP': [], 'PP': []}
       for ch in channels:
           by_type[ch.channel_type].append(ch)
       
       # Calculate statistics for each type
       stats = {'total': len(channels)}
       
       for channel_type, type_channels in by_type.items():
           if type_channels:
               efficiencies = [ch.efficiency for ch in type_channels]
               cross_sections = [ch.cross_section for ch in type_channels]
               path_lengths = [ch.path_length for ch in type_channels]
               
               stats[f'{channel_type}_count'] = len(type_channels)
               stats[f'{channel_type}_avg_efficiency'] = np.mean(efficiencies)
               stats[f'{channel_type}_avg_cross_section'] = np.mean(cross_sections)
               stats[f'{channel_type}_avg_path_length'] = np.mean(path_lengths)
               stats[f'{channel_type}_total_potential'] = sum(e * c for e, c in zip(efficiencies, cross_sections))
           else:
               stats[f'{channel_type}_count'] = 0
               stats[f'{channel_type}_avg_efficiency'] = 0.0
               stats[f'{channel_type}_avg_cross_section'] = 0.0
               stats[f'{channel_type}_avg_path_length'] = 0.0
               stats[f'{channel_type}_total_potential'] = 0.0
       
       return stats
   
    def _classify_nuclear_configuration(self, nucleon_positions: List[Tuple[str, np.ndarray]]) -> str:
       """Classify the nuclear configuration"""
       neutron_count = sum(1 for nucleon_type, _ in nucleon_positions if nucleon_type == 'neutron')
       proton_count = sum(1 for nucleon_type, _ in nucleon_positions if nucleon_type == 'proton')
       total_count = len(nucleon_positions)
       
       # Standard nuclear configurations
       if total_count == 2 and neutron_count == 1 and proton_count == 1:
           return 'deuteron'
       elif total_count == 3 and neutron_count == 2 and proton_count == 1:
           return 'tritium'
       elif total_count == 3 and neutron_count == 1 and proton_count == 2:
           return 'helium3'
       elif total_count == 4 and neutron_count == 2 and proton_count == 2:
           return 'helium4'
       else:
           return f'custom_N{neutron_count}_P{proton_count}'
   
    def _calculate_geometric_efficiency(self, channels: List[LeptonChannel]) -> float:
       """Calculate overall geometric efficiency of the nuclear configuration"""
       if not channels:
           return 0.0
       
       # Weight by cross-sectional area (larger channels matter more)
       total_weighted_efficiency = sum(ch.efficiency * ch.cross_section for ch in channels)
       total_cross_section = sum(ch.cross_section for ch in channels)
       
       return total_weighted_efficiency / total_cross_section if total_cross_section > 0 else 0.0
   
    def create_standard_configurations(self) -> Dict[str, Dict]:
       """Create standard nuclear configurations for testing"""
       configurations = {}
       
       # Deuteron: N-P at optimal distance
       deuteron_positions = [
           ('neutron', np.array([-0.7, 0, 0])),
           ('proton', np.array([0.7, 0, 0]))
       ]
       configurations['deuteron'] = self.analyze_nuclear_configuration(deuteron_positions)
       
       # Reset for next configuration
       self.nucleon_meshes.clear()
       self.binding_channels.clear()
       
       # Tritium: N-P-N triangle
       angle = 2 * np.pi / 3  # 120 degrees
       radius = 0.8
       tritium_positions = [
           ('neutron', np.array([radius, 0, 0])),
           ('proton', np.array([radius * np.cos(angle), radius * np.sin(angle), 0])),
           ('neutron', np.array([radius * np.cos(2*angle), radius * np.sin(2*angle), 0]))
       ]
       configurations['tritium'] = self.analyze_nuclear_configuration(tritium_positions)
       
       # Reset for next configuration
       self.nucleon_meshes.clear()
       self.binding_channels.clear()
       
       # Helium-3: P-N-P triangle
       helium3_positions = [
           ('proton', np.array([radius, 0, 0])),
           ('neutron', np.array([radius * np.cos(angle), radius * np.sin(angle), 0])),
           ('proton', np.array([radius * np.cos(2*angle), radius * np.sin(2*angle), 0]))
       ]
       configurations['helium3'] = self.analyze_nuclear_configuration(helium3_positions)
       
       # Reset for next configuration
       self.nucleon_meshes.clear()
       self.binding_channels.clear()
       
       # Helium-4: Tetrahedral arrangement
       tetrahedron_radius = 0.9
       tetrahedron_positions = [
           ('proton', np.array([tetrahedron_radius, tetrahedron_radius, tetrahedron_radius])),
           ('neutron', np.array([tetrahedron_radius, -tetrahedron_radius, -tetrahedron_radius])),
           ('neutron', np.array([-tetrahedron_radius, tetrahedron_radius, -tetrahedron_radius])),
           ('proton', np.array([-tetrahedron_radius, -tetrahedron_radius, tetrahedron_radius]))
       ]
       # Normalize to unit sphere
       for i, (nucleon_type, pos) in enumerate(tetrahedron_positions):
           tetrahedron_positions[i] = (nucleon_type, pos / np.linalg.norm(pos) * tetrahedron_radius)
       
       configurations['helium4'] = self.analyze_nuclear_configuration(tetrahedron_positions)
       
       return configurations
   
    def export_configuration_analysis(self, configurations: Dict[str, Dict], filepath: str):
       """Export complete configuration analysis to file"""
       
       export_data = {
           'theory': 'James Freeman Pore Structure Analysis',
           'principle': 'Nuclear binding via orthogonal lepton sharing through Sierpinski pores',
           'configurations': {}
       }
       
       for config_name, config_data in configurations.items():
           # Extract key metrics for export
           export_data['configurations'][config_name] = {
               'nucleon_count': config_data['nucleon_count'],
               'total_channels': config_data['total_channels'],
               'geometric_efficiency': config_data['geometric_efficiency'],
               'total_binding_potential': config_data['total_binding_potential'],
               'channel_statistics': config_data['channel_statistics'],
               'configuration_type': config_data['configuration_type']
           }
       
       import json
       with open(filepath, 'w') as f:
           json.dump(export_data, f, indent=2, default=str)

def create_pore_visualization(analyzer: PoreStructureAnalyzer, config_name: str = 'deuteron'):
   """Create 3D visualization of pore structure and binding channels"""
   
   # Create standard configurations
   configurations = analyzer.create_standard_configurations()
   
   if config_name not in configurations:
       print(f"Configuration {config_name} not found")
       return
   
   config = configurations[config_name]
   
   # Set up 3D plot
   fig = plt.figure(figsize=(15, 10))
   
   # Main 3D view
   ax1 = fig.add_subplot(221, projection='3d')
   ax1.set_title(f'{config_name.title()} - Pore Structure')
   
   # Plot nucleon meshes
   colors = {'neutron': 'blue', 'proton': 'red'}
   
   for mesh_id, mesh_data in config['nucleon_meshes'].items():
       nucleon_type = mesh_data['type']
       triangles = mesh_data['triangles']
       pores = mesh_data['pores']
       color = colors[nucleon_type]
       
       # Plot triangle centers
       tri_centers = np.array([tri.center for tri in triangles])
       ax1.scatter(tri_centers[:, 0], tri_centers[:, 1], tri_centers[:, 2], 
                  c=color, alpha=0.3, s=10, label=f'{nucleon_type} triangles')
       
       # Plot pores
       pore_centers = np.array([pore.center for pore in pores])
       ax1.scatter(pore_centers[:, 0], pore_centers[:, 1], pore_centers[:, 2],
                  c=color, alpha=0.8, s=50, marker='o', 
                  edgecolors='black', linewidths=1, label=f'{nucleon_type} pores')
   
   # Plot binding channels
   for pair_id, channels in analyzer.binding_channels.items():
       for channel in channels:
           if channel.efficiency > 0.3:  # Only show efficient channels
               start = channel.pore1.center
               end = channel.pore2.center
               
               channel_color = {'NN': 'green', 'NP': 'orange', 'PP': 'purple'}[channel.channel_type]
               line_width = channel.efficiency * 5  # Scale with efficiency
               
               ax1.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
                       color=channel_color, linewidth=line_width, alpha=0.7,
                       label=f'{channel.channel_type} channel')
   
   ax1.set_xlabel('X (fm)')
   ax1.set_ylabel('Y (fm)')
   ax1.set_zlabel('Z (fm)')
   ax1.legend()
   
   # Channel efficiency plot
   ax2 = fig.add_subplot(222)
   ax2.set_title('Channel Efficiency Distribution')
   
   all_channels = []
   for channels in analyzer.binding_channels.values():
       all_channels.extend(channels)
   
   if all_channels:
       efficiencies = [ch.efficiency for ch in all_channels]
       channel_types = [ch.channel_type for ch in all_channels]
       
       # Group by type
       type_efficiencies = {'NN': [], 'NP': [], 'PP': []}
       for eff, ctype in zip(efficiencies, channel_types):
           type_efficiencies[ctype].append(eff)
       
       # Plot histograms
       for ctype, effs in type_efficiencies.items():
           if effs:
               ax2.hist(effs, alpha=0.7, label=f'{ctype} channels', bins=10)
       
       ax2.set_xlabel('Channel Efficiency')
       ax2.set_ylabel('Count')
       ax2.legend()
   
   # Statistics table
   ax3 = fig.add_subplot(223)
   ax3.axis('off')
   ax3.set_title('Configuration Statistics')
   
   stats = config['channel_statistics']
   stats_text = f"""
Configuration: {config['configuration_type']}
Total Nucleons: {config['nucleon_count']}
Total Channels: {config['total_channels']}
Geometric Efficiency: {config['geometric_efficiency']:.3f}

Channel Breakdown:
NN channels: {stats.get('NN_count', 0)}
NP channels: {stats.get('NP_count', 0)}  
PP channels: {stats.get('PP_count', 0)}

Average Efficiencies:
NN: {stats.get('NN_avg_efficiency', 0):.3f}
NP: {stats.get('NP_avg_efficiency', 0):.3f}
PP: {stats.get('PP_avg_efficiency', 0):.3f}
"""
   
   ax3.text(0.1, 0.9, stats_text, transform=ax3.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace')
   
   # Binding potential comparison
   ax4 = fig.add_subplot(224)
   ax4.set_title('Binding Potential by Channel Type')
   
   channel_types = ['NN', 'NP', 'PP']
   potentials = [stats.get(f'{ct}_total_potential', 0) for ct in channel_types]
   colors_bar = ['green', 'orange', 'purple']
   
   bars = ax4.bar(channel_types, potentials, color=colors_bar, alpha=0.7)
   ax4.set_ylabel('Total Binding Potential')
   
   # Add value labels on bars
   for bar, potential in zip(bars, potentials):
       if potential > 0:
           ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{potential:.3f}', ha='center', va='bottom')
   
   plt.tight_layout()
   plt.show()
   
   # Print detailed analysis
   print(f"\n{'='*60}")
   print(f"PORE STRUCTURE ANALYSIS: {config_name.upper()}")
   print(f"{'='*60}")
   print(f"James Freeman's Theory: Nuclear binding via orthogonal lepton sharing")
   print(f"Mechanism: Pore channels → lepton sharing → γ collapse → binding energy")
   print()
   
   print(f"CONFIGURATION: {config['configuration_type']}")
   print(f"Total nucleons: {config['nucleon_count']}")
   print(f"Total binding channels: {config['total_channels']}")
   print(f"Overall geometric efficiency: {config['geometric_efficiency']:.1%}")
   print()
   
   print("CHANNEL ANALYSIS:")
   for ctype in ['NN', 'NP', 'PP']:
       count = stats.get(f'{ctype}_count', 0)
       if count > 0:
           avg_eff = stats.get(f'{ctype}_avg_efficiency', 0)
           avg_cs = stats.get(f'{ctype}_avg_cross_section', 0)
           potential = stats.get(f'{ctype}_total_potential', 0)
           print(f"  {ctype} channels: {count:2d} | avg efficiency: {avg_eff:.3f} | "
                 f"avg cross-section: {avg_cs:.3f} | potential: {potential:.3f}")
   
   print(f"\nTOTAL BINDING POTENTIAL: {config['total_binding_potential']:.3f}")
   print("="*60)

# Example usage
if __name__ == "__main__":
   # Create analyzer
   analyzer = PoreStructureAnalyzer()
   
   # Analyze standard nuclear configurations
   print("Analyzing nuclear configurations with Sierpinski pore structure...")
   
   configurations = analyzer.create_standard_configurations()
   
   # Create visualizations for each configuration
   for config_name in ['deuteron', 'tritium', 'helium3', 'helium4']:
       print(f"\nAnalyzing {config_name}...")
       # Reset analyzer for each configuration
       analyzer = PoreStructureAnalyzer()
       create_pore_visualization(analyzer, config_name)
   
   # Export analysis
   analyzer.export_configuration_analysis(configurations, 'pore_structure_analysis.json')
   print("\nAnalysis exported to pore_structure_analysis.json")