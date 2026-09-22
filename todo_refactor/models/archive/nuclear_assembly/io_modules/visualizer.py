# nuclear_assembly/io_modules/visualizer.py - FIXED VERSION
"""
Unified visualizer for nuclear assemblies using trimesh.
Clean implementation that shows proper faces.
"""

import numpy as np
import trimesh
from typing import Dict, List, Optional, Any
from geometry.face_labeling import LabeledTetrahedron


class UnifiedVisualizer:
    """
    Single visualizer for all nuclear assemblies.
    Clean rendering of truncated tetrahedra.
    """
    
    def __init__(self):
        """Initialize visualizer."""
        self.scene = trimesh.Scene()
                
    def visualize_assembly(self, assembly: Any, show_ports: bool = True, 
                          wireframe: bool = False, port_rotation: str = 'vertices'):
        """
        Visualize any assembly type.
        
        Args:
            assembly: D2Unit, He4Ring, or generic assembly
            show_ports: Show triangular port outlines
            wireframe: Show as wireframe
            port_rotation: 'vertices' (Ï€/3) or 'edges' (0) - orientation of triangular ports
        """
        # Clear scene
        self.scene = trimesh.Scene()
        
        # Set port rotation offset
        self.port_offset = 0 if port_rotation == 'vertices' else np.pi/3
        
        # Determine assembly type and visualize
        if hasattr(assembly, 'proton') and hasattr(assembly, 'neutron'):
            # D2 unit
            self._visualize_d2(assembly, show_ports, wireframe, self.port_offset)
        elif hasattr(assembly, 'd2_1') and hasattr(assembly, 'd2_2'):
            # He4 ring
            self._visualize_he4(assembly, show_ports, wireframe, self.port_offset)
        
        # Set camera and show
        self._setup_camera()
        self.scene.show()
        
        return self.scene

    def _visualize_d2(self, d2, show_ports: bool, wireframe: bool, port_offset: float):
        """Visualize D2 unit."""
        # Add proton
        self._add_clean_tetrahedron(
            d2.proton, 
            name='proton',
            color=[255, 100, 100, 200],
            wireframe=wireframe
        )
        
        # Add neutron
        self._add_clean_tetrahedron(
            d2.neutron,
            name='neutron', 
            color=[100, 100, 255, 200],
            wireframe=wireframe
        )
        
        # Add port outlines if requested
        if show_ports and not wireframe:
            self._add_port_outlines(d2.proton, 'proton', [255, 100, 100, 200], port_offset)
            self._add_port_outlines(d2.neutron, 'neutron', [100, 100, 255, 200], port_offset)
        
        # Add bond indicator
        p_h0_center = d2.proton.get_face_center(d2.proton.get_face('H0'))
        n_h0_center = d2.neutron.get_face_center(d2.neutron.get_face('H0'))
        
        # Create bond line
        bond_line = trimesh.creation.cylinder(
            radius=0.01,
            height=np.linalg.norm(n_h0_center - p_h0_center),
            transform=trimesh.geometry.align_vectors([0, 0, 1], n_h0_center - p_h0_center)
        )
        bond_line.vertices += (p_h0_center + n_h0_center) / 2
        bond_line.visual.vertex_colors = [0, 255, 0, 255]
        self.scene.add_geometry(bond_line, node_name='bond')
        
        print(f"D2 Assembly - H-H' configuration (60Â° rotation)")
        print(f"  Port rotation offset: {port_offset:.2f} rad ({np.degrees(port_offset):.0f}Â°)")

    def _add_clean_tetrahedron(self, tet: LabeledTetrahedron, name: str, 
                               color: List[int], wireframe: bool = False):
        """
        Add a properly rendered truncated tetrahedron.
        """
        if wireframe:
            self._add_wireframe(tet, name, color)
        else:
            # Get all vertices
            vertices = tet.vertices.copy()
            faces = []
            
            # Process each hexagonal face
            hex_colors = []
            for i in range(4):
                hex_face_indices = tet.get_face(f'H{i}')
                
                # Get the vertices for this hexagon
                hex_verts = vertices[hex_face_indices]
                hex_center = np.mean(hex_verts, axis=0)
                
                # Add center vertex for fan triangulation
                center_idx = len(vertices)
                vertices = np.vstack([vertices, hex_center])
                
                # Fan triangulation from center
                for j in range(len(hex_face_indices)):
                    next_j = (j + 1) % len(hex_face_indices)
                    faces.append([center_idx, hex_face_indices[j], hex_face_indices[next_j]])
                    hex_colors.append(color)
            
            # Process each triangular face (truncations)
            tri_colors = []
            for i in range(4):
                tri_face_indices = tet.get_face(f'T{i}')
                faces.append(tri_face_indices)
                # Make triangular faces slightly darker
                darker_color = [int(c * 0.7) for c in color[:3]] + [color[3]]
                tri_colors.append(darker_color)
            
            # Create mesh
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            
            # Set face colors
            face_colors = np.array(hex_colors + tri_colors)
            mesh.visual.face_colors = face_colors
            
            # Fix normals
            mesh.fix_normals()
            
            self.scene.add_geometry(mesh, node_name=name)
    
    def _add_wireframe(self, tet: LabeledTetrahedron, name: str, color: List[int]):
        """Add clean wireframe representation."""
        edges = []
        
        # Collect unique edges from all faces
        edge_set = set()
        
        # Hexagon edges
        for i in range(4):
            hex_face = tet.get_face(f'H{i}')
            for j in range(len(hex_face)):
                v1 = hex_face[j]
                v2 = hex_face[(j + 1) % len(hex_face)]
                edge = tuple(sorted([v1, v2]))
                edge_set.add(edge)
        
        # Triangle edges
        for i in range(4):
            tri_face = tet.get_face(f'T{i}')
            for j in range(3):
                v1 = tri_face[j]
                v2 = tri_face[(j + 1) % 3]
                edge = tuple(sorted([v1, v2]))
                edge_set.add(edge)
        
        # Convert to line segments
        for v1, v2 in edge_set:
            edges.append([tet.vertices[v1], tet.vertices[v2]])
        
        # Create path
        path = trimesh.load_path(np.array(edges).reshape(-1, 2, 3))
        path.colors = np.array([color] * len(edges))
        self.scene.add_geometry(path, node_name=f'{name}_wireframe')
            
    def _add_port_outlines(self, tet: LabeledTetrahedron, name: str, color: List[int], 
                           port_rotation_offset: float = 0):
        """
        Add triangular port outlines in hexagon faces.
        
        Args:
            tet: The tetrahedron
            name: Name prefix for the geometry
            color: Color for the outline
            port_rotation_offset: Rotation offset for triangular ports (0 or Ï€/3)
                                0 = triangles point to hex vertices
                                Ï€/3 = triangles point to hex edges
        """

        port_rotation_offset -= np.pi/6 # kludge to KISS

        for i in range(4):
            hex_face = tet.get_face(f'H{i}')
            hex_center = tet.get_face_center(hex_face)
            hex_normal = tet.get_face_normal(hex_face)
            
            # Get the vertices of the hexagon to determine orientation
            hex_vertices = tet.vertices[hex_face]
            
            # Find direction from center to first vertex of hexagon
            # This gives us a consistent reference direction
            first_vertex_dir = hex_vertices[0] - hex_center
            first_vertex_dir = first_vertex_dir - np.dot(first_vertex_dir, hex_normal) * hex_normal
            first_vertex_dir = first_vertex_dir / np.linalg.norm(first_vertex_dir)
            
            # Create basis vectors in hexagon plane
            u = first_vertex_dir
            v = np.cross(hex_normal, u)
            
            # Create triangular port centered in hexagon
            port_radius = 1.0 / np.sqrt(3)
            
            # Generate triangle vertices with configurable offset
            # port_rotation_offset = 0: points align with hex vertices
            # port_rotation_offset = Ï€/3: points align with hex edges (Star of David)
            angles = np.array([
                port_rotation_offset,
                port_rotation_offset + 2*np.pi/3,
                port_rotation_offset + 4*np.pi/3
            ])
            
            port_vertices = []
            for angle in angles:
                x = port_radius * np.cos(angle)
                y = port_radius * np.sin(angle)
                vertex = hex_center + x * u + y * v
                port_vertices.append(vertex)
            
            # Close the triangle
            port_vertices.append(port_vertices[0])
            port_array = np.array(port_vertices)
            
            # Create the path
            port_path = trimesh.load_path(port_array)
            
            self.scene.add_geometry(port_path, node_name=f'{name}_port_H{i}')

    def _setup_camera(self):
        """Setup camera for optimal viewing."""
        bounds = self.scene.bounds
        if bounds is not None:
            extents = bounds[1] - bounds[0]
            max_extent = np.max(extents)
            self.scene.set_camera(
                angles=[np.pi/4, np.pi/4, 0],
                distance=max_extent * 3
            )
    
    def _visualize_he4(self, he4, show_ports: bool, wireframe: bool, port_offset: float):
        """Visualize He4 ring."""
        # For now, just visualize both D2 units
        self._visualize_d2(he4.d2_1, show_ports, wireframe)
        self._visualize_d2(he4.d2_2, show_ports, wireframe)
        print(f"He4 Assembly - Chirality: {he4.chirality}")
    
    def export(self, filename: str):
        """Export scene to file."""
        self.scene.export(filename)
        print(f"Exported to {filename}")
