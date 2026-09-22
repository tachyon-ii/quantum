"""
Base truncated tetrahedron geometry.
Pure geometry with 4 hexagons (with triangular ports) and 4 truncation triangles.
All edges = 1.0
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
import json


class TruncatedTetrahedron:
    """
    Pure truncated tetrahedron geometry.
    No species, no colors - just vertices and topology.
    """
    
    def __init__(self, edge_length: float = 1.0):
        """
        Create a truncated tetrahedron with given edge length.
        
        Args:
            edge_length: Length of all edges (default 1.0)
        """
        self.edge_length = edge_length
        self.vertices = self._generate_vertices()
        
        # Face labels will be assigned when symmetry is broken
        self.face_labels = None
        self.hex_faces = None  # Will store H0-H3 indices
        self.tri_faces = None  # Will store T0-T3 indices
        
    def _generate_vertices(self) -> np.ndarray:
        """
        Generate the 12 vertices of a truncated tetrahedron.
        Start with regular tetrahedron and truncate at 1/3 edge length.
        """
        # Regular tetrahedron vertices (before scaling)
        tet_vertices = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1]
        ], dtype=float)
        
        # Scale for desired edge length
        # For a regular tetrahedron with edge length a, vertices are at distance a/sqrt(8)
        scale = self.edge_length / np.sqrt(8) * 3  # Scale up by 3 before truncation
        tet_vertices = tet_vertices * scale
        
        # Generate truncated vertices (12 total)
        # Each original vertex becomes 3 vertices
        truncated_vertices = []
        
        for i, vertex in enumerate(tet_vertices):
            # For each vertex, find the three edges connected to it
            for j, other_vertex in enumerate(tet_vertices):
                if i != j:
                    # Create a vertex 1/3 of the way from vertex to other_vertex
                    new_vertex = vertex + (other_vertex - vertex) / 3
                    truncated_vertices.append(new_vertex)
        
        return np.array(truncated_vertices)
    
    def get_face_indices(self) -> Tuple[List[List[int]], List[List[int]]]:
        """
        Get the vertex indices for hexagonal and triangular faces.
        Returns (hex_faces, tri_faces) before labeling.
        """
        # Hexagon faces (4 total) - indices into vertices array
        # These correspond to the original tetrahedron faces
        hex_faces = [
            [0, 3, 4, 7, 6, 1],    # Face opposite to vertex 3
            [0, 2, 9, 10, 5, 3],   # Face opposite to vertex 2  
            [1, 6, 8, 11, 9, 2],   # Face opposite to vertex 1
            [11, 8, 7, 4, 5, 10]   # Face opposite to vertex 0
        ]
        
        # Triangle faces (4 total) - where vertices were truncated
        tri_faces = [
            [0, 1, 2],    # Truncation of vertex 0
            [3, 4, 5],    # Truncation of vertex 1
            [6, 7, 8],    # Truncation of vertex 2
            [9, 10, 11]   # Truncation of vertex 3
        ]
        
        return hex_faces, tri_faces
    
    def get_face_normal(self, face_indices: List[int]) -> np.ndarray:
        """Calculate outward normal for a face."""
        v0 = self.vertices[face_indices[0]]
        v1 = self.vertices[face_indices[1]]
        v2 = self.vertices[face_indices[2]]
        
        # Calculate normal via cross product
        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = np.cross(edge1, edge2)
        normal = normal / np.linalg.norm(normal)
        
        # Ensure outward direction
        center = np.mean(self.vertices, axis=0)
        face_center = np.mean(self.vertices[face_indices], axis=0)
        if np.dot(normal, face_center - center) < 0:
            normal = -normal
            
        return normal
    
    def get_face_center(self, face_indices: List[int]) -> np.ndarray:
        """Get the centroid of a face."""
        return np.mean(self.vertices[face_indices], axis=0)
    
    def to_dict(self) -> Dict:
        """Export geometry as dictionary."""
        hex_faces, tri_faces = self.get_face_indices()
        
        return {
            'edge_length': self.edge_length,
            'vertices': self.vertices.tolist(),
            'hex_faces': hex_faces,
            'tri_faces': tri_faces
        }
