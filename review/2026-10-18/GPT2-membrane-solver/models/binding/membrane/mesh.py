#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Oriented icospheres, differentiable skin geometry and literal local plane gaps.

The spatial search and point-in-polyhedron classification are discrete. They are
recomputed on EVERY objective evaluation. Autograd differentiates the chosen
plane (its vertices, normal and centroid) on BOTH skins, not the KD-tree choices.
No projection-inside-triangle test is added to the specified plane-gap rule.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from math import pi, sqrt
import numpy as np
import torch
from scipy.spatial import ConvexHull, cKDTree
from . import constants as C

DTYPE = torch.float64


class GeometryError(RuntimeError):
    """The literal functional is undefined at this trial geometry."""


@dataclass(frozen=True)
class Topology:
    unit_vertices: np.ndarray
    faces: np.ndarray
    edges: np.ndarray
    edge_faces: np.ndarray
    subdivision: int

    @property
    def n_vertices(self):
        return len(self.unit_vertices)

    @property
    def n_faces(self):
        return len(self.faces)


@lru_cache(maxsize=None)
def icosphere(subdivision: int = C.SUBDIV) -> Topology:
    if not isinstance(subdivision, int) or subdivision < 0:
        raise ValueError('subdivision must be a nonnegative integer')
    phi = (1 + sqrt(5)) / 2
    vertices = []
    for a in (-1, 1):
        for b in (-1, 1):
            vertices += [(0, a, b * phi), (a, b * phi, 0), (b * phi, 0, a)]
    v = np.asarray(vertices, dtype=float)
    v /= np.linalg.norm(v, axis=-1, keepdims=True)
    f = ConvexHull(v).simplices.copy()
    for face in f:
        a, b, c = v[face]
        if np.dot(np.cross(b - a, c - a), a + b + c) < 0:
            face[1], face[2] = face[2], face[1]
    f = np.asarray(sorted(map(tuple, f)), dtype=np.int64)
    for _ in range(subdivision):
        points = list(v)
        midpoints = {}

        def midpoint(a, b):
            key = tuple(sorted((a, b)))
            if key not in midpoints:
                p = (v[a] + v[b]) / 2
                midpoints[key] = len(points)
                points.append(p / np.linalg.norm(p))
            return midpoints[key]

        faces = []
        for a, b, c in f:
            ab, bc, ca = midpoint(a, b), midpoint(b, c), midpoint(c, a)
            faces.extend(((a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)))
        v, f = np.asarray(points), np.asarray(faces, dtype=np.int64)
    adjacency = {}
    for fi, face in enumerate(f):
        for a, b in zip(face, np.roll(face, -1)):
            adjacency.setdefault(tuple(sorted((a, b))), []).append(fi)
    if any(len(adj) != 2 for adj in adjacency.values()):
        raise GeometryError('The icosphere is not a closed two-manifold.')
    edges = np.asarray(sorted(adjacency), dtype=np.int64)
    edge_faces = np.asarray([adjacency[tuple(e)] for e in edges], dtype=np.int64)
    for array in (v, f, edges, edge_faces):
        array.flags.writeable = False
    return Topology(v, f, edges, edge_faces, subdivision)


def numpy_geometry(vertices: np.ndarray, faces: np.ndarray):
    """Single skin; volume is translation invariant and signed."""
    center = vertices.mean(axis=0)
    tri = vertices[faces]
    cross = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    double_areas = np.linalg.norm(cross, axis=-1)
    if np.any(double_areas <= C.DEGENERATE_EPS):
        raise GeometryError('Degenerate triangle.')
    areas = double_areas / 2
    normals = cross / double_areas[:, None]
    volume = np.einsum('ij,ij->i', tri[:, 0] - center, cross).sum() / 6
    vertex_areas = np.zeros(len(vertices))
    np.add.at(vertex_areas, faces.ravel(), np.repeat(areas / 3, 3))
    return {'center': center, 'face_areas': areas, 'vertex_areas': vertex_areas,
            'face_centers': tri.mean(axis=1), 'normals': normals, 'volume': volume}


def torch_geometry(x: torch.Tensor, faces: torch.Tensor, edges: torch.Tensor,
                   edge_faces: torch.Tensor):
    """Batched exact piecewise-planar areas, volumes and dihedral sum."""
    tri = x[:, faces]
    centroids = x.mean(dim=1)
    cross = torch.linalg.cross(tri[:, :, 1] - tri[:, :, 0], tri[:, :, 2] - tri[:, :, 0])
    double_area = torch.linalg.vector_norm(cross, dim=-1)
    if bool(torch.any(double_area.detach() <= C.DEGENERATE_EPS)):
        raise GeometryError('Degenerate triangle in objective.')
    areas = double_area / 2
    normals = cross / double_area[:, :, None]
    volume = ((tri[:, :, 0] - centroids[:, None]) * cross).sum(dim=(-1, -2)) / 6
    if bool(torch.any(volume.detach() <= C.DEGENERATE_EPS)):
        raise GeometryError('Nonpositive signed enclosed volume.')
    va = x.new_zeros(x.shape[:-1])
    idx = faces.reshape(1, -1).expand(x.shape[0], -1)
    va = va.scatter_add(1, idx, areas.repeat_interleave(3, dim=1) / 3)
    dihedral_cos = (normals[:, edge_faces[:, 0]] * normals[:, edge_faces[:, 1]]).sum(dim=-1)
    bend_sum = (1 - dihedral_cos).sum(dim=-1)
    edge_lengths = torch.linalg.vector_norm(x[:, edges[:, 0]] - x[:, edges[:, 1]], dim=-1)
    return {'centroids': centroids, 'face_areas': areas, 'vertex_areas': va,
            'face_centers': tri.mean(dim=2), 'normals': normals, 'volume': volume,
            'bending_sum': bend_sum, 'mean_edge': edge_lengths.mean(dim=-1)}


