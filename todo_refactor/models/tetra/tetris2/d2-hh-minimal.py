#!/usr/bin/env python3
# visualize_d2_fixed.py
"""
Fixed visualizer for D2 assembly using trimesh.
Properly shows all faces and H-H bonding.
"""

import sys
import os
import numpy as np
import trimesh
sys.path.append('nuclear_assembly')

from assemblies.d2 import D2Unit
from geometry.face_labeling import LabeledTetrahedron


def create_complete_tetrahedron_mesh(tet: LabeledTetrahedron, color=[100, 100, 255, 200]):
    """
    Create a complete trimesh object from a LabeledTetrahedron.
    Shows all faces properly.
    
    Args:
        tet: LabeledTetrahedron object
        color: RGBA color
    
    Returns:
        trimesh.Trimesh object
    """
    all_faces = []
    
    # Create all 4 hexagonal faces
    for i in range(4):
        hex_label = f'H{i}'
        hex_face_indices = tet.get_face(hex_label)
        
        # Triangulate hexagon using fan method from first vertex
        for j in range(1, len(hex_face_indices) - 1):
            face = [hex_face_indices[0], hex_face_indices[j], hex_face_indices[j + 1]]
            all_faces.append(face)
    
    # Create all 4 triangular faces (truncations)
    for i in range(4):
        tri_label = f'T{i}'
        tri_face_indices = tet.get_face(tri_label)
        all_faces.append(tri_face_indices)
    
    # Create mesh
    mesh = trimesh.Trimesh(
        vertices=tet.vertices,
        faces=all_faces,
        process=True
    )
    
    # Set color
    mesh.visual.vertex_colors = color
    
    # Fix normals to ensure they point outward
    mesh.fix_normals()
    
    return mesh


def visualize_d2_complete():
    """
    Create and visualize a complete D2 assembly with H-H bonding.
    """
    print("Creating D2 assembly with H-H bond...")
    
    # Create D2 unit
    d2 = D2Unit()
    
    # Create complete meshes for proton and neutron
    proton_mesh = create_complete_tetrahedron_mesh(
        d2.proton, 
        color=[255, 100, 100, 180]  # Red, semi-transparent
    )
    neutron_mesh = create_complete_tetrahedron_mesh(
        d2.neutron, 
        color=[100, 100, 255, 180]  # Blue, semi-transparent
    )
    
    # Create scene
    scene = trimesh.Scene()
    scene.add_geometry(proton_mesh, node_name='proton')
    scene.add_geometry(neutron_mesh, node_name='neutron')
    
    # Add markers for the bonded H0 faces
    p_h0_center = d2.proton.get_face_center(d2.proton.get_face('H0'))
    p_h0_marker = trimesh.creation.icosphere(subdivisions=2, radius=0.05)
    p_h0_marker.vertices += p_h0_center
    p_h0_marker.visual.vertex_colors = [255, 255, 0, 255]  # Yellow
    scene.add_geometry(p_h0_marker, node_name='proton_H0')
    
    n_h0_center = d2.neutron.get_face_center(d2.neutron.get_face('H0'))
    n_h0_marker = trimesh.creation.icosphere(subdivisions=2, radius=0.05)
    n_h0_marker.vertices += n_h0_center
    n_h0_marker.visual.vertex_colors = [0, 255, 255, 255]  # Cyan
    scene.add_geometry(n_h0_marker, node_name='neutron_H0')
    
    # Add bond indicator
    bond_path = np.array([p_h0_center, n_h0_center])
    bond_line = trimesh.load_path(bond_path)
    scene.add_geometry(bond_line, node_name='H0_H0_bond')
    
    # Print info
    print("\nD2 Assembly created:")
    print(f"  Bond: H0(proton) <-> H0(neutron)")
    print(f"  Bond type: {d2.bond['type']}")
    print(f"  Free faces on proton: {d2.get_free_faces()['proton']}")
    print(f"  Free faces on neutron: {d2.get_free_faces()['neutron']}")
    
    # Set camera
    bounds = scene.bounds
    extents = bounds[1] - bounds[0]
    max_extent = np.max(extents)
    
    scene.set_camera(
        angles=[np.pi/4, np.pi/4, 0], 
        distance=max_extent * 3,
        fov=[60, 60]
    )
    
    print("\nVisualization key:")
    print("  Red = Proton")
    print("  Blue = Neutron")
    print("  Yellow sphere = Proton H0 face center (bonded)")
    print("  Cyan sphere = Neutron H0 face center (bonded)")
    print("  Line = H0-H0 bond")
    
    scene.show()
    
    return d2, scene


def visualize_d2_wireframe():
    """
    Wireframe visualization to see structure clearly.
    """
    print("Creating D2 wireframe visualization...")
    
    # Create D2 unit
    d2 = D2Unit()
    
    # Create scene
    scene = trimesh.Scene()
    
    # Add edges for both tetrahedra
    for name, tet, color in [
        ('proton', d2.proton, [255, 0, 0, 255]),
        ('neutron', d2.neutron, [0, 0, 255, 255])
    ]:
        edges = []
        
        # Get all edges from faces
        # Hexagon edges
        for i in range(4):
            hex_face = tet.get_face(f'H{i}')
            for j in range(len(hex_face)):
                v1_idx = hex_face[j]
                v2_idx = hex_face[(j+1) % len(hex_face)]
                edges.append([v1_idx, v2_idx])
        
        # Triangle edges
        for i in range(4):
            tri_face = tet.get_face(f'T{i}')
            for j in range(3):
                v1_idx = tri_face[j]
                v2_idx = tri_face[(j+1) % 3]
                edges.append([v1_idx, v2_idx])
        
        # Remove duplicates
        unique_edges = []
        seen = set()
        for edge in edges:
            edge_tuple = tuple(sorted(edge))
            if edge_tuple not in seen:
                seen.add(edge_tuple)
                unique_edges.append(edge)
        
        # Create path3D
        path = trimesh.path.Path3D(
            entities=[trimesh.path.entities.Line(e) for e in unique_edges],
            vertices=tet.vertices,
            colors=[color] * len(unique_edges)
        )
        
        scene.add_geometry(path, node_name=f'{name}_edges')
    
    # Highlight bonded faces
    p_h0_verts = d2.proton.vertices[d2.proton.get_face('H0')]
    n_h0_verts = d2.neutron.vertices[d2.neutron.get_face('H0')]
    
    # Add filled hexagons for bonded faces
    p_h0_mesh = trimesh.creation.extrude_polygon(
        trimesh.path.Path2D.from_polygon(p_h0_verts[:, :2]),
        height=0.001
    )
    p_h0_mesh.vertices[:, 2] = np.mean(p_h0_verts[:, 2])
    p_h0_mesh.visual.face_colors = [255, 200, 200, 100]
    
    # Set camera
    bounds = scene.bounds
    extents = bounds[1] - bounds[0]
    max_extent = np.max(extents)
    
    scene.set_camera(
        angles=[np.pi/4, np.pi/4, 0],
        distance=max_extent * 3
    )
    
    scene.show()
    
    return d2, scene


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize D2 assembly')
    parser.add_argument('--wireframe', action='store_true',
                       help='Show as wireframe')
    args = parser.parse_args()
    
    if args.wireframe:
        d2, scene = visualize_d2_wireframe()
    else:
        d2, scene = visualize_d2_complete()
