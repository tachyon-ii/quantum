"""
Tetrahedral mesh utilities for Sierpinski fractal structures.
Advanced geometric calculations for James Freeman's nuclear theory.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull, Delaunay
from dataclasses import dataclass

@dataclass
class TetrahedralFace:
    """Represents one face of a tetrahedral mesh"""
    vertices: np.ndarray  # 3x3 array
    normal: np.ndarray
    area: float
    face_id: int
    triangulation: Optional[List] = None

class TetrahedralMeshGenerator:
    """
    Advanced tetrahedral mesh generation for nuclear capsid structures.
    
    Implements the geometric foundation of James's theory:
    - Perfect tetrahedral symmetry for stability
    - Fractal subdivision for pore structure  
    - Precise geometric calculations for binding analysis
    """
    
    def __init__(self):
        self.golden_ratio = (1 + np.sqrt(5)) / 2
        self.mesh_cache = {}
    
    def create_perfect_tetrahedron(self, radius: float = 1.0, center: np.ndarray = None) -> Tuple[np.ndarray, List[TetrahedralFace]]:
        """
        Create a perfect regular tetrahedron inscribed in a sphere.
        
        Args:
            radius: Radius of circumscribing sphere
            center: Center point (default: origin)
            
        Returns:
            Tuple of (vertices, faces)
        """
        if center is None:
            center = np.array([0.0, 0.0, 0.0])
        
        # Regular tetrahedron vertices in optimal orientation
        # Using the fact that a regular tetrahedron can be constructed
        # by taking alternating vertices of a cube
        
        a = radius * np.sqrt(8/9)  # Distance from center to vertex
        
        vertices = np.array([
            [1, 1, 1],
            [1, -1, -1], 
            [-1, 1, -1],
            [-1, -1, 1]
        ]) * a / np.sqrt(3) + center
        
        # Define the four triangular faces
        face_indices = [
            [0, 1, 2],  # Face 1
            [0, 1, 3],  # Face 2  
            [0, 2, 3],  # Face 3
            [1, 2, 3]   # Face 4
        ]
        
        faces = []
        for i, face_idx in enumerate(face_indices):
            face_vertices = vertices[face_idx]
            face = TetrahedralFace(
                vertices=face_vertices,
                normal=self._calculate_outward_normal(face_vertices, center),
                area=self._calculate_triangle_area(face_vertices),
                face_id=i
            )
            faces.append(face)
        
        return vertices, faces
    
    def create_dual_tetrahedron(self, vertices: np.ndarray) -> Tuple[np.ndarray, List[TetrahedralFace]]:
        """
        Create the dual tetrahedron (stellated form) for complex capsid geometry.
        
        This creates interpenetrating tetrahedral structures that James suggests
        might be involved in quark confinement.
        """
        center = np.mean(vertices, axis=0)
        
        # Dual vertices are at face centers of original tetrahedron
        face_indices = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
        dual_vertices = []
        
        for face_idx in face_indices:
            face_center = np.mean(vertices[face_idx], axis=0)
            # Project outward from center
            direction = face_center - center
            direction = direction / np.linalg.norm(direction)
            # Place dual vertex at same distance as original vertices
            original_distance = np.linalg.norm(vertices[0] - center)
            dual_vertex = center + direction * original_distance
            dual_vertices.append(dual_vertex)
        
        dual_vertices = np.array(dual_vertices)
        
        # Create faces for dual tetrahedron
        _, dual_faces = self.create_perfect_tetrahedron(
            radius=np.linalg.norm(dual_vertices[0] - center),
            center=center
        )
        
        # Update face vertices to use dual vertices
        for i, face in enumerate(dual_faces):
            face.vertices = dual_vertices[[[0,1,2], [0,1,3], [0,2,3], [1,2,3]][i]]
            face.normal = self._calculate_outward_normal(face.vertices, center)
            face.area = self._calculate_triangle_area(face.vertices)
        
        return dual_vertices, dual_faces
    
    def subdivide_tetrahedral_face(self, face: TetrahedralFace, order: int) -> List[np.ndarray]:
        """
        Subdivide a tetrahedral face using Sierpinski fractal pattern.
        
        Args:
            face: TetrahedralFace to subdivide
            order: Subdivision order (0=no subdivision, 1=3 triangles, 2=9 triangles, etc.)
            
        Returns:
            List of triangle vertex arrays
        """
        if order == 0:
            return [face.vertices]
        
        triangles = []
        
        def recursive_subdivide(triangle_vertices, current_order):
            if current_order == 0:
                triangles.append(triangle_vertices.copy())
                return
            
            # Find edge midpoints
            v0, v1, v2 = triangle_vertices
            mid01 = (v0 + v1) / 2
            mid12 = (v1 + v2) / 2  
            mid20 = (v2 + v0) / 2
            
            # Three corner triangles (Sierpinski pattern)
            corner_triangles = [
                np.array([v0, mid01, mid20]),
                np.array([v1, mid12, mid01]),
                np.array([v2, mid20, mid12])
            ]
            
            # Recursively subdivide each corner
            for corner in corner_triangles:
                recursive_subdivide(corner, current_order - 1)
        
        recursive_subdivide(face.vertices, order)
        return triangles
    
    def calculate_pore_locations(self, subdivided_triangles: List[np.ndarray], order: int) -> List[np.ndarray]:
        """
        Calculate the locations of pores in a Sierpinski subdivision.
        
        Pores occur at the centers of the "holes" in the fractal pattern.
        """
        if order == 0:
            return []
        
        pore_centers = []
        
        # Group triangles by subdivision level to find gaps
        if order == 1:
            # For order 1, there's one central pore
            # Find the centroid of the three corner triangles
            if len(subdivided_triangles) == 3:
                all_vertices = np.vstack(subdivided_triangles)
                outer_vertices = []
                
                # Find the three vertices that are farthest from the center
                center = np.mean(all_vertices, axis=0)
                distances = [np.linalg.norm(v - center) for v in all_vertices]
                sorted_indices = np.argsort(distances)
                
                # Take the three farthest vertices (corners of original triangle)
                corner_indices = sorted_indices[-3:]
                corner_vertices = all_vertices[corner_indices]
                
                # Pore center is at centroid of original triangle
                pore_center = np.mean(corner_vertices, axis=0)
                pore_centers.append(pore_center)
        
        elif order >= 2:
            # For higher orders, use more sophisticated pore detection
            # This is a simplified approach - full implementation would use
            # topological analysis of the fractal structure
            
            # Find interior points that are equidistant from multiple triangles
            triangle_centers = [np.mean(tri, axis=0) for tri in subdivided_triangles]
            
            # Use clustering to find pore regions
            from sklearn.cluster import DBSCAN

            points = np.array(triangle_centers)
            if len(points) > 3:
                clustering = DBSCAN(eps=0.3, min_samples=2).fit(points)
                
                # Pores occur in regions with low triangle density
                unique_labels = set(clustering.labels_)
                for label in unique_labels:
                    if label != -1:  # -1 is noise in DBSCAN
                        cluster_points = points[clustering.labels_ == label]
                        if len(cluster_points) >= 2:
                           # Calculate the centroid of gaps between clusters
                           cluster_center = np.mean(cluster_points, axis=0)
                           
                           # Find the point that's farthest from all triangles in this cluster
                           # This approximates the pore location
                           max_distance = 0
                           best_pore_location = cluster_center
                           
                           # Sample points around cluster center to find optimal pore location
                           for theta in np.linspace(0, 2*np.pi, 12):
                               for r in np.linspace(0.1, 0.5, 5):
                                   test_point = cluster_center + r * np.array([np.cos(theta), np.sin(theta), 0])
                                   
                                   # Calculate minimum distance to any triangle center
                                   min_dist_to_triangle = min(np.linalg.norm(test_point - tc) for tc in triangle_centers)
                                   
                                   if min_dist_to_triangle > max_distance:
                                       max_distance = min_dist_to_triangle
                                       best_pore_location = test_point
                           
                           if max_distance > 0.2:  # Minimum threshold for a valid pore
                               pore_centers.append(best_pore_location)
       
        return pore_centers
   
    def calculate_mesh_properties(self, vertices: np.ndarray, faces: List[TetrahedralFace]) -> Dict[str, float]:
       """Calculate geometric properties of the tetrahedral mesh"""
       
       # Basic properties
       center = np.mean(vertices, axis=0)
       
       # Calculate distances from center to each vertex
       distances = [np.linalg.norm(v - center) for v in vertices]
       
       # Calculate edge lengths
       edge_lengths = []
       n_vertices = len(vertices)
       for i in range(n_vertices):
           for j in range(i + 1, n_vertices):
               edge_length = np.linalg.norm(vertices[i] - vertices[j])
               edge_lengths.append(edge_length)
       
       # Calculate face areas and total surface area
       total_surface_area = sum(face.area for face in faces)
       
       # Calculate volume using divergence theorem
       volume = self._calculate_tetrahedron_volume(vertices)
       
       # Calculate sphere metrics
       circumradius = max(distances)
       inradius = 3 * volume / total_surface_area
       
       # Geometric ratios
       sphericity = (np.pi**(1/3) * (6*volume)**(2/3)) / total_surface_area
       aspect_ratio = max(edge_lengths) / min(edge_lengths) if edge_lengths else 1.0
       
       return {
           'volume': volume,
           'surface_area': total_surface_area,
           'circumradius': circumradius,
           'inradius': inradius,
           'sphericity': sphericity,
           'aspect_ratio': aspect_ratio,
           'average_edge_length': np.mean(edge_lengths),
           'edge_length_std': np.std(edge_lengths),
           'center': center,
           'vertices_count': n_vertices,
           'faces_count': len(faces)
       }
   
    def _calculate_outward_normal(self, triangle_vertices: np.ndarray, center: np.ndarray) -> np.ndarray:
       """Calculate outward-pointing normal vector for a triangle face"""
       v1 = triangle_vertices[1] - triangle_vertices[0]
       v2 = triangle_vertices[2] - triangle_vertices[0]
       normal = np.cross(v1, v2)
       normal = normal / np.linalg.norm(normal)
       
       # Ensure normal points outward from center
       face_center = np.mean(triangle_vertices, axis=0)
       to_face = face_center - center
       if np.dot(normal, to_face) < 0:
           normal = -normal
       
       return normal
   
    def _calculate_triangle_area(self, vertices: np.ndarray) -> float:
       """Calculate area of triangle using cross product"""
       v1 = vertices[1] - vertices[0]
       v2 = vertices[2] - vertices[0]
       cross = np.cross(v1, v2)
       return 0.5 * np.linalg.norm(cross)
   
    def _calculate_tetrahedron_volume(self, vertices: np.ndarray) -> float:
       """Calculate volume of tetrahedron"""
       if len(vertices) != 4:
           return 0.0
       
       # Volume = |det(v1-v0, v2-v0, v3-v0)| / 6
       v0 = vertices[0]
       matrix = np.array([
           vertices[1] - v0,
           vertices[2] - v0, 
           vertices[3] - v0
       ]).T
       
       return abs(np.linalg.det(matrix)) / 6.0
   
    def create_compound_tetrahedral_mesh(self, num_tetrahedra: int = 2, 
                                      separation: float = 2.0) -> Dict[str, any]:
       """
       Create compound tetrahedral mesh for multi-nucleon systems.
       
       This models nuclear configurations like deuteron, tritium, etc.
       
       Args:
           num_tetrahedra: Number of nucleons
           separation: Distance between nucleon centers
           
       Returns:
           Dictionary with complete mesh data
       """
       
       if num_tetrahedra == 2:
           # Deuteron: Two tetrahedra along x-axis
           centers = [
               np.array([-separation/2, 0, 0]),
               np.array([separation/2, 0, 0])
           ]
           
       elif num_tetrahedra == 3:
           # Tritium/Helium-3: Three tetrahedra in triangle
           angle_step = 2 * np.pi / 3
           radius = separation / np.sqrt(3)  # Equilateral triangle
           centers = [
               np.array([radius * np.cos(i * angle_step), radius * np.sin(i * angle_step), 0])
               for i in range(3)
           ]
           
       elif num_tetrahedra == 4:
           # Helium-4: Four tetrahedra in tetrahedral arrangement
           base_radius = separation / 2
           height = separation * np.sqrt(2/3)
           centers = [
               np.array([base_radius, 0, -height/3]),
               np.array([-base_radius/2, base_radius*np.sqrt(3)/2, -height/3]),
               np.array([-base_radius/2, -base_radius*np.sqrt(3)/2, -height/3]),
               np.array([0, 0, 2*height/3])
           ]
           
       else:
           # Linear arrangement for other cases
           centers = [np.array([i * separation, 0, 0]) for i in range(num_tetrahedra)]
       
       # Create individual tetrahedra
       compound_mesh = {
           'nucleon_count': num_tetrahedra,
           'nucleon_meshes': [],
           'compound_properties': {},
           'binding_analysis': {}
       }
       
       for i, center in enumerate(centers):
           vertices, faces = self.create_perfect_tetrahedron(radius=0.8, center=center)
           properties = self.calculate_mesh_properties(vertices, faces)
           
           nucleon_mesh = {
               'nucleon_id': i,
               'center': center,
               'vertices': vertices,
               'faces': faces,
               'properties': properties
           }
           compound_mesh['nucleon_meshes'].append(nucleon_mesh)
       
       # Calculate compound properties
       compound_mesh['compound_properties'] = self._analyze_compound_geometry(compound_mesh['nucleon_meshes'])
       
       # Analyze potential binding interfaces
       compound_mesh['binding_analysis'] = self._analyze_binding_interfaces(compound_mesh['nucleon_meshes'])
       
       return compound_mesh
   
    def _analyze_compound_geometry(self, nucleon_meshes: List[Dict]) -> Dict[str, any]:
       """Analyze geometric properties of compound nuclear system"""
       
       centers = np.array([mesh['center'] for mesh in nucleon_meshes])
       
       # Calculate center of mass
       center_of_mass = np.mean(centers, axis=0)
       
       # Calculate moments of inertia tensor (simplified)
       positions_rel = centers - center_of_mass
       
       # Principal moments (eigenvalues of inertia tensor)
       inertia_tensor = np.zeros((3, 3))
       for pos in positions_rel:
           r_squared = np.dot(pos, pos)
           inertia_tensor += r_squared * np.eye(3) - np.outer(pos, pos)
       
       eigenvalues, eigenvectors = np.linalg.eigh(inertia_tensor)
       
       # Inter-nucleon distances
       distances = []
       for i in range(len(centers)):
           for j in range(i + 1, len(centers)):
               distance = np.linalg.norm(centers[i] - centers[j])
               distances.append(distance)
       
       # Geometric classification
       if len(nucleon_meshes) == 2:
           geometry_type = 'linear_dimer'
       elif len(nucleon_meshes) == 3:
           # Check if triangular or linear
           if len(distances) == 3:
               d1, d2, d3 = sorted(distances)
               if abs(d1 - d2) < 0.1 and abs(d2 - d3) < 0.1:
                   geometry_type = 'equilateral_triangle'
               elif d3 > d1 + d2 - 0.1:  # Nearly linear
                   geometry_type = 'linear_trimer'
               else:
                   geometry_type = 'isosceles_triangle'
           else:
               geometry_type = 'triangle'
       elif len(nucleon_meshes) == 4:
           geometry_type = 'tetrahedral'
       else:
           geometry_type = 'complex'
       
       return {
           'center_of_mass': center_of_mass,
           'principal_moments': eigenvalues,
           'principal_axes': eigenvectors,
           'inter_nucleon_distances': distances,
           'average_distance': np.mean(distances),
           'distance_std': np.std(distances),
           'geometry_type': geometry_type,
           'compactness': min(distances) / max(distances) if distances else 1.0
       }
   
    def _analyze_binding_interfaces(self, nucleon_meshes: List[Dict]) -> Dict[str, any]:
       """Analyze potential binding interfaces between nucleons"""
       
       interfaces = []
       
       for i in range(len(nucleon_meshes)):
           for j in range(i + 1, len(nucleon_meshes)):
               mesh1 = nucleon_meshes[i]
               mesh2 = nucleon_meshes[j]
               
               # Calculate closest approach between surfaces
               min_distance = float('inf')
               closest_points = (None, None)
               
               # Check all face-to-face distances
               for face1 in mesh1['faces']:
                   for face2 in mesh2['faces']:
                       # Distance between face centroids
                       center1 = np.mean(face1.vertices, axis=0)
                       center2 = np.mean(face2.vertices, axis=0)
                       distance = np.linalg.norm(center1 - center2)
                       
                       if distance < min_distance:
                           min_distance = distance
                           closest_points = (center1, center2)
               
               # Calculate interface area (overlap region)
               interface_area = self._calculate_interface_area(mesh1, mesh2, min_distance)
               
               # Calculate orientation (how faces align)
               alignment = self._calculate_face_alignment(mesh1, mesh2, closest_points)
               
               interface = {
                   'nucleon_pair': (i, j),
                   'min_distance': min_distance,
                   'closest_points': closest_points,
                   'interface_area': interface_area,
                   'alignment_factor': alignment,
                   'binding_potential': interface_area * alignment / max(min_distance, 0.1)
               }
               interfaces.append(interface)
       
       return {
           'interfaces': interfaces,
           'total_binding_potential': sum(iface['binding_potential'] for iface in interfaces),
           'strongest_interface': max(interfaces, key=lambda x: x['binding_potential']) if interfaces else None
       }
   
    def _calculate_interface_area(self, mesh1: Dict, mesh2: Dict, separation: float) -> float:
       """Calculate effective interface area between two nucleon meshes"""
       
       # Simplified calculation based on sphere overlap
       radius1 = mesh1['properties']['circumradius']
       radius2 = mesh2['properties']['circumradius']
       
       if separation >= radius1 + radius2:
           return 0.0  # No overlap
       
       # Approximate interface area using sphere intersection formula
       if separation <= abs(radius1 - radius2):
           # One sphere inside the other
           return np.pi * min(radius1, radius2)**2
       
       # Partial overlap
       h1 = (radius1**2 - radius2**2 + separation**2) / (2 * separation)
       h2 = separation - h1
       
       area1 = np.pi * (radius1**2 - h1**2) if h1 < radius1 else 0
       area2 = np.pi * (radius2**2 - h2**2) if h2 < radius2 else 0
       
       return (area1 + area2) / 2  # Average interface area
   
    def _calculate_face_alignment(self, mesh1: Dict, mesh2: Dict, closest_points: Tuple) -> float:
       """Calculate how well faces align between two meshes"""
       
       if closest_points[0] is None or closest_points[1] is None:
           return 0.0
       
       point1, point2 = closest_points
       connection_vector = point2 - point1
       connection_vector = connection_vector / np.linalg.norm(connection_vector)
       
       # Find faces closest to the connection points
       best_alignment = 0.0
       
       for face1 in mesh1['faces']:
           face1_center = np.mean(face1.vertices, axis=0)
           if np.linalg.norm(face1_center - point1) < 0.5:  # Close to connection point
               
               for face2 in mesh2['faces']:
                   face2_center = np.mean(face2.vertices, axis=0)
                   if np.linalg.norm(face2_center - point2) < 0.5:
                       
                       # Calculate alignment between face normals and connection vector
                       alignment1 = abs(np.dot(face1.normal, connection_vector))
                       alignment2 = abs(np.dot(face2.normal, -connection_vector))
                       
                       total_alignment = (alignment1 + alignment2) / 2
                       best_alignment = max(best_alignment, total_alignment)
       
       return best_alignment

def create_tetrahedral_mesh_visualization():
   """Create comprehensive visualization of tetrahedral mesh structures"""
   
   generator = TetrahedralMeshGenerator()
   
   # Create visualization for different nuclear configurations
   configurations = ['deuteron', 'tritium', 'helium4']
   nucleon_counts = [2, 3, 4]
   
   fig = plt.figure(figsize=(20, 12))
   
   for idx, (config_name, num_nucleons) in enumerate(zip(configurations, nucleon_counts)):
       # Create compound mesh
       compound_mesh = generator.create_compound_tetrahedral_mesh(
           num_tetrahedra=num_nucleons, 
           separation=2.5
       )
       
       # 3D visualization
       ax = fig.add_subplot(2, 3, idx + 1, projection='3d')
       ax.set_title(f'{config_name.title()} - Tetrahedral Mesh')
       
       colors = ['red', 'blue', 'green', 'orange']
       
       for i, nucleon_mesh in enumerate(compound_mesh['nucleon_meshes']):
           vertices = nucleon_mesh['vertices']
           faces = nucleon_mesh['faces']
           color = colors[i % len(colors)]
           
           # Plot vertices
           ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
                     c=color, s=100, alpha=0.8, label=f'Nucleon {i+1}')
           
           # Plot edges
           for face in faces:
               face_vertices = face.vertices
               # Plot triangle edges
               for j in range(3):
                   start = face_vertices[j]
                   end = face_vertices[(j+1) % 3]
                   ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], 
                          color=color, alpha=0.6, linewidth=1)
       
       # Plot binding interfaces
       binding_analysis = compound_mesh['binding_analysis']
       for interface in binding_analysis['interfaces']:
           if interface['binding_potential'] > 0.1:  # Only show significant interfaces
               p1, p2 = interface['closest_points']
               ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                      'k--', linewidth=3, alpha=0.8, label='Binding Interface')
       
       ax.set_xlabel('X (fm)')
       ax.set_ylabel('Y (fm)')
       ax.set_zlabel('Z (fm)')
       ax.legend()
       
       # Properties table
       ax_table = fig.add_subplot(2, 3, idx + 4)
       ax_table.axis('off')
       ax_table.set_title(f'{config_name.title()} - Properties')
       
       props = compound_mesh['compound_properties']
       binding = compound_mesh['binding_analysis']
       
       properties_text = f"""
