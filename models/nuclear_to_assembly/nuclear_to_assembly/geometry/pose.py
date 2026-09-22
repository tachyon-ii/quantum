from dataclasses import dataclass
import numpy as np

@dataclass
class Port:
    face: str       # e.g., "S+X"
    phase: str      # "A" or "B"

@dataclass
class NucleonPose:
    id: str
    kind: str       # "proton" or "neutron"
    R: np.ndarray   # 3x3
    t: np.ndarray   # 3-vector
    ports: dict     # face -> Port (subset of 14)
