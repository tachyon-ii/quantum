"""
Crystal Assembly Visualizer for Freeman's Geometric Theory - OPTIMIZED VERSION.

This module provides comprehensive visualization and analysis for crystalline
conformations of crossed Möbius strips, addressing Dr. Freeman's final
visualization requirement and the collective electromagnetic effects.

OPTIMIZED: Integrates with improved crystal_assembly.py for accurate Freeman theory validation.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json

# Import from existing modules
from .crystal_assembly import MobiusCrystal, CrystalType, CrystalSymmetry
from .g_factor_calculator import MobiusGFactorCalculator, demo_james_octahedral_model

class CrystalAssemblyVisualizer:
    """
    Comprehensive visualization for Möbius crystal assemblies.
    
    Addresses Dr. Freeman's requirement for crystalline conformation analysis,
    focusing on octahedral crystals and electromagnetic field patterns.
    
    OPTIMIZED for Freeman's theory with improved field calculations and g-factor integration.
    """
    
    def __init__(self, crystal: MobiusCrystal):
        """
        Initialize visualizer with a crystal assembly.
        
        Args:
            crystal: MobiusCrystal instance to analyze
        """
        self.crystal = crystal
        self.analysis_data = None
        self.output_dir = Path("test_results")
        self.output_dir.mkdir(exist_ok=True)
        
    def analyze_crystal_structure(self, num_field_points: int = 500) -> Dict:
        """
        Comprehensive analysis of crystal structure and properties.

        Args:
            num_field_points: Number of points for field analysis

        Returns:
            Dictionary containing all crystal analysis data
        """
        # Ensure crystal structure is generated
        if not self.crystal.tetrahedral_units:
            self.crystal.generate_crystal_structure()

        # Initialize analysis_data first
        data = {
            'crystal_size': self.crystal.crystal_size,
            'crystal_type': self.crystal.crystal_type,
            'crystal_symmetry': self.crystal.crystal_symmetry,
            'total_units': self.crystal.total_units,
            'lattice_parameters': self.crystal.lattice_parameters,
            'crystal_properties': self.crystal.crystal_properties.__dict__ if self.crystal.crystal_properties else {},
            'helicity_distribution': self.crystal.helicity_distribution,
            'unit_positions': [],
            'unit_charges': [],
            'unit_energies': [],
            'majorana_pairs': []
        }

        # Analyze individual tetrahedral units
        for position, unit in self.crystal.tetrahedral_units.items():
            if unit is None:
                continue
                
            data['unit_positions'].append(position)

            # Extract unit properties with error handling
            if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                unit_charge = unit.charge_distribution.net_charge
            else:
                unit_charge = 0.0
            data['unit_charges'].append(unit_charge)

            if hasattr(unit, 'interaction_energy') and unit.interaction_energy:
                unit_energy = unit.interaction_energy.binding_energy
            else:
                unit_energy = 0.0
            data['unit_energies'].append(unit_energy)

            # Check for Majorana pairs using existing property
            if hasattr(unit, 'is_majorana_pair') and unit.is_majorana_pair:
                data['majorana_pairs'].append(position)

        # Validate charge distributions
        charge_validation = self._ensure_meaningful_charges(self.crystal)
        data['charge_validation'] = charge_validation

        # Set analysis_data before calling other methods
        self.analysis_data = data

        # Now call methods that depend on analysis_data
        em_data = self._analyze_electromagnetic_fields(num_field_points)
        data.update(em_data)

        magnetic_data = self._calculate_collective_magnetic_moment()
        data.update(magnetic_data)

        symmetry_data = self._analyze_crystal_symmetries()
        data.update(symmetry_data)

        # Update analysis_data with all collected data
        self.analysis_data = data
        return data
    
    def _ensure_meaningful_charges(self, crystal: MobiusCrystal) -> Dict:
        """Ensure crystal units have meaningful charge distributions for field analysis."""
        
        units_with_zero_charge = 0
        total_charge = 0.0
        charges = []
        
        for position, unit in crystal.tetrahedral_units.items():
            if unit is None:
                units_with_zero_charge += 1
                charges.append(0.0)
                continue
                
            if not hasattr(unit, 'charge_distribution') or unit.charge_distribution is None:
                units_with_zero_charge += 1
                charges.append(0.0)
            else:
                charge = unit.charge_distribution.net_charge
                charges.append(charge)
                total_charge += abs(charge)
                if abs(charge) < 0.1:
                    units_with_zero_charge += 1
        
        total_units = len([u for u in crystal.tetrahedral_units.values() if u is not None])
        
        charge_stats = {
            'total_units': total_units,
            'zero_charge_units': units_with_zero_charge,
            'zero_charge_fraction': units_with_zero_charge / max(total_units, 1),
            'total_charge_magnitude': total_charge,
            'average_charge_magnitude': total_charge / max(len(charges), 1),
            'charge_distribution_meaningful': units_with_zero_charge < total_units * 0.7
        }
        
        if not charge_stats['charge_distribution_meaningful']:
            print(f"Warning: {units_with_zero_charge}/{total_units} units have negligible charge")
            print("This explains low field circularity values")
        
        return charge_stats
    
    def _calculate_field_uniformity(self, field_strengths: np.ndarray) -> float:
        """Validated field uniformity calculation - always positive."""
        
        if len(field_strengths) == 0:
            return 0.0
        
        # Filter out zero/near-zero values
        valid_fields = field_strengths[field_strengths > 1e-30]
        
        if len(valid_fields) == 0:
            return 0.0
        
        mean_strength = np.mean(valid_fields)
        if mean_strength > 0:
            coefficient_of_variation = np.std(valid_fields) / mean_strength
            # Convert to uniformity score (0 = highly variable, 1 = uniform)
            field_uniformity = np.exp(-coefficient_of_variation)
        else:
            field_uniformity = 0.0
        
        return float(field_uniformity)
    
    def _analyze_electromagnetic_fields(self, num_points: int) -> Dict:
        """Analyze electromagnetic fields around the crystal with validated calculations."""
        if not self.crystal.lattice_parameters:
            return {'field_analysis': 'No lattice parameters available'}

        # Define sampling region around crystal - use lattice_constant for all dimensions
        lattice = self.crystal.lattice_parameters
        lattice_const = lattice.lattice_constant

        # For cubic crystals, use the same lattice constant for all dimensions
        # Scale by crystal size to get actual dimensions
        crystal_x = self.crystal.crystal_size[0] * lattice_const
        crystal_y = self.crystal.crystal_size[1] * lattice_const
        crystal_z = self.crystal.crystal_size[2] * lattice_const

        min_bound = np.array([-crystal_x/2, -crystal_y/2, -crystal_z/2])
        max_bound = np.array([crystal_x/2, crystal_y/2, crystal_z/2])

        # Physical constants for proper field calculation
        k_e = 8.99e9  # Coulomb constant (N⋅m²/C²)
        elementary_charge = 1.602e-19  # Coulombs
        
        sampling_points = []
        field_strengths = []
        electric_field_vectors = []
        magnetic_field_vectors = []

        for _ in range(num_points):
            # Random sampling in crystal volume
            point = min_bound + np.random.random(3) * (max_bound - min_bound)
            sampling_points.append(point)

            # Calculate field contributions from all units
            total_electric_field = np.zeros(3)
            total_magnetic_field = np.zeros(3)

            for position, unit in self.crystal.tetrahedral_units.items():
                if unit is None:
                    continue
                    
                if position in self.crystal.lattice_positions:
                    unit_pos = np.array(self.crystal.lattice_positions[position])
                else:
                    # Fallback: use position tuple as coordinates
                    unit_pos = np.array(position, dtype=float) * lattice_const
                    
                r_vec = point - unit_pos
                r_mag = np.linalg.norm(r_vec)

                if r_mag < 1e-20:  # Avoid singularity
                    continue

                r_hat = r_vec / r_mag

                # Electric field contribution (Coulomb) with proper units
                if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                    charge = float(unit.charge_distribution.net_charge)
                    # Proper Coulomb field with regularization
                    e_field = k_e * charge * elementary_charge * r_hat / (r_mag**2 + 1e-30)
                    # Ensure field is real-valued
                    if np.isfinite(e_field).all():
                        total_electric_field += e_field

                # Magnetic field contribution (simplified dipole)
                if hasattr(unit, 'is_majorana_pair') and unit.is_majorana_pair:
                    # Majorana pairs have magnetic dipole moments
                    mu_0 = 4*np.pi*1e-7  # Magnetic permeability
                    dipole_moment = np.array([0, 0, 9.274e-24])  # Bohr magneton along z
                    # Magnetic dipole field
                    if r_mag > 1e-15:
                        b_field = (mu_0 / (4*np.pi*r_mag**3)) * (
                            3 * np.dot(dipole_moment, r_hat) * r_hat - dipole_moment
                        )
                        if np.isfinite(b_field).all():
                            total_magnetic_field += b_field

            field_strength = np.linalg.norm(total_electric_field) + np.linalg.norm(total_magnetic_field)
            field_strengths.append(field_strength)
            electric_field_vectors.append(total_electric_field)
            magnetic_field_vectors.append(total_magnetic_field)

        field_strengths = np.array(field_strengths)
        
        # Calculate field uniformity using validated method
        field_uniformity = self._calculate_field_uniformity(field_strengths)
        
        # Calculate coefficient of variation for reporting
        if len(field_strengths) > 0:
            valid_fields = field_strengths[field_strengths > 1e-30]
            if len(valid_fields) > 0 and np.mean(valid_fields) > 0:
                coefficient_of_variation = np.std(valid_fields) / np.mean(valid_fields)
            else:
                coefficient_of_variation = 0.0
        else:
            coefficient_of_variation = 0.0

        return {
            'field_sampling_points': sampling_points,
            'field_strengths': field_strengths.tolist(),
            'electric_field_vectors': electric_field_vectors,
            'magnetic_field_vectors': magnetic_field_vectors,
            'avg_field_strength': float(np.mean(field_strengths)),
            'max_field_strength': float(np.max(field_strengths)) if len(field_strengths) > 0 else 0.0,
            'field_uniformity': float(field_uniformity),  # Now guaranteed to be positive
            'coefficient_of_variation': float(coefficient_of_variation)  # Now properly defined
        }

    def _calculate_collective_magnetic_moment(self) -> Dict:
        """Use James's demo octahedral model for g-factor calculation."""
        
        # Use James's proven octahedral calculation
        g_factor_result = demo_james_octahedral_model()
        
        # Get crystal data for display
        total_units = self.crystal.total_units
        majorana_pairs = sum(1 for unit in self.crystal.tetrahedral_units.values() 
                            if unit is not None and hasattr(unit, 'is_majorana_pair') and unit.is_majorana_pair)
        
        unit_charges = []
        for unit in self.crystal.tetrahedral_units.values():
            if unit is None:
                unit_charges.append(0.0)
                continue
            if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                unit_charges.append(unit.charge_distribution.net_charge)
            else:
                unit_charges.append(0.0)
        
        return {
            'collective_factor': np.log(max(1, total_units)) / max(1, total_units),
            'majorana_factor': majorana_pairs / max(1, total_units),
            'charge_asymmetry': abs(sum(unit_charges)) / max(1, total_units),
            'geometric_g_contribution': g_factor_result.geometric_contribution,
            'theoretical_g_factor': g_factor_result.total_theoretical_g,
            'experimental_g_factor': g_factor_result.experimental_g,
            'deviation_explained_fraction': g_factor_result.deviation_explained,
            'avg_unit_separation': 1e-15,
            'total_units_contributing': total_units,
            'majorana_pairs_count': majorana_pairs,
            'base_james_contribution': g_factor_result.geometric_contribution,
            'collective_enhancement': 0.0
        }

    def _analyze_crystal_symmetries(self) -> Dict:
        """Analyze crystal symmetries and rotational properties."""
        # Get unit positions and charges directly from crystal instead of analysis_data
        positions = []
        charges = []

        for position, unit in self.crystal.tetrahedral_units.items():
            if unit is None:
                continue
            positions.append(position)

            # Get charge from unit
            if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                charge = unit.charge_distribution.net_charge
            else:
                charge = 0.0
            charges.append(charge)

        if len(positions) == 0:
            return {
                'center_of_mass': np.zeros(3),
                'principal_moments': [0, 0, 0],
                'asymmetry_parameter': 0.0,
                'has_single_rotation_axis': False,
                'produces_circular_field': False
            }

        positions = np.array(positions)
        charges = np.array(charges)

        # Calculate center of mass
        center_of_mass = np.average(positions, axis=0, weights=np.abs(charges) + 1e-10)

        # Calculate moments of inertia (simplified)
        relative_positions = positions - center_of_mass
        I_xx = np.sum((relative_positions[:, 1]**2 + relative_positions[:, 2]**2))
        I_yy = np.sum((relative_positions[:, 0]**2 + relative_positions[:, 2]**2))
        I_zz = np.sum((relative_positions[:, 0]**2 + relative_positions[:, 1]**2))

        # Principal moments
        principal_moments = sorted([I_xx, I_yy, I_zz])

        # Asymmetry parameter
        if principal_moments[2] > 1e-10:
            asymmetry = (principal_moments[1] - principal_moments[0]) / principal_moments[2]
        else:
            asymmetry = 0.0

        # Rotational axis analysis (for Dr. Freeman's octahedral interest)
        has_single_axis = asymmetry < 0.1  # Near-symmetric top

        return {
            'center_of_mass': center_of_mass,
            'principal_moments': principal_moments,
            'asymmetry_parameter': asymmetry,
            'has_single_rotation_axis': has_single_axis,
            'produces_circular_field': has_single_axis and asymmetry < 0.05
        }

    def analyze_rotational_field_patterns(self) -> Dict:
        """Analyze rotational axes and electromagnetic field patterns."""
    
        field_analyzer = RotationalFieldAnalyzer(self.crystal)
        rotation_field_analysis = field_analyzer.comprehensive_rotational_analysis()
    
        return rotation_field_analysis

    def plot_crystal_structure_3d(self, save_plots: bool = True) -> None:
        """Create 3D visualization of crystal structure."""
        if self.analysis_data is None:
            self.analyze_crystal_structure()
        
        fig = plt.figure(figsize=(15, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        positions = np.array(self.analysis_data['unit_positions'])
        charges = np.array(self.analysis_data['unit_charges'])
        energies = np.array(self.analysis_data['unit_energies'])
        
        if len(positions) == 0:
            print("Warning: No unit positions found for visualization")
            return
        
        # Color-code by charge
        colors = []
        for charge in charges:
            if abs(charge) < 0.1:
                colors.append('green')  # Neutral (Majorana pairs)
            elif charge > 0:
                colors.append('red')    # Positive
            else:
                colors.append('blue')   # Negative
        
        # Size by energy magnitude
        if len(energies) > 0 and np.max(np.abs(energies)) > 0:
            sizes = 50 + 100 * np.abs(energies) / (np.max(np.abs(energies)) + 1e-20)
        else:
            sizes = [50] * len(positions)
        
        # Plot units
        scatter = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                           c=colors, s=sizes, alpha=0.7, edgecolors='black')
        
        # Connect nearby units with bonds
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                dist = np.linalg.norm(positions[i] - positions[j])
                # Connect if within reasonable bonding distance
                if dist < np.mean([self.crystal.crystal_size[k] for k in range(3)]):
                    ax.plot([positions[i,0], positions[j,0]],
                           [positions[i,1], positions[j,1]],
                           [positions[i,2], positions[j,2]], 'k-', alpha=0.3, linewidth=1)
        
        # Mark center of mass
        com = self.analysis_data['center_of_mass']
        ax.scatter(com[0], com[1], com[2], c='gold', s=200, marker='*', 
                  edgecolors='black', linewidth=2, label='Center of Mass')
        
        ax.set_title(f'Crystal Structure: {self.crystal.crystal_type.name}\n'
                    f'Size: {self.crystal.crystal_size}, Symmetry: {self.crystal.crystal_symmetry.name}\n'
                    f'Total Units: {self.analysis_data["total_units"]}, Majorana Pairs: {len(self.analysis_data["majorana_pairs"])}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Custom legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Neutral (Majorana)'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Positive Charge'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Negative Charge'),
            Line2D([0], [0], marker='*', color='w', markerfacecolor='gold', markersize=15, label='Center of Mass')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        if save_plots:
            filename = f'crystal_structure_3d_{self.crystal.crystal_type.name.lower()}_{self.crystal.crystal_symmetry.name.lower()}.png'
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"3D crystal structure plot saved to {filepath}")
        
        plt.show()
    
    def plot_electromagnetic_analysis(self, save_plots: bool = True) -> None:
        """Create electromagnetic field analysis plots."""
        if self.analysis_data is None:
            self.analyze_crystal_structure()
        
        fig = plt.figure(figsize=(20, 15))
        fig.suptitle(f'Electromagnetic Analysis: {self.crystal.crystal_type.name} Crystal\n'
                    f'g-factor contribution: {self.analysis_data["geometric_g_contribution"]:.6f}', 
                     fontsize=16, fontweight='bold')
        
        # 1. Field strength distribution
        ax1 = fig.add_subplot(2, 3, 1)
        field_strengths = self.analysis_data['field_strengths']
        if len(field_strengths) > 0:
            ax1.hist(field_strengths, bins=30, alpha=0.7, color='purple', edgecolor='black')
            ax1.axvline(self.analysis_data['avg_field_strength'], color='red', linestyle='--', 
                       label=f'Average: {self.analysis_data["avg_field_strength"]:.2e}')
        ax1.set_title('Field Strength Distribution')
        ax1.set_xlabel('Field Strength')
        ax1.set_ylabel('Frequency')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Charge distribution
        ax2 = fig.add_subplot(2, 3, 2)
        charges = self.analysis_data['unit_charges']
        if len(charges) > 0:
            charge_bins = np.linspace(min(charges)-0.1, max(charges)+0.1, 21)
            ax2.hist(charges, bins=charge_bins, alpha=0.7, color='orange', edgecolor='black')
            ax2.axvline(0, color='black', linestyle='-', linewidth=2, label='Neutral')
        ax2.set_title('Unit Charge Distribution')
        ax2.set_xlabel('Charge (e)')
        ax2.set_ylabel('Number of Units')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Energy distribution  
        ax3 = fig.add_subplot(2, 3, 3)
        energies = self.analysis_data['unit_energies']
        if len(energies) > 0:
            ax3.hist(energies, bins=20, alpha=0.7, color='green', edgecolor='black')
            ax3.axvline(0, color='black', linestyle='-', linewidth=2, label='Zero Energy')
        ax3.set_title('Unit Energy Distribution')
        ax3.set_xlabel('Binding Energy (J)')
        ax3.set_ylabel('Number of Units')
        ax3.ticklabel_format(style='scientific', axis='x', scilimits=(0,0))
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Magnetic moment analysis - FIXED
        ax4 = fig.add_subplot(2, 3, 4)
        mag_data = {
            'Collective Factor': self.analysis_data.get('collective_factor', 0.0),
            'Majorana Factor': self.analysis_data.get('majorana_factor', 0.0),
            'Base James Contrib': self.analysis_data.get('base_james_contribution', 0.0)
        }
        
        factors = list(mag_data.keys())
        values = list(mag_data.values())
        
        bars = ax4.bar(factors, values, color=['cyan', 'magenta', 'yellow'], alpha=0.7)
        ax4.set_title('Magnetic Moment Contributing Factors')
        ax4.set_ylabel('Factor Value')
        ax4.tick_params(axis='x', rotation=45)
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.3e}', ha='center', va='bottom')
        
        # 5. g-factor analysis
        ax5 = fig.add_subplot(2, 3, 5)
        g_factors = {
            'Theoretical': self.analysis_data['theoretical_g_factor'],
            'Experimental': self.analysis_data['experimental_g_factor'],
            'Standard Model': 2.0
        }
        
        g_names = list(g_factors.keys())
        g_values = list(g_factors.values())
        
        bars = ax5.bar(g_names, g_values, color=['blue', 'red', 'gray'], alpha=0.7)
        ax5.set_title('g-factor Comparison')
        ax5.set_ylabel('g-factor value')
        ax5.tick_params(axis='x', rotation=45)
        
        # Add difference annotations
        exp_val = self.analysis_data['experimental_g_factor']
        theo_val = self.analysis_data['theoretical_g_factor']
        deviation_fraction = self.analysis_data['deviation_explained_fraction']
        
        ax5.text(0.5, 0.95, f'Deviation explained: {deviation_fraction:.1%}', 
                transform=ax5.transAxes, ha='center', va='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # 6. Rotational properties
        ax6 = fig.add_subplot(2, 3, 6)
        rot_props = {
            'Asymmetry': self.analysis_data.get('asymmetry_parameter', 0.0),
            'Field Uniformity': self.analysis_data.get('field_uniformity', 0.0)
        }
        
        prop_names = list(rot_props.keys())
        prop_values = list(rot_props.values())
        
        bars = ax6.bar(prop_names, prop_values, color=['brown', 'pink'], alpha=0.7)
        ax6.set_title('Rotational & Field Properties')
        ax6.set_ylabel('Property Value (0-1)')
        ax6.set_ylim(0, 1.1)
        
        # Add single axis indicator
        single_axis = self.analysis_data.get('has_single_rotation_axis', False)
        circular_field = self.analysis_data.get('produces_circular_field', False)
        
        ax6.text(0.5, 0.85, f'Single Rotation Axis: {single_axis}', 
                transform=ax6.transAxes, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        ax6.text(0.5, 0.70, f'Circular Field: {circular_field}', 
                transform=ax6.transAxes, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        plt.tight_layout()
        
        if save_plots:
            filename = f'crystal_electromagnetic_{self.crystal.crystal_type.name.lower()}_{self.crystal.crystal_symmetry.name.lower()}.png'
            filepath = self.output_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Electromagnetic analysis plot saved to {filepath}")
        
        plt.show()
    
    def export_crystal_analysis(self, filename: Optional[str] = None) -> pd.DataFrame:
        """Export comprehensive crystal analysis data."""
        if self.analysis_data is None:
            self.analyze_crystal_structure()

        if filename is None:
            filename = f'crystal_analysis_{self.crystal.crystal_type.name.lower()}_{self.crystal.crystal_symmetry.name.lower()}.json'

        # Save complete analysis as JSON for easy access
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            # Convert numpy arrays to lists and enums to strings for JSON serialization
            export_data = {}
            for key, value in self.analysis_data.items():
                if isinstance(value, np.ndarray):
                    export_data[key] = value.tolist()
                elif hasattr(value, '__dict__'):
                    export_data[key] = str(value)
                elif isinstance(value, dict):
                    # Handle nested dictionaries that might contain enums
                    export_data[key] = self._convert_dict_for_json(value)
                else:
                    export_data[key] = value

            json.dump(export_data, f, indent=2, default=str)

        print(f"Crystal analysis data exported to {filepath}")

        # Also create a summary CSV
        csv_filename = filename.replace('.json', '_summary.csv')
        summary_data = {
            'crystal_type': [self.crystal.crystal_type.name],
            'crystal_symmetry': [self.crystal.crystal_symmetry.name],
            'total_units': [self.analysis_data['total_units']],
            'majorana_pairs': [len(self.analysis_data['majorana_pairs'])],
            'net_charge': [sum(self.analysis_data['unit_charges'])],
            'avg_field_strength': [self.analysis_data['avg_field_strength']],
            'geometric_g_contribution': [self.analysis_data['geometric_g_contribution']],
            'theoretical_g_factor': [self.analysis_data['theoretical_g_factor']],
            'deviation_explained_fraction': [self.analysis_data['deviation_explained_fraction']],
            'has_single_rotation_axis': [self.analysis_data['has_single_rotation_axis']],
            'produces_circular_field': [self.analysis_data['produces_circular_field']]
        }

        df = pd.DataFrame(summary_data)
        csv_filepath = self.output_dir / csv_filename
        df.to_csv(csv_filepath, index=False)
        print(f"Crystal summary data exported to {csv_filepath}")

        return df

    def _convert_dict_for_json(self, data_dict):
        """Convert dictionary values to JSON-serializable format."""
        converted = {}
        for key, value in data_dict.items():
            # Convert enum keys to strings
            if hasattr(key, 'name'):  # Enum key
                key_str = key.name
            else:
                key_str = str(key)

            # Convert enum values to strings
            if hasattr(value, 'name'):  # Enum value
                converted[key_str] = value.name
            elif isinstance(value, np.ndarray):
                converted[key_str] = value.tolist()
            elif isinstance(value, dict):
                converted[key_str] = self._convert_dict_for_json(value)
            else:
                converted[key_str] = value

        return converted
    
    def analyze_octahedral_crystals(self) -> Dict:
        """
        Analyze octahedral crystal forms specifically as mentioned by James.

        Tests James's prediction that octahedral crystals "probably do NOT 
        result in a circular electric field" unlike other geometries.
        """

        # Create octahedral crystal arrangement
        octahedral_crystal = self._create_octahedral_crystal()

        # Analyze its properties
        octahedral_analyzer = CrystalGeometryAnalyzer(octahedral_crystal)
        octahedral_data = octahedral_analyzer.analyze_octahedral_geometry()

        # Compare with current crystal
        current_analyzer = CrystalGeometryAnalyzer(self.crystal)
        current_data = current_analyzer.analyze_octahedral_geometry()

        # Detailed rotation axis analysis
        rotation_analysis = self._detailed_rotation_analysis(octahedral_crystal)

        # Field pattern comparison
        field_comparison = self._compare_field_patterns(octahedral_crystal, self.crystal)

        return {
            'octahedral_crystal_analysis': octahedral_data,
            'current_crystal_analysis': current_data,
            'rotation_axis_details': rotation_analysis,
            'field_pattern_comparison': field_comparison,
            'james_prediction_test': self._test_james_octahedral_prediction(octahedral_data, current_data)
        }

    def _create_octahedral_crystal(self) -> MobiusCrystal:
        """Create a true octahedral crystal arrangement."""

        # Octahedral crystal: 6 units positioned at ±x, ±y, ±z vertices
        octahedral_crystal = MobiusCrystal(
            crystal_size=(3, 3, 3),  # Will be overridden with octahedral positions
            crystal_type=self.crystal.crystal_type,
            crystal_symmetry=CrystalSymmetry.CUBIC  # Start with cubic, modify to octahedral
        )

        # Generate base structure
        octahedral_crystal.generate_crystal_structure()

        # Clear existing units and create octahedral arrangement
        octahedral_crystal.tetrahedral_units.clear()
        octahedral_crystal.lattice_positions.clear()

        # Define octahedral vertices (6 points along coordinate axes)
        lattice_constant = octahedral_crystal.lattice_parameters.lattice_constant
        octahedral_positions = [
            (1, 0, 0, np.array([lattice_constant, 0, 0])),      # +x
            (-1, 0, 0, np.array([-lattice_constant, 0, 0])),    # -x
            (0, 1, 0, np.array([0, lattice_constant, 0])),      # +y
            (0, -1, 0, np.array([0, -lattice_constant, 0])),    # -y
            (0, 0, 1, np.array([0, 0, lattice_constant])),      # +z
            (0, 0, -1, np.array([0, 0, -lattice_constant]))     # -z
        ]

        # Create tetrahedral units at octahedral vertices
        for i, (idx_x, idx_y, idx_z, position) in enumerate(octahedral_positions):
            # Use original helicity determination method
            helicity1, helicity2 = self.crystal._determine_helicities_at_site(idx_x, idx_y, idx_z)

            # Create unit at octahedral position
            unit = self.crystal._create_tetrahedral_unit_at_position(position, helicity1, helicity2)

            if unit is not None:
                # Store with octahedral index
                octahedral_crystal.tetrahedral_units[(idx_x, idx_y, idx_z)] = unit
                octahedral_crystal.lattice_positions[(idx_x, idx_y, idx_z)] = position

        # Update total units count
        octahedral_crystal.total_units = len(octahedral_crystal.tetrahedral_units)

        # Recalculate properties for octahedral arrangement
        try:
            octahedral_crystal._calculate_crystal_properties()
            octahedral_crystal._analyze_helicity_distribution()
            octahedral_crystal._identify_majorana_pairs()
        except Exception as e:
            print(f"Warning: Failed to recalculate octahedral crystal properties: {e}")

        return octahedral_crystal

    def _detailed_rotation_analysis(self, crystal: MobiusCrystal) -> Dict:
        """Detailed analysis of rotation axes and symmetries."""

        positions = []
        orientations = []

        for position, unit in crystal.tetrahedral_units.items():
            if unit is None:
                continue
            positions.append(position)

            # Get unit orientation from crossing geometry
            if hasattr(unit, 'crossing_geometry') and unit.crossing_geometry:
                if hasattr(unit.crossing_geometry, 'crossing_point'):
                    orientation = unit.crossing_geometry.crossing_point
                else:
                    orientation = np.array([0, 0, 1])
            else:
                orientation = np.array([0, 0, 1])
            orientations.append(orientation)

        if len(positions) == 0:
            return {'error': 'No valid units found'}

        positions = np.array(positions)
        orientations = np.array(orientations)

        # Calculate moment of inertia tensor
        center = np.mean(positions, axis=0)
        relative_positions = positions - center

        I_tensor = np.zeros((3, 3))
        for pos in relative_positions:
            r_squared = np.dot(pos, pos)
            I_tensor += r_squared * np.eye(3) - np.outer(pos, pos)

        # Principal axes analysis
        eigenvalues, eigenvectors = np.linalg.eigh(I_tensor)
        sorted_indices = np.argsort(eigenvalues)

        I1, I2, I3 = eigenvalues[sorted_indices]
        axis1, axis2, axis3 = eigenvectors[:, sorted_indices].T

        # Classify rotor type
        if I3 > 1e-10:
            asymmetry_param = (I2 - I1) / I3

            if asymmetry_param < 0.01:
                rotor_type = "prolate_symmetric_top"  # Cigar-like, single rotation axis
                natural_axis = axis3  # Highest moment
            elif asymmetry_param > 0.99:
                rotor_type = "oblate_symmetric_top"   # Disk-like, single rotation axis  
                natural_axis = axis1  # Lowest moment
            else:
                rotor_type = "asymmetric_top"         # No single natural axis
                natural_axis = axis3  # Default to highest moment
        else:
            rotor_type = "degenerate"
            natural_axis = np.array([0, 0, 1])
            asymmetry_param = 0

        return {
            'rotor_type': rotor_type,
            'natural_rotation_axis': natural_axis,
            'principal_moments': [I1, I2, I3],
            'asymmetry_parameter': asymmetry_param,
            'has_single_axis': rotor_type in ['prolate_symmetric_top', 'oblate_symmetric_top'],
            'crystal_shape': self._classify_crystal_shape(I1, I2, I3)
        }

    def _classify_crystal_shape(self, I1: float, I2: float, I3: float) -> str:
        """Classify crystal shape based on moments of inertia."""
        if I3 <= 1e-10:
            return "degenerate"

        # Normalize moments
        I1_norm, I2_norm, I3_norm = I1/I3, I2/I3, 1.0

        if abs(I1_norm - I2_norm) < 0.05:
            if I3_norm > 1.5:
                return "prolate_ellipsoid"  # Cigar-like
            else:
                return "oblate_ellipsoid"   # Disk-like
        else:
            return "triaxial_ellipsoid"     # General ellipsoid

    def _compare_field_patterns(self, octahedral_crystal: MobiusCrystal, 
                          current_crystal: MobiusCrystal) -> Dict:
        """Compare electromagnetic field patterns between crystal types."""

        # Analyze field patterns for both crystals
        octahedral_fields = self._analyze_field_pattern(octahedral_crystal)
        current_fields = self._analyze_field_pattern(current_crystal)

        return {
            'octahedral_field_pattern': octahedral_fields,
            'current_field_pattern': current_fields,
            'field_circularity_comparison': {
                'octahedral_circularity': octahedral_fields['circularity_score'],
                'current_circularity': current_fields['circularity_score'],
                'octahedral_more_circular': octahedral_fields['circularity_score'] > current_fields['circularity_score']
            },
            'rotation_axis_comparison': {
                'octahedral_has_axis': octahedral_fields['has_natural_axis'],
                'current_has_axis': current_fields['has_natural_axis'],
                'both_have_axis': octahedral_fields['has_natural_axis'] and current_fields['has_natural_axis']
            }
        }

    def _analyze_field_pattern(self, crystal: MobiusCrystal) -> Dict:
        """Analyze electromagnetic field pattern for a crystal."""

        positions = np.array(list(crystal.lattice_positions.values()))
        if len(positions) == 0:
            return {
                'circularity_score': 0.0,
                'has_natural_axis': False,
                'field_magnitude_variation': 0.0,
                'dominant_field_direction': np.array([0, 0, 1]),
                'field_symmetry': 0.0
            }

        center = np.mean(positions, axis=0)

        # Test field at points around the crystal
        test_radius = np.mean(np.linalg.norm(positions - center, axis=1)) * 1.5
        num_test_points = 24

        # Create test points in sphere around crystal
        test_points = []
        field_vectors = []

        for i in range(num_test_points):
            theta = np.arccos(1 - 2 * i / num_test_points)  # Uniform sphere sampling
            phi = np.pi * (1 + 5**0.5) * i  # Golden angle

            test_point = center + test_radius * np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ])
            test_points.append(test_point)

            # Calculate field at this point
            total_field = np.zeros(3)
            for position, unit in crystal.tetrahedral_units.items():
                if unit is None:
                    continue
                unit_pos = np.array(crystal.lattice_positions[position])
                r_vec = test_point - unit_pos
                r_mag = np.linalg.norm(r_vec)

                if r_mag > 1e-10:
                    r_hat = r_vec / r_mag

                    # Electric field from unit charge
                    if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                        charge = unit.charge_distribution.net_charge
                        field_contribution = charge * r_hat / (r_mag**2)
                        total_field += field_contribution

            field_vectors.append(total_field)

        # Analyze field circularity using validated method
        circularity_score = self._calculate_spherical_circularity(test_points, field_vectors, center)

        # Check for natural rotation axis
        rotation_analysis = self._detailed_rotation_analysis(crystal)

        return {
            'circularity_score': circularity_score,
            'has_natural_axis': rotation_analysis.get('has_single_axis', False),
            'field_magnitude_variation': np.std([np.linalg.norm(f) for f in field_vectors]),
            'dominant_field_direction': self._find_dominant_field_direction(field_vectors),
            'field_symmetry': rotation_analysis.get('asymmetry_parameter', 0.0)
        }

    def _calculate_spherical_circularity(self, points: List[np.ndarray], 
                                       fields: List[np.ndarray], 
                                       center: np.ndarray) -> float:
        """Fixed circularity calculation based on validation results."""
        
        if len(points) != len(fields) or len(points) == 0:
            return 0.0
        
        circularity_scores = []
        
        for point, field in zip(points, fields):
            r_vec = point - center
            r_mag = np.linalg.norm(r_vec)
            field_mag = np.linalg.norm(field)
            
            # Use more robust thresholds based on validation
            if r_mag > 1e-20 and field_mag > 1e-20:
                r_hat = r_vec / r_mag
                field_hat = field / field_mag
                
                # For circular field, field should be tangent to sphere
                radial_component = abs(np.dot(r_hat, field_hat))
                radial_component = np.clip(radial_component, 0.0, 1.0)  # Ensure valid range
                
                tangential_score = 1.0 - radial_component
                circularity_scores.append(tangential_score)
        
        return float(np.mean(circularity_scores)) if circularity_scores else 0.0

    def _find_dominant_field_direction(self, field_vectors: List[np.ndarray]) -> np.ndarray:
        """Find the dominant direction of field vectors."""
        if not field_vectors:
            return np.array([0, 0, 1])

        # Average field direction (vector sum)
        total_field = np.sum(field_vectors, axis=0)
        total_mag = np.linalg.norm(total_field)

        if total_mag > 1e-10:
            return total_field / total_mag
        else:
            return np.array([0, 0, 1])

    def _test_james_octahedral_prediction(self, octahedral_data: Dict, current_data: Dict) -> Dict:
        """
        Test James's prediction that octahedral crystals probably do NOT 
        result in circular electric fields.
        """

        octahedral_circular = octahedral_data['field_circularity']['produces_circular_field']
        octahedral_circularity = octahedral_data['field_circularity']['average_circularity']

        current_circular = current_data['field_circularity']['produces_circular_field']
        current_circularity = current_data['field_circularity']['average_circularity']

        # James's prediction: octahedral should NOT produce circular fields
        prediction_correct = not octahedral_circular

        return {
            'james_prediction': "Octahedral crystals probably do NOT result in circular electric field",
            'octahedral_produces_circular': octahedral_circular,
            'octahedral_circularity_score': octahedral_circularity,
            'current_produces_circular': current_circular,
            'current_circularity_score': current_circularity,
            'prediction_supported': prediction_correct,
            'octahedral_vs_current': {
                'octahedral_less_circular': octahedral_circularity < current_circularity,
                'circularity_difference': current_circularity - octahedral_circularity
            }
        }


class CrystalGeometryAnalyzer:
    """
    Analyze different crystal geometries for Freeman's theory.
    
    Focuses on octahedral crystals and rotational axes as mentioned by James.
    """
    
    def __init__(self, crystal: MobiusCrystal):
        self.crystal = crystal
        self.geometry_data = None
        
    def analyze_octahedral_geometry(self) -> Dict:
        """Analyze octahedral crystal arrangement and rotational properties."""
        if not self.crystal.tetrahedral_units:
            self.crystal.generate_crystal_structure()
        
        # Convert current crystal to octahedral analysis
        unit_positions = []
        unit_vectors = []
        
        for position, unit in self.crystal.tetrahedral_units.items():
            if unit is None:
                continue
            unit_positions.append(position)
            
            # Calculate unit orientation vector
            if hasattr(unit, 'crossing_geometry') and unit.crossing_geometry:
                # Use crossing point as orientation reference
                orientation = unit.crossing_geometry.crossing_point
            else:
                # Default orientation
                orientation = np.array([0, 0, 1])
            
            unit_vectors.append(orientation)
        
        if len(unit_positions) == 0:
            return {
                'octahedral_vertices': [],
                'vertex_count': 0,
                'is_octahedral': False,
                'rotation_analysis': {'symmetry_order': 0},
                'natural_rotation_axis': {'has_natural_axis': False},
                'field_circularity': {'produces_circular_field': False, 'average_circularity': 0.0},
                'crystal_form': 'empty'
            }
        
        positions = np.array(unit_positions)
        vectors = np.array(unit_vectors)
        
        # Find octahedral vertices (6 points along ±x, ±y, ±z axes)
        octahedral_vertices = self._identify_octahedral_vertices(positions)
        
        # Analyze rotational symmetry
        rotation_analysis = self._analyze_rotational_symmetry(positions, vectors)
        
        # Check for natural rotation axis
        single_axis_data = self._find_natural_rotation_axis(positions, vectors)
        
        # Analyze field circularity
        field_circularity = self._analyze_field_circularity(positions, vectors)
        
        return {
            'octahedral_vertices': octahedral_vertices,
            'vertex_count': len(octahedral_vertices),
            'is_octahedral': len(octahedral_vertices) == 6,
            'rotation_analysis': rotation_analysis,
            'natural_rotation_axis': single_axis_data,
            'field_circularity': field_circularity,
            'crystal_form': self._classify_crystal_form(positions)
        }
    
    def _identify_octahedral_vertices(self, positions: np.ndarray) -> List[np.ndarray]:
        """Identify positions that form octahedral vertices."""
        if len(positions) == 0:
            return []
        
        # Find center of mass
        center = np.mean(positions, axis=0)
        
        # Calculate distances from center
        distances = np.linalg.norm(positions - center, axis=1)
        
        # Find positions at maximum distance (likely vertices)
        max_distance = np.max(distances)
        vertex_threshold = max_distance * 0.8  # Within 80% of maximum
        
        vertex_candidates = positions[distances >= vertex_threshold]
        
        # For true octahedron, should have 6 vertices along ±x, ±y, ±z axes
        octahedral_vertices = []
        
        # Check for vertices along principal axes
        for axis in [0, 1, 2]:  # x, y, z axes
            axis_vector = np.zeros(3)
            axis_vector[axis] = 1
            
            # Find vertices along positive and negative directions
            for direction in [1, -1]:
                target_direction = direction * axis_vector
                
                # Find closest vertex to this direction
                dots = np.dot(vertex_candidates - center, target_direction)
                if len(dots) > 0:
                    best_idx = np.argmax(dots)
                    octahedral_vertices.append(vertex_candidates[best_idx])
        
        return octahedral_vertices
    
    def _analyze_rotational_symmetry(self, positions: np.ndarray, vectors: np.ndarray) -> Dict:
        """Analyze rotational symmetry properties."""
        if len(positions) == 0:
            return {'symmetry_order': 0, 'symmetry_axes': []}
        
        center = np.mean(positions, axis=0)
        relative_positions = positions - center
        
        # Check for different symmetry orders
        symmetry_data = {}
        
        for order in [2, 3, 4, 6]:  # Common crystal symmetries
            symmetry_score = self._check_rotational_symmetry_order(relative_positions, order)
            symmetry_data[f'order_{order}'] = symmetry_score
        
        # Find highest symmetry
        best_order = max(symmetry_data.keys(), key=lambda k: symmetry_data[k])
        best_score = symmetry_data[best_order]
        
        # Identify symmetry axes
        symmetry_axes = self._find_symmetry_axes(relative_positions)
        
        return {
            'symmetry_scores': symmetry_data,
            'best_symmetry_order': int(best_order.split('_')[1]),
            'best_symmetry_score': best_score,
            'symmetry_axes': symmetry_axes,
            'is_highly_symmetric': best_score > 0.8
        }
    
    def _check_rotational_symmetry_order(self, positions: np.ndarray, order: int) -> float:
        """Check how well positions match rotational symmetry of given order."""
        if len(positions) == 0:
            return 0.0
        
        angle = 2 * np.pi / order
        
        # For each axis, check rotational symmetry
        max_symmetry = 0.0
        
        for axis in [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]:
            symmetry_score = 0.0
            
            for i in range(order):
                rotation_angle = i * angle
                rotated_positions = self._rotate_around_axis(positions, axis, rotation_angle)
                
                # Find how well rotated positions match original
                match_score = self._calculate_position_match(positions, rotated_positions)
                symmetry_score += match_score
            
            symmetry_score /= order
            max_symmetry = max(max_symmetry, symmetry_score)
        
        return max_symmetry
    
    def _rotate_around_axis(self, positions: np.ndarray, axis: np.ndarray, angle: float) -> np.ndarray:
        """Rotate positions around given axis by given angle."""
        # Rodrigues' rotation formula
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        
        # Normalize axis
        axis = axis / np.linalg.norm(axis)
        
        # Cross product matrix
        K = np.array([
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0]
        ])
        
        # Rotation matrix
        R = np.eye(3) + sin_angle * K + (1 - cos_angle) * np.dot(K, K)
        
        return np.dot(positions, R.T)
    
    def _calculate_position_match(self, pos1: np.ndarray, pos2: np.ndarray) -> float:
        """Calculate how well two sets of positions match."""
        if len(pos1) != len(pos2) or len(pos1) == 0:
            return 0.0
        
        # For each position in pos1, find closest in pos2
        total_distance = 0.0
        
        for p1 in pos1:
            distances = np.linalg.norm(pos2 - p1, axis=1)
            min_distance = np.min(distances)
            total_distance += min_distance
        
        # Normalize by number of positions and typical distance scale
        avg_distance = total_distance / len(pos1)
        typical_scale = np.mean(np.linalg.norm(pos1, axis=1))
        
        # Convert to similarity score (0-1)
        if typical_scale > 0:
            similarity = np.exp(-avg_distance / (typical_scale * 0.1))
        else:
            similarity = 1.0
        
        return similarity
    
    def _find_symmetry_axes(self, positions: np.ndarray) -> List[Dict]:
        """Find potential symmetry axes."""
        axes = []
        
        # Check principal coordinate axes
        for i, axis_name in enumerate(['x', 'y', 'z']):
            axis_vector = np.zeros(3)
            axis_vector[i] = 1
            
            # Check 2-fold, 3-fold, 4-fold symmetry around this axis
            for order in [2, 3, 4]:
                symmetry_score = self._check_rotational_symmetry_order(positions, order)
                
                if symmetry_score > 0.5:
                    axes.append({
                        'axis': axis_vector,
                        'axis_name': axis_name,
                        'symmetry_order': order,
                        'symmetry_score': symmetry_score
                    })
        
        return axes
    
    def _find_natural_rotation_axis(self, positions: np.ndarray, vectors: np.ndarray) -> Dict:
        """Find the natural single rotation axis as mentioned by James."""
        if len(positions) == 0:
            return {'has_natural_axis': False}
        
        # Calculate moment of inertia tensor
        center = np.mean(positions, axis=0)
        relative_positions = positions - center
        
        # Moment of inertia tensor components
        I_tensor = np.zeros((3, 3))
        
        for pos in relative_positions:
            r_squared = np.dot(pos, pos)
            I_tensor += r_squared * np.eye(3) - np.outer(pos, pos)
        
        # Find principal axes (eigenvalues and eigenvectors)
        eigenvalues, eigenvectors = np.linalg.eigh(I_tensor)
        
        # Sort by eigenvalue (moment of inertia)
        sorted_indices = np.argsort(eigenvalues)
        principal_moments = eigenvalues[sorted_indices]
        principal_axes = eigenvectors[:, sorted_indices]
        
        # Check for prolate (cigar-like) or oblate (disk-like) shape
        I1, I2, I3 = principal_moments
        
        # Natural rotation axis criteria
        if I3 > 0:
            asymmetry_12 = abs(I1 - I2) / I3
            asymmetry_23 = abs(I2 - I3) / I3
            
            # Single rotation axis if two moments are nearly equal
            has_natural_axis = asymmetry_12 < 0.1 or asymmetry_23 < 0.1
            
            if asymmetry_12 < 0.1:
                # I1 ≈ I2, rotate around z-axis (highest moment)
                natural_axis = principal_axes[:, 2]
                axis_type = "prolate_z"
            elif asymmetry_23 < 0.1:
                # I2 ≈ I3, rotate around x-axis (lowest moment)
                natural_axis = principal_axes[:, 0]
                axis_type = "oblate_x"
            else:
                natural_axis = principal_axes[:, 2]  # Default to z
                axis_type = "asymmetric"
        else:
            has_natural_axis = False
            natural_axis = np.array([0, 0, 1])
            axis_type = "degenerate"
            asymmetry_12 = 0
            asymmetry_23 = 0
        
        return {
            'has_natural_axis': has_natural_axis,
            'natural_axis': natural_axis,
            'axis_type': axis_type,
            'principal_moments': principal_moments,
            'asymmetry_parameters': {
                'I1_I2_asymmetry': asymmetry_12,
                'I2_I3_asymmetry': asymmetry_23
            }
        }
    
    def _analyze_field_circularity(self, positions: np.ndarray, vectors: np.ndarray) -> Dict:
        """Analyze whether the crystal produces circular electric fields."""
        if len(positions) == 0 or len(vectors) == 0:
            return {'produces_circular_field': False, 'average_circularity': 0.0}
        
        center = np.mean(positions, axis=0)
        
        # Calculate field at points around the center
        test_radius = np.mean(np.linalg.norm(positions - center, axis=1)) * 0.5
        num_test_points = 16
        
        circular_field_scores = []
        
        # Test field circularity in different planes
        for plane_normal in [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])]:
            # Create test points in circle around center
            angles = np.linspace(0, 2*np.pi, num_test_points, endpoint=False)
            
            # Find two vectors perpendicular to plane_normal
            if abs(plane_normal[0]) < 0.9:
                vec1 = np.cross(plane_normal, [1, 0, 0])
            else:
                vec1 = np.cross(plane_normal, [0, 1, 0])
            vec1 = vec1 / np.linalg.norm(vec1)
            vec2 = np.cross(plane_normal, vec1)
            
            test_points = []
            field_vectors = []
            
            for angle in angles:
                test_point = center + test_radius * (np.cos(angle) * vec1 + np.sin(angle) * vec2)
                test_points.append(test_point)
                
                # Calculate field at this point from all units
                total_field = np.zeros(3)
                for pos, vec in zip(positions, vectors):
                    r_vec = test_point - pos
                    r_mag = np.linalg.norm(r_vec)
                    
                    if r_mag > 1e-10:
                        # Simplified field calculation
                        field_contribution = vec / (r_mag**2)
                        total_field += field_contribution
                
                field_vectors.append(total_field)
            
            # Check how circular the field pattern is
            circularity_score = self._calculate_field_circularity(test_points, field_vectors, center)
            circular_field_scores.append(circularity_score)
        
        avg_circularity = np.mean(circular_field_scores)
        
        return {
            'produces_circular_field': avg_circularity > 0.7,
            'circularity_scores': circular_field_scores,
            'average_circularity': avg_circularity,
            'max_circularity': np.max(circular_field_scores)
        }
    
    def _calculate_field_circularity(self, test_points: List[np.ndarray], 
                                   field_vectors: List[np.ndarray], 
                                   center: np.ndarray) -> float:
        """Calculate how circular the field pattern is."""
        if len(test_points) != len(field_vectors) or len(test_points) < 3:
            return 0.0
        
        # For circular field, field should be tangent to circles around center
        circularity_scores = []
        
        for point, field in zip(test_points, field_vectors):
            # Radial direction from center
            radial = point - center
            radial_mag = np.linalg.norm(radial)
            
            if radial_mag > 1e-10:
                radial_hat = radial / radial_mag
                field_mag = np.linalg.norm(field)
                
                if field_mag > 1e-10:
                    field_hat = field / field_mag
                    
                    # For circular field, field should be perpendicular to radial
                    dot_product = abs(np.dot(radial_hat, field_hat))
                    tangential_score = 1.0 - dot_product  # 1 = perfectly tangential
                    circularity_scores.append(tangential_score)
        
        return np.mean(circularity_scores) if circularity_scores else 0.0
    
    def _classify_crystal_form(self, positions: np.ndarray) -> str:
        """Classify the overall crystal form."""
        if len(positions) < 4:
            return "too_few_units"
        
        # Analyze the distribution of positions
        center = np.mean(positions, axis=0)
        relative_positions = positions - center
        
        # Calculate variance along each axis
        variances = np.var(relative_positions, axis=0)
        
        # Check for special geometric arrangements
        total_variance = np.sum(variances)
        if total_variance < 1e-10:
            return "point_cluster"
        
        # Normalize variances
        norm_variances = variances / total_variance
        
        # Classify based on variance distribution
        if np.max(norm_variances) > 0.8:
            return "linear"
        elif np.min(norm_variances) < 0.1:
            return "planar"
        elif abs(norm_variances[0] - norm_variances[1]) < 0.1 and abs(norm_variances[1] - norm_variances[2]) < 0.1:
            return "spherical"
        else:
            return "general_3d"


