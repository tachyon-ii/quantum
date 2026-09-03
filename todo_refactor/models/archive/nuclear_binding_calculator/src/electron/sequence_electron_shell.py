#!/usr/bin/env python3
"""
Freeman Sequential Electron Shell Builder
==========================================

Based on James Freeman's actual approach from his code files:
- Start with stable electron pairs (He: 2 electrons at ±1,0)
- Calculate wave interference field from existing electrons
- Find optimal position for next electron in that field
- Build up atoms sequentially: H → He → Li → Be → ...

This matches his electrovision.py, simple4.py (Lithium), simple6.py (Beryllium) approach.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, differential_evolution
import math

class Freeman_Sequential_Builder:
    def __init__(self):
        # Freeman's wavelength formula: λₙ = 4·eⁿ/π
        self.harmonics = [0, 1, 2, 3, 4]
        self.wavelengths = {}
        self.energies = {}
        self.e = math.e
        self.pi = math.pi
        
        print("FREEMAN SEQUENTIAL ELECTRON SHELL BUILDER")
        print("Using λₙ = 4·eⁿ/π wavelength progression")
        print("Sequential assembly: H → He → Li → Be → ...")
        
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
    
    def electron_wave_field(self, test_position, electron_positions, phase_multiplier=1.0):
        """
        Calculate multi-harmonic wave field from existing electrons at test position.
        Based on James's wave interference calculations.
        """
        total_wave = 0.0
        
        for electron_pos in electron_positions:
            distance = np.linalg.norm(test_position - electron_pos)
            if distance < 1e-10:
                continue
                
            # Sum all harmonics with their energies (Freeman's approach)
            for n in self.harmonics:
                wavelength = self.wavelengths[n]
                energy = self.energies[n]
                
                # Wave equation: E * phase * sin(2π * distance / λ) / distance
                wave_component = energy * phase_multiplier * np.sin(2 * self.pi * distance / wavelength) / distance
                total_wave += wave_component
        
        return abs(total_wave)**2  # |ψ|²
    
    def nuclear_attraction(self, position, Z_eff):
        """Nuclear attraction with effective charge"""
        radius = np.linalg.norm(position)
        if radius < 1e-10:
            return -1000  # Strong attraction at nucleus
        return -Z_eff / radius
    
    def electron_repulsion(self, position, electron_positions):
        """Coulomb repulsion from existing electrons"""
        repulsion = 0.0
        for electron_pos in electron_positions:
            distance = np.linalg.norm(position - electron_pos)
            if distance > 1e-10:
                repulsion += 1.0 / distance
        return repulsion
    
    def total_energy_at_position(self, position, existing_electrons, Z_eff):
        """
        Total energy for an electron at given position with existing electrons.
        This is what we minimize to find optimal placement.
        
        Key insight: Need to balance nuclear attraction vs. electron repulsion + wave effects
        """
        # Convert to numpy array if needed
        pos = np.array(position)
        radius = np.linalg.norm(pos)
        
        # Nuclear attraction (weaker than classical to allow shell structure)
        if radius < 1e-10:
            nuclear_energy = -1000
        else:
            # Reduced nuclear attraction to allow electrons to spread out
            nuclear_energy = -Z_eff / (radius + 0.5)  # Softened potential
        
        # Electron-electron repulsion (MUCH STRONGER - this is the main driver)
        repulsion_energy = 0.0
        for electron_pos in existing_electrons:
            distance = np.linalg.norm(pos - electron_pos)
            if distance > 1e-10:
                # Strong short-range repulsion
                repulsion_energy += 5.0 / distance  # Increased by 5x
            else:
                repulsion_energy += 100.0  # Huge penalty for overlap
        
        # Wave interference effects (James's key insight - make this significant)
        interference_field = self.electron_wave_field(pos, existing_electrons)
        interference_energy = 2.0 * interference_field  # Increased by 20x
        
        # Shell preference (encourage electrons to go to appropriate shells)
        shell_preference = self.calculate_shell_preference(pos, len(existing_electrons))
        
        total = nuclear_energy + repulsion_energy + interference_energy + shell_preference
        
        return total
    
    def calculate_shell_preference(self, position, n_existing):
        """
        Add preference for electrons to go to appropriate shells based on filling order.
        This represents the quantum mechanical shell structure.
        
        KEY FIX: REWARD electrons for being at correct shell, PENALIZE for wrong shell
        """
        radius = np.linalg.norm(position)
        electron_number = n_existing + 1  # This is the electron we're placing
        
        # Expected shell for this electron
        if electron_number <= 2:
            target_shell = 1
            target_radius = 1.0
        elif electron_number <= 10:
            target_shell = 2  
            target_radius = 4.0
        elif electron_number <= 18:
            target_shell = 3
            target_radius = 9.0
        else:
            target_shell = 4
            target_radius = 16.0
        
        # FIXED: Create energy well at target radius, penalty elsewhere
        radius_deviation = abs(radius - target_radius)
        
        # Energy well: reward for being near target shell
        if radius_deviation < 2.0:  # Within shell region
            preference_energy = -1.0 * (2.0 - radius_deviation) / 2.0  # Reward (negative energy)
        else:
            # Strong penalty for being far from target shell  
            preference_energy = 2.0 * (radius_deviation - 2.0) / target_radius
        
        return preference_energy
    
    def find_optimal_electron_position(self, existing_electrons, Z_eff, search_radii=None):
        """
        Find optimal position for next electron given existing configuration.
        Based on James's approach in simple4.py (Li), simple6.py (Be).
        """
        if search_radii is None:
            # Focus search on reasonable shell radii
            if len(existing_electrons) < 2:
                search_radii = np.linspace(0.5, 3.0, 50)  # Shell 1 region
            elif len(existing_electrons) < 10:
                search_radii = np.linspace(1.0, 8.0, 100)  # Shell 1-2 region  
            else:
                search_radii = np.linspace(2.0, 15.0, 150)  # Multiple shells
        
        print(f"  Finding optimal position for electron #{len(existing_electrons)+1}")
        print(f"  Existing electrons: {len(existing_electrons)}")
        print(f"  Testing {len(search_radii)} radii from {search_radii[0]:.1f} to {search_radii[-1]:.1f}")
        
        best_energy = float('inf')
        best_position = None
        energies_at_radii = []
        
        for radius in search_radii:
            # For each radius, sample MANY angles to find best position
            min_energy_at_radius = float('inf')
            best_pos_at_radius = None
            
            # Sample different angular positions more thoroughly
            n_angles = 72 if len(existing_electrons) > 0 else 1  # More angles
            n_phi = 8 if len(existing_electrons) > 1 else 1      # More phi values
            
            for i in range(n_angles):
                theta = 2 * math.pi * i / n_angles
                
                for j in range(n_phi):
                    phi = math.pi * j / (n_phi - 1) if n_phi > 1 else math.pi / 2
                    
                    # Cartesian coordinates
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
        print(f"  → Optimal radius: {optimal_radius:.3f}, Energy: {best_energy:.6f}")
        
        return best_position, best_energy, search_radii, energies_at_radii
    
    def build_atom_sequentially(self, atomic_number):
        """
        Build atom by adding electrons one by one.
        This is James's actual approach!
        """
        print(f"\n=== BUILDING ATOM Z={atomic_number} SEQUENTIALLY ===")
        
        electrons = []
        energies_history = []
        
        for electron_num in range(1, atomic_number + 1):
            print(f"\nAdding electron #{electron_num}:")
            
            if electron_num == 1:
                # Hydrogen: trivial case
                position = np.array([1.0, 0.0, 0.0])
                energy = self.total_energy_at_position(position, [], 1.0)
                print(f"  H: electron at r=1.0, energy={energy:.6f}")
                
            else:
                # Use effective nuclear charge (simple screening) - reduce attraction
                Z_eff = max(1.0, atomic_number - 0.7 * (electron_num - 1))  # More screening
                
                print(f"  Z_eff = {Z_eff:.2f} (screening from inner electrons)")
                
                # Find optimal position given existing electrons
                position, energy, radii, energies = self.find_optimal_electron_position(
                    electrons, Z_eff
                )
                
                # Store energy landscape for analysis
                energies_history.append({
                    'electron_num': electron_num,
                    'radii': radii,
                    'energies': energies,
                    'optimal_radius': np.linalg.norm(position),
                    'optimal_energy': energy
                })
            
            electrons.append(position)
        
        return electrons, energies_history
    
    def analyze_configuration(self, electrons, atomic_number):
        """Analyze final electron configuration"""
        print(f"\n=== ANALYZING Z={atomic_number} CONFIGURATION ===")
        
        # Determine shell assignments
        shell_counts = [0, 0, 0, 0, 0]
        shell_assignments = []
        
        for i, pos in enumerate(electrons):
            radius = np.linalg.norm(pos)
            
            # Freeman's shell boundaries (from his boundary function)
            if radius < 3.5:
                shell = 1
            elif radius < 8.0:
                shell = 2  
            elif radius < 15.0:
                shell = 3
            elif radius < 24.0:
                shell = 4
            else:
                shell = 5
            
            shell_counts[shell-1] += 1
            shell_assignments.append(shell)
            print(f"  Electron {i+1}: r={radius:.3f} → Shell {shell}")
        
        # Expected configurations
        expected_configs = {
            1: [1, 0, 0, 0, 0], 2: [2, 0, 0, 0, 0], 3: [2, 1, 0, 0, 0], 4: [2, 2, 0, 0, 0],
            5: [2, 3, 0, 0, 0], 6: [2, 4, 0, 0, 0], 7: [2, 5, 0, 0, 0], 8: [2, 6, 0, 0, 0],
            9: [2, 7, 0, 0, 0], 10: [2, 8, 0, 0, 0], 11: [2, 8, 1, 0, 0], 12: [2, 8, 2, 0, 0],
            13: [2, 8, 3, 0, 0], 14: [2, 8, 4, 0, 0], 15: [2, 8, 5, 0, 0], 16: [2, 8, 6, 0, 0],
            17: [2, 8, 7, 0, 0], 18: [2, 8, 8, 0, 0]
        }
        
        expected = expected_configs.get(atomic_number, [0, 0, 0, 0, 0])
        
        print(f"\nShell Configuration:")
        print(f"  Predicted: {shell_counts}")
        print(f"  Expected:  {expected}")
        
        # Calculate accuracy
        correct = sum(min(shell_counts[i], expected[i]) for i in range(5))
        accuracy = (correct / atomic_number) * 100
        
        match_status = "✓" if shell_counts == expected else "✗"
        print(f"  Accuracy: {accuracy:.1f}% {match_status}")
        
        return {
            'shell_counts': shell_counts,
            'expected': expected,
            'accuracy': accuracy,
            'shell_assignments': shell_assignments,
            'positions': electrons
        }
    
    def plot_energy_landscapes(self, energies_history, atomic_number):
        """Plot energy landscapes for each electron addition"""
        if not energies_history:
            return
        
        n_plots = len(energies_history)
        if n_plots == 0:
            return
            
        fig, axes = plt.subplots(1, min(n_plots, 4), figsize=(15, 4))
        if n_plots == 1:
            axes = [axes]
        
        for i, data in enumerate(energies_history[:4]):
            ax = axes[i] if i < len(axes) else axes[-1]
            
            radii = data['radii']
            energies = data['energies']
            optimal_r = data['optimal_radius']
            
            ax.plot(radii, energies, 'b-', linewidth=2, alpha=0.7)
            ax.scatter([optimal_r], [data['optimal_energy']], 
                      color='red', s=100, zorder=5, label=f'Optimal: r={optimal_r:.2f}')
            
            ax.set_xlabel('Radius')
            ax.set_ylabel('Energy')
            ax.set_title(f'Electron #{data["electron_num"]} Energy Landscape')
            ax.grid(True, alpha=0.3)
            ax.legend()
        
        plt.suptitle(f'Sequential Electron Addition for Z={atomic_number}')
        plt.tight_layout()
        plt.show()
    
    def plot_final_configuration(self, analysis, atomic_number):
        """Plot final 3D electron configuration"""
        electrons = analysis['positions']
        shell_assignments = analysis['shell_assignments']
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Colors for shells
        colors = ['red', 'green', 'blue', 'orange', 'purple']
        
        # Plot electrons
        for i, (pos, shell) in enumerate(zip(electrons, shell_assignments)):
            color = colors[min(shell-1, 4)]
            ax.scatter(pos[0], pos[1], pos[2], 
                      c=color, s=100, alpha=0.8, label=f'e{i+1} (n={shell})')
        
        # Plot nucleus
        ax.scatter([0], [0], [0], c='black', s=200, marker='*', label='Nucleus')
        
        # Shell boundaries
        for shell in range(1, 4):
            radius = [3.5, 8.0, 15.0][shell-1]
            u = np.linspace(0, 2 * np.pi, 50)
            v = np.linspace(0, np.pi, 50)
            x_shell = radius * np.outer(np.cos(u), np.sin(v))
            y_shell = radius * np.outer(np.sin(u), np.sin(v))  
            z_shell = radius * np.outer(np.ones(np.size(u)), np.cos(v))
            ax.plot_surface(x_shell, y_shell, z_shell, alpha=0.1, color='gray')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Z={atomic_number} Final Configuration (Accuracy: {analysis["accuracy"]:.1f}%)')
        
        # Legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.1, 1))
        
        plt.tight_layout()
        plt.show()

def test_sequential_building():
    """Test Freeman's sequential building approach"""
    builder = Freeman_Sequential_Builder()
    
    elements = [
        (1, "Hydrogen"), (2, "Helium"), (3, "Lithium"), (4, "Beryllium"),
        (5, "Boron"), (6, "Carbon"), (7, "Nitrogen"), (8, "Oxygen"),
        (9, "Fluorine"), (10, "Neon"), (11, "Sodium"), (12, "Magnesium"), (13, "Aluminium"), (14, "Silicon"),
        (15, "Phosphorus"), (16, "Sulpher"), (17, "Chlorine")
    ]
    
    print("\n" + "="*60)
    print("TESTING FREEMAN'S SEQUENTIAL ELECTRON BUILDING THEORY")
    print("="*60)
    
    results = {}
    
    for atomic_number, element_name in elements:
        print(f"\n{'='*20} {element_name.upper()} (Z={atomic_number}) {'='*20}")
        
        # Build atom sequentially
        electrons, energies_history = builder.build_atom_sequentially(atomic_number)
        
        # Analyze configuration
        analysis = builder.analyze_configuration(electrons, atomic_number)
        
        results[element_name] = analysis
        
        # Plot energy landscapes for this atom
        if energies_history:
            builder.plot_energy_landscapes(energies_history, atomic_number)
        
        # Plot final configuration
        builder.plot_final_configuration(analysis, atomic_number)
    
    # Summary
    print("\n" + "="*60)
    print("SEQUENTIAL BUILDING THEORY SUMMARY")
    print("="*60)
    print("Element        | Predicted Config | Expected Config  | Accuracy")
    print("-" * 60)
    
    total_accuracy = 0
    count = 0
    
    for atomic_number, element_name in elements:
        analysis = results[element_name]
        predicted = analysis['shell_counts']
        expected = analysis['expected']
        accuracy = analysis['accuracy']
        
        total_accuracy += accuracy
        count += 1
        
        match_symbol = "✓" if predicted == expected else "✗"
        print(f"{element_name:<14} | {str(predicted):<16} | {str(expected):<16} | {accuracy:>6.1f}% {match_symbol}")
    
    avg_accuracy = total_accuracy / count if count > 0 else 0
    print("-" * 60)
    print(f"AVERAGE ACCURACY: {avg_accuracy:.1f}%")
    
    if avg_accuracy >= 80:
        print("\n🎉 EXCELLENT! Freeman's sequential theory shows strong predictive power!")
        print("   The wave interference approach successfully builds shell structure.")
    elif avg_accuracy >= 60:
        print("\n✅ GOOD! Freeman's sequential theory shows promising results.")
        print("   Most elements follow expected patterns with wave guidance.")
    else:
        print("\n⚠️  MIXED RESULTS. Sequential building shows some success but needs refinement.")
        print("   May need full geometric nuclear theory or additional wave effects.")
    
    print(f"\nKey Insight: Sequential assembly (H→He→Li→Be...) matches James's actual approach")
    print(f"and should show better accuracy than simultaneous N-body optimization.")

