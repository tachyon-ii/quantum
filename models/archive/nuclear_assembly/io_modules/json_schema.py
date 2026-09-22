"""
JSON import/export for nuclear assemblies.
Compatible with the existing schema from tt_belt_stub.
"""

import json
import numpy as np
from typing import Dict, Any, List


class AssemblySerializer:
    """
    Serialize/deserialize nuclear assemblies to/from JSON.
    """
    
    @staticmethod
    def export_assembly(assembly: Dict, filename: str = None) -> str:
        """
        Export assembly to JSON string or file.
        
        Args:
            assembly: Assembly dictionary
            filename: Optional output filename
            
        Returns:
            JSON string
        """
        # Convert numpy arrays to lists
        json_safe = AssemblySerializer._make_json_safe(assembly)
        
        # Create schema-compliant structure
        output = {
            "assembly": {
                "name": json_safe.get('name', 'unnamed'),
                "units": {"edge_a": 1.0},
                "parts": AssemblySerializer._export_parts(json_safe),
                "bonds": AssemblySerializer._export_bonds(json_safe),
                "meta": {
                    "description": json_safe.get('description', ''),
                    "u_hat": [0, 0, 1]
                }
            }
        }
        
        # Add chirality if present
        if 'chirality' in json_safe:
            output['assembly']['chirality'] = json_safe['chirality']
        
        json_str = json.dumps(output, indent=2)
        
        if filename:
            with open(filename, 'w') as f:
                f.write(json_str)
        
        return json_str
    
    @staticmethod
    def import_assembly(source: str) -> Dict:
        """
        Import assembly from JSON string or file.
        
        Args:
            source: JSON string or filename
            
        Returns:
            Assembly dictionary
        """
        # Check if source is filename or JSON string
        if source.strip().startswith('{'):
            data = json.loads(source)
        else:
            with open(source, 'r') as f:
                data = json.load(f)
        
        # Extract assembly
        if 'assembly' in data:
            assembly = data['assembly']
        else:
            assembly = data
        
        # Convert to internal format
        return {
            'name': assembly.get('name', 'unnamed'),
            'parts': AssemblySerializer._import_parts(assembly.get('parts', [])),
            'bonds': AssemblySerializer._import_bonds(assembly.get('bonds', [])),
            'meta': assembly.get('meta', {})
        }
    
    @staticmethod
    def _make_json_safe(obj: Any) -> Any:
        """Convert numpy arrays to lists recursively."""
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: AssemblySerializer._make_json_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [AssemblySerializer._make_json_safe(item) for item in obj]
        else:
            return obj
    
    @staticmethod
    def _export_parts(assembly: Dict) -> List[Dict]:
        """Export parts in schema format."""
        parts = []
        part_id = 1
        
        for component_type, component in assembly.get('components', []):
            if component_type == 'D2':
                # Export D2 as two parts
                parts.append({
                    "id": f"p{part_id}",
                    "species": "proton",
                    "pose": {
                        "position": component.get('proton', {}).get('position', [0, 0, 0]),
                        "orientation": {"quat": [1, 0, 0, 0]}
                    }
                })
                parts.append({
                    "id": f"n{part_id}",
                    "species": "neutron",
                    "pose": {
                        "position": component.get('neutron', {}).get('position', [0, 0, 0]),
                        "orientation": {"quat": [1, 0, 0, 0]}
                    }
                })
                part_id += 1
            elif component_type in ['proton', 'neutron']:
                parts.append({
                    "id": f"{component_type[0]}{part_id}",
                    "species": component_type,
                    "pose": {
                        "position": [0, 0, 0],
                        "orientation": {"quat": [1, 0, 0, 0]}
                    }
                })
                part_id += 1
        
        return parts
    
    @staticmethod
    def _export_bonds(assembly: Dict) -> List[Dict]:
        """Export bonds in schema format."""
        bonds = []
        
        for bond in assembly.get('bonds', []):
            bonds.append({
                "type": bond.get('type', 'HT'),
                "from": {
                    "part": bond.get('from', [None, None])[0],
                    "face": bond.get('from', [None, None])[1]
                },
                "to": {
                    "part": bond.get('to', [None, None])[0],
                    "face": bond.get('to', [None, None])[1]
                },
                "alignment": {
                    "coaxial": True,
                    "twist_deg": bond.get('twist', 0)
                },
                "routing": {
                    "layer": "outer",
                    "belt_k": bond.get('k', 2)
                }
            })
        
        return bonds
    
    @staticmethod
    def _import_parts(parts: List[Dict]) -> List[Dict]:
        """Import parts from schema format."""
        return parts  # For now, pass through
    
    @staticmethod
    def _import_bonds(bonds: List[Dict]) -> List[Dict]:
        """Import bonds from schema format."""
        imported = []
        
        for bond in bonds:
            imported.append({
                'type': bond.get('type', 'HT'),
                'from': (
                    bond.get('from', {}).get('part'),
                    bond.get('from', {}).get('face')
                ),
                'to': (
                    bond.get('to', {}).get('part'),
                    bond.get('to', {}).get('face')
                ),
                'twist': bond.get('alignment', {}).get('twist_deg', 0),
                'k': bond.get('routing', {}).get('belt_k', 2)
            })
        
        return imported
