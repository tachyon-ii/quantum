"""
Face labeling system for truncated tetrahedron.
Assigns H0-H3 and T0-T3 labels based on reference vector.
"""

import numpy as np
from typing import Tuple, List, Optional
from .tetra_base import TruncatedTetrahedron


class LabeledTetrahedron(TruncatedTetrahedron):
    """
    Truncated tetrahedron with face labels H0-H3, T0-T3.
    Breaking symmetry by choosing a reference direction.
    """
    
    def __init__(self, edge_length: float = 1.0, reference_vector: Optional[np.ndarray] = None):
        """
        Create labeled tetrahedron.
        
        Args:
            edge_length: Edge length
            reference_vector: Vector to determine H0 (default [0,0,1])
        """
        super().__init__(edge_length)
        
        if reference_vector is None:
            reference_vector = np.array([0, 0, 1])
        
        self.reference_vector = reference_vector / np.linalg.norm(reference_vector)
        self._assign_labels()
        
    def _assign_labels(self):
        """
        Assign H0-H3 and T0-T3 labels.
        H0: hex face most aligned with reference vector
        H1-H3: other hexes ordered clockwise when viewed from H0
        Ti parallel to Hi
        """
        hex_faces, tri_faces = self.get_face_indices()
        
        # Find H0 - hex face with normal most aligned with reference
        hex_normals = [self.get_face_normal(face) for face in hex_faces]
        dots = [np.dot(normal, self.reference_vector) for normal in hex_normals]
        h0_idx = np.argmax(dots)
        
        # H0 is found
        self.h0_face = hex_faces[h0_idx]
        self.h0_normal = hex_normals[h0_idx]
        
        # Order remaining hexes clockwise from H0 viewpoint
        other_indices = [i for i in range(4) if i != h0_idx]
        other_centers = [self.get_face_center(hex_faces[i]) for i in other_indices]
        
        # Project to H0 plane and sort clockwise
        ordered = self._clockwise_order(self.h0_normal, other_centers)
        
        # Assign H1, H2, H3
        self.hex_labels = {
            'H0': hex_faces[h0_idx],
            'H1': hex_faces[other_indices[ordered[0]]],
            'H2': hex_faces[other_indices[ordered[1]]],
            'H3': hex_faces[other_indices[ordered[2]]]
        }
        
        # Ti parallel to Hi (same normal direction)
        # Find which tri face has normal parallel to each hex
        tri_normals = [self.get_face_normal(face) for face in tri_faces]
        
        self.tri_labels = {}
        for h_label, h_face in self.hex_labels.items():
            h_normal = self.get_face_normal(h_face)
            # Find parallel tri face
            for i, t_normal in enumerate(tri_normals):
                if np.abs(np.dot(h_normal, t_normal)) > 0.99:  # Parallel or anti-parallel
                    t_label = f'T{h_label[1]}'  # T0, T1, T2, T3
                    self.tri_labels[t_label] = tri_faces[i]
                    break
    
    def _clockwise_order(self, normal: np.ndarray, points: List[np.ndarray]) -> List[int]:
        """
        Order points clockwise when viewed along normal direction.
        """
        # Create orthonormal basis in plane perpendicular to normal
        if abs(normal[0]) < 0.9:
            u = np.cross(normal, [1, 0, 0])
        else:
            u = np.cross(normal, [0, 1, 0])
        u = u / np.linalg.norm(u)
        v = np.cross(normal, u)
        
        # Project points to 2D plane
        angles = []
        for i, point in enumerate(points):
            x = np.dot(point, u)
            y = np.dot(point, v)
            angle = np.arctan2(y, x)
            angles.append((i, angle))
        
        # Sort by angle (clockwise is decreasing angle)
        angles.sort(key=lambda x: -x[1])
        return [i for i, _ in angles]
    
    def get_face(self, label: str) -> List[int]:
        """Get vertex indices for a labeled face."""
        if label in self.hex_labels:
            return self.hex_labels[label]
        elif label in self.tri_labels:
            return self.tri_labels[label]
        else:
            raise ValueError(f"Unknown face label: {label}")
    
    def get_port_pairs(self) -> List[Tuple[str, str]]:
        """Get the H-T parallel pairs (ports)."""
        return [
            ('H0', 'T0'),
            ('H1', 'T1'),
            ('H2', 'T2'),
            ('H3', 'T3')
        ]
