import numpy as np
from nuclear_to_assembly.geometry.transforms import I
from nuclear_to_assembly.geometry.pose import NucleonPose, Port
from nuclear_to_assembly.assemblies.builder import Assembly, Bond
from nuclear_to_assembly.geometry.constants import D_SS, D_HH
import math

class ManualAssembly(Assembly):
    """Assembly that doesn't auto-discover bonds - uses only manually specified bonds."""
    def __post_init__(self):
        pass  # Skip the auto-completion

def build_c12_tetrahedral(name: str = "C12_tetrahedral") -> Assembly:
    """
    C-12 (6 protons, 6 neutrons) in tetrahedral arrangement.
    This tests James's prediction that C-12 should exhibit tetrahedral geometry.
    
    Structure:
    - 4 vertex clusters, each containing 3 nucleons
    - Tetrahedral symmetry with edge length scaled by D_SS
    - Mix of S-S and H-H bonds to maintain geometric constraints
    """
    R = I()
    
    # Tetrahedral vertices (scaled to D_SS distances)
    scale = D_SS / math.sqrt(8/3)  # Scale to get proper inter-cluster distances
    
    vertices = [
        np.array([1, 1, 1], dtype=float) * scale,      # Vertex 1 (+++)
        np.array([1, -1, -1], dtype=float) * scale,    # Vertex 2 (+−−)
        np.array([-1, 1, -1], dtype=float) * scale,    # Vertex 3 (−+−)
        np.array([-1, -1, 1], dtype=float) * scale     # Vertex 4 (−−+)
    ]
    
    nucleons = {}
    bonds = []
    
    # Each vertex gets a cluster of 3 nucleons (mixed P/N)
    cluster_configs = [
        # Cluster 1: 2P, 1N
        {"types": ["proton", "proton", "neutron"], "ids": ["P1", "P2", "N1"]},
        # Cluster 2: 2N, 1P  
        {"types": ["neutron", "neutron", "proton"], "ids": ["N2", "N3", "P3"]},
        # Cluster 3: 2P, 1N
        {"types": ["proton", "proton", "neutron"], "ids": ["P4", "P5", "N4"]},
        # Cluster 4: 2N, 1P
        {"types": ["neutron", "neutron", "proton"], "ids": ["N5", "N6", "P6"]}
    ]
    
    # Build clusters at each tetrahedral vertex
    for cluster_idx, (vertex, config) in enumerate(zip(vertices, cluster_configs)):
        # Small offsets within cluster (triangular arrangement)
        offset_distance = D_SS * 0.3  # Smaller than inter-cluster distance
        
        cluster_offsets = [
            np.array([0, 0, 0], dtype=float),  # Center of cluster
            np.array([offset_distance, 0, 0], dtype=float),  # +X offset
            np.array([-offset_distance/2, offset_distance*math.sqrt(3)/2, 0], dtype=float)  # Triangular
        ]
        
        # Consistent phase assignment for each cluster
        cluster_base_phase = "A" if cluster_idx % 2 == 0 else "B"
        
        for nuc_idx, (nuc_type, nuc_id, offset) in enumerate(zip(
            config["types"], config["ids"], cluster_offsets
        )):
            position = vertex + offset
            
            # Phase alternation within cluster
            phase = cluster_base_phase if nuc_idx == 0 else ("B" if cluster_base_phase == "A" else "A")
            
            ports = {}
            
            # Central nucleon in cluster gets more connectivity
            if nuc_idx == 0:
                # Connect to other clusters via H-H bonds
                h_face = "H+++" if cluster_idx % 2 == 0 else "H---"
                ports[h_face] = Port(h_face, phase)
                
                # Connect within cluster via S-S bonds
                ports["S+X"] = Port("S+X", phase)
                ports["S+Y"] = Port("S+Y", phase)
            else:
                # Peripheral nucleons connect within cluster
                # Ensure opposite phase from center nucleon
                if nuc_idx == 1:  # Receives S+X from center nucleon
                    ports["S-X"] = Port("S-X", phase)
                else:  # nuc_idx == 2, receives S+Y from center nucleon
                    ports["S-Y"] = Port("S-Y", phase)
            
            nucleons[nuc_id] = NucleonPose(
                id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
            )
    
    # Intra-cluster bonds
    cluster_bonds = [
        # Cluster 1
        ("P1", "S+X", "P2", "S-X"),
        ("P1", "S+Y", "N1", "S-Y"),
        # Cluster 2  
        ("N2", "S+X", "N3", "S-X"),
        ("N2", "S+Y", "P3", "S-Y"),
        # Cluster 3
        ("P4", "S+X", "P5", "S-X"), 
        ("P4", "S+Y", "N4", "S-Y"),
        # Cluster 4
        ("N5", "S+X", "N6", "S-X"),
        ("N5", "S+Y", "P6", "S-Y")
    ]
    
    for bond_spec in cluster_bonds:
        bonds.append(Bond(*bond_spec))
    
    # Inter-cluster bonds (tetrahedral edges via H-H connections)
    # Connect cluster centers along tetrahedral edges
    inter_cluster_bonds = [
        ("P1", "H+++", "N2", "H---"),  # Cluster 1-2
        ("P4", "H+++", "N5", "H---"),  # Cluster 3-4
    ]
    
    for bond_spec in inter_cluster_bonds:
        bonds.append(Bond(*bond_spec))
    
    return ManualAssembly(name=name, nucleons=nucleons, bonds=bonds)

