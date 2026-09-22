#!/usr/bin/env python3
"""
Integrated Nuclear Crystal Simulator
Complete implementation of James Freeman's two-stage approach:

Stage 1: Nuclear Attention Network predicts relationship graphs
Stage 2: GPU-accelerated physics simulation optimizes geometry

This integration dramatically reduces computational complexity while
maintaining full physics fidelity.

Authors: Dr. James Freeman (Theory), Suman Pokhrel (Implementation)
Date: August 2025
"""

import numpy as np
import torch
import sys
import time
from typing import Dict, List, Tuple, Optional
import argparse
import json
import logging
from dataclasses import dataclass
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from legacy.enhanced_experimental_database import AdvancedNuclearDatabase, AdvancedNuclearData
    ADVANCED_DB_AVAILABLE = True
except ImportError:
    ADVANCED_DB_AVAILABLE = False
    logger.warning("Advanced nuclear database not available")



@dataclass
class ExperimentalData:
    """Ground truth experimental data for validation"""
    nucleus_name: str
    protons: int
    neutrons: int
    binding_energy_mev: float
    charge_radius_fm: float
    is_stable: bool
    half_life_seconds: Optional[float]
    spin: Optional[str]
# Enhanced experimental database
try:
    from legacy.enhanced_experimental_database import AdvancedNuclearDatabase
    
    class ExperimentalDatabase:
        """Enhanced database using advanced nuclear data with uncertainties"""

        def __init__(self):
            if ADVANCED_DB_AVAILABLE:
                # Use the advanced database
                self.advanced_db = AdvancedNuclearDatabase("binding-energy.txt")
                logger.info("Using advanced nuclear database with uncertainties")
            else:
                # Fallback to original data
                self.data = {}
                self._load_original_experimental_data()
                logger.info("Using fallback experimental database")

        def get_nucleus(self, protons: int, neutrons: int) -> Optional[ExperimentalData]:
            """Get experimental data for a specific nucleus"""
            if ADVANCED_DB_AVAILABLE:
                # Convert from advanced format to original format
                advanced_nucleus = self.advanced_db.get_nucleus(protons, neutrons)
                if advanced_nucleus:
                    return self._convert_to_experimental_data(advanced_nucleus)
                return None
            else:
                # Use original method
                key = f"{protons}p_{neutrons}n"
                return self.data.get(key)

        def _convert_to_experimental_data(self, advanced_nucleus: AdvancedNuclearData) -> ExperimentalData:
            """Convert advanced nuclear data to original ExperimentalData format"""
            return ExperimentalData(
                nucleus_name=f"{advanced_nucleus.element}-{advanced_nucleus.A}",
                protons=advanced_nucleus.Z,
                neutrons=advanced_nucleus.N,
                binding_energy_mev=advanced_nucleus.binding_energy_mev,
                charge_radius_fm=advanced_nucleus.get_nuclear_radius_fm(),
                is_stable=advanced_nucleus.is_stable,
                half_life_seconds=None,  # Not available in advanced format
                spin=None  # Not available in advanced format
            )

        def get_all_stable_nuclei(self) -> List[ExperimentalData]:
            """Get all stable nuclei in the database"""
            if ADVANCED_DB_AVAILABLE:
                stable_nuclei = []
                # Get unique nuclei (avoid duplicates from multiple keys)
                seen = set()
                for nucleus in self.advanced_db.nuclei.values():
                    key = f"{nucleus.Z}_{nucleus.A}"
                    if key not in seen and nucleus.is_stable:
                        stable_nuclei.append(self._convert_to_experimental_data(nucleus))
                        seen.add(key)
                return stable_nuclei
            else:
                return [nucleus for nucleus in self.data.values() if nucleus.is_stable]

        def _load_original_experimental_data(self):
            """Fallback to original experimental data if advanced database not available"""
            experimental_nuclei = [
                ExperimentalData("Deuterium", 1, 1, 2.225, 2.13, True, None, "1+"),
                ExperimentalData("Tritium", 1, 2, 8.482, 1.76, False, 3.888e8, "1/2+"),
                ExperimentalData("Helium-3", 2, 1, 7.718, 1.97, True, None, "1/2+"),
                ExperimentalData("Helium-4", 2, 2, 28.296, 1.68, True, None, "0+"),
                ExperimentalData("Lithium-6", 3, 3, 31.995, 2.59, True, None, "1+"),
                ExperimentalData("Lithium-7", 3, 4, 39.245, 2.44, True, None, "3/2-"),
                ExperimentalData("Beryllium-7", 4, 3, 37.600, 2.51, False, 4.6e6, "3/2-"),
                ExperimentalData("Beryllium-8", 4, 4, 56.500, 2.52, False, 8.19e-17, "0+"),
                ExperimentalData("Boron-10", 5, 5, 64.751, 2.59, True, None, "3+"),
                ExperimentalData("Boron-11", 5, 6, 76.205, 2.40, True, None, "3/2-"),
                ExperimentalData("Carbon-12", 6, 6, 92.162, 2.48, True, None, "0+"),
                ExperimentalData("Carbon-13", 6, 7, 97.108, 2.50, True, None, "1/2-"),
                ExperimentalData("Nitrogen-14", 7, 7, 104.659, 2.56, True, None, "1+"),
                ExperimentalData("Oxygen-16", 8, 8, 127.619, 2.70, True, None, "0+"),
            ]

            for nucleus in experimental_nuclei:
                key = f"{nucleus.protons}p_{nucleus.neutrons}n"
                self.data[key] = nucleus
