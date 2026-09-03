"""
Truncated Tetrahedron Generator and Renderer
=============================================
A simple, focused module that correctly generates and renders 
truncated tetrahedrons with triangular ports in the hexagonal faces.
"""

import numpy as np
import trimesh
from shapely.geometry import Polygon


class TruncatedTetrahedron:
    """
    Generates a proper truncated tetrahedron with:
    - 4 hexagonal faces
    - 4 triangular faces  
    - Triangular ports (holes) in the center of hexagonal faces
    """
    
    def __init__(self, edge_length=1.0, port_rotation=0):
        """
        Args:
            edge_length: Length of all edges (default 1.0)
            port_rotation: Rotation of triangular ports in radians (0 or π/3)
        """
        self.edge_length = edge_length
        self.port_rotation = port_rotation
        
        # Generate the shape
        self.vertices = self._generate_vertices()
        self.hexagon_faces = self._get_hexagon_faces()
        self.triangle_faces = self._get_triangle_faces()
        
    def _generate_vertices(self):
        """
        Generate the 12 vertices of a truncated tetrahedron.
        
        A truncated tetrahedron is created by cutting off the corners
        of a regular tetrahedron at 1/3 of each edge length.
        """
        # Start with vertices of a regular tetrahedron
        # Using standard coordinates
        tet_vertices = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1]
        ])
        
        # Normalize to desired edge length
        # For a regular tetrahedron with edge length a, vertices are at distance a/sqrt(8)
        scale = self.edge_length / np.sqrt(8)
        tet_vertices = tet_vertices * scale * 3  # Scale up by 3 before truncation
        
        # Now truncate: each vertex becomes 3 vertices
        # We cut at 1/3 of the edge length from each vertex
        truncated_vertices = []
        
        # Keep track of which vertices come from which original vertex
        self.vertex_origins = []
        
        for i, vertex in enumerate(tet_vertices):
            # For each vertex, find the three edges connected to it
            # and place new vertices at 2/3 along each edge (1/3 from the vertex)
            for j, other_vertex in enumerate(tet_vertices):
                if i != j:
                    # Create a vertex 1/3 of the way from vertex to other_vertex
                    new_vertex = vertex + (other_vertex - vertex) * (1/3)
                    truncated_vertices.append(new_vertex)
                    self.vertex_origins.append((i, j))  # Track origin for face construction
        
        return np.array(truncated_vertices)
    
    def _get_hexagon_faces(self):
        """
        Define the 4 hexagonal faces by vertex indices.
        Each hexagon is formed where an original tetrahedron face was.
        """
        # Based on debugging with colored vertices, these are the correct orderings
        # that form proper hexagons without crossing truncation boundaries
        
        # Face (0,1,2) - excludes vertex 3
        face_012 = [0, 3, 4, 7, 6, 1]   # red yellow magenta purple orange green
        
        # Face (0,1,3) - excludes vertex 2  
        face_013 = [0, 2, 9, 10, 5, 3]  # red blue sky lime cyan yellow
        
        # Face (0,2,3) - excludes vertex 1
        face_023 = [1, 6, 8, 11, 9, 2]  # green orange pink gray sky blue
        
        # Face (1,2,3) - excludes vertex 0
        face_123 = [11, 8, 7, 4, 5, 10] # gray pink purple magenta cyan lime
        
        hexagon_faces = [face_012, face_013, face_023, face_123]
        
        return hexagon_faces
    
    def _get_triangle_faces(self):
        """
        Define the 4 triangular faces by vertex indices.
        Each triangle is where an original vertex was truncated.
        """
        triangle_faces = [
            [0, 1, 2],     # Triangle from truncation of vertex 0
            [3, 4, 5],     # Triangle from truncation of vertex 1
            [6, 7, 8],     # Triangle from truncation of vertex 2
            [9, 10, 11]    # Triangle from truncation of vertex 3
        ]
        
        return triangle_faces
    
    def create_mesh(self, with_ports=True, with_truncation_holes=True, 
                     with_sphere=True, wireframe=False,
                     inside_color=[100, 100, 100, 255], 
                     outside_color=[200, 50, 50, 255]):
        """
        Create a trimesh object of the truncated tetrahedron.
        
        Args:
            with_ports: If True, add triangular holes to hexagonal faces
            with_truncation_holes: If True, leave truncation triangles as holes
            with_sphere: If True, add internal sphere
            wireframe: If True, create wireframe instead of solid faces
            inside_color: RGBA color for inside faces (darker)
            outside_color: RGBA color for outside faces
            
        Returns:
            trimesh.Trimesh object or Scene for wireframe
        """
        if wireframe:
            return self._create_wireframe(with_ports=with_ports, 
                                         with_sphere=with_sphere)
        
        meshes = []
        
        # Create hexagonal faces (with or without ports)
        for i, hex_indices in enumerate(self.hexagon_faces):
            hex_vertices = self.vertices[hex_indices]
            
            if with_ports:
                # Create hexagon with triangular hole
                mesh = self._create_hexagon_with_port(hex_vertices)
                # Color the hexagon based on normal direction
                mesh.visual.vertex_colors = outside_color
            else:
                # Create solid hexagon
                mesh = self._create_solid_hexagon(hex_vertices)
                mesh.visual.vertex_colors = outside_color
            
            meshes.append(mesh)
        
        # Create triangular faces only if we don't want truncation holes
        if not with_truncation_holes:
            for tri_indices in self.triangle_faces:
                tri_vertices = self.vertices[tri_indices]
                mesh = self._create_triangle(tri_vertices)
                # Triangular faces get the inside color (they face inward)
                mesh.visual.vertex_colors = inside_color
                meshes.append(mesh)
        
        # Add internal sphere if requested
        if with_sphere:
            sphere = self._create_internal_sphere()
            meshes.append(sphere)
        
        # Combine all meshes
        combined = trimesh.util.concatenate(meshes)
        return combined
    
    def _create_wireframe(self, with_ports=True, with_sphere=True):
        """
        Create a wireframe representation using line segments.
        """
        segments = []
        
        # Add edges for each hexagonal face - using actual vertex positions
        for hex_indices in self.hexagon_faces:
            # Get the actual vertices for this hexagon
            hex_vertices = self.vertices[hex_indices]
            
            # Create edges for hexagon perimeter using actual vertices
            for i in range(len(hex_indices)):
                v1 = self.vertices[hex_indices[i]]
                v2 = self.vertices[hex_indices[(i + 1) % len(hex_indices)]]
                segments.append([v1, v2])
            
            # If with ports, add triangular port edges
            if with_ports:
                # Calculate port center and vertices
                center = np.mean(hex_vertices, axis=0)
                
                # Calculate normal for proper orientation
                v1 = hex_vertices[1] - hex_vertices[0]
                v2 = hex_vertices[2] - hex_vertices[0]
                normal = np.cross(v1, v2)
                normal = normal / np.linalg.norm(normal)
                
                # Create port triangle vertices
                port_radius = self.edge_length / np.sqrt(3)
                angles = np.array([0, 2*np.pi/3, 4*np.pi/3]) + self.port_rotation + np.pi/2
                
                # Create local coordinate system
                x_axis = (hex_vertices[0] - center)
                x_axis = x_axis / np.linalg.norm(x_axis)
                y_axis = np.cross(normal, x_axis)
                y_axis = y_axis / np.linalg.norm(y_axis)
                
                # Calculate port vertices in 3D
                port_verts = []
                for angle in angles:
                    local_x = port_radius * np.cos(angle)
                    local_y = port_radius * np.sin(angle)
                    vertex = center + local_x * x_axis + local_y * y_axis
                    port_verts.append(vertex)
                
                # Add port triangle edges
                for i in range(3):
                    v1 = port_verts[i]
                    v2 = port_verts[(i + 1) % 3]
                    segments.append([v1, v2])
        
        # Add edges for triangular truncation holes
        for tri_indices in self.triangle_faces:
            # Create edges using actual vertex positions
            for i in range(3):
                v1 = self.vertices[tri_indices[i]]
                v2 = self.vertices[tri_indices[(i + 1) % 3]]
                segments.append([v1, v2])
        
        # Create path from segments
        path = trimesh.load_path(np.array(segments))
        
        # If sphere requested, add it as a separate mesh
        if with_sphere:
            sphere = self._create_internal_sphere()
            # Return both in a scene
            scene = trimesh.Scene()
            scene.add_geometry(path)
            scene.add_geometry(sphere)
            return scene
        
        return path
    
    def _create_internal_sphere(self):
        """
        Create a gray sphere inside the truncated tetrahedron.
        Radius is from centroid to the center of a triangular port in a hexagon face.
        """
        # Calculate centroid of the truncated tetrahedron
        centroid = np.mean(self.vertices, axis=0)
        
        # Get the center of the first triangular port (in a hexagon face)
        # We need to find the center of one of the hexagonal faces
        hex_vertices = self.vertices[self.hexagon_faces[0]]
        hex_center = np.mean(hex_vertices, axis=0)
        
        # The radius is the distance from centroid to hex face center
        radius = np.linalg.norm(hex_center - centroid)
        
        # Create sphere with more subdivisions for smoother appearance
        sphere = trimesh.creation.icosphere(subdivisions=4, radius=radius)
        
        # Position sphere at centroid
        sphere.vertices += centroid
        
        # Set color to gray with full opacity
        sphere.visual.vertex_colors = [128, 128, 128, 255]  # Gray with full opacity
        
        # The viewer should handle shading to make it look 3D
        # Ensure face normals are correct for proper lighting
        sphere.fix_normals()
        
        return sphere
    
    def _create_hexagon_with_port(self, hex_vertices):
        """
        Create a hexagonal face with a triangular port (hole) in the center.
        """
        # Get the center and normal of the hexagon
        center = np.mean(hex_vertices, axis=0)
        
        # Calculate normal vector
        v1 = hex_vertices[1] - hex_vertices[0]
        v2 = hex_vertices[2] - hex_vertices[0]
        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)
        
        # Project hexagon to 2D for easier manipulation
        # Create a local 2D coordinate system
        x_axis = (hex_vertices[0] - center)
        x_axis = x_axis / np.linalg.norm(x_axis)
        y_axis = np.cross(normal, x_axis)
        y_axis = y_axis / np.linalg.norm(y_axis)
        
        # Convert to 2D coordinates
        hex_2d = []
        for v in hex_vertices:
            local = v - center
            x = np.dot(local, x_axis)
            y = np.dot(local, y_axis)
            hex_2d.append([x, y])
        hex_2d = np.array(hex_2d)
        
        # Ensure the hexagon vertices form a valid polygon (proper ordering)
        # Calculate angles from center to sort vertices
        angles = np.arctan2(hex_2d[:, 1], hex_2d[:, 0])
        sorted_indices = np.argsort(angles)
        hex_2d = hex_2d[sorted_indices]
        
        # Create triangular port in center with same edge length as hexagon
        # For an equilateral triangle with edge length = self.edge_length,
        # the circumradius (distance from center to vertex) is edge_length / sqrt(3)
        port_radius = self.edge_length / np.sqrt(3)
        angles = np.array([0, 2*np.pi/3, 4*np.pi/3]) + self.port_rotation + np.pi/2
        port_2d = port_radius * np.column_stack([np.cos(angles), np.sin(angles)])
        
        try:
            # Create polygon with hole using shapely
            polygon = Polygon(hex_2d, holes=[port_2d])
            
            # Check if polygon is valid
            if not polygon.is_valid:
                # If invalid, try to fix it
                polygon = polygon.buffer(0)
            
            # Extrude to 3D with minimal thickness
            mesh_2d = trimesh.creation.extrude_polygon(polygon, height=0.001)
            
            # Transform back to 3D position
            # Create transformation matrix
            transform = np.eye(4)
            transform[:3, 0] = x_axis
            transform[:3, 1] = y_axis
            transform[:3, 2] = normal
            transform[:3, 3] = center
            
            mesh_2d.apply_transform(transform)
            
            return mesh_2d
            
        except Exception as e:
            print(f"Warning: Could not create hexagon with port: {e}")
            print("Creating solid hexagon instead")
            return self._create_solid_hexagon(hex_vertices)
    
    def _create_solid_hexagon(self, hex_vertices):
        """Create a solid hexagonal face."""
        # Simple triangulation of hexagon
        faces = []
        for i in range(1, 5):
            faces.append([0, i, i+1])
        
        mesh = trimesh.Trimesh(vertices=hex_vertices, faces=faces)
        return mesh
    
    def _create_triangle(self, tri_vertices):
        """Create a triangular face."""
        mesh = trimesh.Trimesh(
            vertices=tri_vertices,
            faces=[[0, 1, 2]]
        )
        return mesh
    
    def get_bonding_geometry(self):
        """
        Extract precise geometric information for bonding calculations.
        Returns centers, normals, and vertices for all bonding surfaces.
        """
        bonding_data = {
            'hexagon_faces': [],
            'triangular_ports': [],
            'truncation_triangles': []
        }
        
        # Process each hexagonal face
        for i, hex_indices in enumerate(self.hexagon_faces):
            hex_vertices = self.vertices[hex_indices]
            
            # Calculate center and normal for hexagon
            hex_center = np.mean(hex_vertices, axis=0)
            
            # Calculate normal (using first three vertices)
            v1 = hex_vertices[1] - hex_vertices[0]
            v2 = hex_vertices[2] - hex_vertices[0]
            hex_normal = np.cross(v1, v2)
            hex_normal = hex_normal / np.linalg.norm(hex_normal)
            
            # Calculate triangular port geometry for this hexagon
            port_radius = self.edge_length / np.sqrt(3)
            angles = np.array([0, 2*np.pi/3, 4*np.pi/3]) + self.port_rotation + np.pi/2
            
            # Create local coordinate system
            x_axis = (hex_vertices[0] - hex_center)
            x_axis = x_axis / np.linalg.norm(x_axis)
            y_axis = np.cross(hex_normal, x_axis)
            y_axis = y_axis / np.linalg.norm(y_axis)
            
            # Calculate port vertices
            port_vertices = []
            for angle in angles:
                local_x = port_radius * np.cos(angle)
                local_y = port_radius * np.sin(angle)
                vertex = hex_center + local_x * x_axis + local_y * y_axis
                port_vertices.append(vertex)
            
            bonding_data['hexagon_faces'].append({
                'index': i,
                'center': hex_center,
                'normal': hex_normal,
                'vertices': hex_vertices,
                'edge_length': np.linalg.norm(hex_vertices[1] - hex_vertices[0])
            })
            
            bonding_data['triangular_ports'].append({
                'index': i,
                'parent_hexagon': i,
                'center': hex_center,  # Port is centered on hexagon
                'normal': hex_normal,   # Same normal as parent hexagon
                'vertices': np.array(port_vertices),
                'edge_length': self.edge_length
            })
        
        # Process truncation triangles
        for i, tri_indices in enumerate(self.triangle_faces):
            tri_vertices = self.vertices[tri_indices]
            
            # Calculate center and normal
            tri_center = np.mean(tri_vertices, axis=0)
            
            # Calculate normal
            v1 = tri_vertices[1] - tri_vertices[0]
            v2 = tri_vertices[2] - tri_vertices[0]
            tri_normal = np.cross(v1, v2)
            tri_normal = tri_normal / np.linalg.norm(tri_normal)
            
            # Ensure normal points outward from tetrahedron center
            tet_center = np.mean(self.vertices, axis=0)
            if np.dot(tri_normal, tri_center - tet_center) < 0:
                tri_normal = -tri_normal
            
            bonding_data['truncation_triangles'].append({
                'index': i,
                'center': tri_center,
                'normal': tri_normal,
                'vertices': tri_vertices,
                'edge_length': np.linalg.norm(tri_vertices[1] - tri_vertices[0])
            })
        
        return bonding_data
    
    def print_bonding_geometry(self):
        """Print detailed bonding geometry information."""
        data = self.get_bonding_geometry()
        
        print("\n" + "="*60)
        print("BONDING GEOMETRY ANALYSIS")
        print("="*60)
        
        print("\nHEXAGON FACES (4 total):")
        print("-"*40)
        for hex_data in data['hexagon_faces']:
            i = hex_data['index']
            print(f"\nHexagon {i}:")
            print(f"  Center: [{hex_data['center'][0]:7.4f}, {hex_data['center'][1]:7.4f}, {hex_data['center'][2]:7.4f}]")
            print(f"  Normal: [{hex_data['normal'][0]:7.4f}, {hex_data['normal'][1]:7.4f}, {hex_data['normal'][2]:7.4f}]")
            print(f"  Edge length: {hex_data['edge_length']:.4f}")
        
        print("\nTRIANGULAR PORTS IN HEXAGONS (4 total):")
        print("-"*40)
        for port_data in data['triangular_ports']:
            i = port_data['index']
            print(f"\nPort {i} (in Hexagon {port_data['parent_hexagon']}):")
            print(f"  Center: [{port_data['center'][0]:7.4f}, {port_data['center'][1]:7.4f}, {port_data['center'][2]:7.4f}]")
            print(f"  Normal: [{port_data['normal'][0]:7.4f}, {port_data['normal'][1]:7.4f}, {port_data['normal'][2]:7.4f}]")
            print(f"  Edge length: {port_data['edge_length']:.4f}")
        
        print("\nTRUNCATION TRIANGLES (4 total):")
        print("-"*40)
        for tri_data in data['truncation_triangles']:
            i = tri_data['index']
            print(f"\nTruncation {i}:")
            print(f"  Center: [{tri_data['center'][0]:7.4f}, {tri_data['center'][1]:7.4f}, {tri_data['center'][2]:7.4f}]")
            print(f"  Normal: [{tri_data['normal'][0]:7.4f}, {tri_data['normal'][1]:7.4f}, {tri_data['normal'][2]:7.4f}]")
            print(f"  Edge length: {tri_data['edge_length']:.4f}")
        
        # Calculate distances between centers
        print("\n" + "="*60)
        print("GEOMETRIC RELATIONSHIPS")
        print("="*60)
        
        # Distance from tetrahedron center to faces
        tet_center = np.mean(self.vertices, axis=0)
        print(f"\nTetrahedron center: [{tet_center[0]:7.4f}, {tet_center[1]:7.4f}, {tet_center[2]:7.4f}]")
        
        print("\nDistances from center:")
        hex_dist = np.linalg.norm(data['hexagon_faces'][0]['center'] - tet_center)
        tri_dist = np.linalg.norm(data['truncation_triangles'][0]['center'] - tet_center)
        print(f"  To hexagon faces: {hex_dist:.4f}")
        print(f"  To truncation triangles: {tri_dist:.4f}")
        
        # Angles between normals
        print("\nAngles between face normals:")
        for i in range(len(data['hexagon_faces'])):
            for j in range(i+1, len(data['hexagon_faces'])):
                dot = np.dot(data['hexagon_faces'][i]['normal'], 
                           data['hexagon_faces'][j]['normal'])
                angle = np.arccos(np.clip(dot, -1, 1)) * 180 / np.pi
                print(f"  Hexagon {i} to Hexagon {j}: {angle:.2f}°")
    
    def show(self, initial_zoom=0.5, wireframe=False, show_vertex_labels=False):
        """
        Display the truncated tetrahedron.
        
        Args:
            initial_zoom: Zoom factor for initial view (0.5 = 50% zoom out)
            wireframe: If True, display as wireframe
            show_vertex_labels: If True, display vertex numbers with color coding
        """
        mesh = self.create_mesh(with_ports=True, with_truncation_holes=True, 
                               with_sphere=True, wireframe=wireframe)
        
        # Create or use scene
        if isinstance(mesh, trimesh.Scene):
            scene = mesh
        else:
            scene = trimesh.Scene(mesh)
        
        # Add vertex labels if requested
        if show_vertex_labels:
            # Color palette for vertices (12 distinct colors)
            colors = [
                [255, 0, 0, 255],      # 0: Red
                [0, 255, 0, 255],      # 1: Green
                [0, 0, 255, 255],      # 2: Blue
                [255, 255, 0, 255],    # 3: Yellow
                [255, 0, 255, 255],    # 4: Magenta
                [0, 255, 255, 255],    # 5: Cyan
                [255, 128, 0, 255],    # 6: Orange
                [128, 0, 255, 255],    # 7: Purple
                [255, 0, 128, 255],    # 8: Pink
                [0, 128, 255, 255],    # 9: Sky blue
                [128, 255, 0, 255],    # 10: Lime
                [128, 128, 128, 255],  # 11: Gray
            ]
            
            # Create spheres at each vertex with unique colors
            for i, vertex in enumerate(self.vertices):
                # Create a small sphere at the vertex
                marker = trimesh.creation.icosphere(subdivisions=2, radius=0.05)
                marker.vertices += vertex
                marker.visual.vertex_colors = colors[i % len(colors)]
                scene.add_geometry(marker, node_name=f'vertex_{i}')
            
            # Print color-coded vertex info
            print("\nVertex colors and positions:")
            color_names = ['Red', 'Green', 'Blue', 'Yellow', 'Magenta', 'Cyan', 
                          'Orange', 'Purple', 'Pink', 'Sky blue', 'Lime', 'Gray']
            for i, vertex in enumerate(self.vertices):
                print(f"Vertex {i:2d} ({color_names[i]}): [{vertex[0]:6.3f}, {vertex[1]:6.3f}, {vertex[2]:6.3f}]")
            
            print("\nHexagon faces (by color):")
            for i, face in enumerate(self.hexagon_faces):
                face_colors = [color_names[v] for v in face]
                print(f"Hexagon {i}: {face} = {face_colors}")
            
            print("\nTriangle faces (by color):")
            for i, face in enumerate(self.triangle_faces):
                face_colors = [color_names[v] for v in face]
                print(f"Triangle {i}: {face} = {face_colors}")
        
        # Set camera to show the whole object at a reasonable distance
        try:
            bounds = scene.bounds
        except:
            bounds = mesh.bounds if hasattr(mesh, 'bounds') else np.array([[-1,-1,-1],[1,1,1]])
            
        extents = bounds[1] - bounds[0]
        max_extent = np.max(extents)
        
        # Set camera distance based on object size
        camera_distance = max_extent / initial_zoom
        scene.camera.z_far = camera_distance * 10
        scene.camera.z_near = camera_distance * 0.01
        
        # Position camera
        scene.set_camera(angles=[np.pi/6, np.pi/6, 0], distance=camera_distance)
        
        scene.show()
        """
        Display the truncated tetrahedron.
        
        Args:
            initial_zoom: Zoom factor for initial view (0.5 = 50% zoom out)
            wireframe: If True, display as wireframe
            show_vertex_labels: If True, display vertex numbers with color coding
        """
        mesh = self.create_mesh(with_ports=True, with_truncation_holes=True, 
                               with_sphere=True, wireframe=wireframe)
        
        # Create or use scene
        if isinstance(mesh, trimesh.Scene):
            scene = mesh
        else:
            scene = trimesh.Scene(mesh)
        
        # Add vertex labels if requested
        if show_vertex_labels:
            # Color palette for vertices (12 distinct colors)
            colors = [
                [255, 0, 0, 255],      # 0: Red
                [0, 255, 0, 255],      # 1: Green
                [0, 0, 255, 255],      # 2: Blue
                [255, 255, 0, 255],    # 3: Yellow
                [255, 0, 255, 255],    # 4: Magenta
                [0, 255, 255, 255],    # 5: Cyan
                [255, 128, 0, 255],    # 6: Orange
                [128, 0, 255, 255],    # 7: Purple
                [255, 0, 128, 255],    # 8: Pink
                [0, 128, 255, 255],    # 9: Sky blue
                [128, 255, 0, 255],    # 10: Lime
                [128, 128, 128, 255],  # 11: Gray
            ]
            
            # Create spheres at each vertex with unique colors
            for i, vertex in enumerate(self.vertices):
                # Create a small sphere at the vertex
                marker = trimesh.creation.icosphere(subdivisions=2, radius=0.05)
                marker.vertices += vertex
                marker.visual.vertex_colors = colors[i % len(colors)]
                scene.add_geometry(marker, node_name=f'vertex_{i}')
            
            # Print color-coded vertex info
            print("\nVertex colors and positions:")
            color_names = ['Red', 'Green', 'Blue', 'Yellow', 'Magenta', 'Cyan', 
                          'Orange', 'Purple', 'Pink', 'Sky blue', 'Lime', 'Gray']
            for i, vertex in enumerate(self.vertices):
                print(f"Vertex {i:2d} ({color_names[i]}): [{vertex[0]:6.3f}, {vertex[1]:6.3f}, {vertex[2]:6.3f}]")
            
            print("\nHexagon faces (by color):")
            for i, face in enumerate(self.hexagon_faces):
                face_colors = [color_names[v] for v in face]
                print(f"Hexagon {i}: {face} = {face_colors}")
            
            print("\nTriangle faces (by color):")
            for i, face in enumerate(self.triangle_faces):
                face_colors = [color_names[v] for v in face]
                print(f"Triangle {i}: {face} = {face_colors}")
        
        # Set camera to show the whole object at a reasonable distance
        try:
            bounds = scene.bounds
        except:
            bounds = mesh.bounds if hasattr(mesh, 'bounds') else np.array([[-1,-1,-1],[1,1,1]])
            
        extents = bounds[1] - bounds[0]
        max_extent = np.max(extents)
        
        # Set camera distance based on object size
        camera_distance = max_extent / initial_zoom
        scene.camera.z_far = camera_distance * 10
        scene.camera.z_near = camera_distance * 0.01
        
        # Position camera
        scene.set_camera(angles=[np.pi/6, np.pi/6, 0], distance=camera_distance)
        
        scene.show()


