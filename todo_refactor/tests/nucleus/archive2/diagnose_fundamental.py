#!/usr/bin/env python3
"""
diagnose_fundamental.py - Check if the fundamental physics is correct
"""

import json
import numpy as np

def analyze_physics():
    """Analyze the fundamental physics of the model"""
    
    print("Fundamental Physics Analysis")
    print("=" * 60)
    
    # Load the "optimal" parameters
    with open("optimal_params.json", "r") as f:
        params = json.load(f)
    
    import importlib
    solver = importlib.import_module("nuclear_solver")
    
    # Test each nucleus
    for nucleus in ["D", "H3", "He3", "He4"]:
        print(f"\n{nucleus} Analysis:")
        print("-" * 40)
        
        res = solver.solve_nucleus(nucleus, params)
        print(f"Binding energy: {res['binding_energy_MeV']:.3f} MeV")
        print(f"Edge lengths: {res['edge_lengths_fm']}")
        
        if nucleus == "H3":
            print("Configuration: N-P-N triangle")
            print("Expected: Strong NN edge makes it more bound")
            
        elif nucleus == "He3":
            print("Configuration: P-N-P triangle")
            print("Expected: PP Coulomb makes it less bound")
            print("But neutron mediation is overcompensating!")
            
        elif nucleus == "He4":
            print("Configuration: Tetrahedron (2P + 2N)")
            print("This is WAY too weakly bound - something is very wrong")
    
    # Check the split physics
    print("\n" + "=" * 60)
    print("Split Analysis:")
    print("-" * 40)
    
    h3 = solver.solve_nucleus("H3", params)
    he3 = solver.solve_nucleus("He3", params)
    
    split_actual = he3["binding_energy_MeV"] - h3["binding_energy_MeV"]
    split_target = 0.764
    
    print(f"H3 binding:  {h3['binding_energy_MeV']:.3f} MeV")
    print(f"He3 binding: {he3['binding_energy_MeV']:.3f} MeV")
    print(f"Split: {split_actual:+.3f} MeV (should be {split_target:+.3f})")
    
    if split_actual < 0:
        print("\n✗ WRONG: He3 is MORE bound than H3!")
        print("  This violates basic physics - Coulomb should make He3 LESS bound")
    
    # The root cause analysis
    print("\n" + "=" * 60)
    print("ROOT CAUSE ANALYSIS:")
    print("-" * 40)
    
    print("\n1. The triangular solver is flawed:")
    print("   - Neutron mediation is too strong for He3")
    print("   - It's overcoming Coulomb too much")
    print("   - The PP edge should have LESS attractive contribution")
    
    print("\n2. The tetrahedral solver is broken:")
    print("   - He4 should be ~28 MeV bound, not ~8 MeV")
    print("   - The simplified approach isn't working")
    
    print("\n3. Possible solutions:")
    print("   a) Reduce neutron mediation for PP edges")
    print("   b) Add proper Coulomb screening/shielding")
    print("   c) Implement proper 3-body/4-body physics")
    print("   d) Go back to edge-by-edge with corrections")
    
    # Test without mediation
    print("\n" + "=" * 60)
    print("Testing without neutron mediation:")
    print("-" * 40)
    
    params_no_med = params.copy()
    params_no_med["neutron_mediation_strength"] = 0.0
    
    for nucleus in ["H3", "He3"]:
        res = solver.solve_nucleus(nucleus, params_no_med)
        print(f"{nucleus}: {res['binding_energy_MeV']:.3f} MeV")
    
    h3_no_med = solver.solve_nucleus("H3", params_no_med)
    he3_no_med = solver.solve_nucleus("He3", params_no_med)
    split_no_med = he3_no_med["binding_energy_MeV"] - h3_no_med["binding_energy_MeV"]
    
    print(f"Split without mediation: {split_no_med:+.3f} MeV")
    
    if split_no_med > 0:
        print("✓ Without mediation, split has correct sign")
        print("  But magnitude is probably too large")

def check_alternative():
    """Check if we should use a different approach"""
    
    print("\n" + "=" * 60)
    print("Alternative Approach Suggestion:")
    print("-" * 40)
    
    print("\nThe hybrid triangular/tetrahedral solver is too complex.")
    print("Consider reverting to the edge-by-edge approach with:")
    
    print("\n1. Proper force balance (mesh vs deflection)")
    print("2. Edge-specific corrections for A=3 nuclei")
    print("3. Three-body terms for He4")
    print("4. Empirical corrections for the split")
    
    print("\nOr adopt the v3_4 approach which gets most things right")
    print("except for the split, and add a small correction term.")

if __name__ == "__main__":
    analyze_physics()
    check_alternative()
