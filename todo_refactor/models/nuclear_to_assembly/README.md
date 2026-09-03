# Nuclear Assembly Framework


Advanced truncated-octahedron (Kelvin cell) nuclear modeling framework with comprehensive assembly generation, scoring, and analysis capabilities for light nuclei.

## 🚀 Features

### **Nuclear Assembly Support**
- **Complete nuclear suite**: D-2, H-3, He-3, He-4, Li-7, C-12, O-16
- **Multiple variants per nucleus**: Linear, ring, layered, cluster, tetrahedral configurations
- **Automated optimization**: Systematic configuration generation and scoring
- **Phase validation**: A↔B alternation rules with zero-violation assemblies

### **Advanced Scoring System**
- **Channel counting**: NP, PP, NN bond analysis
- **Brickwork mechanics**: Orthogonal links, shear penalties, curvature analysis  
- **Phase rules**: Automated validation of physical constraints
- **Distance validation**: D_SS (2.8284) and D_HH (2.4495) bond length verification

### **Visualization & Analysis**
- **2D/3D visualization**: matplotlib and trimesh support
- **Interactive 3D viewer**: Real-time assembly exploration
- **Comparative analysis**: Multi-assembly scoring and ranking
- **JSON export/import**: Complete assembly serialization

## 📦 Installation
Geometric nuclear assembly modeling using truncated octahedron (Kelvin cell) nucleon representation with automated bond discovery and comprehensive scoring.

## Overview

This package models atomic nuclei as assemblies of nucleons represented as truncated octahedra. Each nucleon has 14 faces (6 squares, 8 hexagons) that can form bonds. The system automatically discovers all geometric bonds and analyzes edge constraints to understand nuclear binding.

## Installation

```bash
# Clone repository
git clone <repository-url>
cd nuclear_to_assembly

# Install in editable mode
pip install -e .
```

## 🎯 Quick Start

### Basic Assembly Building
```bash
# Simple nuclei
toasm build d2 -o deuterium.json                    # D-2 (default S-S)
toasm build he4 --variant cross -o helium4.json     # He-4 cross formation
toasm build li7 --variant linear -o lithium7.json   # Li-7 linear chain

# Complex nuclei with variants
toasm build c12 --variant tetrahedral -o c12_tetra.json    # C-12 tetrahedral
toasm build c12 --variant layered -o c12_layered.json      # C-12 layered  
toasm build c12 --variant alpha -o c12_alpha.json          # C-12 alpha clusters

toasm build o16 --variant layered_cube -o o16_cube.json    # O-16 layered cube
toasm build o16 --variant alpha_tetrahedral -o o16_alpha.json  # O-16 alpha tetrahedral
```

### Automated Generation
```bash
# Find optimal configuration for any nucleus
toasm auto 7 3 --best-only -o li7_optimal.json      # Li-7 (A=7, Z=3)
toasm auto 12 6 --max-results 3 -o c12_configs      # Top 3 C-12 configs
toasm auto 16 8 --best-only -o o16_optimal.json     # O-16 optimal
```

### Scoring & Analysis
```bash
# Score individual assemblies
toasm score c12_tetrahedral.json
toasm score o16_layered_cube.json

# Compare multiple assemblies  
toasm compare c12_*.json o16_*.json

# Output example:
# Assembly                  | NP   | PP   | NN   | Orth | Phase | Score
# c12_tetrahedral          | 6    | 2    | 2    | 16   | 0     | 239.1
# c12_layered              | 20   | 0    | 0    | 132  | 0     | 1720.0
# o16_layered_cube         | 28   | 0    | 0    | 256  | 0     | 3120.0
```

### Visualization
```bash
# 2D plots  
toasm viz assembly.json --out image.png --title "C-12 Tetrahedral"

# Interactive 3D viewer
toasm viz3d assembly.json
```

## 🔬 Supported Nuclear Configurations

