#!/usr/bin/env python3
# test_tetrahedral_cluster.py
"""
Test and visualize the tetrahedral cluster.
"""

import sys
import numpy as np
sys.path.append('nuclear_assembly')

from assemblies.tetrahedral_cluster import TetrahedralCluster
from io_modules.visualizer import UnifiedVisualizer
import trimesh

def visualize_cluster():
    """Visualize the tetrahedral cluster."""
    print("Creating tetrahedral cluster...\n")
    
    cluster = TetrahedralCluster(bond_rotation=0)
    cluster.report_geometry()
    
    # Create visualization
    viz = UnifiedVisualizer()
    
    # Add center (inverted) - make it a different color
    viz._add_clean_tetrahedron(
        cluster.center,
        name='center',
        color=[255, 255, 100, 200],  # Yellow for center
        wireframe=False
    )
    
    # Add satellites
    colors = [
        [255, 100, 100, 200],  # Red
        [100, 255, 100, 200],  # Green  
        [100, 100, 255, 200],  # Blue
    ]
    
    for i, (sat, color) in enumerate(zip(cluster.satellites, colors)):
        viz._add_clean_tetrahedron(
            sat,
            name=f'sat{i+1}',
            color=color,
            wireframe=False
        )
    
    # Add bond indicators
    for bond in cluster.bonds:
        # Get face centers
        if bond['from'][0] == 'center':
            from_tet = cluster.center
        else:
            sat_idx = int(bond['from'][0][-1]) - 1
            from_tet = cluster.satellites[sat_idx]
            
        if bond['to'][0] == 'center':
            to_tet = cluster.center
        else:
            sat_idx = int(bond['to'][0][-1]) - 1
            to_tet = cluster.satellites[sat_idx]
        
        from_face = from_tet.get_face(bond['from'][1])
        to_face = to_tet.get_face(bond['to'][1])
        
        from_center = from_tet.get_face_center(from_face)
        to_center = to_tet.get_face_center(to_face)
        
        # Create bond line
        bond_line = trimesh.creation.cylinder(
            radius=0.01,
            height=np.linalg.norm(to_center - from_center),
            sections=8
        )
        
        # Orient
        direction = to_center - from_center
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
        
        bond_line.vertices += (from_center + to_center) / 2
        bond_line.visual.vertex_colors = [0, 255, 0, 150]
        
        viz.scene.add_geometry(bond_line)
    
    print("\nVisualization:")
    print("  Yellow = Center (inverted)")
    print("  Red/Green/Blue = Satellites")
    print("  Green cylinders = H-H bonds")
    
    viz._setup_camera()
    viz.scene.show()

if __name__ == "__main__":
    visualize_cluster()
