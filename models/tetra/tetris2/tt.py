#!/usr/bin/env python3
# test_tetra_debug.py
"""
Debug the triangular face rendering issue.
"""

import sys
import numpy as np
sys.path.append('nuclear_assembly')

from geometry.tetra_base import TruncatedTetrahedron
import trimesh

def test_single_nucleon():
    """Debug triangular face orientation."""
    
    print("Creating truncated tetrahedron...")
    
    # Create a truncated tetrahedron
    tt = TruncatedTetrahedron(edge_length=1.0)
    
    # Get faces
    hex_faces, tri_faces = tt.get_face_indices()
    
    print(f"\nTriangular faces indices:")
    for i, tri in enumerate(tri_faces):
        print(f"  T{i}: {tri}")
        # Check if vertices are ordered correctly
        v0 = tt.vertices[tri[0]]
        v1 = tt.vertices[tri[1]]
        v2 = tt.vertices[tri[2]]
        
        # Calculate normal
        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = np.cross(edge1, edge2)
        normal = normal / np.linalg.norm(normal)
        
        # Check if pointing outward
        center = np.mean(tt.vertices, axis=0)
        face_center = np.mean([v0, v1, v2], axis=0)
        dot = np.dot(normal, face_center - center)
        
        print(f"    Normal dot product: {dot:.3f} {'(outward)' if dot > 0 else '(INWARD - NEEDS FLIP)'}")
        
    # Create separate meshes for hex and tri faces to debug
    print("\nCreating separate meshes for debugging...")
    
    # Hexagonal faces mesh
    hex_triangles = []
    for hex_face in hex_faces:
        for i in range(1, len(hex_face) - 1):
            hex_triangles.append([hex_face[0], hex_face[i], hex_face[i+1]])
    
    hex_mesh = trimesh.Trimesh(
        vertices=tt.vertices,
        faces=hex_triangles
    )
    hex_mesh.visual.face_colors = [100, 100, 255, 200]  # Blue
    
    # Triangular faces mesh - with corrected winding
    tri_triangles = []
    for i, tri in enumerate(tri_faces):
        # Check normal direction
        v0 = tt.vertices[tri[0]]
        v1 = tt.vertices[tri[1]]
        v2 = tt.vertices[tri[2]]
        
        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = np.cross(edge1, edge2)
        normal = normal / np.linalg.norm(normal)
        
        center = np.mean(tt.vertices, axis=0)
        face_center = np.mean([v0, v1, v2], axis=0)
        
        if np.dot(normal, face_center - center) < 0:
            # Flip winding order
            print(f"  Flipping T{i} winding order")
            tri_triangles.append([tri[0], tri[2], tri[1]])
        else:
            tri_triangles.append(tri)
    
    tri_mesh = trimesh.Trimesh(
        vertices=tt.vertices,
        faces=tri_triangles
    )
    tri_mesh.visual.face_colors = [255, 100, 100, 200]  # Red
    
    # Combine meshes
    combined = trimesh.util.concatenate([hex_mesh, tri_mesh])
    
    print("\nShowing combined mesh:")
    print("  Blue = Hexagonal faces")
    print("  Red = Triangular faces")
    print("  All faces should be visible now")
    
    combined.show()

if __name__ == "__main__":
    test_single_nucleon()
