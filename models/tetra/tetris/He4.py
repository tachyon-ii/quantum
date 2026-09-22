"""
He4 Viewer from H-H' Units
===========================
Shows He4 formed from two H-H' deuterium units.
Only P-N connections allowed (no P-P or N-N).
"""

import numpy as np
import trimesh
from tetra_model import TruncatedTetrahedron
from deuterium_assemblies import DeuteriumAssembly


class He4FromHHPrime:
    """
    Creates He4 from two H-H' deuterium units.
    Each H-H' unit has a P end and an N end.
    Only P-N connections are allowed.
    """
    
    def __init__(self, edge_length=1.0):
        self.edge_length = edge_length
        self.unit1 = None  # First H-H' unit (P1-N1)
        self.unit2 = None  # Second H-H' unit (P2-N2)
        self.configuration_name = None
        
    def create_units(self):
        """Create two H-H' deuterium units."""
        # First H-H' unit
        self.unit1 = DeuteriumAssembly(self.edge_length)
        self.unit1.assemble_HH(hex_index_p=0, hex_index_n=0, rotated=True)
        
        # Second H-H' unit
        self.unit2 = DeuteriumAssembly(self.edge_length)
        self.unit2.assemble_HH(hex_index_p=0, hex_index_n=0, rotated=True)
    
    def assemble_P1_to_N2(self, p1_face=1, n2_face=1):
        """
        Connect P1 end of unit1 to N2 end of unit2.
        This creates: N1-P1 :: N2-P2 connection.
        
        Args:
            p1_face: Which free face of P1 to use (1, 2, or 3)
            n2_face: Which free face of N2 to use (1, 2, or 3)
        """
        self.create_units()
        self.configuration_name = "P1-N2 Connection"
        
        # Get the face data
        p1_data = self.unit1.proton.get_bonding_geometry()
        n2_data = self.unit2.neutron.get_bonding_geometry()
        
        # Get the specific faces to connect
        p1_hex = p1_data['hexagon_faces'][p1_face]
        n2_hex = n2_data['hexagon_faces'][n2_face]
        
        # Align N2 face to P1 face
        target_normal = -p1_hex['normal']
        current_normal = n2_hex['normal']
        
        # Calculate rotation
        rotation = self._rotation_matrix_between_vectors(current_normal, target_normal)
        
        # Apply rotation to entire unit2
        self.unit2.proton.vertices = (rotation @ self.unit2.proton.vertices.T).T
        self.unit2.neutron.vertices = (rotation @ self.unit2.neutron.vertices.T).T

        # Rotate by +2π/3 around the bond axis
        bond_rotation = self._rotation_matrix_around_axis(target_normal, 2*np.pi/3)
        self.unit2.proton.vertices = (bond_rotation @ self.unit2.proton.vertices.T).T
        self.unit2.neutron.vertices = (bond_rotation @ self.unit2.neutron.vertices.T).T

        # Recalculate after rotation
        n2_data = self.unit2.neutron.get_bonding_geometry()
        n2_hex = n2_data['hexagon_faces'][n2_face]
        
        # Translate unit2 to align faces
        separation = 0.02  # Small gap to see structure
        translation = p1_hex['center'] + p1_hex['normal'] * separation - n2_hex['center']
        
        self.unit2.proton.vertices += translation
        self.unit2.neutron.vertices += translation
        
        print(f"Assembled {self.configuration_name}:")
        print(f"  Unit1: N1-P1 (P1 face {p1_face} connects)")
        print(f"  Unit2: N2-P2 (N2 face {n2_face} connects)")
        print(f"  Bond: P1-N2")
    
    def assemble_N1_to_P2(self, n1_face=1, p2_face=1):
        """
        Connect N1 end of unit1 to P2 end of unit2.
        This creates: P1-N1 :: P2-N2 connection.
        
        Args:
            n1_face: Which free face of N1 to use (1, 2, or 3)
            p2_face: Which free face of P2 to use (1, 2, or 3)
        """
        self.create_units()
        self.configuration_name = "N1-P2 Connection"
        
        # Get the face data
        n1_data = self.unit1.neutron.get_bonding_geometry()
        p2_data = self.unit2.proton.get_bonding_geometry()
        
        # Get the specific faces to connect
        n1_hex = n1_data['hexagon_faces'][n1_face]
        p2_hex = p2_data['hexagon_faces'][p2_face]
        
        # Align P2 face to N1 face
        target_normal = -n1_hex['normal']
        current_normal = p2_hex['normal']
        
        # Calculate rotation
        rotation = self._rotation_matrix_between_vectors(current_normal, target_normal)
        
        # Apply rotation to entire unit2
        self.unit2.proton.vertices = (rotation @ self.unit2.proton.vertices.T).T
        self.unit2.neutron.vertices = (rotation @ self.unit2.neutron.vertices.T).T

        # Rotate by +2π/3 around the bond axis
        bond_rotation = self._rotation_matrix_around_axis(target_normal, 2*np.pi/3)
        self.unit2.proton.vertices = (bond_rotation @ self.unit2.proton.vertices.T).T
        self.unit2.neutron.vertices = (bond_rotation @ self.unit2.neutron.vertices.T).T
        
        # Recalculate after rotation
        p2_data = self.unit2.proton.get_bonding_geometry()
        p2_hex = p2_data['hexagon_faces'][p2_face]
        
        # Translate unit2 to align faces
        separation = 0.02  # Small gap to see structure
        translation = n1_hex['center'] + n1_hex['normal'] * separation - p2_hex['center']
        
        self.unit2.proton.vertices += translation
        self.unit2.neutron.vertices += translation
        
        print(f"Assembled {self.configuration_name}:")
        print(f"  Unit1: P1-N1 (N1 face {n1_face} connects)")
        print(f"  Unit2: P2-N2 (P2 face {p2_face} connects)")
        print(f"  Bond: N1-P2")
    
    def _rotation_matrix_between_vectors(self, v1, v2):
        """Calculate rotation matrix to rotate v1 to v2."""
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        
        if np.allclose(v1, v2):
            return np.eye(3)
        
        if np.allclose(v1, -v2):
            orthogonal = np.array([1, 0, 0]) if abs(v1[0]) < 0.9 else np.array([0, 1, 0])
            orthogonal = orthogonal - np.dot(orthogonal, v1) * v1
            orthogonal = orthogonal / np.linalg.norm(orthogonal)
            return 2 * np.outer(orthogonal, orthogonal) - np.eye(3)
        
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
    
    def visualize(self, show_spheres=False, wireframe=False):
        """Visualize the He4 assembly."""
        if self.unit1 is None or self.unit2 is None:
            print("No assembly created yet!")
            return
        
        scene = trimesh.Scene()
        
        # Colors for the 4 nucleons
        colors = {
            'P1': [255, 100, 100, 200],  # Light red
            'N1': [100, 100, 255, 200],  # Light blue
            'P2': [200, 50, 50, 200],    # Dark red
            'N2': [50, 50, 200, 200]     # Dark blue
        }
        
        # Add unit1 nucleons
        for name, nucleon, color in [
            ('P1', self.unit1.proton, colors['P1']),
            ('N1', self.unit1.neutron, colors['N1'])
        ]:
            mesh = nucleon.create_mesh(with_ports=True, with_truncation_holes=True,
                                      with_sphere=show_spheres, wireframe=wireframe)
            if not wireframe and hasattr(mesh, 'visual'):
                mesh.visual.vertex_colors = color
            
            if isinstance(mesh, trimesh.Scene):
                for geom_name, geom in mesh.geometry.items():
                    scene.add_geometry(geom, node_name=f'{name}_{geom_name}')
            else:
                scene.add_geometry(mesh, node_name=name)
        
        # Add unit2 nucleons
        for name, nucleon, color in [
            ('P2', self.unit2.proton, colors['P2']),
            ('N2', self.unit2.neutron, colors['N2'])
        ]:
            mesh = nucleon.create_mesh(with_ports=True, with_truncation_holes=True,
                                      with_sphere=show_spheres, wireframe=wireframe)
            if not wireframe and hasattr(mesh, 'visual'):
                mesh.visual.vertex_colors = color
            
            if isinstance(mesh, trimesh.Scene):
                for geom_name, geom in mesh.geometry.items():
                    scene.add_geometry(geom, node_name=f'{name}_{geom_name}')
            else:
                scene.add_geometry(mesh, node_name=name)
        
        # Set camera
        bounds = scene.bounds
        extents = bounds[1] - bounds[0]
        max_extent = np.max(extents)
        
        scene.camera.z_far = max_extent * 10
        scene.camera.z_near = max_extent * 0.01
        scene.set_camera(angles=[np.pi/4, np.pi/4, 0], distance=max_extent*2)
        
        print(f"\nShowing {self.configuration_name}")
        print("  P1: Light red, N1: Light blue (Unit 1)")
        print("  P2: Dark red, N2: Dark blue (Unit 2)")
        
        scene.show()


