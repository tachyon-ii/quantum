NUCLEUS_LIBRARY = {
    "d2": [
        ("N1", "S+X", "P1", "S-X", 0)
    ],
    
    "h3_linear": [
        ("N1", "S+X", "P1", "S-X", 0),
        ("P1", "S+X", "N2", "S-X", 0)
    ],
    
    "h3_orth": [
        ("P1", "S+X", "N1", "S-X", 0),
        ("N1", "S+Y", "P2", "S-Y", 0)
    ],
    
    "he3_linear": [
        ("P1", "S+X", "N1", "S-X", 0),
        ("N1", "S+X", "P2", "S-X", 0)
    ],
    
    "he3_orth": [
        ("P1", "S+X", "N1", "S-X", 0),
        ("N1", "S+Y", "P2", "S-Y", 0)
    ],
    
    "he4_cross": [
        ("N1", "S+X", "P1", "S-X", 0),
        ("N1", "H+++", "P2", "H---", "A"),
        ("P1", "H--+", "N2", "H++-", "A")
    ],
    
    "he4_ring": [
        ("P1", "S+X", "N1", "S-X", 0),
        ("N1", "S+Y", "P2", "S-Y", 0),
        ("P2", "S-X", "N2", "S-X", 0)
    ]
}

def get_nucleus_constraints(name: str):
    """Get constraint definition for a nucleus."""
    if name not in NUCLEUS_LIBRARY:
        raise ValueError(f"Unknown nucleus: {name}. Available: {list(NUCLEUS_LIBRARY.keys())}")
    return NUCLEUS_LIBRARY[name]
