import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

def dipole_wave_system():
    """
    Model a dipole system with orthogonal wave sets following λ_n = k·e^n/π
    where k is derived from λ_0 = 1/2 × 4.85 × 10^-12
    """
    
    # Physical constants
    lambda_0_target = 0.5 * 4.85e-12  # Target λ_0
    k = lambda_0_target * np.pi  # k = λ_0 × π (since λ_0 = k·e^0/π)
    
    print(f"k = {k:.2e}")
    print(f"λ_0 = {lambda_0_target:.2e}")
    
    # Spatial range (normalized units for visualization)
    x_range = np.linspace(-50, 50, 2000)
    
    # Wavelengths for n=0 to n=6
    def get_wavelength(n):
        return k * np.exp(n) / np.pi
    
    def get_amplitude(n):
        # Normalize amplitudes for visualization
        return 1.0 / (1.2 ** n)
    
    # Calculate all wavelengths
    wavelengths = [get_wavelength(n) for n in range(7)]
    amplitudes = [get_amplitude(n) for n in range(7)]
    
    print("\nWavelength progression:")
    for n in range(7):
        print(f"n={n}: λ = {wavelengths[n]:.2e}, A = {amplitudes[n]:.3f}")
    
    # For visualization, we need to scale wavelengths to reasonable pixel units
    # Scale factor to make λ_0 visible on our plot
    scale_factor = 10.0 / wavelengths[0]  # Make λ_0 = 10 units
    wavelengths_scaled = [w * scale_factor for w in wavelengths]
    
    print(f"\nVisualization scale factor: {scale_factor:.2e}")
    print("Scaled wavelengths for plotting:")
    for n in range(7):
        print(f"n={n}: λ_scaled = {wavelengths_scaled[n]:.3f}")
    
    # Colors for each n
    colors = ['#ff0044', '#ff4400', '#ffaa00', '#88ff00', 
              '#0088ff', '#4400ff', '#ff00aa']
    
    def calculate_wave_sets(x, angle_deg=0):
        """
        Two wave sources separated by λ (for each wavelength component),
        both π radians out of phase, viewed from angles around their centroid
        
        angle_deg: viewing angle from centroid
        - 0° = superposition direction (phase + distance effects constructive)
        - 180° = dipole direction (phase + distance effects destructive)  
        """
        
        wave_set_1 = []
        wave_set_2 = []
        
        angle_rad = np.radians(angle_deg)
        
        for n in range(7):
            wavelength = wavelengths_scaled[n]
            amplitude = amplitudes[n]
            frequency = 2 * np.pi / wavelength
            
            # Sources separated by λ/2 on each side of centroid
            source1_position = -wavelength / 4  # λ/4 to the left of centroid
            source2_position = +wavelength / 4   # λ/4 to the right of centroid
            
            # Calculate path difference based on viewing angle
            # For a point at distance r and angle θ from centroid
            r = 100  # arbitrary viewing distance (far field approximation)
            path_diff_1 = source1_position * np.cos(angle_rad)
            path_diff_2 = source2_position * np.cos(angle_rad)
            
            # Wave 1: reference phase
            wave1 = amplitude * np.cos(frequency * (x + path_diff_1))
            wave_set_1.append(wave1)
            
            # Wave 2: π radians out of phase + path difference
            wave2 = amplitude * np.cos(frequency * (x + path_diff_2) + np.pi)
            wave_set_2.append(wave2)
        
        # Sum all components in each set
        total_1 = np.sum(wave_set_1, axis=0)
        total_2 = np.sum(wave_set_2, axis=0)
        
        return wave_set_1, wave_set_2, total_1, total_2
    
    def plot_dipole_system(angle_deg=0):
        """
        Plot the dipole system at a specific viewing angle
        """
        wave_set_1, wave_set_2, total_1, total_2 = calculate_wave_sets(x_range, angle_deg)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Dipole System: Viewing Angle = {angle_deg}° from Centroid\n(0°=Superposition, 180°=Dipole)', fontsize=16)
        
        # Plot wave set 1
        ax1 = axes[0, 0]
        for n, (wave, color) in enumerate(zip(wave_set_1, colors)):
            ax1.plot(x_range, wave, color=color, alpha=0.6, linewidth=1, 
                    label=f'n={n}, λ={wavelengths_scaled[n]:.1f}')
        ax1.plot(x_range, total_1, 'white', linewidth=3, label='Total Source 1')
        ax1.set_title('Source 1 (Reference)')
        ax1.set_ylabel('Amplitude')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('black')
        
        # Plot wave set 2
        ax2 = axes[0, 1]
        for n, (wave, color) in enumerate(zip(wave_set_2, colors)):
            ax2.plot(x_range, wave, color=color, alpha=0.6, linewidth=1,
                    label=f'n={n}, λ={wavelengths_scaled[n]:.1f}')
        ax2.plot(x_range, total_2, 'white', linewidth=3, label='Total Source 2')
        ax2.set_title('Source 2 (π phase shift + spatial offset)')
        ax2.set_ylabel('Amplitude')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('black')
        
        # Plot combined result
        ax3 = axes[1, 0]
        combined = total_1 + total_2
        ax3.plot(x_range, combined, 'cyan', linewidth=3, label='Combined (Source1 + Source2)')
        ax3.plot(x_range, total_1, 'red', alpha=0.5, linewidth=1, label='Source 1')
        ax3.plot(x_range, total_2, 'blue', alpha=0.5, linewidth=1, label='Source 2')
        ax3.set_title('Combined Result')
        ax3.set_xlabel('Position')
        ax3.set_ylabel('Amplitude')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_facecolor('black')
        
        # Plot amplitude analysis
        ax4 = axes[1, 1]
        combined_amplitude = np.abs(combined)
        max_amp = np.max(combined_amplitude)
        rms_amp = np.sqrt(np.mean(combined**2))
        
        ax4.plot(x_range, combined_amplitude, 'yellow', linewidth=2, label=f'|Combined| (Max={max_amp:.2f})')
        ax4.axhline(y=rms_amp, color='orange', linestyle='--', label=f'RMS = {rms_amp:.2f}')
        ax4.set_xlabel('Position')
        ax4.set_ylabel('Amplitude')
        ax4.set_title('Amplitude Analysis')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_facecolor('black')
        
        plt.tight_layout()
        return fig
    
    def analyze_angle_sweep():
        """
        Analyze how the system changes as angle varies from 0° to 180°
        """
        angles = np.linspace(0, 180, 19)  # Every 10 degrees from 0° to 180°
        max_amplitudes = []
        rms_amplitudes = []
        
        print("\nAngle sweep analysis:")
        print("Angle\tMax Amplitude\tRMS Amplitude\tDescription")
        print("-" * 55)
        
        for angle in angles:
            _, _, total_1, total_2 = calculate_wave_sets(x_range, angle)
            combined = total_1 + total_2
            
            max_amp = np.max(np.abs(combined))
            rms_amp = np.sqrt(np.mean(combined**2))
            
            max_amplitudes.append(max_amp)
            rms_amplitudes.append(rms_amp)
            
            # Description based on angle
            if angle == 0:
                desc = "Perfect superposition"
            elif angle == 90:
                desc = "90° phase shift"
            elif angle == 180:
                desc = "Perfect dipole"
            else:
                desc = f"{angle}° phase shift"
            
            print(f"{angle:3.0f}°\t{max_amp:.3f}\t\t{rms_amp:.3f}\t\t{desc}")
        
        # Plot angle sweep results
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.plot(angles, max_amplitudes, 'ro-', linewidth=2, markersize=4)
        ax1.set_xlabel('Phase Angle (degrees)')
        ax1.set_ylabel('Maximum Amplitude')
        ax1.set_title('Maximum Amplitude: Superposition (0°) to Dipole (180°)')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('black')
        ax1.axvline(x=0, color='green', linestyle='--', alpha=0.7, label='Superposition')
        ax1.axvline(x=180, color='red', linestyle='--', alpha=0.7, label='Dipole')
        ax1.legend()
        
        ax2.plot(angles, rms_amplitudes, 'bo-', linewidth=2, markersize=4)
        ax2.set_xlabel('Phase Angle (degrees)')
        ax2.set_ylabel('RMS Amplitude')
        ax2.set_title('RMS Amplitude vs Phase Angle')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('black')
        ax2.axvline(x=0, color='green', linestyle='--', alpha=0.7, label='Superposition')
        ax2.axvline(x=180, color='red', linestyle='--', alpha=0.7, label='Dipole')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
        
        return angles, max_amplitudes, rms_amplitudes
    
    # Create visualizations
    print("\nGenerating visualizations...")
    
    # Plot at key angles
    key_angles = [0, 45, 90, 135, 180]
    
    for angle in key_angles:
        fig = plot_dipole_system(angle)
        plt.show()
    
    # Analyze full angle sweep
    angles, max_amps, rms_amps = analyze_angle_sweep()
    
    return {
        'k': k,
        'wavelengths': wavelengths,
        'wavelengths_scaled': wavelengths_scaled,
        'amplitudes': amplitudes,
        'angles': angles,
        'max_amplitudes': max_amps,
        'rms_amplitudes': rms_amps
    }

if __name__ == "__main__":
    # Set matplotlib style for dark theme
    plt.style.use('dark_background')
    
    # Run the dipole wave system analysis
    results = dipole_wave_system()
    
    print("\nAnalysis complete!")
    print(f"Generated plots for dipole system with k = {results['k']:.2e}")
    print(f"Wavelength range: {results['wavelengths'][0]:.2e} to {results['wavelengths'][-1]:.2e}")
