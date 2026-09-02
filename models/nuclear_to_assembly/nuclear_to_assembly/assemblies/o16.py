import numpy as np
from nuclear_to_assembly.geometry.transforms import I
from nuclear_to_assembly.geometry.pose import NucleonPose, Port
from nuclear_to_assembly.assemblies.builder import Assembly, Bond
from nuclear_to_assembly.geometry.constants import D_SS, D_HH
import math

class ManualAssembly(Assembly):
    """Assembly that doesn't auto-discover bonds - uses only manually specified bonds."""
    def __post_init__(self):
        pass

def build_o16_double_cube(name: str = "O16_double_cube") -> Assembly:
    """
    O-16 as two stacked cubes (2×2×4 arrangement).
    Bottom cube: 4 layers of 2 nucleons each
    Top cube: 4 layers of 2 nucleons each
    Maximizes layered connectivity that scored well for C-12.
    """
    R = I()
    nucleons = {}
    bonds = []
    
    # 8 layers of 2 nucleons each, stacked along Z
    layer_z = [i * D_SS for i in range(8)]
    
    # Alternating P/N pattern optimized for NP bonding
    layer_configs = [
        # Bottom cube layers 0-3
        {"types": ["proton", "neutron"], "ids": ["P1", "N1"]},      # Layer 0
        {"types": ["neutron", "proton"], "ids": ["N2", "P2"]},      # Layer 1  
        {"types": ["proton", "neutron"], "ids": ["P3", "N3"]},      # Layer 2
        {"types": ["neutron", "proton"], "ids": ["N4", "P4"]},      # Layer 3
        # Top cube layers 4-7
        {"types": ["proton", "neutron"], "ids": ["P5", "N5"]},      # Layer 4
        {"types": ["neutron", "proton"], "ids": ["N6", "P6"]},      # Layer 5
        {"types": ["proton", "neutron"], "ids": ["P7", "N7"]},      # Layer 6  
        {"types": ["neutron", "proton"], "ids": ["N8", "P8"]},      # Layer 7
    ]
    
    # Build layers
    for layer_idx, (z_pos, config) in enumerate(zip(layer_z, layer_configs)):
        # Two positions per layer (simple pair arrangement)
        pair_positions = [
            np.array([-D_SS/3, 0.0, z_pos], dtype=float),    # Left position
            np.array([D_SS/3, 0.0, z_pos], dtype=float)      # Right position
        ]
        
        for nuc_idx, (nuc_type, nuc_id, position) in enumerate(zip(
            config["types"], config["ids"], pair_positions
        )):
            # Use Li-7 proven pattern: sending=A, receiving=B
            ports = {
                "S+X": Port("S+X", "A"),  # Sending horizontally
                "S-X": Port("S-X", "B"),  # Receiving horizontally
                "S+Y": Port("S+Y", "A"),  # Sending laterally  
                "S-Y": Port("S-Y", "B"),  # Receiving laterally
            }
            
            # Vertical connections
            if layer_idx < 7:  # Not top layer
                ports["S+Z"] = Port("S+Z", "A")  # Sending up
            if layer_idx > 0:  # Not bottom layer
                ports["S-Z"] = Port("S-Z", "B")  # Receiving from below
                
            nucleons[nuc_id] = NucleonPose(
                id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
            )
    
    # Horizontal bonds within each layer (pair connectivity)
    horizontal_bonds = []
    for layer_idx, config in enumerate(layer_configs):
        ids = config["ids"]
        # Connect the two nucleons in each layer
        horizontal_bonds.append((ids[0], "S+X", ids[1], "S-X"))
    
    for bond_spec in horizontal_bonds:
        bonds.append(Bond(*bond_spec))
    
    # Vertical bonds between adjacent layers  
    vertical_bonds = []
    for layer_idx in range(7):  # 7 connections for 8 layers
        curr_layer = layer_configs[layer_idx]["ids"]
        next_layer = layer_configs[layer_idx + 1]["ids"]
        
        # Connect corresponding positions vertically
        vertical_bonds.extend([
            (curr_layer[0], "S+Z", next_layer[0], "S-Z"),  # Left to left
            (curr_layer[1], "S+Z", next_layer[1], "S-Z")   # Right to right  
        ])
    
    for bond_spec in vertical_bonds:
        bonds.append(Bond(*bond_spec))
    
    return ManualAssembly(name=name, nucleons=nucleons, bonds=bonds)

