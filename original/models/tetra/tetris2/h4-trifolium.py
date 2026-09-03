#!/usr/bin/env python3
# test_tetrahedral_cluster_rotated.py
"""
Test tetrahedral cluster with individual satellite rotations.
"""

import sys
import numpy as np
sys.path.append('nuclear_assembly')

from assemblies.tetrahedral_cluster import TetrahedralCluster
from io_modules.visualizer import UnifiedVisualizer
import trimesh

def visualize_cluster_with_rotation(rotations):
    """Visualize the tetrahedral cluster with specified rotations."""
    
    print(f"Creating tetrahedral cluster with rotations: {rotations}°...\n")
    
    cluster = TetrahedralCluster(sat_rotations=rotations)  # Use the passed rotations!
    cluster.report_geometry()
    
    # Create visualization
    viz = UnifiedVisualizer()
    
    # Add center (inverted) - yellow
    viz._add_clean_tetrahedron(
        cluster.center,
        name='center',
        color=[255, 255, 100, 200],  # Yellow for center
        wireframe=False
    )
    
    # Add satellites with labels
    satellites_info = [
        (f'Red (rotated {rotations[0]}°)', [255, 100, 100, 200]),  
        (f'Green (rotated {rotations[1]}°)', [100, 255, 100, 200]),
        (f'Blue (rotated {rotations[2]}°)', [100, 100, 255, 200])
    ]
    
    for i, (sat, (label, color)) in enumerate(zip(cluster.satellites, satellites_info)):
        viz._add_clean_tetrahedron(
            sat,
            name=f'sat{i+1}',
            color=color,
            wireframe=False
        )
        print(f"  Satellite {i+1}: {label}")
    
    # Add bond cylinders (simplified - just center to satellites)
    for i, sat in enumerate(cluster.satellites):
        center_face = cluster.center.get_face(f'H{i+1}')
        sat_face = sat.get_face('H0')
        
        center_point = cluster.center.get_face_center(center_face)
        sat_point = sat.get_face_center(sat_face)
        
        bond_line = trimesh.creation.cylinder(
            radius=0.01,
            height=np.linalg.norm(sat_point - center_point),
            sections=8
        )
        
        # Orient cylinder
        direction = sat_point - center_point
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
            z_axis = np.array([0, 0, 1])
            if not np.allclose(direction, z_axis):
                axis = np.cross(z_axis, direction)
                if np.linalg.norm(axis) > 0:
                    axis = axis / np.linalg.norm(axis)
                    angle = np.arccos(np.clip(np.dot(z_axis, direction), -1, 1))
                    K = np.array([[0, -axis[2], axis[1]],
                                  [axis[2], 0, -axis[0]],
                                  [-axis[1], axis[0], 0]])
                    R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * np.dot(K, K)
                    bond_line.vertices = (R @ bond_line.vertices.T).T
        
        bond_line.vertices += (center_point + sat_point) / 2
        bond_line.visual.vertex_colors = [0, 255, 0, 150]
        viz.scene.add_geometry(bond_line)
    
    print("\nVisualization:")
    print("  Yellow = Center (inverted)")
    print("  Red = Satellite 1")
    print("  Green = Satellite 2")
    print("  Blue = Satellite 3")
    print("  Green cylinders = H-H bonds")
    
    viz._setup_camera()
    viz.scene.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--rotate', nargs=3, type=float, default=[60, 0, 60],
                       help='Rotation angles for sat1, sat2, sat3 (default: 60 0 60)')
    args = parser.parse_args()
    
    # Use the command line arguments!
    visualize_cluster_with_rotation(args.rotate)
