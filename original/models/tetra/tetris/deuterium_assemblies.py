"""
Deuterium (D2) Assembly Configurations
=======================================
This module uses the TruncatedTetrahedron to assemble all possible
bonding configurations of deuterium (one proton + one neutron).

Bonding modes:
1. T-T: Truncation triangle to truncation triangle
2. T-H: Truncation triangle to hexagon face (triangular port)
3. H-H: Hexagon to hexagon (aligned ports)
4. H-H rotated: Hexagon to hexagon with π/3 rotation (ports form hexagon)
"""

import numpy as np
import trimesh
from tetra_model import TruncatedTetrahedron  # Import from the module we just created

class DeuteriumAssembly:
    """
    Creates and visualizes different bonding configurations of deuterium.
    Proton = red, Neutron = blue
    """
    
    def __init__(self, edge_length=1.0):
        self.edge_length = edge_length
        self.proton = None
        self.neutron = None
        self.assembly_type = None
        
    def create_nucleons(self):
        """Create the proton and neutron tetrahedra."""
        self.proton = TruncatedTetrahedron(edge_length=self.edge_length)
        self.neutron = TruncatedTetrahedron(edge_length=self.edge_length)
    
    def _rotation_matrix_between_vectors(self, v1, v2):
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
    
    def _rotation_matrix_around_axis(self, axis, angle):
        """Create rotation matrix for rotation around axis by angle."""
        axis = axis / np.linalg.norm(axis)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        ux, uy, uz = axis
        
        return np.array([
            [cos_a + ux**2*(1-cos_a), ux*uy*(1-cos_a) - uz*sin_a, ux*uz*(1-cos_a) + uy*sin_a],
            [uy*ux*(1-cos_a) + uz*sin_a, cos_a + uy**2*(1-cos_a), uy*uz*(1-cos_a) - ux*sin_a],
            [uz*ux*(1-cos_a) - uy*sin_a, uz*uy*(1-cos_a) + ux*sin_a, cos_a + uz**2*(1-cos_a)]
        ])

    def assemble_TT(self, truncation_index_p=0, truncation_index_n=0):
        """
        Assemble truncation-to-truncation configuration.
        
        Args:
            truncation_index_p: Which truncation triangle of proton (0-3)
            truncation_index_n: Which truncation triangle of neutron (0-3)
        """
        self.create_nucleons()
        self.assembly_type = "T-T"
        
        # Get bonding geometry
        p_data = self.proton.get_bonding_geometry()
        n_data = self.neutron.get_bonding_geometry()
        
        # Get truncation triangles
        p_trunc = p_data['truncation_triangles'][truncation_index_p]
        n_trunc = n_data['truncation_triangles'][truncation_index_n]
        
        # Calculate transformation to align neutron truncation with proton truncation
        # Neutron normal should point opposite to proton normal
        target_normal = -p_trunc['normal']
        current_normal = n_trunc['normal']
        
        # Calculate rotation to align normals
        rotation = self._rotation_matrix_between_vectors(current_normal, target_normal)
        
        # Apply rotation to neutron vertices
        self.neutron.vertices = (rotation @ self.neutron.vertices.T).T
        
        # Recalculate neutron geometry after rotation
        n_data = self.neutron.get_bonding_geometry()
        n_trunc = n_data['truncation_triangles'][truncation_index_n]
        
        # Calculate translation to align centers
        # Small separation to prevent overlap
        separation = 0.01
        translation = p_trunc['center'] + p_trunc['normal'] * separation - n_trunc['center']
        
        # Apply translation
        self.neutron.vertices += translation
        
        print(f"Assembled T-T configuration:")
        print(f"  Proton truncation {truncation_index_p} to Neutron truncation {truncation_index_n}")

    def assemble_TH(self, truncation_index=0, hexagon_index=0, is_proton_truncation=True, rotated=False):
        """
        Assemble truncation-to-hexagon configuration.

        Args:
            truncation_index: Which truncation triangle (0-3)
            hexagon_index: Which hexagon face (0-3)
            is_proton_truncation: If True, proton truncation to neutron hexagon
            rotated: If True, apply +π/3 rotation for T-H' configuration
                     If False, apply -π/3 rotation for T-H configuration
        """
        self.create_nucleons()
        self.assembly_type = "T-H'" if rotated else "T-H"

        # Get bonding geometry
        p_data = self.proton.get_bonding_geometry()
        n_data = self.neutron.get_bonding_geometry()

        if is_proton_truncation:
            # Proton truncation to neutron hexagon
            p_trunc = p_data['truncation_triangles'][truncation_index]
            n_hex = n_data['hexagon_faces'][hexagon_index]

            # First align normals (proton truncation normal opposite to neutron hexagon normal)
            target_normal = -n_hex['normal']
            current_normal = p_trunc['normal']

            # Rotate proton to align normals
            rotation = self._rotation_matrix_between_vectors(current_normal, target_normal)
            self.proton.vertices = (rotation @ self.proton.vertices.T).T

            # Recalculate after first rotation
            p_data = self.proton.get_bonding_geometry()
            p_trunc = p_data['truncation_triangles'][truncation_index]

            # Apply the appropriate rotation for alignment with hexagon port
            if rotated:
                # T-H': +π/3 rotation (this is currently working correctly)
                rot_angle = np.pi/3
            else:
                # T-H: -π/3 rotation (this fixes the alignment issue)
                rot_angle = -np.pi/3

            rot_matrix = self._rotation_matrix_around_axis(target_normal, rot_angle)
            self.proton.vertices = (rot_matrix @ self.proton.vertices.T).T

            # Recalculate after rotation
            p_data = self.proton.get_bonding_geometry()
            p_trunc = p_data['truncation_triangles'][truncation_index]

            # Translate to align centers
            separation = 0.01
            translation = n_hex['center'] - n_hex['normal'] * separation - p_trunc['center']
            self.proton.vertices += translation

            config_type = "T-H' (+π/3)" if rotated else "T-H (-π/3)"
            print(f"Assembled {config_type} configuration:")
            print(f"  Proton truncation {truncation_index} to Neutron hexagon {hexagon_index}")
        else:
            # Neutron truncation to proton hexagon
            n_trunc = n_data['truncation_triangles'][truncation_index]
            p_hex = p_data['hexagon_faces'][hexagon_index]

            # Align normals
            target_normal = -p_hex['normal']
            current_normal = n_trunc['normal']

            rotation = self._rotation_matrix_between_vectors(current_normal, target_normal)
            self.neutron.vertices = (rotation @ self.neutron.vertices.T).T

            # Recalculate
            n_data = self.neutron.get_bonding_geometry()
            n_trunc = n_data['truncation_triangles'][truncation_index]

            # Apply the appropriate rotation
            if rotated:
                # T-H': +π/3 rotation
                rot_angle = np.pi/3
            else:
                # T-H: -π/3 rotation
                rot_angle = -np.pi/3

            rot_matrix = self._rotation_matrix_around_axis(target_normal, rot_angle)
            self.neutron.vertices = (rot_matrix @ self.neutron.vertices.T).T

            # Recalculate
            n_data = self.neutron.get_bonding_geometry()
            n_trunc = n_data['truncation_triangles'][truncation_index]

            # Translate
            separation = 0.01
            translation = p_hex['center'] - p_hex['normal'] * separation - n_trunc['center']
            self.neutron.vertices += translation

            config_type = "T-H' (+π/3)" if rotated else "T-H (-π/3)"
            print(f"Assembled {config_type} configuration:")
            print(f"  Neutron truncation {truncation_index} to Proton hexagon {hexagon_index}")

    def assemble_HH(self, hex_index_p=0, hex_index_n=0, rotated=False):
        """
        Assemble hexagon-to-hexagon configuration.

        Args:
            hex_index_p: Which hexagon face of proton (0-3)
            hex_index_n: Which hexagon face of neutron (0-3)
            rotated: If True, rotate by π/3 so triangular ports form hexagon
        """
        self.create_nucleons()
        self.assembly_type = "H-H (rotated)" if rotated else "H-H"

        # Get bonding geometry
        p_data = self.proton.get_bonding_geometry()
        n_data = self.neutron.get_bonding_geometry()

        # Get hexagon faces
        p_hex = p_data['hexagon_faces'][hex_index_p]
        n_hex = n_data['hexagon_faces'][hex_index_n]

        # Align neutron hexagon with proton hexagon
        target_normal = -p_hex['normal']
        current_normal = n_hex['normal']

        # Calculate rotation to align normals
        rotation = self._rotation_matrix_between_vectors(current_normal, target_normal)

        # Apply rotation to neutron
        self.neutron.vertices = (rotation @ self.neutron.vertices.T).T

        # If rotated configuration, add π/3 rotation around the normal
        if rotated:
            # Rotate around the aligned normal by 60 degrees
            rot_60 = self._rotation_matrix_around_axis(target_normal, np.pi/3)
            self.neutron.vertices = (rot_60 @ self.neutron.vertices.T).T

        # Recalculate neutron geometry after rotation
        n_data = self.neutron.get_bonding_geometry()
        n_hex = n_data['hexagon_faces'][hex_index_n]

        # Calculate translation to align centers
        separation = 0.01
        translation = p_hex['center'] + p_hex['normal'] * separation - n_hex['center']

        # Apply translation
        self.neutron.vertices += translation

        config_name = "H-H (60° rotated)" if rotated else "H-H (aligned)"
        print(f"Assembled {config_name} configuration:")
        print(f"  Proton hexagon {hex_index_p} to Neutron hexagon {hex_index_n}")

    def _rotation_matrix_between_vectors(self, v1, v2):
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

    def _rotation_matrix_around_axis(self, axis, angle):
        """Create rotation matrix for rotation around axis by angle."""
        axis = axis / np.linalg.norm(axis)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        ux, uy, uz = axis

        return np.array([
            [cos_a + ux**2*(1-cos_a), ux*uy*(1-cos_a) - uz*sin_a, ux*uz*(1-cos_a) + uy*sin_a],
            [uy*ux*(1-cos_a) + uz*sin_a, cos_a + uy**2*(1-cos_a), uy*uz*(1-cos_a) - ux*sin_a],
            [uz*ux*(1-cos_a) - uy*sin_a, uz*uy*(1-cos_a) + ux*sin_a, cos_a + uz**2*(1-cos_a)]
            ])

    def visualize(self, show_spheres=True, wireframe=False):
        """
        Visualize the assembled deuterium configuration.

        Args:
            show_spheres: If True, show internal spheres
            wireframe: If True, show as wireframe
        """
        if self.proton is None or self.neutron is None:
            print("No assembly created yet!")
            return

        # Create meshes for both nucleons
        p_mesh = self.proton.create_mesh(with_ports=True, with_truncation_holes=True,
                                         with_sphere=show_spheres, wireframe=wireframe)
        n_mesh = self.neutron.create_mesh(with_ports=True, with_truncation_holes=True,
                                          with_sphere=show_spheres, wireframe=wireframe)

        # Set colors
        if not wireframe:
            # Proton = red
            if hasattr(p_mesh, 'visual'):
                p_mesh.visual.vertex_colors = [255, 100, 100, 200]

            # Neutron = blue  
            if hasattr(n_mesh, 'visual'):
                n_mesh.visual.vertex_colors = [100, 100, 255, 200]

        # Create scene
        scene = trimesh.Scene()

        # Add geometries based on type
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

        # Set view
        bounds = scene.bounds
        extents = bounds[1] - bounds[0]
        max_extent = np.max(extents)

        scene.camera.z_far = max_extent * 10
        scene.camera.z_near = max_extent * 0.01
        scene.set_camera(angles=[np.pi/4, np.pi/4, 0], distance=max_extent*2)

        # Add title based on assembly type
        print(f"\nShowing {self.assembly_type} configuration")

        scene.show()

