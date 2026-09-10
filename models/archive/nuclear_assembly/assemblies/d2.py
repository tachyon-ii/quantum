# nuclear_assembly/assemblies/d2.py - CORRECTED VERSION with H-H' rotation
"""
D2 assembly - fundamental building block.
One proton + one neutron via H0-H0 bond with π/3 rotation (H-H' form).
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from geometry.face_labeling import LabeledTetrahedron
from geometry.constants import r_eff_HH, COUPLING_HH


class D2Unit:
    """
    Deuterium unit: proton + neutron bonded via H0-H0 with π/3 rotation.
    This is the H-H' configuration - the fundamental building block.
    """
    
    def __init__(self, position: np.ndarray = None, orientation: np.ndarray = None):
        """
        Create D2 unit.
        
        Args:
            position: Center position (default origin)
            orientation: Quaternion for orientation (default identity)
        """
        if position is None:
            position = np.array([0, 0, 0], dtype=float)
        if orientation is None:
            orientation = np.array([1, 0, 0, 0])  # Identity quaternion
            
        self.position = position
        self.orientation = orientation
        
        # Create the two tetrahedra
        self.proton = LabeledTetrahedron()
        self.neutron = LabeledTetrahedron()
        
        # Bond them via H0(p) - H0(n) with π/3 rotation (H-H' form)
        self._create_bond()
        
    def _create_bond(self):
        """Create the H0-H0 bond with π/3 rotation (H-H' configuration)."""
        # Get face normals and centers
        p_h0_normal = self.proton.get_face_normal(self.proton.get_face('H0'))
        p_h0_center = self.proton.get_face_center(self.proton.get_face('H0'))
        
        n_h0_normal = self.neutron.get_face_normal(self.neutron.get_face('H0'))
        n_h0_center = self.neutron.get_face_center(self.neutron.get_face('H0'))
        
        # Position neutron so H0 faces opposite to proton's H0
        # Face normals should be anti-parallel for H-H bond
        
        # First, rotate neutron so its H0 normal is opposite to proton's H0 normal
        target_normal = -p_h0_normal
        current_normal = n_h0_normal
        
        # Calculate rotation needed to align normals
        rotation = self._rotation_matrix_between_vectors(current_normal, target_normal)
        
        # Apply rotation to neutron
        self.neutron.vertices = (rotation @ self.neutron.vertices.T).T
        
        # NOW APPLY THE π/3 ROTATION FOR H-H' CONFIGURATION
        # This is the key difference - rotate by 60 degrees around the bond axis
        rotation_60 = self._rotation_matrix_around_axis(target_normal, np.pi/3)
        self.neutron.vertices = (rotation_60 @ self.neutron.vertices.T).T
        
        # Recalculate neutron face center after rotations
        n_h0_center = self.neutron.get_face_center(self.neutron.get_face('H0'))
        
        # Calculate translation to align faces with small separation
        separation = 0.01  # Small gap for visualization
        translation = p_h0_center + p_h0_normal * separation - n_h0_center
        
        # Apply translation to neutron
        self.neutron.vertices = self.neutron.vertices + translation
        
        # Store bond info
        self.bond = {
            'type': 'HH',  # H-H bond
            'subtype': 'HH_prime',  # H-H' with rotation
            'rotation': 60,  # degrees
            'from': ('proton', 'H0'),
            'to': ('neutron', 'H0'),
            'r_eff': r_eff_HH(),
            'coupling': COUPLING_HH
        }
    
    def _rotation_matrix_between_vectors(self, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """Calculate rotation matrix to rotate v1 to v2."""
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        
        # Check if vectors are already aligned
        if np.allclose(v1, v2):
            return np.eye(3)
        
        # Check if vectors are opposite
        if np.allclose(v1, -v2):
            # Find an orthogonal vector
            orthogonal = np.array([1, 0, 0]) if abs(v1[0]) < 0.9 else np.array([0, 1, 0])
            orthogonal = orthogonal - np.dot(orthogonal, v1) * v1
            orthogonal = orthogonal / np.linalg.norm(orthogonal)
            # 180 degree rotation around orthogonal axis
            return 2 * np.outer(orthogonal, orthogonal) - np.eye(3)
        
        # General case
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
        
        # Rodrigues' rotation formula
        return np.array([
            [cos_a + ux**2*(1-cos_a), ux*uy*(1-cos_a) - uz*sin_a, ux*uz*(1-cos_a) + uy*sin_a],
            [uy*ux*(1-cos_a) + uz*sin_a, cos_a + uy**2*(1-cos_a), uy*uz*(1-cos_a) - ux*sin_a],
            [uz*ux*(1-cos_a) - uy*sin_a, uz*uy*(1-cos_a) + ux*sin_a, cos_a + uz**2*(1-cos_a)]
        ])
    
    def get_free_faces(self) -> Dict[str, List[str]]:
        """
        Get the free (unbonded) faces.
        Note: The H-H' rotation affects which faces are truly "free" geometrically.
        
        Returns:
            Dict with 'proton' and 'neutron' free faces
        """
        return {
            'proton': ['H1', 'H2', 'H3', 'T0', 'T1', 'T2', 'T3'],  # H0 is bonded
            'neutron': ['H1', 'H2', 'H3', 'T0', 'T1', 'T2', 'T3']  # H0 is bonded
        }
    
    def get_stacking_faces(self) -> Dict[str, List[str]]:
        """
        Get the faces that can stack with other D2 units.
        Due to the H-H' geometry, certain faces align better for stacking.
        """
        # This will need refinement based on the actual geometry
        return {
            'proton': ['H1', 'H2', 'H3'],  
            'neutron': ['H1', 'H2', 'H3']
        }
    
    def apply_transform(self, rotation: np.ndarray = None, translation: np.ndarray = None):
        """Apply transformation to entire D2 unit."""
        if rotation is not None:
            # Apply rotation to both tetrahedra
            self.proton.vertices = (rotation @ self.proton.vertices.T).T
            self.neutron.vertices = (rotation @ self.neutron.vertices.T).T
            
        if translation is not None:
            # Ensure translation is float array to match vertices
            translation = np.array(translation, dtype=float)
            # Apply translation to both tetrahedra
            self.proton.vertices = self.proton.vertices + translation
            self.neutron.vertices = self.neutron.vertices + translation
            self.position = self.position + translation
    
    def to_dict(self) -> Dict:
        """Export D2 configuration."""
        return {
            'type': 'D2',
            'subtype': 'HH_prime',
            'position': self.position.tolist(),
            'orientation': self.orientation.tolist(),
            'proton': self.proton.to_dict(),
            'neutron': self.neutron.to_dict(),
            'bond': self.bond,
            'free_faces': self.get_free_faces()
        }
