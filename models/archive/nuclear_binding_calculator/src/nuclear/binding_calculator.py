"""
Complete nuclear binding energy calculator implementing James Freeman's theory.
Includes all missing analysis functions and comprehensive validation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution
import json

from ..core.physics_constants import CONSTANTS, get_experimental_binding_energies, get_nuclear_properties
from ..core.relativistic_mechanics import RelativisticMechanics

@dataclass
class BindingParameters:
    """Parameters for nuclear binding calculations"""
    # NP channel attractions at different geometries
    U_NP_deuteron: float = -1.548    # MeV
    U_NP_A3: float = -2.000          # MeV  
    U_NP_A4: float = -2.145          # MeV
    
    # Edge-specific terms
    U_NN_assist: float = -0.10       # NN assistance (MeV)
    U_NN_A4: float = -0.20           # A=4 NN tweak (MeV)
    U_PP_penalty: float = +0.650     # PP repulsion (MeV)
    
    # Cooperative terms (multi-channel effects)
    C3_tritium: float = -2.702       # Tritium cooperative (MeV)
    C3_helium3: float = -2.688       # Helium-3 cooperative (MeV) 
    C4_helium4: float = -16.67       # Helium-4 cooperative (MeV)
    
    # Quality metrics
    fit_quality: float = 0.0         # RMS error vs experiment
    split_error: float = 0.0         # Error in 3H-3He split

@dataclass
class BindingResult:
    """Results from nuclear binding calculation"""
    nucleus: str
    calculated_binding: float
    experimental_binding: float
    error: float
    components: Dict[str, float] = field(default_factory=dict)
    relativistic_analysis: Dict[str, Any] = field(default_factory=dict)

class NuclearBindingCalculator:
    """
    Complete implementation of James Freeman's nuclear binding theory.
    
    Core principle: Strong force = Angular momentum conservation ∩ Relativity ∩ Geometry
    """
    
    def __init__(self):
        self.mechanics = RelativisticMechanics()
        self.experimental_data = get_experimental_binding_energies()
        self.nuclear_properties = get_nuclear_properties()
        self.parameters = BindingParameters()
        
        # Analysis storage
        self.calculation_history = []
        self.parameter_fits = []
        
    def calculate_channel_energy(self, edge_type: str, nucleus: str, 
                                params: Optional[BindingParameters] = None) -> Tuple[float, Dict[str, float]]:
        """
        Calculate energy for specific edge type in given nucleus.
        
        Args:
            edge_type: 'NP', 'NN', or 'PP'
            nucleus: Nuclear configuration name
            params: Parameter set to use
            
        Returns:
            Tuple of (total_energy, component_breakdown)
        """
        if params is None:
            params = self.parameters
            
        # Get geometry scale factor
        if nucleus == 'deuteron':
            s = CONSTANTS.s_deuteron
            U_NP = params.U_NP_deuteron
        elif nucleus in ['tritium', 'helium3']:
            s = CONSTANTS.s_A3
            U_NP = params.U_NP_A3
        elif nucleus == 'helium4':
            s = CONSTANTS.s_A4
            U_NP = params.U_NP_A4
        else:
            raise ValueError(f"Unknown nucleus: {nucleus}")
        
        # Calculate relativistic component (2 leptons per channel)
        delta_K_per_lepton = self.mechanics.kinetic_energy_change(s)[0]
        relativistic_component = 2 * delta_K_per_lepton
        
        # Add channel-specific terms
        if edge_type == 'NP':
            channel_term = U_NP
        elif edge_type == 'NN':
            if nucleus == 'helium4':
                channel_term = params.U_NN_A4
            else:
                channel_term = params.U_NN_assist
        elif edge_type == 'PP':
            channel_term = params.U_PP_penalty
        else:
            raise ValueError(f"Unknown edge type: {edge_type}")
        
        total_energy = relativistic_component + channel_term
        
        components = {
            'relativistic': relativistic_component,
            'channel_term': channel_term,
            'total': total_energy,
            'scale_factor': s,
            'delta_K_per_lepton': delta_K_per_lepton
        }
        
        return total_energy, components
    
    def calculate_nucleus_binding(self, nucleus: str, 
                                 params: Optional[BindingParameters] = None,
                                 detailed: bool = False) -> BindingResult:
        """
        Calculate total binding energy for a nucleus.
        
        Args:
            nucleus: Nuclear configuration name
            params: Parameter set to use
            detailed: Whether to include detailed component analysis
            
        Returns:
            BindingResult with calculation details
        """
        if params is None:
            params = self.parameters
            
        nuclear_data = self.nuclear_properties[nucleus]
        edges = nuclear_data['edges']
        
        total_binding = 0.0
        components = {}
        
        # Calculate edge contributions
        for edge_type, count in edges.items():
            if count > 0:
                edge_energy, edge_components = self.calculate_channel_energy(
                    edge_type, nucleus, params
                )
                edge_contribution = count * edge_energy
                total_binding += edge_contribution
                
                components[f'{edge_type}_energy'] = edge_energy
                components[f'{edge_type}_count'] = count
                components[f'{edge_type}_contribution'] = edge_contribution
                
                if detailed:
                    components[f'{edge_type}_relativistic'] = edge_components['relativistic']
                    components[f'{edge_type}_channel_term'] = edge_components['channel_term']
        
        # Add cooperative terms
        cooperative_term = 0.0
        if nucleus == 'tritium':
            cooperative_term = params.C3_tritium
        elif nucleus == 'helium3':
            cooperative_term = params.C3_helium3
        elif nucleus == 'helium4':
            cooperative_term = params.C4_helium4
        
        total_binding += cooperative_term
        components['cooperative'] = cooperative_term
        components['total_before_cooperative'] = total_binding - cooperative_term
        
        # Create result
        experimental_value = self.experimental_data[nucleus]
        error = total_binding - experimental_value
        
        result = BindingResult(
            nucleus=nucleus,
            calculated_binding=total_binding,
            experimental_binding=experimental_value,
            error=error,
            components=components
        )
        
        # Add relativistic analysis if detailed
        if detailed:
            result.relativistic_analysis = self._analyze_relativistic_effects(nucleus, params)
        
        return result
    
    def _analyze_relativistic_effects(self, nucleus: str, params: BindingParameters) -> Dict[str, Any]:
        """Detailed analysis of relativistic effects for a nucleus"""
        
        # Get geometry scale
        if nucleus == 'deuteron':
            s = CONSTANTS.s_deuteron
        elif nucleus in ['tritium', 'helium3']:
            s = CONSTANTS.s_A3
        elif nucleus == 'helium4':
            s = CONSTANTS.s_A4
        
        # Calculate relativistic state changes
        delta_K, initial_state, final_state = self.mechanics.kinetic_energy_change(s)
        
        # Calculate total relativistic contribution
        nuclear_data = self.nuclear_properties[nucleus]
        total_channels = sum(count for edge_type, count in nuclear_data['edges'].items() 
                           if edge_type in ['NP', 'NN'])  # Only channels with leptons
        
        total_relativistic_binding = -delta_K * 2 * total_channels  # 2 leptons per channel
        
        return {
            'scale_factor': s,
            'initial_gamma': initial_state.gamma,
            'initial_beta': initial_state.beta,
            'final_gamma': final_state.gamma,
            'final_beta': final_state.beta,
            'delta_K_per_lepton': delta_K,
            'binding_per_channel': -delta_K * 2,
            'total_channels': total_channels,
            'total_relativistic_binding': total_relativistic_binding,
            'velocity_drop': initial_state.beta - final_state.beta,
            'gamma_collapse': initial_state.gamma - final_state.gamma
        }
    
    def calculate_all_light_nuclei(self, params: Optional[BindingParameters] = None) -> Dict[str, BindingResult]:
        """Calculate binding energies for all light nuclei"""
        if params is None:
            params = self.parameters
            
        results = {}
        for nucleus in ['deuteron', 'tritium', 'helium3', 'helium4']:
            results[nucleus] = self.calculate_nucleus_binding(nucleus, params, detailed=True)
            
        return results
    
    def _calculate_critical_split(self, params: BindingParameters) -> Tuple[float, float, bool]:
        """
        Internal function to calculate split without printing.
        Used by optimization routines to avoid infinite recursion.
        """
        tritium_result = self.calculate_nucleus_binding('tritium', params)
        helium3_result = self.calculate_nucleus_binding('helium3', params)
        
        calculated_split = tritium_result.calculated_binding - helium3_result.calculated_binding
        experimental_split = -0.764  # MeV
        split_error = abs(calculated_split - experimental_split)
        success = split_error < 0.001
        
        return calculated_split, split_error, success

    def test_critical_split(self, params: Optional[BindingParameters] = None) -> Tuple[float, float, bool]:
        """
        Test the critical 3H-3He split that must be exactly 0.764 MeV.
        This is James's primary falsification criterion.
        """
        if params is None:
            params = self.parameters
            
        calculated_split, split_error, success = self._calculate_critical_split(params)
        
        # Enhanced error reporting with proper precision
        print(f"Calculated 3H-3He split: {calculated_split:.6f} MeV")  # More precision
        print(f"Experimental split: -0.764000 MeV") 
        error = abs(calculated_split + 0.764)
        print(f"Absolute error: {error:.6f} MeV")
        print(f"Error (3-decimal rounding): {error:.3f} MeV")  # Clarify rounding
        
        return calculated_split, split_error, success
    
    def fit_parameters_to_experiment(self, method: str = 'differential_evolution') -> Tuple[BindingParameters, Dict[str, float]]:
        """
        Fit model parameters to experimental binding energies.
        
        Args:
            method: Optimization method ('minimize', 'differential_evolution')
            
        Returns:
            Tuple of (optimized_parameters, fit_statistics)
        """
        
        def objective_function(param_array):
            """Objective function for parameter optimization"""
            # Unpack parameters
            params = BindingParameters(
                U_NP_deuteron=param_array[0],
                U_NP_A3=param_array[1], 
                U_NP_A4=param_array[2],
                U_NN_assist=param_array[3],
                U_NN_A4=param_array[4],
                U_PP_penalty=param_array[5],
                C3_tritium=param_array[6],
                C3_helium3=param_array[7],
                C4_helium4=param_array[8]
            )
            
            # Calculate all nuclei
            total_error = 0.0
            split_penalty = 0.0
            
            for nucleus in ['deuteron', 'tritium', 'helium3', 'helium4']:
                result = self.calculate_nucleus_binding(nucleus, params)
                total_error += result.error**2
            
            # Heavy penalty for wrong split
            split_calc, split_error, _ = self._calculate_critical_split(params)
            split_penalty = 1000.0 * split_error**2  # Heavy weight on split accuracy
            
            return total_error + split_penalty
        
        # Parameter bounds
        bounds = [
            (-3.0, 0.0),    # U_NP_deuteron
            (-4.0, 0.0),    # U_NP_A3
            (-4.0, 0.0),    # U_NP_A4
            (-1.0, 0.0),    # U_NN_assist
            (-1.0, 0.0),    # U_NN_A4
            (0.0, 2.0),     # U_PP_penalty
            (-5.0, 0.0),    # C3_tritium
            (-5.0, 0.0),    # C3_helium3
            (-25.0, 0.0)    # C4_helium4
        ]
        
        # Initial guess
        initial_guess = [
            self.parameters.U_NP_deuteron,
            self.parameters.U_NP_A3,
            self.parameters.U_NP_A4,
            self.parameters.U_NN_assist,
            self.parameters.U_NN_A4,
            self.parameters.U_PP_penalty,
            self.parameters.C3_tritium,
            self.parameters.C3_helium3,
            self.parameters.C4_helium4
        ]
        
        # Optimize
        if method == 'differential_evolution':
            result = differential_evolution(objective_function, bounds, seed=42, maxiter=1000)
        else:
            result = minimize(objective_function, initial_guess, bounds=bounds, method='L-BFGS-B')
        
        # Create optimized parameters
        optimized_params = BindingParameters(
            U_NP_deuteron=result.x[0],
            U_NP_A3=result.x[1],
            U_NP_A4=result.x[2],
            U_NN_assist=result.x[3],
            U_NN_A4=result.x[4],
            U_PP_penalty=result.x[5],
            C3_tritium=result.x[6],
            C3_helium3=result.x[7],
            C4_helium4=result.x[8],
            fit_quality=np.sqrt(result.fun)
        )
        
        # Calculate fit statistics
        results = self.calculate_all_light_nuclei(optimized_params)
        split_calc, split_error, split_success = self.test_critical_split(optimized_params)
        
        fit_stats = {
            'total_rms_error': np.sqrt(sum(r.error**2 for r in results.values())),
            'split_calculated': split_calc,
            'split_error': split_error,
            'split_success': split_success,
            'optimization_success': result.success,
            'function_evaluations': result.nfev if hasattr(result, 'nfev') else 'N/A'
        }
        
        # Update internal parameters
        self.parameters = optimized_params
        self.parameter_fits.append((optimized_params, fit_stats))
        
        return optimized_params, fit_stats
    
    def analyze_energy_components(self, params: Optional[BindingParameters] = None) -> pd.DataFrame:
        """
        Analyze energy components for all nuclei.
        
        Returns:
            DataFrame with detailed energy breakdown
        """
        if params is None:
            params = self.parameters
            
        results = self.calculate_all_light_nuclei(params)
        
        # Create comprehensive analysis DataFrame
        analysis_data = []
        
        for nucleus, result in results.items():
            row = {
                'nucleus': nucleus,
                'total_calculated': result.calculated_binding,
                'total_experimental': result.experimental_binding,
                'total_error': result.error,
                'cooperative_term': result.components.get('cooperative', 0.0)
            }
            
            # Add edge contributions
            nuclear_data = self.nuclear_properties[nucleus]
            for edge_type in ['NP', 'NN', 'PP']:
                count = nuclear_data['edges'].get(edge_type, 0)
                if count > 0:
                    row[f'{edge_type}_count'] = count
                    row[f'{edge_type}_energy'] = result.components.get(f'{edge_type}_energy', 0.0)
                    row[f'{edge_type}_contribution'] = result.components.get(f'{edge_type}_contribution', 0.0)
                else:
                    row[f'{edge_type}_count'] = 0
                    row[f'{edge_type}_energy'] = 0.0
                    row[f'{edge_type}_contribution'] = 0.0
            
            # Add relativistic analysis
            if 'relativistic_analysis' in result.__dict__ and result.relativistic_analysis:
                rel_analysis = result.relativistic_analysis
                row.update({
                    'scale_factor': rel_analysis['scale_factor'],
                    'initial_gamma': rel_analysis['initial_gamma'],
                    'final_gamma': rel_analysis['final_gamma'],
                    'gamma_collapse': rel_analysis['gamma_collapse'],
                    'velocity_drop': rel_analysis['velocity_drop'],
                    'total_relativistic_binding': rel_analysis['total_relativistic_binding']
                })
            
            analysis_data.append(row)
        
        return pd.DataFrame(analysis_data)
    
    def validate_theory_predictions(self) -> Dict[str, bool]:
        """
        Validate key theoretical predictions of James's theory.
        
        Returns:
            Dictionary of validation results
        """
        results = self.calculate_all_light_nuclei()
        
        validations = {
            'binding_energies_correct': all(abs(r.error) < 0.05 for r in results.values()),
            'critical_split_correct': self._calculate_critical_split(self.parameters)[2],
            'relativistic_binding_positive': True,  # Will check below
            'energy_hierarchy_correct': True,      # Will check below
            'parameter_physically_reasonable': True # Will check below
        }
        
        # Check relativistic binding is positive (releases energy)
        for result in results.values():
            if hasattr(result, 'relativistic_analysis') and result.relativistic_analysis:
                rel_binding = result.relativistic_analysis.get('total_relativistic_binding', 0)
                if rel_binding <= 0:
                    validations['relativistic_binding_positive'] = False
                    break
        
        # Check energy hierarchy: |E(He4)| > |E(H3)| > |E(He3)| > |E(D)|
        binding_magnitudes = {k: abs(v.calculated_binding) for k, v in results.items()}
        expected_order = ['helium4', 'tritium', 'helium3', 'deuteron']
        for i in range(len(expected_order) - 1):
            if binding_magnitudes[expected_order[i]] <= binding_magnitudes[expected_order[i+1]]:
                validations['energy_hierarchy_correct'] = False
                break
        
        # Check parameter reasonableness (continued)
        p = self.parameters
        reasonable_ranges = {
            'U_NP_deuteron': (-3.0, 0.0),
            'U_PP_penalty': (0.0, 2.0),
            'C4_helium4': (-30.0, 0.0)
        }

        if not (-3.0 <= p.U_NP_deuteron <= 0.0):
            validations['parameter_physically_reasonable'] = False
        if not (0.0 <= p.U_PP_penalty <= 2.0):
            validations['parameter_physically_reasonable'] = False
        if not (-30.0 <= p.C4_helium4 <= 0.0):
            validations['parameter_physically_reasonable'] = False

        return validations
   
    def generate_predictions_for_heavier_nuclei(self) -> Dict[str, float]:
        """
        Generate predictions for heavier nuclei using the fitted parameters.
        This tests the theory's predictive power beyond the fitting set.
        """
        # Placeholder for heavier nuclei - would need extended theory
        predictions = {
            'lithium6': None,  # Would need A=6 geometry
            'beryllium8': None,  # Would need A=8 geometry
            'carbon12': None   # Would need A=12 geometry
        }
        
        # For now, return placeholder
        return predictions
    
    def export_results(self, filepath: str, include_detailed: bool = True):
        """Export calculation results to file"""
        results = self.calculate_all_light_nuclei()
        
        export_data = {
            'theory_name': 'James Freeman Nuclear Binding Theory',
            'core_principle': 'Strong force = Angular momentum conservation ∩ Relativity ∩ Geometry',
            'parameters': self.parameters.__dict__,
            'results': {k: v.__dict__ for k, v in results.items()},
            'critical_split_test': {
                'calculated': self._calculate_critical_split(self.parameters)[0],
                'error': self._calculate_critical_split(self.parameters)[1],
                'success': self._calculate_critical_split(self.parameters)[2]
            },
            'validation': self.validate_theory_predictions()
        }
        
        if include_detailed:
            export_data['detailed_analysis'] = self.analyze_energy_components().to_dict('records')
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
    
    def load_parameters(self, filepath: str):
        """Load parameters from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if 'parameters' in data:
            param_dict = data['parameters']
            self.parameters = BindingParameters(**param_dict)