def build_o16_spherical(name: str = "O16_spherical") -> Assembly:
    """
    O-16 in spherical arrangement with central core.
    Inner shell: 4 nucleons around center
    Outer shell: 12 nucleons in icosahedral-like pattern
    Tests whether spherical geometry suits larger nuclei.
    """
    R = I()
    nucleons = {}
    bonds = []
    
    # Central core - single nucleon
    center_pos = np.array([0.0, 0.0, 0.0], dtype=float)
    
    # Inner shell - 4 nucleons in tetrahedral arrangement
    inner_radius = D_SS
    inner_positions = [
        np.array([inner_radius, inner_radius, inner_radius], dtype=float),    # +++
        np.array([inner_radius, -inner_radius, -inner_radius], dtype=float),  # +--
        np.array([-inner_radius, inner_radius, -inner_radius], dtype=float),  # -+-
        np.array([-inner_radius, -inner_radius, inner_radius], dtype=float)   # --+
    ]
    
    # Outer shell - 12 nucleons approximating icosahedral vertices
    outer_radius = D_SS * 1.8
    phi = (1 + math.sqrt(5)) / 2  # Golden ratio for icosahedral geometry
    
    # Icosahedral vertex coordinates (normalized then scaled)
    ico_coords = [
        (1, phi, 0), (-1, phi, 0), (1, -phi, 0), (-1, -phi, 0),
        (phi, 0, 1), (phi, 0, -1), (-phi, 0, 1), (-phi, 0, -1),
        (0, 1, phi), (0, -1, phi), (0, 1, -phi), (0, -1, -phi)
    ]
    
    outer_positions = []
    for coord in ico_coords:
        # Normalize and scale to outer radius
        norm = math.sqrt(sum(x*x for x in coord))
        scaled = [x * outer_radius / norm for x in coord]
        outer_positions.append(np.array(scaled, dtype=float))
    
    # Assign nucleon types for balanced P/N distribution
    all_positions = [center_pos] + inner_positions + outer_positions
    all_types = (["neutron"] + ["proton", "neutron", "proton", "neutron"] +
                ["proton", "neutron"] * 6)  # Alternating P/N for outer shell
    
    # Simple sequential numbering
    all_ids = ["N_center"]
    p_count = 1
    n_count = 1
    
    for i, nuc_type in enumerate(all_types[1:], 1):  # Skip center nucleon
        if nuc_type == "proton":
            all_ids.append(f"P{p_count}")
            p_count += 1
        else:
            all_ids.append(f"N{n_count}")
            n_count += 1
    
    # Create all nucleons
    for nuc_id, nuc_type, position in zip(all_ids, all_types, all_positions):
        # Universal port assignment for maximum connectivity
        ports = {}
        
        # All square faces
        for face in ["S+X", "S-X", "S+Y", "S-Y", "S+Z", "S-Z"]:
            phase = "A" if face.startswith("S+") else "B"
            ports[face] = Port(face, phase)
        
        # Some hexagonal faces for longer-range connections
        for face in ["H+++", "H---", "H++-", "H--+"]:
            phase = "A" if "+++" in face or "+-" in face else "B"
            ports[face] = Port(face, phase)
            
        nucleons[nuc_id] = NucleonPose(
            id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
        )
    
    # Minimal bond structure - let automatic discovery find optimal connections
    # Just establish some core connectivity
    bonds = [
        Bond("N_center", "S+X", "P1", "S-X"),  # Center to first inner proton
        Bond("N_center", "S-X", "N1", "S+X"),  # Center to first inner neutron
    ]
    
    return ManualAssembly(name=name, nucleons=nucleons, bonds=bonds)