except ImportError:
    # Fallback to original database if enhanced version not available
    logger.warning("Enhanced database not available, using original")
    
    class ExperimentalDatabase:
        """Database of experimental nuclear data for validation"""
    
        def __init__(self):
            self.data = {}
            self._load_experimental_data()


    
        def _load_experimental_data(self):
            """Load known experimental nuclear data"""

            # Key light nuclei for testing James's theory
            experimental_nuclei = [
                ExperimentalData("Deuterium", 1, 1, 2.225, 2.13, True, None, "1+"),
                ExperimentalData("Tritium", 1, 2, 8.482, 1.76, False, 3.888e8, "1/2+"),
                ExperimentalData("Helium-3", 2, 1, 7.718, 1.97, True, None, "1/2+"),
                ExperimentalData("Helium-4", 2, 2, 28.296, 1.68, True, None, "0+"),
                ExperimentalData("Lithium-6", 3, 3, 31.995, 2.59, True, None, "1+"),
                ExperimentalData("Lithium-7", 3, 4, 39.245, 2.44, True, None, "3/2-"),
                ExperimentalData("Beryllium-7", 4, 3, 37.600, 2.51, False, 4.6e6, "3/2-"),
                ExperimentalData("Beryllium-8", 4, 4, 56.500, 2.52, False, 8.19e-17, "0+"),
                ExperimentalData("Boron-10", 5, 5, 64.751, 2.59, True, None, "3+"),
                ExperimentalData("Boron-11", 5, 6, 76.205, 2.40, True, None, "3/2-"),
                ExperimentalData("Carbon-12", 6, 6, 92.162, 2.48, True, None, "0+"),
                ExperimentalData("Carbon-13", 6, 7, 97.108, 2.50, True, None, "1/2-"),
                ExperimentalData("Nitrogen-14", 7, 7, 104.659, 2.56, True, None, "1+"),
                ExperimentalData("Oxygen-16", 8, 8, 127.619, 2.70, True, None, "0+"),
            ]

            for nucleus in experimental_nuclei:
                key = f"{nucleus.protons}p_{nucleus.neutrons}n"
                self.data[key] = nucleus

        def get_nucleus(self, protons: int, neutrons: int) -> Optional[ExperimentalData]:
            """Get experimental data for a specific nucleus"""
            key = f"{protons}p_{neutrons}n"
            return self.data.get(key)

        def get_all_stable_nuclei(self) -> List[ExperimentalData]:
            """Get all stable nuclei in the database"""
            return [nucleus for nucleus in self.data.values() if nucleus.is_stable]

