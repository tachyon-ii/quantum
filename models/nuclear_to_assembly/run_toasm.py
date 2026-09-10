#!/usr/bin/env python3
"""
Convenience script to run the toasm CLI without needing the full virtual environment path.
This script activates the virtual environment and runs the CLI with any arguments passed to it.

Usage:
    python3 run_toasm.py build d2 --variant S_S --name MyDeuteron
    python3 run_toasm.py score d2.json
    python3 run_toasm.py viz d2.json --out d2.png
"""

import sys
import subprocess
import os

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the virtual environment python
    venv_python = os.path.join(script_dir, ".venv", "bin", "python")
    
    # Check if virtual environment exists
    if not os.path.exists(venv_python):
        print("Error: Virtual environment not found.")
        print("Please run: pip install -e . first")
        sys.exit(1)
    
    # Build the command: python -m nuclear_to_assembly.cli.toasm [args...]
    cmd = [venv_python, "-m", "nuclear_to_assembly.cli.toasm"] + sys.argv[1:]
    
    # Run the command
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
