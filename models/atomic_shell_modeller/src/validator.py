"""
validator.py - Configuration validation and comparison

Compares predicted vs known electron configurations and generates reports.
Pure validation logic with detailed analysis capabilities.
"""

from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
import json
from datetime import datetime
from .atom import Atom


class ConfigurationValidator:
    """
    Validates and compares electron configurations
    
    Responsibilities:
    - Compare predicted vs known configurations
    - Calculate accuracy metrics
    - Generate detailed reports
    - Identify common error patterns
    """
    
    def __init__(self, results_dir: str = "results"):
        """
        Initialize validator
        
        Args:
            results_dir: Directory to save validation reports
        """
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
        self.validation_results = []
        self.summary_stats = {}
    
    def validate_atom(self, atom: Atom) -> Dict[str, Any]:
        """
        Validate configuration for a single atom
        
        Args:
            atom: Atom with known and predicted configurations
            
        Returns:
            Validation result dictionary
        """
        if not atom.predicted_config:
            return {
                "atom": atom,
                "status": "error",
                "error": "No predicted configuration",
                "accuracy": 0.0,
                "match": False
            }
        
        known = atom.known_config
        predicted = atom.predicted_config
        
        # Calculate electron-by-electron accuracy
        correct_electrons = sum(min(predicted[i], known[i]) for i in range(5))
        accuracy = (correct_electrons / atom.Z) * 100 if atom.Z > 0 else 0
        
        # Check exact match
        exact_match = predicted == known
        
        # Detailed shell-by-shell analysis
        shell_errors = []
        for shell_n in range(5):
            pred_e = predicted[shell_n]
            known_e = known[shell_n]
            if pred_e != known_e:
                error_type = self._classify_shell_error(shell_n, pred_e, known_e)
                shell_errors.append({
                    "shell": shell_n + 1,
                    "predicted": pred_e,
                    "expected": known_e,
                    "difference": pred_e - known_e,
                    "error_type": error_type
                })
        
        # Check for systematic patterns
        error_patterns = self._identify_error_patterns(atom, shell_errors)
        
        result = {
            "atom": atom,
            "status": "validated",
            "accuracy": accuracy,
            "match": exact_match,
            "correct_electrons": correct_electrons,
            "total_electrons": atom.Z,
            "shell_errors": shell_errors,
            "error_patterns": error_patterns,
            "validation_timestamp": datetime.now().isoformat()
        }
        
        # Store result in atom
        atom.validation_result = result
        
        return result
    
    def _classify_shell_error(self, shell_n: int, predicted: int, expected: int) -> str:
        """Classify the type of shell error"""
        diff = predicted - expected
        
        if diff > 0:
            return f"overfilled_by_{diff}"
        elif diff < 0:
            return f"underfilled_by_{abs(diff)}"
        else:
            return "correct"
    
    def _identify_error_patterns(self, atom: Atom, shell_errors: List[Dict]) -> List[str]:
        """Identify systematic error patterns"""
        patterns = []
        
        if not shell_errors:
            return patterns
        
        # Check for shell jumping
        config = atom.predicted_config
        for i in range(4):  # Check shells 1-4
            current_shell = config[i]
            next_shell = config[i + 1]
            
            # If current shell not full but next shell has electrons
            max_capacity = 2 * (i + 1) ** 2  # Freeman's 2n²
            if current_shell < max_capacity and next_shell > 0:
                patterns.append(f"shell_jumping_{i+1}_to_{i+2}")
        
        # Check for total electron conservation
        predicted_total = sum(atom.predicted_config)
        if predicted_total != atom.Z:
            if predicted_total > atom.Z:
                patterns.append("electron_excess")
            else:
                patterns.append("electron_deficit")
        
        # Check for capacity violations
        for i, electrons in enumerate(atom.predicted_config):
            max_capacity = 2 * (i + 1) ** 2
            if electrons > max_capacity:
                patterns.append(f"capacity_violation_shell_{i+1}")
        
        # Check for specific known problems
        if atom.Z == 19 and config[2] > 8:  # Potassium
            patterns.append("potassium_3d_problem")
        if atom.Z == 20 and config[2] > 8:  # Calcium
            patterns.append("calcium_3d_problem")
        
        return patterns
    
    def validate_atoms(self, atoms: List[Atom], verbose: bool = True) -> List[Dict]:
        """
        Validate configurations for multiple atoms
        
        Args:
            atoms: List of atoms to validate
            verbose: Whether to print progress
            
        Returns:
            List of validation results
        """
        if verbose:
            print(f"\nValidating {len(atoms)} atoms...")
            print("=" * 60)
        
        self.validation_results = []
        
        for atom in atoms:
            result = self.validate_atom(atom)
            self.validation_results.append(result)
            
            if verbose:
                status_symbol = "✓" if result["match"] else "✗"
                print(f"{atom.symbol:>3}: {result['accuracy']:5.1f}% {status_symbol}")
                
                # Show first error for failed cases
                if not result["match"] and result["shell_errors"]:
                    error = result["shell_errors"][0]
                    print(f"     └─ Shell {error['shell']}: {error['predicted']} ≠ {error['expected']}")
        
        # Calculate summary statistics
        self._calculate_summary_stats()
        
        if verbose:
            print("-" * 60)
            print(f"Summary: {self.summary_stats['average_accuracy']:.1f}% accuracy, "
                  f"{self.summary_stats['perfect_matches']}/{len(atoms)} perfect matches")
        
        return self.validation_results
    
    def _calculate_summary_stats(self):
        """Calculate summary statistics from validation results"""
        if not self.validation_results:
            return
        
        total_atoms = len(self.validation_results)
        total_accuracy = sum(r["accuracy"] for r in self.validation_results)
        perfect_matches = sum(1 for r in self.validation_results if r["match"])
        
        # Error pattern analysis
        all_patterns = []
        for result in self.validation_results:
            all_patterns.extend(result["error_patterns"])
        
        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        # Shell-specific error analysis
        shell_errors = {i: {"overfilled": 0, "underfilled": 0} for i in range(1, 6)}
        for result in self.validation_results:
            for error in result["shell_errors"]:
                shell_n = error["shell"]
                if error["difference"] > 0:
                    shell_errors[shell_n]["overfilled"] += 1
                else:
                    shell_errors[shell_n]["underfilled"] += 1
        
        self.summary_stats = {
            "total_atoms": total_atoms,
            "average_accuracy": total_accuracy / total_atoms,
            "perfect_matches": perfect_matches,
            "success_rate": (perfect_matches / total_atoms) * 100,
            "pattern_counts": pattern_counts,
            "shell_error_breakdown": shell_errors,
            "validation_timestamp": datetime.now().isoformat()
        }
    
    def generate_detailed_report(self) -> str:
        """Generate detailed validation report"""
        if not self.validation_results:
            return "No validation results available"
        
        report_lines = []
        report_lines.append("DETAILED VALIDATION REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Total atoms analyzed: {self.summary_stats['total_atoms']}")
        report_lines.append("")
        
        # Summary statistics
        report_lines.append("SUMMARY STATISTICS")
        report_lines.append("-" * 40)
        report_lines.append(f"Average accuracy: {self.summary_stats['average_accuracy']:.1f}%")
        report_lines.append(f"Perfect matches: {self.summary_stats['perfect_matches']}")
        report_lines.append(f"Success rate: {self.summary_stats['success_rate']:.1f}%")
        report_lines.append("")
        
        # Detailed results table
        report_lines.append("DETAILED RESULTS")
        report_lines.append("-" * 80)
        report_lines.append(f"{'Element':<8} | {'Z':<3} | {'Predicted':<20} | {'Expected':<20} | {'Acc%':<6} | {'Status'}")
        report_lines.append("-" * 80)
        
        for result in self.validation_results:
            atom = result["atom"]
            pred_str = str(atom.predicted_config) if atom.predicted_config else "None"
            known_str = str(atom.known_config)
            accuracy = result["accuracy"]
            status = "✓" if result["match"] else "✗"
            
            report_lines.append(
                f"{atom.symbol:<8} | {atom.Z:<3} | {pred_str:<20} | {known_str:<20} | "
                f"{accuracy:<6.1f} | {status}"
            )
        
        # Error pattern analysis
        if self.summary_stats["pattern_counts"]:
            report_lines.append("")
            report_lines.append("ERROR PATTERN ANALYSIS")
            report_lines.append("-" * 40)
            for pattern, count in sorted(self.summary_stats["pattern_counts"].items()):
                report_lines.append(f"{pattern}: {count} occurrences")
        
        # Shell error breakdown
        report_lines.append("")
        report_lines.append("SHELL ERROR BREAKDOWN")
        report_lines.append("-" * 40)
        for shell_n, errors in self.summary_stats["shell_error_breakdown"].items():
            if errors["overfilled"] > 0 or errors["underfilled"] > 0:
                report_lines.append(f"Shell {shell_n}: {errors['overfilled']} overfilled, "
                                   f"{errors['underfilled']} underfilled")
        
        return "\n".join(report_lines)
    
    def save_report(self, filename: Optional[str] = None) -> Path:
        """Save validation report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"validation_report_{timestamp}.txt"
        
        filepath = self.results_dir / filename
        
        report_content = self.generate_detailed_report()
        
        with open(filepath, 'w') as f:
            f.write(report_content)
        
        print(f"Validation report saved: {filepath}")
        return filepath
    
    def save_json_results(self, filename: Optional[str] = None) -> Path:
        """Save validation results as JSON for programmatic analysis"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"validation_results_{timestamp}.json"
        
        filepath = self.results_dir / filename
        
        # Convert results to JSON-serializable format
        json_results = {
            "summary": self.summary_stats,
            "results": []
        }
        
        for result in self.validation_results:
            atom_data = {
                "Z": result["atom"].Z,
                "symbol": result["atom"].symbol,
                "known_config": result["atom"].known_config,
                "predicted_config": result["atom"].predicted_config,
                "accuracy": result["accuracy"],
                "match": result["match"],
                "shell_errors": result["shell_errors"],
                "error_patterns": result["error_patterns"]
            }
            json_results["results"].append(atom_data)
        
        with open(filepath, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"JSON results saved: {filepath}")
        return filepath
    
    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary statistics"""
        return self.summary_stats.copy() if self.summary_stats else {}