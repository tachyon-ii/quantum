#!/usr/bin/env python3
"""
check_params.py - Check if energy_scale is actually being used
"""

import importlib

def test_param_variations():
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
        "coop_c1": 0.15,
        "coop_c2": 0.05,
        "gap_floor_ratio": 0.005
    }
    
    print("Testing energy_scale parameter usage:")
    print("=" * 60)
    
    # Test WITHOUT energy_scale
    print("\n1. WITHOUT energy_scale key:")
    res = solver.solve_nucleus("D", base_params)
    print(f"   Result: {res.get('binding_energy_MeV')}")
    
    # Test with energy_scale = 1.0
    params2 = base_params.copy()
    params2["energy_scale"] = 1.0
    print("\n2. WITH energy_scale = 1.0:")
    res2 = solver.solve_nucleus("D", params2)
    print(f"   Result: {res2.get('binding_energy_MeV')}")
    
    # Test with energy_scale = 0.001
    params3 = base_params.copy()
    params3["energy_scale"] = 0.001
    print("\n3. WITH energy_scale = 0.001:")
    res3 = solver.solve_nucleus("D", params3)
    print(f"   Result: {res3.get('binding_energy_MeV')}")
    
    # Test with energy_scale = -0.001
    params4 = base_params.copy()
    params4["energy_scale"] = -0.001
    print("\n4. WITH energy_scale = -0.001:")
    res4 = solver.solve_nucleus("D", params4)
    print(f"   Result: {res4.get('binding_energy_MeV')}")
    
    # Check if it's looking for a different key name
    params5 = base_params.copy()
    params5["energy_scale"] = 0.001
    params5["energy_scaling"] = -1000  # Wrong key
    params5["scale_energy"] = -1000    # Wrong key
    print("\n5. WITH energy_scale = 0.001 and wrong keys:")
    res5 = solver.solve_nucleus("D", params5)
    print(f"   Result: {res5.get('binding_energy_MeV')}")
    
    # Now let's check what DEFAULT value is used if not provided
    print("\n" + "=" * 60)
    print("Checking default value in nuclear_solver.py:")
    
    import inspect
    source = inspect.getsource(solver.solve_nucleus)
    
    # Look for energy_scale usage
    for line in source.split('\n'):
        if 'energy_scale' in line:
            print(f"   {line.strip()}")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  No param:           {res.get('binding_energy_MeV')}")
    print(f"  energy_scale=1.0:   {res2.get('binding_energy_MeV')}")
    print(f"  energy_scale=0.001: {res3.get('binding_energy_MeV')}")
    print(f"  energy_scale=-0.001:{res4.get('binding_energy_MeV')}")

if __name__ == "__main__":
    test_param_variations()
