#!/usr/bin/env python3
"""
debug_hybrid.py - Debug why the hybrid solver isn't working
"""

import importlib
import json
import numpy as np

def analyze_triangle(Z, params):
    """Detailed analysis of triangle solving"""
    
    solver = importlib.import_module("nuclear_solver")
    
    # Import the triangle solver internals
    from nuclear_solver import (
        coulomb_energy, mesh_energy, deflection_energy,
        neutron_mediated_deflection, calculate_triangle_area
    )
    
    nucleus = "H3" if Z == 1 else "He3"
    print(f"\n{'='*60}")
    print(f"Analyzing {nucleus} (Z={Z})")
    print('='*60)
    
    # Solve
    result = solver.solve_nucleus(nucleus, params)
    print(f"Total binding: {result['binding_energy_MeV']:.3f} MeV")
    print(f"Edge lengths: {result['edge_lengths_fm']}")
    
    # Now break down the energy contributions
    if Z == 1:  # H3: N-P-N
        edge_types = ["NP", "NN", "NP"]
        charges = [(1, 0), (0, 0), (1, 0)]
        print("\nExpected: 2 NP edges + 1 NN edge")
    else:  # He3: P-N-P
        edge_types = ["NP", "PP", "NP"]
        charges = [(1, 1), (1, 0), (1, 0)]
        print("\nExpected: 2 NP edges + 1 PP edge")
    
    # Get the actual edge lengths from the result
    edges = []
    for et in edge_types:
        edges.append(result['edge_lengths_fm'][et])
    
    r12, r13, r23 = edges
    area = calculate_triangle_area(r12, r13, r23)
    print(f"\nTriangle area: {area:.3f} fm²")
    
    # Calculate energy breakdown
    print("\nEnergy breakdown by edge:")
    print("-" * 40)
    
    total_unscaled = 0.0
    for i, (edge_type, (q1, q2)) in enumerate(zip(edge_types, charges)):
        r = edges[i]
        r0 = {"NN": 1.6, "NP": 1.8, "PP": 2.0}[edge_type]
        
        E_coulomb = coulomb_energy(r, q1, q2)
        E_mesh = mesh_energy(r, r0, edge_type, params)
        
        if edge_type == "PP":
            E_deflect_direct = deflection_energy(r, edge_type, params)
            E_deflect_mediated = neutron_mediated_deflection(r, area, params)
            E_deflect = E_deflect_mediated  # Only mediated for PP
            
            print(f"Edge {i+1} ({edge_type}, r={r:.3f}):")
            print(f"  Coulomb:  {E_coulomb:+.6f}")
            print(f"  Mesh:     {E_mesh:+.6f}")
            print(f"  Direct deflection: {E_deflect_direct:+.6f} (should be 0)")
            print(f"  Mediated deflection: {E_deflect_mediated:+.6f}")
            print(f"  Subtotal: {E_coulomb + E_mesh + E_deflect:+.6f}")
        else:
            E_deflect = deflection_energy(r, edge_type, params)
            
            print(f"Edge {i+1} ({edge_type}, r={r:.3f}):")
            print(f"  Coulomb:  {E_coulomb:+.6f}")
            print(f"  Mesh:     {E_mesh:+.6f}")
            print(f"  Deflection: {E_deflect:+.6f}")
            print(f"  Subtotal: {E_coulomb + E_mesh + E_deflect:+.6f}")
        
        total_unscaled += E_coulomb + E_mesh + E_deflect
    
    print(f"\nTotal unscaled: {total_unscaled:.6f}")
    print(f"Energy scale: {params['energy_scale']}")
    print(f"Total scaled: {total_unscaled * params['energy_scale']:.3f} MeV")
    print(f"Reported binding: {result['binding_energy_MeV']:.3f} MeV")
    
    # Check PP mediation specifically
    if Z == 2:  # He3
        print("\n" + "="*40)
        print("PP Edge Mediation Analysis:")
        r_pp = result['edge_lengths_fm']['PP']
        h = 2 * area / r_pp if r_pp > 0 else 0
        print(f"  PP edge length: {r_pp:.3f} fm")
        print(f"  Perpendicular distance to neutron: {h:.3f} fm")
        print(f"  Mediation range parameter: {params['mediation_range']}")
        print(f"  Effectiveness: {np.exp(-h/params['mediation_range']):.3f}")
        print(f"  Mediation strength: {params['neutron_mediation_strength']}")

def main():
    # Load best params
    with open("best_params.json", "r") as f:
        params = json.load(f)
    
    print("Debugging Hybrid Solver")
    print("=" * 60)
    
    # Test both triangles
    analyze_triangle(1, params)  # H3
    analyze_triangle(2, params)  # He3
    
    # Compare
    print("\n" + "="*60)
    print("COMPARISON:")
    print("-" * 40)
    
    solver = importlib.import_module("nuclear_solver")
    h3 = solver.solve_nucleus("H3", params)
    he3 = solver.solve_nucleus("He3", params)
    
    print(f"H3 binding:  {h3['binding_energy_MeV']:.3f} MeV")
    print(f"He3 binding: {he3['binding_energy_MeV']:.3f} MeV")
    print(f"Split (He3-H3): {he3['binding_energy_MeV'] - h3['binding_energy_MeV']:.3f} MeV")
    print(f"Expected split: +0.764 MeV")
    
    print("\nProblem diagnosis:")
    if he3['binding_energy_MeV'] > h3['binding_energy_MeV']:
        print("✗ He3 is LESS bound than H3 (correct direction)")
        print("  But the magnitude is way too large!")
    else:
        print("✗ He3 is MORE bound than H3 (wrong direction!)")
    
    print("\nLikely issues:")
    print("1. PP Coulomb repulsion is too strong")
    print("2. Neutron mediation is too weak or ineffective")
    print("3. The geometry (triangle area) might be wrong")
    print("4. Energy scale is masking the real physics")

if __name__ == "__main__":
    main()
