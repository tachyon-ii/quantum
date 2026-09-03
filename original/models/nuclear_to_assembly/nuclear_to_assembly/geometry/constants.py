import math

# Edge length is 1
EDGE = 1.0

# In-sphere radii (distance from center to face planes) for edge=1 truncated octahedron
R_SQ = math.sqrt(2.0)           # squares:  r_S = √2  ≈ 1.4142135623
R_HEX = math.sqrt(6.0) / 2.0    # hexes:    r_H = √6/2 ≈ 1.2247448714

# Contact separations for face-to-face touching (no overlap, no gap)
D_SS = 2.0 * R_SQ               # S–S separation: 2√2  ≈ 2.8284271247
D_HH = 2.0 * R_HEX              # H–H separation: √6    ≈ 2.449489743

