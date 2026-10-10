#!/usr/bin/env python3
"""
direct_test.py - Bypass test harness and test directly
"""

import importlib

def test_directly():
    solver = importlib.import_module("nuclear_solver")
    
    # Use EXACT params that should work
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
        "energy_scale": 0.001,  # This SHOULD give us the right magnitudes with negative sign
        "coop_c1": 0.15,
        "coop_c2": 0.05,
        "gap_floor_ratio": 0.005
    }
    
    print("Direct test with energy_scale = 0.001")
    print("=" * 60)
    
    targets = {
        "D": -2.224,
        "H3": -8.482,
        "He3": -7.718,
        "He4": -28.30
    }
    
    results = {}
    for nucleus in ["D", "H3", "He3", "He4"]:
        res = solver.solve_nucleus(nucleus, params)
        energy = res.get("binding_energy_MeV", 0)
        results[nucleus] = energy
        
        # Scale up to see the actual value
        scaled = energy / 0.001
        target = targets[nucleus]
        
        print(f"{nucleus:4s}: {energy:+.6f} MeV  (÷0.001 = {scaled:+.3f} vs target {target:.3f})")
    
    split = results["H3"] - results["He3"]
    split_scaled = split / 0.001
    print(f"\nSplit: {split:+.6f} MeV  (÷0.001 = {split_scaled:+.3f} vs target +0.764)")
    
    print("\n" + "=" * 60)
    print("Now import test_harness and check its DEFAULT_PARAMS...")
    
    harness = importlib.import_module("test_harness_v1")
    
    # Compare parameters
    for key in ["energy_scale", "deflection_scale", "coop_c1", "coop_c2"]:
        harness_val = harness.DEFAULT_PARAMS.get(key, "NOT FOUND")
        our_val = params.get(key)
        match = "✓" if harness_val == our_val else "✗"
        print(f"{key:20s}: harness={harness_val:10f} ours={our_val:10f} {match}")

if __name__ == "__main__":
    test_directly()