class IntegratedNuclearSimulator:
    """
    Master class that orchestrates the two-stage simulation process
    """
    
    def __init__(self, use_attention_network: bool = True, 
                 attention_model_path: str = "nuclear_model.pth"):
        self.use_attention_network = use_attention_network
        self.experimental_db = ExperimentalDatabase()
        
        # Initialize Stage 1: Neural Network (if available)
        self.predictor = None
        if use_attention_network:
            try:
                # Import the fixed advanced predictor
                import sys
                sys.path.append('.')  # Ensure current directory is in path
                from core.physics_informed_neural_network import FixedAdvancedPredictor
    
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
                self.predictor = FixedAdvancedPredictor("advanced_physics_model.pth", device)
                logger.info(f"Stage 7 Advanced Physics-Informed Network loaded on {device}")
            except (ImportError, FileNotFoundError) as e:
                logger.warning(f"Physics-informed network not available: {e}")
                logger.info("Falling back to physics-only simulation")
                self.use_attention_network = False
        
        # Initialize Stage 2: Physics Simulation
        # This would import from our physics simulation module
        try:
            from core.nuclear_simulator import NuclearSimulation, NuclearForceModel
            self.NuclearSimulation = NuclearSimulation
            self.NuclearForceModel = NuclearForceModel
            logger.info("Physics simulation engine loaded")
        except ImportError as e:
            logger.error(f"Physics simulation not available: {e}")
            raise ImportError("Physics simulation engine is required")
    
    def predict_nuclear_structure(self, protons: int, neutrons: int) -> Dict:
        """
        Stage 1: Use advanced physics-informed neural network to predict optimal nucleon relationships
        """
        if not self.use_attention_network or self.predictor is None:
            logger.info("Using random initialization (no neural network)")
            return self._random_initialization(protons, neutrons)
    
        logger.info(f"Stage 1: Advanced Physics-Informed Prediction for {protons}p + {neutrons}n")
        
        # Get prediction from the advanced system
        prediction = self.predictor.predict_structure(protons, neutrons)
        
        logger.info(f"Advanced neural network predictions:")
        logger.info(f"  Binding energy: {prediction['predicted_binding_energy']:.2f} MeV")
        logger.info(f"  Stability probability: {prediction['stability_probability']:.3f}")
    
        # Enhanced Stage 7 analysis (optional detailed logging)
        if 'physics_informed' in prediction:
            pi = prediction['physics_informed']
            logger.info(f"  Enhanced Physics Analysis:")
            logger.info(f"    Nuclear radius: {pi['nuclear_radius']:.2f} fm")
            logger.info(f"    Magic number score: {pi['magic_number_score']:.3f}")
            logger.info(f"    Physics quality: {pi['physics_quality_score']:.3f}")
            logger.info(f"    Conservation violations: {len(pi['conservation_violations'])}")
            
            # James Freeman resonance analysis
            jf = pi['james_freeman_resonance']
            logger.info(f"    James Freeman Theory:")
            logger.info(f"      Resonance accuracy: {jf['resonance_accuracy']:.3f}")
            logger.info(f"      Interference score: {jf['interference_score']:.3f}")
            logger.info(f"      Theory applies: {jf['theory_applies']}")
            logger.info(f"      Scroll coherence: {jf['scroll_coherence']:.3f}")
        
        return prediction
    
    def _random_initialization(self, protons: int, neutrons: int) -> Dict:
        """Fallback random initialization when neural network is not available"""
        num_nucleons = protons + neutrons
        
        # Create random adjacency matrix
        adjacency_prob = np.random.random((num_nucleons, num_nucleons))
        adjacency_prob = (adjacency_prob + adjacency_prob.T) / 2  # Make symmetric
        np.fill_diagonal(adjacency_prob, 0)  # No self-connections
        
        adjacency_binary = (adjacency_prob > 0.6).astype(int)
        
        return {
            'adjacency_probabilities': adjacency_prob,
            'adjacency_binary': adjacency_binary,
            'predicted_binding_energy': 0.0,  # Unknown
            'stability_probability': 0.5,     # Unknown
            'nucleon_types': [0] * protons + [1] * neutrons,
            'num_protons': protons,
            'num_neutrons': neutrons
        }
    
    def run_physics_simulation(self, structure_prediction: Dict, 
                             simulation_time: float = 10.0, 
                             use_constraints: bool = True) -> Dict:
        """
        Stage 2: Run GPU-accelerated physics simulation with neural network constraints
        """
        protons = structure_prediction['num_protons']
        neutrons = structure_prediction['num_neutrons']
        
        logger.info(f"Stage 2: Running physics simulation for {protons}p + {neutrons}n")
        logger.info(f"Simulation time: {simulation_time} fm/c")
        
        # Create physics simulation
        simulation = self.NuclearSimulation(protons, neutrons)
        
        # Apply neural network constraints if available
        if use_constraints and 'adjacency_binary' in structure_prediction:
            self._apply_network_constraints(simulation, structure_prediction)
        
        # Run simulation
        start_time = time.time()
        num_steps = int(simulation_time / simulation.time_step)
        
        energy_history = []
        geometry_history = []
        
        for step in range(num_steps):
            simulation.update_physics()
            
            # Record data every 100 steps
            if step % 100 == 0:
                energy = simulation.calculate_total_energy()
                analysis = simulation.analyze_geometry()
                
                energy_history.append(energy)
                geometry_history.append(analysis)
                
                if step % 1000 == 0:
                    logger.info(f"Step {step:5d}: Energy = {energy:.3f} MeV, "
                              f"Radius = {analysis['nuclear_radius']:.2f} fm")
        
        # Final analysis
        final_analysis = simulation.analyze_geometry()
        simulation_time = time.time() - start_time
        
        logger.info(f"Physics simulation completed in {simulation_time:.2f} seconds")
        
        return {
            'final_analysis': final_analysis,
            'energy_history': energy_history,
            'geometry_history': geometry_history,
            'simulation_time_seconds': simulation_time,
            'nucleons': simulation.nucleons,
            'final_energy': final_analysis['total_energy']
        }
    
    def _apply_network_constraints(self, simulation, prediction: Dict):
        """Apply neural network predictions as soft constraints on nucleon positions"""
        adjacency = prediction['adjacency_binary']
        nucleons = simulation.nucleons
        
        # Modify initial positions based on predicted connectivity
        for i, nucleon1 in enumerate(nucleons):
            for j, nucleon2 in enumerate(nucleons):
                if i >= j:
                    continue
                
                if adjacency[i, j] == 1:
                    # These nucleons should be close - move them closer
                    direction = nucleon2.position - nucleon1.position
                    distance = np.linalg.norm(direction)
                    
                    if distance > 0:
                        # Target distance for "connected" nucleons
                        target_distance = 2.0  # fm
                        if distance > target_distance:
                            # Move nucleons closer
                            adjustment = direction * 0.1 * (distance - target_distance) / distance
                            nucleon1.position += adjustment
                            nucleon2.position -= adjustment
        
        # Recenter system
        simulation.recenter_system()
        
        logger.info("Applied neural network constraints to initial positions")
    
    def validate_against_experiment(self, result: Dict, protons: int, neutrons: int) -> Dict:
        """Enhanced validation with uncertainty analysis"""
        experimental = self.experimental_db.get_nucleus(protons, neutrons)

        if experimental is None:
            logger.warning(f"No experimental data available for {protons}p + {neutrons}n")
            return {'experimental_data_available': False}

        # Calculate deviations
        simulated_energy = abs(result['final_energy'])
        energy_error = abs(simulated_energy - experimental.binding_energy_mev)
        energy_error_percent = (energy_error / experimental.binding_energy_mev) * 100

        simulated_radius = result['final_analysis']['nuclear_radius']
        radius_error = abs(simulated_radius - experimental.charge_radius_fm)
        radius_error_percent = (radius_error / experimental.charge_radius_fm) * 100

        # Stability prediction
        predicted_stable = result['final_analysis']['total_energy'] < -10.0
        stability_correct = predicted_stable == experimental.is_stable

        # Enhanced validation with uncertainties (if advanced database available)
        enhanced_validation = {}
        if ADVANCED_DB_AVAILABLE and hasattr(self.experimental_db, 'advanced_db'):
            advanced_nucleus = self.experimental_db.advanced_db.get_nucleus(protons, neutrons)
            if advanced_nucleus:
                exp_uncertainty = advanced_nucleus.binding_energy_uncertainty / 1000.0  # Convert to MeV
                within_uncertainty = energy_error <= (2 * exp_uncertainty)  # 2-sigma

                enhanced_validation = {
                    'experimental_uncertainty_mev': exp_uncertainty,
                    'within_experimental_uncertainty': within_uncertainty,
                    'decay_mode': advanced_nucleus.decay_mode,
                    'separation_energy_n': advanced_nucleus.separation_energy_n,
                    'separation_energy_p': advanced_nucleus.separation_energy_p,
                    'binding_per_nucleon_experimental': advanced_nucleus.binding_energy_per_nucleon,
                    'binding_per_nucleon_simulated': simulated_energy / (protons + neutrons)
                }

        validation = {
            'experimental_data_available': True,
            'nucleus_name': experimental.nucleus_name,
            'binding_energy': {
                'experimental_mev': experimental.binding_energy_mev,
                'simulated_mev': simulated_energy,
                'error_mev': energy_error,
                'error_percent': energy_error_percent
            },
            'nuclear_radius': {
                'experimental_fm': experimental.charge_radius_fm,
                'simulated_fm': simulated_radius,
                'error_fm': radius_error,
                'error_percent': radius_error_percent
            },
            'stability': {
                'experimental': experimental.is_stable,
                'predicted': predicted_stable,
                'correct': stability_correct
            },
            **enhanced_validation  # Add enhanced validation if available
        }

        # Enhanced logging
        logger.info(f"Validation results for {experimental.nucleus_name}:")
        logger.info(f"  Binding energy error: {energy_error_percent:.1f}%")
        logger.info(f"  Nuclear radius error: {radius_error_percent:.1f}%")
        logger.info(f"  Stability prediction: {'Correct' if stability_correct else 'Incorrect'}")

        if enhanced_validation:
            logger.info(f"  Within experimental uncertainty: {enhanced_validation.get('within_experimental_uncertainty', 'Unknown')}")
            logger.info(f"  Experimental decay mode: {enhanced_validation.get('decay_mode', 'Unknown')}")

        return validation
    def run_complete_analysis(self, protons: int, neutrons: int, 
                            simulation_time: float = 10.0,
                            save_results: bool = True) -> Dict:
        """
        Run the complete two-stage analysis pipeline
        """
        logger.info("="*60)
        logger.info(f"COMPLETE NUCLEAR ANALYSIS: {protons} protons + {neutrons} neutrons")
        logger.info("="*60)
        
        start_time = time.time()
        
        # Stage 1: Neural Network Prediction
        structure_prediction = self.predict_nuclear_structure(protons, neutrons)
        
        # Stage 2: Physics Simulation
        physics_result = self.run_physics_simulation(
            structure_prediction, simulation_time, use_constraints=True
        )
        
        # Validation against experimental data
        validation = self.validate_against_experiment(physics_result, protons, neutrons)
        
        # Compile complete results
        complete_results = {
            'input': {
                'protons': protons,
                'neutrons': neutrons,
                'mass_number': protons + neutrons,
                'n_to_z_ratio': neutrons / protons if protons > 0 else 0
            },
            'stage1_neural_prediction': structure_prediction,
            'stage2_physics_simulation': physics_result,
            'experimental_validation': validation,
            'total_analysis_time': time.time() - start_time
        }
        
        # Save results if requested
        if save_results:
            filename = f"results/nuclear_analysis_{protons}p_{neutrons}n.json"
            # Convert numpy arrays to lists for JSON serialization
            json_results = self._prepare_for_json(complete_results)
            with open(filename, 'w') as f:
                json.dump(json_results, f, indent=2)
            logger.info(f"Results saved to {filename}")
        
        logger.info(f"Complete analysis finished in {complete_results['total_analysis_time']:.2f} seconds")
        
        return complete_results
    
    def _prepare_for_json(self, data):
        """Convert numpy arrays and other non-serializable objects for JSON"""
        if isinstance(data, dict):
            return {key: self._prepare_for_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._prepare_for_json(item) for item in data]
        elif isinstance(data, bool):  # Handle bool BEFORE other types
            return data
        elif hasattr(data, '_value_'):  # Handle Enum objects
            return data._value_
        elif hasattr(data, '__dict__') and not isinstance(data, type):  # Handle other objects
            return {k: self._prepare_for_json(v) for k, v in data.__dict__.items() 
                    if not k.startswith('_')}
        elif isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, np.floating):
            return float(data)
        elif isinstance(data, np.integer):
            return int(data)
        elif isinstance(data, (type(None), str, int, float)):  # Handle basic types
            return data
        else:
            try:
                return str(data)  # Convert anything else to string
            except:
                return None

