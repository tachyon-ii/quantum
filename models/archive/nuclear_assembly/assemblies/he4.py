"""
He4 assembly - two D2 units forming a ring.
Chirality emerges from ±60° twist on closure.
"""

import numpy as np
from typing import Dict, List, Optional
from .d2 import D2Unit
from geometry.constants import r_eff_HT, COUPLING_HT


class He4Ring:
    """
    Helium-4 ring: two D2 units with 4-cycle H-T bonds.
    Chirality determined by ±60° twist on closure.
    """
    
    def __init__(self, chirality: str = 'L'):
        """
        Create He4 ring.
        
        Args:
            chirality: 'L' for left-handed (+60°), 'R' for right-handed (-60°)
        """
        if chirality not in ['L', 'R']:
            raise ValueError("Chirality must be 'L' or 'R'")
            
        self.chirality = chirality
        self.twist_angle = 60 if chirality == 'L' else -60
        
        # Create two D2 units
        self.d2_1 = D2Unit()
        self.d2_2 = D2Unit()
        
        # Form the ring
        self._create_ring()
        
    def _create_ring(self):
        """
        Create the 4-cycle ring with H-T bonds.
        Bond pattern:
        - p1:H0 - n1:T0 (from D2_1)
        - p2:H0 - n2:T0 (from D2_2)  
        - n1:H1 - p2:T1 (cross link with twist)
        - n2:H1 - p1:T1 (cross link)
        """
        # Position second D2 unit
        # This requires calculating proper alignment for ring closure
        
        # Get required faces from each unit
        n1_h1_center = self.d2_1.neutron.get_face_center(
            self.d2_1.neutron.get_face('H1'))
        p1_t1_center = self.d2_1.proton.get_face_center(
            self.d2_1.proton.get_face('T1'))
        
        # Calculate transformation for d2_2
        # This is simplified - full implementation needs proper rotation matrices
        translation = np.array([2.0, 0, 0])  # Approximate positioning
        self.d2_2.apply_transform(translation=translation)
        
        # Apply twist for chirality
        if self.twist_angle != 0:
            # Rotation around bond axis
            angle_rad = np.radians(self.twist_angle)
            # Simplified - need proper rotation matrix
            rotation = self._rotation_matrix_z(angle_rad)
            self.d2_2.apply_transform(rotation=rotation)
        
        # Store ring bonds
        self.bonds = [
            {'type': 'HT', 'from': ('d2_1', 'p1', 'H0'), 
             'to': ('d2_1', 'n1', 'T0')},
            {'type': 'HT', 'from': ('d2_2', 'p2', 'H0'), 
             'to': ('d2_2', 'n2', 'T0')},
            {'type': 'HT', 'from': ('d2_1', 'n1', 'H1'), 
             'to': ('d2_2', 'p2', 'T1'), 'twist': self.twist_angle},
            {'type': 'HT', 'from': ('d2_2', 'n2', 'H1'), 
             'to': ('d2_1', 'p1', 'T1')}
        ]
        
    def _rotation_matrix_z(self, angle: float) -> np.ndarray:
        """Rotation matrix around z-axis."""
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([
            [c, -s, 0],
            [s, c, 0],
            [0, 0, 1]
        ])
    
    def get_chirality_sign(self) -> int:
        """
        Calculate chirality sign χ = ±1.
        Based on three non-coplanar face normals.
        """
        # Get three face normals
        n1 = self.d2_1.proton.get_face_normal(
            self.d2_1.proton.get_face('H0'))
        n2 = self.d2_1.neutron.get_face_normal(
            self.d2_1.neutron.get_face('H1'))
        n3 = self.d2_2.proton.get_face_normal(
            self.d2_2.proton.get_face('H0'))
        
        # Calculate triple product
        chi_value = np.dot(n1, np.cross(n2, n3))
        return 1 if chi_value > 0 else -1
    
    def get_free_faces(self) -> Dict:
        """Get remaining free faces for further assembly."""
        # Each D2 has used 2 more faces for ring closure
        # Detailed calculation needed based on actual bonds
        return {
            'd2_1': {
                'proton': ['H2', 'H3', 'T2', 'T3'],
                'neutron': ['H2', 'H3', 'T2', 'T3']
            },
            'd2_2': {
                'proton': ['H2', 'H3', 'T2', 'T3'],
                'neutron': ['H2', 'H3', 'T2', 'T3']
            }
        }
    
    def to_dict(self) -> Dict:
        """Export He4 configuration."""
        return {
            'type': 'He4',
            'chirality': self.chirality,
            'twist_angle': self.twist_angle,
            'chi_sign': self.get_chirality_sign(),
            'd2_1': self.d2_1.to_dict(),
            'd2_2': self.d2_2.to_dict(),
            'bonds': self.bonds,
            'free_faces': self.get_free_faces()
        }
