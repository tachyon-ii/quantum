import math

SQRT3 = math.sqrt(3.0)

# Unit normals for the 14 faces of the truncated octahedron (Kelvin cell)
FACE_NORMALS = {
    # Squares (axis-aligned)
    "S+X": ( 1.0,  0.0,  0.0),
    "S-X": (-1.0,  0.0,  0.0),
    "S+Y": ( 0.0,  1.0,  0.0),
    "S-Y": ( 0.0, -1.0,  0.0),
    "S+Z": ( 0.0,  0.0,  1.0),
    "S-Z": ( 0.0,  0.0, -1.0),

    # Hexes (cube body diagonals, normalized)
    "H+++": ( 1.0/SQRT3,  1.0/SQRT3,  1.0/SQRT3),
    "H++-": ( 1.0/SQRT3,  1.0/SQRT3, -1.0/SQRT3),
    "H+-+": ( 1.0/SQRT3, -1.0/SQRT3,  1.0/SQRT3),
    "H-++": (-1.0/SQRT3,  1.0/SQRT3,  1.0/SQRT3),
    "H+--": ( 1.0/SQRT3, -1.0/SQRT3, -1.0/SQRT3),
    "H-+-": (-1.0/SQRT3,  1.0/SQRT3, -1.0/SQRT3),
    "H--+": (-1.0/SQRT3, -1.0/SQRT3,  1.0/SQRT3),
    "H---": (-1.0/SQRT3, -1.0/SQRT3, -1.0/SQRT3),
}

# Natural groupings for u/d channels and symmetry
SQUARE_BELTS = {
    "X": ("S+X", "S-X"),
    "Y": ("S+Y", "S-Y"),
    "Z": ("S+Z", "S-Z"),
}

HEX_TETRADS = {
    "A": ("H+++", "H+--", "H-+-", "H--+"),  # sign product +1 (even # of negatives)
    "B": ("H++-", "H+-+", "H-++", "H---"),  # sign product -1 (odd  # of negatives)
}

def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
def norm(u):   return math.sqrt(dot(u, u))

def angle_deg_by_faces(faceA: str, faceB: str) -> float:
    """Angle (degrees) between face normals."""
    u, v = FACE_NORMALS[faceA], FACE_NORMALS[faceB]
    c = dot(u, v) / (norm(u) * norm(v))
    c = max(-1.0, min(1.0, c))
    return math.degrees(math.acos(c))

def face_class(face: str) -> str:
    """Return 'S' for square faces, 'H' for hex faces."""
    return "S" if face.startswith("S") else "H"

def is_opposite(faceA: str, faceB: str) -> bool:
    """True if faces are opposite (180° apart)."""
    return abs(angle_deg_by_faces(faceA, faceB) - 180.0) < 1e-6

def is_orthogonal(faceA: str, faceB: str, tol_deg: float = 5.0) -> bool:
    """True if faces are ~90° apart within tolerance."""
    return abs(angle_deg_by_faces(faceA, faceB) - 90.0) <= tol_deg