@dataclass
class System:
    name: str
    species: tuple[str, ...]
    topology: Topology
    rest_areas: np.ndarray
    rest_volume: np.ndarray
    rest_total_area: np.ndarray
    radii: np.ndarray
    initial: np.ndarray
    singlet_np: frozenset[tuple[int, int]] = frozenset()

    @property
    def count(self):
        return len(self.species)

    @property
    def pairs(self):
        return tuple(combinations(range(self.count), 2))

    def singlet(self, i, j):
        return self.species[i] == self.species[j] or (min(i, j), max(i, j)) in self.singlet_np


def starting_centres(name: str):
    d, a, b = C.START_EDGE, C.START_TRI_X, C.START_TRI_Y
    geometries = {
        'p': (('p',), ((0, 0, 0),)),
        'n': (('n',), ((0, 0, 0),)),
        'D': (('p', 'n'), ((0, 0, 0), (d, 0, 0))),
        'T': (('p', 'n', 'n'), ((0, 0, 0), (d, 0, 0), (a, b, 0))),
        'He3': (('p', 'p', 'n'), ((0, 0, 0), (d, 0, 0), (a, b, 0))),
        'He4': (('p', 'p', 'n', 'n'), ((0, 0, 0), (d, 0, 0),
                 (d / 2, sqrt(3) * d / 2, 0),
                 (d / 2, sqrt(3) * d / 6, sqrt(2 / 3) * d))),
    }
    if name not in geometries:
        raise ValueError(f'Unknown geometry {name!r}')
    species, centers = geometries[name]
    return species, np.asarray(centers, dtype=float)


def make_system(name: str, subdivision: int = C.SUBDIV, *,
                singlet_np: frozenset[tuple[int, int]] = frozenset()) -> System:
    species, centers = starting_centres(name)
    topology = icosphere(subdivision)
    radii = np.array([C.RP if s == 'p' else C.RN for s in species])
    vertices = radii[:, None, None] * topology.unit_vertices[None]
    rest_areas = np.asarray([numpy_geometry(v, topology.faces)['face_areas'] for v in vertices])
    return System(name, species, topology, rest_areas, 4 * pi * radii ** 3 / 3,
                  4 * pi * radii ** 2, radii, vertices + centers[:, None], singlet_np)


def solid_angle_inside(points: np.ndarray, vertices: np.ndarray, faces: np.ndarray):
    """Generalized winding fallback: oriented closed mesh, including nonconvex skins."""
    result = np.zeros(len(points), dtype=bool)
    triangles = vertices[faces]
    for start in range(0, len(points), C.WINDING_CHUNK):
        p = points[start:start + C.WINDING_CHUNK]
        abc = triangles[None] - p[:, None, None]
        a, b, c = abc[:, :, 0], abc[:, :, 1], abc[:, :, 2]
        la, lb, lc = (np.linalg.norm(vec, axis=-1) for vec in (a, b, c))
        numerator = np.einsum('pfi,pfi->pf', a, np.cross(b, c))
        denominator = la * lb * lc + np.einsum('pfi,pfi->pf', a, b) * lc \
            + np.einsum('pfi,pfi->pf', b, c) * la + np.einsum('pfi,pfi->pf', c, a) * lb
        winding = (2 * np.arctan2(numerator, denominator)).sum(axis=-1) / (4 * pi)
        result[start:start + len(p)] = np.abs(winding) > C.WINDING_INSIDE
    return result


