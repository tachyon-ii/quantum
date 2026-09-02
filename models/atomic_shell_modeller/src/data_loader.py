"""
data_loader.py - Data loading and management

Handles loading ground truth electron configurations from JSON.
Pure data access layer with no business logic.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from .atom import Atom


class DataLoader:
    """Loads and manages electron configuration data"""
    
    def __init__(self, data_file: Optional[str] = None):
        """
        Initialize DataLoader
        
        Args:
            data_file: Path to JSON data file. If None, uses default location.
        """
        if data_file is None:
            # Default to data/known_configurations.json relative to project root
            current_dir = Path(__file__).parent.parent
            self.data_file = current_dir / "data" / "known_configurations.json"
        else:
            self.data_file = Path(data_file)
        
        self._data = None
    
    def _load_data(self) -> Dict:
        """Load configuration data from JSON file"""
        if self._data is not None:
            return self._data
        
        try:
            with open(self.data_file, 'r') as f:
                self._data = json.load(f)
            return self._data
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.data_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def get_configurations(self) -> Dict[int, Dict]:
        """
        Get all electron configurations
        
        Returns:
            Dict mapping atomic number to configuration data
        """
        data = self._load_data()
        configs = {}
        
        for z_str, config_data in data["configurations"].items():
            z = int(z_str)
            configs[z] = config_data
        
        return configs
    
    def get_configuration(self, z: int) -> Optional[Dict]:
        """
        Get configuration for specific atomic number
        
        Args:
            z: Atomic number
            
        Returns:
            Configuration data or None if not found
        """
        configs = self.get_configurations()
        return configs.get(z)
    
    def get_metadata(self) -> Dict:
        """Get metadata about the configurations"""
        data = self._load_data()
        return data.get("metadata", {})
    
    def create_atom(self, z: int) -> Atom:
        """
        Create an Atom object for given atomic number
        
        Args:
            z: Atomic number
            
        Returns:
            Atom object with known configuration loaded
            
        Raises:
            ValueError: If atomic number not found in data
        """
        config_data = self.get_configuration(z)
        if config_data is None:
            raise ValueError(f"No configuration data found for Z={z}")
        
        return Atom(
            Z=z,
            symbol=config_data["symbol"],
            name=config_data.get("name", ""),
            known_config=config_data["config"]
        )
    
    def create_atoms(self, z_range: range) -> List[Atom]:
        """
        Create Atom objects for range of atomic numbers
        
        Args:
            z_range: Range of atomic numbers
            
        Returns:
            List of Atom objects
        """
        atoms = []
        configs = self.get_configurations()
        
        for z in z_range:
            if z in configs:
                atom = self.create_atom(z)
                atoms.append(atom)
            else:
                print(f"Warning: No data for Z={z}, skipping")
        
        return atoms
    
    def get_available_elements(self) -> List[int]:
        """Get list of available atomic numbers"""
        configs = self.get_configurations()
        return sorted(configs.keys())
    
    def get_shell_capacities(self) -> List[int]:
        """Get theoretical shell capacities from metadata"""
        metadata = self.get_metadata()
        return metadata.get("capacities", [2, 8, 18, 8, 8])
    
    def validate_data_integrity(self) -> List[str]:
        """
        Validate data integrity
        
        Returns:
            List of error messages, empty if all valid
        """
        errors = []
        configs = self.get_configurations()
        
        for z, config_data in configs.items():
            # Check required fields
            required_fields = ["symbol", "config"]
            for field in required_fields:
                if field not in config_data:
                    errors.append(f"Z={z}: Missing required field '{field}'")
            
            if "config" in config_data:
                config = config_data["config"]
                
                # Check configuration length
                if len(config) != 5:
                    errors.append(f"Z={z}: Config must have 5 shells, has {len(config)}")
                
                # Check electron count matches Z
                elif sum(config) != z:
                    errors.append(f"Z={z}: Electron count {sum(config)} != atomic number {z}")
                
                # Check non-negative electrons
                elif any(e < 0 for e in config):
                    errors.append(f"Z={z}: Negative electron count in config")
        
        return errors
    
    def summary(self) -> str:
        """Return summary of loaded data"""
        try:
            configs = self.get_configurations()
            metadata = self.get_metadata()
            
            min_z = min(configs.keys())
            max_z = max(configs.keys())
            total_elements = len(configs)
            
            return (f"Data Summary:\n"
                   f"  Elements: {total_elements} (Z={min_z} to Z={max_z})\n"
                   f"  Source: {metadata.get('source', 'Unknown')}\n"
                   f"  Shell capacities: {metadata.get('capacities', 'Unknown')}")
        
        except Exception as e:
            return f"Error loading data: {e}"