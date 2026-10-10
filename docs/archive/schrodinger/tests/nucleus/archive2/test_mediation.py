#!/usr/bin/env python3
"""
test_mediation.py - Test with much stronger neutron mediation
"""

import json
import numpy as np

def test_mediation_strength():
    """Test different mediation strengths"""
    
    # Base parameters
    with open("best_params.json", "r") as f:
        base_params = json.load(f)
    
    print("Testing Neutron Mediation Strength")
    print("=" * 60)
    
    # Test range of mediation strengths
    test_strengths = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0]
    test_ranges = [0.5, 1.0, 1.5, 2.0]
    
    import importlib
    solver = importlib.import_module("nuclear_solver")
    
    print("\nVarying mediation_strength (with range=0.7):")
    print("-" * 40)
    print("Strength | D      | H3     | He3    | He4    | Split  | PP edge")
    print("-" * 60)
    
    for strength in test_strengths:
        params = base_params.copy()
        params["neutron_mediation_strength"] = strength
        params["mediation_range"] = 0.7
        
        results = {}
        for nuc in ["D", "H3", "He3", "He4"]:
            res = solver.solve_nucleus(nuc, params)
            results[nuc] = res["binding_energy_MeV"]
        
        he3_res = solver.solve_nucleus("He3", params)
        pp_edge = he3_res["edge_lengths_fm"]["PP"]
        
        split = results["He3"] - results["H3"]
        
        print(f"{strength:8.1f} | {results['D']:6.2f} | {results['H3']:6.2f} | "
              f"{results['He3']:6.2f} | {results['He4']:6.2f} | {split:+6.3f} | {pp_edge:.2f}")
    
    print("\n" + "=" * 60)
    print("Varying mediation_range (with strength=3.0):")
    print("-" * 40)
    print("Range   | D      | H3     | He3    | He4    | Split  | PP edge")
    print("-" * 60)
    
    for range_val in test_ranges:
        params = base_params.copy()
        params["neutron_mediation_strength"] = 3.0
        params["mediation_range"] = range_val
        
        results = {}
        for nuc in ["D", "H3", "He3", "He4"]:
            res = solver.solve_nucleus(nuc, params)
            results[nuc] = res["binding_energy_MeV"]
        
        he3_res = solver.solve_nucleus("He3", params)
        pp_edge = he3_res["edge_lengths_fm"]["PP"]
        
        split = results["He3"] - results["H3"]
        
        print(f"{range_val:8.1f} | {results['D']:6.2f} | {results['H3']:6.2f} | "
              f"{results['He3']:6.2f} | {results['He4']:6.2f} | {split:+6.3f} | {pp_edge:.2f}")
    
    print("\n" + "=" * 60)
    print("Target values:")
    print(f"D: -2.224, H3: -8.482, He3: -7.718, He4: -28.30, Split: +0.764")
    
    print("\nObservations:")
    print("- Stronger mediation should make He3 more bound")
    print("- PP edge should shrink as mediation gets stronger")
    print("- Split should approach +0.764 MeV")

def calculate_optimal_mediation():
    """Calculate what mediation strength would be needed"""
    
    print("\n" + "=" * 60)
    print("Calculating required mediation strength:")
    print("-" * 40)
    
    # At PP distance of 2.0 fm (reasonable), what mediation is needed?
    r_pp = 2.0
    coulomb_at_2fm = 1.44 / 2.0  # 0.72 MeV
    
    print(f"At PP distance = {r_pp} fm:")
    print(f"  Coulomb repulsion: +{coulomb_at_2fm:.3f} MeV")
    print(f"  Needed mediation: at least -{coulomb_at_2fm:.3f} MeV")
    
    # With current mediation formula
    area = 1.5  # Approximate triangle area
    h = 2 * area / r_pp  # Perpendicular distance
    
    for med_range in [0.5, 1.0, 1.5, 2.0]:
        effectiveness = np.exp(-h / med_range)
        
        # To overcome Coulomb, we need: strength * effectiveness * sin(theta) > coulomb
        # Assuming sin(theta) ≈ 0.6 (for 35 degrees)
        needed_strength = coulomb_at_2fm / (effectiveness * 0.6)
        
        print(f"\n  With mediation_range = {med_range}:")
        print(f"    Perpendicular distance h = {h:.2f} fm")
        print(f"    Effectiveness = {effectiveness:.3f}")
        print(f"    Needed strength ≈ {needed_strength:.1f}")

if __name__ == "__main__":
    test_mediation_strength()
    calculate_optimal_mediation()
