"""Main scoring module that coordinates all scoring functions."""

import json
import numpy as np
from nuclear_to_assembly.assemblies.builder import Assembly, Bond
from nuclear_to_assembly.geometry.pose import NucleonPose, Port
from nuclear_to_assembly.scoring.brickwork import score_brickwork
from nuclear_to_assembly.scoring.channels import count_channels
from nuclear_to_assembly.scoring.phase_rules import score_phase
from nuclear_to_assembly.scoring.comprehensive import extract_all_features

def assembly_from_json(data: dict) -> Assembly:
    """Reconstruct Assembly object from JSON data."""
    nucleons = {}
    for n in data["nucleons"]:
        nucleons[n["id"]] = NucleonPose(
            id=n["id"],
            kind=n["kind"],
            R=np.array(n["R"]),
            t=np.array(n["t"]),
            ports={p["face"]: Port(p["face"], p["phase"]) for p in n["ports"]}
        )
    
    bonds = []
    for b in data["bonds"]:
        bonds.append(Bond(b["n1"], b["face1"], b["n2"], b["face2"]))
    
    return Assembly(name=data["name"], nucleons=nucleons, bonds=bonds)

def score_assembly(assembly: Assembly) -> dict:
    """Run all scoring functions on an assembly."""
    return {
        "channels": count_channels(assembly),
        "brickwork": score_brickwork(assembly),
        "phase": score_phase(assembly),
        "comprehensive": extract_all_features(assembly)
    }

def score_from_json(data: dict) -> dict:
    """Score an assembly from JSON data."""
    assembly = assembly_from_json(data)
    return score_assembly(assembly)