| Nucleus | Mass (A) | Protons (Z) | Available Variants | Best Score | Status |
|---------|----------|-------------|-------------------|------------|---------|
| **D-2**   | 2 | 1 | S_S | 70.0 | ✅ Complete |
| **H-3**   | 3 | 1 | orth, linear | 100.0 | ✅ Complete |
| **He-3**  | 3 | 2 | orth, linear | 100.0 | ✅ Complete |
| **He-4**  | 4 | 2 | cross, ring | 155.0 | ✅ Complete |
| **Li-7**  | 7 | 3 | linear, compact, ring | 135.0 | ✅ Complete |
| **C-12**  | 12 | 6 | tetrahedral, layered, alpha | 1720.0 | ✅ Complete |
| **O-16**  | 16 | 8 | double_cube, spherical, alpha_tetrahedral, layered_cube | 3120.0 | ✅ Complete |

### Configuration Highlights

**C-12 Assemblies (All 0 phase violations):**
- **Tetrahedral**: 239.1 score - Compact 4-vertex clusters, mixed S-S/H-H bonds
- **Layered**: 1720.0 score - 3 layers × 4 nucleons, pure S-S bonds, highest connectivity  
- **Alpha Cluster**: 613.65 score - 3 He-4 clusters in triangular arrangement

**O-16 Assemblies (All 0 phase violations):**
- **Layered Cube**: 3120.0 score - 4 layers × 4 nucleons, maximum orthogonal links
- **Alpha Tetrahedral**: 1038.2 score - 4 He-4 clusters in tetrahedral geometry
- **Double Cube**: 1560.0 score - 8 layers × 2 nucleons, simple stacking
- **Spherical**: 5.0 score - Central core + shells, minimal connectivity

## 🛠️ Advanced Usage

### Automated Generator API
```python
from nuclear_to_assembly.assemblies.automated_generator import AutomatedGenerator

generator = AutomatedGenerator()

# Generate all configurations for C-12
results = generator.generate_all_configurations(A=12, Z=6)

# Find single best configuration  
best = generator.find_best_configuration(A=16, Z=8)
print(f"Best O-16 config: {best.assembly.name} (score: {best.total_score})")

# Validate existing assembly
validation = generator.validate_assembly_file("assembly.json")
```

### Custom Assembly Building
```python
from nuclear_to_assembly.assemblies.c12 import build_c12_tetrahedral
from nuclear_to_assembly.assemblies.o16 import build_o16_layered_cube

# Build specific configurations
c12 = build_c12_tetrahedral("Custom_C12")
o16 = build_o16_layered_cube("Custom_O16")

# Access assembly data
print(f"C-12 nucleons: {len(c12.nucleons)}")
print(f"C-12 bonds: {len(c12.bonds)}")
```

## 📊 Scoring System

### Channel Scoring
- **NP bonds**: +20 points each (favored)
- **PP/NN bonds**: -10 points each (penalized)
- **S-S vs H-H**: Tracked separately for analysis

### Structural Scoring  
- **Orthogonal links**: +10 points each
- **Shear penalty**: -5 points each
- **Curvature penalty**: -3 points each

### Validation Scoring
- **Phase violations**: -50 points each
- **Distance violations**: -100 points each  
- **Perfect geometry bonus**: +50 points

## 🔍 Technical Details

### Geometric Constraints
- **D_SS distance**: 2.8284 (square-square face bonds)
- **D_HH distance**: 2.4495 (hexagon-hexagon face bonds)
- **Phase alternation**: A↔B across all bonds
- **Truncated octahedron**: 6 square + 8 hexagonal faces per nucleon

### File Formats
```json
{
  "name": "Assembly_Name",
  "nucleons": [
    {
      "id": "P1",
      "kind": "proton", 
      "R": [[1,0,0], [0,1,0], [0,0,1]],
      "t": [0.0, 0.0, 0.0],
```

## Usage

### Building Nuclei