Nucleon Count: {compound_mesh['nucleon_count']}
Geometry Type: {props['geometry_type']}
Average Distance: {props['average_distance']:.2f} fm
Compactness: {props['compactness']:.3f}

Binding Analysis:
Total Interfaces: {len(binding['interfaces'])}
Total Binding Potential: {binding['total_binding_potential']:.3f}
Strongest Interface: {(binding['strongest_interface']['binding_potential'] if binding['strongest_interface'] else 0):.3f}

Inter-nucleon Distances:
"""
       
       for i, dist in enumerate(props['inter_nucleon_distances']):
           properties_text += f"  Pair {i+1}: {dist:.2f} fm\n"
       
       ax_table.text(0.1, 0.9, properties_text, transform=ax_table.transAxes, 
                    fontsize=9, verticalalignment='top', fontfamily='monospace')
   
   plt.tight_layout()
   plt.show()
   
   # Print summary analysis
   print("\n" + "="*80)
   print("TETRAHEDRAL MESH ANALYSIS - JAMES FREEMAN'S NUCLEAR THEORY")
   print("="*80)
   print("Core Principle: Nuclear binding via geometric pore structures in tetrahedral meshes")
   print("Mechanism: Sierpinski fractals → pore channels → lepton sharing → binding")
   print()
   
   for config_name, num_nucleons in zip(configurations, nucleon_counts):
       compound_mesh = generator.create_compound_tetrahedral_mesh(num_nucleons, 2.5)
       props = compound_mesh['compound_properties']
       binding = compound_mesh['binding_analysis']
       
       print(f"{config_name.upper()}:")
       print(f"  Nucleons: {num_nucleons}")
       print(f"  Geometry: {props['geometry_type']}")
       print(f"  Compactness: {props['compactness']:.3f}")
       print(f"  Binding Potential: {binding['total_binding_potential']:.3f}")
       print()

# Example usage and testing
if __name__ == "__main__":
   print("Creating tetrahedral mesh visualizations...")
   create_tetrahedral_mesh_visualization()
   
   # Test individual tetrahedron
   generator = TetrahedralMeshGenerator()
   vertices, faces = generator.create_perfect_tetrahedron(radius=1.0)
   properties = generator.calculate_mesh_properties(vertices, faces)
   
   print("\nPerfect Tetrahedron Properties:")
   for key, value in properties.items():
       if isinstance(value, (int, float)):
           print(f"  {key}: {value:.4f}")
       else:
           print(f"  {key}: {value}")