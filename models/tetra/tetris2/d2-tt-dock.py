#!/usr/bin/env python3
# test_tt_variant_full.py
"""
Test and visualize T-T variant with crossed bonds.
"""

import sys
import numpy as np
sys.path.append('nuclear_assembly')

from assemblies.d2_tt_variant import D2_TT_Variant
from io_modules.visualizer import UnifiedVisualizer
import trimesh

def visualize_with_crossed_bonds(d2_tt):
    """Visualize T-T variant with potential crossed bonds shown."""
    viz = UnifiedVisualizer()
    
    # Create basic visualization
    class MockD2:
        def __init__(self, d2_tt):
            self.proton = d2_tt.proton
            self.neutron = d2_tt.neutron
            self.bond = d2_tt.central_bond
    
    mock = MockD2(d2_tt)
    viz.visualize_assembly(mock, show_ports=True, port_rotation='edges')
    
    # Add lines for feasible crossed bonds
    feasible = [b for b in d2_tt.crossed_bonds if b['feasible']]
    
    for bond in feasible[:6]:  # Show first 6 crossed bonds
        # Get face centers
        if bond['from'][0] == 'proton':
            from_center = d2_tt.proton.get_face_center(
                d2_tt.proton.get_face(bond['from'][1]))
        else:
            from_center = d2_tt.neutron.get_face_center(
                d2_tt.neutron.get_face(bond['from'][1]))
            
        if bond['to'][0] == 'neutron':
            to_center = d2_tt.neutron.get_face_center(
                d2_tt.neutron.get_face(bond['to'][1]))
        else:
            to_center = d2_tt.proton.get_face_center(
                d2_tt.proton.get_face(bond['to'][1]))
        
        # Create line for potential bond
        bond_line = trimesh.creation.cylinder(
            radius=0.005,  # Thinner than main bond
            height=np.linalg.norm(to_center - from_center)
        )
        
        # Orient and position
        direction = to_center - from_center
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
            # Create rotation to align cylinder
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
        
        # Color based on bond type
        if bond['type'] == 'HH':
            color = [255, 128, 0, 100]  # Orange for H-H crosses
        else:
            color = [0, 255, 128, 100]  # Green-cyan for H-T crosses
            
        bond_line.visual.vertex_colors = color
        viz.scene.add_geometry(bond_line, node_name=f"crossed_{bond['from'][1]}_{bond['to'][1]}")
    
    print(f"\nShowing {len(feasible)} potential crossed bonds as orange cylinders")
    print("Main T-T bond shown in green")
    
    viz.scene.show()

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Test T-T variant D2')
    parser.add_argument('--twist', type=float, default=0, 
                       help='T-T bond twist angle in degrees')
    args = parser.parse_args()
    
    print(f"Testing T-T variant with {args.twist}° twist\n")
    d2_tt = D2_TT_Variant(tt_twist=args.twist)
    d2_tt.report_geometry()
    
    print("\nVisualizing with crossed bonds...")
    visualize_with_crossed_bonds(d2_tt)

if __name__ == "__main__":
    main()
