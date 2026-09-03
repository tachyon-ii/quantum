"""
Crossed Möbius Tetrahedral Visualizer for Freeman's Geometric Theory.

This module provides comprehensive visualization and analysis for crossed
Möbius strips in tetrahedral configuration, the next step in Dr. Freeman's
visualization requirements.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Import from existing modules
from .geometric_mobius import GeometricMobius, create_standard_mobius, HelicityType
from .crossed_mobius import CrossedMobiusTetrahedron, create_standard_crossed_tetrahedral

class CrossedMobiusVisualizer:
    """
    Comprehensive visualization and analysis for crossed Möbius strips.
    
    This class addresses Dr. Freeman's requirement for crossed Möbius
    analysis, showing tetrahedral configurations and interaction properties.
    """
    
    def __init__(self, crossed_unit: CrossedMobiusTetrahedron):
        """
        Initialize visualizer with a crossed Möbius tetrahedral unit.
        
        Args:
            crossed_unit: CrossedMobiusTetrahedron instance to analyze
        """
        self.crossed_unit = crossed_unit
        self.analysis_data = None
        self.output_dir = Path("test_results")
        self.output_dir.mkdir(exist_ok=True)
        
    def analyze_tetrahedral_geometry(self, num_points: int = 100) -> Dict:
        """
        Analyze the tetrahedral geometry of crossed Möbius strips.
        
        Args:
            num_points: Number of analysis points
            
        Returns:
            Dictionary containing tetrahedral analysis data
        """
        # Ensure geometry is calculated
        if self.crossed_unit.crossing_geometry is None:
            self.crossed_unit.calculate_crossing_geometry()
        
        # Ensure interaction energy is calculated
        if self.crossed_unit.interaction_energy is None:
            self.crossed_unit.calculate_interaction_energy()
        
        # Ensure charge distribution is calculated
        if self.crossed_unit.charge_distribution is None:
            self.crossed_unit.analyze_charge_distribution()
        
        data = {
            'crossing_point': self.crossed_unit.crossing_geometry.crossing_point,
            'crossing_angle': self.crossed_unit.crossing_geometry.crossing_angle,
            'tetrahedral_vertices': self.crossed_unit.crossing_geometry.tetrahedral_vertices,
            'tetrahedral_edge_length': self.crossed_unit.crossing_geometry.tetrahedral_edge_length,
            'tetrahedral_volume': self.crossed_unit.crossing_geometry.tetrahedral_volume,
            'is_majorana_pair': self.crossed_unit.is_majorana_pair,
            'binding_energy': self.crossed_unit.interaction_energy.binding_energy,
            'coulomb_energy': self.crossed_unit.interaction_energy.coulomb_energy,
            'exchange_energy': self.crossed_unit.interaction_energy.exchange_energy,
            'total_energy': (self.crossed_unit.interaction_energy.binding_energy + 
                           self.crossed_unit.interaction_energy.coulomb_energy + 
                           self.crossed_unit.interaction_energy.exchange_energy),
            'net_charge': self.crossed_unit.charge_distribution.net_charge,
            'dipole_moment': self.crossed_unit.charge_distribution.dipole_moment,
            'helicity1': self.crossed_unit.mobius1.helicity,
            'helicity2': self.crossed_unit.mobius2.helicity
        }
        
        # Analyze field interactions at multiple points
        field_analysis = self._analyze_field_interactions(num_points)
        data.update(field_analysis)
        
        # Calculate stability metrics
        total_energy = (self.crossed_unit.interaction_energy.binding_energy + 
                       self.crossed_unit.interaction_energy.coulomb_energy + 
                       self.crossed_unit.interaction_energy.exchange_energy)
        
        # Calculate stability metrics inline to avoid parameter issues
        if total_energy < 0:
            stability_index = min(1.0, abs(total_energy) / 1e-19)
        else:
            stability_index = 0.0
        
        # Geometric stability based on tetrahedral quality
        edge_length = self.crossed_unit.crossing_geometry.tetrahedral_edge_length
        vertices = self.crossed_unit.crossing_geometry.tetrahedral_vertices
        
        # Calculate all edge lengths for symmetry assessment
        edge_lengths = []
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                length = np.linalg.norm(vertices[i] - vertices[j])
                edge_lengths.append(length)
        
        geometric_stability = 1.0 - (np.std(edge_lengths) / np.mean(edge_lengths))
        
        stability_data = {
            'stability_index': stability_index,
            'geometric_stability': geometric_stability,
            'is_stable': total_energy < 0 and geometric_stability > 0.8
        }
        data.update(stability_data)
        
        self.analysis_data = data
        return data
    
    def _analyze_field_interactions(self, num_points: int) -> Dict:
        """Analyze electromagnetic field interactions between strips."""
        # Sample points around the tetrahedral structure
        vertices = self.crossed_unit.crossing_geometry.tetrahedral_vertices
        center = np.mean(vertices, axis=0)
        
        # Create sampling points around the tetrahedron
        sampling_points = []
        field_strengths = []
        energy_densities = []
        
        for i in range(num_points):
            # Sample points in spherical coordinates around center
            theta = np.random.uniform(0, 2*np.pi)
            phi = np.random.uniform(0, np.pi)
            radius = self.crossed_unit.crossing_geometry.tetrahedral_edge_length * 0.5
            
            x = center[0] + radius * np.sin(phi) * np.cos(theta)
            y = center[1] + radius * np.sin(phi) * np.sin(theta)
            z = center[2] + radius * np.cos(phi)
            
            point = np.array([x, y, z])
            sampling_points.append(point)
            
            # Calculate field strength at this point
            # Distance-based field strength (simplified)
            dist1 = np.linalg.norm(point - vertices[0])
            dist2 = np.linalg.norm(point - vertices[1])
            
            field_strength = 1.0 / (dist1**2 + 1e-10) + 1.0 / (dist2**2 + 1e-10)
            field_strengths.append(field_strength)
            
            # Energy density (simplified)
            energy_density = field_strength * 1e-20
            energy_densities.append(energy_density)
        
        return {
            'sampling_points': sampling_points,
            'field_strengths': field_strengths,
            'energy_densities': energy_densities,
            'avg_field_strength': np.mean(field_strengths),
            'max_field_strength': np.max(field_strengths),
            'field_variation': np.std(field_strengths)
        }
    
    def _calculate_stability_metrics(self) -> Dict:
        """Calculate stability metrics for the crossed configuration."""
        total_energy = self.analysis_data['total_energy']
        
        # Stability index based on energy
        if total_energy < 0:
            stability_index = min(1.0, abs(total_energy) / 1e-19)
        else:
            stability_index = 0.0
        
        # Geometric stability based on tetrahedral quality
        edge_length = self.crossed_unit.crossing_geometry.tetrahedral_edge_length
        vertices = self.crossed_unit.crossing_geometry.tetrahedral_vertices
        
        # Calculate all edge lengths for symmetry assessment
        edge_lengths = []
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                length = np.linalg.norm(vertices[i] - vertices[j])
                edge_lengths.append(length)
        
        geometric_stability = 1.0 - (np.std(edge_lengths) / np.mean(edge_lengths))
        
        return {
            'stability_index': stability_index,
            'geometric_stability': geometric_stability,
            'is_stable': total_energy < 0 and geometric_stability > 0.8
        }
    
    def plot_tetrahedral_analysis(self, save_plots: bool = True) -> None:
        """
        Create comprehensive visualization of crossed Möbius tetrahedron.
        
        Args:
            save_plots: Whether to save plots to files
        """
        if self.analysis_data is None:
            self.analyze_tetrahedral_geometry()
        
        # Create large figure with multiple subplots
        fig = plt.figure(figsize=(20, 15))
        fig.suptitle(f'Crossed Möbius Tetrahedral Analysis\n'
                    f'Helicities: {self.analysis_data["helicity1"].name} × {self.analysis_data["helicity2"].name}\n'
                    f'Majorana Pair: {self.analysis_data["is_majorana_pair"]}', 
                     fontsize=16, fontweight='bold')
        
        # 1. 3D Tetrahedral structure
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        vertices = self.analysis_data['tetrahedral_vertices']
        crossing_point = self.analysis_data['crossing_point']
        
        # Plot tetrahedral edges
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                v1, v2 = vertices[i], vertices[j]
                ax1.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], 'b-', linewidth=2, alpha=0.7)
        
        # Plot vertices
        for i, vertex in enumerate(vertices):
            ax1.scatter(vertex[0], vertex[1], vertex[2], s=100, c='red', label=f'Vertex {i+1}' if i < 4 else '')
        
        # Plot crossing point
        ax1.scatter(crossing_point[0], crossing_point[1], crossing_point[2], 
                   s=200, c='gold', marker='*', label='Crossing Point')
        
        ax1.set_title('Tetrahedral Structure')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.legend()
        
        # 2. Energy analysis
        ax2 = fig.add_subplot(2, 3, 2)
        energies = [
            self.analysis_data['binding_energy'],
            self.analysis_data['coulomb_energy'], 
            self.analysis_data['exchange_energy']
        ]
        energy_labels = ['Binding', 'Coulomb', 'Exchange']
        colors = ['blue', 'red', 'green']
        
        bars = ax2.bar(energy_labels, energies, color=colors, alpha=0.7)
        ax2.set_title('Energy Components')
        ax2.set_ylabel('Energy (J)')
        ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, energy in zip(bars, energies):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{energy:.2e}', ha='center', va='bottom' if height >= 0 else 'top')
        
        # 3. Field strength distribution
        ax3 = fig.add_subplot(2, 3, 3)
        field_strengths = self.analysis_data['field_strengths']
        ax3.hist(field_strengths, bins=20, alpha=0.7, color='purple', edgecolor='black')
        ax3.axvline(self.analysis_data['avg_field_strength'], color='red', linestyle='--', 
                   label=f'Average: {self.analysis_data["avg_field_strength"]:.2e}')
        ax3.set_title('Field Strength Distribution')
        ax3.set_xlabel('Field Strength')
        ax3.set_ylabel('Frequency')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Geometric properties
        ax4 = fig.add_subplot(2, 3, 4)
        geometric_props = {
            'Edge Length': self.analysis_data['tetrahedral_edge_length'],
            'Volume': self.analysis_data['tetrahedral_volume'],
            'Crossing Angle': np.degrees(self.analysis_data['crossing_angle'])
        }
        
        prop_names = list(geometric_props.keys())
        prop_values = list(geometric_props.values())
        
        bars = ax4.bar(prop_names, prop_values, color=['orange', 'cyan', 'lime'], alpha=0.7)
        ax4.set_title('Geometric Properties')
        ax4.set_ylabel('Value')
        ax4.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, value in zip(bars, prop_values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2e}', ha='center', va='bottom', rotation=0)
        
        # 5. Stability analysis
        ax5 = fig.add_subplot(2, 3, 5)
        stability_metrics = {
            'Energy Stability': self.analysis_data['stability_index'],
            'Geometric Stability': self.analysis_data['geometric_stability']
        }
        
        metric_names = list(stability_metrics.keys())
        metric_values = list(stability_metrics.values())
        
        bars = ax5.bar(metric_names, metric_values, color=['darkblue', 'darkgreen'], alpha=0.7)
        ax5.set_title('Stability Metrics')
        ax5.set_ylabel('Stability Index (0-1)')
        ax5.set_ylim(0, 1.1)
        ax5.tick_params(axis='x', rotation=45)
        ax5.grid(True, alpha=0.3)
        
        # Add stability threshold line
        ax5.axhline(y=0.8, color='red', linestyle='--', alpha=0.7, label='Stable Threshold')
        ax5.legend()
        
        # 6. Charge and magnetic properties
        ax6 = fig.add_subplot(2, 3, 6)
        charge_props = {
            'Net Charge (e)': self.analysis_data['net_charge'],
            'Dipole Moment': self.analysis_data['dipole_moment'] * 1e30,  # Scale for visibility
            'Total Energy': self.analysis_data['total_energy'] * 1e20     # Scale for visibility
        }
        
        charge_names = list(charge_props.keys())
        charge_values = list(charge_props.values())
        
        bars = ax6.bar(charge_names, charge_values, color=['magenta', 'yellow', 'brown'], alpha=0.7)
        ax6.set_title('Electromagnetic Properties')
        ax6.set_ylabel('Scaled Values')
        ax6.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, value in zip(bars, charge_values):
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2f}', ha='center', va='bottom' if height >= 0 else 'top')
        
        plt.tight_layout()
        
        if save_plots:
            h1_name = self.analysis_data['helicity1'].name.lower()
            h2_name = self.analysis_data['helicity2'].name.lower()
            filename = f'crossed_mobius_analysis_{h1_name}_{h2_name}.png'
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Crossed Möbius analysis plot saved to {filepath}")
        
        plt.show()
    
    def plot_3d_field_visualization(self, save_plots: bool = True) -> None:
        """Create 3D visualization of electromagnetic fields."""
        if self.analysis_data is None:
            self.analyze_tetrahedral_geometry()
        
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot tetrahedral structure
        vertices = self.analysis_data['tetrahedral_vertices']
        crossing_point = self.analysis_data['crossing_point']
        
        # Plot edges
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                v1, v2 = vertices[i], vertices[j]
                ax.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]], 'k-', linewidth=3, alpha=0.8)
        
        # Plot field strength as colored points
        sampling_points = self.analysis_data['sampling_points']
        field_strengths = self.analysis_data['field_strengths']
        
        # Normalize field strengths for color mapping
        norm_fields = (np.array(field_strengths) - np.min(field_strengths)) / (np.max(field_strengths) - np.min(field_strengths))
        
        scatter = ax.scatter([p[0] for p in sampling_points],
                           [p[1] for p in sampling_points],
                           [p[2] for p in sampling_points],
                           c=norm_fields, cmap='plasma', s=50, alpha=0.6)
        
        # Plot vertices
        for vertex in vertices:
            ax.scatter(vertex[0], vertex[1], vertex[2], s=200, c='red', marker='o')
        
        # Plot crossing point
        ax.scatter(crossing_point[0], crossing_point[1], crossing_point[2], 
                  s=300, c='gold', marker='*')
        
        ax.set_title(f'3D Electromagnetic Field Visualization\n'
                    f'Helicities: {self.analysis_data["helicity1"].name} × {self.analysis_data["helicity2"].name}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=20)
        cbar.set_label('Normalized Field Strength')
        
        if save_plots:
            h1_name = self.analysis_data['helicity1'].name.lower()
            h2_name = self.analysis_data['helicity2'].name.lower()
            filename = f'crossed_mobius_3d_field_{h1_name}_{h2_name}.png'
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"3D field visualization saved to {filepath}")
        
        plt.show()
    
    def export_analysis_data(self, filename: Optional[str] = None) -> pd.DataFrame:
        """Export detailed crossed Möbius analysis data."""
        if self.analysis_data is None:
            self.analyze_tetrahedral_geometry()
        
        if filename is None:
            h1_name = self.analysis_data['helicity1'].name.lower()
            h2_name = self.analysis_data['helicity2'].name.lower()
            filename = f'crossed_mobius_detailed_{h1_name}_{h2_name}.csv'
        
        # Create comprehensive data structure
        data_rows = []
        
        # Add geometric data
        vertices = self.analysis_data['tetrahedral_vertices']
        for i, vertex in enumerate(vertices):
            row = {
                'type': 'vertex',
                'index': i,
                'x': vertex[0],
                'y': vertex[1], 
                'z': vertex[2],
                'field_strength': 0,  # Vertices have no field data
                'energy_density': 0
            }
            data_rows.append(row)
        
        # Add crossing point
        cp = self.analysis_data['crossing_point']
        data_rows.append({
            'type': 'crossing_point',
            'index': 0,
            'x': cp[0],
            'y': cp[1],
            'z': cp[2],
            'field_strength': 0,
            'energy_density': 0
        })
        
        # Add field sampling points
        for i, (point, field, energy) in enumerate(zip(
            self.analysis_data['sampling_points'],
            self.analysis_data['field_strengths'], 
            self.analysis_data['energy_densities']
        )):
            row = {
                'type': 'field_point',
                'index': i,
                'x': point[0],
                'y': point[1],
                'z': point[2],
                'field_strength': field,
                'energy_density': energy
            }
            data_rows.append(row)
        
        df = pd.DataFrame(data_rows)
        
        # Add summary information
        summary_data = {
            'tetrahedral_edge_length': self.analysis_data['tetrahedral_edge_length'],
            'tetrahedral_volume': self.analysis_data['tetrahedral_volume'],
            'crossing_angle_degrees': np.degrees(self.analysis_data['crossing_angle']),
            'is_majorana_pair': self.analysis_data['is_majorana_pair'],
            'binding_energy': self.analysis_data['binding_energy'],
            'coulomb_energy': self.analysis_data['coulomb_energy'],
            'exchange_energy': self.analysis_data['exchange_energy'],
            'total_energy': self.analysis_data['total_energy'],
            'net_charge': self.analysis_data['net_charge'],
            'dipole_moment': self.analysis_data['dipole_moment'],
            'stability_index': self.analysis_data['stability_index'],
            'geometric_stability': self.analysis_data['geometric_stability'],
            'is_stable': self.analysis_data['is_stable'],
            'avg_field_strength': self.analysis_data['avg_field_strength'],
            'helicity1': self.analysis_data['helicity1'].value,
            'helicity2': self.analysis_data['helicity2'].value
        }
        
        # Save summary separately
        summary_filename = filename.replace('.csv', '_summary.json')
        import json
        with open(self.output_dir / summary_filename, 'w') as f:
            json.dump(summary_data, f, indent=2, default=str)
        
        # Save main data
        filepath = self.output_dir / filename
        df.to_csv(filepath, index=False, float_format='%.6f')
        print(f"Crossed Möbius analysis data exported to {filepath}")
        print(f"Summary data exported to {self.output_dir / summary_filename}")
        
        return df

def analyze_crossed_mobius_complete(helicity1: HelicityType = HelicityType.RIGHT,
                                  helicity2: HelicityType = HelicityType.LEFT) -> Tuple[CrossedMobiusVisualizer, pd.DataFrame]:
    """
    Complete analysis of crossed Möbius strips in tetrahedral configuration.
    
    Args:
        helicity1: Helicity of first strip
        helicity2: Helicity of second strip
        
    Returns:
        Tuple of (visualizer, analysis_dataframe)
    """
    print(f"Analyzing crossed Möbius with {helicity1.name} × {helicity2.name} helicities...")
    
    # Create crossed tetrahedral unit
    crossed_unit = create_standard_crossed_tetrahedral(helicity1, helicity2)
    
    # Create visualizer
    visualizer = CrossedMobiusVisualizer(crossed_unit)
    
    # Perform analysis
    analysis_data = visualizer.analyze_tetrahedral_geometry(num_points=100)
    
    # Create visualizations
    visualizer.plot_tetrahedral_analysis()
    visualizer.plot_3d_field_visualization()
    
    # Export data
    analysis_df = visualizer.export_analysis_data()
    
    # Print key results
    print(f"\nCrossed Möbius Analysis Results:")
    print(f"Majorana pair: {analysis_data['is_majorana_pair']}")
    print(f"Total energy: {analysis_data['total_energy']:.2e} J")
    print(f"Net charge: {analysis_data['net_charge']:.3f} e")
    print(f"Stability index: {analysis_data['stability_index']:.3f}")
    print(f"Is stable: {analysis_data['is_stable']}")
    
    return visualizer, analysis_df

if __name__ == "__main__":
    # Run complete crossed Möbius analysis
    print("Freeman's Crossed Möbius Tetrahedral Analysis")
    print("=" * 45)
    
    # Analyze different helicity combinations
    combinations = [
        (HelicityType.RIGHT, HelicityType.LEFT),   # Majorana pair
        (HelicityType.RIGHT, HelicityType.RIGHT),  # Same helicity
        (HelicityType.LEFT, HelicityType.LEFT)     # Same helicity
    ]
    
    for h1, h2 in combinations:
        print(f"\n--- Analyzing {h1.name} × {h2.name} ---")
        viz, data = analyze_crossed_mobius_complete(h1, h2)
    
    print("\nCrossed Möbius analysis complete!")
    print("Generated visualizations and data files in test_results/")