def show_both_he4_configurations():
    """Show both valid He4 configurations from H-H' units."""
    
    print("="*70)
    print("He4 FROM TWO H-H' UNITS")
    print("="*70)
    print("\nEach H-H' unit has:")
    print("  - P end (proton, red)")
    print("  - N end (neutron, blue)")
    print("\nValid connections (P-N only):")
    print("  1. P1-N2: Connect P end of unit1 to N end of unit2")
    print("  2. N1-P2: Connect N end of unit1 to P end of unit2")
    print("\n" + "="*70)
    
    # Configuration 1: P1-N2
    print("\n1. P1-N2 CONFIGURATION")
    print("-"*40)
    he4_p1n2 = He4FromHHPrime()
    he4_p1n2.assemble_P1_to_N2(p1_face=1, n2_face=1)
    he4_p1n2.visualize(show_spheres=False, wireframe=False)
    
    # Configuration 2: N1-P2
    print("\n2. N1-P2 CONFIGURATION")
    print("-"*40)
    he4_n1p2 = He4FromHHPrime()
    he4_n1p2.assemble_N1_to_P2(n1_face=1, p2_face=1)
    he4_n1p2.visualize(show_spheres=False, wireframe=False)
    
    print("\n" + "="*70)
    print("Both valid He4 configurations shown!")
    print("="*70)


