# models/binding/membrane/mesh.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import math
import numpy as np
from scipy.spatial import cKDTree
import constants as C

_ICOSPHERE_CACHE = {}

def build_unit_icosphere(subdiv=C.SUBDIV):
    """Builds a unit icosphere with subdiv loop subdivisions (642 verts, 1280 faces at subdiv=3)."""
    if subdiv in _ICOSPHERE_CACHE:
        v, f, edges, edge_faces, v_faces = _ICOSPHERE_CACHE[subdiv]
        return v.copy(), f.copy(), edges.copy(), edge_faces.copy(), v_faces

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    verts = np.array([
        [-1,  phi, 0], [ 1,  phi, 0], [-1, -phi, 0], [ 1, -phi, 0],
        [ 0, -1,  phi], [ 0,  1,  phi], [ 0, -1, -phi], [ 0,  1, -phi],
        [ phi, 0, -1], [ phi, 0,  1], [-phi, 0, -1], [-phi, 0,  1],
    ], dtype=np.float64)
    verts /= np.linalg.norm(verts, axis=1, keepdims=True)

    faces = np.array([
        [0,11,5], [0,5,1], [0,1,7], [0,7,10], [0,10,11],
        [1,5,9], [5,11,4], [11,10,2], [10,7,6], [7,1,8],
        [3,9,4], [3,4,2], [3,2,6], [3,6,8], [3,8,9],
        [4,9,5], [2,4,11], [6,2,10], [8,6,7], [9,8,1],
    ], dtype=np.int32)

    for _ in range(subdiv):
        mid_cache = {}
        v_list = verts.tolist()
        new_faces = []

        def get_mid(i1, i2):
            key = (min(i1, i2), max(i1, i2))
            if key not in mid_cache:
                m = 0.5 * ( np.array(v_list[i1]) + np.array(v_list[i2]) )
                m /= np.linalg.norm(m)
                mid_cache[key] = len(v_list)
                v_list.append(m.tolist())
            return mid_cache[key]

        for tri in faces:
            v0, v1, v2 = int(tri[0]), int(tri[1]), int(tri[2])
            a = get_mid(v0, v1)
            b = get_mid(v1, v2)
            c = get_mid(v2, v0)
            new_faces.extend([[v0, a, c], [v1, b, a], [v2, c, b], [a, b, c]])
        verts = np.array(v_list, dtype=np.float64)
        faces = np.array(new_faces, dtype=np.int32)

    # Ensure outward orientation (normals dot position > 0)
    v0, v1, v2 = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
    fn = np.cross(v1 - v0, v2 - v0)
    fc = (v0 + v1 + v2) / 3.0
    flip = np.sum(fn * fc, axis=1) < 0
    faces[flip, 1], faces[flip, 2] = faces[flip, 2].copy(), faces[flip, 1].copy()

    # Build edge-to-adjacent-faces map for Helfrich bending
    edge_dict = {}
    for fi, (a, b, c) in enumerate(faces):
        for u, w in ((a, b), (b, c), (c, a)):
            k = (min(int(u), int(w)), max(int(u), int(w)))
            edge_dict.setdefault(k, []).append(fi)
    edges = np.array(list(edge_dict.keys()), dtype=np.int32)
    edge_faces = np.array([edge_dict[tuple(e)] for e in edges], dtype=np.int32)

    v_faces = [[] for _ in range(len(verts))]
    for fi, tri in enumerate(faces):
        for vi in tri:
            v_faces[int(vi)].append(fi)

    _ICOSPHERE_CACHE[subdiv] = (verts, faces, edges, edge_faces, v_faces)
    return verts.copy(), faces.copy(), edges.copy(), edge_faces.copy(), v_faces


class CapsidTemplate:
    """Precomputed rest-state properties of a single capsid mesh of radius R_i."""
    def __init__(self, radius, subdiv=C.SUBDIV):
        u_verts, self.faces, self.edges, self.edge_faces, self.v_faces = build_unit_icosphere(subdiv)
        self.radius = float(radius)
        self.rest_verts = u_verts * self.radius
        self.n_verts = len(self.rest_verts)
        self.n_faces = len(self.faces)

        # Rest face areas, total area, and volume from discrete mesh (so relaxed sphere has E = 0 to machine precision)
        v0 = self.rest_verts[self.faces[:, 0]]
        v1 = self.rest_verts[self.faces[:, 1]]
        v2 = self.rest_verts[self.faces[:, 2]]
        cross = np.cross(v1 - v0, v2 - v0)
        self.rest_face_areas = 0.5 * np.linalg.norm(cross, axis=1)
        self.A0 = float(np.sum(self.rest_face_areas))
        self.V0 = float(np.sum(np.sum(v0 * cross, axis=1)) / 6.0)
        self.A0_analytic = 4.0 * math.pi * self.radius**2
        self.V0_analytic = (4.0 / 3.0) * math.pi * self.radius**3

        # Mean edge length for KD-tree 3-edge-length radius (§3.4)
        e_vecs = self.rest_verts[self.edges[:, 0]] - self.rest_verts[self.edges[:, 1]]
        self.mean_edge_len = float(np.mean(np.linalg.norm(e_vecs, axis=1)))