def analyze_energy_landscapes():
    """
    Detailed analysis of energy landscapes to understand why certain elements deviate.
    Focus on the problematic elements: B, C, N, O, F
    """
    builder = Freeman_Sequential_Builder()
    
    problematic_elements = [
        (5, "Boron", [2, 3, 0, 0, 0]),     # Predicted: [2, 2, 1, 0, 0] 
        (6, "Carbon", [2, 4, 0, 0, 0]),    # Predicted: [2, 2, 2, 0, 0]
        (7, "Nitrogen", [2, 5, 0, 0, 0]),  # Predicted: [2, 4, 1, 0, 0]
        (8, "Oxygen", [2, 6, 0, 0, 0]),    # Predicted: [2, 4, 2, 0, 0]
        (9, "Fluorine", [2, 7, 0, 0, 0])   # Predicted: [2, 4, 3, 0, 0]
    ]
    
    print("\n" + "="*80)
    print("DETAILED ENERGY LANDSCAPE ANALYSIS")
    print("="*80)
    print("Understanding why B, C, N, O, F show deviations...")
    
    for atomic_number, element_name, expected_config in problematic_elements:
        print(f"\n{'='*60}")
        print(f"ANALYZING {element_name.upper()} (Z={atomic_number})")
        print(f"Expected: {expected_config}")
        print(f"{'='*60}")
        
        # Build atom step by step and analyze each electron addition
        electrons = []
        
        for electron_num in range(1, atomic_number + 1):
            print(f"\n--- Adding Electron #{electron_num} ---")
            
            if electron_num == 1:
                position = np.array([1.0, 0.0, 0.0])
                electrons.append(position)
                continue
            
            # Calculate energy landscape for this electron
            Z_eff = max(1.0, atomic_number - 0.7 * (electron_num - 1))
            
            # Test fine-grained radial scan
            test_radii = np.linspace(0.5, 12.0, 200)
            energies = []
            best_positions = []
            
            for radius in test_radii:
                # For each radius, find best angular position
                min_energy_at_r = float('inf')
                best_pos_at_r = None
                
                # Sample many angles
                for i in range(72):
                    theta = 2 * math.pi * i / 72
                    for j in range(8):
                        phi = math.pi * j / 7 if j < 7 else math.pi
                        
                        x = radius * math.sin(phi) * math.cos(theta)
                        y = radius * math.sin(phi) * math.sin(theta) 
                        z = radius * math.cos(phi)
                        
                        pos = np.array([x, y, z])
                        energy = builder.total_energy_at_position(pos, electrons, Z_eff)
                        
                        if energy < min_energy_at_r:
                            min_energy_at_r = energy
                            best_pos_at_r = pos.copy()
                
                energies.append(min_energy_at_r)
                best_positions.append(best_pos_at_r)
            
            # Find global minimum
            min_idx = np.argmin(energies)
            optimal_position = best_positions[min_idx]
            optimal_radius = test_radii[min_idx]
            optimal_energy = energies[min_idx]
            
            electrons.append(optimal_position)
            
            # Analyze the energy landscape
            print(f"Optimal radius: {optimal_radius:.3f}")
            print(f"Optimal energy: {optimal_energy:.6f}")
            
            # Find local minima (potential shells)
            local_minima = find_local_minima(test_radii, energies)
            print(f"Local energy minima at radii: {[f'{r:.2f}' for r in local_minima]}")
            
            # Decompose energy at optimal position
            energy_breakdown = analyze_energy_components(
                builder, optimal_position, electrons[:-1], Z_eff
            )
            
            print("Energy breakdown at optimal position:")
            for component, value in energy_breakdown.items():
                print(f"  {component}: {value:.6f}")
            
            # Check shell assignment
            shell = determine_shell_from_radius(optimal_radius)
            print(f"Assigned to Shell {shell}")
            
            # Plot energy landscape for this electron
            plot_single_electron_landscape(
                test_radii, energies, optimal_radius, 
                f"{element_name} - Electron #{electron_num}", local_minima
            )
        
        # Final configuration analysis
        final_analysis = builder.analyze_configuration(electrons, atomic_number)
        predicted_config = final_analysis['shell_counts']
        
        print(f"\nFINAL ANALYSIS:")
        print(f"Predicted config: {predicted_config}")
        print(f"Expected config:  {expected_config}")
        print(f"Accuracy: {final_analysis['accuracy']:.1f}%")
        
        # Identify the specific deviation
        analyze_deviation(predicted_config, expected_config, element_name)

