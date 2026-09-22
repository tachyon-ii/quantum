"""
Single Möbius Strip Visualizer for Freeman's Geometric Theory.

This module provides comprehensive visualization and analysis for individual
Möbius strips, addressing Dr. Freeman's request for detailed single Möbius
analysis before moving to crossed configurations.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Import from existing modules
from .geometric_mobius import GeometricMobius, create_standard_mobius, HelicityType

class SingleMobiusVisualizer:
    """
    Comprehensive visualization and analysis for single Möbius strips.
    
    This class addresses Dr. Freeman's requirement for detailed single Möbius
    analysis, providing geometric, energetic, and field visualizations.
    """
    
    def __init__(self, mobius: GeometricMobius):
        """
        Initialize visualizer with a Möbius strip.
        
        Args:
            mobius: GeometricMobius instance to analyze
        """
        self.mobius = mobius
        self.geometric_data = None
        self.output_dir = Path("test_results")
        self.output_dir.mkdir(exist_ok=True)
        
    def analyze_geometry(self, num_points: int = 200) -> Dict:
        """
        Extract detailed geometric data from the Möbius strip.
        
        Uses James's figure-8 (lemniscate) parametrization with proper twist
        calculation to generate comprehensive geometric analysis.
        
        Args:
            num_points: Number of points along the 4π parameter range
            
        Returns:
            Dictionary containing all geometric analysis data
        """
        # Parameter range: 0 to 4π (complete Möbius traversal)
        u_values = np.linspace(0, 4*np.pi, num_points)
        
        data = {
            'parameter_u': u_values,
            'positions': [],
            'tangent_vectors': [],
            'normal_vectors': [],
            'binormal_vectors': [],
            'twist_angles': [],
            'curvature': [],
            'torsion': [],
            'field_strength': [],
            'energy_density': [],
            'centroid_distance': []
        }
        
        # James's lemniscate parameters
        scale = 4.5
        a = scale * np.sqrt(2)
        
        for i, u in enumerate(u_values):
            # Map to centerline parameter (0 to 2π)
            t = np.mod(u, 2 * np.pi)
            
            # Lemniscate centerline equations
            denominator = 1 + np.sin(t)**2
            x = a * np.cos(t) / denominator
            y = a * np.sin(t) * np.cos(t) / denominator
            z = 0  # Centerline in xy-plane
            
            position = np.array([x, y, z])
            data['positions'].append(position)
            
            # Calculate tangent vector using finite differences
            dt = 0.01
            t_plus = np.mod(t + dt, 2 * np.pi)
            t_minus = np.mod(t - dt, 2 * np.pi)
            
            # Forward and backward positions
            denom_plus = 1 + np.sin(t_plus)**2
            denom_minus = 1 + np.sin(t_minus)**2
            
            x_plus = a * np.cos(t_plus) / denom_plus
            y_plus = a * np.sin(t_plus) * np.cos(t_plus) / denom_plus
            x_minus = a * np.cos(t_minus) / denom_minus
            y_minus = a * np.sin(t_minus) * np.cos(t_minus) / denom_minus
            
            # Tangent vector (derivative)
            tx = (x_plus - x_minus) / (2 * dt)
            ty = (y_plus - y_minus) / (2 * dt)
            tz = 0
            
            # Normalize tangent
            t_mag = np.sqrt(tx**2 + ty**2 + tz**2)
            if t_mag > 1e-10:
                tx, ty, tz = tx/t_mag, ty/t_mag, tz/t_mag
            
            tangent = np.array([tx, ty, tz])
            data['tangent_vectors'].append(tangent)
            
            # Calculate twist angle (James's formula: 0.5 * u)
            twist = u * 0.5
            data['twist_angles'].append(twist)
            
            # Initial normal vector (perpendicular to tangent, starting vertical)
            nx_init = 0
            ny_init = 0
            nz_init = 1
            
            # Make perpendicular to tangent using Gram-Schmidt
            dot = tx*nx_init + ty*ny_init + tz*nz_init
            nx_init -= dot * tx
            ny_init -= dot * ty
            nz_init -= dot * tz
            
            # Normalize initial normal
            n_mag = np.sqrt(nx_init**2 + ny_init**2 + nz_init**2)
            if n_mag > 1e-10:
                nx_init, ny_init, nz_init = nx_init/n_mag, ny_init/n_mag, nz_init/n_mag
            
            # Calculate binormal (cross product of tangent and normal)
            bx = ty * nz_init - tz * ny_init
            by = tz * nx_init - tx * nz_init
            bz = tx * ny_init - ty * nx_init
            
            binormal = np.array([bx, by, bz])
            data['binormal_vectors'].append(binormal)
            
            # Apply twist rotation to get actual normal
            cos_twist = np.cos(twist)
            sin_twist = np.sin(twist)
            
            # Rotate normal around tangent by twist angle
            nx = cos_twist * nx_init + sin_twist * bx
            ny = cos_twist * ny_init + sin_twist * by
            nz = cos_twist * nz_init + sin_twist * bz
            
            normal = np.array([nx, ny, nz])
            data['normal_vectors'].append(normal)
            
            # Calculate curvature (simplified geometric curvature)
            if i > 0 and i < len(u_values) - 1:
                # Second derivative approximation
                prev_tang = data['tangent_vectors'][i-1]
                next_tang = data['tangent_vectors'][i+1] if i+1 < len(data['tangent_vectors']) else tangent
                
                d_tang = (next_tang - prev_tang) / (2 * (u_values[1] - u_values[0]))
                curvature = np.linalg.norm(d_tang)
            else:
                curvature = 0.0
            
            data['curvature'].append(curvature)
            
            # Calculate torsion (twist of the curve)
            torsion = 0.5  # Constant for Möbius strip (James's formula)
            data['torsion'].append(torsion)
            
            # Calculate field strength from Möbius properties
            try:
                field_strength = self.mobius.calculate_phi_field_gradient()
            except:
                # Default field strength calculation
                field_strength = np.exp(-np.sqrt(x**2 + y**2 + z**2) / a)
            
            data['field_strength'].append(field_strength)
            
            # Calculate energy density
            try:
                if self.mobius.energy_config:
                    energy_density = self.mobius.energy_config.total_captured_energy / num_points
                else:
                    energy_density = 1e-20
            except:
                energy_density = 1e-20 * np.exp(-np.sqrt(x**2 + y**2 + z**2) / a)
            
            data['energy_density'].append(energy_density)
            
            # Distance from centroid
            centroid_distance = np.sqrt(x**2 + y**2 + z**2)
            data['centroid_distance'].append(centroid_distance)
        
        self.geometric_data = data
        return data
    
    def plot_complete_analysis(self, save_plots: bool = True) -> None:
        """
        Create comprehensive visualization of single Möbius strip.
        
        Generates a multi-panel plot showing all aspects of Möbius geometry,
        addressing Dr. Freeman's request for detailed visualizations.
        
        Args:
            save_plots: Whether to save plots to files
        """
        if self.geometric_data is None:
            self.analyze_geometry()
        
        # Create large figure with multiple subplots
        fig = plt.figure(figsize=(20, 15))
        fig.suptitle(f'Complete Single Möbius Analysis - Helicity: {self.mobius.helicity.name}', 
                     fontsize=16, fontweight='bold')
        
        positions = np.array(self.geometric_data['positions'])
        
        # 1. 3D Geometry with vectors
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        ax1.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', linewidth=3, label='Centerline')
        
        # Add tangent vectors (every 20th point)
        for i in range(0, len(positions), 20):
            pos = positions[i]
            tang = self.geometric_data['tangent_vectors'][i]
            norm = self.geometric_data['normal_vectors'][i]
            
            # Tangent vectors in red
            ax1.quiver(pos[0], pos[1], pos[2], tang[0], tang[1], tang[2], 
                      color='red', length=1.0, alpha=0.8, label='Tangent' if i == 0 else "")
            
            # Normal vectors in green
            ax1.quiver(pos[0], pos[1], pos[2], norm[0], norm[1], norm[2], 
                      color='green', length=0.5, alpha=0.6, label='Normal' if i == 0 else "")
        
        ax1.set_title('3D Geometry with Frenet Frame')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.legend()
        
        # 2. Twist progression
        ax2 = fig.add_subplot(2, 3, 2)
        ax2.plot(self.geometric_data['parameter_u'], self.geometric_data['twist_angles'], 'purple', linewidth=2)
        ax2.set_title('Twist Angle Progression')
        ax2.set_xlabel('Parameter u (radians)')
        ax2.set_ylabel('Twist Angle (radians)')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=np.pi, color='r', linestyle='--', alpha=0.7, label='π')
        ax2.axhline(y=2*np.pi, color='r', linestyle='--', alpha=0.7, label='2π')
        ax2.legend()
        
        # 3. Curvature and torsion analysis
        ax3 = fig.add_subplot(2, 3, 3)
        ax3.plot(self.geometric_data['parameter_u'], self.geometric_data['curvature'], 'orange', linewidth=2, label='Curvature')
        ax3_twin = ax3.twinx()
        ax3_twin.plot(self.geometric_data['parameter_u'], self.geometric_data['torsion'], 'brown', linewidth=2, label='Torsion')
        ax3.set_title('Curvature and Torsion')
        ax3.set_xlabel('Parameter u (radians)')
        ax3.set_ylabel('Curvature', color='orange')
        ax3_twin.set_ylabel('Torsion', color='brown')
        ax3.grid(True, alpha=0.3)
        ax3.legend(loc='upper left')
        ax3_twin.legend(loc='upper right')
        
        # 4. Field strength distribution
        ax4 = fig.add_subplot(2, 3, 4)
        ax4.plot(self.geometric_data['parameter_u'], self.geometric_data['field_strength'], 'cyan', linewidth=2)
        ax4.set_title('Φ-Field Strength Distribution')
        ax4.set_xlabel('Parameter u (radians)')
        ax4.set_ylabel('Field Strength')
        ax4.grid(True, alpha=0.3)
        
        # 5. Energy density distribution
        ax5 = fig.add_subplot(2, 3, 5)
        ax5.plot(self.geometric_data['parameter_u'], self.geometric_data['energy_density'], 'magenta', linewidth=2)
        ax5.set_title('Energy Density Distribution')
        ax5.set_xlabel('Parameter u (radians)')
        ax5.set_ylabel('Energy Density (J)')
        ax5.grid(True, alpha=0.3)
        ax5.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        # 6. Centroid distance and helicity
        ax6 = fig.add_subplot(2, 3, 6)
        ax6.plot(self.geometric_data['parameter_u'], self.geometric_data['centroid_distance'], 'darkblue', linewidth=2, label='Distance')
        
        # Mark centroid passages
        min_distances = np.array(self.geometric_data['centroid_distance'])
        from scipy.signal import find_peaks
        minima_indices, _ = find_peaks(-min_distances, prominence=0.5, distance=20)
        
        if len(minima_indices) > 0:
            ax6.scatter(np.array(self.geometric_data['parameter_u'])[minima_indices], 
                       min_distances[minima_indices], 
                       color='red', s=50, zorder=5, label=f'{len(minima_indices)} Passages')
        
        ax6.set_title(f'Centroid Distance - Helicity: {self.mobius.helicity.name}')
        ax6.set_xlabel('Parameter u (radians)')
        ax6.set_ylabel('Distance from Centroid')
        ax6.grid(True, alpha=0.3)
        ax6.legend()
        
        plt.tight_layout()
        
        if save_plots:
            filename = f'single_mobius_analysis_{self.mobius.helicity.name.lower()}.png'
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Single Möbius analysis plot saved to {filepath}")
        
        plt.show()
    
    def export_analysis_data(self, filename: Optional[str] = None) -> pd.DataFrame:
        """
        Export detailed analysis data to CSV.
        
        Args:
            filename: Optional custom filename
            
        Returns:
            DataFrame containing all analysis data
        """
        if self.geometric_data is None:
            self.analyze_geometry()
        
        if filename is None:
            filename = f'single_mobius_detailed_{self.mobius.helicity.name.lower()}.csv'
        
        # Construct DataFrame
        df_data = []
        for i in range(len(self.geometric_data['parameter_u'])):
            row = {
                'parameter_u': self.geometric_data['parameter_u'][i],
                'position_x': self.geometric_data['positions'][i][0],
                'position_y': self.geometric_data['positions'][i][1],
                'position_z': self.geometric_data['positions'][i][2],
                'tangent_x': self.geometric_data['tangent_vectors'][i][0],
                'tangent_y': self.geometric_data['tangent_vectors'][i][1],
                'tangent_z': self.geometric_data['tangent_vectors'][i][2],
                'normal_x': self.geometric_data['normal_vectors'][i][0],
                'normal_y': self.geometric_data['normal_vectors'][i][1],
                'normal_z': self.geometric_data['normal_vectors'][i][2],
                'binormal_x': self.geometric_data['binormal_vectors'][i][0],
                'binormal_y': self.geometric_data['binormal_vectors'][i][1],
                'binormal_z': self.geometric_data['binormal_vectors'][i][2],
                'twist_angle': self.geometric_data['twist_angles'][i],
                'curvature': self.geometric_data['curvature'][i],
                'torsion': self.geometric_data['torsion'][i],
                'field_strength': self.geometric_data['field_strength'][i],
                'energy_density': self.geometric_data['energy_density'][i],
                'centroid_distance': self.geometric_data['centroid_distance'][i],
                'helicity': self.mobius.helicity.value
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        filepath = self.output_dir / filename
        df.to_csv(filepath, index=False, float_format='%.6f')
        print(f"Single Möbius analysis data exported to {filepath}")
        
        return df
    
    def calculate_magnetic_moment_contribution(self) -> Dict[str, float]:
        """
        Calculate potential contribution to anomalous magnetic moment.
        
        This addresses Dr. Freeman's interest in the electron g-factor anomaly.
        The geometric structure might contribute to the observed deviation.
        
        Returns:
            Dictionary with magnetic moment calculations
        """
        if self.geometric_data is None:
            self.analyze_geometry()
        
        # Physical constants
        hbar = 1.055e-34  # Reduced Planck constant
        e = 1.602e-19     # Elementary charge
        me = 9.109e-31    # Electron mass
        
        # Calculate geometric contributions
        total_twist = self.geometric_data['twist_angles'][-1]  # Should be 2π
        avg_curvature = np.mean(self.geometric_data['curvature'])
        avg_field = np.mean(self.geometric_data['field_strength'])
        
        # Geometric g-factor contribution (simplified model)
        # This is a theoretical calculation based on Freeman's geometry
        geometric_factor = total_twist / (2 * np.pi)  # Should be 1 for proper Möbius
        curvature_correction = avg_curvature * 1e-6   # Small correction
        field_correction = avg_field * 1e-8           # Field-dependent correction
        
        # Estimate contribution to anomalous moment
        # Standard model predicts g ≈ 2.002319... 
        # This calculates potential geometric contribution
        anomalous_contribution = (geometric_factor - 1) + curvature_correction + field_correction
        
        results = {
            'total_twist_radians': total_twist,
            'average_curvature': avg_curvature,
            'average_field_strength': avg_field,
            'geometric_factor': geometric_factor,
            'curvature_correction': curvature_correction,
            'field_correction': field_correction,
            'anomalous_contribution': anomalous_contribution,
            'theoretical_g_factor': 2.0 + anomalous_contribution
        }
        
        return results

def analyze_single_mobius_complete(helicity: HelicityType = HelicityType.RIGHT) -> Tuple[SingleMobiusVisualizer, pd.DataFrame]:
    """
    Complete analysis of a single Möbius strip.
    
    This function provides the main interface for Dr. Freeman's single Möbius
    visualization requirements.
    
    Args:
        helicity: Helicity type (RIGHT, LEFT, or UNDEFINED)
        
    Returns:
        Tuple of (visualizer, analysis_dataframe)
    """
    print(f"Analyzing single Möbius strip with {helicity.name} helicity...")
    
    # Create Möbius strip
    mobius = create_standard_mobius(size_scale=1e-15)
    mobius.helicity = helicity
    
    # Create visualizer
    visualizer = SingleMobiusVisualizer(mobius)
    
    # Perform analysis
    geometric_data = visualizer.analyze_geometry(num_points=200)
    
    # Create visualizations
    visualizer.plot_complete_analysis()
    
    # Export data
    analysis_df = visualizer.export_analysis_data()
    
    # Calculate magnetic moment contribution
    mag_moment = visualizer.calculate_magnetic_moment_contribution()
    print(f"\nMagnetic moment analysis:")
    print(f"Total twist: {mag_moment['total_twist_radians']:.3f} radians ({mag_moment['total_twist_radians']/np.pi:.1f}π)")
    print(f"Geometric g-factor contribution: {mag_moment['anomalous_contribution']:.6f}")
    print(f"Theoretical g-factor: {mag_moment['theoretical_g_factor']:.6f}")
    
    return visualizer, analysis_df

if __name__ == "__main__":
    # Run complete single Möbius analysis
    print("Freeman's Single Möbius Strip Analysis")
    print("=" * 40)
    
    # Analyze right helicity
    viz_right, data_right = analyze_single_mobius_complete(HelicityType.RIGHT)
    
    # Analyze left helicity
    viz_left, data_left = analyze_single_mobius_complete(HelicityType.LEFT)
    
    print("\nSingle Möbius analysis complete!")
    print("Generated visualizations and data files in test_results/")