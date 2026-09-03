#!/usr/bin/env python3
"""
find_optimal.py - Fine-tune mediation parameters for correct split
"""

import json
import numpy as np

def test_combination(strength, med_range, scale):
    """Test a specific combination of parameters"""
    
    params = {
        "kappa": 1.0,
        "mu": 0.005,
        "eps0": 1.0,
        "R0": 0.86,
        "delta_eff": 0.08,
        "lambda_c": 0.5,
        "sigma_NN": 1.25,
        "sigma_NP": 1.0,
        "sigma_PP": 0.0,
        "r0_NN": 1.6,
        "r0_NP": 1.8,
        "r0_PP": 2.0,
        "theta_max_deg": 35.0,
        "gap_floor_ratio": 0.005,
        "deflection_scale": 1.0,
        "neutron_mediation_strength": strength,
        "mediation_range": med_range,
        "energy_scale": scale
    }
    
    import importlib
    solver = importlib.import_module("nuclear_solver")
    
    results = {}
    for nuc in ["D", "H3", "He3", "He4"]:
        res = solver.solve_nucleus(nuc, params)
        results[nuc] = res["binding_energy_MeV"]
    
    return results

def find_optimal():
    """Find optimal parameters"""
    
    print("Finding Optimal Mediation Parameters")
    print("=" * 60)
    
    # Based on previous results, search in this range
    strength_range = np.linspace(4.0, 4.8, 9)
    range_range = [0.8, 1.0, 1.2, 1.5]
    scale_range = [5, 6, 7]
    
    targets = {"D": -2.224, "H3": -8.482, "He3": -7.718, "He4": -28.30}
    target_split = 0.764
    
    best_score = float('inf')
    best_params = None
    best_results = None
    
    print("Searching parameter space...")
    print("-" * 60)
    
    for scale in scale_range:
        for med_range in range_range:
            for strength in strength_range:
                results = test_combination(strength, med_range, scale)
                
                # Calculate errors
                split = results["He3"] - results["H3"]
                
                # Weighted error score
                score = (
                    10 * abs(results["D"] - targets["D"]) +
                    4 * abs(results["H3"] - targets["H3"]) +
                    4 * abs(results["He3"] - targets["He3"]) +
                    2 * abs(results["He4"] - targets["He4"]) +
                    8 * abs(split - target_split)
                )
                
                if score < best_score:
                    best_score = score
                    best_params = (strength, med_range, scale)
                    best_results = results
                    
                    print(f"New best: strength={strength:.1f}, range={med_range:.1f}, scale={scale}")
                    print(f"  Split: {split:+.3f} MeV (target: +0.764)")
                    print(f"  Score: {score:.2f}")
    
    print("\n" + "=" * 60)
    print("OPTIMAL PARAMETERS FOUND:")
    print("-" * 40)
    
    strength, med_range, scale = best_params
    print(f"neutron_mediation_strength: {strength:.2f}")
    print(f"mediation_range: {med_range:.2f}")
    print(f"energy_scale: {scale}")
    
    print("\nResults with optimal parameters:")
    for nuc in ["D", "H3", "He3", "He4"]:
        calc = best_results[nuc]
        target = targets[nuc]
        error = abs(calc - target)
        print(f"{nuc:3s}: {calc:7.3f} MeV (target: {target:7.3f}, error: {error:5.3f})")
    
    split = best_results["He3"] - best_results["H3"]
    print(f"\nSplit: {split:+.3f} MeV (target: +{target_split:.3f})")
    
    # Check pass/fail
    print("\nPASS/FAIL:")
    pass_d = abs(best_results["D"] - targets["D"]) < 0.001
    pass_h3 = abs(best_results["H3"] - targets["H3"]) < 0.05
    pass_he3 = abs(best_results["He3"] - targets["He3"]) < 0.05
    pass_he4 = abs(best_results["He4"] - targets["He4"]) < 0.10
    pass_split = abs(split - target_split) < 0.05
    
    print(f"  D:     {'PASS' if pass_d else 'FAIL'}")
    print(f"  H3:    {'PASS' if pass_h3 else 'FAIL'}")
    print(f"  He3:   {'PASS' if pass_he3 else 'FAIL'}")
    print(f"  He4:   {'PASS' if pass_he4 else 'FAIL'}")
    print(f"  Split: {'PASS' if pass_split else 'FAIL'}")
    
    # Save optimal parameters
    optimal_params = {
        "kappa": 1.0,
        "mu": 0.005,
        "eps0": 1.0,
        "R0": 0.86,
        "delta_eff": 0.08,
        "lambda_c": 0.5,
        "sigma_NN": 1.25,
        "sigma_NP": 1.0,
        "sigma_PP": 0.0,
        "r0_NN": 1.6,
        "r0_NP": 1.8,
        "r0_PP": 2.0,
        "theta_max_deg": 35.0,
        "gap_floor_ratio": 0.005,
        "deflection_scale": 1.0,
        "neutron_mediation_strength": strength,
        "mediation_range": med_range,
        "energy_scale": scale
    }
    
    with open("optimal_params.json", "w") as f:
        json.dump(optimal_params, f, indent=2)
    
    print("\nOptimal parameters saved to optimal_params.json")
    
    return optimal_params

if __name__ == "__main__":
    find_optimal()
