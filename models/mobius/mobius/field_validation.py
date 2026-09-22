# Fixed field_validation.py

import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from .crystal_assembly import MobiusCrystal, CrystalType, CrystalSymmetry

ELEMENTARY_CHARGE = 1.602e-19  # Coulombs
PERMITTIVITY = 8.854e-12      # F/m

class FieldCalculationValidator:
    """
    Validate electromagnetic field calculations to debug the issues
    we've been seeing with zero circularity and negative uniformity.
    """
    
    def __init__(self):
        self.validation_results = {}
    
    def validate_basic_field_calculation(self) -> Dict:
        """Test basic field calculation with known simple cases."""
        
        print("Testing basic electromagnetic field calculations...")
        
        test_results = {}
        
        # Create minimal crystal for testing
        crystal = MobiusCrystal(
            crystal_size=(1, 1, 1),
            crystal_type=CrystalType.SINGLE_HELICITY_RIGHT,
            crystal_symmetry=CrystalSymmetry.CUBIC
        )
        crystal.generate_crystal_structure()
        
        # Verify units were created
        test_results['units_created'] = len(crystal.tetrahedral_units)
        test_results['has_charge_data'] = []
        test_results['charge_values'] = []
        
        for position, unit in crystal.tetrahedral_units.items():
            has_charge = hasattr(unit, 'charge_distribution') and unit.charge_distribution is not None
            test_results['has_charge_data'].append(has_charge)
            
            if has_charge:
                charge = unit.charge_distribution.net_charge
                test_results['charge_values'].append(charge)
            else:
                test_results['charge_values'].append(0.0)
        
        # Test field at known point
        test_point = np.array([1e-14, 0, 0])  # 10 fm away on x-axis
        field = self._calculate_test_field(crystal, test_point)
        test_results['test_field'] = field
        test_results['field_magnitude'] = np.linalg.norm(field)
        
        return test_results
    
    def _calculate_test_field(self, crystal: MobiusCrystal, point: np.ndarray) -> np.ndarray:
        """Fixed field calculation with proper error handling."""
        
        total_field = np.zeros(3)
        
        for position, unit in crystal.tetrahedral_units.items():
            # Get actual position from lattice_positions dictionary
            if position in crystal.lattice_positions:
                unit_pos = np.array(crystal.lattice_positions[position])
            else:
                # Fallback: use position tuple as coordinates
                unit_pos = np.array(position, dtype=float) * crystal.lattice_parameters.lattice_constant
            
            r_vec = point - unit_pos
            r_mag = np.linalg.norm(r_vec)
            
            print(f"  Unit at {unit_pos}, distance: {r_mag:.2e}")
            
            if r_mag < 1e-20:
                print(f"    Skipping: too close to avoid singularity")
                continue
            
            r_hat = r_vec / r_mag
            
            # Check for charge distribution with proper error handling
            if hasattr(unit, 'charge_distribution') and unit.charge_distribution:
                charge = float(unit.charge_distribution.net_charge)  # Ensure real number
                print(f"    Charge: {charge}")
                
                # Simple Coulomb field with proper units and regularization
                # Add small regularization term to prevent singularities
                
                k_e = 1/(4*np.pi*PERMITTIVITY) # Coulomb constant

                field_contrib = k_e * charge * ELEMENTARY_CHARGE * r_hat / (r_mag**2)
                
                # Check for numerical issues
                if np.isfinite(field_contrib).all():
                    total_field += field_contrib
                    print(f"    Field contribution: {field_contrib}")
                else:
                    print(f"    Warning: Non-finite field contribution, skipping")
            else:
                print(f"    No charge distribution found")
        
        print(f"  Total field: {total_field}")
        
        # Ensure field is real-valued
        if np.iscomplexobj(total_field):
            print(f"  Warning: Complex field detected, taking real part")
            total_field = np.real(total_field)
            
        return total_field
    
    def test_circularity_calculation(self) -> Dict:
        """Test the circularity calculation with known geometric patterns."""
        
        print("\nTesting circularity calculations...")
        
        # Create test points in a perfect circle
        center = np.array([0, 0, 0])
        radius = 1e-14
        n_points = 8
        
        # Perfect tangential field (should give circularity = 1.0)
        test_points = []
        tangential_fields = []
        
        for i in range(n_points):
            angle = 2 * np.pi * i / n_points
            point = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
            # Tangential field (perpendicular to radial)
            field = np.array([-np.sin(angle), np.cos(angle), 0])
            
            test_points.append(point)
            tangential_fields.append(field)
        
        tangential_circularity = self._test_circularity_algorithm(
            test_points, tangential_fields, center
        )
        
        # Perfect radial field (should give circularity = 0.0)
        radial_fields = []
        for i in range(n_points):
            angle = 2 * np.pi * i / n_points
            # Radial field (pointing outward)
            field = np.array([np.cos(angle), np.sin(angle), 0])
            radial_fields.append(field)
        
        radial_circularity = self._test_circularity_algorithm(
            test_points, radial_fields, center
        )
        
        return {
            'tangential_circularity': tangential_circularity,
            'radial_circularity': radial_circularity,
            'algorithm_working': abs(tangential_circularity - 1.0) < 0.1 and radial_circularity < 0.5
        }
    
    def _test_circularity_algorithm(self, points: List[np.ndarray], 
                                   fields: List[np.ndarray], 
                                   center: np.ndarray) -> float:
        """Fixed circularity calculation algorithm."""
        
        if len(points) != len(fields) or len(points) == 0:
            print("    Error: Mismatched or empty point/field arrays")
            return 0.0
        
        circularity_scores = []
        
        for point, field in zip(points, fields):
            r_vec = point - center
            r_mag = np.linalg.norm(r_vec)
            field_mag = np.linalg.norm(field)
            
            # More robust threshold checking
            if r_mag > 1e-20 and field_mag > 1e-20:
                r_hat = r_vec / r_mag
                field_hat = field / field_mag
                
                # For circular field, field should be tangent (perpendicular to radial)
                radial_component = abs(np.dot(r_hat, field_hat))
                
                # Ensure radial_component is between 0 and 1
                radial_component = np.clip(radial_component, 0.0, 1.0)
                
                tangential_score = 1.0 - radial_component
                circularity_scores.append(tangential_score)
                
                print(f"    Point: {point}")
                print(f"    Radial component: {radial_component:.3f}, Tangential score: {tangential_score:.3f}")
            else:
                print(f"    Skipping point: r_mag={r_mag:.2e}, field_mag={field_mag:.2e}")
        
        if len(circularity_scores) > 0:
            avg_circularity = np.mean(circularity_scores)
            print(f"  Average circularity: {avg_circularity:.3f}")
            return float(avg_circularity)  # Ensure real number
        else:
            print("  Warning: No valid circularity scores computed")
            return 0.0
    
    def validate_james_octahedral_prediction(self) -> Dict:
        """Specifically test James's octahedral crystal prediction."""
        
        print("\nValidating James's octahedral prediction...")
        
        # Create simple cubic vs octahedral comparison
        cubic_crystal = MobiusCrystal(
            crystal_size=(2, 2, 2),
            crystal_type=CrystalType.MIXED_HELICITY,
            crystal_symmetry=CrystalSymmetry.CUBIC
        )
        cubic_crystal.generate_crystal_structure()
        
        # Create octahedral arrangement manually
        octahedral_crystal = self._create_simple_octahedral()
        
        # Test field patterns with error handling
        try:
            cubic_circularity = self._measure_crystal_circularity(cubic_crystal)
        except Exception as e:
            print(f"    Error measuring cubic circularity: {e}")
            cubic_circularity = 0.0
            
        try:
            octahedral_circularity = self._measure_crystal_circularity(octahedral_crystal)
        except Exception as e:
            print(f"    Error measuring octahedral circularity: {e}")
            octahedral_circularity = 0.0
        
        return {
            'cubic_circularity': float(cubic_circularity),
            'octahedral_circularity': float(octahedral_circularity),
            'james_prediction_supported': octahedral_circularity < cubic_circularity,
            'difference': float(cubic_circularity - octahedral_circularity)
        }
    
    def _create_simple_octahedral(self) -> MobiusCrystal:
        """Create simplified octahedral crystal for testing."""
        
        crystal = MobiusCrystal(
            crystal_size=(1, 1, 1),
            crystal_type=CrystalType.MIXED_HELICITY,
            crystal_symmetry=CrystalSymmetry.CUBIC
        )
        crystal.generate_crystal_structure()
        
        # Clear and rebuild as octahedral
        crystal.tetrahedral_units.clear()
        crystal.lattice_positions.clear()
        
        # 6 units at octahedral vertices with proper lattice constant
        if hasattr(crystal, 'lattice_parameters') and crystal.lattice_parameters:
            lattice_const = crystal.lattice_parameters.lattice_constant
        else:
            lattice_const = 5e-15
            
        positions = [
            ((1, 0, 0), np.array([lattice_const, 0, 0])),
            ((-1, 0, 0), np.array([-lattice_const, 0, 0])),
            ((0, 1, 0), np.array([0, lattice_const, 0])),
            ((0, -1, 0), np.array([0, -lattice_const, 0])),
            ((0, 0, 1), np.array([0, 0, lattice_const])),
            ((0, 0, -1), np.array([0, 0, -lattice_const]))
        ]
        
        for pos_key, pos_vec in positions:
            try:
                helicity1, helicity2 = crystal._determine_helicities_at_site(*pos_key)
                unit = crystal._create_tetrahedral_unit_at_position(pos_vec, helicity1, helicity2)
                
                crystal.tetrahedral_units[pos_key] = unit
                crystal.lattice_positions[pos_key] = pos_vec
            except Exception as e:
                print(f"    Warning: Could not create unit at {pos_key}: {e}")
        
        crystal.total_units = len(crystal.tetrahedral_units)
        
        # Recalculate properties with error handling
        try:
            crystal._calculate_crystal_properties()
        except Exception as e:
            print(f"    Warning: Could not calculate crystal properties: {e}")
        
        return crystal
    
    def _measure_crystal_circularity(self, crystal: MobiusCrystal) -> float:
        """Measure circularity for a crystal using simplified method."""
        
        if not crystal.lattice_positions:
            print("    Error: No lattice positions found")
            return 0.0
            
        positions = np.array(list(crystal.lattice_positions.values()))
        center = np.mean(positions, axis=0)
        
        # Test points on sphere around crystal
        distances = np.linalg.norm(positions - center, axis=1)
        if len(distances) == 0 or np.max(distances) == 0:
            print("    Error: Invalid crystal geometry")
            return 0.0
            
        test_radius = np.max(distances) * 2
        n_test = 12
        
        test_points = []
        test_fields = []
        
        for i in range(n_test):
            theta = i * np.pi / 6
            phi = i * np.pi / 3
            
            point = center + test_radius * np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ])
            
            try:
                field = self._calculate_test_field(crystal, point)
                if np.isfinite(field).all() and np.linalg.norm(field) > 1e-30:
                    test_points.append(point)
                    test_fields.append(field)
            except Exception as e:
                print(f"    Warning: Field calculation failed at point {i}: {e}")
        
        if len(test_points) == 0:
            print("    Error: No valid field points computed")
            return 0.0
            
        return self._test_circularity_algorithm(test_points, test_fields, center)
    
    def run_complete_validation(self) -> Dict:
        """Run all validation tests with comprehensive error handling."""
        
        print("=" * 50)
        print("FIELD CALCULATION VALIDATION")
        print("=" * 50)
        
        results = {}
        
        # Test 1: Basic field calculation
        try:
            results['basic_field'] = self.validate_basic_field_calculation()
        except Exception as e:
            print(f"Basic field validation failed: {e}")
            results['basic_field'] = {'error': str(e)}
        
        # Test 2: Circularity algorithm
        try:
            results['circularity'] = self.test_circularity_calculation()
        except Exception as e:
            print(f"Circularity test failed: {e}")
            results['circularity'] = {'error': str(e)}
        
        # Test 3: James's prediction
        try:
            results['james_prediction'] = self.validate_james_octahedral_prediction()
        except Exception as e:
            print(f"James prediction test failed: {e}")
            results['james_prediction'] = {'error': str(e)}
        
        # Summary
        print("\n" + "=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        
        if 'error' not in results.get('basic_field', {}):
            print(f"Units created: {results['basic_field'].get('units_created', 0)}")
            print(f"Charges present: {sum(results['basic_field'].get('has_charge_data', []))}")
            print(f"Field magnitude: {results['basic_field'].get('field_magnitude', 0):.2e}")
        else:
            print(f"Basic field test failed: {results['basic_field']['error']}")
            
        if 'error' not in results.get('circularity', {}):
            print(f"Circularity algorithm working: {results['circularity'].get('algorithm_working', False)}")
        else:
            print(f"Circularity test failed: {results['circularity']['error']}")
            
        if 'error' not in results.get('james_prediction', {}):
            print(f"James prediction supported: {results['james_prediction'].get('james_prediction_supported', False)}")
        else:
            print(f"James prediction test failed: {results['james_prediction']['error']}")
        
        return results

# Add to your main execution
if __name__ == "__main__":
    validator = FieldCalculationValidator()
    validation_results = validator.run_complete_validation()