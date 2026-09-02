#!/usr/bin/env python3
"""
main.py - Command Line Interface

Entry point for the Atomic Shell Modeller.
Handles user input and orchestrates the complete workflow.
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.modeller import AtomicModeller
from src.validator import ConfigurationValidator
from src.theory import AVAILABLE_THEORIES


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Atomic Shell Modeller - Test theories of electron configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --theory freeman --range 1 20
  python main.py --theory quantum --range 1 30 --verbose
  python main.py --theory modified_freeman --range 19 25 --save-results
        """
    )
    
    parser.add_argument(
        "--theory", 
        choices=list(AVAILABLE_THEORIES.keys()),
        default="freeman",
        help="Theory to use for predictions (default: freeman)"
    )
    
    parser.add_argument(
        "--range",
        nargs=2,
        type=int,
        default=[1, 20],
        metavar=("START", "END"),
        help="Range of atomic numbers to model (default: 1 20)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress and debug information"
    )
    
    parser.add_argument(
        "--save-results",
        action="store_true",
        help="Save validation results to files"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode in theory calculations"
    )
    
    parser.add_argument(
        "--compare",
        nargs="+",
        choices=list(AVAILABLE_THEORIES.keys()),
        help="Compare multiple theories"
    )
    
    return parser.parse_args()


def run_single_theory(theory_name: str, z_range: range, verbose: bool = True, 
                     debug: bool = False, save_results: bool = False):
    """Run modeling with a single theory"""
    
    print(f"ATOMIC SHELL MODELLER")
    print(f"Theory: {theory_name}")
    print(f"Range: Z={z_range.start} to {z_range.stop-1}")
    print("=" * 60)
    
    # Initialize components
    theory_kwargs = {"debug_mode": debug} if theory_name == "freeman" else {}
    modeller = AtomicModeller(theory_name, theory_kwargs)
    validator = ConfigurationValidator()
    
    try:
        # Run modeling workflow
        atoms = modeller.run_modeling(z_range, verbose=verbose)
        
        # Validate results
        validation_results = validator.validate_atoms(atoms, verbose=True)
        
        # Generate report
        report = validator.generate_detailed_report()
        print("\n" + "=" * 80)
        print(report)
        
        # Save results if requested
        if save_results:
            validator.save_report()
            validator.save_json_results()
        
        # Return summary for further analysis
        return {
            "theory": theory_name,
            "atoms": len(atoms),
            "summary": validator.get_summary()
        }
    
    except Exception as e:
        print(f"Error during modeling: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return None


def run_theory_comparison(theory_names: list, z_range: range, verbose: bool = True):
    """Compare multiple theories"""
    
    print(f"THEORY COMPARISON")
    print(f"Theories: {', '.join(theory_names)}")
    print(f"Range: Z={z_range.start} to {z_range.stop-1}")
    print("=" * 80)
    
    results = {}
    
    for theory_name in theory_names:
        print(f"\n{'='*20} {theory_name.upper()} {'='*20}")
        
        result = run_single_theory(
            theory_name, z_range, 
            verbose=False,  # Less verbose for comparison
            debug=False, 
            save_results=False
        )
        
        if result:
            results[theory_name] = result
            summary = result["summary"]
            print(f"{theory_name}: {summary['average_accuracy']:.1f}% accuracy, "
                  f"{summary['perfect_matches']}/{summary['total_atoms']} perfect matches")
    
    # Comparison summary
    print("\n" + "="*80)
    print("THEORY COMPARISON SUMMARY")
    print("="*80)
    print(f"{'Theory':<20} | {'Accuracy':<10} | {'Perfect':<10} | {'Success Rate'}")
    print("-"*80)
    
    for theory_name, result in results.items():
        summary = result["summary"]
        accuracy = summary["average_accuracy"]
        perfect = summary["perfect_matches"]
        total = summary["total_atoms"]
        success_rate = summary["success_rate"]
        
        print(f"{theory_name:<20} | {accuracy:>8.1f}% | {perfect:>4}/{total:<4} | {success_rate:>9.1f}%")
    
    return results


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Validate arguments
    z_start, z_end = args.range
    if z_start >= z_end or z_start < 1:
        print("Error: Invalid atomic number range")
        sys.exit(1)
    
    z_range = range(z_start, z_end + 1)
    
    try:
        if args.compare:
            # Compare multiple theories
            results = run_theory_comparison(
                args.compare, z_range, args.verbose
            )
        else:
            # Run single theory
            result = run_single_theory(
                args.theory, z_range, 
                args.verbose, args.debug, args.save_results
            )
            
            if result:
                print(f"\nModeling complete:")
                print(f"  Theory: {result['theory']}")
                print(f"  Atoms: {result['atoms']}")
                print(f"  Accuracy: {result['summary']['average_accuracy']:.1f}%")
    
    except KeyboardInterrupt:
        print("\nModeling interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()