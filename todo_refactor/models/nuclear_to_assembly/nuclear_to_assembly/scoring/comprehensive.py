"""Comprehensive scoring that extracts all geometric features."""

import numpy as np
from nuclear_to_assembly.geometry.solids import truncated_octahedron_vertices_faces
from nuclear_to_assembly.geometry.to_geometry import FACE_NORMALS

def get_to_edges():
    """Get all 36 edges of a truncated octahedron."""
    V, faces = truncated_octahedron_vertices_faces()
    edges = set()
    
    # Extract edges from all faces
    for face_name, vertex_indices in faces.items():
        for i in range(len(vertex_indices)):
            v1 = vertex_indices[i]
            v2 = vertex_indices[(i + 1) % len(vertex_indices)]
            edge = tuple(sorted([v1, v2]))
            edges.add(edge)
    
    return list(edges), V

def classify_edge_constraints(assembly):
    """
    For each nucleon, classify all 36 edges as:
    0: Unconstrained (no neighbor)
    1: Singly constrained (1 neighbor)
    2: Doubly constrained (2 neighbors)
    """
    edges, V = get_to_edges()
    edge_constraints = {}
    
    # Get world positions of all edge midpoints for all nucleons
    nucleon_edges = {}
    for n_id, nucleon in assembly.nucleons.items():
        R = nucleon.R
        t = nucleon.t
        edge_midpoints = []
        for v1_idx, v2_idx in edges:
            v1 = V[v1_idx]
            v2 = V[v2_idx]
            midpoint_local = (v1 + v2) / 2
            midpoint_world = R @ midpoint_local + t
            edge_midpoints.append(midpoint_world)
        nucleon_edges[n_id] = edge_midpoints
    
    # Count neighbors for each edge
    tolerance = 0.01
    for n_id, edge_points in nucleon_edges.items():
        constraints = []
        for edge_mid in edge_points:
            neighbor_count = 0
            for other_id, other_edges in nucleon_edges.items():
                if other_id == n_id:
                    continue
                for other_mid in other_edges:
                    if np.linalg.norm(edge_mid - other_mid) < tolerance:
                        neighbor_count += 1
                        break
            constraints.append(min(neighbor_count, 2))
        edge_constraints[n_id] = constraints
    
    return edge_constraints

def extract_all_features(assembly):
    """Extract all geometric features for binding analysis."""
    features = {}
    
    # Basic composition
    features['A'] = len(assembly.nucleons)
    features['Z'] = sum(1 for n in assembly.nucleons.values() if n.kind == "proton")
    features['N'] = features['A'] - features['Z']
    
    # Bond analysis by type and channel
    bond_types = {'SS': 0, 'HH': 0, 'SH': 0}
    channels = {'NP': 0, 'PP': 0, 'NN': 0}
    
    for bond in assembly.bonds:
        # Bond type
        f1_type = bond.face1[0]
        f2_type = bond.face2[0]
        if f1_type == 'S' and f2_type == 'S':
            bond_types['SS'] += 1
        elif f1_type == 'H' and f2_type == 'H':
            bond_types['HH'] += 1
        else:
            bond_types['SH'] += 1
        
        # Channel type
        k1 = assembly.nucleons[bond.n1].kind
        k2 = assembly.nucleons[bond.n2].kind
        if {k1, k2} == {'proton', 'neutron'}:
            channels['NP'] += 1
        elif k1 == k2 == 'proton':
            channels['PP'] += 1
        else:
            channels['NN'] += 1
    
    features.update({f'bonds_{k}': v for k, v in bond_types.items()})
    features.update({f'channel_{k}': v for k, v in channels.items()})
    
    # Edge constraints
    edge_constraints = classify_edge_constraints(assembly)
    edge_totals = {'edge_0': 0, 'edge_1': 0, 'edge_2': 0}
    
    for constraints in edge_constraints.values():
        for c in constraints:
            edge_totals[f'edge_{c}'] += 1
    
    features.update(edge_totals)
    
    # Surface vs interior nucleons
    surface_count = 0
    interior_count = 0
    
    for n_id in assembly.nucleons:
        bonded_faces = set()
        for b in assembly.bonds:
            if b.n1 == n_id:
                bonded_faces.add(b.face1)
            if b.n2 == n_id:
                bonded_faces.add(b.face2)
        
        if len(bonded_faces) < 14:  # Not all faces bonded
            surface_count += 1
        else:
            interior_count += 1
    
    features['surface_nucleons'] = surface_count
    features['interior_nucleons'] = interior_count
    
    # Topology - check for closed loops
    def has_closed_loop(bonds):
        if len(bonds) < 3:
            return False
        
        # Build adjacency
        from collections import defaultdict
        graph = defaultdict(set)
        for b in bonds:
            graph[b.n1].add(b.n2)
            graph[b.n2].add(b.n1)
        
        # Check for cycles
        visited = set()
        for start in graph:
            if start in visited:
                continue
            # DFS for cycle
            stack = [(start, None, [start])]
            while stack:
                node, parent, path = stack.pop()
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor == parent:
                        continue
                    if neighbor in path:
                        return True  # Found cycle
                    stack.append((neighbor, node, path + [neighbor]))
        return False
    
    features['has_closed_loop'] = 1 if has_closed_loop(assembly.bonds) else 0
    
    # Normalized features
    if features['A'] > 0:
        features['bonds_per_A'] = len(assembly.bonds) / features['A']
        features['edge1_per_A'] = edge_totals['edge_1'] / features['A']
        features['edge2_per_A'] = edge_totals['edge_2'] / features['A']
    
    return features
