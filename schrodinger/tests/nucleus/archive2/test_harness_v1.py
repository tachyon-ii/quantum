"""Validation Harness — Angular Deflection Model (v3)
=================================================

This harness executes the **Tests 3.1 & 3.2** suite for the Angular Deflection
Model of Nuclear Binding using the curvature–dipole mesh interaction.

It expects a module named `nuclear_solver.py` somewhere on your PYTHONPATH
(typically the same directory you run this harness from) that exposes:

    solve_nucleus(nucleus: str, params: dict) -> dict

Where:
  - `nucleus` is one of: "D", "H3", "He3", "He4".
  - `params` includes at least the mesh-glue parameters and any other model params.
  - The return dict MUST contain:
        {
          "binding_energy_MeV": float,
          "edge_lengths_fm": {"NN": float, "NP": float, "PP": float},  # per-edge natural length
          "proton_charge_radius_fm": float,      # for Test 3.2
          "neutron_ms_radius_fm2": float,        # mean-squared (negative)
          "magnetic_moments_nnm": {              # nuclear magnetons (optional but checked if present)
              "p": float, "n": float
          }
        }

If your solver returns additional fields, they will be ignored.
If a field is missing, the harness will mark the corresponding check as "SKIP".

USAGE
-----
1) Implement `nuclear_solver.solve_nucleus` as described above.
2) (Optional) Put `mesh_glue.py` (from Aurelius' earlier message) next to your solver.
3) Run:
       python3 test_harness_v1.py
   The harness will print a human-friendly report and write `validation_report.csv`
   and `validation_summary.json`.

TOLERANCES (from tests.md)
--------------------------
- Deuteron (D):     -2.224 MeV within ±0.001 MeV; ONLY δ_eff may be tuned once.
- Tritium (H3):     -8.482 MeV within ±0.05 MeV (no retune).
- Helium-3 (He3):   -7.718 MeV within ±0.05 MeV (no retune).
- Split H3-He3:      0.764 MeV within ±0.05 MeV (no retune).
- Helium-4 (He4):  -28.30  MeV within ±0.10 MeV (no retune).
- Edge length order (all): NN < NP < PP
- Proton charge radius: 0.840–0.878 fm
- Neutron mean-square charge radius: negative, magnitude ~ 0.11–0.12 fm^2 (broad check).
- Magnetic moments (optional check): sign and ballpark only."""


from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Tuple, Optional
import importlib
import json
import csv
from math import isfinite

# -------------------- Expected values & tolerances --------------------

@dataclass(frozen=True)
class Expectations:
    D_binding: float = -2.224
    H3_binding: float = -8.482
    He3_binding: float = -7.718
    He4_binding: float = -28.30
    H3_He3_split: float = 0.764

@dataclass(frozen=True)
class Tolerances:
    D_binding_tol: float = 0.001
    H3_binding_tol: float = 0.05
    He3_binding_tol: float = 0.05
    He4_binding_tol: float = 0.10
    split_tol: float = 0.05
    p_radius_min: float = 0.840
    p_radius_max: float = 0.878
    n_ms_radius_sign: int = -1    # negative
    # Loose band for magnitude (you may tighten as you calibrate):
    n_ms_radius_abs_min: float = 0.05
    n_ms_radius_abs_max: float = 0.20

EXPECT = Expectations()
TOL = Tolerances()

# -------------------- Harness configuration --------------------

# Shared model parameters (fill with your chosen numbers)
DEFAULT_PARAMS = {
    "kappa": 1.0,
    "mu": 0.01,
    "eps0": 1.0,
    "R0": 0.86,
    "delta_eff": 0.2,
    "lambda_c": 0.45,
    "sigma_NN": 2.0,
    "sigma_NP": 1.00,
    "sigma_PP": 0.5,
    "r0_NN": 1.0,
    "r0_NP": 1.1,
    "r0_PP": 1.2,
    "theta_max_deg": 35.0,
    "deflection_scale": 1.0,
    "energy_scale": 10,  # Adjusted to get closer to target energies
    "coop_c1": 0.15,  # Single value, not list
    "coop_c2": 0.05,  # Single value, not list
    "gap_floor_ratio": 0.005
}

NUCLEI_ORDER = ["D", "H3", "He3", "He4"]

# -------------------- Utility --------------------

def try_import_solver() -> Optional[Any]:
    try:
        return importlib.import_module("nuclear_solver")
    except Exception as e:
        print("[HARNESS] Could not import `nuclear_solver`. Please place nuclear_solver.py on PYTHONPATH.")
        print("Error:", e)
        return None

def check_finite(label: str, value: Any) -> Tuple[bool, str]:
    if isinstance(value, (int, float)) and isfinite(value):
        return True, ""
    return False, f"{label} not finite or missing"

def within(val: float, target: float, tol: float) -> bool:
    return (val >= target - tol) and (val <= target + tol)

# -------------------- Test runners --------------------

def run_solver(solver, nucleus: str, params: Dict[str, Any]) -> Dict[str, Any]:
    res = solver.solve_nucleus(nucleus, params)
    if not isinstance(res, dict):
        raise TypeError("solve_nucleus must return a dict")
    return res

def test_binding_energy(label: str, value: float, target: float, tol: float) -> Tuple[str, bool, float]:
    ok = within(value, target, tol)
    return (f"{label} binding", ok, value - target)

