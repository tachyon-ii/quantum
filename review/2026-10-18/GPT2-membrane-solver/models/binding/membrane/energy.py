#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""The eight terms in §3, literally; float64 PyTorch autograd."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import torch
from . import constants as C
from .mesh import DTYPE, System, SurfaceQuery, selected_gaps, torch_geometry, graph_connected


@dataclass
class Evaluation:
    energy: float
    terms: dict
    capsids: list
    pairs: dict
    centers: np.ndarray
    connected: bool

    @property
    def binding_energy(self):
        return -self.energy

    @property
    def all_pairs_contact(self):
        return all(pair['contact'] for pair in self.pairs.values())


def fade(gap: torch.Tensor, delta: float, shape: str):
    value = torch.clamp(1 - gap / delta, min=0, max=1)
    return value.square() if shape == 'quadratic' else value


class Functional:
    def __init__(self, system: System, parameters: C.Parameters):
        self.system, self.p = system, parameters
        t = system.topology
        self.faces = torch.tensor(t.faces.copy(), dtype=torch.long)
        self.edges = torch.tensor(t.edges.copy(), dtype=torch.long)
        self.edge_faces = torch.tensor(t.edge_faces.copy(), dtype=torch.long)
        self.rest_areas = torch.tensor(system.rest_areas, dtype=DTYPE)
        self.rest_volume = torch.tensor(system.rest_volume, dtype=DTYPE)
        self.rest_total_area = torch.tensor(system.rest_total_area, dtype=DTYPE)

    def torch_value(self, x: torch.Tensor):
        geo = torch_geometry(x, self.faces, self.edges, self.edge_faces)
        inflate = self.p.E0 * (self.rest_volume / geo['volume'] - 1)
        area = self.p.area_factor * self.p.E0 / self.rest_total_area * \
            ((geo['face_areas'] - self.rest_areas).square() / self.rest_areas).sum(dim=-1)
        bend = self.p.bend_fraction * self.p.E0 * geo['bending_sum']
        zero = x.sum() * 0
        terms = {'inflate': inflate.sum(), 'area': area.sum(), 'bend': bend.sum(),
                 'adhesion': zero, 'penetration': zero, 'mesh': zero, 'coulomb': zero}
        pair_data, contacts = {}, {}
        detached = x.detach().numpy()
        queries = [SurfaceQuery(v, self.system.topology) for v in detached] if self.system.count > 1 else []
        for i, j in self.system.pairs:
            gi = selected_gaps(x[i], geo['face_centers'][j], geo['normals'][j], queries[j].select(detached[i]))
            gj = selected_gaps(x[j], geo['face_centers'][i], geo['normals'][i], queries[i].select(detached[j]))
            si, sj = fade(gi, self.p.delta, self.p.fade), fade(gj, self.p.delta, self.p.fade)
            ai, aj = geo['vertex_areas'][i], geo['vertex_areas'][j]
            adhesion = -self.p.e0 * ((ai * si).sum() + (aj * sj).sum())
            penetration = C.K_PEN(self.p.e0) * ((ai * torch.clamp(-gi, min=0).square()).sum()
                                          + (aj * torch.clamp(-gj, min=0).square()).sum())
            active = bool(torch.any(gi.detach() < self.p.delta) or torch.any(gj.detach() < self.p.delta))
            contacts[(i, j)] = active
            mesh = zero + (self.p.mesh_energy if active and self.system.singlet(i, j) else 0)
            distance = torch.linalg.vector_norm(geo['centroids'][i] - geo['centroids'][j])
            coulomb = C.AHC / distance if self.system.species[i] == self.system.species[j] == 'p' else zero
            for key, val in [('adhesion', adhesion), ('penetration', penetration), ('mesh', mesh), ('coulomb', coulomb)]:
                terms[key] = terms[key] + val
            pair_data[(i, j)] = {'contact': active, 'singlet': self.system.singlet(i, j),
                'gap_i': gi, 'gap_j': gj, 'weight_i': si, 'weight_j': sj,
                'area_i': ai, 'area_j': aj, 'adhesion': adhesion, 'penetration': penetration,
                'mesh': mesh, 'coulomb': coulomb, 'distance': distance}
        connected = graph_connected(self.system.count, contacts)
        terms['slingshot'] = zero - (self.system.count * C.Y(self.system.count) if connected else 0)
        total = sum(terms.values())
        return total, {'terms': terms, 'capsids': {'inflate': inflate, 'area': area, 'bend': bend},
                       'geo': geo, 'pairs': pair_data, 'connected': connected}

    def value_and_gradient(self, vertices: np.ndarray):
        x = torch.tensor(np.asarray(vertices), dtype=DTYPE, requires_grad=True)
        value, _ = self.torch_value(x)
        gradient, = torch.autograd.grad(value, x)
        return float(value.detach()), gradient.detach().numpy()

    def evaluate(self, vertices: np.ndarray) -> Evaluation:
        with torch.no_grad():
            value, data = self.torch_value(torch.as_tensor(vertices, dtype=DTYPE))
        pair_data = {}
        for key, vals in data['pairs'].items():
            pair_data[key] = {name: (val.numpy().copy() if val.ndim else float(val))
                              if isinstance(val, torch.Tensor) else val for name, val in vals.items()}
        capsids = []
        for i, species in enumerate(self.system.species):
            capsids.append({'species': species, 'volume': float(data['geo']['volume'][i]),
                            'area': float(data['geo']['face_areas'][i].sum()),
                            'rest_volume': float(self.system.rest_volume[i]),
                            'rest_total_area': float(self.system.rest_total_area[i]),
                            'mean_edge': float(data['geo']['mean_edge'][i]),
                            **{k: float(v[i]) for k, v in data['capsids'].items()}})
        return Evaluation(float(value), {k: float(v) for k, v in data['terms'].items()}, capsids,
                          pair_data, data['geo']['centroids'].numpy().copy(), data['connected'])