Build nuclei from the library and save as JSON with complete bond discovery:

```bash
# Build various nuclei configurations
toasm build d2 -o d2.json
toasm build h3_linear -o h3_linear.json
toasm build h3_orth -o h3_orth.json
toasm build he3_linear -o he3_linear.json
toasm build he3_orth -o he3_orth.json
toasm build he4_cross -o he4_cross.json
toasm build he4_ring -o he4_ring.json

# Output automatically saves to [nucleus_name].json if -o not specified
toasm build he4_cross  # Creates he4_cross.json
```

### Scoring Assemblies

Analyze geometric features and bond characteristics:

```bash
toasm score he4_cross.json
```

Outputs comprehensive scoring including:
- Bond counts by type (S-S, H-H)
- Channel analysis (N-P, P-P, N-N)
- Edge constraint classification (unconstrained/single/double)
- Topology features (closed loops, surface vs interior nucleons)
- Phase rail validation

### Visualization

Static 3D visualization with matplotlib:

```bash
toasm viz he4_cross.json --out he4_cross.png
toasm viz he4_cross.json --title "He-4 Cross Configuration"
```

Interactive 3D viewer with trimesh:

```bash
toasm viz3d he4_cross.json
```

## Assembly Definition Format

Assemblies are defined in `assemblies/library.py` using minimal constraint specifications. Each constraint is a tuple:

```python
(id1, face1, id2, face2, angle)
```

