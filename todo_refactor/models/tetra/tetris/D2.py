"""
H-H' Deuterium Viewer
=====================
Simple viewer for the H-H' (rotated hexagon-to-hexagon) deuterium configuration.
"""

import numpy as np
import trimesh
from tetra_model import TruncatedTetrahedron
from deuterium_assemblies import DeuteriumAssembly


def view_hh_prime(show_spheres=True, wireframe=False, show_face_labels=False):
    """
    Create and display the H-H' deuterium configuration.
    
    Args:
        show_spheres: If True, show internal spheres
        wireframe: If True, show as wireframe
        show_face_labels: If True, add markers to identify faces
    """
    print("="*60)
    print("H-H' DEUTERIUM CONFIGURATION VIEWER")
    print("="*60)
    print("\nCreating H-H' configuration (hexagon-to-hexagon rotated π/3)")
    print("Proton = Red, Neutron = Blue\n")
    
    # Create the H-H' assembly
    hh_prime = DeuteriumAssembly()
    hh_prime.assemble_HH(hex_index_p=0, hex_index_n=0, rotated=True)
    
    # Get bonding geometry for analysis
    p_data = hh_prime.proton.get_bonding_geometry()
    n_data = hh_prime.neutron.get_bonding_geometry()
    
    # Identify free faces (those not used in bonding)
    print("FACE ANALYSIS:")
    print("-"*40)
    print(f"Proton hexagon 0: BONDED")
    print(f"Neutron hexagon 0: BONDED")
    print(f"\nFREE FACES (6 total):")
    
    free_faces = []
    
    # Proton free faces (hexagons 1,2,3)
    for i in [1, 2, 3]:
        print(f"  Proton hexagon {i} + truncations")
        free_faces.append(('P', i))
    
    # Neutron free faces (hexagons 1,2,3)
    for i in [1, 2, 3]:
        print(f"  Neutron hexagon {i} + truncations")
        free_faces.append(('N', i))
    
    # Create visualization
    scene = trimesh.Scene()
    
    # Add proton mesh
    p_mesh = hh_prime.proton.create_mesh(with_ports=True, with_truncation_holes=True,
                                         with_sphere=show_spheres, wireframe=wireframe)
    if not wireframe and hasattr(p_mesh, 'visual'):
        p_mesh.visual.vertex_colors = [255, 100, 100, 200]  # Red
    
    # Add neutron mesh
    n_mesh = hh_prime.neutron.create_mesh(with_ports=True, with_truncation_holes=True,
                                          with_sphere=show_spheres, wireframe=wireframe)
    if not wireframe and hasattr(n_mesh, 'visual'):
        n_mesh.visual.vertex_colors = [100, 100, 255, 200]  # Blue
    
    # Add meshes to scene
    if isinstance(p_mesh, trimesh.Scene):
        for name, geom in p_mesh.geometry.items():
            scene.add_geometry(geom, node_name=f'proton_{name}')
    else:
        scene.add_geometry(p_mesh, node_name='proton')
    
    if isinstance(n_mesh, trimesh.Scene):
        for name, geom in n_mesh.geometry.items():
            scene.add_geometry(geom, node_name=f'neutron_{name}')
    else:
        scene.add_geometry(n_mesh, node_name='neutron')
    
    # Add face markers if requested
    if show_face_labels:
        print("\nAdding face markers...")
        
        # Mark proton free hexagon centers
        for i in [1, 2, 3]:
            hex_data = p_data['hexagon_faces'][i]
            marker = trimesh.creation.icosphere(subdivisions=1, radius=0.05)
            marker.vertices += hex_data['center']
            marker.visual.vertex_colors = [255, 255, 0, 255]  # Yellow
            scene.add_geometry(marker, node_name=f'P_hex_{i}_marker')
        
        # Mark neutron free hexagon centers
        for i in [1, 2, 3]:
            hex_data = n_data['hexagon_faces'][i]
            marker = trimesh.creation.icosphere(subdivisions=1, radius=0.05)
            marker.vertices += hex_data['center']
            marker.visual.vertex_colors = [0, 255, 255, 255]  # Cyan
            scene.add_geometry(marker, node_name=f'N_hex_{i}_marker')
    
    # Set camera
    bounds = scene.bounds
    extents = bounds[1] - bounds[0]
    max_extent = np.max(extents)
    
    scene.camera.z_far = max_extent * 10
    scene.camera.z_near = max_extent * 0.01
    scene.set_camera(angles=[np.pi/4, np.pi/4, 0], distance=max_extent*2)
    
    print("\n" + "="*60)
    print("Visualization ready!")
    print("Yellow markers = Proton free face centers")
    print("Cyan markers = Neutron free face centers")
    print("="*60)
    
    scene.show()
    
    return hh_prime


def analyze_hh_prime_faces():
    """
    Analyze the face types (D vs D') in the H-H' configuration.
    """
    print("\nAnalyzing H-H' face types for D/D' classification...")
    print("-"*60)
    
    # Create H-H' assembly
    hh_prime = DeuteriumAssembly()
    hh_prime.assemble_HH(hex_index_p=0, hex_index_n=0, rotated=True)
    
    # Get geometry data
    p_data = hh_prime.proton.get_bonding_geometry()
    n_data = hh_prime.neutron.get_bonding_geometry()
    
    # For each free face, check triangle orientations
    print("\nChecking triangle orientations on free faces:\n")
    
    for nucleon_type, data in [('Proton', p_data), ('Neutron', n_data)]:
        for i in [1, 2, 3]:  # Free hexagon faces
            hex_face = data['hexagon_faces'][i]
            hex_port = data['triangular_ports'][i]
            
            # Find nearest truncation triangle
            min_dist = float('inf')
            nearest_trunc = None
            for j, trunc in enumerate(data['truncation_triangles']):
                dist = np.linalg.norm(hex_face['center'] - trunc['center'])
                if dist < min_dist:
                    min_dist = dist
                    nearest_trunc = j
            
            print(f"{nucleon_type} Face {i}:")
            print(f"  Hexagon normal: {hex_face['normal']}")
            print(f"  Nearest truncation: {nearest_trunc} at distance {min_dist:.3f}")
            
            # TODO: Determine if triangles are aligned (D') or mirrored (D)
            # This requires checking the relative orientation of the port triangle
            # vertices vs the truncation triangle vertices
    
    return hh_prime


if __name__ == "__main__":
    # Simple viewer
    print("Viewing H-H' configuration...\n")
    hh_prime = view_hh_prime(show_spheres=True, wireframe=False, show_face_labels=True)
    
    # Optionally analyze faces
    # analyze_hh_prime_faces()
