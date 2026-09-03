"""
General assembly builder for creating nuclei from components.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from .d2 import D2Unit
from .he4 import He4Ring
from geometry.face_labeling import LabeledTetrahedron


class NuclearBuilder:
    """
    Builder for assembling nuclei from D2 units and single tetrahedra.
    """
    
    def __init__(self):
        """Initialize builder with component library."""
        self.components = []
        self.bonds = []
        
    def add_d2(self, position: np.ndarray = None) -> D2Unit:
        """Add a D2 unit to the assembly."""
        d2 = D2Unit(position=position)
        self.components.append(('D2', d2))
        return d2
    
    def add_neutron(self, position: np.ndarray = None) -> LabeledTetrahedron:
        """Add a single neutron tetrahedron."""
        neutron = LabeledTetrahedron()
        if position is not None:
            neutron.vertices += position
        self.components.append(('neutron', neutron))
        return neutron
    
    def add_proton(self, position: np.ndarray = None) -> LabeledTetrahedron:
        """Add a single proton tetrahedron (only for He3)."""
        proton = LabeledTetrahedron()
        if position is not None:
            proton.vertices += position
        self.components.append(('proton', proton))
        return proton
    
    def bond_ht(self, 
                component1: Tuple[object, str],
                component2: Tuple[object, str],
                twist: float = 0):
        """
        Create H-T bond between two components.
        
        Args:
            component1: (component, face_label) for H face
            component2: (component, face_label) for T face
            twist: Optional twist angle in degrees
        """
        obj1, face1 = component1
        obj2, face2 = component2
        
        # Validate faces
        if not (face1.startswith('H') and face2.startswith('T')):
            raise ValueError("Must bond H face to T face")
        
        # Store bond
        self.bonds.append({
            'type': 'HT',
            'from': (obj1, face1),
            'to': (obj2, face2),
            'twist': twist
        })
    
    def build_nucleus(self, Z: int, N: int) -> Dict:
        """
        Build a specific nucleus.
        
        Args:
            Z: Number of protons
            N: Number of neutrons
            
        Returns:
            Assembly dictionary
        """
        A = Z + N
        
        # Clear previous build
        self.components = []
        self.bonds = []
        
        # Build based on N-Z difference
        if N == Z:
            # Pure D2 stacking
            return self._build_symmetric(Z)
        elif N == Z + 1:
            # D2 stack + 1 neutron
            base = self._build_symmetric(Z)
            self.add_neutron()
            # Bond neutron to available site
            return self._finalize_assembly(f"{A}{self._element_symbol(Z)}")
        elif N == Z - 1:
            # Only He3 case
            if Z == 2:
                d2 = self.add_d2()
                proton = self.add_proton()
                # Bond extra proton
                return self._finalize_assembly("He3")
        else:
            raise NotImplementedError(f"Configuration Z={Z}, N={N} not yet implemented")
    
    def _build_symmetric(self, n_d2: int) -> Dict:
        """Build symmetric nucleus from D2 units."""
        if n_d2 == 1:
            # Deuterium
            self.add_d2()
        elif n_d2 == 2:
            # He4
            he4 = He4Ring()
            self.components.append(('He4', he4))
        elif n_d2 == 3:
            # Li6 - needs implementation
            raise NotImplementedError("Li6 assembly not yet implemented")
        else:
            raise NotImplementedError(f"Symmetric assembly for {n_d2} D2 units not implemented")
        
        return self._finalize_assembly(f"{2*n_d2}{self._element_symbol(n_d2)}")
    
    def _element_symbol(self, Z: int) -> str:
        """Get element symbol from proton number."""
        symbols = ['n', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne']
        return symbols[Z] if Z < len(symbols) else f"Z{Z}"
    
    def _finalize_assembly(self, name: str) -> Dict:
        """Create final assembly dictionary."""
        return {
            'name': name,
            'components': [(typ, comp.to_dict() if hasattr(comp, 'to_dict') else str(comp)) 
                          for typ, comp in self.components],
            'bonds': self.bonds,
            'n_components': len(self.components),
            'n_bonds': len(self.bonds)
        }