class NuclearBenchmark:
    """Benchmark suite for testing James's theory against known nuclei"""
    
    def __init__(self, simulator: IntegratedNuclearSimulator):
        self.simulator = simulator
        self.results = []
    
    def run_helium4_benchmark(self):
        """Test the perfect crystal case: Helium-4"""
        logger.info("BENCHMARK: Helium-4 (Perfect Tetrahedral Crystal)")
        result = self.simulator.run_complete_analysis(2, 2, simulation_time=15.0)
        self.results.append(('Helium-4', result))
        
        # Special analysis for tetrahedral geometry
        if 'tetrahedral_score' in result['stage2_physics_simulation']['final_analysis']:
            score = result['stage2_physics_simulation']['final_analysis']['tetrahedral_score']
            logger.info(f"Tetrahedral geometry score: {score:.3f} (1.0 = perfect)")
        
        return result
    
    def run_lithium7_benchmark(self):
        """Test the imperfect crystal case: Lithium-7"""
        logger.info("BENCHMARK: Lithium-7 (Asymmetric Crystal)")
        result = self.simulator.run_complete_analysis(3, 4, simulation_time=20.0)
        self.results.append(('Lithium-7', result))
        return result
    
    def run_beryllium8_benchmark(self):
        """Test the unstable case: Beryllium-8"""
        logger.info("BENCHMARK: Beryllium-8 (Unstable)")
        result = self.simulator.run_complete_analysis(4, 4, simulation_time=5.0)
        self.results.append(('Beryllium-8', result))
        return result
    
    def run_full_benchmark_suite(self):
        """Run all benchmark tests"""
        logger.info("Starting Full Benchmark Suite for James Freeman's Crystal Particle Hypothesis")
        
        benchmark_start = time.time()
        
        # Primary test cases
        he4_result = self.run_helium4_benchmark()
        li7_result = self.run_lithium7_benchmark()
        be8_result = self.run_beryllium8_benchmark()
        
        # Additional light nuclei
        logger.info("BENCHMARK: Additional Light Nuclei")
        additional_nuclei = [(1, 1), (1, 2), (2, 1), (3, 3), (5, 5), (6, 6)]
        
        for protons, neutrons in additional_nuclei:
            result = self.simulator.run_complete_analysis(protons, neutrons, simulation_time=10.0)
            nucleus_name = f"{protons}p_{neutrons}n"
            self.results.append((nucleus_name, result))
        
        total_time = time.time() - benchmark_start
        logger.info(f"Full benchmark suite completed in {total_time:.2f} seconds")
        
        # Generate summary report
        self.generate_summary_report()
        
        return self.results
    
    def generate_summary_report(self):
        """Generate a summary report of all benchmark results"""
        logger.info("="*60)
        logger.info("BENCHMARK SUMMARY REPORT")
        logger.info("="*60)
        
        total_cases = len(self.results)
        successful_predictions = 0
        energy_errors = []
        radius_errors = []
        
        for nucleus_name, result in self.results:
            validation = result['experimental_validation']
            
            if validation['experimental_data_available']:
                energy_error = validation['binding_energy']['error_percent']
                radius_error = validation['nuclear_radius']['error_percent']
                
                energy_errors.append(energy_error)
                radius_errors.append(radius_error)
                
                # Consider successful if both errors < 20%
                if energy_error < 20.0 and radius_error < 20.0:
                    successful_predictions += 1
                
                logger.info(f"{nucleus_name:12s}: Energy {energy_error:5.1f}% error, "
                          f"Radius {radius_error:5.1f}% error")
        
        if energy_errors:
            logger.info("-" * 60)
            logger.info(f"Overall Performance:")
            logger.info(f"  Success Rate: {successful_predictions}/{len(energy_errors)} "
                      f"({100*successful_predictions/len(energy_errors):.1f}%)")
            logger.info(f"  Mean Energy Error: {np.mean(energy_errors):.1f}%")
            logger.info(f"  Mean Radius Error: {np.mean(radius_errors):.1f}%")
            logger.info(f"  Max Energy Error: {np.max(energy_errors):.1f}%")
            logger.info(f"  Max Radius Error: {np.max(radius_errors):.1f}%")

