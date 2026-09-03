"""
param_scan_v1.py — n^x grid search for Angular Deflection Model (v3)

Purpose
-------
Programmatically search the global parameter space to minimize a composite
objective derived from Tests 3.1 & 3.2. This removes manual tuning.

It expects `nuclear_solver.py` on PYTHONPATH (same folder) with the function:
    solve_nucleus(nucleus: str, params: dict) -> dict

Usage
-----
1) Prepare a parameter grid JSON (optional). If omitted, built-in defaults are used.
   Example: params_grid.json (values are lists to scan)
   {
     "kappa": [1.0],
     "mu": [0.01, 0.015, 0.02, 0.025],
     "eps0": [1.0],
     "R0": [0.86],
     "delta_eff": [0.08, 0.07, 0.06, 0.055, 0.05],
     "lambda_c": [0.40, 0.45, 0.50, 0.55],
     "sigma_NN": [1.25, 1.30, 1.35],
     "sigma_NP": [1.00],
     "sigma_PP": [0.00],
     "gap_floor_ratio": [0.005],
     "r0_NN": [1.6], "r0_NP": [1.8], "r0_PP": [2.0],
     "theta_max_deg": [35.0],
     "deflection_scale": [0.05, 0.08, 0.12],
     "energy_scale": [1.0]
   }

2) Run:
       python3 param_scan_v1.py --grid params_grid.json
   or simply:
       python3 param_scan_v1.py

3) Outputs:
   - scan_results.csv     : every trial with objective and components
   - top10.json           : top 10 parameter sets by objective (lowest first)
"""

import argparse, csv, importlib, sys, os, json, itertools
from math import isfinite

# Targets
ED_star   = -2.224
EH3_star  = -8.482
EHe3_star = -7.718
EHe4_star = -28.30
SPLIT_star = 0.764

# Weights (tweak if desired)
WEIGHTS = {
    "D":     10.0,
    "H3":     4.0,
    "He3":    4.0,
    "He4":    4.0,
    "Split":  6.0,
    "Edge":   8.0,   # ordering
    "Rp":     2.0,   # proton radius band
    "Rn2":    1.0    # neutron <r^2> band/sign
}

def try_import_solver():
    try:
        return importlib.import_module("nuclear_solver")
    except Exception as e:
        print("[SCAN] Could not import nuclear_solver:", e)
        sys.exit(1)

def run_case(solver, nucleus, params):
    return solver.solve_nucleus(nucleus, params)

def edge_order_ok(el):
    try:
        nn, np_, pp = el.get("NN"), el.get("NP"), el.get("PP")
        return (nn is not None) and (np_ is not None) and (pp is not None) and (nn < np_ < pp)
    except Exception:
        return False

def objective(resD, resH3, resHe3, resHe4):
    # Energies
    ED   = resD.get("binding_energy_MeV", float("nan"))
    EH3  = resH3.get("binding_energy_MeV", float("nan"))
    EHe3 = resHe3.get("binding_energy_MeV", float("nan"))
    EHe4 = resHe4.get("binding_energy_MeV", float("nan"))
    # Edge orders
    edge_ok = edge_order_ok(resD.get("edge_lengths_fm", {})) \
              and edge_order_ok(resH3.get("edge_lengths_fm", {})) \
              and edge_order_ok(resHe3.get("edge_lengths_fm", {})) \
              and edge_order_ok(resHe4.get("edge_lengths_fm", {}))
    # Radii
    rp = resHe4.get("proton_charge_radius_fm", None) or resHe3.get("proton_charge_radius_fm", None) \
         or resH3.get("proton_charge_radius_fm", None) or resD.get("proton_charge_radius_fm", None)
    rn2 = resHe4.get("neutron_ms_radius_fm2", None) or resHe3.get("neutron_ms_radius_fm2", None) \
          or resH3.get("neutron_ms_radius_fm2", None) or resD.get("neutron_ms_radius_fm2", None)

    # Base squared errors (nan-safe large penalty)
    def se(val, tgt): 
        if val is None or not isfinite(val): return 1e6
        return (val - tgt) ** 2

    J = 0.0
    J += WEIGHTS["D"]    * se(ED,   ED_star)
    J += WEIGHTS["H3"]   * se(EH3,  EH3_star)
    J += WEIGHTS["He3"]  * se(EHe3, EHe3_star)
    J += WEIGHTS["He4"]  * se(EHe4, EHe4_star)
    # Split
    if isfinite(EH3) and isfinite(EHe3):
        split = EH3 - EHe3
        J += WEIGHTS["Split"] * (split - SPLIT_star) ** 2
    else:
        J += WEIGHTS["Split"] * 1e6

    # Constraints as penalties
    if not edge_ok:
        J += WEIGHTS["Edge"] * 1e4
    if rp is None or (rp < 0.840 or rp > 0.878):
        J += WEIGHTS["Rp"] * 5e3
    if rn2 is None or (rn2 >= 0) or (abs(rn2) < 0.05 or abs(rn2) > 0.20):
        J += WEIGHTS["Rn2"] * 2e3

    return J

