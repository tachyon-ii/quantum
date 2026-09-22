#!/usr/bin/env python3
"""
debug_charges.py - See what charges are actually being used
"""

import json
import numpy as np

def debug_triangle_calculation():
    """Step through the triangle calculation manually"""
    
    # Load parameters
    with open("best_params.json", "r") as f:
        params = json.load(f)
    
    print("Manual Triangle Calculation for He3")
    print("=" * 60)
    
    # He3: P-N-P
    edge_types = ["NP", "PP", "NP"]
    charges = [(1, 0), (1, 1), (0, 1)]  # What we set
    
    print("Edge configuration:")
    for i, (et, (q1, q2)) in enumerate(zip(edge_types, charges)):
        print(f"  Edge {i+1}: {et}, charges=({q1},{q2})")
    
    # Use the actual edge lengths from the solver output
    edge_lengths = [1.764, 2.5, 1.764]  # From He3 debug output
    
    print("\nCalculating energies with these edge lengths:")
    print("-" * 40)
    
    from nuclear_solver import coulomb_energy, mesh_energy, deflection_energy
    from nuclear_solver import neutron_mediated_deflection, calculate_triangle_area
    
    r12, r13, r23 = edge_lengths
    area = calculate_triangle_area(r12, r13, r23)
    print(f"Triangle area: {area:.3f} fm²")
    
    total = 0.0
    for i, (edge_type, (q1, q2)) in enumerate(zip(edge_types, charges)):
        r = edge_lengths[i]
        r0 = {"NN": 1.6, "NP": 1.8, "PP": 2.0}[edge_type]
        
        print(f"\nEdge {i+1} ({edge_type}, r={r:.3f}):")
        print(f"  Charges: q1={q1}, q2={q2}")
        
        # Calculate each component
        E_coulomb = coulomb_energy(r, q1, q2)
        print(f"  Coulomb: {E_coulomb:.6f}")
        
        E_mesh = mesh_energy(r, r0, edge_type, params)
        print(f"  Mesh: {E_mesh:.6f}")
        
        if edge_type == "PP":
            E_deflect = neutron_mediated_deflection(r, area, params)
            print(f"  Neutron-mediated deflection: {E_deflect:.6f}")
        else:
            E_deflect = deflection_energy(r, edge_type, params)
            print(f"  Direct deflection: {E_deflect:.6f}")
        
        edge_total = E_coulomb + E_mesh + E_deflect
        print(f"  Edge subtotal: {edge_total:.6f}")
        total += edge_total
    
    print(f"\nTotal unscaled: {total:.6f}")
    print(f"Energy scale: {params['energy_scale']}")
    print(f"Total scaled: {total * params['energy_scale']:.3f} MeV")
    
    # Now check what the solver actually returns
    print("\n" + "=" * 60)
    print("Comparing with solver output:")
    
    import importlib
    solver = importlib.import_module("nuclear_solver")
    result = solver.solve_nucleus("He3", params)
    
    print(f"Solver returns: {result['binding_energy_MeV']:.3f} MeV")
    print(f"Edge lengths: {result['edge_lengths_fm']}")
    
    # The problem might be in the optimization
    print("\n" + "=" * 60)
    print("The issue might be:")
    print("1. The optimizer is finding the wrong minimum")
    print("2. The PP edge is expanding too much (2.5 fm is very long)")
    print("3. The neutron mediation is too weak at that distance")
    
    # Let's check with a forced shorter PP edge
    print("\n" + "=" * 60)
    print("Testing with forced shorter PP edge (1.9 fm):")
    
    test_edges = [1.764, 1.9, 1.764]  # Force PP to be shorter
    test_area = calculate_triangle_area(*test_edges)
    
    total_forced = 0.0
    for i, (edge_type, (q1, q2)) in enumerate(zip(edge_types, charges)):
        r = test_edges[i]
        r0 = {"NN": 1.6, "NP": 1.8, "PP": 2.0}[edge_type]
        
        E_coulomb = coulomb_energy(r, q1, q2)
        E_mesh = mesh_energy(r, r0, edge_type, params)
        
        if edge_type == "PP":
            E_deflect = neutron_mediated_deflection(r, test_area, params)
        else:
            E_deflect = deflection_energy(r, edge_type, params)
        
        total_forced += E_coulomb + E_mesh + E_deflect
    
    print(f"Total with PP=1.9: {total_forced * params['energy_scale']:.3f} MeV")
    print(f"(Compare to PP=2.5: {total * params['energy_scale']:.3f} MeV)")
    
    if total_forced < total:
        print("✓ Shorter PP edge gives lower energy - optimizer is wrong!")
    else:
        print("✗ Longer PP edge is actually lower energy")

if __name__ == "__main__":
    debug_triangle_calculation()
