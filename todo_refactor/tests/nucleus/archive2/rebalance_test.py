#!/usr/bin/env python3
"""
rebalance_test.py - Find parameters that balance mesh and deflection forces
"""

import importlib
import numpy as np

def test_balance(params):
    """Test the force balance with given parameters"""
    solver = importlib.import_module("nuclear_solver")
    
    # Test on all nuclei
    results = {}
    for nucleus in ["D", "H3", "He3", "He4"]:
        res = solver.solve_nucleus(nucleus, params)
        results[nucleus] = res["binding_energy_MeV"]
    
    # Calculate split
    split = results["H3"] - results["He3"]
    
    # Check how close we are to targets
    targets = {"D": -2.224, "H3": -8.482, "He3": -7.718, "He4": -28.30}
    errors = {k: abs(results[k] - targets[k]) for k in targets}
    total_error = sum(errors.values())
    
    return results, split, total_error

def main():
    print("Finding better force balance")
    print("=" * 60)
    
    base_params = {
        "kappa": 1.0,
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
        "energy_scale": 10,
        "coop_c1": 0.15,
        "coop_c2": 0.05,
        "gap_floor_ratio": 0.005
    }
    
    print("Current issue: Deflection is 275x stronger than mesh")
    print("Testing different force balances...\n")
    
    # Test different combinations to balance forces
    test_configs = [
        {"name": "Baseline", "mu": 0.001, "deflection_scale": 1.0},
        {"name": "Weaker deflection", "mu": 0.001, "deflection_scale": 0.1},
        {"name": "Stronger mesh", "mu": 0.01, "deflection_scale": 1.0},
        {"name": "Both adjusted", "mu": 0.005, "deflection_scale": 0.2},
        {"name": "Balanced", "mu": 0.01, "deflection_scale": 0.05},
        {"name": "Mesh dominant", "mu": 0.02, "deflection_scale": 0.01},
    ]
    
    best_config = None
    best_error = float('inf')
    
    for config in test_configs:
        params = base_params.copy()
        params["mu"] = config["mu"]
        params["deflection_scale"] = config["deflection_scale"]
        
        results, split, error = test_balance(params)
        
        print(f"{config['name']:20s} (mu={config['mu']:.3f}, defl={config['deflection_scale']:.2f}):")
        print(f"  D={results['D']:7.3f}, H3={results['H3']:7.3f}, He3={results['He3']:7.3f}, He4={results['He4']:7.3f}")
        print(f"  Split={split:6.3f} (target=-0.764), Total error={error:.2f}")
        
        if error < best_error:
            best_error = error
            best_config = config.copy()
            best_config["results"] = results
            best_config["split"] = split
    
    print("\n" + "=" * 60)
    print("Best configuration:")
    print(f"  mu = {best_config['mu']}")
    print(f"  deflection_scale = {best_config['deflection_scale']}")
    print(f"  Results: {best_config['results']}")
    print(f"  Split: {best_config['split']:.3f}")
    
    # Now test parameter sensitivity with best config
    print("\n" + "=" * 60)
    print("Testing parameter sensitivity with balanced forces:")
    
    params = base_params.copy()
    params["mu"] = best_config["mu"]
    params["deflection_scale"] = best_config["deflection_scale"]
    
    # Test r0 sensitivity
    print("\nEffect of r0_NP on Deuteron:")
    for r0 in [1.6, 1.8, 2.0]:
        params["r0_NP"] = r0
        res = importlib.import_module("nuclear_solver").solve_nucleus("D", params)
        print(f"  r0_NP={r0}: edge={res['edge_lengths_fm']['NP']:.3f}, binding={res['binding_energy_MeV']:.3f}")
    
    # Test sigma sensitivity
    params["r0_NP"] = 1.8  # Reset
    print("\nEffect of sigma_NP on H3:")
    for sigma in [0.5, 1.0, 2.0]:
        params["sigma_NP"] = sigma
        res = importlib.import_module("nuclear_solver").solve_nucleus("H3", params)
        print(f"  sigma_NP={sigma}: binding={res['binding_energy_MeV']:.3f}")
    
    # Analyze force contributions
    print("\n" + "=" * 60)
    print("Force contribution analysis with balanced parameters:")
    
    from nuclear_solver import (
        coulomb_energy_and_force,
        deflection_energy_and_force,
        _extract_mesh_params
    )
    import mesh_glue as mg
    
    params["sigma_NP"] = 1.0  # Reset
    P = _extract_mesh_params(params)
    mp = mg.MeshGlueParams(P.kappa, params["mu"], P.eps0, P.R0, P.delta_eff, P.lambda_c,
                           P.sigma_NN, P.sigma_NP, P.sigma_PP)
    
    r = 1.8  # Test at r0
    
    # NP edge forces
    Uc, _ = coulomb_energy_and_force(r, 1.0, 0.0, k_e=0.05)
    Ud, _ = deflection_energy_and_force(r, "NP", theta_max_deg=35.0,
                                       scale=params["deflection_scale"], r0_hint=1.8)
    Um = mg.u_mesh_per_edge(r, 1.8, "NP", mp)
    
    print(f"\nAt r=1.8 for NP edge:")
    print(f"  Coulomb: {Uc:.6f}")
    print(f"  Deflection: {Ud:.6f}")
    print(f"  Mesh: {Um:.6f}")
    print(f"  Deflection/Mesh ratio: {abs(Ud/Um):.1f}x")
    print(f"  Total: {Uc + Ud + Um:.6f}")

if __name__ == "__main__":
    main()
