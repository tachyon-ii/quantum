import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
N_ANGLE_SAMPLES = 3600  # Number of angular orientations to sample (0.1° increments)
WAVELENGTH_TEST = "4e_pi"  # λₙ = 4·eⁿ/π

class LithiumInterference:
    def __init__(self):
        # Wavelength formulation λₙ = 4·eⁿ/π
        self.harmonics = [0, 1, 2, 3, 4]
        self.wavelengths = {}
        self.energies = {}
        self.e = np.e
        
        print("MODELING 3 ELECTRONS: Lithium Configuration")
        print("2 electrons (sin/cos pair) at ±1,0 + 1 additional electron")
        print("WAVELENGTHS: λₙ = 4·eⁿ/π")
        
        # Calculate wavelengths: λₙ = 4·eⁿ/π
        for n in self.harmonics:
            self.wavelengths[n] = 4.0 * (self.e ** n) / np.pi
            self.energies[n] = 1.0 / self.wavelengths[n]  # E ∝ 1/λ
        
        # Normalize energies
        total_energy = sum(self.energies.values())
        for n in self.harmonics:
            self.energies[n] /= total_energy
            
        # Shell radii to test
        self.r1 = 1.0  # Shell 1
        self.r2 = 4.0  # Shell 2
        
        print("Wavelengths and normalized energies:")
        for n in self.harmonics:
            print(f"  λ_{n} = {self.wavelengths[n]:.6f} Bohr, E_{n} = {self.energies[n]:.6f}")
        
    def calculate_wave_from_source(self, x_grid, y_grid, source_pos, phase_multiplier):
        """
        Calculate multi-harmonic wave from an electron source
        """
        # Distance from source to each grid point
        distances = np.sqrt((x_grid - source_pos[0])**2 + (y_grid - source_pos[1])**2)
        
        # Avoid division by zero at source position
        distances = np.where(distances < 1e-10, 1e-10, distances)
        
        # Sum all harmonics with their fundamental energies
        total_wave = np.zeros_like(distances)
        
        for n in self.harmonics:
            wavelength = self.wavelengths[n]
            energy = self.energies[n]
            
            # Wave contribution: energy * phase * sin(2π * distance / wavelength) / distance
            wave_component = energy * phase_multiplier * np.sin(2 * np.pi * distances / wavelength) / distances
            total_wave += wave_component
        
        return total_wave
    
    def calculate_probability_weight(self, theta):
        """
        Probability weighting function - maximum at 90°, minimum at 0° and 180°
        """
        return np.sin(theta)**2
    
    def calculate_lithium_field(self, third_electron_radius, x_range=(-8, 8), y_range=(-8, 8), resolution=320, n_angles=N_ANGLE_SAMPLES):
        """
        Calculate the interference field experienced by a 3rd electron at given radius
        from the existing 2-electron pair at ±1,0
        """
        # Create coordinate grids
        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        X, Y = np.meshgrid(x, y)
        
        # Initialize averaged interference pattern
        total_interference = np.zeros((resolution, resolution))
        total_weight = 0.0
        
        # Sample different orientations of the existing 2-electron pair
        angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)
        
        print(f"Calculating Li field with 3rd electron at r={third_electron_radius}...")
        
        for i, theta in enumerate(angles):
            # Fixed 2-electron pair positions (at ±1,0, rotated by theta)
            electron_1 = np.array([self.r1 * np.cos(theta + np.pi), self.r1 * np.sin(theta + np.pi)])  # at -1,0 (sin phase)
            electron_2 = np.array([self.r1 * np.cos(theta), self.r1 * np.sin(theta)])                  # at +1,0 (cos phase)
            
            # Calculate waves from the existing 2-electron pair
            wave_1 = self.calculate_wave_from_source(X, Y, electron_1, phase_multiplier=1.0)   # sin phase
            wave_2 = self.calculate_wave_from_source(X, Y, electron_2, phase_multiplier=-1.0)  # cos phase
            
            # Interference field from the existing pair (this is what the 3rd electron "sees")
            pair_field = wave_1 + wave_2
            
            # Probability weight for this orientation
            weight = self.calculate_probability_weight(theta)
            
            # Add to weighted average
            total_interference += weight * pair_field
            total_weight += weight
            
            if i % 600 == 0:
                print(f"  Processed orientation {i+1}/{n_angles}, θ={theta*180/np.pi:.1f}°")
        
        # Normalize by total weight
        averaged_field = total_interference / total_weight
        
        return X, Y, averaged_field
    
    def find_optimal_third_electron_position(self):
        """
        Find where a 3rd electron would naturally position itself
        by testing different radii and finding the minimum energy position
        """
        test_radii = np.linspace(0.5, 8.0, 50)  # Test radii from 0.5 to 8.0 Bohr
        energy_at_radius = []
        
        print("Finding optimal position for 3rd electron...")
        
        for r in test_radii:
            # Calculate the field at this radius (average around the circle)
            X, Y, field = self.calculate_lithium_field(r, resolution=160, n_angles=720)  # Lower resolution for speed
            
            # Calculate average field strength at this radius
            center_x, center_y = field.shape[1] // 2, field.shape[0] // 2
            max_radius_pixels = min(center_x, center_y)
            r_pixels = (r / 8.0) * max_radius_pixels
            
            if r_pixels < max_radius_pixels:
                # Create mask for points at this radius
                y_indices, x_indices = np.ogrid[:field.shape[0], :field.shape[1]]
                distances = np.sqrt((x_indices - center_x)**2 + (y_indices - center_y)**2)
                mask = np.abs(distances - r_pixels) <= 2.0
                
                if np.sum(mask) > 5:
                    avg_field = np.mean(field[mask])
                    energy_at_radius.append(avg_field)
                else:
                    energy_at_radius.append(0)
            else:
                energy_at_radius.append(0)
            
            if len(energy_at_radius) % 10 == 0:
                print(f"  Tested radius {r:.1f}, energy = {energy_at_radius[-1]:.4f}")
        
        return test_radii, np.array(energy_at_radius)
    
    def plot_lithium_analysis(self):
        """
        Plot the complete Lithium analysis
        """
        # Find optimal position for 3rd electron
        radii, energies = self.find_optimal_third_electron_position()
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
        
        # Plot 1: Field experienced by 3rd electron
        X, Y, field = self.calculate_lithium_field(2.0)  # Show field for electron at r=2
        
        im1 = ax1.imshow(field, extent=[-8, 8, -8, 8], origin='lower', 
                        cmap='RdBu_r', aspect='equal')
        
        # Mark shell positions
        circle1 = plt.Circle((0, 0), 1.0, fill=False, color='white', linestyle='--', alpha=0.7)
        circle2 = plt.Circle((0, 0), 4.0, fill=False, color='yellow', linestyle=':', alpha=0.5)
        ax1.add_patch(circle1)
        ax1.add_patch(circle2)
        
        ax1.scatter(0, 0, color='blue', s=100, marker='o', label='Nucleus')
        ax1.set_title(f'Field Experienced by 3rd Electron\n(from 2-electron pair at ±1,0)')
        ax1.set_xlabel('x (Bohr radii)')
        ax1.set_ylabel('y (Bohr radii)')
        ax1.set_xticks(range(-8, 9, 2))
        ax1.set_yticks(range(-8, 9, 2))
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        plt.colorbar(im1, ax=ax1, label='Wave Interference Field')
        
        # Plot 2: Energy vs radius for 3rd electron
        ax2.plot(radii, energies, 'g-', linewidth=3, label='3rd Electron Energy')
        
        # Mark shell positions
        ax2.axvline(1, color='red', linestyle='--', alpha=0.7, label='Shell 1 (r=1)')
        ax2.axvline(4, color='orange', linestyle='--', alpha=0.7, label='Shell 2 (r=4)')
        ax2.axhline(0, color='gray', linestyle='-', alpha=0.3)
        
        # Find and mark the minimum
        min_idx = np.argmin(energies)
        optimal_radius = radii[min_idx]
        min_energy = energies[min_idx]
        ax2.scatter(optimal_radius, min_energy, color='red', s=100, zorder=5, 
                   label=f'Optimal position: r={optimal_radius:.1f}')
        
        ax2.set_title(f'Energy Landscape for 3rd Electron\nLithium Configuration')
        ax2.set_xlabel('Distance from Nucleus (Bohr radii)')
        ax2.set_ylabel('Wave Interference Energy')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Analysis
        print(f"\n=== LITHIUM (3-ELECTRON) ANALYSIS ===")
        print(f"2-electron pair at ±1,0 (Shell 1 filled)")
        print(f"3rd electron optimal position: r = {optimal_radius:.2f} Bohr")
        print(f"Minimum energy: {min_energy:.4f}")
        
        # Compare to known shell positions
        if optimal_radius < 2.0:
            print("→ 3rd electron prefers to stay near Shell 1")
        elif 2.0 <= optimal_radius < 5.0:
            print("→ 3rd electron forced to Shell 2 region")
        else:
            print("→ 3rd electron pushed to outer shells")
            
        # Check specific positions
        shell_1_energy = energies[np.argmin(np.abs(radii - 1.0))]
        shell_2_energy = energies[np.argmin(np.abs(radii - 4.0))]
        
        print(f"Energy at Shell 1 (r=1.0): {shell_1_energy:.4f}")
        print(f"Energy at Shell 2 (r=4.0): {shell_2_energy:.4f}")
        print(f"Energy difference (Shell 2 - Shell 1): {shell_2_energy - shell_1_energy:.4f}")
        
        return radii, energies, optimal_radius

def main():
    """Generate Lithium interference analysis"""
    
    wave_sim = LithiumInterference()
    
    print("=== LITHIUM (3-ELECTRON) WAVE INTERFERENCE ===")
    print("Configuration: 2 electrons (sin/cos pair) at ±1,0")
    print("Question: Where does the 3rd electron naturally position itself?")
    print("Expected: Transition showing Shell 1 → Shell 2 formation")
    
    radii, energies, optimal_radius = wave_sim.plot_lithium_analysis()
    
    return wave_sim, radii, energies, optimal_radius

if __name__ == "__main__":
    simulation, radii, energies, optimal_radius = main()

