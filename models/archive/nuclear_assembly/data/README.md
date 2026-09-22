# Data Directory Structure

## Directories

- `schemas/`: JSON schema definitions and templates
- `samples/`: Sample configurations (D2, He4_L, He4_R, etc.)
- `configurations/`: User-created nuclear configurations
- `output/`: Generated output from simulations

## File Naming Convention

- D2 configurations: `D2_*.json`
- He4 configurations: `He4_[LR]_*.json`
- He3/H3 configurations: `He3_*.json`, `H3_*.json`
- Larger nuclei: `{element}{A}_*.json` (e.g., `Li6_*.json`)
