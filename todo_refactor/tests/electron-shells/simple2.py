import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
N_ANGLE_SAMPLES = 36000

class RotationalAveraging2D:
    def __init__(self):
        # Wavelength = 2 Bohr radii
        self.wavelength = 2.0
        # Shell 1 radius
        self.r1 = 1.0
        
    def calculate_wave_from_electron(self, x_grid, y_grid, electron_pos, phase):
        """
        Calculate wave from an electron at given position with given phase
        """
        # Distance from electron to each grid point
        distances = np.sqrt((x_grid - electron_pos[0])**2 + (y_grid - electron_pos[1])**2)
        
        # Avoid division by zero at electron position
        distances = np.where(distances < 1e-10, 1e-10, distances)
        
        # Wave equation: phase * sin(2π * distance / wavelength) / distance
        wave = phase * np.sin(2 * np.pi * distances / self.wavelength) / distances
        
        return wave
    
    def calculate_probability_weight(self, theta):
        """
        Probability weighting function - maximum at 90°, minimum at 0° and 180°
        """
        # sin²(θ) gives the right distribution
        return np.sin(theta)**2
    
    def calculate_rotational_average(self, x_range=(-4, 4), y_range=(-4, 4), resolution=200, n_angles=N_ANGLE_SAMPLES):
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
            # Electron positions for this orientation
            # Electron A (spin up, sin phase)
            electron_A = np.array([self.r1 * np.cos(theta), self.r1 * np.sin(theta)])
            # Electron B (spin down, cos phase) - 180° opposite
            electron_B = np.array([self.r1 * np.cos(theta + np.pi), self.r1 * np.sin(theta + np.pi)])
            
            # Calculate waves from each electron
            wave_A = self.calculate_wave_from_electron(X, Y, electron_A, phase=1.0)  # sin phase
            wave_B = self.calculate_wave_from_electron(X, Y, electron_B, phase=-1.0) # cos phase (opposite)
            
            # Total interference for this orientation
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
        im1 = ax1.imshow(interference, extent=[-4, 4, -4, 4], origin='lower', 
                        cmap='RdBu_r', aspect='equal')
        
        # Mark shell 1 circle
        circle = plt.Circle((0, 0), self.r1, fill=False, color='white', linestyle='--', alpha=0.7)
        ax1.add_patch(circle)
        
        # Mark potential shell 2 position
        circle2 = plt.Circle((0, 0), 2.0, fill=False, color='yellow', linestyle=':', alpha=0.5)
        ax1.add_patch(circle2)
        
        ax1.scatter(0, 0, color='blue', s=100, marker='o', label='Nucleus')
        ax1.set_title('Rotationally Averaged 2D Interference Pattern')
        ax1.set_xlabel('x (Bohr radii)')
        ax1.set_ylabel('y (Bohr radii)')
        ax1.set_xticks(range(-4, 5))
        ax1.set_yticks(range(-4, 5))
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        plt.colorbar(im1, ax=ax1, label='Wave Interference')
        
        # Plot 2: Radial cross-section
        center_idx = interference.shape[0] // 2
        radial_profile = interference[center_idx, center_idx:]
        
        x_radial = np.linspace(0, 4, len(radial_profile))
        ax2.plot(x_radial, radial_profile, 'b-', linewidth=2, label='Radial Profile')
        
        # Mark shell positions
        ax2.axvline(1, color='red', linestyle='--', alpha=0.7, label='Shell 1 (r=1)')
        ax2.axvline(2, color='orange', linestyle='--', alpha=0.7, label='Potential Shell 2')
        ax2.axvline(3, color='green', linestyle='--', alpha=0.7, label='Potential Shell 3')
        ax2.axhline(0, color='gray', linestyle='-', alpha=0.3)
        
        ax2.set_title('Radial Profile: Interference vs Distance from Nucleus')
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
    
    print("=== 2D ROTATIONAL AVERAGING ===")
    print("Modeling electron pair at varying orientations on shell 1")
    print("Wavelength: 2.0 Bohr radii")
    print("Expected: Non-zero interference pattern revealing shell structure")
    
    X, Y, interference = wave_sim.plot_rotational_average()
    
    return wave_sim, X, Y, interference

if __name__ == "__main__":
    simulation, X, Y, interference = main()
