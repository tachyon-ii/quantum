import numpy as np
import matplotlib.pyplot as plt

class NuclearWaves:
    def __init__(self):
        # Wavelength = 2 Bohr radii
        self.wavelength = 2.0
        
        # Nuclear source at origin
        self.nucleus_pos = 0.0
        
    def calculate_waves(self, x_range=(-10, 10), num_points=1000):
        """
        Calculate sin and cos waves from nucleus (0,0)
        """
        x = np.linspace(x_range[0], x_range[1], num_points)
        
        # Sin wave from nucleus: sin(πx) - already zero at x=0
        sin_wave = np.sin(np.pi * x)
        
        # Cos wave shifted to be zero at x=0: cos(π(x+0.5)) = -sin(πx)
        cos_wave = np.cos(np.pi * (x + 0.5))
        
        # Total interference
        interference = sin_wave + cos_wave
        
        return x, sin_wave, cos_wave, interference
        
    def plot_nuclear_waves(self):
        """
        Plot sin and cos waves from nucleus
        """
        x, sin_wave, cos_wave, interference = self.calculate_waves()
        
        # Plot
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
        ax.plot(x, sin_wave, 'g-', linewidth=2, label='Sin Wave (Green)', alpha=0.7)
        ax.plot(x, cos_wave, 'orange', linewidth=2, label='Cos Wave (Orange)', alpha=0.7)
        ax.plot(x, interference, 'm-', linewidth=3, label='Interference (Purple)')
        
        # Mark key positions
        ax.axvline(0, color='blue', linestyle='--', alpha=0.7, label='Nucleus (0,0)')
        ax.axvline(-1, color='red', linestyle='--', alpha=0.7, label='Electron (-1,0)')
        ax.axvline(1, color='red', linestyle='--', alpha=0.7, label='Electron (+1,0)')
        ax.axhline(0, color='gray', linestyle='-', alpha=0.3)
        
        ax.set_title('Nuclear Waves: sin(πx) + cos(πx) from nucleus')
        ax.set_xlabel('x (Bohr radii)')
        ax.set_ylabel('Wave Amplitude')
        ax.set_xticks(range(-10, 11, 2))
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Check values at key points
        nucleus_idx = np.argmin(np.abs(x - 0.0))
        electron_minus_idx = np.argmin(np.abs(x - (-1.0)))
        electron_plus_idx = np.argmin(np.abs(x - 1.0))
        
        print(f"At nucleus (0,0):")
        print(f"  Sin wave: {sin_wave[nucleus_idx]:+.3f}")
        print(f"  Cos wave: {cos_wave[nucleus_idx]:+.3f}")
        print(f"  Interference: {interference[nucleus_idx]:+.3f}")
        print(f"At electron (-1,0):")
        print(f"  Sin wave: {sin_wave[electron_minus_idx]:+.3f}")
        print(f"  Cos wave: {cos_wave[electron_minus_idx]:+.3f}")
        print(f"  Interference: {interference[electron_minus_idx]:+.3f}")
        print(f"At electron (+1,0):")
        print(f"  Sin wave: {sin_wave[electron_plus_idx]:+.3f}")
        print(f"  Cos wave: {cos_wave[electron_plus_idx]:+.3f}")
        print(f"  Interference: {interference[electron_plus_idx]:+.3f}")
        
        return x, sin_wave, cos_wave, interference

def main():
    """Generate nuclear waves with sin and cos components"""
    
    wave_sim = NuclearWaves()
    
    print("=== NUCLEAR WAVES FROM ORIGIN ===")
    print("Sin wave: sin(πx) from nucleus (0,0)")
    print("Cos wave: cos(πx) from nucleus (0,0)")
    print("Looking for maxima at electron positions ±1")
    
    x, sin_wave, cos_wave, interference = wave_sim.plot_nuclear_waves()
    
    return wave_sim, x, sin_wave, cos_wave, interference

if __name__ == "__main__":
    simulation, x, sin_wave, cos_wave, interference = main()