def build_c12_layered(name: str = "C12_layered") -> Assembly:
    """
    Alternative C-12 structure: layered approach.
    3 layers of 4 nucleons each, stacked along Z-axis.
    """
    R = I()
    nucleons = {}
    bonds = []
    
    layer_z = [0.0, D_SS, 2*D_SS]
    layer_configs = [
        {"types": ["proton", "neutron", "proton", "neutron"], 
         "ids": ["P1", "N1", "P2", "N2"]},
        {"types": ["neutron", "proton", "neutron", "proton"], 
         "ids": ["N3", "P3", "N4", "P4"]},
        {"types": ["proton", "neutron", "proton", "neutron"], 
         "ids": ["P5", "N5", "P6", "N6"]}
    ]
    
    # Build layers
    for layer_idx, (z_pos, config) in enumerate(zip(layer_z, layer_configs)):
        square_positions = [
            np.array([D_SS/2, D_SS/2, z_pos], dtype=float),
            np.array([-D_SS/2, D_SS/2, z_pos], dtype=float),
            np.array([-D_SS/2, -D_SS/2, z_pos], dtype=float),
            np.array([D_SS/2, -D_SS/2, z_pos], dtype=float)
        ]
        
        for nuc_idx, (nuc_type, nuc_id, position) in enumerate(zip(
            config["types"], config["ids"], square_positions
        )):
            # Follow Li-7 pattern: sending ports = A, receiving ports = B
            ports = {
                "S+X": Port("S+X", "A"),  # Sending
                "S-X": Port("S-X", "B"),  # Receiving
                "S+Y": Port("S+Y", "A"),  # Sending
                "S-Y": Port("S-Y", "B"),  # Receiving
            }
            
            # Vertical connections
            if layer_idx < 2:
                ports["S+Z"] = Port("S+Z", "A")  # Sending up
            if layer_idx > 0:
                ports["S-Z"] = Port("S-Z", "B")  # Receiving from below
            
            nucleons[nuc_id] = NucleonPose(
                id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
            )
    
    # Intra-layer bonds (square rings)
    layer_bond_specs = [
        [("P1", "S+X", "N1", "S-X"), ("N1", "S+Y", "P2", "S-Y"),
         ("P2", "S+X", "N2", "S-X"), ("N2", "S+Y", "P1", "S-Y")],
        [("N3", "S+X", "P3", "S-X"), ("P3", "S+Y", "N4", "S-Y"),
         ("N4", "S+X", "P4", "S-X"), ("P4", "S+Y", "N3", "S-Y")],
        [("P5", "S+X", "N5", "S-X"), ("N5", "S+Y", "P6", "S-Y"),
         ("P6", "S+X", "N6", "S-X"), ("N6", "S+Y", "P5", "S-Y")]
    ]
    
    for layer_bonds in layer_bond_specs:
        for bond_spec in layer_bonds:
            bonds.append(Bond(*bond_spec))
    
    # Inter-layer bonds (vertical connections)
    vertical_bonds = [
        ("P1", "S+Z", "N3", "S-Z"), ("N1", "S+Z", "P3", "S-Z"),
        ("P2", "S+Z", "N4", "S-Z"), ("N2", "S+Z", "P4", "S-Z"),
        ("N3", "S+Z", "P5", "S-Z"), ("P3", "S+Z", "N5", "S-Z"),
        ("N4", "S+Z", "P6", "S-Z"), ("P4", "S+Z", "N6", "S-Z")
    ]
    
    for bond_spec in vertical_bonds:
        bonds.append(Bond(*bond_spec))
    
    return ManualAssembly(name=name, nucleons=nucleons, bonds=bonds)