def demonstrate_all_configurations(show_mode='sequential'):
    """
    Create and visualize all FIVE deuterium bonding configurations.
    
    Args:
        show_mode: 'sequential' (one at a time), 'combined' (all in one scene),
                   or 'grid' (arranged in a grid)
    """
    
    print("="*60)
    print("DEUTERIUM (D2) ASSEMBLY CONFIGURATIONS")
    print("="*60)
    print("\nProton = Red, Neutron = Blue")
    print("Showing all 5 configurations: T-T, T-H, T-H', H-H, H-H'\n")
    
    if show_mode == 'combined' or show_mode == 'grid':
        # Create all configurations and show in one scene
        configurations = []
        
        # Configuration 1: T-T
        print("1. Creating TRUNCATION-TO-TRUNCATION (T-T)")
        d2_tt = DeuteriumAssembly()
        d2_tt.assemble_TT(truncation_index_p=0, truncation_index_n=0)
        configurations.append(('T-T', d2_tt))
        
        # Configuration 2: T-H (with π/6 base rotation)
        print("2. Creating TRUNCATION-TO-HEXAGON (T-H)")
        d2_th = DeuteriumAssembly()
        d2_th.assemble_TH(truncation_index=0, hexagon_index=0, 
                         is_proton_truncation=True, rotated=False)
        configurations.append(('T-H', d2_th))
        
        # Configuration 3: T-H' (with π/6 + π/3 rotation)
        print("3. Creating TRUNCATION-TO-HEXAGON ROTATED (T-H')")
        d2_th_rot = DeuteriumAssembly()
        d2_th_rot.assemble_TH(truncation_index=0, hexagon_index=0, 
                             is_proton_truncation=True, rotated=True)
        configurations.append(("T-H'", d2_th_rot))
        
        # Configuration 4: H-H aligned
        print("4. Creating HEXAGON-TO-HEXAGON ALIGNED (H-H)")
        d2_hh = DeuteriumAssembly()
        d2_hh.assemble_HH(hex_index_p=0, hex_index_n=0, rotated=False)
        configurations.append(('H-H', d2_hh))
        
        # Configuration 5: H-H' rotated
        print("5. Creating HEXAGON-TO-HEXAGON ROTATED (H-H')")
        d2_hh_rot = DeuteriumAssembly()
        d2_hh_rot.assemble_HH(hex_index_p=0, hex_index_n=0, rotated=True)
        configurations.append(("H-H'", d2_hh_rot))
        
        # Show all in one scene
        if show_mode == 'grid':
            show_all_in_grid(configurations)  # Will need to modify for 5 configs
        else:
            show_all_combined(configurations)
    
    else:  # sequential mode
        # Configuration 1: T-T
        print("\n1. TRUNCATION-TO-TRUNCATION (T-T)")
        print("-"*40)
        d2_tt = DeuteriumAssembly()
        d2_tt.assemble_TT(truncation_index_p=0, truncation_index_n=0)
        d2_tt.visualize(show_spheres=True, wireframe=False)
        
        # Configuration 2: T-H
        print("\n2. TRUNCATION-TO-HEXAGON (T-H)")
        print("-"*40)
        d2_th = DeuteriumAssembly()
        d2_th.assemble_TH(truncation_index=0, hexagon_index=0, 
                         is_proton_truncation=True, rotated=False)
        d2_th.visualize(show_spheres=True, wireframe=False)
        
        # Configuration 3: T-H'
        print("\n3. TRUNCATION-TO-HEXAGON ROTATED (T-H')")
        print("-"*40)
        d2_th_rot = DeuteriumAssembly()
        d2_th_rot.assemble_TH(truncation_index=0, hexagon_index=0, 
                             is_proton_truncation=True, rotated=True)
        d2_th_rot.visualize(show_spheres=True, wireframe=False)
        
        # Configuration 4: H-H
        print("\n4. HEXAGON-TO-HEXAGON ALIGNED (H-H)")
        print("-"*40)
        d2_hh = DeuteriumAssembly()
        d2_hh.assemble_HH(hex_index_p=0, hex_index_n=0, rotated=False)
        d2_hh.visualize(show_spheres=True, wireframe=False)
        
        # Configuration 5: H-H'
        print("\n5. HEXAGON-TO-HEXAGON ROTATED (H-H')")
        print("-"*40)
        d2_hh_rot = DeuteriumAssembly()
        d2_hh_rot.assemble_HH(hex_index_p=0, hex_index_n=0, rotated=True)
        d2_hh_rot.visualize(show_spheres=True, wireframe=False)
    
    print("\n" + "="*60)
    print("All 5 configurations demonstrated!")
    print("="*60)