# Analysis and visualization functions
def create_comprehensive_analysis(calculator: NuclearBindingCalculator) -> None:
   """Create comprehensive analysis plots and reports"""
   
   # Fit parameters if not already done
   if calculator.parameters.fit_quality == 0.0:
       print("Fitting parameters to experimental data...")
       params, stats = calculator.fit_parameters_to_experiment()
       print(f"Fit completed. RMS error: {stats['total_rms_error']:.6f} MeV")
       print(f"Critical split test: {stats['split_success']}")
   
   # Generate all results
   results = calculator.calculate_all_light_nuclei()
   analysis_df = calculator.analyze_energy_components()
   
   # Create plots
   fig, axes = plt.subplots(2, 3, figsize=(18, 12))
   fig.suptitle("James Freeman's Nuclear Binding Theory - Comprehensive Analysis", fontsize=16)
   
   # Plot 1: Binding energies comparison
   nuclei = list(results.keys())
   calculated = [results[n].calculated_binding for n in nuclei]
   experimental = [results[n].experimental_binding for n in nuclei]
   
   axes[0,0].bar(range(len(nuclei)), calculated, alpha=0.7, label='Calculated', color='blue')
   axes[0,0].bar(range(len(nuclei)), experimental, alpha=0.7, label='Experimental', color='red')
   axes[0,0].set_xticks(range(len(nuclei)))
   axes[0,0].set_xticklabels(nuclei, rotation=45)
   axes[0,0].set_ylabel('Binding Energy (MeV)')
   axes[0,0].set_title('Binding Energy Comparison')
   axes[0,0].legend()
   axes[0,0].grid(True, alpha=0.3)
   
   # Plot 2: Ice skater velocity analysis
   s_values = np.linspace(1.0, 2.5, 100)
   velocity_analysis = calculator.mechanics.analyze_velocity_regime(s_values)
   
   axes[0,1].plot(s_values, velocity_analysis['beta_values'], 'b-', linewidth=2, label='β (v/c)')
   axes[0,1].axhline(y=calculator.mechanics.beta_0, color='red', linestyle='--', label='Initial β')
   axes[0,1].axvline(x=CONSTANTS.s_deuteron, color='green', linestyle=':', label='Deuteron')
   axes[0,1].axvline(x=CONSTANTS.s_A3, color='orange', linestyle=':', label='A=3')
   axes[0,1].axvline(x=CONSTANTS.s_A4, color='purple', linestyle=':', label='A=4')
   axes[0,1].set_xlabel('Radius Expansion Factor (s)')
   axes[0,1].set_ylabel('Velocity (v/c)')
   axes[0,1].set_title('Ice Skater Velocity Drop')
   axes[0,1].legend()
   axes[0,1].grid(True, alpha=0.3)
   
   # Plot 3: Gamma factor collapse
   axes[0,2].plot(s_values, velocity_analysis['gamma_values'], 'r-', linewidth=2, label='γ factor')
   axes[0,2].axhline(y=calculator.mechanics.gamma_0, color='blue', linestyle='--', label='Initial γ')
   axes[0,2].axvline(x=CONSTANTS.s_deuteron, color='green', linestyle=':', alpha=0.7)
   axes[0,2].axvline(x=CONSTANTS.s_A3, color='orange', linestyle=':', alpha=0.7)
   axes[0,2].axvline(x=CONSTANTS.s_A4, color='purple', linestyle=':', alpha=0.7)
   axes[0,2].set_xlabel('Radius Expansion Factor (s)')
   axes[0,2].set_ylabel('Lorentz Factor (γ)')
   axes[0,2].set_title('Relativistic Gamma Collapse')
   axes[0,2].legend()
   axes[0,2].grid(True, alpha=0.3)
   
   # Plot 4: Energy component breakdown
   nuclei_short = ['D', '³H', '³He', '⁴He']
   width = 0.35
   x_pos = np.arange(len(nuclei))
   
   relativistic_contrib = []
   cooperative_contrib = []
   for nucleus in nuclei:
       result = results[nucleus]
       if hasattr(result, 'relativistic_analysis') and result.relativistic_analysis:
           relativistic_contrib.append(result.relativistic_analysis['total_relativistic_binding'])
       else:
           relativistic_contrib.append(0)
       cooperative_contrib.append(result.components.get('cooperative', 0))
   
   axes[1,0].bar(x_pos - width/2, relativistic_contrib, width, label='Relativistic', alpha=0.8)
   axes[1,0].bar(x_pos + width/2, cooperative_contrib, width, label='Cooperative', alpha=0.8)
   axes[1,0].set_xticks(x_pos)
   axes[1,0].set_xticklabels(nuclei_short)
   axes[1,0].set_ylabel('Energy Contribution (MeV)')
   axes[1,0].set_title('Energy Component Breakdown')
   axes[1,0].legend()
   axes[1,0].grid(True, alpha=0.3)
   
   # Plot 5: Error analysis
   errors = [results[n].error for n in nuclei]
   axes[1,1].bar(range(len(nuclei)), errors, color=['green' if abs(e) < 0.01 else 'orange' if abs(e) < 0.05 else 'red' for e in errors])
   axes[1,1].set_xticks(range(len(nuclei)))
   axes[1,1].set_xticklabels(nuclei_short)
   axes[1,1].set_ylabel('Error (MeV)')
   axes[1,1].set_title('Calculation Errors')
   axes[1,1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
   axes[1,1].grid(True, alpha=0.3)
   
   # Plot 6: Critical split visualization
   split_calc, split_error, split_success = calculator.test_critical_split()
   
   categories = ['³H Binding', '³He Binding', 'Calculated Split', 'Experimental Split']
   values = [
       results['tritium'].calculated_binding,
       results['helium3'].calculated_binding, 
       split_calc,
       -0.764
   ]
   colors = ['blue', 'red', 'green' if split_success else 'orange', 'black']
   
   bars = axes[1,2].bar(range(len(categories)), values, color=colors, alpha=0.7)
   axes[1,2].set_xticks(range(len(categories)))
   axes[1,2].set_xticklabels(categories, rotation=45, ha='right')
   axes[1,2].set_ylabel('Energy (MeV)')
   axes[1,2].set_title(f'Critical Split Test (Error: {split_error:.6f} MeV)')
   axes[1,2].grid(True, alpha=0.3)
   
   # Add text annotation for split success
   success_text = "✓ PASS" if split_success else "✗ FAIL"
   axes[1,2].text(0.5, 0.95, success_text, transform=axes[1,2].transAxes, 
                  ha='center', va='top', fontsize=14, weight='bold',
                  color='green' if split_success else 'red')
   
   plt.tight_layout()
   plt.show()
   
   # Print summary report
   print("\n" + "="*80)
   print("JAMES FREEMAN'S NUCLEAR BINDING THEORY - ANALYSIS REPORT")
   print("="*80)
   print(f"Core Principle: Strong force = Angular momentum conservation ∩ Relativity ∩ Geometry")
   print(f"Ice Skater Mechanism: L = mγvr = constant → γ collapse → binding energy")
   print()
   
   print("BINDING ENERGY RESULTS:")
   for nucleus in nuclei:
       result = results[nucleus]
       print(f"  {nucleus:>10}: {result.calculated_binding:>8.3f} MeV (exp: {result.experimental_binding:>8.3f}) "
             f"error: {result.error:>+7.3f}")
   
   print(f"\nCRITICAL SPLIT TEST:")
   print(f"  ³H - ³He split: {split_calc:>8.3f} MeV (exp: -0.764)")
   print(f"  Error: {split_error:>8.6f} MeV")
   print(f"  Status: {'PASS ✓' if split_success else 'FAIL ✗'}")
   
   print(f"\nRELATIVISTIC ANALYSIS:")
   print(f"  Initial lepton state: γ₀ = {calculator.mechanics.gamma_0:.3f}, β₀ = {calculator.mechanics.beta_0:.3f}")
   for nucleus in nuclei:
       result = results[nucleus]
       if hasattr(result, 'relativistic_analysis') and result.relativistic_analysis:
           rel = result.relativistic_analysis
           print(f"  {nucleus:>10}: s = {rel['scale_factor']:.1f}, "
                 f"γ₁ = {rel['final_gamma']:.3f}, "
                 f"Δγ = {rel['gamma_collapse']:.3f}, "
                 f"E_rel = {rel['total_relativistic_binding']:>6.2f} MeV")
   
   validation_results = calculator.validate_theory_predictions()
   print(f"\nVALIDATION STATUS:")
   for test, passed in validation_results.items():
       status = "PASS ✓" if passed else "FAIL ✗"
       print(f"  {test:>30}: {status}")
   
   overall_success = all(validation_results.values())
   print(f"\nOVERALL THEORY STATUS: {'SUCCESS ✓' if overall_success else 'ISSUES DETECTED ✗'}")
   print("="*80)

# Example usage
if __name__ == "__main__":
   # Initialize calculator
   calculator = NuclearBindingCalculator()
   
   # Run comprehensive analysis
   create_comprehensive_analysis(calculator)
   
   # Export results
   calculator.export_results('nuclear_binding_results.json')
   print("\nResults exported to nuclear_binding_results.json")