def build_o16_alpha_tetrahedral(name: str = "O16_alpha_tetrahedral") -> Assembly:
    """
    O-16 as 4 alpha particles in perfect tetrahedral arrangement.
    This tests the alpha clustering hypothesis for O-16.
    Each alpha: 2P + 2N in He-4 configuration
    """
    R = I()
    nucleons = {}
    bonds = []
    
    # Tetrahedral vertices for 4 alpha clusters
    cluster_distance = D_SS * 2.0  # Larger separation for alpha clusters
    scale = cluster_distance / math.sqrt(8/3)
    
    alpha_centers = [
        np.array([1, 1, 1], dtype=float) * scale,      # Alpha 1
        np.array([1, -1, -1], dtype=float) * scale,    # Alpha 2
        np.array([-1, 1, -1], dtype=float) * scale,    # Alpha 3
        np.array([-1, -1, 1], dtype=float) * scale     # Alpha 4
    ]
    
    # Build each alpha cluster
    for alpha_idx, center in enumerate(alpha_centers):
        # He-4 ring formation for each alpha
        alpha_offset = D_SS * 0.35
        
        # Square positions within alpha cluster
        alpha_positions = [
            center + np.array([alpha_offset, alpha_offset, 0], dtype=float),    # P
            center + np.array([-alpha_offset, alpha_offset, 0], dtype=float),   # N
            center + np.array([-alpha_offset, -alpha_offset, 0], dtype=float),  # P
            center + np.array([alpha_offset, -alpha_offset, 0], dtype=float)    # N
        ]
        
        # IDs for this alpha cluster
        base_id = alpha_idx * 4
        alpha_ids = [f"P{base_id+1}", f"N{base_id+1}", f"P{base_id+2}", f"N{base_id+2}"]
        alpha_types = ["proton", "neutron", "proton", "neutron"]
        
        # Create nucleons in this alpha cluster
        for nuc_idx, (nuc_id, nuc_type, position) in enumerate(zip(
            alpha_ids, alpha_types, alpha_positions
        )):
            # Phases for perfect ring alternation within alpha
            phase = "A" if nuc_idx % 2 == 0 else "B"
            
            # Comprehensive port assignment
            ports = {}
            
            # Intra-alpha connectivity (square ring)
            square_faces = ["S+X", "S-X", "S+Y", "S-Y"]
            for face in square_faces:
                face_phase = "A" if face.startswith("S+") else "B"
                ports[face] = Port(face, face_phase)
            
            # Inter-alpha connectivity via H-H bonds
            if nuc_idx == 0:  # First nucleon connects to other alphas
                h_faces = ["H+++", "H++-", "H+-+", "H-++"]
                ports[h_faces[alpha_idx]] = Port(h_faces[alpha_idx], "A")
            elif nuc_idx == 1:  # Second nucleon receives from other alphas
                h_faces_receive = ["H---", "H--+", "H-+-", "H+--"]
                ports[h_faces_receive[alpha_idx]] = Port(h_faces_receive[alpha_idx], "B")
                
            nucleons[nuc_id] = NucleonPose(
                id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
            )
        
        # Intra-alpha bonds (He-4 ring)
        alpha_bonds = [
            (alpha_ids[0], "S+Y", alpha_ids[1], "S-Y"),    # P → N
            (alpha_ids[1], "S+X", alpha_ids[2], "S-X"),    # N → P
            (alpha_ids[2], "S+Y", alpha_ids[3], "S-Y"),    # P → N
            (alpha_ids[3], "S+X", alpha_ids[0], "S-X")     # N → P (ring closure)
        ]
        
        for bond_spec in alpha_bonds:
            bonds.append(Bond(*bond_spec))
    
    # Inter-alpha bonds (tetrahedral edges)
    inter_alpha_bonds = [
        ("P1", "H+++", "N5", "H--+"),   # Alpha 1-2 (P1 sends H+++, N5 receives H--+)
        ("P5", "H++-", "N9", "H-+-"),   # Alpha 2-3 (P5 sends H++-, N9 receives H-+-)
        ("P9", "H+-+", "N13", "H+--"),  # Alpha 3-4 (P9 sends H+-+, N13 receives H+--)
        ("P13", "H-++", "N1", "H---")   # Alpha 4-1 (P13 sends H-++, N1 receives H---)
    ]
    
    for bond_spec in inter_alpha_bonds:
        bonds.append(Bond(*bond_spec))
    
    return ManualAssembly(name=name, nucleons=nucleons, bonds=bonds)

