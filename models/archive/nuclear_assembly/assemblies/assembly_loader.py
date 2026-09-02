# nuclear_assembly/assemblies/assembly_loader.py
"""
Load assemblies from JSON specifications.
"""

import json
import numpy as np
from typing import Dict, Any
from geometry.face_labeling import LabeledTetrahedron
from assemblies.d2 import D2Unit
from assemblies.he4 import He4Ring


class AssemblyLoader:
    """Load and create assemblies from JSON specifications."""
    
    @staticmethod
    def load_from_file(filepath: str):
        """Load an assembly from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return AssemblyLoader.create_from_spec(data)
    
    @staticmethod
    def create_from_spec(spec: Dict[str, Any]):
        """Create an assembly from a JSON specification."""
        assembly = spec.get('assembly', spec)
        name = assembly.get('name', '')
        
        # Determine assembly type from name or structure
        if 'D2' in name or len(assembly.get('parts', [])) == 2:
            return AssemblyLoader._create_d2(assembly)
        elif 'He4' in name or len(assembly.get('parts', [])) == 4:
            return AssemblyLoader._create_he4(assembly)
        else:
            return AssemblyLoader._create_generic(assembly)
    
    @staticmethod
    def _create_d2(spec: Dict[str, Any]) -> D2Unit:
        """Create D2 from specification."""
        # Create base D2 unit
        d2 = D2Unit()
        
        # Apply any specified transformations from the spec
        parts = spec.get('parts', [])
        if len(parts) >= 2:
            # Position from spec if available
            for part in parts:
                if part.get('species') == 'proton':
                    pos = part.get('pose', {}).get('position', [0, 0, 0])
                    # Could apply position if needed
                    
        # Apply bonds from spec
        bonds = spec.get('bonds', [])
        for bond in bonds:
            # The D2 is already created with the correct bond
            # but we could verify or modify based on spec
            if bond.get('alignment', {}).get('twist_deg', 0) != 0:
                # This confirms it's an H-H' configuration
                pass
                
        return d2
    
    @staticmethod
    def _create_he4(spec: Dict[str, Any]) -> He4Ring:
        """Create He4 from specification."""
        # Determine chirality from bonds
        bonds = spec.get('bonds', [])
        chirality = 'L'  # default
        
        for bond in bonds:
            twist = bond.get('alignment', {}).get('twist_deg', 0)
            if twist > 0:
                chirality = 'L'
                break
            elif twist < 0:
                chirality = 'R'
                break
        
        return He4Ring(chirality=chirality)
    
    @staticmethod
    def _create_generic(spec: Dict[str, Any]):
        """Create generic assembly from parts and bonds."""
        # This would be for more complex assemblies
        # For now, return the spec itself
        return spec
