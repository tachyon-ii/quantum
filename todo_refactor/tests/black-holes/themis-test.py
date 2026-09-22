#!/usr/bin/env python3
"""
themis_check.py — minimal smoke test for a Themis install.

- Verifies import of the 'themis' package
- Prints version (if available) and lists a few top-level attributes
- Tries to import a handful of typical submodules, reporting success/failure
- Prints basic environment info (Python, NumPy)

Run:  python3 themis_check.py
"""

import sys
import platform
import importlib

def dotted(modname):
    try:
        m = importlib.import_module(modname)
        return True, m
    except Exception as e:
        return False, e

def maybe_attr(obj, *names, default="<not present>"):
    for n in names:
        if hasattr(obj, n):
            try:
                return getattr(obj, n)
            except Exception:
                pass
    return default

def main():
    print("="*60)
    print("THEMIS SMOKE TEST")
    print("="*60)
    print(f"Python  : {platform.python_version()}  ({sys.executable})")
    try:
        import numpy as np
        print(f"NumPy   : {np.__version__}")
    except Exception as e:
        print(f"NumPy   : import failed ({e})")

    ok, themis = dotted("themis")
    if not ok:
        print("\nThemis  : import FAILED")
        print("Error   :", themis)
        print("\nTips:")
        print("  • If you installed in a virtualenv/conda env, make sure it’s active.")
        print("  • Try:  pip show themis   or   python -m pip install themis")
        sys.exit(1)

    print("\nThemis  : import OK")
    ver = maybe_attr(themis, "__version__", "version", default="<unknown>")
    print("Version :", ver)

    # Show a few top-level names (truncate for readability)
    names = sorted([n for n in dir(themis) if not n.startswith("_")])
    show = ", ".join(names[:12]) + (" …" if len(names) > 12 else "")
    print("Top-level attributes:", show or "<none>")

    # Probe common submodules without failing the script
    probes = [
        "themis.model",      # sometimes 'model' or 'models'
        "themis.models",
        "themis.likelihood", # likelihood machinery
        "themis.priors",     # priors/parameters
        "themis.sampler",    # samplers/inference
        "ehtim"              # EHT imaging toolkit (optional but handy)
    ]
    print("\nSubmodule probes:")
    for mod in probes:
        ok, obj = dotted(mod)
        tag = "OK" if ok else "missing"
        print(f"  {mod:<20} : {tag}")

    print("\n✅ Themis appears importable. You’re ready to try a simple vis-domain fit.")
    print("   Next step suggestion:")
    print("     • Install 'themis' extras and 'eht-imaging' if you haven’t already")
    print("     • Pull M87* 2017 visibilities and run a parametric ring fit in the")
    print("       visibility domain (GR ring vs. GR ring × exponential envelope).")
    print("="*60)

if __name__ == "__main__":
    main()

