# nuclear_assembly/assemblies/d2_tt_variant.py
"""
Experimental D2 variant with T-T bond at center.
Testing if crossed form with H-H or H-T bonds can work.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from geometry.face_labeling import LabeledTetrahedron
from geometry.constants import r_eff_TT, COUPLING_TT


class D2_TT_Variant:
    """
    Experimental D2: proton + neutron bonded via T0-T0.
    Then test crossed bonds using remaining faces.
    """
    
    def __init__(self, position: np.ndarray = None, orientation: np.ndarray = None,
                 tt_twist: float = 0.0):
        """
        Create T-T variant D2 unit.
        
        Args:
            position: Center position (default origin)
            orientation: Quaternion for orientation (default identity)
            tt_twist: Rotation angle for T-T bond (degrees)
        """
        if position is None:
            position = np.array([0, 0, 0], dtype=float)
        if orientation is None:
            orientation = np.array([1, 0, 0, 0])
            
        self.position = position
        self.orientation = orientation
        self.tt_twist = tt_twist
        
        # Create the two tetrahedra
        self.proton = LabeledTetrahedron()
        self.neutron = LabeledTetrahedron()
        
        # Bond them via T0(p) - T0(n) - smallest aperture at center
        self._create_tt_bond()
        
        # Test what additional bonds are possible
        self.crossed_bonds = self._test_crossed_bonds()
        
    def _create_tt_bond(self):
        """Create the T0-T0 bond between proton and neutron."""
        # Get face normals and centers
        p_t0_normal = self.proton.get_face_normal(self.proton.get_face('T0'))
        p_t0_center = self.proton.get_face_center(self.proton.get_face('T0'))
        
        n_t0_normal = self.neutron.get_face_normal(self.neutron.get_face('T0'))
        n_t0_center = self.neutron.get_face_center(self.neutron.get_face('T0'))
        
        # Align neutron T0 opposite to proton T0
        target_normal = -p_t0_normal
        rotation = self._rotation_matrix_between_vectors(n_t0_normal, target_normal)
        
        # Apply rotation
        self.neutron.vertices = (rotation @ self.neutron.vertices.T).T
        
        # Apply twist if specified
        if abs(self.tt_twist) > 0.001:
            twist_rad = np.radians(self.tt_twist)
            twist_rotation = self._rotation_matrix_around_axis(target_normal, twist_rad)
            self.neutron.vertices = (twist_rotation @ self.neutron.vertices.T).T
        
        # Recalculate center after rotations
        n_t0_center = self.neutron.get_face_center(self.neutron.get_face('T0'))
        
        # Position with small gap
        separation = 0.01
        translation = p_t0_center + p_t0_normal * separation - n_t0_center
        self.neutron.vertices = self.neutron.vertices + translation
        
        # Store bond info
        self.central_bond = {
            'type': 'TT',
            'from': ('proton', 'T0'),
            'to': ('neutron', 'T0'),
            'r_eff': r_eff_TT(),
            'coupling': COUPLING_TT,
            'twist': self.tt_twist
        }
    
    def _test_crossed_bonds(self) -> List[Dict]:
        """
        Test what crossed bonds are geometrically possible.
        With T0-T0 at center, check if H or T faces can reach across.
        """
        possible_bonds = []
        
        # Check all possible H-H combinations
        for p_face in ['H0', 'H1', 'H2', 'H3']:
            p_center = self.proton.get_face_center(self.proton.get_face(p_face))
            p_normal = self.proton.get_face_normal(self.proton.get_face(p_face))
            
            for n_face in ['H0', 'H1', 'H2', 'H3']:
                n_center = self.neutron.get_face_center(self.neutron.get_face(n_face))
                n_normal = self.neutron.get_face_normal(self.neutron.get_face(n_face))
                
                # Check if faces are roughly opposing
                dot = np.dot(p_normal, n_normal)
                if dot < -0.5:  # Faces roughly opposite
                    distance = np.linalg.norm(n_center - p_center)
                    angle = np.degrees(np.arccos(np.clip(-dot, -1, 1)))
                    
                    possible_bonds.append({
                        'type': 'HH',
                        'from': ('proton', p_face),
                        'to': ('neutron', n_face),
                        'distance': distance,
                        'angle_offset': angle,
                        'feasible': distance < 2.0  # Rough feasibility check
                    })
        
        # Check H-T combinations
        for p_h_face in ['H0', 'H1', 'H2', 'H3']:
            p_center = self.proton.get_face_center(self.proton.get_face(p_h_face))
            p_normal = self.proton.get_face_normal(self.proton.get_face(p_h_face))
            
            for n_t_face in ['T1', 'T2', 'T3']:  # T0 already used
                n_center = self.neutron.get_face_center(self.neutron.get_face(n_t_face))
                n_normal = self.neutron.get_face_normal(self.neutron.get_face(n_t_face))
                
                dot = np.dot(p_normal, n_normal)
                if dot < -0.5:
                    distance = np.linalg.norm(n_center - p_center)
                    angle = np.degrees(np.arccos(np.clip(-dot, -1, 1)))
                    
                    possible_bonds.append({
                        'type': 'HT',
                        'from': ('proton', p_h_face),
                        'to': ('neutron', n_t_face),
                        'distance': distance,
                        'angle_offset': angle,
                        'feasible': distance < 2.0
                    })
        
        return possible_bonds
    
    def report_geometry(self):
        """Report on the geometric feasibility of crossed bonds."""
        print(f"D2 T-T Variant Analysis (twist={self.tt_twist}°)")
        print(f"Central bond: T0-T0, r_eff={self.central_bond['r_eff']:.3f}")
        print("\nPossible crossed bonds:")
        
        feasible = [b for b in self.crossed_bonds if b['feasible']]
        
        if feasible:
            print(f"Found {len(feasible)} feasible crossed bonds:")
            for bond in feasible[:5]:  # Show first 5
                print(f"  {bond['from'][1]}(p) -> {bond['to'][1]}(n): "
                      f"dist={bond['distance']:.3f}, angle_off={bond['angle_offset']:.1f}°")
        else:
            print("  No feasible crossed bonds with current geometry")
        
        # Check if this creates a stable configuration
        if len(feasible) >= 2:
            print("\n✓ Configuration could be stable with multiple crossed bonds")
        else:
            print("\n✗ Configuration unlikely to be stable")
    
    def _rotation_matrix_between_vectors(self, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """Calculate rotation matrix to rotate v1 to v2."""
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        
        if np.allclose(v1, v2):
            return np.eye(3)
        
        if np.allclose(v1, -v2):
            perp = np.array([1, 0, 0]) if abs(v1[0]) < 0.9 else np.array([0, 1, 0])
            perp = perp - np.dot(perp, v1) * v1
            perp = perp / np.linalg.norm(perp)
            return 2 * np.outer(perp, perp) - np.eye(3)
        
        axis = np.cross(v1, v2)
        axis = axis / np.linalg.norm(axis)
        angle = np.arccos(np.clip(np.dot(v1, v2), -1, 1))
        return self._rotation_matrix_around_axis(axis, angle)
    
    def _rotation_matrix_around_axis(self, axis: np.ndarray, angle: float) -> np.ndarray:
        """Create rotation matrix for rotation around axis by angle."""
        axis = axis / np.linalg.norm(axis)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        ux, uy, uz = axis
        
        return np.array([
            [cos_a + ux**2*(1-cos_a), ux*uy*(1-cos_a) - uz*sin_a, ux*uz*(1-cos_a) + uy*sin_a],
            [uy*ux*(1-cos_a) + uz*sin_a, cos_a + uy**2*(1-cos_a), uy*uz*(1-cos_a) - ux*sin_a],
            [uz*ux*(1-cos_a) - uy*sin_a, uz*uy*(1-cos_a) + ux*sin_a, cos_a + uz**2*(1-cos_a)]
        ])


# Test script
if __name__ == "__main__":
    print("Testing T-T variant D2 configurations...\n")
    
    # Test different twist angles
    for twist in [0, 30, 60, 90, 120]:
        print(f"\n{'='*50}")
        d2_tt = D2_TT_Variant(tt_twist=twist)
        d2_tt.report_geometry()
        
    # Visualize the most promising configuration
    print("\n\nVisualize with: python3 test_tt_variant.py")