def render_multiple(tetrahedrons, colors=None):
    """
    Render multiple truncated tetrahedrons.
    
    Args:
        tetrahedrons: List of TruncatedTetrahedron objects
        colors: Optional list of colors for each tetrahedron
    """
    if colors is None:
        colors = ['red', 'blue'] * (len(tetrahedrons) // 2 + 1)
    
    meshes = []
    for i, tet in enumerate(tetrahedrons):
        mesh = tet.create_mesh(with_ports=True)
        
        # Set color
        color = colors[i % len(colors)]
        if color == 'red':
            mesh.visual.vertex_colors = [255, 0, 0, 200]
        elif color == 'blue':
            mesh.visual.vertex_colors = [0, 0, 255, 200]
        else:
            mesh.visual.vertex_colors = [128, 128, 128, 200]
        
        meshes.append(mesh)
    
    # Combine and show
    scene = trimesh.Scene(meshes)
    scene.show()


# Test the module
if __name__ == "__main__":
    print("Creating truncated tetrahedron with triangular ports...")
    
    # Create a single truncated tetrahedron
    tet = TruncatedTetrahedron(edge_length=1.0, port_rotation=0)
    
    # Display it
    print("Rendering...")
    tet.show()
    
    # Test multiple tetrahedrons
    print("\nCreating multiple tetrahedrons...")
    tet1 = TruncatedTetrahedron(edge_length=1.0, port_rotation=0)
    tet2 = TruncatedTetrahedron(edge_length=1.0, port_rotation=np.pi/3)
    
    # Translate the second one
    tet2.vertices += np.array([2, 0, 0])
    
    render_multiple([tet1, tet2], colors=['red', 'blue'])
