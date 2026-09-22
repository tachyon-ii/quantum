# Nuclear Assembly

Clean implementation of nuclear binding models using truncated tetrahedron geometry.

## Structure

- `geometry/`: Base geometric structures and constants
- `assemblies/`: D2, He4, and general nuclear assemblies  
- `scoring/`: Belt energy calculations
- `io/`: JSON import/export and visualization

## Usage

```python
from assemblies.d2 import D2Unit
from assemblies.he4 import He4Ring

# Create deuterium
d2 = D2Unit()

# Create He4 with left chirality
he4 = He4Ring(chirality='L')
