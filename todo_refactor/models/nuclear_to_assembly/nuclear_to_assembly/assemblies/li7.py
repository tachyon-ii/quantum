import numpy as np
from nuclear_to_assembly.geometry.transforms import I
from nuclear_to_assembly.geometry.pose import NucleonPose, Port
from nuclear_to_assembly.assemblies.builder import Assembly, Bond
from nuclear_to_assembly.geometry.constants import D_SS, D_HH
import math

def build_li7_linear(name: str = "Li7_linear") -> Assembly:
    """
    Li-7 (3 protons, 4 neutrons) in linear arrangement.
    Pattern: P-N-P-N-P-N-N 
    All S-S bonds along X-axis for maximum stability.
    """
    R = I()
    
    # Linear arrangement along X-axis
    nucleons = {}
    positions = []
    
    # Calculate positions for 7 nucleons in line
    for i in range(7):
        x_pos = i * D_SS
        positions.append(np.array([x_pos, 0.0, 0.0], dtype=float))
    
    # Nucleon sequence: P-N-P-N-P-N-N (alternating P-N for first 5, then N-N)
    sequence = ["proton", "neutron", "proton", "neutron", "proton", "neutron", "neutron"]
    ids = ["P1", "N1", "P2", "N2", "P3", "N3", "N4"]
    
    # Create nucleons with appropriate ports and proper phase alternation
    # We'll set phases to ensure each bond connects A↔B
    for i, (nuc_id, kind, pos) in enumerate(zip(ids, sequence, positions)):
        ports = {}
        
        if i == 0:  # First nucleon - only sends
            ports["S+X"] = Port("S+X", "A")
        elif i == 6:  # Last nucleon - only receives  
            ports["S-X"] = Port("S-X", "B")  # Receives from N3 who sends with "A"
        else:  # Middle nucleons
            # Each bond should be A↔B
            # Bond pattern: A↔B, A↔B, A↔B, A↔B, A↔B, A↔B
            # This means every sending port is "A" and every receiving port is "B"
            ports["S-X"] = Port("S-X", "B")  # Always receive with B
            ports["S+X"] = Port("S+X", "A")  # Always send with A
        
        # Actually create and add the nucleon to the dictionary
        nucleons[nuc_id] = NucleonPose(
            id=nuc_id, kind=kind, R=R, t=pos, ports=ports
        )    # Create bonds between adjacent nucleons
    bonds = []
    for i in range(6):  # 6 bonds for 7 nucleons
        n1_id = ids[i]
        n2_id = ids[i + 1]
        bonds.append(Bond(n1_id, "S+X", n2_id, "S-X"))
    
    return Assembly(name=name, nucleons=nucleons, bonds=bonds)