def show_all_combined(configurations):
    """Show all configurations in a single scene with labels."""
    scene = trimesh.Scene()

    # Arrange configurations in a line with spacing
    spacing = 4.0  # Space between configurations

    for i, (name, assembly) in enumerate(configurations):
        # Create meshes
        p_mesh = assembly.proton.create_mesh(with_ports=True, with_truncation_holes=True,
                                             with_sphere=True, wireframe=False)
        n_mesh = assembly.neutron.create_mesh(with_ports=True, with_truncation_holes=True,
                                              with_sphere=True, wireframe=False)

        # Translate to position in line
        x_offset = i * spacing - (len(configurations) - 1) * spacing / 2

        # Create a transform matrix for translation
        transform = np.eye(4)
        transform[0, 3] = x_offset

        # Apply transform and colors
        p_mesh.apply_transform(transform)
        n_mesh.apply_transform(transform)

        # Set colors
        if hasattr(p_mesh, 'visual'):
            p_mesh.visual.vertex_colors = [255, 100, 100, 200]
        if hasattr(n_mesh, 'visual'):
            n_mesh.visual.vertex_colors = [100, 100, 255, 200]

        # Add to scene
        scene.add_geometry(p_mesh, node_name=f'{name}_proton')
        scene.add_geometry(n_mesh, node_name=f'{name}_neutron')

        # Add a label (as a small marker above each configuration)
        label_marker = trimesh.creation.icosphere(subdivisions=1, radius=0.1)
        label_marker.vertices += [x_offset, 0, 2]
        label_marker.visual.vertex_colors = [255, 255, 0, 255]  # Yellow markers
        scene.add_geometry(label_marker, node_name=f'{name}_label')

        print(f"  {i+1}. {name} at x={x_offset:.1f}")

    # Set camera
    bounds = scene.bounds
    extents = bounds[1] - bounds[0]
    max_extent = np.max(extents)

    scene.camera.z_far = max_extent * 10
    scene.camera.z_near = max_extent * 0.01
    scene.set_camera(angles=[np.pi/6, np.pi/4, 0], distance=max_extent*1.5)

    print("\nShowing all configurations in one view")
    print("Yellow markers indicate position of each configuration")
    print("From left to right: T-T, T-H, H-H, H-H_rotated")

    scene.show()