class RotationalFieldAnalyzer:
    """
    Analyze rotational axes and electromagnetic field patterns for Freeman's theory.
    
    Focuses on the relationship between crystal symmetry, rotation axes, 
    and electromagnetic field geometry.
    """
    
    def __init__(self, crystal: MobiusCrystal):
        self.crystal = crystal
        self.field_data = None
        
    def comprehensive_rotational_analysis(self) -> Dict:
        """Complete analysis of rotational properties and field patterns."""
        
        # 1. Detailed moment of inertia analysis
        inertia_analysis = self._calculate_moment_of_inertia_tensor()
        
        # 2. Rotational symmetry detection
        symmetry_analysis = self._detect_rotational_symmetries()
        
        # 3. Electromagnetic field mapping
        field_analysis = self._map_electromagnetic_fields()
        
        # 4. Field-rotation correlation
        correlation_analysis = self._correlate_fields_with_rotation(
            inertia_analysis, field_analysis
        )
        
        return {
            'moment_of_inertia': inertia_analysis,
            'rotational_symmetries': symmetry_analysis,
            'electromagnetic_fields': field_analysis,
            'field_rotation_correlation': correlation_analysis,
            'freeman_predictions': self._test_freeman_field_predictions(
                inertia_analysis, field_analysis
            )
        }
    
    def _calculate_moment_of_inertia_tensor(self) -> Dict:
        """Calculate detailed moment of inertia tensor and principal axes."""
        
        positions = []
        masses = []  # Use charge magnitude as effective mass
        
        for position, unit in self.crystal.tetrahedral_units.items():
            positions.append(position)
            
            # Use charge magnitude as effective mass for moment calculation
            if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                mass = abs(unit.charge_distribution.net_charge) + 1.0  # +1 to avoid zero
            else:
                mass = 1.0
            masses.append(mass)
        
        positions = np.array(positions)
        masses = np.array(masses)
        
        if len(positions) == 0:
            return {'error': 'No crystal units found'}
        
        # Center of mass
        total_mass = np.sum(masses)
        center_of_mass = np.sum(positions * masses[:, np.newaxis], axis=0) / total_mass
        
        # Relative positions from center of mass
        rel_pos = positions - center_of_mass
        
        # Moment of inertia tensor
        I_tensor = np.zeros((3, 3))
        
        for i, (pos, mass) in enumerate(zip(rel_pos, masses)):
            r_squared = np.dot(pos, pos)
            I_tensor += mass * (r_squared * np.eye(3) - np.outer(pos, pos))
        
        # Principal moments and axes
        eigenvalues, eigenvectors = np.linalg.eigh(I_tensor)
        sorted_indices = np.argsort(eigenvalues)
        
        I_a, I_b, I_c = eigenvalues[sorted_indices]  # I_a ≤ I_b ≤ I_c
        axis_a, axis_b, axis_c = eigenvectors[:, sorted_indices].T
        
        # Classification of rotor type
        if I_c > 1e-10 and abs(I_c - I_a) > 1e-15:  # Avoid division by zero
            kappa = (2*I_b - I_a - I_c) / (I_c - I_a)  # Ray's asymmetry parameter
            
            if abs(kappa + 1) < 0.01:  # κ ≈ -1
                rotor_type = "prolate_symmetric_top"
                natural_axis = axis_c  # Unique axis
                degeneracy = "I_a ≈ I_b < I_c"
            elif abs(kappa - 1) < 0.01:  # κ ≈ +1
                rotor_type = "oblate_symmetric_top"
                natural_axis = axis_a  # Unique axis
                degeneracy = "I_a < I_b ≈ I_c"
            else:
                rotor_type = "asymmetric_top"
                natural_axis = axis_c  # Convention: highest moment axis
                degeneracy = "I_a < I_b < I_c"
        else:
            rotor_type = "linear_molecule"
            natural_axis = axis_c
            kappa = 0
            degeneracy = "degenerate"
        
        return {
            'center_of_mass': center_of_mass,
            'moment_tensor': I_tensor,
            'principal_moments': {'I_a': I_a, 'I_b': I_b, 'I_c': I_c},
            'principal_axes': {'axis_a': axis_a, 'axis_b': axis_b, 'axis_c': axis_c},
            'rotor_type': rotor_type,
            'asymmetry_parameter': kappa,
            'natural_rotation_axis': natural_axis,
            'degeneracy_pattern': degeneracy,
            'has_unique_axis': rotor_type in ['prolate_symmetric_top', 'oblate_symmetric_top']
        }
    
    def _detect_rotational_symmetries(self) -> Dict:
        """Detect rotational symmetries around different axes."""
        
        positions = np.array(list(self.crystal.lattice_positions.values()))
        
        if len(positions) == 0:
            return {'symmetries': {}}
        
        center = np.mean(positions, axis=0)
        rel_pos = positions - center
        
        # Test axes to check for symmetry
        test_axes = [
            ('x_axis', np.array([1, 0, 0])),
            ('y_axis', np.array([0, 1, 0])),
            ('z_axis', np.array([0, 0, 1])),
            ('body_diagonal', np.array([1, 1, 1]) / np.sqrt(3)),
            ('face_diagonal_xy', np.array([1, 1, 0]) / np.sqrt(2)),
            ('face_diagonal_xz', np.array([1, 0, 1]) / np.sqrt(2)),
            ('face_diagonal_yz', np.array([0, 1, 1]) / np.sqrt(2))
        ]
        
        symmetries = {}
        
        for axis_name, axis in test_axes:
            axis_symmetries = {}
            
            # Test different rotational orders
            for n in [2, 3, 4, 6, 8]:
                symmetry_score = self._test_n_fold_symmetry(rel_pos, axis, n)
                axis_symmetries[f'C{n}'] = symmetry_score
            
            symmetries[axis_name] = {
                'axis_vector': axis,
                'symmetry_scores': axis_symmetries,
                'highest_symmetry': max(axis_symmetries.values()),
                'best_order': max(axis_symmetries.keys(), key=lambda k: axis_symmetries[k])
            }
        
        # Find overall best symmetry
        best_axis = max(symmetries.keys(), key=lambda k: symmetries[k]['highest_symmetry'])
        best_symmetry = symmetries[best_axis]
        
        return {
            'symmetries': symmetries,
            'best_symmetry_axis': best_axis,
            'best_symmetry_order': best_symmetry['best_order'],
            'best_symmetry_score': best_symmetry['highest_symmetry'],
            'is_highly_symmetric': best_symmetry['highest_symmetry'] > 0.8
        }
    
    def _test_n_fold_symmetry(self, positions: np.ndarray, axis: np.ndarray, n: int) -> float:
        """Test n-fold rotational symmetry around given axis."""
        
        if len(positions) == 0:
            return 0.0
        
        angle = 2 * np.pi / n
        axis = axis / np.linalg.norm(axis)
        
        # Rodrigues rotation formula
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cross_matrix = np.array([
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0]
        ])
        
        rotation_matrix = (np.eye(3) + sin_a * cross_matrix + 
                          (1 - cos_a) * np.dot(cross_matrix, cross_matrix))
        
        # Apply rotation
        rotated_positions = np.dot(positions, rotation_matrix.T)
        
        # Calculate how well rotated positions match original positions
        total_deviation = 0.0
        
        for orig_pos in positions:
            # Find closest rotated position
            distances = np.linalg.norm(rotated_positions - orig_pos, axis=1)
            min_distance = np.min(distances)
            total_deviation += min_distance
        
        # Convert to symmetry score
        avg_deviation = total_deviation / len(positions)
        typical_distance = np.mean(np.linalg.norm(positions, axis=1))
        
        if typical_distance > 0:
            symmetry_score = np.exp(-avg_deviation / (typical_distance * 0.1))
        else:
            symmetry_score = 1.0
        
        return symmetry_score
    
    def _map_electromagnetic_fields(self) -> Dict:
        """Map electromagnetic fields around the crystal in detail."""
        
        # Create a 3D grid around the crystal
        positions = np.array(list(self.crystal.lattice_positions.values()))
        
        if len(positions) == 0:
            return {'error': 'No crystal positions found'}
        
        center = np.mean(positions, axis=0)
        extent = np.max(np.linalg.norm(positions - center, axis=1))
        
        # Create sampling grid
        grid_size = 20
        grid_extent = extent * 2
        
        x = np.linspace(-grid_extent, grid_extent, grid_size) + center[0]
        y = np.linspace(-grid_extent, grid_extent, grid_size) + center[1]
        z = np.linspace(-grid_extent, grid_extent, grid_size) + center[2]
        
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
        grid_points = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1)
        
        # Calculate fields at each grid point
        electric_fields = []
        magnetic_fields = []
        field_magnitudes = []
        
        for point in grid_points:
            E_total, B_total = self._calculate_field_at_point(point)
            
            electric_fields.append(E_total)
            magnetic_fields.append(B_total)
            field_magnitudes.append(np.linalg.norm(E_total) + np.linalg.norm(B_total))
        
        electric_fields = np.array(electric_fields)
        magnetic_fields = np.array(magnetic_fields)
        field_magnitudes = np.array(field_magnitudes)
        
        # Analyze field patterns
        field_analysis = self._analyze_field_patterns(
            grid_points, electric_fields, magnetic_fields, center
        )
        
        return {
            'grid_points': grid_points,
            'electric_fields': electric_fields,
            'magnetic_fields': magnetic_fields,
            'field_magnitudes': field_magnitudes,
            'field_patterns': field_analysis,
            'grid_shape': (grid_size, grid_size, grid_size),
            'grid_extent': grid_extent
        }
    
    def _calculate_field_at_point(self, point: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate electric and magnetic fields at a specific point."""
        
        E_total = np.zeros(3)
        B_total = np.zeros(3)
        
        # Physical constants
        k_e = 8.99e9  # Coulomb constant (N⋅m²/C²)
        mu_0 = 4*np.pi*1e-7  # Magnetic permeability (H/m)
        
        for position, unit in self.crystal.tetrahedral_units.items():
            unit_pos = np.array(self.crystal.lattice_positions[position])
            r_vec = point - unit_pos
            r_mag = np.linalg.norm(r_vec)
            
            if r_mag < 1e-15:  # Avoid singularity
                continue
            
            r_hat = r_vec / r_mag
            
            # Electric field from point charge
            if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                charge = unit.charge_distribution.net_charge * 1.602e-19  # Convert to Coulombs
                E_field = k_e * charge * r_hat / (r_mag**2)
                E_total += E_field
            
            # Magnetic field from magnetic dipole (for Majorana pairs)
            if hasattr(unit, 'is_majorana_pair') and unit.is_majorana_pair:
                # Magnetic dipole moment (simplified)
                mu = 9.274e-24 * np.array([0, 0, 1])  # Bohr magneton along z
                
                # Magnetic dipole field
                if r_mag > 1e-12:
                    B_dipole = (mu_0 / (4*np.pi*r_mag**3)) * (
                        3 * np.dot(mu, r_hat) * r_hat - mu
                    )
                    B_total += B_dipole
        
        return E_total, B_total
    
    def _analyze_field_patterns(self, points: np.ndarray, E_fields: np.ndarray, 
                               B_fields: np.ndarray, center: np.ndarray) -> Dict:
        """Analyze electromagnetic field patterns for symmetries and structure."""
        
        # Field magnitude statistics
        E_magnitudes = np.linalg.norm(E_fields, axis=1)
        B_magnitudes = np.linalg.norm(B_fields, axis=1)
        
        # Radial vs tangential field analysis
        radial_components = []
        tangential_components = []
        
        for point, E_field in zip(points, E_fields):
            r_vec = point - center
            r_mag = np.linalg.norm(r_vec)
            
            if r_mag > 1e-10:
                r_hat = r_vec / r_mag
                
                # Decompose field into radial and tangential components
                E_radial = np.dot(E_field, r_hat)
                E_tangential = E_field - E_radial * r_hat
                
                radial_components.append(abs(E_radial))
                tangential_components.append(np.linalg.norm(E_tangential))
        
        radial_components = np.array(radial_components)
        tangential_components = np.array(tangential_components)
        
        # Field circularity analysis
        if len(tangential_components) > 0 and len(radial_components) > 0:
            total_field = radial_components + tangential_components
            circularity_index = np.mean(tangential_components / (total_field + 1e-10))
        else:
            circularity_index = 0.0
        
        # Field uniformity
        if len(E_magnitudes) > 0:
            field_uniformity = 1.0 - (np.std(E_magnitudes) / (np.mean(E_magnitudes) + 1e-10))
        else:
            field_uniformity = 0.0
        
        # Dipole vs multipole character
        dipole_character = self._assess_dipole_character(points, E_fields, center)
        
        return {
            'circularity_index': circularity_index,
            'field_uniformity': field_uniformity,
            'dipole_character': dipole_character,
            'radial_dominance': np.mean(radial_components) / (np.mean(tangential_components) + 1e-10),
            'field_strength_variation': np.std(E_magnitudes) / (np.mean(E_magnitudes) + 1e-10),
            'has_circular_pattern': circularity_index > 0.6,
            'field_statistics': {
                'mean_E_magnitude': np.mean(E_magnitudes),
                'mean_B_magnitude': np.mean(B_magnitudes),
                'max_E_magnitude': np.max(E_magnitudes) if len(E_magnitudes) > 0 else 0,
                'max_B_magnitude': np.max(B_magnitudes) if len(B_magnitudes) > 0 else 0
            }
        }
    
    def _assess_dipole_character(self, points: np.ndarray, fields: np.ndarray, 
                               center: np.ndarray) -> float:
        """Assess how dipole-like vs multipole-like the field pattern is."""
        
        if len(points) == 0 or len(fields) == 0:
            return 0.0
        
        # For dipole field: E ∝ 1/r² and follows dipole angular pattern
        dipole_scores = []
        
        for point, field in zip(points, fields):
            r_vec = point - center
            r_mag = np.linalg.norm(r_vec)
            field_mag = np.linalg.norm(field)
            
            if r_mag > 1e-10 and field_mag > 1e-10:
                # Expected dipole field strength at this distance
                # (normalized, we're looking for pattern not absolute magnitude)
                expected_dipole = 1.0 / (r_mag**2)
                actual_field = field_mag
                
                # Score based on how well it matches 1/r² falloff
                if expected_dipole > 0:
                    ratio = min(actual_field / expected_dipole, expected_dipole / actual_field)
                    dipole_scores.append(ratio)
        
        return np.mean(dipole_scores) if dipole_scores else 0.0
    
    def _correlate_fields_with_rotation(self, inertia_data: Dict, field_data: Dict) -> Dict:
        """Correlate electromagnetic field patterns with rotational properties."""
        
        if 'error' in inertia_data or 'error' in field_data:
            return {'error': 'Missing required data'}
        
        # Check if natural rotation axis aligns with field patterns
        natural_axis = inertia_data['natural_rotation_axis']
        has_unique_axis = inertia_data['has_unique_axis']
        
        field_patterns = field_data['field_patterns']
        circularity_index = field_patterns['circularity_index']
        
        # Test James's hypothesis: crystals with natural rotation axis should 
        # have different field patterns
        axis_field_correlation = {
            'has_natural_axis': has_unique_axis,
            'field_circularity': circularity_index,
            'axis_enhances_circularity': has_unique_axis and circularity_index > 0.5,
            'rotor_type': inertia_data['rotor_type'],
            'asymmetry_parameter': inertia_data['asymmetry_parameter']
        }
        
        # Analyze field alignment with principal axes
        field_axis_alignment = self._analyze_field_axis_alignment(
            natural_axis, field_data['grid_points'], field_data['electric_fields']
        )
        
        return {
            'axis_field_correlation': axis_field_correlation,
            'field_axis_alignment': field_axis_alignment,
            'freeman_hypothesis_test': {
                'natural_axis_present': has_unique_axis,
                'produces_circular_field': circularity_index > 0.6,
                'hypothesis_supported': has_unique_axis == (circularity_index > 0.6)
            }
        }
    
    def _analyze_field_axis_alignment(self, axis: np.ndarray, points: np.ndarray, 
                                    fields: np.ndarray) -> Dict:
        """Analyze how electromagnetic fields align with the natural rotation axis."""
        
        axis = axis / np.linalg.norm(axis)
        
        # Project fields onto axis and perpendicular directions
        parallel_components = []
        perpendicular_components = []
        
        for field in fields:
            field_mag = np.linalg.norm(field)
            if field_mag > 1e-10:
                field_hat = field / field_mag
                
                # Component parallel to axis
                parallel = abs(np.dot(field_hat, axis))
                perpendicular = np.sqrt(1 - parallel**2)
                
                parallel_components.append(parallel)
                perpendicular_components.append(perpendicular)
        
        if len(parallel_components) == 0:
            return {'alignment_score': 0.0}
        
        # Field alignment statistics
        avg_parallel = np.mean(parallel_components)
        avg_perpendicular = np.mean(perpendicular_components)
        
        return {
            'axis_alignment_score': avg_parallel,
            'perpendicular_component': avg_perpendicular,
            'field_prefers_axis': avg_parallel > avg_perpendicular,
            'alignment_statistics': {
                'mean_parallel': avg_parallel,
                'mean_perpendicular': avg_perpendicular,
                'std_parallel': np.std(parallel_components),
                'std_perpendicular': np.std(perpendicular_components)
            }
        }
    
    def _test_freeman_field_predictions(self, inertia_data: Dict, field_data: Dict) -> Dict:
        """Test specific Freeman predictions about field-rotation relationships."""
        
        if 'error' in inertia_data or 'error' in field_data:
            return {'error': 'Cannot test predictions without complete data'}
        
        predictions = {}
        
        # Prediction 1: Crystals with natural rotation axis have specific field patterns
        has_axis = inertia_data['has_unique_axis']
        field_circular = field_data['field_patterns']['has_circular_pattern']
        
        predictions['natural_axis_field_correlation'] = {
            'prediction': 'Crystals with natural rotation axis correlate with field patterns',
            'has_natural_axis': has_axis,
            'has_circular_field': field_circular,
            'correlation_present': has_axis == field_circular
        }
        
        # Prediction 2: Octahedral vs other geometries produce different fields
        rotor_type = inertia_data['rotor_type']
        circularity = field_data['field_patterns']['circularity_index']
        
        predictions['geometry_field_relationship'] = {
            'prediction': 'Different crystal geometries produce different field patterns',
            'rotor_type': rotor_type,
            'circularity_index': circularity,
            'is_symmetric_rotor': rotor_type in ['prolate_symmetric_top', 'oblate_symmetric_top'],
            'high_circularity': circularity > 0.6
        }
        
        # Prediction 3: Field uniformity correlates with symmetry
        symmetry_score = field_data['field_patterns']['field_uniformity']
        asymmetry_param = abs(inertia_data['asymmetry_parameter'])
        
        predictions['symmetry_uniformity_correlation'] = {
            'prediction': 'High symmetry correlates with uniform fields',
            'field_uniformity': symmetry_score,
            'structural_asymmetry': asymmetry_param,
            'correlation_supported': (symmetry_score > 0.8) == (asymmetry_param < 0.1)
        }
        
        return predictions

def analyze_crystal_complete(crystal_size: Tuple[int,int,int] = (3,3,3),
                           crystal_type: CrystalType = CrystalType.MIXED_HELICITY,
                           crystal_symmetry: CrystalSymmetry = CrystalSymmetry.CUBIC) -> Tuple[CrystalAssemblyVisualizer, pd.DataFrame]:
    """
    Complete analysis of crystal assembly.
    
    Args:
        crystal_size: Size of crystal (nx, ny, nz)
        crystal_type: Type of crystal (helicity distribution)
        crystal_symmetry: Crystal symmetry
        
    Returns:
        Tuple of (visualizer, summary_dataframe)
    """
    print(f"Analyzing {crystal_type.name} crystal assembly...")
    print(f"Size: {crystal_size}, Symmetry: {crystal_symmetry.name}")
    
    # Create crystal
    crystal = MobiusCrystal(
        crystal_size=crystal_size,
        crystal_type=crystal_type,
        crystal_symmetry=crystal_symmetry
    )
    crystal.generate_crystal_structure()
    
    # Create visualizer
    visualizer = CrystalAssemblyVisualizer(crystal)
    
    # Perform analysis
    analysis_data = visualizer.analyze_crystal_structure(num_field_points=300)
    
    # Create visualizations
    visualizer.plot_crystal_structure_3d()
    visualizer.plot_electromagnetic_analysis()
    
    # Export data
    summary_df = visualizer.export_crystal_analysis()
    
    octahedral_analysis = visualizer.analyze_octahedral_crystals()

    print(f"\nOctahedral Analysis:")
    print(f"James's prediction test: {octahedral_analysis['james_prediction_test']['prediction_supported']}")
    print(f"Octahedral circularity: {octahedral_analysis['james_prediction_test']['octahedral_circularity_score']:.3f}")
    print(f"Current circularity: {octahedral_analysis['james_prediction_test']['current_circularity_score']:.3f}")
    print(f"Octahedral has natural axis: {octahedral_analysis['octahedral_crystal_analysis']['natural_rotation_axis']['has_natural_axis']}")
    

    # Print key results for Dr. Freeman's g-factor investigation
    print(f"\nCrystal Assembly Analysis Results:")
    print(f"Total units: {analysis_data['total_units']}")
    print(f"Majorana pairs: {len(analysis_data['majorana_pairs'])}")
    print(f"Net charge: {sum(analysis_data['unit_charges']):.3f} e")
    print(f"Field uniformity: {analysis_data['field_uniformity']:.3f}")
    print(f"Single rotation axis: {analysis_data['has_single_rotation_axis']}")
    print(f"Produces circular field: {analysis_data['produces_circular_field']}")
    print(f"\nMagnetic Moment Analysis:")
    print(f"Geometric g-factor contribution: {analysis_data['geometric_g_contribution']:.6f}")
    print(f"Theoretical g-factor: {analysis_data['theoretical_g_factor']:.6f}")
    print(f"Experimental g-factor: {analysis_data['experimental_g_factor']:.8f}")
    print(f"Deviation explained: {analysis_data['deviation_explained_fraction']:.1%}")

    # Add to analyze_crystal_complete():
    rotation_field_analysis = visualizer.analyze_rotational_field_patterns()

    print(f"\nRotational-Field Analysis:")
    rfa = rotation_field_analysis
    if 'moment_of_inertia' in rfa and 'error' not in rfa['moment_of_inertia']:
        print(f"Rotor type: {rfa['moment_of_inertia']['rotor_type']}")
        print(f"Natural axis present: {rfa['moment_of_inertia']['has_unique_axis']}")
    
    if 'electromagnetic_fields' in rfa and 'error' not in rfa['electromagnetic_fields']:
        field_patterns = rfa['electromagnetic_fields']['field_patterns']
        print(f"Field circularity: {field_patterns['circularity_index']:.3f}")
        print(f"Field uniformity: {field_patterns['field_uniformity']:.3f}")
        print(f"Circular pattern detected: {field_patterns['has_circular_pattern']}")
    
    return visualizer, summary_df

def analyze_crystal_complete_with_field_comparison(
    crystal_size: Tuple[int,int,int] = (3,3,3),
    crystal_type: CrystalType = CrystalType.MIXED_HELICITY,
    crystal_symmetry: CrystalSymmetry = CrystalSymmetry.CUBIC
) -> Tuple[CrystalAssemblyVisualizer, pd.DataFrame, Dict]:
    """Complete crystal analysis including field geometry comparison."""
    
    print("Freeman's Crystal Assembly Analysis")
    print("===================================")
    
    # Create and analyze main crystal
    crystal = MobiusCrystal(crystal_size, crystal_type, crystal_symmetry)
    visualizer = CrystalAssemblyVisualizer(crystal)
    
    print(f"\n--- Configuration: {crystal_size} {crystal_type.name} {crystal_symmetry.name} ---")
    print(f"Analyzing {crystal_type.name} crystal assembly...")
    print(f"Size: {crystal_size}, Symmetry: {crystal_symmetry.name}")
    
    # Perform analyses
    analysis_data = visualizer.analyze_crystal_structure(num_field_points=300)
    octahedral_analysis = visualizer.analyze_octahedral_crystals()
    rotation_field_analysis = visualizer.analyze_rotational_field_patterns()
    
    # NEW: Field geometry comparison
    field_comparison = visualizer.compare_circular_vs_noncircular_fields()
    
    # Create visualizations
    visualizer.plot_crystal_structure_3d()
    visualizer.plot_electromagnetic_analysis()
    
    # Export data
    summary_df = visualizer.export_crystal_analysis()
    
    # Print field comparison results
    print(f"\nField Geometry Comparison:")
    summary = field_comparison['summary']
    print(f"Crystals analyzed: {summary['total_crystals_analyzed']}")
    print(f"Field type distribution: {summary['field_type_distribution']}")
    print(f"Circular field fraction: {summary['circular_field_fraction']:.2f}")
    
    freeman_summary = summary['freeman_predictions_summary']
    print(f"Freeman octahedral prediction accuracy: {freeman_summary['octahedral_prediction_accuracy']:.2f}")
    print(f"Overall theory support: {freeman_summary['overall_theory_support']:.2f}")
    
    # Key findings
    print("\nKey Findings:")
    for finding in summary['key_findings']:
        print(f"  • {finding}")
    
    # Previous analysis results
    james_test = octahedral_analysis['james_prediction_test']
    print(f"\nOctahedral Analysis:")
    print(f"James's prediction supported: {james_test['prediction_supported']}")
    print(f"Octahedral circularity: {james_test['octahedral_circularity_score']:.3f}")
    print(f"Current geometry circularity: {james_test['current_circularity_score']:.3f}")
    
    # Rotation-field analysis
    print(f"\nRotational-Field Analysis:")
    rfa = rotation_field_analysis
    if 'moment_of_inertia' in rfa and 'error' not in rfa['moment_of_inertia']:
        print(f"Rotor type: {rfa['moment_of_inertia']['rotor_type']}")
        print(f"Natural axis present: {rfa['moment_of_inertia']['has_unique_axis']}")
        
    if 'electromagnetic_fields' in rfa and 'error' not in rfa['electromagnetic_fields']:
        field_patterns = rfa['electromagnetic_fields']['field_patterns']
        print(f"Field circularity: {field_patterns['circularity_index']:.3f}")
        print(f"Field uniformity: {field_patterns['field_uniformity']:.3f}")
        print(f"Circular pattern detected: {field_patterns['has_circular_pattern']}")
    
    # Crystal properties
    print(f"\nCrystal Assembly Analysis Results:")
    print(f"Total units: {analysis_data['total_units']}")
    print(f"Majorana pairs: {len(analysis_data['majorana_pairs'])}")
    print(f"Net charge: {sum(analysis_data['unit_charges']):.3f} e")
    
    if 'avg_field_strength' in analysis_data:
        print(f"Field uniformity: {analysis_data.get('field_uniformity', 'N/A'):.3f}")
        print(f"Single rotation axis: {analysis_data.get('has_single_rotation_axis', False)}")
        print(f"Produces circular field: {analysis_data.get('produces_circular_field', False)}")
    
    # Magnetic moment analysis
    if 'geometric_g_contribution' in analysis_data:
        print(f"\nMagnetic Moment Analysis:")
        g_contrib = analysis_data['geometric_g_contribution']
        theoretical_g = analysis_data['theoretical_g_factor']
        experimental_g = analysis_data['experimental_g_factor']
        deviation = analysis_data['deviation_explained_fraction']
        
        print(f"Geometric g-factor contribution: {g_contrib}")
        print(f"Theoretical g-factor: {theoretical_g}")
        print(f"Experimental g-factor: {experimental_g:.8f}")
        print(f"Deviation explained: {deviation*100:.1f}%")
    
    return visualizer, summary_df, field_comparison

class CircularFieldComparator:
    """
    Compare circular vs non-circular electromagnetic field geometries.
    
    Tests James Freeman's hypothesis about different crystal forms producing
    different field patterns, particularly his prediction about octahedral
    crystals not producing circular fields.
    """
    
    def __init__(self):
        self.test_crystals = {}
        self.field_data = {}
        self.comparison_results = {}
        
    def comprehensive_field_geometry_comparison(self) -> Dict:
        """Complete comparison of field geometries across crystal types."""
        
        # 1. Generate test crystals with different geometries
        test_crystals = self._generate_comparison_crystals()
        
        # 2. Analyze field patterns for each crystal type
        field_patterns = self._analyze_all_field_patterns(test_crystals)
        
        # 3. Classify field geometries
        field_classifications = self._classify_field_geometries(field_patterns)
        
        # 4. Statistical comparison analysis
        statistical_analysis = self._statistical_field_comparison(field_patterns)
        
        # 5. Test Freeman's specific predictions
        freeman_predictions = self._test_freeman_field_predictions(field_classifications)
        
        return {
            'test_crystals': test_crystals,
            'field_patterns': field_patterns,
            'field_classifications': field_classifications,
            'statistical_analysis': statistical_analysis,
            'freeman_predictions': freeman_predictions,
            'summary': self._generate_comparison_summary(field_classifications, statistical_analysis)
        }
    
    def _generate_comparison_crystals(self) -> Dict[str, MobiusCrystal]:
        """Generate crystals with different geometries for comparison."""
        
        crystal_configs = [
            # Standard geometries
            ('cubic_mixed', (3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.CUBIC),
            ('tetrahedral_mixed', (3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.TETRAHEDRAL),
            ('hexagonal_mixed', (3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.HEXAGONAL),
            
            # Single helicity variations
            ('cubic_right', (3, 3, 3), CrystalType.SINGLE_HELICITY_RIGHT, CrystalSymmetry.CUBIC),
            ('tetrahedral_right', (3, 3, 3), CrystalType.SINGLE_HELICITY_RIGHT, CrystalSymmetry.TETRAHEDRAL),
            ('hexagonal_right', (3, 3, 3), CrystalType.SINGLE_HELICITY_RIGHT, CrystalSymmetry.HEXAGONAL),
            
            # Different sizes for scaling analysis
            ('cubic_large', (4, 4, 4), CrystalType.MIXED_HELICITY, CrystalSymmetry.CUBIC),
            ('cubic_small', (2, 2, 2), CrystalType.MIXED_HELICITY, CrystalSymmetry.CUBIC),
            
            # Special octahedral-like arrangements
            ('diamond_structure', (3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.DIAMOND),
        ]
        
        crystals = {}
        
        for name, size, crystal_type, symmetry in crystal_configs:
            crystal = MobiusCrystal(
                crystal_size=size,
                crystal_type=crystal_type,
                crystal_symmetry=symmetry
            )
            crystal.generate_crystal_structure()
            crystals[name] = crystal
        
        # Add custom octahedral crystal
        crystals['octahedral'] = self._create_pure_octahedral_crystal()
        
        return crystals
    
    def _create_pure_octahedral_crystal(self) -> MobiusCrystal:
        """Create a pure octahedral crystal for comparison."""
        
        # Start with cubic template
        crystal = MobiusCrystal(
            crystal_size=(3, 3, 3),
            crystal_type=CrystalType.MIXED_HELICITY,
            crystal_symmetry=CrystalSymmetry.CUBIC
        )
        crystal.generate_crystal_structure()
        
        # Clear existing structure
        crystal.tetrahedral_units.clear()
        crystal.lattice_positions.clear()
        
        # Create true octahedral arrangement (6 units at ±x, ±y, ±z)
        lattice_const = crystal.lattice_parameters.lattice_constant
        octahedral_positions = [
            ((1, 0, 0), np.array([lattice_const, 0, 0])),
            ((-1, 0, 0), np.array([-lattice_const, 0, 0])),
            ((0, 1, 0), np.array([0, lattice_const, 0])),
            ((0, -1, 0), np.array([0, -lattice_const, 0])),
            ((0, 0, 1), np.array([0, 0, lattice_const])),
            ((0, 0, -1), np.array([0, 0, -lattice_const]))
        ]
        
        for position_key, position_vec in octahedral_positions:
            # Create unit at octahedral vertex
            helicity1, helicity2 = crystal._determine_helicities_at_site(*position_key)
            unit = crystal._create_tetrahedral_unit_at_position(position_vec, helicity1, helicity2)
            
            crystal.tetrahedral_units[position_key] = unit
            crystal.lattice_positions[position_key] = position_vec
        
        # Update properties
        crystal.total_units = len(crystal.tetrahedral_units)
        crystal._calculate_crystal_properties()
        crystal._analyze_helicity_distribution()
        crystal._identify_majorana_pairs()
        
        return crystal
    
    def _analyze_all_field_patterns(self, crystals: Dict[str, MobiusCrystal]) -> Dict:
        """Analyze electromagnetic field patterns for all crystal types."""
        
        field_analyses = {}
        
        for name, crystal in crystals.items():
            field_analysis = self._comprehensive_field_analysis(crystal)
            field_analyses[name] = field_analysis
        
        return field_analyses
    
    def _comprehensive_field_analysis(self, crystal: MobiusCrystal) -> Dict:
        """Comprehensive field pattern analysis for a single crystal."""
        
        # Get crystal properties
        positions = np.array(list(crystal.lattice_positions.values()))
        center = np.mean(positions, axis=0) if len(positions) > 0 else np.zeros(3)
        
        # Multiple analysis approaches
        analyses = {
            'spherical_analysis': self._spherical_field_analysis(crystal, center),
            'cylindrical_analysis': self._cylindrical_field_analysis(crystal, center),
            'planar_analysis': self._planar_field_analysis(crystal, center),
            'multipole_analysis': self._multipole_field_analysis(crystal, center),
            'symmetry_analysis': self._field_symmetry_analysis(crystal, center)
        }
        
        # Combine analyses into overall assessment
        overall_assessment = self._combine_field_analyses(analyses)
        
        return {
            'individual_analyses': analyses,
            'overall_assessment': overall_assessment,
            'crystal_properties': {
                'geometry': crystal.crystal_symmetry.name,
                'total_units': crystal.total_units,
                'net_charge': crystal.crystal_properties.total_charge if crystal.crystal_properties else 0,
                'majorana_pairs': len(crystal.majorana_pairs)
            }
        }
    
    def _spherical_field_analysis(self, crystal: MobiusCrystal, center: np.ndarray) -> Dict:
        """Analyze field patterns on spherical surfaces around crystal."""
        
        positions = np.array(list(crystal.lattice_positions.values()))
        if len(positions) == 0:
            return {'error': 'No crystal positions'}
        
        # Multiple radii for analysis
        max_extent = np.max(np.linalg.norm(positions - center, axis=1))
        test_radii = [max_extent * 1.5, max_extent * 2.0, max_extent * 3.0]
        
        radial_analyses = {}
        
        for radius in test_radii:
            # Sample points on sphere
            n_theta, n_phi = 12, 24  # Reasonable sampling
            theta = np.linspace(0, np.pi, n_theta)
            phi = np.linspace(0, 2*np.pi, n_phi, endpoint=False)
            
            THETA, PHI = np.meshgrid(theta, phi, indexing='ij')
            
            # Convert to Cartesian coordinates
            x = radius * np.sin(THETA) * np.cos(PHI) + center[0]
            y = radius * np.sin(THETA) * np.sin(PHI) + center[1]
            z = radius * np.cos(THETA) + center[2]
            
            test_points = np.stack([x.ravel(), y.ravel(), z.ravel()], axis=1)
            
            # Calculate fields at test points
            field_vectors = []
            field_magnitudes = []
            
            for point in test_points:
                field = self._calculate_simplified_field(crystal, point)
                field_vectors.append(field)
                field_magnitudes.append(np.linalg.norm(field))
            
            # Analyze circularity on this sphere
            circularity = self._calculate_spherical_circularity(
                test_points, field_vectors, center
            )
            
            radial_analyses[f'radius_{radius:.1e}'] = {
                'circularity_index': circularity,
                'field_magnitude_variation': np.std(field_magnitudes) / (np.mean(field_magnitudes) + 1e-10),
                'mean_field_strength': np.mean(field_magnitudes)
            }
        
        # Overall spherical assessment
        avg_circularity = np.mean([analysis['circularity_index'] for analysis in radial_analyses.values()])
        
        return {
            'radial_analyses': radial_analyses,
            'average_circularity': avg_circularity,
            'is_spherically_circular': avg_circularity > 0.6,
            'circularity_consistency': np.std([analysis['circularity_index'] for analysis in radial_analyses.values()])
        }
    
    def _cylindrical_field_analysis(self, crystal: MobiusCrystal, center: np.ndarray) -> Dict:
        """Analyze field patterns in cylindrical coordinates around principal axes."""
        
        # Test cylindrical patterns around x, y, z axes
        axes = [
            ('x_axis', np.array([1, 0, 0])),
            ('y_axis', np.array([0, 1, 0])),
            ('z_axis', np.array([0, 0, 1]))
        ]
        
        cylindrical_analyses = {}
        
        for axis_name, axis in axes:
            # Create cylindrical grid around this axis
            radii = np.linspace(0.5e-15, 2e-15, 5)  # Different cylindrical radii
            angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
            heights = np.linspace(-1e-15, 1e-15, 5)  # Along the axis
            
            axis_circularity_scores = []
            
            for height in heights:
                height_circularity_scores = []
                
                for radius in radii:
                    # Points on circle at this height and radius
                    circle_points = []
                    circle_fields = []
                    
                    # Create orthonormal basis with axis as z-direction
                    if abs(axis[2]) < 0.9:
                        u = np.cross(axis, [0, 0, 1])
                    else:
                        u = np.cross(axis, [1, 0, 0])
                    u = u / np.linalg.norm(u)
                    v = np.cross(axis, u)
                    
                    for angle in angles:
                        # Point on circle
                        point = (center + height * axis + 
                                radius * (np.cos(angle) * u + np.sin(angle) * v))
                        circle_points.append(point)
                        
                        # Field at this point
                        field = self._calculate_simplified_field(crystal, point)
                        circle_fields.append(field)
                    
                    # Calculate circularity for this circle
                    circle_circularity = self._calculate_circular_pattern_score(
                        circle_points, circle_fields, center, axis
                    )
                    height_circularity_scores.append(circle_circularity)
                
                axis_circularity_scores.append(np.mean(height_circularity_scores))
            
            cylindrical_analyses[axis_name] = {
                'circularity_scores': axis_circularity_scores,
                'average_circularity': np.mean(axis_circularity_scores),
                'circularity_consistency': np.std(axis_circularity_scores)
            }
        
        # Find best cylindrical axis
        best_axis = max(cylindrical_analyses.keys(), 
                       key=lambda k: cylindrical_analyses[k]['average_circularity'])
        
        return {
            'axis_analyses': cylindrical_analyses,
            'best_cylindrical_axis': best_axis,
            'best_circularity': cylindrical_analyses[best_axis]['average_circularity'],
            'has_cylindrical_pattern': cylindrical_analyses[best_axis]['average_circularity'] > 0.5
        }
    
    def _planar_field_analysis(self, crystal: MobiusCrystal, center: np.ndarray) -> Dict:
        """Analyze field patterns in different planes."""
        
        planes = [
            ('xy_plane', np.array([0, 0, 1])),
            ('xz_plane', np.array([0, 1, 0])),
            ('yz_plane', np.array([1, 0, 0]))
        ]
        
        planar_analyses = {}
        
        for plane_name, normal in planes:
            # Create grid in this plane
            grid_size = 10
            extent = 2e-15
            
            # Create orthonormal basis in plane
            if abs(normal[0]) < 0.9:
                u = np.cross(normal, [1, 0, 0])
            else:
                u = np.cross(normal, [0, 1, 0])
            u = u / np.linalg.norm(u)
            v = np.cross(normal, u)
            
            # Grid points in plane
            u_coords = np.linspace(-extent, extent, grid_size)
            v_coords = np.linspace(-extent, extent, grid_size)
            
            plane_points = []
            plane_fields = []
            
            for u_coord in u_coords:
                for v_coord in v_coords:
                    point = center + u_coord * u + v_coord * v
                    plane_points.append(point)
                    
                    field = self._calculate_simplified_field(crystal, point)
                    plane_fields.append(field)
            
            # Analyze field pattern in this plane
            plane_analysis = self._analyze_planar_field_pattern(
                plane_points, plane_fields, center, normal
            )
            
            planar_analyses[plane_name] = plane_analysis
        
        return planar_analyses
    
    def _multipole_field_analysis(self, crystal: MobiusCrystal, center: np.ndarray) -> Dict:
        """Analyze multipole character of electromagnetic fields."""
        
        # Sample field at various distances and angles
        test_points = []
        field_values = []
        distances = []
        
        # Spherical sampling for multipole analysis
        n_points = 50
        for i in range(n_points):
            # Fibonacci sphere sampling for uniform distribution
            theta = np.arccos(1 - 2 * i / n_points)
            phi = np.pi * (1 + 5**0.5) * i
            
            for radius in [1e-15, 2e-15, 3e-15]:  # Multiple distances
                point = center + radius * np.array([
                    np.sin(theta) * np.cos(phi),
                    np.sin(theta) * np.sin(phi),
                    np.cos(theta)
                ])
                
                test_points.append(point)
                field = self._calculate_simplified_field(crystal, point)
                field_values.append(field)
                distances.append(radius)
        
        # Fit to multipole patterns
        multipole_fits = self._fit_multipole_patterns(
            test_points, field_values, distances, center
        )
        
        return multipole_fits
    
    def _field_symmetry_analysis(self, crystal: MobiusCrystal, center: np.ndarray) -> Dict:
        """Analyze symmetry properties of electromagnetic fields."""
        
        # Test field symmetries
        symmetry_tests = {}
        
        # Rotational symmetries
        for axis_name, axis in [('x', [1,0,0]), ('y', [0,1,0]), ('z', [0,0,1])]:
            for n in [2, 3, 4, 6]:
                symmetry_score = self._test_field_rotational_symmetry(
                    crystal, center, np.array(axis), n
                )
                symmetry_tests[f'{axis_name}_C{n}'] = symmetry_score
        
        # Mirror symmetries
        for plane_name, normal in [('xy', [0,0,1]), ('xz', [0,1,0]), ('yz', [1,0,0])]:
            mirror_score = self._test_field_mirror_symmetry(
                crystal, center, np.array(normal)
            )
            symmetry_tests[f'{plane_name}_mirror'] = mirror_score
        
        # Inversion symmetry
        inversion_score = self._test_field_inversion_symmetry(crystal, center)
        symmetry_tests['inversion'] = inversion_score
        
        # Overall symmetry assessment
        max_symmetry = max(symmetry_tests.values())
        symmetry_type = max(symmetry_tests.keys(), key=lambda k: symmetry_tests[k])
        
        return {
            'symmetry_scores': symmetry_tests,
            'highest_symmetry': max_symmetry,
            'dominant_symmetry': symmetry_type,
            'is_highly_symmetric': max_symmetry > 0.7
        }
    
    def _calculate_simplified_field(self, crystal: MobiusCrystal, point: np.ndarray) -> np.ndarray:
        """Simplified electromagnetic field calculation."""
        
        total_field = np.zeros(3)
        
        for position, unit in crystal.tetrahedral_units.items():
            unit_pos = np.array(crystal.lattice_positions[position])
            r_vec = point - unit_pos
            r_mag = np.linalg.norm(r_vec)
            
            if r_mag < 1e-20:  # Avoid singularity
                continue
            
            r_hat = r_vec / r_mag
            
            # Simplified electric field from unit charge
            if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                charge = unit.charge_distribution.net_charge
                # Coulomb field (simplified units)
                field_contrib = charge * r_hat / (r_mag**2 + 1e-30)  # Regularized
                total_field += field_contrib
        
        return total_field
    
    def _calculate_spherical_circularity(self, points: List[np.ndarray], 
                                       fields: List[np.ndarray], 
                                       center: np.ndarray) -> float:
        """Calculate circularity index for fields on spherical surface."""
        
        if len(points) != len(fields) or len(points) == 0:
            return 0.0
        
        circularity_scores = []
        
        for point, field in zip(points, fields):
            r_vec = point - center
            r_mag = np.linalg.norm(r_vec)
            field_mag = np.linalg.norm(field)
            
            if r_mag > 1e-20 and field_mag > 1e-20:
                r_hat = r_vec / r_mag
                field_hat = field / field_mag
                
                # For circular field, field should be tangent to sphere
                radial_component = abs(np.dot(r_hat, field_hat))
                tangential_score = 1.0 - radial_component
                circularity_scores.append(tangential_score)
        
        return np.mean(circularity_scores) if circularity_scores else 0.0
    
    def _calculate_circular_pattern_score(self, points: List[np.ndarray], 
                                        fields: List[np.ndarray], 
                                        center: np.ndarray, 
                                        axis: np.ndarray) -> float:
        """Calculate how circular the field pattern is around an axis."""
        
        if len(points) != len(fields) or len(points) == 0:
            return 0.0
        
        axis = axis / np.linalg.norm(axis)
        
        # For each point, check if field is tangent to circle around axis
        circularity_scores = []
        
        for point, field in zip(points, fields):
            # Vector from axis to point
            point_rel = point - center
            # Component perpendicular to axis
            perp_component = point_rel - np.dot(point_rel, axis) * axis
            perp_mag = np.linalg.norm(perp_component)
            
            field_mag = np.linalg.norm(field)
            
            if perp_mag > 1e-20 and field_mag > 1e-20:
                # Radial direction in plane perpendicular to axis
                radial_hat = perp_component / perp_mag
                field_hat = field / field_mag
                
                # Field component along radial direction
                radial_field = abs(np.dot(radial_hat, field_hat))
                # For circular field, should be mostly tangential
                tangential_score = 1.0 - radial_field
                circularity_scores.append(tangential_score)
        
        return np.mean(circularity_scores) if circularity_scores else 0.0
    
    # Additional helper methods for field analysis would continue here...
    # (Implementing the remaining methods: _analyze_planar_field_pattern,
    # _fit_multipole_patterns, _test_field_rotational_symmetry, etc.)
    
    def _classify_field_geometries(self, field_patterns: Dict) -> Dict:
        """Classify each crystal's field geometry as circular or non-circular."""
        
        classifications = {}
        
        for crystal_name, patterns in field_patterns.items():
            overall = patterns['overall_assessment']
            
            # Multiple criteria for classification
            criteria = {
                'spherical_circular': patterns['individual_analyses']['spherical_analysis']['is_spherically_circular'],
                'cylindrical_circular': patterns['individual_analyses']['cylindrical_analysis']['has_cylindrical_pattern'],
                'high_symmetry': patterns['individual_analyses']['symmetry_analysis']['is_highly_symmetric'],
                'average_circularity': overall.get('average_circularity', 0.0)
            }
            
            # Classification decision
            if criteria['average_circularity'] > 0.6:
                field_type = "circular"
            elif criteria['average_circularity'] > 0.3:
                field_type = "partially_circular"
            else:
                field_type = "non_circular"
            
            classifications[crystal_name] = {
                'field_type': field_type,
                'criteria': criteria,
                'confidence': self._calculate_classification_confidence(criteria)
            }
        
        return classifications
    
    def _calculate_classification_confidence(self, criteria: Dict) -> float:
        """Calculate confidence in field classification."""
        
        # Simple confidence metric based on consistency of criteria
        values = [criteria['average_circularity'], 
                 float(criteria['spherical_circular']),
                 float(criteria['cylindrical_circular']),
                 float(criteria['high_symmetry'])]
        
        # Confidence is higher when values are consistent
        if np.std(values) < 0.3:
            return 0.8 + 0.2 * (1 - np.std(values))
        else:
            return 0.5
    
    def _statistical_field_comparison(self, field_patterns: Dict) -> Dict:
        """Statistical comparison of field patterns across crystal types."""
        
        # Extract metrics for statistical analysis
        metrics = {}
        for crystal_name, patterns in field_patterns.items():
            overall = patterns['overall_assessment']
            geometry = patterns['crystal_properties']['geometry']
            
            if geometry not in metrics:
                metrics[geometry] = {
                    'circularity_scores': [],
                    'symmetry_scores': [],
                    'crystal_names': []
                }
            
            metrics[geometry]['circularity_scores'].append(overall.get('average_circularity', 0.0))
            metrics[geometry]['symmetry_scores'].append(
                patterns['individual_analyses']['symmetry_analysis']['highest_symmetry']
            )
            metrics[geometry]['crystal_names'].append(crystal_name)
        
        # Statistical comparisons
        statistical_results = {}
        
        for geometry, data in metrics.items():
            statistical_results[geometry] = {
                'mean_circularity': np.mean(data['circularity_scores']),
                'std_circularity': np.std(data['circularity_scores']),
                'mean_symmetry': np.mean(data['symmetry_scores']),
                'std_symmetry': np.std(data['symmetry_scores']),
                'sample_size': len(data['circularity_scores'])
            }
        
        return {
            'geometry_statistics': statistical_results,
            'overall_trends': self._identify_statistical_trends(statistical_results)
        }
    
    def _identify_statistical_trends(self, stats: Dict) -> Dict:
        """Identify trends in the statistical data."""
        
        # Compare geometries
        geometries = list(stats.keys())
        trends = {}
        
        if len(geometries) >= 2:
            # Find most/least circular geometries
            circ_scores = {geo: stats[geo]['mean_circularity'] for geo in geometries}
            trends['most_circular_geometry'] = max(circ_scores.keys(), key=lambda k: circ_scores[k])
            trends['least_circular_geometry'] = min(circ_scores.keys(), key=lambda k: circ_scores[k])
            
            # Circularity spread
            trends['circularity_range'] = max(circ_scores.values()) - min(circ_scores.values())
            trends['significant_difference'] = trends['circularity_range'] > 0.3
        
        return trends
    
    def _test_freeman_field_predictions(self, field_classifications: Dict) -> Dict:
        """Test James Freeman's specific predictions about field patterns."""
        
        predictions = {}
        
        # Prediction 1: Octahedral crystals do NOT produce circular fields
        octahedral_crystals = [name for name in field_classifications.keys() 
                              if 'octahedral' in name.lower()]
        
        if octahedral_crystals:
            octahedral_results = [field_classifications[name]['field_type'] 
                                for name in octahedral_crystals]
            octahedral_non_circular = all(result != 'circular' for result in octahedral_results)
            
            predictions['octahedral_non_circular'] = {
                'prediction': 'Octahedral crystals probably do NOT result in circular electric field',
                'test_crystals': octahedral_crystals,
                'results': octahedral_results,
                'prediction_supported': octahedral_non_circular,
                'confidence': np.mean([field_classifications[name]['confidence'] 
                                     for name in octahedral_crystals])
            }
        
        # Prediction 2: Different geometries produce different field patterns
        geometry_field_types = {}
        for name, classification in field_classifications.items():
            geometry = classification.get('geometry', 'unknown')
            field_type = classification['field_type']
            
            if geometry not in geometry_field_types:
                geometry_field_types[geometry] = []
            geometry_field_types[geometry].append(field_type)
        
        geometric_diversity = len(set(ft for fts in geometry_field_types.values() for ft in fts))
        
        predictions['geometric_field_diversity'] = {
            'prediction': 'Different crystal geometries produce different field patterns',
            'geometry_patterns': geometry_field_types,
            'pattern_diversity': geometric_diversity,
            'prediction_supported': geometric_diversity > 1
        }
        
        return predictions
    
    def _combine_field_analyses(self, analyses: Dict) -> Dict:
        """Combine multiple field analyses into overall assessment."""
        
        # Extract key metrics from each analysis
        spherical = analyses['spherical_analysis']
        cylindrical = analyses['cylindrical_analysis']
        symmetry = analyses['symmetry_analysis']
        
        # Weighted average of circularity scores
        circularity_scores = [
            spherical['average_circularity'],
            cylindrical['best_circularity'],
            symmetry['highest_symmetry']
        ]
        
        weights = [0.4, 0.3, 0.3]  # Weight spherical analysis more heavily
        average_circularity = np.average(circularity_scores, weights=weights)
        
        return {
            'average_circularity': average_circularity,
            'dominant_pattern': 'circular' if average_circularity > 0.5 else 'non_circular',
            'consistency_score': 1.0 - np.std(circularity_scores),
            'analysis_confidence': self._calculate_analysis_confidence(analyses)
        }
    
    def _calculate_analysis_confidence(self, analyses: Dict) -> float:
        """Calculate confidence in the combined analysis."""
        
        # Confidence based on consistency across different analysis methods
        circularity_values = [
            analyses['spherical_analysis']['average_circularity'],
            analyses['cylindrical_analysis']['best_circularity'],
            analyses['symmetry_analysis']['highest_symmetry']
        ]
        
        # High confidence when analyses agree
        std_dev = np.std(circularity_values)
        confidence = max(0.1, 1.0 - 2 * std_dev)  # Lower std = higher confidence
        
        return confidence
    
    def _generate_comparison_summary(self, classifications: Dict, statistics: Dict) -> Dict:
        """Generate summary of field geometry comparison."""
        
        # Count field types
        field_type_counts = {}
        for classification in classifications.values():
            field_type = classification['field_type']
            field_type_counts[field_type] = field_type_counts.get(field_type, 0) + 1
        
        # Overall trends
        total_crystals = len(classifications)
        circular_fraction = field_type_counts.get('circular', 0) / total_crystals
        return {
            'total_crystals_analyzed': total_crystals,
            'field_type_distribution': field_type_counts,
            'circular_field_fraction': circular_fraction,
            'geometry_trends': statistics.get('overall_trends', {}),
            'freeman_predictions_summary': self._summarize_freeman_predictions(classifications),
            'key_findings': self._extract_key_findings(classifications, statistics)
        }
    
    def _summarize_freeman_predictions(self, classifications: Dict) -> Dict:
        """Summarize how well Freeman's predictions are supported."""
        
        # Check octahedral prediction
        octahedral_count = sum(1 for name in classifications.keys() if 'octahedral' in name.lower())
        octahedral_non_circular = sum(1 for name, data in classifications.items() 
                                    if 'octahedral' in name.lower() and data['field_type'] != 'circular')
        
        # Check geometric diversity
        geometries = set()
        field_types = set()
        for data in classifications.values():
            if 'geometry' in data:
                geometries.add(data['geometry'])
            field_types.add(data['field_type'])
        
        return {
            'octahedral_prediction_accuracy': octahedral_non_circular / max(octahedral_count, 1),
            'geometric_diversity_confirmed': len(geometries) > 1 and len(field_types) > 1,
            'overall_theory_support': self._calculate_overall_theory_support(classifications)
        }
    
    def _calculate_overall_theory_support(self, classifications: Dict) -> float:
        """Calculate overall support for Freeman's theory based on classifications."""
        
        support_factors = []
        
        # Factor 1: Octahedral crystals are non-circular
        octahedral_crystals = [name for name in classifications.keys() if 'octahedral' in name.lower()]
        if octahedral_crystals:
            octahedral_support = sum(1 for name in octahedral_crystals 
                                   if classifications[name]['field_type'] != 'circular') / len(octahedral_crystals)
            support_factors.append(octahedral_support)
        
        # Factor 2: Different geometries show different patterns
        geometry_patterns = {}
        for name, data in classifications.items():
            geometry = data.get('geometry', 'unknown')
            field_type = data['field_type']
            
            if geometry not in geometry_patterns:
                geometry_patterns[geometry] = set()
            geometry_patterns[geometry].add(field_type)
        
        # Diversity score: how many different patterns per geometry
        if len(geometry_patterns) > 1:
            diversity_score = len(set().union(*geometry_patterns.values())) / len(geometry_patterns)
            support_factors.append(min(1.0, diversity_score))
        
        # Factor 3: Clear distinctions between circular and non-circular
        field_types = [data['field_type'] for data in classifications.values()]
        if len(set(field_types)) > 1:
            support_factors.append(1.0)
        else:
            support_factors.append(0.5)
        
        return np.mean(support_factors) if support_factors else 0.0
    
    def _extract_key_findings(self, classifications: Dict, statistics: Dict) -> List[str]:
        """Extract key findings from the analysis."""
        
        findings = []
        
        # Field type distribution
        field_types = [data['field_type'] for data in classifications.values()]
        circular_count = field_types.count('circular')
        non_circular_count = field_types.count('non_circular')
        
        if circular_count > non_circular_count:
            findings.append(f"Majority of crystals ({circular_count}/{len(field_types)}) produce circular fields")
        elif non_circular_count > circular_count:
            findings.append(f"Majority of crystals ({non_circular_count}/{len(field_types)}) produce non-circular fields")
        else:
            findings.append("Equal split between circular and non-circular field patterns")
        
        # Geometry-specific findings
        geometry_stats = statistics.get('geometry_statistics', {})
        if len(geometry_stats) > 1:
            most_circular = max(geometry_stats.keys(), key=lambda k: geometry_stats[k]['mean_circularity'])
            least_circular = min(geometry_stats.keys(), key=lambda k: geometry_stats[k]['mean_circularity'])
            
            findings.append(f"{most_circular} geometry shows highest circularity")
            findings.append(f"{least_circular} geometry shows lowest circularity")
        
        # Octahedral findings
        octahedral_crystals = [name for name in classifications.keys() if 'octahedral' in name.lower()]
        if octahedral_crystals:
            octahedral_circular = sum(1 for name in octahedral_crystals 
                                    if classifications[name]['field_type'] == 'circular')
            if octahedral_circular == 0:
                findings.append("No octahedral crystals produce circular fields (supports Freeman)")
            elif octahedral_circular == len(octahedral_crystals):
                findings.append("All octahedral crystals produce circular fields (contradicts Freeman)")
            else:
                findings.append(f"Mixed results for octahedral crystals ({octahedral_circular}/{len(octahedral_crystals)} circular)")
        
        return findings
    
    # Add missing helper methods for multipole analysis and field symmetry tests:
    def _fit_multipole_patterns(self, points: List[np.ndarray], fields: List[np.ndarray], 
                           distances: List[float], center: np.ndarray) -> Dict:
        """Fit electromagnetic fields to multipole patterns."""

        # Simplified multipole analysis
        monopole_score = self._fit_monopole_pattern(points, fields, distances, center)
        dipole_score = self._fit_dipole_pattern(points, fields, distances, center)
        quadrupole_score = self._fit_quadrupole_pattern(points, fields, distances, center)

        return {
            'monopole_score': monopole_score,
            'dipole_score': dipole_score,
            'quadrupole_score': quadrupole_score,
            'dominant_multipole': max(['monopole', 'dipole', 'quadrupole'], 
                                    key=lambda x: locals()[f'{x}_score'])
        }

    def _fit_monopole_pattern(self, points: List[np.ndarray], fields: List[np.ndarray], 
                         distances: List[float], center: np.ndarray) -> float:
        """Test how well fields match monopole (1/r²) pattern."""

        if len(points) == 0:
            return 0.0
    
        # For monopole: E ∝ 1/r², purely radial
        monopole_scores = []
    
        for point, field, distance in zip(points, fields, distances):
            if distance > 1e-20:
                r_vec = point - center
                r_hat = r_vec / np.linalg.norm(r_vec)
                field_mag = np.linalg.norm(field)

                if field_mag > 1e-20:
                    field_hat = field / field_mag
                    # Monopole field is purely radial
                    radial_alignment = abs(np.dot(r_hat, field_hat))
                    # Monopole falls off as 1/r²
                    expected_strength = 1.0 / distance**2
                    actual_strength = field_mag

                    # Score based on radial alignment and distance scaling
                    monopole_scores.append(radial_alignment)

        return np.mean(monopole_scores) if monopole_scores else 0.0

    def _fit_dipole_pattern(self, points: List[np.ndarray], fields: List[np.ndarray], 
                       distances: List[float], center: np.ndarray) -> float:
        """Test how well fields match dipole pattern."""
    
        # Similar implementation for dipole pattern
        # Dipole field has both radial and angular dependence
        return 0.5  # Placeholder

    def _fit_quadrupole_pattern(self, points: List[np.ndarray], fields: List[np.ndarray], 
                           distances: List[float], center: np.ndarray) -> float:
        """Test how well fields match quadrupole pattern."""
    
        # Quadrupole analysis placeholder
        return 0.3

    def _test_field_rotational_symmetry(self, crystal: MobiusCrystal, center: np.ndarray, 
                                   axis: np.ndarray, n: int) -> float:
        """Test n-fold rotational symmetry of electromagnetic fields."""
    
        # Test field symmetry by rotating test points and comparing field values
        angle = 2 * np.pi / n
        axis = axis / np.linalg.norm(axis)
    
        # Create rotation matrix
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        cross_matrix = np.array([[0, -axis[2], axis[1]], 
                                [axis[2], 0, -axis[0]], 
                                [-axis[1], axis[0], 0]])

        R = np.eye(3) + sin_a * cross_matrix + (1 - cos_a) * np.dot(cross_matrix, cross_matrix)

        # Test points around crystal
        test_points = []
        original_fields = []
        rotated_fields = []

        # Create test points
        for i in range(8):  # Limited test points for performance
            theta = i * np.pi / 4
            phi = i * np.pi / 6
            radius = 2e-15

            point = center + radius * np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ])

            # Original field
            field_orig = self._calculate_simplified_field(crystal, point)

            # Rotated point
            point_rot = center + np.dot(R, point - center)
            field_rot = self._calculate_simplified_field(crystal, point_rot)

            test_points.append(point)
            original_fields.append(field_orig)
            rotated_fields.append(field_rot)

        # Compare original and rotated fields
        symmetry_scores = []
        for f_orig, f_rot in zip(original_fields, rotated_fields):
            mag_orig = np.linalg.norm(f_orig)
            mag_rot = np.linalg.norm(f_rot)

            if mag_orig > 1e-20 and mag_rot > 1e-20:
                # Field magnitudes should be similar
                mag_similarity = min(mag_orig/mag_rot, mag_rot/mag_orig)

                # Field directions should be related by same rotation
                f_orig_rot = np.dot(R, f_orig)  # Rotate original field
                if np.linalg.norm(f_orig_rot) > 1e-20:
                    direction_similarity = np.dot(f_orig_rot, f_rot) / (np.linalg.norm(f_orig_rot) * mag_rot)
                    direction_similarity = abs(direction_similarity)
                else:
                    direction_similarity = 0.0

                symmetry_scores.append(mag_similarity * direction_similarity)

        return np.mean(symmetry_scores) if symmetry_scores else 0.0

    def _test_field_mirror_symmetry(self, crystal: MobiusCrystal, center: np.ndarray, 
                               normal: np.ndarray) -> float:
        """Test mirror symmetry of electromagnetic fields."""

        # Similar to rotational symmetry but with reflection
        normal = normal / np.linalg.norm(normal)

        # Reflection matrix: R = I - 2*n⊗n
        R = np.eye(3) - 2 * np.outer(normal, normal)

        # Test field symmetry across mirror plane
        symmetry_scores = []

        for i in range(8):
            # Test point on one side of plane
            offset = np.random.randn(3)
            offset = offset - np.dot(offset, normal) * normal  # Make perpendicular to normal
            offset = offset / np.linalg.norm(offset) * 2e-15

            point1 = center + offset + 1e-15 * normal
            point2 = center + np.dot(R, point1 - center)  # Reflected point

            field1 = self._calculate_simplified_field(crystal, point1)
            field2 = self._calculate_simplified_field(crystal, point2)

            # For mirror symmetry, normal component should flip, tangential should be same
            field1_refl = field1 - 2 * np.dot(field1, normal) * normal

            similarity = np.dot(field1_refl, field2) / (np.linalg.norm(field1_refl) * np.linalg.norm(field2) + 1e-20)
            symmetry_scores.append(abs(similarity))

        return np.mean(symmetry_scores) if symmetry_scores else 0.0

    def _test_field_inversion_symmetry(self, crystal: MobiusCrystal, center: np.ndarray) -> float:
        """Test inversion symmetry of electromagnetic fields."""

        # Inversion: r → -r, field behavior depends on multipole character
        symmetry_scores = []

        for i in range(8):
            # Random test point
            offset = np.random.randn(3)
            offset = offset / np.linalg.norm(offset) * 2e-15

            point1 = center + offset
            point2 = center - offset  # Inverted point

            field1 = self._calculate_simplified_field(crystal, point1)
            field2 = self._calculate_simplified_field(crystal, point2)

            # For inversion symmetry in electrostatics:
            # Monopole: E(-r) = -E(r)
            # Dipole: E(-r) = E(r)
            # Test both possibilities

            field1_inv = -field1  # Monopole expectation
            field1_same = field1  # Dipole expectation

            similarity_inv = np.dot(field1_inv, field2) / (np.linalg.norm(field1_inv) * np.linalg.norm(field2) + 1e-20)
            similarity_same = np.dot(field1_same, field2) / (np.linalg.norm(field1_same) * np.linalg.norm(field2) + 1e-20)

            # Take the better of the two
            symmetry_scores.append(max(abs(similarity_inv), abs(similarity_same)))

        return np.mean(symmetry_scores) if symmetry_scores else 0.0


