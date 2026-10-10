#!/usr/bin/env python3
"""
diagnose_sensitivity.py - Diagnose why parameters have little effect
"""

import importlib
import numpy as np

def test_parameter_sensitivity():
    solver = importlib.import_module("nuclear_solver")
    
    base_params = {
        "kappa": 1.0,
        "mu": 0.001,
        "eps0": 1.0,
        "R0": 0.86,
        "delta_eff": 0.10,
        "lambda_c": 0.45,
        "sigma_NN": 1.25,
        "sigma_NP": 1.00,
        "sigma_PP": 0.00,
        "r0_NN": 1.6,
        "r0_NP": 1.8,
        "r0_PP": 2.0,
        "theta_max_deg": 35.0,
        "deflection_scale": 1.0,
        "energy_scale": 1.0,  # Set to 1 to see raw values
        "coop_c1": 0.15,
        "coop_c2": 0.05,
        "gap_floor_ratio": 0.005
    }
    
    # Get baseline
    res_base = solver.solve_nucleus("H3", base_params)
    base_energy = res_base.get("binding_energy_MeV", 0)
    base_lengths = res_base.get("edge_lengths_fm", {})
    
    print("Parameter Sensitivity Analysis for H3")
    print("=" * 60)
    print(f"Baseline energy: {base_energy:.6f} MeV")
    print(f"Baseline edge lengths: {base_lengths}")
    print("\n" + "-" * 60)
    
    # Test each parameter
    tests = [
        ("sigma_NN", [0.0, 0.5, 1.0, 2.0, 5.0]),
        ("sigma_NP", [0.0, 0.5, 1.0, 2.0, 5.0]),
        ("sigma_PP", [0.0, 0.5, 1.0, 2.0, 5.0]),
        ("deflection_scale", [0.0, 0.5, 1.0, 2.0, 5.0]),
        ("mu", [0.0001, 0.0005, 0.001, 0.005, 0.01]),
        ("delta_eff", [0.05, 0.08, 0.10, 0.15, 0.20]),
        ("lambda_c", [0.2, 0.3, 0.45, 0.6, 0.8]),
        ("r0_NN", [1.0, 1.3, 1.6, 1.9, 2.2]),
        ("r0_NP", [1.2, 1.5, 1.8, 2.1, 2.4]),
        ("theta_max_deg", [0, 20, 35, 50, 80]),
        ("coop_c1", [0.0, 0.1, 0.2, 0.3, 0.5]),
        ("coop_c2", [0.0, 0.05, 0.1, 0.15, 0.2]),
    ]
    
    for param_name, values in tests:
        print(f"\nTesting {param_name}:")
        energies = []
        
        for val in values:
            params = base_params.copy()
            params[param_name] = val
            
            try:
                res = solver.solve_nucleus("H3", params)
                energy = res.get("binding_energy_MeV", 0)
                energies.append(energy)
                
                change = energy - base_energy
                pct_change = (change / abs(base_energy)) * 100 if base_energy != 0 else 0
                
                print(f"  {param_name}={val:8.4f}: E={energy:10.6f} MeV, Δ={change:+8.6f} ({pct_change:+6.2f}%)")
            except Exception as e:
                print(f"  {param_name}={val:8.4f}: ERROR - {e}")
                energies.append(np.nan)
        
        # Calculate range
        valid_energies = [e for e in energies if not np.isnan(e)]
        if valid_energies:
            e_range = max(valid_energies) - min(valid_energies)
            print(f"  Range: {e_range:.6f} MeV")
            if e_range < 0.01:
                print(f"  *** WARNING: Parameter has almost NO effect! ***")
    
    # Now test combinations
    print("\n" + "=" * 60)
    print("Testing extreme combinations:")
    
    # All mesh parameters to zero
    params1 = base_params.copy()
    params1.update({"sigma_NN": 0, "sigma_NP": 0, "sigma_PP": 0})
    res1 = solver.solve_nucleus("H3", params1)
    print(f"\nAll sigmas = 0: {res1['binding_energy_MeV']:.6f} MeV")
    
    # All mesh parameters to max
    params2 = base_params.copy()
    params2.update({"sigma_NN": 5, "sigma_NP": 5, "sigma_PP": 5})
    res2 = solver.solve_nucleus("H3", params2)
    print(f"All sigmas = 5: {res2['binding_energy_MeV']:.6f} MeV")
    
    # No deflection
    params3 = base_params.copy()
    params3["deflection_scale"] = 0.0
    res3 = solver.solve_nucleus("H3", params3)
    print(f"No deflection: {res3['binding_energy_MeV']:.6f} MeV")
    
    # Check if mesh force is even being calculated
    print("\n" + "=" * 60)
    print("Checking if mesh force is working:")
    
    # Import mesh_glue if available
    try:
        mg = importlib.import_module("mesh_glue")
        
        # Test mesh force directly
        test_params = mg.MeshGlueParams(
            kappa=1.0, mu=0.001, eps0=1.0, R0=0.86,
            delta_eff=0.10, lambda_c=0.45,
            sigma_NN=1.25, sigma_NP=1.0, sigma_PP=0.0
        )
        
        # Calculate mesh force at different distances
        print("\nMesh force at different separations (NP edge):")
        for r in [1.5, 1.6, 1.7, 1.8, 1.9, 2.0]:
            u = mg.u_mesh_per_edge(r, 1.8, "NP", test_params)
            f = mg.f_mesh_per_edge(r, 1.8, "NP", test_params)
            print(f"  r={r:.1f}: U={u:12.9f}, F={f:12.9f}")
            
    except Exception as e:
        print(f"Could not test mesh_glue: {e}")

if __name__ == "__main__":
    test_parameter_sensitivity()