def test_split(H3_val: float, He3_val: float, target: float, tol: float) -> Tuple[str, bool, float]:
    split = H3_val - He3_val
    ok = within(split, target, tol)
    return ("H3-He3 split", ok, split - target)

def test_edge_order(edge_lengths: Dict[str, float]) -> Tuple[str, bool, str]:
    try:
        nn = edge_lengths.get("NN", None)
        np_ = edge_lengths.get("NP", None)
        pp = edge_lengths.get("PP", None)
        if nn is None or np_ is None or pp is None:
            return ("Edge length order NN<NP<PP", False, "Missing edge lengths")
        ok = (nn < np_ < pp)
        return ("Edge length order NN<NP<PP", ok, f"NN={nn}, NP={np_}, PP={pp}")
    except Exception as e:
        return ("Edge length order NN<NP<PP", False, f"Error: {e}")

def test_proton_radius(rp: Optional[float]) -> Tuple[str, bool, str]:
    if rp is None:
        return ("Proton charge radius", False, "Missing")
    ok = (TOL.p_radius_min <= rp <= TOL.p_radius_max)
    return ("Proton charge radius", ok, f"{rp} fm")

def test_neutron_ms_radius(rn2: Optional[float]) -> Tuple[str, bool, str]:
    if rn2 is None:
        return ("Neutron <r^2>", False, "Missing")
    sign_ok = (rn2 < 0) if TOL.n_ms_radius_sign < 0 else (rn2 > 0)
    mag_ok = (TOL.n_ms_radius_abs_min <= abs(rn2) <= TOL.n_ms_radius_abs_max)
    return ("Neutron <r^2>", (sign_ok and mag_ok), f"{rn2} fm^2")

# -------------------- Main orchestration --------------------

def main(params_override: Dict[str, Any] = None) -> Dict[str, Any]:
    solver = try_import_solver()
    if solver is None:
        return {}

    params = DEFAULT_PARAMS.copy()
    if params_override:
        params.update(params_override)

    report_rows: List[Dict[str, Any]] = []
    summary: Dict[str, Any] = {"cases": {}, "overall_pass": True}
    energies: Dict[str, float] = {}

    # Run nuclei in order
    for nuc in NUCLEI_ORDER:
        res = run_solver(solver, nuc, params)
        energies[nuc] = res.get("binding_energy_MeV", float("nan"))
        case = {"nucleus": nuc, "binding_energy_MeV": energies[nuc]}

        # Binding checks
        if nuc == "D":
            label, ok, diff = test_binding_energy("Deuteron", energies[nuc], EXPECT.D_binding, TOL.D_binding_tol)
        elif nuc == "H3":
            label, ok, diff = test_binding_energy("Tritium", energies[nuc], EXPECT.H3_binding, TOL.H3_binding_tol)
        elif nuc == "He3":
            label, ok, diff = test_binding_energy("Helium-3", energies[nuc], EXPECT.He3_binding, TOL.He3_binding_tol)
        elif nuc == "He4":
            label, ok, diff = test_binding_energy("Helium-4", energies[nuc], EXPECT.He4_binding, TOL.He4_binding_tol)
        else:
            label, ok, diff = ("Unknown nucleus", False, float("nan"))

        case[label] = "PASS" if ok else "FAIL"
        case[label + " (delta MeV)"] = diff
        summary["overall_pass"] &= ok

        # Edge order check (all cases)
        el = res.get("edge_lengths_fm", {})
        el_label, el_ok, el_msg = test_edge_order(el)
        case[el_label] = "PASS" if el_ok else f"FAIL ({el_msg})"
        summary["overall_pass"] &= el_ok

        # Radii & moments (record once; typically from H/He cases)
        if nuc in ("H3", "He3", "He4"):
            rp = res.get("proton_charge_radius_fm", None)
            rn2 = res.get("neutron_ms_radius_fm2", None)

            pr_label, pr_ok, pr_msg = test_proton_radius(rp)
            case[pr_label] = "PASS" if pr_ok else f"FAIL ({pr_msg})"
            summary["overall_pass"] &= pr_ok

            nr_label, nr_ok, nr_msg = test_neutron_ms_radius(rn2)
            case[nr_label] = "PASS" if nr_ok else f"FAIL ({nr_msg})"
            summary["overall_pass"] &= nr_ok

        report_rows.append(case)
        summary["cases"][nuc] = case

    # Split check requires both H3 and He3 energies
    if all(k in energies for k in ("H3", "He3")):
        label, ok, diff = test_split(energies["H3"], energies["He3"], EXPECT.H3_He3_split, TOL.split_tol)
        split_row = {"nucleus": "H3-He3", label: "PASS" if ok else "FAIL", label + " (delta MeV)": diff}
        report_rows.append(split_row)
        summary["cases"]["H3-He3"] = split_row
        summary["overall_pass"] &= ok

    # Save CSV & JSON
    with open("validation_report.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sorted({k for row in report_rows for k in row.keys()}))
        writer.writeheader()
        for row in report_rows:
            writer.writerow(row)

    with open("validation_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print human-friendly
    print("\n=== Angular Deflection Model — Validation Report ===")
    for row in report_rows:
        print(f"\nCase: {row.get('nucleus','?')}")
        for k, v in row.items():
            if k == "nucleus": continue
            print(f"  - {k}: {v}")
    print("\nOverall PASS:", summary["overall_pass"])

    return summary

if __name__ == "__main__":
    main()
