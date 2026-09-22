#!/usr/bin/env python3
"""
Pure Freeman Wave Interference Theory Test
==========================================

This implementation tests Freeman's theory WITHOUT any artificial shell preferences.
Only uses:
1. Nuclear attraction (Coulomb's law with screening)  
2. Electron-electron repulsion (Coulomb repulsion)
3. Freeman's wave interference (λₙ = 4·eⁿ/π)

NO hardcoded shell preferences, energy wells, or other artificial constraints.
This is the real test of whether Freeman's theory can predict atomic structure
from first principles.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, differential_evolution
import math

class Pure_Freeman_Theory_Test:
    def __init__(self, repulsion_strength=1.0, interference_strength=1.0):
        """
        Initialize with tunable physics parameters.
        These are the ONLY parameters we can adjust - no artificial shell preferences.
        """
        self.repulsion_strength = repulsion_strength
        self.interference_strength = interference_strength
        
        # Freeman's wavelength formula: λₙ = 4·eⁿ/π
        self.harmonics = [0, 1, 2, 3, 4]
        self.wavelengths = {}
        self.energies = {}
        self.e = math.e
        self.pi = math.pi
        
        print("PURE FREEMAN WAVE INTERFERENCE THEORY TEST")
        print("=" * 50)
        print("Testing ONLY:")
        print("  1. Nuclear attraction (screened Coulomb)")
        print("  2. Electron repulsion (Coulomb)")  
        print("  3. Freeman's wave interference (λₙ = 4·eⁿ/π)")
        print("NO artificial shell preferences or energy wells!")
        print(f"Parameters: repulsion={repulsion_strength:.2f}, interference={interference_strength:.2f}")
        
        # Calculate Freeman's wavelength progression
        for n in self.harmonics:
            self.wavelengths[n] = 4.0 * (self.e ** n) / self.pi
            self.energies[n] = 1.0 / self.wavelengths[n]
        
        # Normalize energies
        total_energy = sum(self.energies.values())
        for n in self.harmonics:
            self.energies[n] /= total_energy
            
        print("\nFreeman's Wavelength Progression:")
        for n in self.harmonics:
            print(f"  λ_{n} = {self.wavelengths[n]:.3f}, E_{n} = {self.energies[n]:.6f}")
        print()
    
    def freeman_wave_interference(self, test_position, electron_positions):
        """
        Calculate Freeman's multi-harmonic wave interference field.
        This is the CORE of Freeman's theory - the only non-classical physics.
        """
        if not electron_positions:
            return 0.0
            
        total_wave = 0.0
        
        for electron_pos in electron_positions:
            distance = np.linalg.norm(test_position - electron_pos)
            if distance < 1e-10:
                continue
                
            # Freeman's multi-harmonic wave field
            for n in self.harmonics:
                wavelength = self.wavelengths[n]
                energy = self.energies[n]
                
                # Wave equation: E * sin(2π * distance / λ) / distance
                wave_component = energy * np.sin(2 * self.pi * distance / wavelength) / distance
                total_wave += wave_component
        
        return abs(total_wave)**2  # |ψ|²
    
    def total_energy_at_position(self, position, existing_electrons, Z_eff):
        """
        Total energy function - the heart of the theory.
        ONLY includes fundamental physics - no artificial preferences.
        """
        pos = np.array(position)
        radius = np.linalg.norm(pos)
        
        # 1. Nuclear attraction with screening (standard quantum chemistry)
        if radius < 1e-10:
            nuclear_energy = -1000  # Strong attraction at nucleus
        else:
            nuclear_energy = -Z_eff / radius
        
        # 2. Electron-electron repulsion (classical Coulomb repulsion)
        repulsion_energy = 0.0
        for electron_pos in existing_electrons:
            distance = np.linalg.norm(pos - electron_pos)
            if distance > 1e-10:
                repulsion_energy += self.repulsion_strength / distance
            else:
                repulsion_energy += 1000.0  # Huge penalty for overlap
        
        # 3. Freeman's wave interference (the new physics being tested)
        interference_field = self.freeman_wave_interference(pos, existing_electrons)
        interference_energy = self.interference_strength * interference_field
        
        # Total energy - NO artificial shell preferences
        total = nuclear_energy + repulsion_energy + interference_energy
        
        return total
    
    def find_optimal_electron_position(self, existing_electrons, Z_eff, verbose=False):
        """
        Find the optimal position for the next electron using pure physics.
        No guidance toward specific shell radii.
        """
        if not existing_electrons:
            return np.array([1.0, 0.0, 0.0])  # Hydrogen trivial case
        
        if verbose:
            print(f"  Finding optimal position for electron #{len(existing_electrons)+1}")
            print(f"  Z_eff = {Z_eff:.2f}")
        
        # Search over a wide range of radii with no bias
        search_radii = np.linspace(0.3, 12.0, 150)
        
        best_energy = float('inf')
        best_position = None
        energies_at_radii = []
        
        for radius in search_radii:
            min_energy_at_radius = float('inf')
            best_pos_at_radius = None
            
            # Sample angular positions thoroughly
            n_angles = 36
            n_phi = 6
            
            for i in range(n_angles):
                theta = 2 * math.pi * i / n_angles
                
                for j in range(n_phi):
                    if n_phi == 1:
                        phi = math.pi / 2  # Equatorial plane
                    else:
                        phi = math.pi * j / (n_phi - 1)
                    
                    # Convert to Cartesian coordinates
                    x = radius * math.sin(phi) * math.cos(theta)
                    y = radius * math.sin(phi) * math.sin(theta)
                    z = radius * math.cos(phi)
                    
                    position = np.array([x, y, z])
                    energy = self.total_energy_at_position(position, existing_electrons, Z_eff)
                    
                    if energy < min_energy_at_radius:
                        min_energy_at_radius = energy
                        best_pos_at_radius = position.copy()
            
            energies_at_radii.append(min_energy_at_radius)
            
            if min_energy_at_radius < best_energy:
                best_energy = min_energy_at_radius
                best_position = best_pos_at_radius.copy()
        
        optimal_radius = np.linalg.norm(best_position)
        if verbose:
            print(f"  → Optimal radius: {optimal_radius:.3f}, Energy: {best_energy:.6f}")
        
        return best_position, best_energy, search_radii, energies_at_radii
    
    def build_atom_sequentially(self, atomic_number, verbose=True):
        """
        Build atom by adding electrons one by one.
        Uses ONLY pure physics - no artificial guidance.
        """
        if verbose:
            print(f"\n=== BUILDING ATOM Z={atomic_number} ===")
        
        electrons = []
        energy_landscapes = []
        
        for electron_num in range(1, atomic_number + 1):
            if verbose:
                print(f"\nElectron #{electron_num}:")
            
            if electron_num == 1:
                # Hydrogen: trivial case
                position = np.array([1.0, 0.0, 0.0])
                if verbose:
                    print(f"  Hydrogen: r=1.0")
                
            else:
                # Calculate effective nuclear charge with simple screening
                Z_eff = max(1.0, atomic_number - 0.3 * (electron_num - 1))
                
                # Find optimal position using pure physics
                result = self.find_optimal_electron_position(electrons, Z_eff, verbose)
                position, energy, radii, energies = result
                
                # Store energy landscape for analysis
                energy_landscapes.append({
                    'electron_num': electron_num,
                    'radii': radii,
                    'energies': energies,
                    'optimal_radius': np.linalg.norm(position),
                    'optimal_energy': energy
                })
            
            electrons.append(position)
        
        return electrons, energy_landscapes
    
    def determine_shells_from_positions(self, electrons):
        """
        Determine shell structure based purely on radial distances.
        Uses natural clustering of electron positions, not predetermined boundaries.
        """
        if not electrons:
            return []
        
        radii = [np.linalg.norm(pos) for pos in electrons]
        radii.sort()
        
        # Find natural gaps in radial distribution to define shells
        shell_assignments = []
        current_shell = 1
        shell_boundary_threshold = 2.0  # Minimum gap to define new shell
        
        for i, radius in enumerate([np.linalg.norm(pos) for pos in electrons]):
            # Determine shell based on position in sorted radii
            shell = 1
            for j, sorted_r in enumerate(radii[:-1]):
                if radii[j+1] - sorted_r > shell_boundary_threshold:
                    if radius > sorted_r:
                        shell += 1
            shell_assignments.append(min(shell, 5))  # Cap at shell 5
        
        # Count electrons per shell
        shell_counts = [0, 0, 0, 0, 0]
        for shell in shell_assignments:
            if shell <= 5:
                shell_counts[shell-1] += 1
        
        return shell_counts, shell_assignments
    
    def analyze_configuration(self, electrons, atomic_number, verbose=True):
        """
        Analyze the electron configuration WITHOUT using predetermined shell boundaries.
        """
        if verbose:
            print(f"\n=== ANALYZING Z={atomic_number} CONFIGURATION ===")
        
        # Determine shells from natural clustering
        shell_counts, shell_assignments = self.determine_shells_from_positions(electrons)
        
        if verbose:
            print("Electron positions and shell assignments:")
            for i, (pos, shell) in enumerate(zip(electrons, shell_assignments)):
                radius = np.linalg.norm(pos)
                print(f"  Electron {i+1}: r={radius:.3f} → Shell {shell}")
        
        # Expected configurations (known quantum mechanical results)
        expected_configs = {
            1: [1, 0, 0, 0, 0], 2: [2, 0, 0, 0, 0], 3: [2, 1, 0, 0, 0], 4: [2, 2, 0, 0, 0],
            5: [2, 3, 0, 0, 0], 6: [2, 4, 0, 0, 0], 7: [2, 5, 0, 0, 0], 8: [2, 6, 0, 0, 0],
            9: [2, 7, 0, 0, 0], 10: [2, 8, 0, 0, 0], 11: [2, 8, 1, 0, 0], 12: [2, 8, 2, 0, 0],
            13: [2, 8, 3, 0, 0], 14: [2, 8, 4, 0, 0], 15: [2, 8, 5, 0, 0], 16: [2, 8, 6, 0, 0],
            17: [2, 8, 7, 0, 0], 18: [2, 8, 8, 0, 0]
        }
        
        expected = expected_configs.get(atomic_number, [0, 0, 0, 0, 0])
        
        # Calculate accuracy
        correct_electrons = sum(min(shell_counts[i], expected[i]) for i in range(5))
        accuracy = (correct_electrons / atomic_number) * 100 if atomic_number > 0 else 0
        
        if verbose:
            print(f"\nShell Configuration:")
            print(f"  Predicted: {shell_counts}")
            print(f"  Expected:  {expected}")
            match_status = "✓" if shell_counts == expected else "✗"
            print(f"  Accuracy: {accuracy:.1f}% {match_status}")
        
        return {
            'shell_counts': shell_counts,
            'expected': expected,
            'accuracy': accuracy,
            'shell_assignments': shell_assignments,
            'positions': electrons
        }
    
    def plot_energy_landscape(self, electron_num, radii, energies, optimal_radius, element_name):
        """Plot the energy landscape for a specific electron addition"""
        plt.figure(figsize=(10, 6))
        
        plt.plot(radii, energies, 'b-', linewidth=2, label='Total Energy')
        
        # Mark the optimal position
        optimal_idx = np.argmin(np.abs(radii - optimal_radius))
        plt.scatter([optimal_radius], [energies[optimal_idx]], 
                   color='red', s=100, zorder=5, label=f'Optimal: r={optimal_radius:.2f}')
        
        plt.xlabel('Radius (Bohr radii)')
        plt.ylabel('Energy (Hartree)')
        plt.title(f'{element_name} - Electron #{electron_num} Energy Landscape (Pure Freeman Theory)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Add note about what this represents
        plt.figtext(0.02, 0.02, 
                   'Note: This uses ONLY nuclear attraction + electron repulsion + Freeman wave interference',
                   fontsize=9, style='italic')
        
        plt.tight_layout()
        plt.show()
    
    def analyze_energy_components(self, position, existing_electrons, Z_eff):
        """Break down the energy into its components for analysis"""
        pos = np.array(position)
        radius = np.linalg.norm(pos)
        
        # Nuclear attraction
        nuclear = -Z_eff / radius if radius > 1e-10 else -1000
        
        # Electron repulsion
        repulsion = 0.0
        for electron_pos in existing_electrons:
            distance = np.linalg.norm(pos - electron_pos)
            if distance > 1e-10:
                repulsion += self.repulsion_strength / distance
        
        # Wave interference
        interference_field = self.freeman_wave_interference(pos, existing_electrons)
        interference = self.interference_strength * interference_field
        
        total = nuclear + repulsion + interference
        
        return {
            'Nuclear attraction': nuclear,
            'Electron repulsion': repulsion,
            'Freeman wave interference': interference,
            'Total': total
        }

def run_pure_freeman_test():
    """
    Run the pure Freeman theory test on multiple elements.
    This will show us what Freeman's theory actually predicts without cheating.
    """
    # Test with default physics parameters
    tester = Pure_Freeman_Theory_Test(repulsion_strength=1.0, interference_strength=1.0)
    
    # Test elements
    elements = [
        (1, "Hydrogen"), (2, "Helium"), (3, "Lithium"), (4, "Beryllium"),
        (5, "Boron"), (6, "Carbon"), (7, "Nitrogen"), (8, "Oxygen"),
        (9, "Fluorine"), (10, "Neon")
    ]
    
    print("\n" + "="*70)
    print("PURE FREEMAN THEORY TEST RESULTS")
    print("="*70)
    print("Testing Freeman's wave interference theory WITHOUT artificial shell preferences")
    print("Only using: Nuclear attraction + Electron repulsion + Freeman wave interference")
    print("="*70)
    
    results = []
    total_accuracy = 0
    
    for atomic_number, element_name in elements:
        print(f"\n{'='*20} {element_name.upper()} (Z={atomic_number}) {'='*20}")
        
        # Build atom using pure Freeman theory
        electrons, energy_landscapes = tester.build_atom_sequentially(atomic_number, verbose=True)
        
        # Analyze configuration
        analysis = tester.analyze_configuration(electrons, atomic_number, verbose=True)
        
        results.append({
            'element': element_name,
            'Z': atomic_number,
            'predicted': analysis['shell_counts'],
            'expected': analysis['expected'],
            'accuracy': analysis['accuracy']
        })
        
        total_accuracy += analysis['accuracy']
        
        # Plot energy landscapes for problematic cases
        if analysis['accuracy'] < 100 and energy_landscapes:
            print(f"\nEnergy landscape analysis for {element_name}:")
            for landscape in energy_landscapes[-2:]:  # Last 2 electrons
                tester.plot_energy_landscape(
                    landscape['electron_num'], landscape['radii'], 
                    landscape['energies'], landscape['optimal_radius'], element_name
                )
    
    # Summary
    avg_accuracy = total_accuracy / len(elements)
    
    print("\n" + "="*70)
    print("PURE FREEMAN THEORY TEST SUMMARY")
    print("="*70)
    print(f"{'Element':<12} | {'Predicted Config':<18} | {'Expected Config':<18} | {'Accuracy':<8}")
    print("-" * 70)
    
    for result in results:
        pred_str = str(result['predicted'])
        exp_str = str(result['expected'])
        acc = result['accuracy']
        match_symbol = "✓" if result['predicted'] == result['expected'] else "✗"
        
        print(f"{result['element']:<12} | {pred_str:<18} | {exp_str:<18} | {acc:>6.1f}% {match_symbol}")
    
    print("-" * 70)
    print(f"{'AVERAGE':<12} | {'':<18} | {'':<18} | {avg_accuracy:>6.1f}%")
    print("="*70)
    
    # Analysis
    print("\nRESULT ANALYSIS:")
    if avg_accuracy >= 80:
        print(f"HIGH ACCURACY ({avg_accuracy:.1f}%): Freeman's pure theory shows strong predictive power!")
        print("The wave interference mechanism successfully creates shell structure.")
    elif avg_accuracy >= 50:
        print(f"MODERATE ACCURACY ({avg_accuracy:.1f}%): Freeman's theory shows partial success.")
        print("Wave interference contributes to shell structure but is insufficient alone.")
    else:
        print(f"LOW ACCURACY ({avg_accuracy:.1f}%): Freeman's pure theory struggles to predict shell structure.")
        print("Additional physics beyond wave interference appears necessary.")
    
    print(f"\nKey findings:")
    print(f"- Pure Freeman theory (no artificial shell preferences) achieves {avg_accuracy:.1f}% average accuracy")
    print(f"- This represents what the theory actually predicts from first principles")
    print(f"- Any higher accuracy claims likely involve artificial constraints")
    
    return results, avg_accuracy

def parameter_sweep_test():
    """
    Test different parameter combinations to find optimal physics balance.
    This explores whether there exists parameter values that make Freeman's theory work.
    """
    print("\n" + "="*60)
    print("PARAMETER SWEEP TEST")
    print("="*60)
    print("Testing different repulsion/interference strength combinations...")
    
    # Parameter ranges to test
    repulsion_values = [0.5, 1.0, 2.0, 5.0]
    interference_values = [0.1, 0.5, 1.0, 2.0, 5.0]
    
    best_accuracy = 0
    best_params = (1.0, 1.0)
    
    test_elements = [(2, "Helium"), (3, "Lithium"), (4, "Beryllium"), (8, "Oxygen")]
    
    print(f"Testing {len(repulsion_values) * len(interference_values)} parameter combinations on 4 elements...")
    
    for rep_strength in repulsion_values:
        for int_strength in interference_values:
            tester = Pure_Freeman_Theory_Test(rep_strength, int_strength)
            
            total_acc = 0
            count = 0
            
            for atomic_number, element_name in test_elements:
                electrons, _ = tester.build_atom_sequentially(atomic_number, verbose=False)
                analysis = tester.analyze_configuration(electrons, atomic_number, verbose=False)
                total_acc += analysis['accuracy']
                count += 1
            
            avg_acc = total_acc / count if count > 0 else 0
            print(f"  Rep={rep_strength:.1f}, Int={int_strength:.1f}: {avg_acc:.1f}% accuracy")
            
            if avg_acc > best_accuracy:
                best_accuracy = avg_acc
                best_params = (rep_strength, int_strength)
    
    print(f"\nBest parameters found:")
    print(f"  Repulsion strength: {best_params[0]}")
    print(f"  Interference strength: {best_params[1]}")  
    print(f"  Best accuracy: {best_accuracy:.1f}%")
    
    if best_accuracy > 60:
        print(f"\nRunning full test with optimized parameters...")
        tester = Pure_Freeman_Theory_Test(best_params[0], best_params[1])
        return run_pure_freeman_test_with_tester(tester)
    else:
        print(f"\nEven with optimized parameters, accuracy remains low.")
        print(f"This suggests fundamental limitations in Freeman's pure theory.")
    
    return best_params, best_accuracy

def run_pure_freeman_test_with_tester(tester):
    """Run the test with a specific tester instance"""
    elements = [(1, "Hydrogen"), (2, "Helium"), (3, "Lithium"), (4, "Beryllium"),
                (5, "Boron"), (6, "Carbon"), (7, "Nitrogen"), (8, "Oxygen")]
    
    results = []
    total_accuracy = 0
    
    for atomic_number, element_name in elements:
        electrons, _ = tester.build_atom_sequentially(atomic_number, verbose=False)
        analysis = tester.analyze_configuration(electrons, atomic_number, verbose=False)
        
        results.append({
            'element': element_name,
            'predicted': analysis['shell_counts'],
            'expected': analysis['expected'],
            'accuracy': analysis['accuracy']
        })
        
        total_accuracy += analysis['accuracy']
    
    avg_accuracy = total_accuracy / len(elements)
    
    print(f"Optimized parameters result: {avg_accuracy:.1f}% average accuracy")
    return results, avg_accuracy

if __name__ == "__main__":
    print("FREEMAN WAVE INTERFERENCE THEORY - PURE PHYSICS TEST")
    print("="*60)
    print("This test uses ONLY the physics Freeman proposed:")
    print("1. Standard nuclear attraction (Coulomb)")
    print("2. Standard electron repulsion (Coulomb)")  
    print("3. Freeman's wave interference (λₙ = 4·eⁿ/π)")
    print("\nNO artificial shell preferences or predetermined energy wells.")
    print("This will show what Freeman's theory actually predicts.\n")
    
    # Run the main test
    results, accuracy = run_pure_freeman_test()
    
    print(f"\n{'='*60}")
    print(f"CONCLUSION:")
    print(f"Pure Freeman theory achieves {accuracy:.1f}% accuracy without artificial constraints.")
    print(f"This represents the true predictive power of his wave interference mechanism.")
    
    # If accuracy is low, try parameter optimization
    if accuracy < 60:
        print(f"\nSince accuracy is low, testing parameter optimization...")
        parameter_sweep_test()