def expand_grid(grid_dict):
    keys = list(grid_dict.keys())
    vals = [grid_dict[k] if isinstance(grid_dict[k], list) else [grid_dict[k]] for k in keys]
    for combo in itertools.product(*vals):
        yield dict(zip(keys, combo))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", type=str, default=None, help="JSON file with parameter grid (values as lists)")
    parser.add_argument("--out_csv", type=str, default="scan_results.csv")
    parser.add_argument("--topk_json", type=str, default="top10.json")
    parser.add_argument("--topk", type=int, default=10)
    args = parser.parse_args()

    # Default grid (coarse but sensible)
    grid = {
        "kappa": [1.0],
        "mu": [0.010, 0.015, 0.020, 0.025],
        "eps0": [1.0],
        "R0": [0.86],
        "delta_eff": [0.080, 0.070, 0.060, 0.055, 0.050],
        "lambda_c": [0.40, 0.45, 0.50, 0.55],
        "sigma_NN": [1.25, 1.30, 1.35],
        "sigma_NP": [1.00],
        "sigma_PP": [0.00],
        "gap_floor_ratio": [0.005],
        "r0_NN": [1.6], "r0_NP": [1.8], "r0_PP": [2.0],
        "theta_max_deg": [35.0],
        "deflection_scale": [0.05, 0.08, 0.12],
        "energy_scale": [1.0]
    }

    if args.grid and os.path.exists(args.grid):
        with open(args.grid, "r") as f:
            user_grid = json.load(f)
        grid.update(user_grid)

    solver = try_import_solver()

    rows = []
    best = []  # list of (J, params, metrics)
    for params in expand_grid(grid):
        try:
            resD   = run_case(solver, "D",   params)
            resH3  = run_case(solver, "H3",  params)
            resHe3 = run_case(solver, "He3", params)
            resHe4 = run_case(solver, "He4", params)
            J = objective(resD, resH3, resHe3, resHe4)
        except Exception as e:
            J = 1e12
            resD = resH3 = resHe3 = resHe4 = {"error": str(e)}

        row = {
            "J": J,
            **params,
            "E_D":   resD.get("binding_energy_MeV"),
            "E_H3":  resH3.get("binding_energy_MeV"),
            "E_He3": resHe3.get("binding_energy_MeV"),
            "E_He4": resHe4.get("binding_energy_MeV"),
            "edge_ok_D":   edge_order_ok(resD.get("edge_lengths_fm", {})),
            "edge_ok_H3":  edge_order_ok(resH3.get("edge_lengths_fm", {})),
            "edge_ok_He3": edge_order_ok(resHe3.get("edge_lengths_fm", {})),
            "edge_ok_He4": edge_order_ok(resHe4.get("edge_lengths_fm", {})),
            "rp_any":  resHe4.get("proton_charge_radius_fm", None),
            "rn2_any": resHe4.get("neutron_ms_radius_fm2", None),
        }
        rows.append(row)

        best.append((J, params, {"E_D": row["E_D"], "E_H3": row["E_H3"], "E_He3": row["E_He3"], "E_He4": row["E_He4"]}))
        best.sort(key=lambda t: t[0])
        best = best[:args.topk]

    # Write CSV
    with open(args.out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    # Write top-k JSON
    top = [{"J": J, "params": p, "energies": e} for (J, p, e) in best]
    with open(args.topk_json, "w") as f:
        json.dump(top, f, indent=2)

    print(f"[SCAN] Done. Wrote {args.out_csv} and {args.topk_json}.")
    if top:
        print("[SCAN] Best candidate:")
        print(json.dumps(top[0], indent=2))

if __name__ == "__main__":
    main()

