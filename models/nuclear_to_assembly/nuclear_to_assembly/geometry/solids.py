import itertools
import math
import numpy as np

SQRT2 = math.sqrt(2.0)
INV_SQRT2 = 1.0 / SQRT2

def _unique_rows(a: np.ndarray) -> np.ndarray:
    a = np.ascontiguousarray(a)
    unique = np.unique(a.view([('', a.dtype)] * a.shape[1]))
    return unique.view(a.dtype).reshape(-1, a.shape[1])

def truncated_octahedron_vertices_faces():
    """
    Return (V, faces) where:
      V: (24,3) array of vertex coords for a canonical truncated octahedron
         with edge length 1, built from all unique permutations of
         (0, ±1/√2, ±√2).
      faces: dict[str, List[int]] mapping face label -> ordered vertex indices.
    """
    # Build vertices: all permutations of (0, ±1/√2, ±√2) with signs on nonzero entries
    verts = []
    base = (0.0, INV_SQRT2, SQRT2)
    for signs in itertools.product([1.0, -1.0], repeat=2):
        a, b = signs
        for perm in set(itertools.permutations((0.0, a * INV_SQRT2, b * SQRT2), 3)):
            verts.append(perm)
    V = _unique_rows(np.array(verts, dtype=float))
    assert V.shape == (24, 3), f"Unexpected vertex count {V.shape}"

    # Helper: order face vertices cyclically in its plane for proper rendering
    def order_face(indices, normal):
        pts = V[indices]
        center = pts.mean(axis=0)
        n = np.asarray(normal, dtype=float)
        n = n / np.linalg.norm(n)
        # reference not parallel to n
        ref = np.array([0.0, 0.0, 1.0])
        if abs(np.dot(ref, n)) > 0.9:
            ref = np.array([1.0, 0.0, 0.0])
        u = np.cross(n, ref); u /= np.linalg.norm(u)
        v = np.cross(n, u)
        rel = pts - center
        angles = np.arctan2(rel @ v, rel @ u)
        order = np.argsort(angles)
        return [indices[i] for i in order.tolist()]

    faces = {}

    # Squares: x = ±√2 ; y = ±√2 ; z = ±√2
    idx_xp = np.where(np.isclose(V[:, 0],  SQRT2))[0].tolist()
    idx_xn = np.where(np.isclose(V[:, 0], -SQRT2))[0].tolist()
    idx_yp = np.where(np.isclose(V[:, 1],  SQRT2))[0].tolist()
    idx_yn = np.where(np.isclose(V[:, 1], -SQRT2))[0].tolist()
    idx_zp = np.where(np.isclose(V[:, 2],  SQRT2))[0].tolist()
    idx_zn = np.where(np.isclose(V[:, 2], -SQRT2))[0].tolist()

    faces["S+X"] = order_face(idx_xp, ( 1, 0, 0))
    faces["S-X"] = order_face(idx_xn, (-1, 0, 0))
    faces["S+Y"] = order_face(idx_yp, (0,  1, 0))
    faces["S-Y"] = order_face(idx_yn, (0, -1, 0))
    faces["S+Z"] = order_face(idx_zp, (0, 0,  1))
    faces["S-Z"] = order_face(idx_zn, (0, 0, -1))

    # Hexes: s1*x + s2*y + s3*z = 3/√2
    def plane_indices(s1, s2, s3):
        vals = s1 * V[:, 0] + s2 * V[:, 1] + s3 * V[:, 2]
        rhs = 3.0 * INV_SQRT2
        return np.where(np.isclose(vals, rhs))[0].tolist()

    faces["H+++"] = order_face(plane_indices( 1,  1,  1), ( 1,  1,  1))
    faces["H++-"] = order_face(plane_indices( 1,  1, -1), ( 1,  1, -1))
    faces["H+-+"] = order_face(plane_indices( 1, -1,  1), ( 1, -1,  1))
    faces["H-++"] = order_face(plane_indices(-1,  1,  1), (-1,  1,  1))
    faces["H+--"] = order_face(plane_indices( 1, -1, -1), ( 1, -1, -1))
    faces["H-+-"] = order_face(plane_indices(-1,  1, -1), (-1,  1, -1))
    faces["H--+"] = order_face(plane_indices(-1, -1,  1), (-1, -1,  1))
    faces["H---"] = order_face(plane_indices(-1, -1, -1), (-1, -1, -1))

    return V, faces