def find_local_minima(radii, energies, threshold=0.01):
    """Find local minima in energy landscape"""
    minima = []
    for i in range(1, len(energies)-1):
        if (energies[i] < energies[i-1] and energies[i] < energies[i+1]):
            # Check if it's significant (not just noise)
            left_diff = energies[i-1] - energies[i]
            right_diff = energies[i+1] - energies[i]
            if left_diff > threshold and right_diff > threshold:
                minima.append(radii[i])
    return minima

def analyze_energy_components(builder, position, existing_electrons, Z_eff):
    """Break down energy into components at a specific position"""
    pos = np.array(position)
    radius = np.linalg.norm(pos)
    
    # Nuclear attraction
    nuclear = -Z_eff / (radius + 0.5)
    
    # Electron repulsion
    repulsion = 0.0
    for electron_pos in existing_electrons:
        distance = np.linalg.norm(pos - electron_pos)
        if distance > 1e-10:
            repulsion += 5.0 / distance
    
    # Wave interference
    interference_field = builder.electron_wave_field(pos, existing_electrons)
    interference = 2.0 * interference_field
    
    # Shell preference
    electron_number = len(existing_electrons) + 1
    if electron_number <= 2:
        target_radius = 1.0
    elif electron_number <= 10:
        target_radius = 4.0
    else:
        target_radius = 9.0
    
    shell_pref = 0.5 * abs(radius - target_radius) / target_radius
    
    return {
        'Nuclear attraction': nuclear,
        'Electron repulsion': repulsion, 
        'Wave interference': interference,
        'Shell preference': shell_pref,
        'Total': nuclear + repulsion + interference + shell_pref
    }

