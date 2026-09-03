"""
modeller.py - Main simulation engine

Orchestrates the modeling process by coordinating data loading,
theory application, and result collection. Pure orchestration logic.
"""

from typing import List, Optional, Dict, Any
from .atom import Atom
from .data_loader import DataLoader
from .theory import TheoryBase, create_theory


class AtomicModeller:
    """
    Main simulation engine that orchestrates the modeling process
    
    Responsibilities:
    - Load atoms from data
    - Apply theory to predict configurations
    - Collect results and debug information
    - Coordinate between components
    """
    
    def __init__(self, theory_name: str = "freeman", theory_kwargs: Optional[Dict] = None):
        """
        Initialize modeller with specified theory
        
        Args:
            theory_name: Name of theory to use
            theory_kwargs: Parameters to pass to theory constructor
        """
        self.theory_name = theory_name
        self.theory_kwargs = theory_kwargs or {}
        self.theory = create_theory(theory_name, **self.theory_kwargs)
        self.data_loader = DataLoader()
        
        self.atoms: List[Atom] = []
        self.modeling_complete = False
        
        print(f"AtomicModeller initialized:")
        print(f"  Theory: {theory_name}")
        print(f"  Theory class: {self.theory.__class__.__name__}")
        if theory_kwargs:
            print(f"  Theory parameters: {theory_kwargs}")
    
    def load_atoms(self, z_range: range) -> List[Atom]:
        """
        Load atoms for given atomic number range
        
        Args:
            z_range: Range of atomic numbers to load
            
        Returns:
            List of loaded Atom objects
        """
        print(f"Loading atoms for Z={z_range.start} to {z_range.stop-1}")
        
        self.atoms = self.data_loader.create_atoms(z_range)
        
        print(f"Loaded {len(self.atoms)} atoms")
        available_z = [atom.Z for atom in self.atoms]
        print(f"Available Z values: {sorted(available_z)}")
        
        return self.atoms
    
    def predict_configurations(self, atoms: Optional[List[Atom]] = None, verbose: bool = True) -> List[Atom]:
        """
        Apply theory to predict electron configurations
        
        Args:
            atoms: Atoms to process (uses self.atoms if None)
            verbose: Whether to print detailed progress
            
        Returns:
            List of atoms with predictions added
        """
        if atoms is None:
            atoms = self.atoms
        
        if not atoms:
            raise ValueError("No atoms to process. Call load_atoms() first.")
        
        print(f"\nPredicting configurations using {self.theory_name} theory:")
        print("=" * 60)
        
        for atom in atoms:
            if verbose:
                print(f"\n{atom.symbol} (Z={atom.Z}):")
            
            try:
                predicted_config, debug_info = self.theory.predict_configuration(atom.Z)
                
                atom.predicted_config = predicted_config
                atom.debug_info = debug_info
                
                if verbose:
                    print(f"  Known:     {atom.known_config}")
                    print(f"  Predicted: {predicted_config}")
                    
                    # Show validation errors if any
                    if "violations" in debug_info and debug_info["violations"]:
                        print(f"  Violations: {debug_info['violations']}")
            
            except Exception as e:
                print(f"  ERROR: {e}")
                atom.debug_info = {"error": str(e)}
        
        self.modeling_complete = True
        return atoms
    
    def run_modeling(self, z_range: range, verbose: bool = True) -> List[Atom]:
        """
        Complete modeling workflow: load data + predict configurations
        
        Args:
            z_range: Range of atomic numbers to model
            verbose: Whether to print detailed progress
            
        Returns:
            List of atoms with predictions
        """
        print(f"Starting complete modeling workflow:")
        print(f"  Range: Z={z_range.start} to {z_range.stop-1}")
        print(f"  Theory: {self.theory_name}")
        print()
        
        # Step 1: Load atoms
        atoms = self.load_atoms(z_range)
        
        # Step 2: Predict configurations
        atoms = self.predict_configurations(atoms, verbose=verbose)
        
        print(f"\nModeling complete: {len(atoms)} atoms processed")
        return atoms
    
    def get_theory_info(self) -> Dict[str, Any]:
        """Get information about the current theory"""
        return {
            "name": self.theory_name,
            "class": self.theory.__class__.__name__,
            "parameters": self.theory_kwargs,
            "shell_capacities": self.theory.get_shell_capacities()
        }
    
    def get_modeling_summary(self) -> Dict[str, Any]:
        """Get summary of modeling results"""
        if not self.modeling_complete:
            return {"status": "modeling not complete"}
        
        total_atoms = len(self.atoms)
        atoms_with_predictions = sum(1 for atom in self.atoms if atom.predicted_config is not None)
        atoms_with_errors = sum(1 for atom in self.atoms if atom.debug_info and "error" in atom.debug_info)
        
        z_values = [atom.Z for atom in self.atoms]
        min_z = min(z_values) if z_values else 0
        max_z = max(z_values) if z_values else 0
        
        return {
            "status": "complete",
            "total_atoms": total_atoms,
            "atoms_with_predictions": atoms_with_predictions,
            "atoms_with_errors": atoms_with_errors,
            "z_range": (min_z, max_z),
            "theory_info": self.get_theory_info()
        }
    
    def reset(self):
        """Reset modeller state"""
        self.atoms = []
        self.modeling_complete = False
        print("Modeller reset")
    
    def change_theory(self, theory_name: str, theory_kwargs: Optional[Dict] = None):
        """
        Change the theory used by the modeller
        
        Args:
            theory_name: New theory name
            theory_kwargs: New theory parameters
        """
        old_theory = self.theory_name
        self.theory_name = theory_name
        self.theory_kwargs = theory_kwargs or {}
        self.theory = create_theory(theory_name, **self.theory_kwargs)
        
        # Reset predictions since we changed theory
        for atom in self.atoms:
            atom.predicted_config = None
            atom.debug_info = None
        
        self.modeling_complete = False
        
        print(f"Theory changed: {old_theory} → {theory_name}")
        print(f"Existing predictions cleared")