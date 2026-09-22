import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class WaveInterference2D:
    def __init__(self):
        # Wavelengths (in Bohr radii)
        self.wavelengths = {
            0: 2.000000,
            1: 5.436564,
            2: 14.785166
        }
        
        # Wave energies
        self.energies = {
            0: 0.632456,
            1: 0.232455,
            2: 0.085465
        }
        
        # Source positions
        self.e_up = np.array([-1.0, 0.0])    # e↑ at (-1,0)
        self.nucleus = np.array([0.0, 0.0])   # N at (0,0)
        self.e_down = np.array([1.0, 0.0])    # e↓ at (+1,0)
        
    def calculate_wave_at_point(self, position, source_pos, wavelength, energy, phase_offset=0):
        """
        Calculate wave amplitude at a point from a source
        Wave = energy * sin(2π * distance/wavelength + phase_offset)
        """
        distance = np.linalg.norm(position - source_pos)
        if distance < 1e-10:
            return energy  # At source position
        
        # Wave equation
        phase = 2 * np.pi * distance / wavelength + phase_offset
        amplitude = energy * np.sin(phase)
        
        return amplitude, phase
    
    def calculate_total_interference(self, x_grid, y_grid):
        """
        Calculate total interference pattern across the 2D grid
        """
        # Initialize grids for each wave component
        total_amplitude = np.zeros_like(x_grid)
        total_red_intensity = np.zeros_like(x_grid)  # For visualization
        
        # For each point in the grid
        for i in range(x_grid.shape[0]):
            for j in range(x_grid.shape[1]):
                point = np.array([x_grid[i, j], y_grid[i, j]])
                
                # Initialize total amplitude at this point
                point_amplitude = 0.0
                point_red_intensity = 0.0
                
                # Waves from e↑ (phase = 0, red color)
                for n in [0, 1, 2]:
                    amp_up, phase_up = self.calculate_wave_at_point(
                        point, self.e_up, self.wavelengths[n], self.energies[n], phase_offset=0
                    )
                    point_amplitude += amp_up
                    
                    # Red intensity based on energy and wave phase
                    red_contribution = self.energies[n] * abs(np.sin(phase_up))
                    point_red_intensity += red_contribution
                
                # Waves from e↓ (phase = π for λ₀, 0 for others)
                for n in [0, 1, 2]:
                    if n == 0:
                        # λ₀ wave from e↓ has π phase shift for complete interference at N
                        phase_offset = np.pi
                    else:
                        phase_offset = 0
                    
                    amp_down, phase_down = self.calculate_wave_at_point(
                        point, self.e_down, self.wavelengths[n], self.energies[n], phase_offset
                    )
                    point_amplitude += amp_down
                
                # Store results
                total_amplitude[i, j] = point_amplitude
                total_red_intensity[i, j] = point_red_intensity
        
        return total_amplitude, total_red_intensity
    
    def plot_interference_pattern(self, x_range=(-3, 3), y_range=(-3, 3), resolution=200):
        """
        Plot the 2D interference pattern
        """
        # Create coordinate grids
        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        X, Y = np.meshgrid(x, y)
        
        # Calculate interference pattern
        print("Calculating interference pattern...")
        total_amplitude, red_intensity = self.calculate_total_interference(X, Y)
        
        # Create the plot
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Total wave amplitude
        im1 = ax1.imshow(total_amplitude, extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
                        origin='lower', cmap='RdBu_r', aspect='equal')
        ax1.scatter(*self.e_up, color='red', s=100, marker='^', label='e↑ (-1,0)')
        ax1.scatter(*self.nucleus, color='blue', s=100, marker='o', label='N (0,0)')
        ax1.scatter(*self.e_down, color='red', s=100, marker='v', label='e↓ (+1,0)')
        ax1.set_title('Total Wave Amplitude')
        ax1.set_xlabel('x (Bohr radii)')
        ax1.set_ylabel('y (Bohr radii)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        plt.colorbar(im1, ax=ax1)
        
        # Plot 2: Intensity (|amplitude|²)
        intensity = np.abs(total_amplitude)**2
        im2 = ax2.imshow(intensity, extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
                        origin='lower', cmap='hot', aspect='equal')
        ax2.scatter(*self.e_up, color='cyan', s=100, marker='^', label='e↑ (-1,0)')
        ax2.scatter(*self.nucleus, color='cyan', s=100, marker='o', label='N (0,0)')
        ax2.scatter(*self.e_down, color='cyan', s=100, marker='v', label='e↓ (+1,0)')
        ax2.set_title('Interference Intensity |Ψ|²')
        ax2.set_xlabel('x (Bohr radii)')
        ax2.set_ylabel('y (Bohr radii)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        plt.colorbar(im2, ax=ax2)
        
        # Plot 3: Red wave visualization (opacity based on En * sin(phase))
        red_opacity = np.clip(red_intensity / np.max(red_intensity), 0, 1)
        
        # Create red colormap with variable opacity
        red_colors = np.zeros((resolution, resolution, 4))
        red_colors[:, :, 0] = 1.0  # Full red
        red_colors[:, :, 3] = red_opacity  # Variable alpha
        
        ax3.imshow(red_colors, extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
                  origin='lower', aspect='equal')
        ax3.scatter(*self.e_up, color='white', s=100, marker='^', label='e↑ (-1,0)')
        ax3.scatter(*self.nucleus, color='white', s=100, marker='o', label='N (0,0)')
        ax3.scatter(*self.e_down, color='white', s=100, marker='v', label='e↓ (+1,0)')
        ax3.set_title('Red Waves from e↑ (opacity ∝ E_n·sin(φ))')
        ax3.set_xlabel('x (Bohr radii)')
        ax3.set_ylabel('y (Bohr radii)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Cross-section along x-axis (y=0)
        y_zero_idx = resolution // 2
        x_line = x
        amplitude_line = total_amplitude[y_zero_idx, :]
        intensity_line = intensity[y_zero_idx, :]
        
        ax4.plot(x_line, amplitude_line, 'b-', linewidth=2, label='Wave Amplitude')
        ax4.plot(x_line, intensity_line, 'r-', linewidth=2, label='Intensity |Ψ|²')
        
        # Mark key positions
        ax4.axvline(-1, color='red', linestyle=':', alpha=0.7, label='e↑')
        ax4.axvline(0, color='blue', linestyle=':', alpha=0.7, label='N')
        ax4.axvline(1, color='red', linestyle=':', alpha=0.7, label='e↓')
        
        # Mark wavelength scales
        for n, wavelength in self.wavelengths.items():
            ax4.axhline(0, xmin=0.1, xmax=0.1 + wavelength/(2*x_range[1]), 
                       color='gray', alpha=0.5)
            ax4.text(-2.5, 0.1 + n*0.05, f'λ_{n}={wavelength:.1f}', fontsize=8)
        
        ax4.set_title('Cross-section: λ₂↑...λ₁↑...e↑...{λ₀↑ N λ₀↓}...e↓...λ₁↓...λ₂↓')
        ax4.set_xlabel('x (Bohr radii)')
        ax4.set_ylabel('Amplitude / Intensity')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Print analysis
        print("\n=== INTERFERENCE ANALYSIS ===")
        print(f"Wavelengths: λ₀={self.wavelengths[0]:.3f}, λ₁={self.wavelengths[1]:.3f}, λ₂={self.wavelengths[2]:.3f}")
        print(f"Energies: E₀={self.energies[0]:.3f}, E₁={self.energies[1]:.3f}, E₂={self.energies[2]:.3f}")
        
        # Check interference at nucleus (should be zero for λ₀)
        nucleus_idx = (resolution//2, resolution//2)
        nucleus_amplitude = total_amplitude[nucleus_idx]
        print(f"\nAmplitude at nucleus (0,0): {nucleus_amplitude:.6f}")
        print("(Should be near zero due to λ₀ wave interference)")
        
        return X, Y, total_amplitude, intensity, red_intensity

def main():
    """Generate and display the 2D wave interference pattern"""
    
    wave_sim = WaveInterference2D()
    
    print("=== 2D WAVE INTERFERENCE SIMULATION ===")
    print("Pattern: λ₂↑ ... λ₁↑ ... e↑ ... {λ₀↑ N λ₀↓} ... e↓ ... λ₁↓ ... λ₂↓")
    print("\nSources:")
    print("  e↑ at (-1,0) - red waves, phase=0")
    print("  N  at (0,0)  - nuclear center")  
    print("  e↓ at (+1,0) - waves with λ₀ phase=π for interference")
    
    # Generate the interference pattern
    X, Y, amplitude, intensity, red_intensity = wave_sim.plot_interference_pattern()
    
    return wave_sim, X, Y, amplitude, intensity

if __name__ == "__main__":
    simulation, X, Y, amplitude, intensity = main()