class SurfaceQuery:
    """One current skin's acceleration structures, rebuilt each objective call.

    Interior sign uses an exact triangle-ray parity test. The projected KD query
    is conservative (maximum triangle radius); ambiguous edge hits fall back to
    solid angles. This does not assume convexity or use centres as distance DOFs.
    """
    def __init__(self, vertices, topology):
        self.v, self.topology = np.asarray(vertices), topology
        self.tri = self.v[topology.faces]
        g = numpy_geometry(self.v, topology.faces)
        self.centers, self.normals = g['face_centers'], g['normals']
        self.tree = cKDTree(self.centers)
        self.mean_edge = np.linalg.norm(self.v[topology.edges[:, 0]] - self.v[topology.edges[:, 1]], axis=-1).mean()
        ray = np.asarray(C.RAY_DIRECTION)
        self.ray = ray / np.linalg.norm(ray)
        b1 = np.cross(self.ray, np.eye(3)[-1]); b1 /= np.linalg.norm(b1)
        self.basis = np.stack((b1, np.cross(self.ray, b1)), axis=1)
        projected = self.centers @ self.basis
        self.projected_tree = cKDTree(projected)
        self.projected_radius = np.linalg.norm((self.tri - self.centers[:, None]) @ self.basis, axis=-1).max()

    def inside(self, points):
        result = np.zeros(len(points), dtype=bool)
        lo, hi = self.v.min(axis=0), self.v.max(axis=0)
        rows = np.flatnonzero(np.all((points >= lo) & (points <= hi), axis=1))
        if not len(rows):
            return result
        p = points[rows]
        candidates = self.projected_tree.query_ball_point(p @ self.basis,
            self.projected_radius + C.RAY_EPS, workers=C.KD_WORKERS, return_sorted=True)
        counts = np.fromiter(map(len, candidates), dtype=np.int64)
        if not counts.sum():
            return result
        owner = np.repeat(np.arange(len(p)), counts)
        fi = np.concatenate(candidates).astype(np.int64)
        tri, origin = self.tri[fi], p[owner]
        e1, e2 = tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]
        h = np.cross(np.broadcast_to(self.ray, e2.shape), e2)
        det = np.einsum('ij,ij->i', e1, h)
        valid = np.abs(det) > C.RAY_EPS
        inv = np.divide(1., det, out=np.zeros_like(det), where=valid)
        s = origin - tri[:, 0]
        u = inv * np.einsum('ij,ij->i', s, h)
        q = np.cross(s, e1)
        vv = inv * (q @ self.ray)
        t = inv * np.einsum('ij,ij->i', e2, q)
        hit = valid & (t > C.RAY_EPS) & (u >= -C.RAY_EPS) & (vv >= -C.RAY_EPS) & (u + vv <= 1 + C.RAY_EPS)
        hits = np.bincount(owner[hit], minlength=len(p))
        local = (hits % 2) == 1
        edge = hit & ((np.abs(u) <= C.RAY_EPS) | (np.abs(vv) <= C.RAY_EPS) | (np.abs(u + vv - 1) <= C.RAY_EPS))
        surface = valid & (np.abs(t) <= C.RAY_EPS) & (u >= -C.RAY_EPS) & (vv >= -C.RAY_EPS) & (u + vv <= 1 + C.RAY_EPS)
        ambiguous = np.unique(owner[edge | surface])
        if len(ambiguous):
            local[ambiguous] = solid_angle_inside(p[ambiguous], self.v, self.topology.faces)
        result[rows] = local
        return result

    def select(self, points):
        candidates = self.tree.query_ball_point(points, C.NEIGHBOUR_REACH * self.mean_edge,
                         workers=C.KD_WORKERS, return_sorted=True)
        counts = np.fromiter(map(len, candidates), dtype=np.int64)
        selected = np.full(len(points), -1, dtype=np.int64)
        if counts.sum():
            owner = np.repeat(np.arange(len(points)), counts)
            fi = np.concatenate(candidates).astype(np.int64)
            distance = np.abs(np.einsum('ij,ij->i', points[owner] - self.centers[fi], self.normals[fi]))
            order = np.lexsort((fi, distance, owner))
            ordered_rows = owner[order]
            first = np.r_[True, ordered_rows[1:] != ordered_rows[:-1]]
            selected[ordered_rows[first]] = fi[order[first]]
        inside = self.inside(points)
        if np.any(inside & (selected < 0)):
            raise GeometryError('Inside vertex has no face in the specified KD neighbourhood; gap is undefined. No fallback energy was invented.')
        return selected, inside


def selected_gaps(source: torch.Tensor, target_centers: torch.Tensor,
                  target_normals: torch.Tensor, selection):
    """+inf for outside vertices without local candidates (explicit convention)."""
    index, inside = selection
    valid = index >= 0
    out = source.new_full((len(source),), float('inf'))
    if np.any(valid):
        rows = torch.as_tensor(np.flatnonzero(valid), dtype=torch.long)
        fi = torch.as_tensor(index[valid], dtype=torch.long)
        signs = torch.as_tensor(np.where(inside[valid], -1., 1.), dtype=DTYPE)
        distance = ((source[rows] - target_centers[fi]) * target_normals[fi]).sum(dim=-1).abs()
        out = out.index_copy(0, rows, signs * distance)
    return out


def graph_connected(count: int, contacts: dict[tuple[int, int], bool]) -> bool:
    if count <= 1:
        return True
    seen, pending = {0}, [0]
    while pending:
        node = pending.pop()
        for (a, b), active in contacts.items():
            if active and node in (a, b):
                other = b if node == a else a
                if other not in seen:
                    seen.add(other); pending.append(other)
    return len(seen) == count