Where:
- **id1, id2**: Nucleon identifiers (N# for neutron, P# for proton)
- **face1, face2**: Face identifiers (e.g., "S+X", "H+++")
- **angle**: Rotation angle
  - For S-S bonds: Always 0 (no rotational significance)
  - For H-H bonds: "A" or "B" (phase alignment)

### Constraint Rules

1. **First constraint**: Creates both nucleons (N1 at origin, P1 positioned relative)
2. **Subsequent constraints**: At least one nucleon must already exist
3. **Sequential building**: Each constraint positions one new nucleon relative to an existing one

### Example Definition

```python
"he4_cross": [
    ("N1", "S+X", "P1", "S-X", 0),      # Create N1 and P1 with S-S bond
    ("N1", "H+++", "P2", "H---", "A"),  # Add P2 bonded to N1 via H-H
    ("P1", "H--+", "N2", "H++-", "A")   # Add N2 bonded to P1 via H-H
]
```

## Architecture

### Core Components

- **assemblies/library.py**: Minimal constraint definitions for each nucleus
- **assemblies/builder.py**: Constructs assemblies from constraints, automatically discovers all bonds
- **scoring/comprehensive.py**: Extracts geometric features for binding energy analysis
- **scoring/score.py**: Coordinates all scoring functions
- **cli/toasm.py**: Command-line interface orchestration

### Data Flow

1. **Build**: Library → Assembly → Bond Discovery → JSON
2. **Score**: JSON → Assembly Reconstruction → Feature Extraction
3. **Visualize**: JSON → 3D Rendering

## Available Nuclei

| Nucleus | Variants | Description |
|---------|----------|-------------|
| d2 | - | Deuteron (1n, 1p) |
| h3 | linear, orth | Tritium (2n, 1p) |
| he3 | linear, orth | Helium-3 (1n, 2p) |
| he4 | cross, ring | Helium-4 (2n, 2p) |

## Key Features

### Automatic Bond Discovery
The system finds all geometric bonds based on:
- Center-to-center distance matching D_SS (2√2) or D_HH (√6)
- Face normal alignment
- Automatic port addition for discovered bonds

### Edge Constraint Analysis
Classifies all 36 edges per nucleon:
- **Unconstrained (0)**: No neighbors, remains spherical
- **Singly constrained (1)**: One neighbor forces edge formation
- **Doubly constrained (2)**: Two neighbors create rigid edge

### Phase System
Tracks A/B phase alternation for hex faces:
- Phase A: Edges align with square face positions
- Phase B: Edges align with hex face positions (60° rotation)

## Theory

The model represents nucleons as truncated octahedra that deform under compression. Edge constraints emerge from neighboring nucleons, creating the "edge zipper" effect that contributes to nuclear binding.

### Binding Energy Components

1. **Face-to-face bonds**: Weak baseline interaction
2. **Edge constraints**: Strong contribution from forced edge formation
3. **Relativistic effects**: Enhanced binding in closed loops (H3/He3 transition)

### Geometric Transitions

- **D2**: Two spheres touching, minimal edge formation
- **H3/He3**: First closed loop, edge constraints begin
- **He4**: Multiple constraint types, complex edge network

## JSON Format

Assemblies are stored with complete geometric information:

```json
{
  "name": "he4_cross",
  "nucleons": [
    {
      "id": "N1",
      "kind": "neutron",
      "R": [[1,0,0],[0,1,0],[0,0,1]],
      "t": [0,0,0],
      "ports": [{"face": "S+X", "phase": "A"}]
    }
  ],
  "bonds": [
    {"n1": "P1", "face1": "S+X", "n2": "N1", "face2": "S-X"}
    {"n1": "N1", "face1": "S+X", "n2": "P1", "face2": "S-X"}
  ]
}
```

## 🎮 CLI Reference

### Commands
- `toasm build <nucleus>` - Build nuclear assembly
- `toasm auto <A> <Z>` - Automated generation  
- `toasm score <file>` - Score assembly
- `toasm compare <files...>` - Compare assemblies
- `toasm viz <file>` - 2D visualization
- `toasm viz3d <file>` - 3D interactive viewer

### Options
- `--variant <name>` - Choose specific variant
- `--output/-o <file>` - Output file
- `--best-only` - Generate only best configuration
- `--max-results <n>` - Limit number of results

## 🧪 Example Results

### Li-7 Linear Assembly
```bash
$ toasm build li7 --variant linear -o li7.json && toasm score li7.json
{
  "channels": {"NP": 6, "PP": 0, "NN": 0},
  "brickwork": {"orthogonal_links": 12, "shear_penalty": 0},
  "phase": {"bad_phase_bonds": 0},
  "total_score": 240.0
}
```

### C-12 Comparison
```bash
$ toasm compare c12_*.json
Assembly                  | NP   | PP   | NN   | Orth | Phase | Score
c12_tetrahedral          | 6    | 2    | 2    | 16   | 0     | 239.1
c12_layered              | 20   | 0    | 0    | 132  | 0     | 1720.0  
c12_alpha                | 15   | 0    | 0    | 36   | 0     | 613.7
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-nucleus`)
3. Add nucleus builders in `nuclear_to_assembly/assemblies/`
4. Update CLI in `nuclear_to_assembly/cli/toasm.py`
5. Add tests and documentation
6. Submit pull request

## 📈 Recent Major Updates

### Version 2.0 Features
- ✅ **Complete nuclear suite**: Added Li-7, C-12, O-16 with multiple variants each
- ✅ **Automated generation**: Systematic configuration discovery and optimization  
- ✅ **Advanced scoring**: Multi-factor scoring with validation and penalties
- ✅ **Zero phase violations**: All assemblies achieve perfect A↔B alternation
- ✅ **Distance validation**: Automatic geometric constraint verification
- ✅ **Enhanced CLI**: Comprehensive commands for building, scoring, comparison
- ✅ **3D visualization**: Interactive trimesh viewer and 2D matplotlib plots

### Performance Highlights
- **Li-7**: 3 variants, 0 phase violations, scores 90-135
- **C-12**: 3 variants, 0 phase violations, scores 239-1720  
- **O-16**: 4 variants, 0 phase violations, scores 5-3120
- **Automated generator**: Handles A=2-16, finds optimal configurations

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

Built for advanced nuclear physics modeling using truncated octahedron geometric constraints and phase alternation rules.
