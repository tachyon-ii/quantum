from dataclasses import dataclass
from typing import Dict, List
import numpy as np
from nuclear_to_assembly.geometry.pose import NucleonPose, Port
from nuclear_to_assembly.geometry.constants import D_SS, D_HH
from nuclear_to_assembly.geometry.to_geometry import FACE_NORMALS
from nuclear_to_assembly.geometry.solids import truncated_octahedron_vertices_faces
from nuclear_to_assembly.geometry.transforms import I, Rx, Ry, Rz

@dataclass
class Bond:
    n1: str; face1: str
    n2: str; face2: str

@dataclass
class Assembly:
    name: str
    nucleons: Dict[str, NucleonPose]
    bonds: List[Bond]
    
    def __post_init__(self):
        """Automatically complete bonds based on geometry after initialization."""
        self._complete_bonds()

    def _complete_bonds(self, tolerance: float = 0.001, debug: bool = True):
        """Discover and add any missing bonds based on geometric criteria."""
        # Keep track of existing bonds to avoid duplicates
        existing = set()
        for b in self.bonds:
            existing.add((b.n1, b.face1, b.n2, b.face2))
            existing.add((b.n2, b.face2, b.n1, b.face1))

        original_count = len(self.bonds)
        nucleon_list = list(self.nucleons.values())

        if debug:
            print(f"\n  Checking {self.name}:")
            print(f"    Starting with {original_count} bonds")

        # Import Port for adding discovered ports
        from nuclear_to_assembly.geometry.pose import Port

        # Check all nucleon pairs
        for i, n1 in enumerate(nucleon_list):
            for j, n2 in enumerate(nucleon_list):
                if i == j:  # Skip self
                    continue
                if j < i:  # Skip already checked pairs
                    continue

                # Vector from n1 to n2
                vec = n2.t - n1.t
                cc = np.linalg.norm(vec)

                # Determine bond type from center distance
                bond_type = None
                if abs(cc - D_SS) < tolerance:
                    bond_type = "S-S"
                    face_pairs = [
                        ("S+X", "S-X"), ("S-X", "S+X"),
                        ("S+Y", "S-Y"), ("S-Y", "S+Y"),
                        ("S+Z", "S-Z"), ("S-Z", "S+Z")
                    ]
                elif abs(cc - D_HH) < tolerance:
                    bond_type = "H-H"
                    face_pairs = [
                        ("H+++", "H---"), ("H---", "H+++"),
                        ("H++-", "H--+"), ("H--+", "H++-"),
                        ("H+-+", "H-+-"), ("H-+-", "H+-+"),
                        ("H-++", "H+--"), ("H+--", "H-++")
                    ]

                if bond_type:
                    # Check which face pair is aligned with the connection vector
                    vec_norm = vec / cc

                    for face1, face2 in face_pairs:
                        # Get face normals (assuming identity rotation for now)
                        normal1 = np.array(FACE_NORMALS[face1])
                        normal2 = np.array(FACE_NORMALS[face2])

                        # Check if face1 of n1 points toward n2
                        if np.dot(normal1, vec_norm) > 0.95:
                            # Check if face2 of n2 points back toward n1
                            if np.dot(normal2, -vec_norm) > 0.95:
                                # This is a valid bond
                                if (n1.id, face1, n2.id, face2) not in existing:
                                    if debug:
                                        print(f"      FOUND: {n1.id}:{face1} -- {n2.id}:{face2} [{bond_type}]")
                                    
                                    # Add the bond
                                    self.bonds.append(Bond(n1.id, face1, n2.id, face2))
                                    existing.add((n1.id, face1, n2.id, face2))
                                    existing.add((n2.id, face2, n1.id, face1))
                                    
                                    # Add ports if they don't exist
                                    if face1 not in n1.ports:
                                        # Determine phase based on face pattern
                                        phase1 = "A" if face1.count('+') % 2 == 0 else "B"
                                        n1.ports[face1] = Port(face1, phase1)
                                        if debug:
                                            print(f"        Added port {face1} (phase {phase1}) to {n1.id}")
                                    
                                    if face2 not in n2.ports:
                                        # Opposite phase for bonding
                                        phase2 = "B" if face2.count('+') % 2 == 0 else "A"
                                        n2.ports[face2] = Port(face2, phase2)
                                        if debug:
                                            print(f"        Added port {face2} (phase {phase2}) to {n2.id}")

        if debug:
            added = len(self.bonds) - original_count
            if added > 0:
                print(f"    Added {added} bonds")
                print(f"    Final: {len(self.bonds)} total bonds")

    @classmethod
    def from_constraints(cls, name: str, constraints: list):
        """Build assembly from minimal constraints with angle/phase control."""
        
        nucleons = {}
        bonds = []
        
        for constraint in constraints:
            id1, face1, id2, face2, angle = constraint
            
            # Infer nucleon types from ID prefix
            kind1 = "proton" if id1[0] == 'P' else "neutron"
            kind2 = "proton" if id2[0] == 'P' else "neutron"
            
            # Create first nucleon at origin if new
            if id1 not in nucleons:
                nucleons[id1] = NucleonPose(
                    id=id1, kind=kind1,
                    R=I(), t=np.array([0.0, 0.0, 0.0]),
                    ports={}
                )
            
            # Add port to first nucleon
            if face1 not in nucleons[id1].ports:
                phase = "A"  # Default, will be refined
                nucleons[id1].ports[face1] = Port(face1, phase)
            
            # Position second nucleon if new
            if id2 not in nucleons:
                n1 = nucleons[id1]
                normal1 = np.array(FACE_NORMALS[face1])
                normal2 = np.array(FACE_NORMALS[face2])
                
                # Determine bond distance
                if face1[0] == 'S' and face2[0] == 'S':
                    dist = D_SS
                elif face1[0] == 'H' and face2[0] == 'H':
                    dist = D_HH
                else:
                    raise ValueError(f"Mixed bond type not supported: {face1}-{face2}")
                
                # Base position along the normal
                base_position = n1.t + dist * (n1.R @ normal1)
                
                # Calculate rotation to align face2 back toward n1
                # The face2 normal needs to point back toward n1 (opposite of normal1)
                target_dir = -normal1  # Face2 should point back
                
                # Find rotation that aligns normal2 with target_dir
                # This is a rotation about the axis perpendicular to both
                axis = np.cross(normal2, target_dir)
                if np.linalg.norm(axis) > 1e-10:
                    axis = axis / np.linalg.norm(axis)
                    cos_angle = np.dot(normal2, target_dir)
                    angle_rad = np.arccos(np.clip(cos_angle, -1, 1))
                    
                    # Rodrigues rotation formula
                    K = np.array([[0, -axis[2], axis[1]],
                                 [axis[2], 0, -axis[0]],
                                 [-axis[1], axis[0], 0]])
                    R2 = I() + np.sin(angle_rad) * K + (1 - np.cos(angle_rad)) * K @ K
                else:
                    # Already aligned or opposite
                    R2 = I() if np.dot(normal2, target_dir) > 0 else -I()
                
                # Apply phase rotation for hex faces
                if face1[0] == 'H' and face2[0] == 'H':
                    if angle == 'A':
                        # Phase A: align with square edges
                        # No additional rotation needed for now
                        pass
                    elif angle == 'B':
                        # Phase B: rotate 60 degrees about bond axis
                        bond_axis = normal1
                        rotation_angle = 2* np.pi / 3  # 60 degrees
                        
                        K = np.array([[0, -bond_axis[2], bond_axis[1]],
                                     [bond_axis[2], 0, -bond_axis[0]],
                                     [-bond_axis[1], bond_axis[0], 0]])
                        phase_rotation = I() + np.sin(rotation_angle) * K + (1 - np.cos(rotation_angle)) * K @ K
                        R2 = phase_rotation @ R2
                
                nucleons[id2] = NucleonPose(
                    id=id2, kind=kind2,
                    R=R2, t=base_position,
                    ports={}
                )
            
            # Add port to second nucleon
            if face2 not in nucleons[id2].ports:
                phase = "B" if nucleons[id1].ports[face1].phase == "A" else "A"
                nucleons[id2].ports[face2] = Port(face2, phase)
            
            bonds.append(Bond(id1, face1, id2, face2))
        
        # Create assembly - bond discovery happens in __post_init__
        return cls(name=name, nucleons=nucleons, bonds=bonds)