def face_geometry_and_grads(verts, faces):
    """
    Computes face normals, face areas A_f, vertex areas A_v = (1/3) sum_{f ni v} A_f,
    and volume V by divergence theorem, plus exact vertex gradients dV/dx_v and dA_f/dx_v.
    """
    eps = C.UNDECLARED_NUMERIC['EPS_NORM'][0]
    i0, i1, i2 = faces[:, 0], faces[:, 1], faces[:, 2]
    v0, v1, v2 = verts[i0], verts[i1], verts[i2]

    e1 = v1 - v0
    e2 = v2 - v0
    cross = np.cross(e1, e2)
    norm_c = np.sqrt(np.sum(cross**2, axis=1) + eps**2)
    n_hat = cross / norm_c[:, None]
    A_f = 0.5 * norm_c
    f_centroids = (v0 + v1 + v2) / 3.0

    # Vertex areas A_v = (1/3) sum_{f ni v} A_f
    A_v = np.zeros(len(verts), dtype=np.float64)
    np.add.at(A_v, i0, A_f / 3.0)
    np.add.at(A_v, i1, A_f / 3.0)
    np.add.at(A_v, i2, A_f / 3.0)

    # Volume V = (1/6) sum_f v0 . (v1 x v2) and exact gradient dV/dv
    V = float(np.sum(np.sum(v0 * cross, axis=1)) / 6.0)
    grad_V = np.zeros_like(verts)
    np.add.at(grad_V, i0, np.cross(v1, v2) / 6.0)
    np.add.at(grad_V, i1, np.cross(v2, v0) / 6.0)
    np.add.at(grad_V, i2, np.cross(v0, v1) / 6.0)

    # Gradient of A_f wrt its three vertices: dA_f/dv0 = 0.5 * (v1 - v2) x n_hat, etc.
    dAf_dv0 = 0.5 * np.cross(v2 - v1, n_hat)
    dAf_dv1 = 0.5 * np.cross(v0 - v2, n_hat)
    dAf_dv2 = 0.5 * np.cross(v1 - v0, n_hat)

    return A_f, A_v, V, n_hat, f_centroids, grad_V, (dAf_dv0, dAf_dv1, dAf_dv2)


def compute_signed_gaps(verts_i, verts_j, faces_j, n_hat_j, f_cent_j, search_radius):
    """
    §3.4: For each vertex v of capsid i, computes signed distance g_v to capsid j's surface
    as the distance to the nearest face plane of j among faces whose centroid is within
    search_radius (3 mean-edge-lengths) of v, via a KD-tree on j's face centroids.
    Returns:
      g_v: array of shape (N_v,) with signed gap (inf if no face within search_radius)
      nearest_fi: index of the matched face on j (-1 if none)
    """
    tree = cKDTree(f_cent_j)
    # Fast bounding check: query up to k=16 nearest face centroids within search_radius
    dists, idx = tree.query(verts_i, k=8, distance_upper_bound=search_radius)
    N_v = len(verts_i)
    n_f = len(faces_j)
    g_v = np.full(N_v, np.inf, dtype=np.float64)
    nearest_fi = np.full(N_v, -1, dtype=np.int32)

    valid_rows = np.where(dists[:, 0] < np.inf)[0]
    if len(valid_rows) == 0:
        return g_v, nearest_fi

    for vi in valid_rows:
        cand = idx[vi][dists[vi] < np.inf]
        cand = cand[cand < n_f]
        if len(cand) == 0:
            continue
        # Signed distance to each candidate face plane: (x_v - c_f) . n_f
        diff = verts_i[vi][None, :] - f_cent_j[cand]
        plane_Signed = np.sum(diff * n_hat_j[cand], axis=1)
        # Select face with smallest |plane distance| + tangential proximity
        best_k = int(np.argmin(np.abs(plane_Signed) + 0.25 * dists[vi, :len(cand)]))
        fi = int(cand[best_k])
        g_v[vi] = float(plane_Signed[best_k])
        nearest_fi[vi] = fi

    return g_v, nearest_fi