def build_c12_alpha_cluster(name: str = "C12_alpha") -> Assembly:
    """
    C-12 as 3 alpha particles (He-4 clusters).
    This reflects the known nuclear physics model where C-12 can be 
    viewed as three alpha particles in a triangular arrangement.
    """
    R = I()
    
    # Positions for 3 alpha clusters in triangular arrangement
    cluster_distance = D_SS * 1.5  # Distance between cluster centers
    angles = [0, 2*math.pi/3, 4*math.pi/3]  # 120° apart
    
    cluster_centers = []
    for angle in angles:
        x = cluster_distance * math.cos(angle)
        y = cluster_distance * math.sin(angle) 
        cluster_centers.append(np.array([x, y, 0.0], dtype=float))
    
    nucleons = {}
    bonds = []
    
    # Each alpha cluster: 2P + 2N in He-4 ring formation
    for cluster_idx, center in enumerate(cluster_centers):
        # Small square formation for each alpha particle
        alpha_offset = D_SS * 0.4  # Smaller than inter-cluster distance
        
        alpha_positions = [
            center + np.array([alpha_offset, alpha_offset, 0], dtype=float),    # P
            center + np.array([-alpha_offset, alpha_offset, 0], dtype=float),   # N
            center + np.array([-alpha_offset, -alpha_offset, 0], dtype=float),  # P  
            center + np.array([alpha_offset, -alpha_offset, 0], dtype=float)    # N
        ]
        
        # IDs for this cluster
        base_idx = cluster_idx * 4
        nuc_ids = [f"P{base_idx+1}", f"N{base_idx+1}", f"P{base_idx+2}", f"N{base_idx+2}"]
        nuc_types = ["proton", "neutron", "proton", "neutron"]
        
        # Create nucleons for this alpha cluster
        for nuc_idx, (nuc_id, nuc_type, position) in enumerate(zip(
            nuc_ids, nuc_types, alpha_positions
        )):
            # Assign phases to ensure A↔B alternation within each cluster
            phase = "A" if nuc_idx % 2 == 0 else "B"
            
            ports = {}
            
            # Intra-cluster ring bonds - square ring formation
            if nuc_idx == 0:    # First nucleon (proton) - phase A
                ports["S+Y"] = Port("S+Y", "A")
                ports["S-X"] = Port("S-X", "A")
            elif nuc_idx == 1:  # Second nucleon (neutron) - phase B
                ports["S-Y"] = Port("S-Y", "B")  # Connects to previous A
                ports["S+X"] = Port("S+X", "B")
            elif nuc_idx == 2:  # Third nucleon (proton) - phase A
                ports["S-X"] = Port("S-X", "A")  # Connects to previous B
                ports["S+Y"] = Port("S+Y", "A")
            else:               # Fourth nucleon (neutron) - phase B
                ports["S-Y"] = Port("S-Y", "B")  # Connects to previous A
                ports["S+X"] = Port("S+X", "B")  # Will connect to first A
            
            # Inter-cluster connectivity via H-H bonds
            if nuc_idx == 0:  # First nucleon in each cluster connects to other clusters
                h_faces = ["H+++", "H++-", "H+-+"]
                ports[h_faces[cluster_idx]] = Port(h_faces[cluster_idx], "A")
            elif nuc_idx == 1:  # Second nucleon provides return path
                h_faces_return = ["H---", "H--+", "H-+-"]
                ports[h_faces_return[cluster_idx]] = Port(h_faces_return[cluster_idx], "B")
            
            nucleons[nuc_id] = NucleonPose(
                id=nuc_id, kind=nuc_type, R=R, t=position, ports=ports
            )
        
        # Intra-cluster bonds (alpha particle ring) - FIXED ring closure
        alpha_bonds = [
            (nuc_ids[0], "S+Y", nuc_ids[1], "S-Y"),    # P -> N
            (nuc_ids[1], "S+X", nuc_ids[2], "S-X"),    # N -> P  
            (nuc_ids[2], "S+Y", nuc_ids[3], "S-Y"),    # P -> N
            (nuc_ids[3], "S+X", nuc_ids[0], "S-X")     # N -> P (FIXED: proper ring closure)
        ]
        
        for bond_spec in alpha_bonds:
            bonds.append(Bond(*bond_spec))
    
    # Inter-cluster bonds (connect alpha particles)
    inter_alpha_bonds = [
        ("P1", "H+++", "N5", "H---"),   # Alpha 1 - Alpha 2
        ("P5", "H++-", "N9", "H--+"),   # Alpha 2 - Alpha 3  
        ("P9", "H+-+", "N1", "H-+-")    # Alpha 3 - Alpha 1
    ]
    
    for bond_spec in inter_alpha_bonds:
        bonds.append(Bond(*bond_spec))
    
    return ManualAssembly(name=name, nucleons=nucleons, bonds=bonds)