def build_li7_compact(name: str = "Li7_compact") -> Assembly:
    """
    Li-7 in a more compact 3D arrangement.
    Central neutron with 6 nucleons around it in octahedral pattern.
    Mixes S-S and H-H bonds for geometric diversity.
    """
    R = I()
    
    # Central neutron at origin
    center = np.array([0.0, 0.0, 0.0], dtype=float)
    
    # Six surrounding positions at S-S distance
    positions = {
        "N_center": center,
        "P1": np.array([D_SS, 0.0, 0.0], dtype=float),     # +X
        "P2": np.array([-D_SS, 0.0, 0.0], dtype=float),    # -X
        "P3": np.array([0.0, D_SS, 0.0], dtype=float),     # +Y
        "N1": np.array([0.0, -D_SS, 0.0], dtype=float),    # -Y
        "N2": np.array([0.0, 0.0, D_SS], dtype=float),     # +Z
        "N3": np.array([0.0, 0.0, -D_SS], dtype=float),    # -Z
    }
    
    # Create nucleons
    nucleons = {}
    
    # Central neutron with 6 ports
    nucleons["N_center"] = NucleonPose(
        id="N_center", kind="neutron", R=R, t=positions["N_center"],
        ports={
            "S+X": Port("S+X", "A"),
            "S-X": Port("S-X", "A"), 
            "S+Y": Port("S+Y", "A"),
            "S-Y": Port("S-Y", "A"),
            "S+Z": Port("S+Z", "A"),
            "S-Z": Port("S-Z", "A")
        }
    )
    
    # Surrounding nucleons
    port_configs = {
        "P1": {"S-X": Port("S-X", "B")},
        "P2": {"S+X": Port("S+X", "B")},
        "P3": {"S-Y": Port("S-Y", "B")},
        "N1": {"S+Y": Port("S+Y", "B")},
        "N2": {"S-Z": Port("S-Z", "B")},
        "N3": {"S+Z": Port("S+Z", "B")}
    }
    
    kinds = {
        "P1": "proton", "P2": "proton", "P3": "proton",
        "N1": "neutron", "N2": "neutron", "N3": "neutron"
    }
    
    for nuc_id in ["P1", "P2", "P3", "N1", "N2", "N3"]:
        nucleons[nuc_id] = NucleonPose(
            id=nuc_id, kind=kinds[nuc_id], R=R, t=positions[nuc_id],
            ports=port_configs[nuc_id]
        )
    
    # Bonds from center to all surrounding nucleons
    bonds = [
        Bond("N_center", "S+X", "P1", "S-X"),
        Bond("N_center", "S-X", "P2", "S+X"), 
        Bond("N_center", "S+Y", "P3", "S-Y"),
        Bond("N_center", "S-Y", "N1", "S+Y"),
        Bond("N_center", "S+Z", "N2", "S-Z"),
        Bond("N_center", "S-Z", "N3", "S+Z")
    ]
    
    return Assembly(name=name, nucleons=nucleons, bonds=bonds)

def build_li7_ring(name: str = "Li7_ring") -> Assembly:
    """
    Li-7 in ring formation with central nucleon.
    """
    R = I()
    
    # Central neutron at origin
    center = np.array([0.0, 0.0, 0.0], dtype=float)
    
    # Ring positions (hexagon in XY plane)
    ring_radius = D_SS
    angles = [i * 2 * math.pi / 6 for i in range(6)]
    
    positions = {"N_center": center}
    ring_ids = ["P1", "N1", "P2", "N2", "P3", "N3"]
    ring_kinds = ["proton", "neutron", "proton", "neutron", "proton", "neutron"]
    
    for i, (nuc_id, angle) in enumerate(zip(ring_ids, angles)):
        x = ring_radius * math.cos(angle)
        y = ring_radius * math.sin(angle)
        positions[nuc_id] = np.array([x, y, 0.0], dtype=float)
    
    # Create nucleons
    nucleons = {}
    
    # Central neutron needs ALL possible ports since bond discovery will find connections
    center_ports = {
        "S+X": Port("S+X", "A"),
        "S-X": Port("S-X", "A"),
        "S+Y": Port("S+Y", "A"),
        "S-Y": Port("S-Y", "A"),
        "S+Z": Port("S+Z", "A"),
        "S-Z": Port("S-Z", "A")
    }
    
    nucleons["N_center"] = NucleonPose(
        id="N_center", kind="neutron", R=R, t=center,
        ports=center_ports
    )
    
    # Ring nucleons with consistent phase alternation
    for i, (nuc_id, kind) in enumerate(zip(ring_ids, ring_kinds)):
        phase = "B"  # All ring nucleons get phase B to connect with center's phase A
        
        ports = {
            "S+X": Port("S+X", phase),
            "S-X": Port("S-X", phase),
            "S+Y": Port("S+Y", phase),
            "S-Y": Port("S-Y", phase)
        }
        
        nucleons[nuc_id] = NucleonPose(
            id=nuc_id, kind=kind, R=R, t=positions[nuc_id],
            ports=ports
        )
    
    bonds = []
    return Assembly(name=name, nucleons=nucleons, bonds=bonds)