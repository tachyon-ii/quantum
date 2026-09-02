import json
import numpy as np
import trimesh
from nuclear_to_assembly.geometry.solids import truncated_octahedron_vertices_faces

# Per-nucleon face colors
RGBA_PROTON  = np.array([0.86, 0.18, 0.26, 1.0])  # red
RGBA_NEUTRON = np.array([0.25, 0.41, 0.88, 1.0])  # blue

def _apply_RT(R, t, pts):
    pts = np.asanyarray(pts, dtype=float)
    return pts @ np.asarray(R, float).T + np.asarray(t, float)

def _fan_tris(indices):
    if len(indices) < 3:
        return []
    i0 = indices[0]
    return [(i0, indices[k], indices[k + 1]) for k in range(1, len(indices) - 1)]

def _mesh_for_nucleon(nucleon_dict, face_rgba):
    """
    Build Trimesh for one truncated-octahedron nucleon with uniform face color.
    """
    V, faces = truncated_octahedron_vertices_faces()
    R = np.array(nucleon_dict["R"], dtype=float)
    t = np.array(nucleon_dict["t"], dtype=float)

    W = _apply_RT(R, t, V)

    tri_faces = []
    tri_colors = []

    for _, idxs in faces.items():
        tris = _fan_tris(idxs)
        if not tris:
            continue
        tri_faces.extend(tris)
        tri_colors.extend([face_rgba] * len(tris))

    tri_faces = np.asarray(tri_faces, dtype=np.int64)
    tri_colors = (np.asarray(tri_colors, dtype=float) * 255).astype(np.uint8)

    mesh = trimesh.Trimesh(vertices=W, faces=tri_faces, process=False)
    mesh.visual.face_colors = tri_colors
    return mesh

def show_assembly_trimesh(path: str, bg_color=(0, 0, 0, 0)):
    """
    Interactive 3D viewer (trimesh). Renders nucleon solids only:
      - proton faces tinted red, neutron faces tinted blue
      - no axes, no grids, no bonds/markers
    """
    with open(path) as f:
        data = json.load(f)

    scene = trimesh.Scene()

    for n in data["nucleons"]:
        color = RGBA_PROTON if n["kind"] == "proton" else RGBA_NEUTRON
        mesh = _mesh_for_nucleon(n, face_rgba=color)
        scene.add_geometry(mesh, node_name=n["id"])

    scene.background = np.array(bg_color, dtype=float)
    scene.show()

