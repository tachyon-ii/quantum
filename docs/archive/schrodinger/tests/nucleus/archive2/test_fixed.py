#!/usr/bin/env python3
"""
test_fixed.py - Test the nuclear solver with fixed charge assignments
"""

import json

def test_with_params(params):
    """Test with given parameters"""
    import importlib
    solver = importlib.import_module("nuclear_solver")
    
    results = {}
    for nucleus in ["D", "H3", "He3", "He4"]:
        res = solver.solve_nucleus(nucleus, params)
        results[nucleus] = res["binding_energy_MeV"]
    
    return results

def main():
    # Load best params
    try:
        with open("best_params.json", "r") as f:
            params = json.load(f)
    except:
        # Use defaults if no best_params.json
        params = {
            "kappa": 1.0,
            "mu": 0.01,
            "eps0": 1.0,
            "R0": 0.86,
            "delta_eff": 0.10,
            "lambda_c": 0.45,
            "sigma_NN": 2.0,
            "sigma_NP": 1.0,
            "sigma_PP": 0.5,
            "theta_max_deg": 45.0,
            "deflection_scale": 0.8,
            "neutron_mediation_strength": 0.6,
            "mediation_range": 0.5,
            "energy_scale": 8.0,
            "gap_floor_ratio": 0.005
        }
    
    print("Testing Fixed Nuclear Solver")
    print("=" * 60)
    
    results = test_with_params(params)
    
    # Targets
    targets = {
        "D": -2.224,
        "H3": -8.482,
        "He3": -7.718,
        "He4": -28.30
    }
    
    print("\nResults with fixed charge assignments:")
    print("-" * 40)
    
    for nucleus in ["D", "H3", "He3", "He4"]:
        calc = results[nucleus]
        target = targets[nucleus]
        error = abs(calc - target)
        status = "✓" if error < (0.001 if nucleus == "D" else 0.1) else "✗"
        
        print(f"{nucleus:3s}: {calc:7.3f} MeV (target: {target:7.3f}, error: {error:5.3f}) {status}")
    
    # Calculate split
    split = results["He3"] - results["H3"]
    split_target = 0.764
    split_error = abs(split - split_target)
    split_status = "✓" if split_error < 0.05 else "✗"
    
    print(f"\nH3/He3 split: {split:+.3f} MeV (target: {split_target:+.3f}, error: {split_error:.3f}) {split_status}")
    
    print("\n" + "=" * 60)
    print("Analysis:")
    
    if split > 0:
        print("✓ Split has correct sign (He3 less bound than H3)")
    else:
        print("✗ Split has wrong sign (He3 more bound than H3)")
    
    if results["He3"] < -5:
        print("✓ He3 is reasonably bound")
    else:
        print("✗ He3 is too weakly bound")
    
    # Now debug He3 specifically
    print("\n" + "=" * 60)
    print("He3 Debug:")
    
    from nuclear_solver import solve_triangle
    he3_detailed = solve_triangle(2, params)
    print(f"He3 binding: {he3_detailed['binding_energy_MeV']:.3f} MeV")
    print(f"Edge lengths: {he3_detailed['edge_lengths_fm']}")

if __name__ == "__main__":
    main()
