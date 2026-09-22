"""
Sierpinski fractal generation and analysis for nuclear capsid structures.
Implements James Freeman's theory that nucleons are fractal tetrahedral meshes.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional, Set, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
from scipy.spatial.distance import cdist
import json

@dataclass
class Triangle:
    """Represents a single triangular unit (s-unit)"""
    vertices: np.ndarray  # 3x3 array of vertex coordinates
    center: np.ndarray    # Center point
    area: float
    normal: np.ndarray    # Surface normal vector
    id: int
    level: int = 0        # Fractal level (0 = base triangle)
    chirality: str = 'L'  # 'L' or 'R' for left/right handedness
    
    def __post_init__(self):
        if self.center is None:
            self.center = np.mean(self.vertices, axis=0)
        if self.normal is None:
            # Calculate normal using cross product
            v1 = self.vertices[1] - self.vertices[0]
            v2 = self.vertices[2] - self.vertices[0]
            self.normal = np.cross(v1, v2)
            self.normal = self.normal / np.linalg.norm(self.normal)

@dataclass
class Pore:
    """Represents a pore (hole) in the Sierpinski mesh"""
    center: np.ndarray
    vertices: List[np.ndarray]  # Vertices defining the pore boundary
    area: float
    diameter: float
    connectivity: List[int]     # IDs of connected triangles
    pore_type: str = 'internal' # 'internal', 'edge', 'vertex'

class SierpinskiGenerator:
    """
    Generates Sierpinski triangle fractals for nuclear capsid architecture.
    
    Key insight from James's theory:
    - Order 0: 4 triangles (basic tetrahedron) 
    - Order 1: 12 triangles (quark shell)
    - Order 2: 36 triangles (nucleon shell)
    - Pattern: N_triangles(n) = 4 * 3^n
    """
    
    def __init__(self):
        self.triangles = {}  # Dictionary of Triangle objects
        self.pores = {}      # Dictionary of Pore objects
        self.connectivity_graph = None
        self.triangle_counter = 0
        self.pore_counter = 0
    
    def generate_2d_sierpinski(self, order: int, base_size: float = 1.0) -> List[Triangle]:
        """
        Generate 2D Sierpinski triangle for visualization and analysis.
        
        Args:
            order: Fractal order (0, 1, 2, ...)
            base_size: Size of the base triangle
            
        Returns:
            List of Triangle objects
        """
        # Base triangle vertices
        height = base_size * np.sqrt(3) / 2
        base_vertices = np.array([
            [-base_size/2, -height/3, 0],
            [base_size/2, -height/3, 0], 
            [0, 2*height/3, 0]
        ])
        
        triangles = []
        
        def subdivide_triangle(vertices, current_order, target_order, chirality='L'):
            """Recursively subdivide triangle"""
            if current_order == target_order:
                # Create triangle at target order
                triangle = Triangle(
                    vertices=vertices.copy(),
                    center=np.mean(vertices, axis=0),
                    area=self._calculate_triangle_area(vertices),
                    normal=np.array([0, 0, 1]),  # 2D case
                    id=self.triangle_counter,
                    level=current_order,
                    chirality=chirality
                )
                self.triangle_counter += 1
                triangles.append(triangle)
                self.triangles[triangle.id] = triangle
                return
            
            # Find midpoints of edges
            mid01 = (vertices[0] + vertices[1]) / 2
            mid12 = (vertices[1] + vertices[2]) / 2
            mid20 = (vertices[2] + vertices[0]) / 2
            
            # Create three smaller triangles (corner triangles)
            corner_triangles = [
                np.array([vertices[0], mid01, mid20]),  # Bottom left
                np.array([vertices[1], mid12, mid01]),  # Bottom right  
                np.array([vertices[2], mid20, mid12])   # Top
            ]
            
            # Recursively subdivide each corner triangle
            for i, corner_tri in enumerate(corner_triangles):
                # Alternate chirality for geometric diversity
                new_chirality = 'R' if (chirality == 'L' and i % 2 == 1) else 'L'
                subdivide_triangle(corner_tri, current_order + 1, target_order, new_chirality)
        
        # Generate fractal
        subdivide_triangle(base_vertices, 0, order)
        
        return triangles
    
    def generate_tetrahedral_sierpinski(self, order: int, radius: float = 1.0) -> Tuple[List[Triangle], List[Pore]]:
        """
        Generate 3D tetrahedral Sierpinski mesh for nuclear capsids.
        
        This is the core of James's theory: nucleons as fractal tetrahedral meshes.
        
        Args:
            order: Fractal order (1 for quarks, 2 for nucleons)
            radius: Radius of containing sphere
            
        Returns:
            Tuple of (triangles, pores)
        """
        # Regular tetrahedron vertices
        # Using coordinates that center the tetrahedron at origin
        a = radius * np.sqrt(8/9)  # Distance from center to vertex
        tetrahedron_vertices = np.array([
            [a, a, a],
            [a, -a, -a],
            [-a, a, -a],
            [-a, -a, a]
        ]) / np.sqrt(3)
        
        # Tetrahedron faces (each face is a triangle)
        faces = [
            [0, 1, 2],  # Face 1
            [0, 1, 3],  # Face 2
            [0, 2, 3],  # Face 3
            [1, 2, 3]   # Face 4
        ]
        
        triangles = []
        all_pores = []
        
        # Generate Sierpinski pattern on each face
        for face_idx, face_vertices_idx in enumerate(faces):
            face_vertices = tetrahedron_vertices[face_vertices_idx]
            
            # Generate 2D Sierpinski on this face, then project to 3D
            face_triangles = self._generate_face_sierpinski(
                face_vertices, order, face_idx
            )
            triangles.extend(face_triangles)
            
            # Find pores on this face
            face_pores = self._find_face_pores(face_triangles, face_idx)
            all_pores.extend(face_pores)
        
        # Find inter-face pores (connecting different faces)
        inter_pores = self._find_inter_face_pores(triangles)
        all_pores.extend(inter_pores)
        
        # Store results
        for pore in all_pores:
            self.pores[self.pore_counter] = pore
            self.pore_counter += 1
        
        # Build connectivity graph
        self._build_connectivity_graph(triangles, all_pores)
        
        return triangles, all_pores
    
    def _generate_face_sierpinski(self, face_vertices: np.ndarray, order: int, face_id: int) -> List[Triangle]:
        """Generate Sierpinski pattern on a single tetrahedral face"""
        
        def subdivide_3d_triangle(vertices, current_order, target_order, face_id, chirality='L'):
            triangles = []
            
            if current_order == target_order:
                # Create triangle
                triangle = Triangle(
                    vertices=vertices.copy(),
                    center=np.mean(vertices, axis=0),
                    area=self._calculate_triangle_area(vertices),
                    normal=self._calculate_normal(vertices),
                    id=self.triangle_counter,
                    level=current_order,
                    chirality=chirality
                )
                self.triangle_counter += 1
                triangles.append(triangle)
                self.triangles[triangle.id] = triangle
                return triangles
            
            # Find edge midpoints
            mid01 = (vertices[0] + vertices[1]) / 2
            mid12 = (vertices[1] + vertices[2]) / 2
            mid20 = (vertices[2] + vertices[0]) / 2
            
            # Three corner triangles
            corner_triangles = [
                np.array([vertices[0], mid01, mid20]),
                np.array([vertices[1], mid12, mid01]),
                np.array([vertices[2], mid20, mid12])
            ]
            
            # Recursively subdivide
            for i, corner_tri in enumerate(corner_triangles):
                new_chirality = 'R' if (chirality == 'L' and i % 2 == 1) else 'L'
                subtriangles = subdivide_3d_triangle(
                    corner_tri, current_order + 1, target_order, face_id, new_chirality
                )
                triangles.extend(subtriangles)
            
            return triangles
        
        return subdivide_3d_triangle(face_vertices, 0, order, face_id)
    
    def _find_face_pores(self, triangles: List[Triangle], face_id: int) -> List[Pore]:
        """Find pores within a single face"""
        pores = []
        
        # Pores are the "holes" in the Sierpinski pattern
        # They occur at the centers of subdivided regions
        
        # Group triangles by their subdivision level
        triangles_by_level = {}
        for tri in triangles:
            level = tri.level
            if level not in triangles_by_level:
                triangles_by_level[level] = []
            triangles_by_level[level].append(tri)
        
        # Find gaps between triangles at each level
        for level, level_triangles in triangles_by_level.items():
            if level == 0:
                continue  # No pores at base level
            
            # Use Delaunay triangulation to find holes
            centers = np.array([tri.center for tri in level_triangles])
            pore_candidates = self._find_holes_in_triangulation(centers, level_triangles)
            
            for pore_center, connected_triangles in pore_candidates:
                pore = Pore(
                    center=pore_center,
                    vertices=self._get_pore_boundary_vertices(pore_center, connected_triangles),
                    area=self._calculate_pore_area(pore_center, connected_triangles),
                    diameter=self._calculate_pore_diameter(pore_center, connected_triangles),
                    connectivity=[tri.id for tri in connected_triangles],
                    pore_type='internal'
                )
                pores.append(pore)
        
        return pores
    
    def _find_inter_face_pores(self, triangles: List[Triangle]) -> List[Pore]:
        """Find pores that connect different faces (inter-nucleon channels)"""
        inter_pores = []
        
        # These are the critical pores for James's nuclear binding theory
        # They allow lepton sharing between nucleons
        
        # Group triangles by face (roughly)
        face_groups = self._group_triangles_by_face(triangles)
        
        # Find connection points between faces
        for face1_id, face1_triangles in face_groups.items():
            for face2_id, face2_triangles in face_groups.items():
                if face1_id >= face2_id:  # Avoid duplicates
                    continue
                
                # Find close triangles between faces
                connection_pores = self._find_face_connection_pores(
                    face1_triangles, face2_triangles
                )
                inter_pores.extend(connection_pores)
        
        return inter_pores
    
    def _calculate_triangle_area(self, vertices: np.ndarray) -> float:
        """Calculate area of triangle using cross product"""
        v1 = vertices[1] - vertices[0]
        v2 = vertices[2] - vertices[0]
        cross = np.cross(v1, v2)
        if cross.ndim == 1:  # 2D case
            return 0.5 * abs(cross) if np.isscalar(cross) else 0.5 * np.linalg.norm(cross)
        else:  # 3D case
            return 0.5 * np.linalg.norm(cross)
    
    def _calculate_normal(self, vertices: np.ndarray) -> np.ndarray:
        """Calculate surface normal of triangle"""
        v1 = vertices[1] - vertices[0]
        v2 = vertices[2] - vertices[0]
        normal = np.cross(v1, v2)
        norm = np.linalg.norm(normal)
        return normal / norm if norm > 0 else np.array([0, 0, 1])
    
    def _group_triangles_by_face(self, triangles: List[Triangle]) -> Dict[int, List[Triangle]]:
        """Group triangles by which tetrahedral face they belong to"""
        # Use clustering based on normal vectors
        normals = np.array([tri.normal for tri in triangles])
        
        # K-means clustering to group by 4 tetrahedral faces
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=4, random_state=42)
        face_labels = kmeans.fit_predict(normals)
        
        face_groups = {}
        for i, triangle in enumerate(triangles):
            face_id = face_labels[i]
            if face_id not in face_groups:
                face_groups[face_id] = []
            face_groups[face_id].append(triangle)
        
        return face_groups
    
    def _find_holes_in_triangulation(self, centers: np.ndarray, triangles: List[Triangle]) -> List[Tuple[np.ndarray, List[Triangle]]]:
        """Find holes in triangle arrangement that become pores"""
        from scipy.spatial import Delaunay
        
        if len(centers) < 3:
            return []
        
        # Project to 2D for Delaunay triangulation
        # Use PCA to find best 2D projection
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        centers_2d = pca.fit_transform(centers)
        
        # Delaunay triangulation
        tri = Delaunay(centers_2d)
        
        # Find circumcenters that are far from any triangle center
        # These represent holes in the mesh
        holes = []
        
        for simplex in tri.simplices:
            # Get the three triangle centers forming this Delaunay triangle
            tri_centers = centers[simplex]
            tri_objects = [triangles[i] for i in simplex]
            
            # Calculate circumcenter
            circumcenter = self._calculate_circumcenter_3d(tri_centers)
            
            # Check if this circumcenter represents a genuine hole
            if self._is_genuine_pore(circumcenter, tri_objects):
                holes.append((circumcenter, tri_objects))
        
        return holes
    
    def _calculate_circumcenter_3d(self, points: np.ndarray) -> np.ndarray:
        """Calculate circumcenter of three points in 3D"""
        if len(points) != 3:
            return np.mean(points, axis=0)
        
        # Use the average for simplicity (more complex calculation possible)
        return np.mean(points, axis=0)
    
    def _is_genuine_pore(self, center: np.ndarray, surrounding_triangles: List[Triangle]) -> bool:
        """Check if a point represents a genuine pore"""
        # Check distance to surrounding triangles
        min_distance = float('inf')
        for tri in surrounding_triangles:
            distance = np.linalg.norm(center - tri.center)
            min_distance = min(min_distance, distance)
        
        # If the center is reasonably far from triangles, it's a pore
        return min_distance > 0.1  # Threshold for pore detection
    
    def _get_pore_boundary_vertices(self, pore_center: np.ndarray, connected_triangles: List[Triangle]) -> List[np.ndarray]:
        """Get vertices that define the boundary of a pore"""
        # Collect all vertices from connected triangles
        all_vertices = []
        for tri in connected_triangles:
            all_vertices.extend(tri.vertices)
        
        # Remove duplicates and find vertices closest to pore center
        unique_vertices = []
        for vertex in all_vertices:
            is_duplicate = False
            for existing in unique_vertices:
                if np.linalg.norm(vertex - existing) < 1e-6:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_vertices.append(vertex)
        
        # Sort by distance to pore center and take closest ones
        unique_vertices.sort(key=lambda v: np.linalg.norm(v - pore_center))
        
        # Return 3-6 closest vertices that form the pore boundary
        return unique_vertices[:6]
    
    def _calculate_pore_area(self, pore_center: np.ndarray, connected_triangles: List[Triangle]) -> float:
        """Calculate effective area of a pore"""
        # Approximate as circle with radius = average distance to connected triangles
        distances = [np.linalg.norm(pore_center - tri.center) for tri in connected_triangles]
        avg_radius = np.mean(distances)
        return np.pi * avg_radius**2
    
    def _calculate_pore_diameter(self, pore_center: np.ndarray, connected_triangles: List[Triangle]) -> float:
        """Calculate effective diameter of a pore"""
        distances = [np.linalg.norm(pore_center - tri.center) for tri in connected_triangles]
        return 2 * np.mean(distances)
    
    def _find_face_connection_pores(self, face1_triangles: List[Triangle], face2_triangles: List[Triangle]) -> List[Pore]:
        """Find pores that connect two faces"""
        connection_pores = []
        
        # Find triangle pairs that are close between faces
        threshold_distance = 0.5  # Adjust based on geometry
        
        for tri1 in face1_triangles:
            for tri2 in face2_triangles:
                distance = np.linalg.norm(tri1.center - tri2.center)
                if distance < threshold_distance:
                    # Create connection pore
                    pore_center = (tri1.center + tri2.center) / 2
                    pore = Pore(
                        center=pore_center,
                        vertices=self._get_pore_boundary_vertices(pore_center, [tri1, tri2]),
                        area=self._calculate_pore_area(pore_center, [tri1, tri2]),
                        diameter=self._calculate_pore_diameter(pore_center, [tri1, tri2]),
                        connectivity=[tri1.id, tri2.id],
                        pore_type='inter_face'
                    )
                    connection_pores.append(pore)
        
        return connection_pores
    
    def _build_connectivity_graph(self, triangles: List[Triangle], pores: List[Pore]):
        """Build graph representation of triangle-pore connectivity"""
        self.connectivity_graph = nx.Graph()
        
        # Add triangle nodes
        for tri in triangles:
            self.connectivity_graph.add_node(f"tri_{tri.id}", type='triangle', object=tri)
        
        # Add pore nodes
        for pore in pores:
            pore_id = f"pore_{id(pore)}"  # Use memory ID since pores don't have IDs yet
            self.connectivity_graph.add_node(pore_id, type='pore', object=pore)
            
            # Connect pore to its triangles
            for tri_id in pore.connectivity:
                self.connectivity_graph.add_edge(f"tri_{tri_id}", pore_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the generated Sierpinski mesh"""
        triangles = list(self.triangles.values())
        pores = list(self.pores.values())
        
        stats = {
            'total_triangles': len(triangles),
            'total_pores': len(pores),
            'triangles_by_level': {},
            'triangles_by_chirality': {'L': 0, 'R': 0},
            'pores_by_type': {'internal': 0, 'inter_face': 0, 'edge': 0, 'vertex': 0},
            'average_triangle_area': 0.0,
            'average_pore_area': 0.0,
            'average_pore_diameter': 0.0,
            'connectivity_degree': 0.0
        }
        
        # Triangle statistics
        for tri in triangles:
            level = tri.level
            if level not in stats['triangles_by_level']:
                stats['triangles_by_level'][level] = 0
            stats['triangles_by_level'][level] += 1
            
            stats['triangles_by_chirality'][tri.chirality] += 1
            stats['average_triangle_area'] += tri.area
        
        if triangles:
            stats['average_triangle_area'] /= len(triangles)
        
        # Pore statistics
        for pore in pores:
            stats['pores_by_type'][pore.pore_type] += 1
            stats['average_pore_area'] += pore.area
            stats['average_pore_diameter'] += pore.diameter
        
        if pores:
            stats['average_pore_area'] /= len(pores)
            stats['average_pore_diameter'] /= len(pores)
        
        # Connectivity statistics
        if self.connectivity_graph:
            degrees = [self.connectivity_graph.degree(node) for node in self.connectivity_graph.nodes()]
            stats['connectivity_degree'] = np.mean(degrees) if degrees else 0.0
        
        return stats

# Example usage and testing
if __name__ == "__main__":
    # Generate Sierpinski meshes for different orders
    generator = SierpinskiGenerator()
    
    print("Generating Sierpinski meshes...")
    
    # Order 1: Quark shell (12 triangles)
    triangles_1, pores_1 = generator.generate_tetrahedral_sierpinski(order=1)
    stats_1 = generator.get_statistics()
    
    print(f"Order 1 (Quark): {stats_1['total_triangles']} triangles, {stats_1['total_pores']} pores")
    
    # Reset for Order 2
    generator = SierpinskiGenerator()
    
    # Order 2: Nucleon shell (36 triangles)  
    triangles_2, pores_2 = generator.generate_tetrahedral_sierpinski(order=2)
    stats_2 = generator.get_statistics()
    
    print(f"Order 2 (Nucleon): {stats_2['total_triangles']} triangles, {stats_2['total_pores']} pores")
    print(f"Theoretical triangles: Order 1 = {4 * 3**1}, Order 2 = {4 * 3**2}")