def build_o16_layered_cube(name: str = "O16_layered_cube") -> Assembly:
    """
    O-16 in 4-layer cube arrangement (4×2×2).
    Based on the successful C-12 layered approach.
    4 layers of 4 nucleons each in square formation.
    """
    R = I()
    nucleons = {}
    bonds = []
    
    # 4 layers of 4 nucleons each
    layer_z = [0.0, D_SS, 2*D_SS, 3*D_SS]
    
    # Optimized P/N distribution for maximum NP bonding
    layer_configs = [
        # Layer 1: 2P, 2N
        {"types": ["proton", "neutron", "proton", "neutron"], 
         "ids": ["P1", "N1", "P2", "N2"]},
        # Layer 2: 2N, 2P (alternated)
        {"types": ["neutron", "proton", "neutron", "proton"], 
         "ids": ["N3", "P3", "N4", "P4"]},
        # Layer 3: 2P, 2N  
        {"types": ["proton", "neutron", "proton", "neutron"], 
         "ids": ["P5", "N5", "P6", "N6"]},
        # Layer 4: 2N, 2P
        {"types": ["neutron", "proton", "neutron", "proton"], 
         "ids": ["N7", "P7", "N8", "P8"]}
    ]
    
    # Build layers
    for layer_idx, (z_pos, config) in enumerate(zip(layer_z, layer_configs)):
        # Square positions in XY plane  
        square_positions = [
            np.array([D_SS/2, D_SS/2, z_pos], dtype=float),    # +X+Y
            np.array([-D_SS/2, D_SS/2, z_pos], dtype=float),   # -X+Y
            np.array([-D_SS/2, -D_SS/2, z_pos], dtype=float),  # -X-Y
            np.array([D_SS/2, -D_SS/2, z_pos], dtype=float)    # +X-Y
        ]
        
        for nuc_idx, (nuc_type, nuc_id, position) in enumerate(zip(
            config["types"], config["ids"], square_positions
        )):
            # Proven Li-7/C-12 pattern: sending=A, receiving=B
            ports = {
                "S+X": Port("S+X", "A"),  
                "S-X": Port("S-X", "B"),  
                "S+Y": Port("S+Y", "A"),  
                "S-Y": Port("S-Y", "B"),  
            }
            
            # Vertical connections
            if layer_idx < 3:  # Not top layer
                ports["S+Z"] = Port("S+Z", "A")
            if layer_idx > 0:  # Not bottom layer
                ports["S-Z"] = Port("S-Z", "B")
                
            nucleons[nuc_id] = NucleonPose(
                id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
            )
    
    # Intra-layer bonds (square rings) - same pattern as successful C-12
    layer_bond_specs = [
        # Layer 1 square
        [("P1", "S+X", "N1", "S-X"), ("N1", "S+Y", "P2", "S-Y"),
         ("P2", "S+X", "N2", "S-X"), ("N2", "S+Y", "P1", "S-Y")],
        # Layer 2 square
        [("N3", "S+X", "P3", "S-X"), ("P3", "S+Y", "N4", "S-Y"),
         ("N4", "S+X", "P4", "S-X"), ("P4", "S+Y", "N3", "S-Y")],
        # Layer 3 square  
        [("P5", "S+X", "N5", "S-X"), ("N5", "S+Y", "P6", "S-Y"),
         ("P6", "S+X", "N6", "S-X"), ("N6", "S+Y", "P5", "S-Y")],
        # Layer 4 square
        [("N7", "S+X", "P7", "S-X"), ("P7", "S+Y", "N8", "S-Y"),
         ("N8", "S+X", "P8", "S-X"), ("P8", "S+Y", "N7", "S-Y")]
    ]
    
    for layer_bonds in layer_bond_specs:
        for bond_spec in layer_bonds:
            bonds.append(Bond(*bond_spec))
    
    # Inter-layer bonds (vertical connections)
    vertical_bonds = [
        # Layer 1 → Layer 2
        ("P1", "S+Z", "N3", "S-Z"), ("N1", "S+Z", "P3", "S-Z"),
        ("P2", "S+Z", "N4", "S-Z"), ("N2", "S+Z", "P4", "S-Z"),
        # Layer 2 → Layer 3  
        ("N3", "S+Z", "P5", "S-Z"), ("P3", "S+Z", "N5", "S-Z"),
        ("N4", "S+Z", "P6", "S-Z"), ("P4", "S+Z", "N6", "S-Z"),
        # Layer 3 → Layer 4
        ("P5", "S+Z", "N7", "S-Z"), ("N5", "S+Z", "P7", "S-Z"),
        ("P6", "S+Z", "N8", "S-Z"), ("N6", "S+Z", "P8", "S-Z")
    ]
    
    for bond_spec in vertical_bonds:
        bonds.append(Bond(*bond_spec))
    
    return ManualAssembly(name=name, nucleons=nucleons, bonds=bonds)