def show_all_in_grid(configurations):
    """Show all configurations arranged in a grid (handles 5 configs)."""
    scene = trimesh.Scene()
    
    # Arrange 5 configurations: 3 on top, 2 on bottom
    spacing = 3.5
    if len(configurations) == 5:
        positions = [
            (-spacing, spacing, 0),      # Top left
            (0, spacing, 0),              # Top center  
            (spacing, spacing, 0),        # Top right
            (-spacing/2, -spacing/2, 0),  # Bottom left
            (spacing/2, -spacing/2, 0)    # Bottom right
        ]
    else:
        # Original 2x2 for 4 configs
        positions = [
            (-spacing/2, spacing/2, 0),   # Top left
            (spacing/2, spacing/2, 0),    # Top right
            (-spacing/2, -spacing/2, 0),  # Bottom left
            (spacing/2, -spacing/2, 0)    # Bottom right
        ]
    
    for i, ((name, assembly), pos) in enumerate(zip(configurations, positions)):
        # Create meshes
        p_mesh = assembly.proton.create_mesh(with_ports=True, with_truncation_holes=True,
                                            with_sphere=True, wireframe=False)
        n_mesh = assembly.neutron.create_mesh(with_ports=True, with_truncation_holes=True,
                                            with_sphere=True, wireframe=False)
        
        # Create transform
        transform = np.eye(4)
        transform[0:3, 3] = pos
        
        # Apply transform
        p_mesh.apply_transform(transform)
        n_mesh.apply_transform(transform)
        
        # Set colors
        if hasattr(p_mesh, 'visual'):
            p_mesh.visual.vertex_colors = [255, 100, 100, 200]
        if hasattr(n_mesh, 'visual'):
            n_mesh.visual.vertex_colors = [100, 100, 255, 200]
        
        # Add to scene
        scene.add_geometry(p_mesh, node_name=f'{name}_proton')
        scene.add_geometry(n_mesh, node_name=f'{name}_neutron')
        
        print(f"  {i+1}. {name} at position {pos}")
    
    # Set camera
    bounds = scene.bounds
    extents = bounds[1] - bounds[0]
    max_extent = np.max(extents)
    
    scene.camera.z_far = max_extent * 10
    scene.camera.z_near = max_extent * 0.01
    scene.set_camera(angles=[np.pi/6, np.pi/4, 0], distance=max_extent*1.2)
    
    if len(configurations) == 5:
        print("\nShowing all 5 configurations:")
        print("Top row: T-T, T-H, T-H'")
        print("Bottom row: H-H, H-H'")
    else:
        print("\nShowing all configurations in 2x2 grid")
    
    scene.show()

if __name__ == "__main__":
    # Choose display mode:
    # 'sequential' - one at a time (close window to see next)
    # 'combined' - all in a line in one window
    # 'grid' - all in a 2x2 grid in one window

    # Show all in a grid (recommended)
    demonstrate_all_configurations(show_mode='grid')

    # Or show all in a line
    # demonstrate_all_configurations(show_mode='combined')

    # Or show one at a time
    # demonstrate_all_configurations(show_mode='sequential')

    # Or create individual configurations:
    # d2 = DeuteriumAssembly()
    # d2.assemble_HH(rotated=True)  # Example: rotated hexagon-hexagon
    # d2.visualize()
