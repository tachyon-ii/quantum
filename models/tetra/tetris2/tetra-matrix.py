import numpy as np

# Define vertex coordinates (e.g., for a single tetrahedron)
vertices = np.array([
    [0.0, 0.0, 0.0],  # Vertex 0
    [1.0, 0.0, 0.0],  # Vertex 1
    [0.5, np.sqrt(3)/2, 0.0],  # Vertex 2
    [0.5, np.sqrt(3)/6, np.sqrt(2/3)]  # Vertex 3
])

# Define the tetrahedral connectivity (the "tetrahedral matrix")
# This represents a single tetrahedron formed by vertices 0, 1, 2, and 3
tetra_matrix = np.array([
    [0, 1, 2, 3]
])

print("Vertices:\n", vertices)
print("\nTetrahedral Matrix:\n", tetra_matrix)