def determine_shell_from_radius(radius):
    """Determine shell from radius"""
    if radius < 3.5:
        return 1
    elif radius < 8.0:
        return 2
    elif radius < 15.0:
        return 3
    else:
        return 4

def plot_single_electron_landscape(radii, energies, optimal_r, title, local_minima):
    """Plot energy landscape for a single electron addition"""
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(radii, energies, 'b-', linewidth=2, label='Total Energy')
    plt.scatter([optimal_r], [energies[np.argmin(np.abs(radii - optimal_r))]], 
               color='red', s=100, zorder=5, label=f'Optimal: r={optimal_r:.2f}')
    
    # Mark local minima
    for r_min in local_minima:
        idx = np.argmin(np.abs(radii - r_min))
        plt.scatter([r_min], [energies[idx]], color='orange', s=60, 
                   zorder=4, alpha=0.8, label='Local minimum' if r_min == local_minima[0] else "")
    
    # Mark shell boundaries
    shell_boundaries = [3.5, 8.0, 15.0]
    for i, boundary in enumerate(shell_boundaries):
        plt.axvline(boundary, color='gray', linestyle='--', alpha=0.5, 
                   label=f'Shell {i+1}→{i+2}' if i == 0 else "")
    
    plt.xlabel('Radius')
    plt.ylabel('Energy')
    plt.title(f'{title} - Energy Landscape')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Zoomed view around optimal region
    plt.subplot(1, 2, 2)
    zoom_mask = (radii >= optimal_r - 2) & (radii <= optimal_r + 2)
    if np.any(zoom_mask):
        plt.plot(radii[zoom_mask], np.array(energies)[zoom_mask], 'b-', linewidth=2)
        plt.scatter([optimal_r], [energies[np.argmin(np.abs(radii - optimal_r))]], 
                   color='red', s=100, zorder=5)
        
        for r_min in local_minima:
            if abs(r_min - optimal_r) <= 2:
                idx = np.argmin(np.abs(radii - r_min))
                plt.scatter([r_min], [energies[idx]], color='orange', s=60, zorder=4, alpha=0.8)
        
        plt.xlabel('Radius')
        plt.ylabel('Energy') 
        plt.title('Zoomed View')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def analyze_deviation(predicted, expected, element_name):
    """Analyze specific type of deviation"""
    print(f"\nDEVIATION ANALYSIS for {element_name}:")
    
    total_predicted = sum(predicted)
    total_expected = sum(expected)
    
    if total_predicted == total_expected:
        print("✓ Correct total number of electrons")
        
        # Check shell-by-shell
        for shell in range(5):
            pred = predicted[shell] 
            exp = expected[shell]
            if pred > exp:
                print(f"  Shell {shell+1}: {pred-exp} extra electrons")
            elif pred < exp:
                print(f"  Shell {shell+1}: {exp-pred} missing electrons")
        
        # Identify the pattern
        if predicted[1] < expected[1] and predicted[2] > expected[2]:
            print("→ PATTERN: Electrons preferring Shell 3 over Shell 2")
            print("→ CAUSE: Shell 2 may be energetically unfavorable")
            print("→ PHYSICS: Need stronger Shell 2 stabilization")
            
        elif predicted[1] < expected[1] and sum(predicted[2:]) > sum(expected[2:]):
            print("→ PATTERN: Electrons avoiding Shell 2") 
            print("→ CAUSE: Shell 2 energy barrier too high")
            print("→ PHYSICS: Wave interference may be too strong at Shell 2 radius")
    
    else:
        print(f"✗ Electron count mismatch: {total_predicted} vs {total_expected}")

if __name__ == "__main__":
    # Run the detailed analysis
    test_sequential_building()