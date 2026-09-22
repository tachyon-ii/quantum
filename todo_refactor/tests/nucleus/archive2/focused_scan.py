#!/usr/bin/env python3
"""
focused_scan.py - Focused parameter scan to optimize the model
Updated for hybrid solver with neutron mediation parameters
"""

import importlib
import itertools
import json

# Target values
TARGETS = {
    "D": -2.224,
    "H3": -8.482,
    "He3": -7.718,
    "He4": -28.30
}

def objective(results):
    """Calculate objective function"""
    score = 0
    
    # Energy errors (weighted)
    score += 10 * abs(results["D"] - TARGETS["D"])
    score += 4 * abs(results["H3"] - TARGETS["H3"])
    score += 4 * abs(results["He3"] - TARGETS["He3"])
    score += 4 * abs(results["He4"] - TARGETS["He4"])
    
    # Split error (critical!)
    split = results["H3"] - results["He3"]
    score += 6 * abs(split - 0.764)
    
    # Penalty if split has wrong sign
    if split < 0:
        score += 100
        
    return score

def test_params(params):
    """Test a parameter set"""
    solver = importlib.import_module("nuclear_solver")
    
    results = {}
    for nucleus in ["D", "H3", "He3", "He4"]:
        res = solver.solve_nucleus(nucleus, params)
        results[nucleus] = res.get("binding_energy_MeV", 0)
    
    return results, objective(results)

def main():
    base_params = {
        "kappa": 1.0,
        "eps0": 1.0,
        "R0": 0.86,
        "sigma_NN": 1.25,
        "sigma_NP": 1.00,
        "sigma_PP": 0.00,
        "r0_NN": 1.6,
        "r0_NP": 1.8,
        "r0_PP": 2.0,
        "theta_max_deg": 35.0,
        "gap_floor_ratio": 0.005,
        # New parameters for hybrid solver
        "neutron_mediation_strength": 0.6,
        "mediation_range": 0.5
    }
    
    # Focus on key parameters that affect the results
    grid = {
        "mu": [0.005, 0.01, 0.02],
        "delta_eff": [0.08, 0.10, 0.12],
        "lambda_c": [0.40, 0.45, 0.50],
        "deflection_scale": [0.5, 0.8, 1.0],
        "energy_scale": [6, 8, 10, 12],
        "neutron_mediation_strength": [0.3, 0.6, 0.9],
        "mediation_range": [0.3, 0.5, 0.7]
    }
    
    print("Scanning parameters...")
    print("=" * 60)
    
    best_score = float('inf')
    best_params = None
    best_results = None
    
    # Generate all combinations
    keys = list(grid.keys())
    values = [grid[k] for k in keys]
    
    total_combos = 1
    for v in values:
        total_combos *= len(v)
    print(f"Testing {total_combos} combinations...")
    
    count = 0
    for combo in itertools.product(*values):
        count += 1
        if count % 100 == 0:
            print(f"  Tested {count}/{total_combos}...")
        
        # Build params
        params = base_params.copy()
        for i, key in enumerate(keys):
            params[key] = combo[i]
        
        # Test
        try:
            results, score = test_params(params)
            
            if score < best_score:
                best_score = score
                best_params = params
                best_results = results
                
                # Print improvement
                split = results["H3"] - results["He3"]
                print(f"\nNew best (score={score:.2f}):")
                print(f"  D:    {results['D']:7.3f} (target: {TARGETS['D']})")
                print(f"  H3:   {results['H3']:7.3f} (target: {TARGETS['H3']})")
                print(f"  He3:  {results['He3']:7.3f} (target: {TARGETS['He3']})")
                print(f"  He4:  {results['He4']:7.3f} (target: {TARGETS['He4']})")
                print(f"  Split: {split:6.3f} (target: 0.764)")
                print(f"  Key params: mu={params['mu']:.3f}, delta={params['delta_eff']:.2f}, "
                      f"scale={params['energy_scale']}, defl={params['deflection_scale']:.1f}, "
                      f"med={params['neutron_mediation_strength']:.1f}")
        except Exception as e:
            # Skip failed parameter combinations
            continue
    
    if best_params is None:
        print("\nNo valid parameter combinations found!")
        return
    
    print("\n" + "=" * 60)
    print("BEST PARAMETERS FOUND:")
    print(json.dumps(best_params, indent=2))
    
    print("\nFINAL RESULTS:")
    split = best_results["H3"] - best_results["He3"]
    print(f"  D:    {best_results['D']:7.3f} MeV (error: {abs(best_results['D']-TARGETS['D']):.3f})")
    print(f"  H3:   {best_results['H3']:7.3f} MeV (error: {abs(best_results['H3']-TARGETS['H3']):.3f})")
    print(f"  He3:  {best_results['He3']:7.3f} MeV (error: {abs(best_results['He3']-TARGETS['He3']):.3f})")
    print(f"  He4:  {best_results['He4']:7.3f} MeV (error: {abs(best_results['He4']-TARGETS['He4']):.3f})")
    print(f"  Split: {split:6.3f} MeV (error: {abs(split-0.764):.3f})")
    
    # Check pass conditions
    print("\nPASS/FAIL:")
    print(f"  D:    {'PASS' if abs(best_results['D']-TARGETS['D']) < 0.001 else 'FAIL'}")
    print(f"  H3:   {'PASS' if abs(best_results['H3']-TARGETS['H3']) < 0.05 else 'FAIL'}")
    print(f"  He3:  {'PASS' if abs(best_results['He3']-TARGETS['He3']) < 0.05 else 'FAIL'}")
    print(f"  He4:  {'PASS' if abs(best_results['He4']-TARGETS['He4']) < 0.10 else 'FAIL'}")
    print(f"  Split: {'PASS' if abs(split-0.764) < 0.05 else 'FAIL'}")
    
    # Save best params
    with open("best_params.json", "w") as f:
        json.dump(best_params, f, indent=2)
    print("\nBest parameters saved to best_params.json")

if __name__ == "__main__":
    main()
