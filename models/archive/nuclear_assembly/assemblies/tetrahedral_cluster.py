# nuclear_assembly/assemblies/tetrahedral_cluster.py
"""
Tetrahedral cluster assembly with individual satellite rotation control.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from geometry.face_labeling import LabeledTetrahedron
from geometry.constants import r_eff_HH, COUPLING_HH


class TetrahedralCluster:
    """
    Four tetrahedra in tetrahedral arrangement.
    One inverted at center, three upright at vertices.
    Can rotate individual satellites around their bond axes.
    """
    
    def __init__(self, sat_rotations: List[float] = None):
        """
        Create tetrahedral cluster.
        
        Args:
            sat_rotations: List of rotation angles for each satellite [sat1, sat2, sat3] in degrees
                          Default is [0, 0, 0]
        """
        if sat_rotations is None:
            sat_rotations = [0, 0, 0]
        
        self.sat_rotations = sat_rotations
        
        # Create the four tetrahedra
        self.center = LabeledTetrahedron()  # Will be inverted
        self.sat1 = LabeledTetrahedron()    # Satellite 1
        self.sat2 = LabeledTetrahedron()    # Satellite 2
        self.sat3 = LabeledTetrahedron()    # Satellite 3
        
        # Store as list for easier iteration
        self.satellites = [self.sat1, self.sat2, self.sat3]
        
        # Invert the center tetrahedron
        self._invert_center()
        
        # Position satellites around center with individual rotations
        self._position_satellites()
        
        # Create inter-satellite bonds
        self._bond_satellites()
        
        # Store bond information
        self.bonds = []
        self._record_bonds()
    
    def _invert_center(self):
        """Invert the center tetrahedron (flip it upside down)."""
        # Flip around xy plane
        self.center.vertices[:, 2] *= -1
        
        # This makes the center's H0 face point down and T faces point up
        # We need to relabel to maintain consistency
        # After inversion, what was "up" is now "down"
    
    def _position_satellites(self):
        """Position three satellites with individual rotations."""
        # The center has 3 hex faces (H1, H2, H3) available for bonding
        center_faces = ['H1', 'H2', 'H3']
        
        for i, (sat, face_label, rotation_deg) in enumerate(zip(
            self.satellites, center_faces, self.sat_rotations)):
            
            # Get center's face info
            center_face = self.center.get_face(face_label)
            center_face_center = self.center.get_face_center(center_face)
            center_face_normal = self.center.get_face_normal(center_face)
            
            # Satellite will bond its H0 to center's face
            sat_face = sat.get_face('H0')
            sat_face_center = sat.get_face_center(sat_face)
            sat_face_normal = sat.get_face_normal(sat_face)
            
            # Rotate satellite so its H0 faces opposite to center's face
            target_normal = -center_face_normal
            rotation = self._rotation_between_vectors(sat_face_normal, target_normal)
            sat.vertices = (rotation @ sat.vertices.T).T
            
            # Apply individual rotation for this satellite
            if abs(rotation_deg) > 0.001:
                twist_rad = np.radians(rotation_deg)
                twist_rotation = self._rotation_around_axis(target_normal, twist_rad)
                sat.vertices = (twist_rotation @ sat.vertices.T).T
                print(f"  Satellite {i+1}: Rotated {rotation_deg}° around bond axis")
            
            # Recalculate face center after rotation
            sat_face_center = sat.get_face_center(sat.get_face('H0'))
            
            # Translate satellite to position
            separation = 0.02  # Small gap for visualization
            translation = center_face_center + center_face_normal * separation - sat_face_center
            sat.vertices = sat.vertices + translation
    
    def _bond_satellites(self):
        """Create H-H bonds between adjacent satellites."""
        # Each satellite needs to bond to its two neighbors
        # Sat1 bonds to Sat2 and Sat3
        # Sat2 bonds to Sat3 (and Sat1 already done)
        
        # The satellites form a triangle, each needs to find the best face to bond
        satellite_bonds = [
            (0, 1),  # sat1 to sat2
            (1, 2),  # sat2 to sat3
            (2, 0),  # sat3 to sat1
        ]
        
        for idx1, idx2 in satellite_bonds:
            sat1 = self.satellites[idx1]
            sat2 = self.satellites[idx2]
            
            # Find best matching faces between satellites
            # They each have H1, H2, H3 available (H0 is bonded to center)
            best_match = self._find_best_face_match(sat1, sat2, 
                                                   exclude1=['H0'], 
                                                   exclude2=['H0'])
            
            if best_match:
                # For this implementation, we just record the bond
                # In reality, satellites are already positioned by center bonds
                # Additional positioning would require optimization
                pass
    
    def _find_best_face_match(self, tet1: LabeledTetrahedron, 
                            tet2: LabeledTetrahedron,
                            exclude1: List[str] = None,
                            exclude2: List[str] = None) -> Tuple[str, str]:
        """Find best matching faces between two tetrahedra."""
        if exclude1 is None:
            exclude1 = []
        if exclude2 is None:
            exclude2 = []
            
        faces1 = [f'H{i}' for i in range(4) if f'H{i}' not in exclude1]
        faces2 = [f'H{i}' for i in range(4) if f'H{i}' not in exclude2]
        
        best_match = None
        best_score = float('inf')
        
        for f1 in faces1:
            face1_center = tet1.get_face_center(tet1.get_face(f1))
            face1_normal = tet1.get_face_normal(tet1.get_face(f1))
            
            for f2 in faces2:
                face2_center = tet2.get_face_center(tet2.get_face(f2))
                face2_normal = tet2.get_face_normal(tet2.get_face(f2))
                
                # Check if faces are roughly opposing
                dot = np.dot(face1_normal, face2_normal)
                if dot < -0.5:  # Roughly opposite
                    distance = np.linalg.norm(face2_center - face1_center)
                    if distance < best_score:
                        best_score = distance
                        best_match = (f1, f2)
        
        return best_match
    
    def _record_bonds(self):
        """Record all bonds in the cluster."""
        # Center to satellites (3 bonds)
        for i, sat in enumerate(self.satellites):
            self.bonds.append({
                'type': 'HH',
                'from': ('center', f'H{i+1}'),
                'to': (f'sat{i+1}', 'H0'),
                'r_eff': r_eff_HH(),
                'coupling': COUPLING_HH
            })
        
        # Between satellites (3 bonds)
        satellite_pairs = [(0, 1), (1, 2), (2, 0)]
        for idx1, idx2 in satellite_pairs:
            # Find which faces are bonding
            match = self._find_best_face_match(
                self.satellites[idx1], 
                self.satellites[idx2],
                exclude1=['H0'], 
                exclude2=['H0']
            )
            
            if match:
                self.bonds.append({
                    'type': 'HH',
                    'from': (f'sat{idx1+1}', match[0]),
                    'to': (f'sat{idx2+1}', match[1]),
                    'r_eff': r_eff_HH(),
                    'coupling': COUPLING_HH
                })
    
    def _rotation_between_vectors(self, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """Calculate rotation matrix to rotate v1 to v2."""
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        
        if np.allclose(v1, v2):
            return np.eye(3)
        
        if np.allclose(v1, -v2):
            perp = np.array([1, 0, 0]) if abs(v1[0]) < 0.9 else np.array([0, 1, 0])
            perp = perp - np.dot(perp, v1) * v1
            perp = perp / np.linalg.norm(perp)
            return 2 * np.outer(perp, perp) - np.eye(3)
        
        axis = np.cross(v1, v2)
        axis = axis / np.linalg.norm(axis)
        angle = np.arccos(np.clip(np.dot(v1, v2), -1, 1))
        return self._rotation_around_axis(axis, angle)
    
    def _rotation_around_axis(self, axis: np.ndarray, angle: float) -> np.ndarray:
        """Create rotation matrix for rotation around axis."""
        axis = axis / np.linalg.norm(axis)
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        ux, uy, uz = axis
        
        return np.array([
            [cos_a + ux**2*(1-cos_a), ux*uy*(1-cos_a) - uz*sin_a, ux*uz*(1-cos_a) + uy*sin_a],
            [uy*ux*(1-cos_a) + uz*sin_a, cos_a + uy**2*(1-cos_a), uy*uz*(1-cos_a) - ux*sin_a],
            [uz*ux*(1-cos_a) - uy*sin_a, uz*uy*(1-cos_a) + ux*sin_a, cos_a + uz**2*(1-cos_a)]
        ])
    
    def report_geometry(self):
        """Report cluster geometry."""
        print("Tetrahedral Cluster Configuration")
        print("="*50)
        print("Structure: 1 inverted center + 3 upright satellites")
        print(f"Satellite rotations: {self.sat_rotations}°")
        print(f"Total bonds: {len(self.bonds)}")
        print("\nBonds:")
        for bond in self.bonds:
            print(f"  {bond['from'][0]}:{bond['from'][1]} <-> "
                  f"{bond['to'][0]}:{bond['to'][1]} ({bond['type']})")
        
        # Calculate cluster size
        all_vertices = np.vstack([
            self.center.vertices,
            self.sat1.vertices,
            self.sat2.vertices,
            self.sat3.vertices
        ])
        
        bounds = [all_vertices.min(axis=0), all_vertices.max(axis=0)]
        size = bounds[1] - bounds[0]
        
        print(f"\nCluster dimensions: {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f}")
        print(f"Volume: {np.prod(size):.2f}")
        
        # Check if it's flat (one dimension much smaller)
        min_dim = np.min(size)
        max_dim = np.max(size)
        if min_dim / max_dim < 0.5:
            print("✓ Forms a flat (planar) configuration")
        else:
            print("Forms a 3D configuration")
