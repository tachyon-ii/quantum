#!/usr/bin/env python3
"""
deep_trace.py - Find where the sign is being forced positive
"""

import importlib
import sys

def monkey_patch_solver():
    """Monkey patch the solver to trace the calculation"""
    solver = importlib.import_module("nuclear_solver")
    
    # Save original function
    original_solve = solver.solve_nucleus
    
    def traced_solve(nucleus, params):
        print(f"\n=== Solving {nucleus} ===")
        print(f"energy_scale parameter: {params.get('energy_scale')}")
        
        # Call original
        result = original_solve(nucleus, params)
        
        print(f"Returned binding_energy_MeV: {result.get('binding_energy_MeV')}")
        
        # Try to trace the calculation by re-implementing key parts
        edge_types = solver.NUCLEUS_EDGES.get(nucleus, [])
        print(f"Edge types for {nucleus}: {edge_types}")
        
        # Check if there's any post-processing
        if hasattr(solver, 'total_energy'):
            print(f"total_energy (if accessible): {solver.total_energy}")
        
        return result
    
    solver.solve_nucleus = traced_solve
    return solver

def test_direct_calculation():
    """Try to directly access the internals"""
    solver = importlib.import_module("nuclear_solver")
    
    params = {
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
        "energy_scale": 0.001,
        "coop_c1": 0.15,
        "coop_c2": 0.05,
        "gap_floor_ratio": 0.005
    }
    
    print("Testing different energy_scale values:")
    print("=" * 60)
    
    for scale in [1.0, 0.001, -0.001, -1.0]:
        params["energy_scale"] = scale
        res = solver.solve_nucleus("D", params)
        energy = res.get("binding_energy_MeV", 0)
        print(f"energy_scale = {scale:+.3f}: binding = {energy:+.10f}")
    
    # Now let's check if the issue is in _extract_mesh_params or similar
    print("\n" + "=" * 60)
    print("Checking parameter extraction:")
    
    # Look for any abs() in the source
    import inspect
    source = inspect.getsource(solver.solve_nucleus)
    if 'abs(' in source:
        print("WARNING: Found abs() in solve_nucleus!")
        # Find all occurrences
        lines = source.split('\n')
        for i, line in enumerate(lines):
            if 'abs(' in line:
                print(f"  Line {i}: {line.strip()}")
    
    # Check minimise_edge_energy
    if hasattr(solver, 'minimise_edge_energy'):
        source2 = inspect.getsource(solver.minimise_edge_energy)
        if 'abs(' in source2:
            print("WARNING: Found abs() in minimise_edge_energy!")
            lines = source2.split('\n')
            for i, line in enumerate(lines):
                if 'abs(' in line:
                    print(f"  Line {i}: {line.strip()}")
    
    # Check for float() conversions that might be problematic
    print("\n" + "=" * 60)
    print("Checking for problematic float() conversions:")
    
    # Test if energy_scale is being extracted properly
    if hasattr(solver, '_as_scalar'):
        test_vals = [0.001, -0.001, [0.001], [-0.001]]
        for val in test_vals:
            result = solver._as_scalar(val, 1.0)
            print(f"_as_scalar({val}) = {result}")

def check_test_harness():
    """Check if test harness is doing something weird"""
    print("\n" + "=" * 60)
    print("Checking test harness behavior:")
    
    # Simulate what test_harness does
    test_energy = 0.00030135302391281316  # Your actual D result
    target = -2.224
    tol = 0.001
    
    # The actual comparison
    in_range = (test_energy >= target - tol) and (test_energy <= target + tol)
    print(f"Energy {test_energy} in range [{target - tol}, {target + tol}]? {in_range}")
    
    # What if we flip it?
    test_energy_neg = -test_energy
    in_range_neg = (test_energy_neg >= target - tol) and (test_energy_neg <= target + tol)
    print(f"Energy {test_energy_neg} in range [{target - tol}, {target + tol}]? {in_range_neg}")

if __name__ == "__main__":
    print("DEEP TRACE: Finding the sign issue")
    print("=" * 60)
    
    test_direct_calculation()
    check_test_harness()
    
    print("\n" + "=" * 60)
    print("Monkey patching to trace execution:")
    solver = monkey_patch_solver()
    
    params = {
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
        "energy_scale": -0.001,  # Try negative
        "coop_c1": 0.15,
        "coop_c2": 0.05,
        "gap_floor_ratio": 0.005
    }
    
    res = solver.solve_nucleus("D", params)
    print(f"\nFinal result: {res.get('binding_energy_MeV')}")