def main():
    """Main entry point with command-line interface"""
    parser = argparse.ArgumentParser(
        description="Nuclear Crystal Simulator - Testing James Freeman's Theory"
    )
    
    parser.add_argument('--protons', type=int, help='Number of protons')
    parser.add_argument('--neutrons', type=int, help='Number of neutrons')
    parser.add_argument('--benchmark', action='store_true', 
                       help='Run full benchmark suite')
    parser.add_argument('--time', type=float, default=10.0,
                       help='Simulation time in fm/c units')
    parser.add_argument('--no-neural', action='store_true',
                       help='Skip neural network stage')
    parser.add_argument('--visualize', action='store_true',
                       help='Show 3D visualization')
    
    args = parser.parse_args()
    
    try:
        # Initialize simulator
        simulator = IntegratedNuclearSimulator(
            use_attention_network=not args.no_neural
        )
        
        if args.benchmark:
            # Run full benchmark suite
            benchmark = NuclearBenchmark(simulator)
            benchmark.run_full_benchmark_suite()
            
        elif args.protons is not None and args.neutrons is not None:
            # Single nucleus analysis
            result = simulator.run_complete_analysis(
                args.protons, args.neutrons, simulation_time=args.time
            )
            
            # Show 3D visualization if requested
            if args.visualize:
                logger.info("Starting 3D visualization...")
                from core.nuclear_simulator import OpenGLVisualizer, NuclearSimulation
                
                # Create fresh simulation for visualization
                vis_simulation = NuclearSimulation(args.protons, args.neutrons)
                visualizer = OpenGLVisualizer(vis_simulation)
                visualizer.run()
        
        else:
            # Show usage examples
            print("Nuclear Crystal Simulator - Usage Examples:")
            print()
            print("Single nucleus analysis:")
            print("  python integrated_nuclear_system.py --protons 2 --neutrons 2")
            print("  python integrated_nuclear_system.py --protons 3 --neutrons 4 --visualize")
            print()
            print("Full benchmark suite:")
            print("  python integrated_nuclear_system.py --benchmark")
            print()
            print("Physics-only (skip neural network):")
            print("  python integrated_nuclear_system.py --protons 2 --neutrons 2 --no-neural")
    
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()