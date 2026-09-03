#!/usr/bin/env python3
"""
diagnose_r0.py - Understand why r0_* parameters have no effect
"""

import importlib
import numpy as np
import matplotlib.pyplot as plt

def analyze_r0_behavior():
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
        "energy_scale": 1.0,
        "coop_c1": 0.15,
        "coop_c2": 0.05,
        "gap_floor_ratio": 0.005
    }
    
    print("Analyzing r0 parameter behavior")
    print("=" * 60)
    
    # Test Deuteron (single NP edge) with different r0_NP values
    print("\nDeuteron with different r0_NP values:")
    print("-" * 40)
    
    r0_values = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
    
    for r0 in r0_values:
        params = base_params.copy()
        params["r0_NP"] = r0
        
        res = solver.solve_nucleus("D", params)
        edge_length = res["edge_lengths_fm"]["NP"]
        binding = res["binding_energy_MeV"]
        
        print(f"  r0_NP={r0:.1f}: edge_length={edge_length:.4f}, binding={binding:.6f}")
        
        # Check if edge length equals r0
        if abs(edge_length - r0) < 0.001:
            print(f"    -> Edge length MATCHES r0!")
        else:
            print(f"    -> Edge length differs by {edge_length - r0:+.4f}")
    
    # Now let's trace through the energy landscape
    print("\n" + "=" * 60)
    print("Energy landscape analysis for NP edge:")
    print("-" * 40)
    
    # Import the functions directly
    from nuclear_solver import (
        coulomb_energy_and_force,
        deflection_energy_and_force,
        _extract_mesh_params
    )
    
    # Check if using fixed or original deflection
    import inspect
    deflection_source = inspect.getsource(deflection_energy_and_force)
    if "theta_max_rad" in deflection_source:
        print("Using FIXED deflection function ✓")
    else:
        print("Using ORIGINAL (broken) deflection function ✗")
    
    mg = importlib.import_module("mesh_glue")
    
    # Calculate energies at different distances
    r_values = np.linspace(1.0, 2.5, 50)
    r0_test = 1.8
    
    U_coulomb = []
    U_deflect = []
    U_mesh = []
    U_total = []
    
    P = _extract_mesh_params(base_params)
    mp = mg.MeshGlueParams(P.kappa, P.mu, P.eps0, P.R0, P.delta_eff, P.lambda_c,
                           P.sigma_NN, P.sigma_NP, P.sigma_PP)
    
    for r in r_values:
        # Coulomb (NP edge has q1=+1, q2=0)
        Uc, _ = coulomb_energy_and_force(r, 1.0, 0.0, k_e=0.05)
        U_coulomb.append(Uc)
        
        # Deflection
        Ud, _ = deflection_energy_and_force(r, "NP", theta_max_deg=35.0,
                                           scale=1.0, r0_hint=r0_test)
        U_deflect.append(Ud)
        
        # Mesh
        Um = mg.u_mesh_per_edge(r, r0_test, "NP", mp)
        U_mesh.append(Um)
        
        # Total
        U_total.append(Uc + Ud + Um)
    
    # Find minimum
    min_idx = np.argmin(U_total)
    r_min = r_values[min_idx]
    U_min = U_total[min_idx]
    
    print(f"\nFor r0_NP={r0_test}:")
    print(f"  Energy minimum at r={r_min:.3f}")
    print(f"  Minimum energy: {U_min:.6f}")
    print(f"  Differs from r0 by: {r_min - r0_test:+.3f}")
    
    # Component contributions at minimum
    print(f"\nAt minimum (r={r_min:.3f}):")
    print(f"  Coulomb: {U_coulomb[min_idx]:.6f}")
    print(f"  Deflection: {U_deflect[min_idx]:.6f}")
    print(f"  Mesh: {U_mesh[min_idx]:.6f}")
    print(f"  Deflection/Mesh ratio: {abs(U_deflect[min_idx]/U_mesh[min_idx]):.1f}x")
    
    # Plot if matplotlib available
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(r_values, U_coulomb, 'r-', label='Coulomb')
        plt.plot(r_values, U_deflect, 'b-', label='Deflection')
        plt.plot(r_values, np.array(U_mesh) * 100, 'g-', label='Mesh (×100)')
        plt.plot(r_values, U_total, 'k-', linewidth=2, label='Total')
        plt.axvline(r0_test, color='gray', linestyle='--', label=f'r0={r0_test}')
        plt.axvline(r_min, color='red', linestyle='--', label=f'minimum={r_min:.3f}')
        plt.xlabel('Distance (fm)')
        plt.ylabel('Energy')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.title('Energy Components vs Distance for NP Edge')
        plt.savefig('energy_landscape.png')
        print("\nPlot saved as energy_landscape.png")
    except:
        print("\n(Matplotlib not available for plotting)")

if __name__ == "__main__":
    analyze_r0_behavior()