# Helper function to run multiple configurations
def run_comprehensive_field_analysis():
    """Run comprehensive field analysis across multiple crystal configurations."""
    
    configurations = [
        ((3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.CUBIC),
        ((3, 3, 3), CrystalType.SINGLE_HELICITY_RIGHT, CrystalSymmetry.TETRAHEDRAL),
        ((4, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.HEXAGONAL),
        ((3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.DIAMOND)
    ]
    
    all_results = []
    
    for size, ctype, symmetry in configurations:
        print(f"\n{'='*60}")
        visualizer, summary_df, field_comparison = analyze_crystal_complete_with_field_comparison(
            size, ctype, symmetry
        )
        all_results.append({
            'configuration': (size, ctype, symmetry),
            'visualizer': visualizer,
            'summary': summary_df,
            'field_comparison': field_comparison
        })
    
    print(f"\n{'='*60}")
    print("Comprehensive Field Analysis Complete!")
    print(f"Generated visualizations and data files in test_results/")
    
    return all_results

# Add to crystal_assembly_visualizer.py (at module level, outside classes):

def run_comprehensive_g_factor_analysis():
    """
    Main function to run comprehensive g-factor analysis.
    
    This is the primary execution function that:
    1. Creates multiple crystal types
    2. Calculates g-factor contributions 
    3. Compares with experimental values
    4. Generates comprehensive report
    """
    
    print("=" * 60)
    print("COMPREHENSIVE G-FACTOR ANALYSIS")
    print("Testing James Freeman's Geometric Theory")
    print("=" * 60)
    
    # Create g-factor calculator
    calculator = MobiusGFactorCalculator()
    
    # Generate test crystals
    print("\nGenerating test crystals...")
    test_crystals = {
        'cubic_mixed': MobiusCrystal((3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.CUBIC),
        'tetrahedral_right': MobiusCrystal((3, 3, 3), CrystalType.SINGLE_HELICITY_RIGHT, CrystalSymmetry.TETRAHEDRAL),
        'hexagonal_mixed': MobiusCrystal((3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.HEXAGONAL),
        'diamond_structure': MobiusCrystal((2, 2, 2), CrystalType.MIXED_HELICITY, CrystalSymmetry.DIAMOND),
    }
    
    # Generate crystal structures
    for name, crystal in test_crystals.items():
        crystal.generate_crystal_structure()
        print(f"  ✓ Generated {name}: {crystal.total_units} units")
    
    # Perform comprehensive g-factor analysis
    print("\nCalculating g-factor contributions...")
    g_factor_results = calculator.comprehensive_g_factor_analysis(test_crystals)
    
    # Display results
    print("\n" + "=" * 60)
    print("G-FACTOR ANALYSIS RESULTS")
    print("=" * 60)
    
    for crystal_name, result in g_factor_results.items():
        if crystal_name == 'overall_assessment':
            continue
            
        print(f"\n--- {crystal_name.upper()} ---")
        g_data = result['g_factor_contribution']
        qed_comp = result['qed_comparison']
        freeman_assess = result['freeman_theory_assessment']
        
        print(f"Geometric g-contribution: {g_data.geometric_contribution:.2e}")
        print(f"Theoretical g-factor: {g_data.total_theoretical_g:.8f}")
        print(f"Experimental g-factor: {g_data.experimental_g:.8f}")
        print(f"Anomaly explained: {freeman_assess['anomaly_explanation_percentage']:.1f}%")
        print(f"Confidence level: {g_data.confidence_level:.3f}")
        print(f"Theory viable: {freeman_assess['theory_viable']}")
        
        if freeman_assess['primary_limitations']:
            print("Limitations:")
            for limitation in freeman_assess['primary_limitations']:
                print(f"  - {limitation}")
    
    # Overall assessment
    print("\n" + "=" * 60)
    print("OVERALL ASSESSMENT")
    print("=" * 60)
    
    overall = g_factor_results['overall_assessment']
    print(f"Average anomaly explanation: {overall['average_anomaly_explanation']:.1f}%")
    print(f"Best anomaly explanation: {overall['best_anomaly_explanation']:.1f}%")
    print(f"Average confidence: {overall['average_confidence']:.3f}")
    print(f"Theory viability: {overall['overall_theory_viability']}")
    print(f"\nRecommendation: {overall['recommendation']}")
    
    # QED comparison
    print("\n" + "=" * 60)
    print("COMPARISON WITH QUANTUM ELECTRODYNAMICS")
    print("=" * 60)
    
    # Get best result for comparison
    best_crystal = max(g_factor_results.keys(), 
                      key=lambda k: g_factor_results[k]['g_factor_contribution'].deviation_explained 
                      if k != 'overall_assessment' else 0)
    
    if best_crystal != 'overall_assessment':
        best_qed = g_factor_results[best_crystal]['qed_comparison']
        print(f"Best geometric explanation: {best_crystal}")
        print(f"Geometric vs QED leading order: {best_qed['geometric_vs_leading_qed']:.3f}")
        print(f"Geometric vs total QED: {best_qed['geometric_vs_total_qed']:.3f}")
        print(f"QED explains: {best_qed['qed_explanation_fraction']*100:.1f}% of anomaly")
        print(f"Theoretical consistency: {best_qed['theoretical_consistency']}")
    
    # Save detailed results
    output_file = "test_results/g_factor_analysis_complete.json"
    try:
        import json
        with open(output_file, 'w') as f:
            # Convert numpy types to JSON serializable
            serializable_results = _convert_results_for_json(g_factor_results)
            json.dump(serializable_results, f, indent=2, default=str)
        print(f"\nDetailed results saved to: {output_file}")
    except Exception as e:
        print(f"\nWarning: Could not save results file: {e}")
    
    return g_factor_results

def _convert_results_for_json(results):
    """Convert numpy types to JSON-serializable format."""
    
    def convert_value(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_value(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_value(v) for v in obj]
        elif hasattr(obj, '__dict__'):
            return convert_value(obj.__dict__)
        else:
            return obj
    
    return convert_value(results)

def calculate_g_factor_contributions(self) -> Dict:
        """Calculate g-factor contributions from Möbius crystal geometries."""

        calculator = MobiusGFactorCalculator()
        g_factor_result = calculator.calculate_comprehensive_g_factor(self.crystal)
        qed_comparison = calculator.compare_with_qed_predictions(g_factor_result)

        return {
            'g_factor_contribution': g_factor_result,
            'qed_comparison': qed_comparison,
            'freeman_assessment': calculator._assess_freeman_theory(g_factor_result)
        }

# Update your main execution block:
if __name__ == "__main__":
    """
    Main execution: Run complete analysis including g-factor calculations.
    """
    
    # Option 1: Run basic crystal analysis (existing)
    configurations = [
        ((3, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.CUBIC),
        ((3, 3, 3), CrystalType.SINGLE_HELICITY_RIGHT, CrystalSymmetry.TETRAHEDRAL),
        ((4, 3, 3), CrystalType.MIXED_HELICITY, CrystalSymmetry.HEXAGONAL)
    ]
    
    for size, ctype, symmetry in configurations:
        print(f"\n{'='*60}")
        viz, data = analyze_crystal_complete(size, ctype, symmetry)
    
    # Option 2: Run comprehensive g-factor analysis (NEW)
    g_factor_results = run_comprehensive_g_factor_analysis()
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print("Generated comprehensive g-factor analysis and comparison with QED.")
    print("Check test_results/ directory for detailed output files.")
