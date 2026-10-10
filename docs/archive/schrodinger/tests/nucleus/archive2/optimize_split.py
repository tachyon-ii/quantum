#!/usr/bin/env python3
"""
optimize_split.py - Focus on getting the H3/He3 split magnitude correct
"""

import importlib
import numpy as np

def test_configuration(params):
    """Test a parameter configuration"""
    solver = importlib.import_module("nuclear_solver")
    
    results = {}
    for nucleus in ["D", "H3", "He3", "He4"]:
        res = solver.solve_nucleus(nucleus, params)
        results[nucleus] = res.get("binding_energy_MeV", 0)
    
    split = results["H3"] - results["He3"]
    
    return results, split

def main():
    base_params = {
        "kappa": 1.0,
        "mu": 0.001,
        "eps0": 1.0,
        "R0": 0.86,
        "delta_eff": 0.10,
        "lambda_c": 0.45,
        "r0_NN": 1.6,
        "r0_NP": 1.8,
        "r0_PP": 2.0,
        "theta_max_deg": 35.0,
        "deflection_scale": 1.0,
        "energy_scale": 10,
        "gap_floor_ratio": 0.005
    }
    
    print("Optimizing H3/He3 split magnitude")
    print("=" * 60)
    print("Current issue: Split is -5.18 MeV, should be -0.764 MeV")
    print("Need to reduce the difference between H3 and He3 binding\n")
    
    # The key parameters that affect the split
    print("Testing different sigma and cooperative parameters...")
    print("-" * 60)
    
    best_split_error = float('inf')
    best_params = None
    best_results = None
    
    # Try different combinations
    for sigma_NN in [0.8, 1.0, 1.25, 1.5]:
        for sigma_NP in [0.8, 1.0, 1.2]:
            for sigma_PP in [0.0, 0.2, 0.4, 0.6]:
                for coop_c1 in [0.0, 0.05, 0.10, 0.15]:
                    for coop_c2 in [0.0, 0.02, 0.05]:
                        
                        params = base_params.copy()
                        params["sigma_NN"] = sigma_NN
                        params["sigma_NP"] = sigma_NP
                        params["sigma_PP"] = sigma_PP
                        params["coop_c1"] = coop_c1
                        params["coop_c2"] = coop_c2
                        
                        results, split = test_configuration(params)
                        
                        # Target split is -0.764
                        split_error = abs(split - (-0.764))
                        
                        if split_error < best_split_error:
                            best_split_error = split_error
                            best_params = params.copy()
                            best_results = results.copy()
                            
                            print(f"\nImproved split: {split:.3f} MeV (error: {split_error:.3f})")
                            print(f"  sigma_NN={sigma_NN}, sigma_NP={sigma_NP}, sigma_PP={sigma_PP}")
                            print(f"  coop_c1={coop_c1}, coop_c2={coop_c2}")
                            print(f"  H3: {results['H3']:.3f}, He3: {results['He3']:.3f}")
    
    print("\n" + "=" * 60)
    print("BEST CONFIGURATION FOUND:")
    print("-" * 60)
    
    split = best_results["H3"] - best_results["He3"]
    
    print(f"Binding energies:")
    print(f"  D:   {best_results['D']:7.3f} MeV (target: -2.224)")
    print(f"  H3:  {best_results['H3']:7.3f} MeV (target: -8.482)")
    print(f"  He3: {best_results['He3']:7.3f} MeV (target: -7.718)")
    print(f"  He4: {best_results['He4']:7.3f} MeV (target: -28.30)")
    print(f"\nSplit: {split:6.3f} MeV (target: -0.764)")
    print(f"Split error: {abs(split - (-0.764)):.3f} MeV")
    
    print(f"\nKey parameters:")
    print(f"  sigma_NN: {best_params['sigma_NN']}")
    print(f"  sigma_NP: {best_params['sigma_NP']}")
    print(f"  sigma_PP: {best_params['sigma_PP']}")
    print(f"  coop_c1: {best_params['coop_c1']}")
    print(f"  coop_c2: {best_params['coop_c2']}")
    
    # Now fine-tune energy_scale to get absolute values right
    print("\n" + "=" * 60)
    print("Fine-tuning energy_scale for absolute values...")
    
    # Calculate what energy_scale should be based on deuteron
    current_D = best_results["D"]
    target_D = -2.224
    suggested_scale = 10 * (target_D / current_D)
    
    print(f"Current D: {current_D:.3f}, Target: {target_D}")
    print(f"Suggested energy_scale: {suggested_scale:.2f}")
    
    # Test with suggested scale
    best_params["energy_scale"] = suggested_scale
    final_results, final_split = test_configuration(best_params)
    
    print(f"\nWith energy_scale = {suggested_scale:.2f}:")
    print(f"  D:   {final_results['D']:7.3f} MeV (error: {abs(final_results['D']+2.224):.3f})")
    print(f"  H3:  {final_results['H3']:7.3f} MeV (error: {abs(final_results['H3']+8.482):.3f})")
    print(f"  He3: {final_results['He3']:7.3f} MeV (error: {abs(final_results['He3']+7.718):.3f})")
    print(f"  He4: {final_results['He4']:7.3f} MeV (error: {abs(final_results['He4']+28.30):.3f})")
    print(f"  Split: {final_split:6.3f} MeV (error: {abs(final_split+0.764):.3f})")

if __name__ == "__main__":
    main()
