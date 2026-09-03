import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from nuclear_to_assembly.geometry.to_geometry import FACE_NORMALS, face_class
from nuclear_to_assembly.geometry.solids import truncated_octahedron_vertices_faces

# Simple color theme
COLOR_SQ = (0.80, 0.85, 0.95, 0.9)   # squares
COLOR_HE = (0.75, 0.75, 0.75, 0.9)   # hexes
EDGE_CLR = (0.2, 0.2, 0.2, 0.8)
PN_COL   = {"proton": "crimson", "neutron": "royalblue"}

def _apply_RT(R, t, pts):
    """Apply rotation R (3x3) and translation t (3,) to Nx3 points."""
    pts = np.asarray(pts, dtype=float)
    R = np.asarray(R, dtype=float); t = np.asarray(t, dtype=float)
    return pts @ R.T + t

def _solid_poly3d(nucleon):
    """
    Build a Poly3DCollection for one nucleon:
    - Returns (collection, centers) where centers maps face label -> centroid (3,)
      (used to draw bond stubs cleanly on the face)
    """
    V, faces = truncated_octahedron_vertices_faces()
    R = np.array(nucleon["R"], dtype=float)
    t = np.array(nucleon["t"], dtype=float)

    # Transform vertices into world coords for this nucleon
    WV = _apply_RT(R, t, V)

    poly_verts = []
    poly_color = []
    face_centers = {}

    for label, idxs in faces.items():
        poly = WV[idxs]               # (n,3)
        poly_verts.append(poly)
        poly_color.append(COLOR_SQ if face_class(label) == "S" else COLOR_HE)
        face_centers[label] = poly.mean(axis=0)

    coll = Poly3DCollection(poly_verts, facecolors=poly_color,
                            edgecolors=EDGE_CLR, linewidths=0.8)
    return coll, face_centers

def plot_assembly_json(path, out_png=None, title=None):
    """
    Render full truncated-octahedron solids for each nucleon + bonds:
    - proton centers in crimson, neutrons in royal blue
    - solids colored by face class (S vs H)
    - bonds drawn as green segments between face-normal tip points
    """
    with open(path) as f:
        data = json.load(f)

    fig = plt.figure(figsize=(7.2, 6.4))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_box_aspect([1, 1, 1])

    # Draw each nucleon
    centers = {}
    face_centers_by_id = {}

    for n in data["nucleons"]:
        # store center for quick bond helpers
        centers[n["id"]] = np.array(n["t"], dtype=float)

        # draw solid
        coll, face_centers = _solid_poly3d(n)
        ax.add_collection3d(coll)
        face_centers_by_id[n["id"]] = face_centers

        # draw center point + label
        ax.scatter(*centers[n["id"]], c=PN_COL.get(n["kind"], "k"), s=30, depthshade=True)
        ax.text(*centers[n["id"]], n["id"], fontsize=8, color="k")

    # Draw bonds as segments between face-centers slightly pushed outward
    for b in data["bonds"]:
        n1, f1 = b["n1"], b["face1"]
        n2, f2 = b["n2"], b["face2"]
        # start at the face centroid and walk a short distance along the face normal
        p1c = face_centers_by_id[n1][f1]
        p2c = face_centers_by_id[n2][f2]
        nrm1 = np.array(FACE_NORMALS[f1]); nrm1 /= np.linalg.norm(nrm1)
        nrm2 = np.array(FACE_NORMALS[f2]); nrm2 /= np.linalg.norm(nrm2)
        p1 = p1c + 0.15 * nrm1
        p2 = p2c + 0.15 * nrm2

        ax.plot([p1[0], p2[0]],
                [p1[1], p2[1]],
                [p1[2], p2[2]],
                color="g", lw=2.0)

    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.view_init(elev=22, azim=35)
    if title:
        ax.set_title(title)
    plt.tight_layout()
    if out_png:
        plt.savefig(out_png, dpi=180)
        print(f"Saved: {out_png}")
    else:
        plt.show()

