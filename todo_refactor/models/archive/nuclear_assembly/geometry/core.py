# nuclear_assembly/core/nucleus.py
"""
Simple, clean API for nuclear assembly.
"""

import numpy as np
import trimesh
from geometry.tetra_base import TruncatedTetrahedron

class Nucleon:
    """A single nucleon (proton or neutron)."""
    
    def __init__(self, type='proton'):
        self.type = type
        self.tt = TruncatedTetrahedron(edge_length=1.0)
        self.color = [255, 100, 100, 200] if type == 'proton' else [100, 100, 255, 200]
        
    def get_mesh(self):
        """Get trimesh representation - handles all the complexity internally."""
        hex_faces, tri_faces = self.tt.get_face_indices()
        
        triangles = []
        # Triangulate hexagons
        for hex_face in hex_faces:
            for i in range(1, len(hex_face) - 1):
                triangles.append([hex_face[0], hex_face[i], hex_face[i+1]])
        
        # Add triangles with correct winding
        for tri in tri_faces:
            # Check and fix winding automatically
            v = self.tt.vertices[tri]
            normal = np.cross(v[1] - v[0], v[2] - v[0])
            center = np.mean(self.tt.vertices, axis=0)
            face_center = np.mean(v, axis=0)
            
            if np.dot(normal, face_center - center) < 0:
                triangles.append([tri[0], tri[2], tri[1]])
            else:
                triangles.append(tri)
        
        mesh = trimesh.Trimesh(vertices=self.tt.vertices, faces=triangles)
        mesh.visual.face_colors = self.color
        return mesh


class Nucleus:
    """A collection of nucleons."""
    
    def __init__(self):
        self.nucleons = []
        
    def add(self, nucleon_type='proton', position=[0,0,0]):
        """Add a nucleon at position."""
        n = Nucleon(nucleon_type)
        n.tt.vertices += np.array(position)
        self.nucleons.append(n)
        return n
        
    def show(self):
        """Render the nucleus."""
        if not self.nucleons:
            print("No nucleons to show")
            return
            
        meshes = [n.get_mesh() for n in self.nucleons]
        combined = trimesh.util.concatenate(meshes) if len(meshes) > 1 else meshes[0]
        combined.show()


# Make it even simpler with convenience functions
def show(*nucleons):
    """Show one or more nucleons."""
    n = Nucleus()
    for nucleon in nucleons:
        if isinstance(nucleon, str):
            n.add(nucleon)
        elif isinstance(nucleon, tuple):
            n.add(nucleon[0], nucleon[1])
    n.show()
