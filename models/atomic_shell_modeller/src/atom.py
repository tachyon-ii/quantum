"""
atom.py - Atom class definition

Defines the Atom object that holds all data for a single element.
Clean data structure with no business logic.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Atom:
    """
    Holds all data for a single element.
    
    Attributes:
        Z (int): Atomic number
        symbol (str): Element symbol (H, He, Li, etc.)
        name (str): Full element name
        known_config (List[int]): Experimentally known electron configuration
        predicted_config (Optional[List[int]]): Theory-predicted configuration
        energy (Optional[float]): Total energy if calculated
        debug_info (Optional[Dict]): Debug information from theory calculation
        validation_result (Optional[Dict]): Results from validation comparison
    """
    Z: int
    symbol: str
    name: str = ""
    known_config: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    predicted_config: Optional[List[int]] = None
    energy: Optional[float] = None
    debug_info: Optional[Dict[str, Any]] = None
    validation_result: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate atom data after initialization"""
        if self.Z <= 0:
            raise ValueError(f"Atomic number must be positive, got {self.Z}")
        if len(self.known_config) != 5:
            raise ValueError(f"Configuration must have 5 shells, got {len(self.known_config)}")
        if sum(self.known_config) != self.Z:
            raise ValueError(f"Configuration electrons ({sum(self.known_config)}) != Z ({self.Z})")
    
    @property
    def total_electrons(self) -> int:
        """Total electrons in known configuration"""
        return sum(self.known_config)
    
    @property
    def predicted_total_electrons(self) -> int:
        """Total electrons in predicted configuration"""
        return sum(self.predicted_config) if self.predicted_config else 0
    
    @property
    def has_prediction(self) -> bool:
        """Whether atom has a predicted configuration"""
        return self.predicted_config is not None
    
    @property
    def is_validated(self) -> bool:
        """Whether atom has been validated"""
        return self.validation_result is not None
    
    def get_shell_electrons(self, shell_number: int, config_type: str = "known") -> int:
        """
        Get number of electrons in specific shell
        
        Args:
            shell_number (int): Shell number (1-5)
            config_type (str): "known" or "predicted"
        """
        if not (1 <= shell_number <= 5):
            raise ValueError(f"Shell number must be 1-5, got {shell_number}")
        
        if config_type == "known":
            return self.known_config[shell_number - 1]
        elif config_type == "predicted" and self.predicted_config:
            return self.predicted_config[shell_number - 1]
        else:
            return 0
    
    def summary(self) -> str:
        """Return a summary string of the atom"""
        pred_str = str(self.predicted_config) if self.predicted_config else "None"
        return f"{self.symbol}({self.Z}): Known={self.known_config}, Predicted={pred_str}"
    
    def __str__(self) -> str:
        return f"Atom({self.symbol}, Z={self.Z})"
    
    def __repr__(self) -> str:
        return f"Atom(Z={self.Z}, symbol='{self.symbol}', name='{self.name}')"