import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
N_ANGLE_SAMPLES = 36000  # Number of angular orientations to sample (0.1° increments)
WAVELENGTH_TEST = "4e_pi"  # Options: "original" (2·eⁿ), "halved" (eⁿ), "4e_pi" (4·eⁿ/π)

class RotationalAveraging2D:
    def __init__(self):
        # Test both wavelength formulations
        self.harmonics = [0, 1, 2, 3, 4]
        self.wavelengths = {}
        self.energies = {}
        self.e = np.e
        
        if WAVELENGTH_TEST == "4e_pi":
            print("TESTING 4·eⁿ/π WAVELENGTHS")
            # New formulation: λₙ = 4·eⁿ/π
            for n in self.harmonics:
                self.wavelengths[n] = 4.0 * (self.e ** n) / np.pi
                self.energies[n] = 1.0 / self.wavelengths[n]  # E ∝ 1/λ
        elif WAVELENGTH_TEST == "halved":
            print("TESTING HALVED WAVELENGTHS: λₙ = eⁿ")
            # Halved wavelengths: λₙ = eⁿ
            for n in self.harmonics:
                self.wavelengths[n] = self.e ** n
                self.energies[n] = 1.0 / self.wavelengths[n]  # E ∝ 1/λ
        else:  # "original"
            print("ORIGINAL WAVELENGTHS: λₙ = 2·eⁿ")
            # Original wavelengths: λₙ = 2·eⁿ  
            wavelength_values = [2.000000, 5.436564, 14.785166, 40.194074, 109.196300]
            energy_values = [0.632456, 0.232455, 0.085465, 0.031444, 0.011573]
            
            for i, n in enumerate(self.harmonics):
                self.wavelengths[n] = wavelength_values[i]
                self.energies[n] = energy_values[i]
        
        # Normalize energies
        total_energy = sum(self.energies.values())
        for n in self.harmonics:
            self.energies[n] /= total_energy
            
        # Shell 1 radius
        self.r1 = 1.0
        
        print("Wavelengths and normalized energies:")
        for n in self.harmonics:
            print(f"  λ_{n} = {self.wavelengths[n]:.6f} Bohr, E_{n} = {self.energies[n]:.6f}")
        print("Sources: e↑(-1,0), e↓(+1,0) - NO emission from nucleus")
        
    def calculate_wave_from_source(self, x_grid, y_grid, source_pos, phase_multiplier):
        """
        Calculate multi-harmonic wave from a source (e↑, N, or e↓) 
        Each source emits ALL wavelengths with their fundamental energies
        """
        # Distance from source to each grid point
        distances = np.sqrt((x_grid - source_pos[0])**2 + (y_grid - source_pos[1])**2)
        
        # Avoid division by zero at source position
        distances = np.where(distances < 1e-10, 1e-10, distances)
        
        # Sum all harmonics with their fundamental energies
        total_wave = np.zeros_like(distances)
        
        for n in self.harmonics:
            wavelength = self.wavelengths[n]
            energy = self.energies[n]  # Fundamental energy of this wavelength
            
            # Wave contribution: energy * phase * sin(2π * distance / wavelength) / distance
            wave_component = energy * phase_multiplier * np.sin(2 * np.pi * distances / wavelength) / distances
            total_wave += wave_component
        
        return total_wave
    
    def calculate_probability_weight(self, theta):
        """
        Probability weighting function - maximum at 90°, minimum at 0° and 180°
        """
        # sin²(θ) gives the right distribution
        return np.sin(theta)**2
    
    def calculate_rotational_average(self, x_range=(-8, 8), y_range=(-8, 8), resolution=320, n_angles=N_ANGLE_SAMPLES):
        """
        Calculate rotationally averaged interference pattern in 2D
        """
        # Create coordinate grids
        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        X, Y = np.meshgrid(x, y)
        
        # Initialize averaged interference pattern
        total_interference = np.zeros((resolution, resolution))
        total_weight = 0.0
        
        # Sample different orientations
        angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)
        
        print(f"Calculating rotational average over {n_angles} orientations...")
        
        for i, theta in enumerate(angles):
            # Source positions for this orientation
            # e↑ (electron A, sin phase)
            electron_A = np.array([self.r1 * np.cos(theta), self.r1 * np.sin(theta)])
            # e↓ (electron B, cos phase) - 180° opposite
            electron_B = np.array([self.r1 * np.cos(theta + np.pi), self.r1 * np.sin(theta + np.pi)])
            
            # Calculate waves from ONLY the two electrons (no nucleus emission)
            wave_A = self.calculate_wave_from_source(X, Y, electron_A, phase_multiplier=1.0)   # sin phase
            wave_B = self.calculate_wave_from_source(X, Y, electron_B, phase_multiplier=-1.0)  # cos phase (opposite)
            
            # Total interference for this orientation (only electrons emit)
            interference = wave_A + wave_B
            
            # Probability weight for this orientation
            weight = self.calculate_probability_weight(theta)
            
            # Add to weighted average
            total_interference += weight * interference
            total_weight += weight
            
            if i % 600 == 0:  # Print every 600 samples for 3600 total
                print(f"  Processed orientation {i+1}/{n_angles}, θ={theta*180/np.pi:.1f}°, weight={weight:.3f}")
        
        # Normalize by total weight
        averaged_interference = total_interference / total_weight
        
        return X, Y, averaged_interference, angles
    
    def plot_rotational_average(self):
        """
        Plot the rotationally averaged 2D interference pattern
        """
        X, Y, interference, angles = self.calculate_rotational_average()
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: 2D interference pattern
        im1 = ax1.imshow(interference, extent=[-8, 8, -8, 8], origin='lower', 
                        cmap='RdBu_r', aspect='equal')
        
        # Mark shell 1 circle
        circle = plt.Circle((0, 0), self.r1, fill=False, color='white', linestyle='--', alpha=0.7)
        ax1.add_patch(circle)
        
        # Mark potential shell 2 position (r=4)
        circle2 = plt.Circle((0, 0), 4.0, fill=False, color='yellow', linestyle=':', alpha=0.5)
        ax1.add_patch(circle2)
        
        ax1.scatter(0, 0, color='blue', s=100, marker='o', label='Nucleus')
        wavelength_type = {"4e_pi": "λₙ = 4·eⁿ/π", "halved": "λₙ = eⁿ", "original": "λₙ = 2·eⁿ"}[WAVELENGTH_TEST]
        ax1.set_title(f'Rotationally Averaged 2D Interference Pattern\n{wavelength_type}')
        ax1.set_xlabel('x (Bohr radii)')
        ax1.set_ylabel('y (Bohr radii)')
        ax1.set_xticks(range(-8, 9, 2))
        ax1.set_yticks(range(-8, 9, 2))
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        plt.colorbar(im1, ax=ax1, label='Wave Interference')
        
        # Plot 2: Proper radial averaging with WIDE SMOOTH BUCKETS
        center_x, center_y = interference.shape[1] // 2, interference.shape[0] // 2
        max_radius = min(center_x, center_y)
        
        # Create fewer, wider radial bins for smoothing
        radial_bins = np.linspace(0, 8, 80)  # Extend to 8 Bohr radii
        radial_profile = []
        
        for r in radial_bins:
            # Convert radius to pixel coordinates
            r_pixels = (r / 8.0) * max_radius
            
            if r_pixels < max_radius:
                # Create mask for all points at this radius - WIDER BUCKET
                y_indices, x_indices = np.ogrid[:interference.shape[0], :interference.shape[1]]
                distances = np.sqrt((x_indices - center_x)**2 + (y_indices - center_y)**2)
                
                # Find points within ±2 pixels of target radius (WIDER BUCKET)
                mask = np.abs(distances - r_pixels) <= 2.0
                
                if np.sum(mask) > 10:  # Need at least 10 points for good average
                    # Average all points at this radius
                    radial_value = np.mean(interference[mask])
                    radial_profile.append(radial_value)
                else:
                    radial_profile.append(0)
            else:
                radial_profile.append(0)
        
        # Additional smoothing: moving average
        radial_profile = np.array(radial_profile)
        smoothed_profile = []
        window_size = 5  # Larger smoothing window
        
        for i in range(len(radial_profile)):
            start_idx = max(0, i - window_size//2)
            end_idx = min(len(radial_profile), i + window_size//2 + 1)
            smoothed_value = np.mean(radial_profile[start_idx:end_idx])
            smoothed_profile.append(smoothed_value)
        
        ax2.plot(radial_bins, smoothed_profile, 'b-', linewidth=3, label='Smooth Radial Average')
        
        # Mark shell positions
        ax2.axvline(1, color='red', linestyle='--', alpha=0.7, label='Shell 1 (r=1)')
        ax2.axvline(4, color='orange', linestyle='--', alpha=0.7, label='Shell 2 (r=4)')
        ax2.axvline(6, color='green', linestyle='--', alpha=0.7, label='Potential Shell 3')
        ax2.axhline(0, color='gray', linestyle='-', alpha=0.3)
        
        wavelength_type = {"4e_pi": "λₙ = 4·eⁿ/π", "halved": "λₙ = eⁿ", "original": "λₙ = 2·eⁿ"}[WAVELENGTH_TEST]
        ax2.set_title(f'Radial Profile: {wavelength_type}')
        ax2.set_xlabel('Distance from Nucleus (Bohr radii)')
        ax2.set_ylabel('Wave Interference')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Analyze for shell formation
        print(f"\n=== SHELL FORMATION ANALYSIS ===")
        print(f"Shell 1 radius: {self.r1:.1f} Bohr")
        
        # Check interference values at key radii
        for r in [1.0, 2.0, 3.0, 4.0]:
            r_idx = int((r / 4.0) * (interference.shape[1] // 2))
            if r_idx < len(radial_profile):
                intensity = radial_profile[r_idx]
                print(f"Interference at r={r:.1f}: {intensity:.4f}")
        
        return X, Y, interference

def main():
    """Generate rotationally averaged 2D interference pattern"""
    
    wave_sim = RotationalAveraging2D()
    
    print("=== 2D ROTATIONAL AVERAGING WITH HARMONICS ===")
    print("Modeling electron pair with multi-harmonic waves:")
    print("Harmonics: n = 0, 1, 2, 3")
    print("Wavelengths: λₙ = 2eⁿ")
    print("Expected: Complex interference creating shell structure")
    
    X, Y, interference = wave_sim.plot_rotational_average()
    
    return wave_sim, X, Y, interference

if __name__ == "__main__":
    simulation, X, Y, interference = main()
