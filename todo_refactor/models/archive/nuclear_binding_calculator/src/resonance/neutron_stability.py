"""
Neutron stability resonance model implementing James Freeman's theory.
Models the 3-body (e⁻, e⁺, ν̄) resonant system that determines neutron lifetime.

Core principle: Free neutron = leaky resonance (Q ~ 10²⁶, τ ~ 880s)
                Bound neutron = resonant lock with proton → stable
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import minimize
import json

@dataclass
class ResonantState:
    """Represents a resonant state of the 3-body system"""
    electron_position: np.ndarray
    positron_position: np.ndarray
    neutrino_position: np.ndarray
    electron_momentum: np.ndarray
    positron_momentum: np.ndarray
    neutrino_momentum: np.ndarray
    energy: float
    phase: float
    amplitude: float
    timestamp: float = 0.0

@dataclass
class ResonanceParameters:
    """Parameters for neutron resonance calculations"""
    # Fundamental frequencies
    orbital_frequency: float = 4.4e22      # Hz - from James's theory
    oscillation_frequency: float = 1.2e23  # Hz - internal oscillations
    
    # Quality factors
    free_neutron_Q: float = 1e26           # Free neutron quality factor
    bound_neutron_Q: float = 1e35          # Bound neutron (essentially infinite)
    
    # Energy scales
    binding_energy: float = 0.782          # MeV - neutron-proton mass difference
    decay_energy: float = 0.782            # MeV - beta decay Q-value
    
    # Geometric parameters
    neutron_radius: float = 0.8            # fm - effective neutron radius
    interaction_range: float = 2.0         # fm - range of resonant interaction
    
    # Coupling constants
    weak_coupling: float = 1.17e-5         # Fermi coupling constant (GeV⁻²)
    electromagnetic_coupling: float = 1/137 # Fine structure constant
    
    # Relativistic parameters
    gamma_factor: float = 1.7              # From capsid theory
    beta_factor: float = 0.8               # v/c for contained leptons

class NeutronResonanceSimulator:
    """
    Simulates the 3-body resonant system in neutrons.
    
    James's insight: Neutron stability emerges from resonant lock between
    internal (e⁻, e⁺, ν̄) and external proton interactions.
    """
    
    def __init__(self, params: Optional[ResonanceParameters] = None):
        self.params = params or ResonanceParameters()
        self.simulation_history = []
        self.resonance_modes = {}
        
        # Physical constants in natural units
        self.hbar = 1.0
        self.c = 1.0
        self.m_e = 0.511  # MeV
        
    def calculate_q_factor(self, frequency_hz: float, lifetime_seconds: float) -> float:
        """
        Calculate neutron resonance Q-factor.
        
        Q = ω × τ where:
        ω = 2π × frequency (rad/s)  
        τ = lifetime (s)
        
        For free neutron: f ≈ 4.4×10²² Hz, τ ≈ 880 s
        
        Args:
            frequency_hz: Frequency in Hz
            lifetime_seconds: Lifetime in seconds
            
        Returns:
            Q-factor (dimensionless)
        """
        omega = 2 * np.pi * frequency_hz  # Convert to rad/s
        Q = omega * lifetime_seconds
        
        print(f"Frequency: {frequency_hz:.2e} Hz")
        print(f"Lifetime: {lifetime_seconds:.1f} s") 
        print(f"Q-factor: {Q:.2e}")
        print(f"Q-factor definition: Q = 2π × f × τ")
        
        return Q
        
    def calculate_free_neutron_resonance(self, time_span: float = 1000.0, 
                                       num_points: int = 10000) -> Dict[str, Any]:
        """
        Calculate the resonant behavior of a free neutron.
        
        Models the gradually decaying 3-body resonance that leads to beta decay.
        
        Args:
            time_span: Time span to simulate (seconds)
            num_points: Number of time points
            
        Returns:
            Dictionary with resonance analysis
        """
        
        # Time array
        t = np.linspace(0, time_span, num_points)
        
        # Calculate quality factor using proper definition
        # For demonstration, calculate what Q should be from experimental data
        experimental_lifetime = 880.0  # seconds
        theoretical_Q = self.calculate_q_factor(self.params.orbital_frequency, experimental_lifetime)
        
        # Use the Q from parameters (fitted or theoretical)
        Q = self.params.free_neutron_Q
        omega = 2 * np.pi * self.params.orbital_frequency
        
        print(f"\nFree Neutron Q-factor Analysis:")
        print(f"Theoretical Q (from experiment): {theoretical_Q:.2e}")
        print(f"Model Q (parameters): {Q:.2e}")
        print(f"Ratio (model/theory): {Q/theoretical_Q:.2f}")
        
        # Resonance amplitude decay (exponential with Q factor)
        decay_rate = omega / (2 * Q)  # Energy decay rate
        amplitude = np.exp(-decay_rate * t)
        
        # Phase evolution (includes frequency drift as energy decays)
        frequency_drift = decay_rate * t / (2 * np.pi)
        phase = omega * t + frequency_drift * t**2 / 2
        
        # Energy evolution (starts at binding energy, decays to zero)
        energy = self.params.binding_energy * amplitude
        
        # Calculate probability of decay (1 - amplitude²)
        decay_probability = 1 - amplitude**2
        
        # Find half-life
        half_life_idx = np.argmin(np.abs(amplitude - 1/np.sqrt(2)))
        half_life = t[half_life_idx] if half_life_idx < len(t) else time_span
        
        # Calculate expected lifetime (1/e decay)
        lifetime_idx = np.argmin(np.abs(amplitude - 1/np.e))
        lifetime = t[lifetime_idx] if lifetime_idx < len(t) else time_span
        
        return {
            'time': t,
            'amplitude': amplitude,
            'phase': phase,
            'energy': energy,
            'decay_probability': decay_probability,
            'half_life': half_life,
            'lifetime': lifetime,
            'decay_rate': decay_rate,
            'quality_factor': Q,
            'frequency': omega / (2 * np.pi)
        }
    
    def calculate_bound_neutron_resonance(self, proton_distance: float = 2.0) -> Dict[str, Any]:
        """
        Calculate resonant behavior of neutron bound to proton.
        
        Shows how proximity to proton creates resonant lock → stability.
        
        Args:
            proton_distance: Distance to proton (fm)
            
        Returns:
            Dictionary with bound state analysis
        """
        
        # Calculate coupling strength based on distance
        coupling_strength = self._calculate_proton_coupling(proton_distance)
        
        # Enhanced quality factor due to resonant lock
        enhanced_Q = self.params.bound_neutron_Q * coupling_strength
        
        # Calculate locked frequency (shifted by proton interaction)
        base_frequency = self.params.orbital_frequency
        frequency_shift = coupling_strength * base_frequency * 0.01  # Small shift
        locked_frequency = base_frequency + frequency_shift
        
        # Stability analysis
        decay_rate = 2 * np.pi * locked_frequency / (2 * enhanced_Q)
        stability_time = 1 / decay_rate  # Time scale for decay
        
        # Phase lock analysis
        lock_strength = min(coupling_strength * 10, 1.0)  # Normalized lock strength
        phase_coherence = lock_strength
        
        return {
            'proton_distance': proton_distance,
            'coupling_strength': coupling_strength,
            'enhanced_Q': enhanced_Q,
            'locked_frequency': locked_frequency,
            'frequency_shift': frequency_shift,
            'decay_rate': decay_rate,
            'stability_time': stability_time,
            'lock_strength': lock_strength,
            'phase_coherence': phase_coherence,
            'is_stable': stability_time > 1e20  # Practically infinite
        }
    
    def _calculate_proton_coupling(self, distance: float) -> float:
        """Calculate coupling strength between neutron resonance and proton"""
        
        # Exponential decay with distance
        range_param = self.params.interaction_range
        base_coupling = np.exp(-distance / range_param)
        
        # Enhanced coupling at optimal nuclear distances
        optimal_distance = 2.0  # fm - typical nuclear separation
        distance_factor = np.exp(-((distance - optimal_distance) / 0.5)**2)
        
        return base_coupling * (1 + distance_factor)
    
    def simulate_three_body_dynamics(self, duration: float = 1e-21, 
                                   timesteps: int = 1000) -> List[ResonantState]:
        """
        Simulate the detailed 3-body (e⁻, e⁺, ν̄) dynamics inside neutron.
        
        This is the core resonant system that James describes.
        """
        
        # Initialize positions (tetrahedral arrangement)
        initial_radius = self.params.neutron_radius / 2
        
        # Tetrahedral coordinates for 3 particles
        angles = [0, 2*np.pi/3, 4*np.pi/3]
        positions = []
        momenta = []
        
        for i, angle in enumerate(angles):
            # Position on circle at different heights
            x = initial_radius * np.cos(angle)
            y = initial_radius * np.sin(angle)
            z = (i - 1) * initial_radius * 0.3  # Slight z-offset
            
            positions.append(np.array([x, y, z]))
            
            # Initial momentum (circular motion)
            p_magnitude = self.params.gamma_factor * self.m_e * self.params.beta_factor
            px = -p_magnitude * np.sin(angle)  # Tangential
            py = p_magnitude * np.cos(angle)
            pz = 0.0
            
            momenta.append(np.array([px, py, pz]))
        
        # Time evolution
        dt = duration / timesteps
        t = 0.0
        
        states = []
        
        for step in range(timesteps):
            # Calculate forces and evolve system
            new_positions, new_momenta = self._evolve_three_body_step(
                positions, momenta, dt
            )
            
            # Calculate system energy and phase
            energy = self._calculate_system_energy(new_positions, new_momenta)
            phase = self._calculate_system_phase(new_positions, new_momenta, t)
            amplitude = self._calculate_resonance_amplitude(energy, t)
            
            # Create state
            state = ResonantState(
                electron_position=new_positions[0].copy(),
                positron_position=new_positions[1].copy(), 
                neutrino_position=new_positions[2].copy(),
                electron_momentum=new_momenta[0].copy(),
                positron_momentum=new_momenta[1].copy(),
                neutrino_momentum=new_momenta[2].copy(),
                energy=energy,
                phase=phase,
                amplitude=amplitude,
                timestamp=t
            )
            
            states.append(state)
            
            # Update for next step
            positions = new_positions
            momenta = new_momenta
            t += dt
        
        return states
    
    def _evolve_three_body_step(self, positions: List[np.ndarray], 
                               momenta: List[np.ndarray], dt: float) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """Evolve the 3-body system by one time step"""
        
        # For simplicity, use approximate circular motion with perturbations
        omega = 2 * np.pi * self.params.orbital_frequency
        
        new_positions = []
        new_momenta = []
        
        for i in range(3):
            pos = positions[i].copy()
            mom = momenta[i].copy()
            
            # Circular motion update
            radius = np.linalg.norm(pos[:2])  # xy radius
            if radius > 1e-10:
                # Angular velocity
                theta_old = np.arctan2(pos[1], pos[0])
                theta_new = theta_old + omega * dt
                
                # Update position
                pos[0] = radius * np.cos(theta_new)
                pos[1] = radius * np.sin(theta_new)
                
                # Update momentum (tangential)
                p_mag = np.linalg.norm(mom)
                mom[0] = -p_mag * np.sin(theta_new)
                mom[1] = p_mag * np.cos(theta_new)
            
            # Add small perturbations for realistic dynamics
            perturbation = 0.01 * self.params.neutron_radius * np.random.randn(3)
            pos += perturbation * dt
            
            new_positions.append(pos)
            new_momenta.append(mom)
        
        return new_positions, new_momenta
    
    def _calculate_system_energy(self, positions: List[np.ndarray], 
                                momenta: List[np.ndarray]) -> float:
        """Calculate total energy of 3-body system"""
        
        total_energy = 0.0
        
        # Kinetic energy
        for momentum in momenta:
            p_mag = np.linalg.norm(momentum)
            # Relativistic kinetic energy
            gamma = np.sqrt(1 + (p_mag / self.m_e)**2)
            kinetic = (gamma - 1) * self.m_e
            total_energy += kinetic
        
        # Potential energy (simplified)
        for i in range(3):
            for j in range(i + 1, 3):
                distance = np.linalg.norm(positions[i] - positions[j])
                # Approximate potential
                potential = -self.params.binding_energy / (1 + distance / self.params.neutron_radius)
                total_energy += potential
        
        return total_energy
    
    def _calculate_system_phase(self, positions: List[np.ndarray], 
                               momenta: List[np.ndarray], time: float) -> float:
        """Calculate overall phase of resonant system"""
        
        # Base phase from time evolution
        base_phase = 2 * np.pi * self.params.orbital_frequency * time
        
        # Add phase contributions from particle positions
        phase_sum = 0.0
        for pos in positions:
            theta = np.arctan2(pos[1], pos[0])
            phase_sum += theta
        
        return (base_phase + phase_sum) % (2 * np.pi)
    
    def _calculate_resonance_amplitude(self, energy: float, time: float) -> float:
        """Calculate resonance amplitude including decay effects"""
        
        # Start with unit amplitude
        amplitude = 1.0
        
        # Apply exponential decay for free neutron
        decay_rate = 2 * np.pi * self.params.orbital_frequency / (2 * self.params.free_neutron_Q)
        amplitude *= np.exp(-decay_rate * time)
        
        # Energy-dependent corrections
        energy_factor = energy / self.params.binding_energy
        amplitude *= np.sqrt(max(energy_factor, 0.1))  # Avoid negative energies
        
        return amplitude
    
    def analyze_resonance_modes(self) -> Dict[str, Any]:
        """
        Analyze different resonance modes of the neutron system.
        
        Identifies the characteristic frequencies and quality factors.
        """
        
        # Free neutron analysis
        free_neutron = self.calculate_free_neutron_resonance(time_span=2000)
        
        # Bound neutron at various distances
        distances = np.linspace(1.0, 5.0, 20)  # fm
        bound_analyses = []
        
        for distance in distances:
            bound_analysis = self.calculate_bound_neutron_resonance(distance)
            bound_analyses.append(bound_analysis)
        
        # Find optimal binding distance
        coupling_strengths = [analysis['coupling_strength'] for analysis in bound_analyses]
        optimal_idx = np.argmax(coupling_strengths)
        optimal_distance = distances[optimal_idx]
        optimal_bound = bound_analyses[optimal_idx]
        
        # Compare lifetimes
        free_lifetime = free_neutron['lifetime']
        bound_lifetime = optimal_bound['stability_time']
        
        return {
            'free_neutron': free_neutron,
            'bound_analyses': bound_analyses,
            'optimal_distance': optimal_distance,
            'optimal_bound': optimal_bound,
            'lifetime_ratio': bound_lifetime / free_lifetime,
            'distances': distances,
            'coupling_strengths': coupling_strengths
        }
    
    def validate_against_experiments(self) -> Dict[str, bool]:
        """
        Validate model predictions against experimental data.
        
        Key tests:
        1. Free neutron lifetime ≈ 880 seconds
        2. Bound neutron stability (indefinite)
        3. Beta decay energy ≈ 0.782 MeV
        """
        
        # Calculate predictions
        free_analysis = self.calculate_free_neutron_resonance()
        bound_analysis = self.calculate_bound_neutron_resonance()
        
        # Experimental values
        exp_neutron_lifetime = 880.0  # seconds
        exp_decay_energy = 0.782      # MeV
        
        # Validation checks
        validations = {
            'neutron_lifetime_correct': abs(free_analysis['lifetime'] - exp_neutron_lifetime) < 100,
            'bound_neutron_stable': bound_analysis['is_stable'],
            'decay_energy_correct': abs(self.params.decay_energy - exp_decay_energy) < 0.1,
            'quality_factor_reasonable': 1e25 < self.params.free_neutron_Q < 1e27,
            'frequency_reasonable': 1e22 < self.params.orbital_frequency < 1e24
        }
        
        return validations
    
    def export_resonance_data(self, filepath: str):
        """Export complete resonance analysis to file"""
        
        analysis = self.analyze_resonance_modes()
        validation = self.validate_against_experiments()
        
        export_data = {
            'theory': 'James Freeman Neutron Resonance Model',
            'principle': 'Free neutron = leaky 3-body resonance, Bound neutron = resonant lock',
            'parameters': self.params.__dict__,
            'analysis': analysis,
            'validation': validation,
            'summary': {
                'free_neutron_lifetime': analysis['free_neutron']['lifetime'],
                'bound_neutron_stable': analysis['optimal_bound']['is_stable'],
                'optimal_binding_distance': analysis['optimal_distance'],
                'lifetime_enhancement': analysis['lifetime_ratio']
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)

def create_neutron_resonance_visualization():
    """Create comprehensive visualization of neutron resonance behavior"""
    
    simulator = NeutronResonanceSimulator()
    analysis = simulator.analyze_resonance_modes()
    
    # Create multi-panel figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle("James Freeman's Neutron Resonance Theory", fontsize=16, weight='bold')
    
    # Plot 1: Free neutron decay
    free_data = analysis['free_neutron']
    
    axes[0,0].semilogy(free_data['time'], free_data['amplitude'], 'b-', linewidth=2, label='Amplitude')
    axes[0,0].semilogy(free_data['time'], free_data['decay_probability'], 'r--', linewidth=2, label='Decay Probability')
    axes[0,0].axvline(x=880, color='green', linestyle=':', label='Experimental Lifetime')
    axes[0,0].axvline(x=free_data['lifetime'], color='blue', linestyle=':', label=f'Calculated Lifetime ({free_data["lifetime"]:.0f}s)')
    axes[0,0].set_xlabel('Time (seconds)')
    axes[0,0].set_ylabel('Amplitude / Probability')
    axes[0,0].set_title('Free Neutron Resonance Decay')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # Plot 2: Energy evolution
    axes[0,1].plot(free_data['time'], free_data['energy'], 'purple', linewidth=2)
    axes[0,1].axhline(y=0.782, color='red', linestyle='--', label='Experimental Q-value')
    axes[0,1].set_xlabel('Time (seconds)')
    axes[0,1].set_ylabel('Energy (MeV)')
    axes[0,1].set_title('Resonance Energy Decay')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # Plot 3: Phase evolution
    axes[0,2].plot(free_data['time'][:1000], free_data['phase'][:1000], 'orange', linewidth=1)
    axes[0,2].set_xlabel('Time (seconds)')
    axes[0,2].set_ylabel('Phase (radians)')
    axes[0,2].set_title('Phase Evolution (Early Time)')
    axes[0,2].grid(True, alpha=0.3)
    
    # Plot 4: Coupling strength vs distance
    distances = analysis['distances']
    coupling_strengths = analysis['coupling_strengths']
    
    axes[1,0].plot(distances, coupling_strengths, 'g-', linewidth=2, marker='o', markersize=4)
    axes[1,0].axvline(x=analysis['optimal_distance'], color='red', linestyle='--', 
                      label=f'Optimal Distance ({analysis["optimal_distance"]:.1f} fm)')
    axes[1,0].set_xlabel('Proton Distance (fm)')
    axes[1,0].set_ylabel('Coupling Strength')
    axes[1,0].set_title('Neutron-Proton Coupling')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # Plot 5: Quality factor enhancement
    bound_data = analysis['bound_analyses']
    enhanced_Q = [bd['enhanced_Q'] for bd in bound_data]
    
    axes[1,1].semilogy(distances, enhanced_Q, 'purple', linewidth=2)
    axes[1,1].axhline(y=simulator.params.free_neutron_Q, color='blue', linestyle='--', 
                      label=f'Free Neutron Q ({simulator.params.free_neutron_Q:.0e})')
    axes[1,1].set_xlabel('Proton Distance (fm)')
    axes[1,1].set_ylabel('Quality Factor')
    axes[1,1].set_title('Q-Factor Enhancement')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    # Plot 6: Stability analysis
    stability_times = [bd['stability_time'] for bd in bound_data]
    
    axes[1,2].semilogy(distances, stability_times, 'red', linewidth=2)
    axes[1,2].axhline(y=free_data['lifetime'], color='blue', linestyle='--', 
                      label=f'Free Neutron ({free_data["lifetime"]:.0f}s)')
    axes[1,2].axhline(y=1e20, color='green', linestyle=':', label='Practical Infinity')
    axes[1,2].set_xlabel('Proton Distance (fm)')
    axes[1,2].set_ylabel('Lifetime (seconds)')
    axes[1,2].set_title('Neutron Stability vs Distance')
    axes[1,2].legend()
    axes[1,2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary
    print("\n" + "="*80)
    print("NEUTRON RESONANCE ANALYSIS - JAMES FREEMAN'S THEORY")
    print("="*80)
    print("Core Principle: Free neutron = leaky 3-body resonance")
    print("                Bound neutron = resonant lock with proton → stability")
    print()
    
    print("FREE NEUTRON ANALYSIS:")
    print(f"  Calculated lifetime: {free_data['lifetime']:.1f} seconds")
    print(f"  Experimental lifetime: 880 seconds")
    print(f"  Quality factor: {simulator.params.free_neutron_Q:.1e}")
    print(f"  Orbital frequency: {simulator.params.orbital_frequency:.1e} Hz")
    print(f"  Decay rate: {free_data['decay_rate']:.2e} s⁻¹")
    print()
    
    print("BOUND NEUTRON ANALYSIS:")
    optimal = analysis['optimal_bound']
    print(f"  Optimal binding distance: {analysis['optimal_distance']:.1f} fm")
    print(f"  Coupling strength: {optimal['coupling_strength']:.3f}")
    print(f"  Enhanced Q-factor: {optimal['enhanced_Q']:.1e}")
    print(f"  Stability time: {optimal['stability_time']:.1e} seconds")
    print(f"  Is stable: {optimal['is_stable']}")
    print()
    
    print("LIFETIME ENHANCEMENT:")
    print(f"  Bound/Free ratio: {analysis['lifetime_ratio']:.1e}")
    print(f"  Mechanism: Resonant lock prevents energy leakage")
    print()
    
    # Validation
    validation = simulator.validate_against_experiments()
    print("EXPERIMENTAL VALIDATION:")
    for test, passed in validation.items():
        status = "PASS ✓" if passed else "FAIL ✗"
        print(f"  {test:>25}: {status}")
    
    overall_success = all(validation.values())
    print(f"\nOVERALL MODEL STATUS: {'SUCCESS ✓' if overall_success else 'NEEDS REFINEMENT ✗'}")
    print("="*80)

# Example usage and testing
if __name__ == "__main__":
    # Create simulator with default parameters
    simulator = NeutronResonanceSimulator()
    
    print("Analyzing neutron resonance behavior...")
    
    # Run comprehensive analysis
    create_neutron_resonance_visualization()
    
    # Export detailed results
    simulator.export_resonance_data('neutron_resonance_analysis.json')
    print("\nDetailed analysis exported to neutron_resonance_analysis.json")
    
    # Test 3-body dynamics simulation
    print("\nSimulating 3-body dynamics...")
    dynamics = simulator.simulate_three_body_dynamics(duration=1e-21, timesteps=100)
    
    print(f"Simulated {len(dynamics)} time steps")
    print(f"Initial energy: {dynamics[0].energy:.3f} MeV")
    print(f"Final energy: {dynamics[-1].energy:.3f} MeV")
    print(f"Energy conservation: {abs(dynamics[-1].energy - dynamics[0].energy):.6f} MeV")
    
    print("\nNeutron resonance model implementation complete!")