def show_both_in_grid():
    """Show both configurations side by side."""
    scene = trimesh.Scene()
    
    # Create both configurations
    configs = []
    
    # P1-N2 configuration
    he4_p1n2 = He4FromHHPrime()
    he4_p1n2.assemble_P1_to_N2(p1_face=1, n2_face=1)
    configs.append(('P1-N2', he4_p1n2))
    
    # N1-P2 configuration  
    he4_n1p2 = He4FromHHPrime()
    he4_n1p2.assemble_N1_to_P2(n1_face=1, p2_face=1)
    configs.append(('N1-P2', he4_n1p2))
    
    # Position them side by side
    positions = [(-3, 0, 0), (3, 0, 0)]
    
    colors = {
        'P1': [255, 100, 100, 200],
        'N1': [100, 100, 255, 200],
        'P2': [200, 50, 50, 200],
        'N2': [50, 50, 200, 200]
    }
    
    for (name, he4), pos in zip(configs, positions):
        # Transform for this position
        transform = np.eye(4)
        transform[0:3, 3] = pos
        
        # Add all four nucleons
        for nuc_name, nucleon, color in [
            ('P1', he4.unit1.proton, colors['P1']),
            ('N1', he4.unit1.neutron, colors['N1']),
            ('P2', he4.unit2.proton, colors['P2']),
            ('N2', he4.unit2.neutron, colors['N2'])
        ]:
            mesh = nucleon.create_mesh(with_ports=True, with_truncation_holes=True,
                                      with_sphere=False, wireframe=False)
            mesh.apply_transform(transform)
            
            if hasattr(mesh, 'visual'):
                mesh.visual.vertex_colors = color
            
            scene.add_geometry(mesh, node_name=f'{name}_{nuc_name}')
        
        print(f"  {name} at position {pos}")
    
    # Set view
    bounds = scene.bounds
    extents = bounds[1] - bounds[0]
    max_extent = np.max(extents)
    
    scene.camera.z_far = max_extent * 10
    scene.camera.z_near = max_extent * 0.01
    scene.set_camera(angles=[np.pi/6, np.pi/4, 0], distance=max_extent*1.5)
    
    print("\nShowing both He4 configurations side by side")
    print("Left: P1-N2 connection")
    print("Right: N1-P2 connection")
    
    scene.show()


if __name__ == "__main__":
    # Show both configurations sequentially
    # show_both_he4_configurations()
    
    # Or show both side by side
    print("Showing both He4 configurations from H-H' units...\n")
    show_both_in_grid()
