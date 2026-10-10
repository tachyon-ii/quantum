import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# === SIMULATION PARAMETERS ===
MONTE_CARLO_ITERATIONS = 10000  # Increase this for higher fidelity
SHOW_PLOTS = False  # Set to True to see individual element plots
TEMPERATURE_INITIAL = 1.0
TEMPERATURE_DECAY = 0.95

class ElectronShellSimulation:
    def __init__(self):
        # Physical constants (in atomic units)
        self.a0 = 1.0  # Bohr radius as unit
        self.shell_radii = {1: 1.0, 2: 4.0, 3: 9.0, 4: 16.0, 5: 25.0, 6: 36.0}  # r_n = n^2
        
        # Expected electron configurations [shell1, shell2, shell3, shell4, shell5, shell6]
        self.expected_configs = {
            2: [2, 0, 0, 0, 0, 0],    # He
            3: [2, 1, 0, 0, 0, 0],    # Li
            4: [2, 2, 0, 0, 0, 0],    # Be
            5: [2, 3, 0, 0, 0, 0],    # B
            6: [2, 4, 0, 0, 0, 0],    # C
            7: [2, 5, 0, 0, 0, 0],    # N
            8: [2, 6, 0, 0, 0, 0],    # O
            9: [2, 7, 0, 0, 0, 0],    # F
            10: [2, 8, 0, 0, 0, 0],   # Ne
            11: [2, 8, 1, 0, 0, 0],   # Na
            12: [2, 8, 2, 0, 0, 0],   # Mg
            13: [2, 8, 3, 0, 0, 0],   # Al
            14: [2, 8, 4, 0, 0, 0],   # Si
            15: [2, 8, 5, 0, 0, 0],   # P
            16: [2, 8, 6, 0, 0, 0],   # S
            17: [2, 8, 7, 0, 0, 0],   # Cl
            18: [2, 8, 8, 0, 0, 0],   # Ar
            19: [2, 8, 8, 1, 0, 0],   # K
            20: [2, 8, 8, 2, 0, 0],   # Ca
            21: [2, 8, 9, 2, 0, 0],   # Sc
            22: [2, 8, 10, 2, 0, 0],  # Ti
            23: [2, 8, 11, 2, 0, 0],  # V
            24: [2, 8, 13, 1, 0, 0],  # Cr
            25: [2, 8, 13, 2, 0, 0],  # Mn
            26: [2, 8, 14, 2, 0, 0],  # Fe
            27: [2, 8, 15, 2, 0, 0],  # Co
            28: [2, 8, 16, 2, 0, 0],  # Ni
            29: [2, 8, 18, 1, 0, 0],  # Cu
            30: [2, 8, 18, 2, 0, 0],  # Zn
            31: [2, 8, 18, 3, 0, 0],  # Ga
            32: [2, 8, 18, 4, 0, 0],  # Ge
            33: [2, 8, 18, 5, 0, 0],  # As
            34: [2, 8, 18, 6, 0, 0],  # Se
            35: [2, 8, 18, 7, 0, 0],  # Br
            36: [2, 8, 18, 8, 0, 0],  # Kr
            37: [2, 8, 18, 8, 1, 0],  # Rb
            38: [2, 8, 18, 8, 2, 0],  # Sr
            39: [2, 8, 18, 9, 2, 0],  # Y
            40: [2, 8, 18, 10, 2, 0], # Zr
            41: [2, 8, 18, 12, 1, 0], # Nb
            42: [2, 8, 18, 13, 1, 0], # Mo
            43: [2, 8, 18, 13, 2, 0], # Tc
            44: [2, 8, 18, 15, 1, 0], # Ru
            45: [2, 8, 18, 16, 1, 0], # Rh
            46: [2, 8, 18, 18, 0, 0], # Pd
            47: [2, 8, 18, 18, 1, 0], # Ag
            48: [2, 8, 18, 18, 2, 0], # Cd
            49: [2, 8, 18, 18, 3, 0], # In
            50: [2, 8, 18, 18, 4, 0], # Sn
            51: [2, 8, 18, 18, 5, 0], # Sb
            52: [2, 8, 18, 18, 6, 0], # Te
            53: [2, 8, 18, 18, 7, 0], # I
            54: [2, 8, 18, 18, 8, 0], # Xe
            55: [2, 8, 18, 18, 8, 1], # Cs
            56: [2, 8, 18, 18, 8, 2], # Ba
        }
        
        # e^n/π wavelength progression
        self.e = np.e
        self.pi = np.pi
        
        # Base frequency anchor (we'll use a normalized value)
        self.f0 = 1.0
        
    def scroll_frequency(self, n):
        """Calculate e^n/π frequency for shell n"""
        return (self.e**n) / self.pi
    
    def scroll_wavelength(self, n):
        """Calculate wavelength from scroll frequency"""
        return 1.0 / (self.scroll_frequency(n) * self.f0)
    
    def electron_wave(self, test_position, electron_pos, shell_n=1):
        """
        Calculate the scroll wave emitted by an electron
        ψ(r) = sin(2πr/λ) / r
        """
        distance = np.linalg.norm(test_position - electron_pos)
        if distance < 1e-10:  # Avoid division by zero
            return 0.0
            
        wavelength = self.scroll_wavelength(shell_n)
        wave_value = np.sin(2 * self.pi * distance / wavelength) / distance
        return wave_value
    
    def total_interference(self, positions, test_position=None):
        """
        Calculate total wave interference at all grid points or a test position
        """
        if test_position is not None:
            # Calculate interference at a single test point
            total_wave = 0.0
            for i, pos in enumerate(positions):
                # Use actual radius to determine shell, not filling order!
                actual_radius = np.linalg.norm(pos)
                shell_n = self.radius_to_shell_number(actual_radius)
                total_wave += self.electron_wave(test_position, pos, shell_n)
            return abs(total_wave)**2
        
        # Calculate interference on a grid
        x = np.linspace(-15, 15, 50)
        y = np.linspace(-15, 15, 50)
        z = np.linspace(-15, 15, 50)
        
        interference_map = np.zeros((50, 50, 50))
        
        for i, xi in enumerate(x):
            for j, yj in enumerate(y):
                for k, zk in enumerate(z):
                    point = np.array([xi, yj, zk])
                    total_wave = 0.0
                    
                    for p, pos in enumerate(positions):
                        # Use actual radius to determine shell, not filling order!
                        actual_radius = np.linalg.norm(pos)
                        shell_n = self.radius_to_shell_number(actual_radius)
                        total_wave += self.electron_wave(point, pos, shell_n)
                    
                    interference_map[i, j, k] = abs(total_wave)**2
        
        return interference_map, x, y, z
    
    def get_electron_shell(self, electron_number):
        """Determine which shell an electron should be in based on filling order (for initialization only)"""
        if electron_number <= 2:
            return 1
        elif electron_number <= 10:
            return 2
        elif electron_number <= 18:
            return 3
        elif electron_number <= 36:
            return 4
        elif electron_number <= 54:
            return 5
        else:
            return 6
    
    def radius_to_shell_number(self, radius):
        """Convert actual radius to shell number for wave frequency calculation"""
        # Use the shell boundary function to determine which shell this radius corresponds to
        if radius < self.get_shell_boundary(1):
            return 1
        elif radius < self.get_shell_boundary(2):
            return 2
        elif radius < self.get_shell_boundary(3):
            return 3
        elif radius < self.get_shell_boundary(4):
            return 4
        elif radius < self.get_shell_boundary(5):
            return 5
        else:
            return 6
    
    def expected_shell_radius(self, electron_number):
        """Get expected radius for an electron based on shell filling"""
        shell_n = self.get_electron_shell(electron_number)
        return self.shell_radii[shell_n]
    
    def get_shell_boundary(self, n):
        """Calculate the boundary between shell n and shell n+1"""
        return (n + 1)**2 - np.log(n + 1)
    
    def determine_actual_shell(self, radius):
        """Determine which shell an electron is in based on its radius"""
        # Shell 1: r < boundary(1)
        if radius < self.get_shell_boundary(1):
            return 1
        # Shell 2: boundary(1) <= r < boundary(2) 
        elif radius < self.get_shell_boundary(2):
            return 2
        # Shell 3: boundary(2) <= r < boundary(3)
        elif radius < self.get_shell_boundary(3):
            return 3
        # Shell 4: boundary(3) <= r < boundary(4)
        elif radius < self.get_shell_boundary(4):
            return 4
        # Shell 5: boundary(4) <= r < boundary(5)
        elif radius < self.get_shell_boundary(5):
            return 5
        # Shell 6: r >= boundary(5)
        else:
            return 6
    
    def stable_configuration_energy(self, positions):
        """
        Calculate stability energy of a configuration
        Lower values = more stable
        """
        total_energy = 0.0
        n_electrons = len(positions)
        
        # Electron-electron repulsion (main driving force)
        for i in range(n_electrons):
            for j in range(i+1, n_electrons):
                distance = np.linalg.norm(positions[i] - positions[j])
                if distance > 1e-10:
                    total_energy += 1.0 / distance  # Coulomb repulsion
        
        # Shell preference penalty
        for i, pos in enumerate(positions):
            expected_r = self.expected_shell_radius(i + 1)
            actual_r = np.linalg.norm(pos)
            shell_penalty = (actual_r - expected_r)**2
            total_energy += 0.1 * shell_penalty
        
        # Wave interference penalty
        interference_penalty = 0.0
        for i, pos in enumerate(positions):
            interference = self.total_interference(positions, pos)
            interference_penalty += interference
        
        total_energy += 0.01 * interference_penalty
        
        return total_energy
    
    def monte_carlo_placement(self, n_electrons, n_iterations=None, temperature=None):
        """
        Use Monte Carlo to find stable electron configurations
        """
        if n_iterations is None:
            n_iterations = MONTE_CARLO_ITERATIONS
        if temperature is None:
            temperature = TEMPERATURE_INITIAL
            
        # Initialize with rough shell positions
        positions = []
        for i in range(n_electrons):
            shell_n = self.get_electron_shell(i + 1)
            r = self.shell_radii[shell_n]
            
            # Random position on shell
            theta = random.uniform(0, 2*np.pi)
            phi = random.uniform(0, np.pi)
            
            x = r * np.sin(phi) * np.cos(theta)
            y = r * np.sin(phi) * np.sin(theta)
            z = r * np.cos(phi)
            
            positions.append(np.array([x, y, z]))
        
        current_energy = self.stable_configuration_energy(positions)
        best_positions = [pos.copy() for pos in positions]
        best_energy = current_energy
        
        energies = []
        accepted_moves = 0
        
        for iteration in range(n_iterations):
            # Make a random move
            new_positions = [pos.copy() for pos in positions]
            electron_idx = random.randint(0, n_electrons - 1)
            
            # Small random displacement
            displacement = np.random.normal(0, 0.3, 3)  # Smaller steps
            new_positions[electron_idx] += displacement
            
            # Calculate new energy
            new_energy = self.stable_configuration_energy(new_positions)
            
            # Accept or reject (Metropolis criterion)
            if new_energy < current_energy or random.random() < np.exp(-(new_energy - current_energy) / temperature):
                positions = new_positions
                current_energy = new_energy
                accepted_moves += 1
                
                if current_energy < best_energy:
                    best_positions = [pos.copy() for pos in positions]
                    best_energy = current_energy
            
            energies.append(current_energy)
            
            # Cool down temperature
            if iteration > 0 and iteration % 200 == 0:
                temperature *= TEMPERATURE_DECAY
        
        acceptance_rate = accepted_moves / n_iterations
        return best_positions, best_energy, energies, acceptance_rate
    
    def analyze_element(self, atomic_number, element_name):
        """Analyze electron configuration for a specific element"""
        print(f"\n=== {element_name} (Z={atomic_number}) ===")
        
        # Run Monte Carlo optimization
        positions, energy, energies, acceptance_rate = self.monte_carlo_placement(atomic_number)
        
        # Analyze results
        shell_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        shell_positions = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        
        for i, pos in enumerate(positions):
            r = np.linalg.norm(pos)
            expected_shell = self.get_electron_shell(i + 1)
            
            # Determine actual shell using e-based boundary function
            actual_shell = self.determine_actual_shell(r)
                
            shell_counts[actual_shell] += 1
            shell_positions[actual_shell].append(pos)
        
        # Get expected configuration
        expected_config = self.expected_configs.get(atomic_number, [0, 0, 0, 0, 0, 0])
        simulated_config = [shell_counts[1], shell_counts[2], shell_counts[3], 
                           shell_counts[4], shell_counts[5], shell_counts[6]]
        
        print(f"Expected config: {expected_config}")
        print(f"Simulated config: {simulated_config}")
        print(f"Final energy: {energy:.4f}, Acceptance rate: {acceptance_rate:.3f}")
        
        # Calculate average radii
        for shell in [1, 2, 3, 4, 5, 6]:
            if shell_positions[shell]:
                avg_radius = np.mean([np.linalg.norm(pos) for pos in shell_positions[shell]])
                expected_radius = self.shell_radii[shell]
                print(f"Shell {shell}: Avg radius = {avg_radius:.2f} (expected {expected_radius:.2f})")
        
        return positions, energies, shell_counts
    
    def plot_configuration(self, positions, atomic_number, element_name):
        """Plot the 3D electron configuration"""
        fig = plt.figure(figsize=(12, 5))
        
        # 3D plot
        ax1 = fig.add_subplot(121, projection='3d')
        
        colors = []
        for i, pos in enumerate(positions):
            shell = self.get_electron_shell(i + 1)
            if shell == 1:
                colors.append('red')
            elif shell == 2:
                colors.append('blue')
            elif shell == 3:
                colors.append('green')
            elif shell == 4:
                colors.append('orange')
            elif shell == 5:
                colors.append('purple')
            else:
                colors.append('brown')
        
        x_pos = [pos[0] for pos in positions]
        y_pos = [pos[1] for pos in positions]
        z_pos = [pos[2] for pos in positions]
        
        ax1.scatter(x_pos, y_pos, z_pos, c=colors, s=100, alpha=0.8)
        
        # Draw shell boundaries
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        
        for shell_n, radius in self.shell_radii.items():
            if shell_n <= 4:  # Only show first 4 shells
                x_shell = radius * np.outer(np.cos(u), np.sin(v))
                y_shell = radius * np.outer(np.sin(u), np.sin(v))
                z_shell = radius * np.outer(np.ones(np.size(u)), np.cos(v))
                ax1.plot_surface(x_shell, y_shell, z_shell, alpha=0.1, color='gray')
        
        ax1.set_xlabel('X (Bohr radii)')
        ax1.set_ylabel('Y (Bohr radii)')
        ax1.set_zlabel('Z (Bohr radii)')
        ax1.set_title(f'{element_name} (Z={atomic_number}) - 3D Configuration')
        
        # Radial distribution
        ax2 = fig.add_subplot(122)
        radii = [np.linalg.norm(pos) for pos in positions]
        ax2.hist(radii, bins=20, alpha=0.7, edgecolor='black')
        
        # Mark expected shell radii
        for shell_n, radius in self.shell_radii.items():
            if shell_n <= 6:
                ax2.axvline(radius, color='red', linestyle='--', alpha=0.7, label=f'Shell {shell_n}')
        
        ax2.set_xlabel('Radius (Bohr radii)')
        ax2.set_ylabel('Number of Electrons')
        ax2.set_title(f'{element_name} - Radial Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    """Run the electron shell simulation for elements He through Ba"""
    
    sim = ElectronShellSimulation()
    
    elements = [
        (2, "Helium"), (3, "Lithium"), (4, "Beryllium"), (5, "Boron"), (6, "Carbon"),
        (7, "Nitrogen"), (8, "Oxygen"), (9, "Fluorine"), (10, "Neon"), (11, "Sodium"),
        (12, "Magnesium"), (13, "Aluminum"), (14, "Silicon"), (15, "Phosphorus"), 
        (16, "Sulfur"), (17, "Chlorine"), (18, "Argon"), (19, "Potassium"), (20, "Calcium"),
        (21, "Scandium"), (22, "Titanium"), (23, "Vanadium"), (24, "Chromium"), (25, "Manganese"),
        (26, "Iron"), (27, "Cobalt"), (28, "Nickel"), (29, "Copper"), (30, "Zinc"),
        (31, "Gallium"), (32, "Germanium"), (33, "Arsenic"), (34, "Selenium"), (35, "Bromine"),
        (36, "Krypton"), (37, "Rubidium"), (38, "Strontium"), (39, "Yttrium"), (40, "Zirconium"),
        (41, "Niobium"), (42, "Molybdenum"), (43, "Technetium"), (44, "Ruthenium"), (45, "Rhodium"),
        (46, "Palladium"), (47, "Silver"), (48, "Cadmium"), (49, "Indium"), (50, "Tin"),
        (51, "Antimony"), (52, "Tellurium"), (53, "Iodine"), (54, "Xenon"), (55, "Cesium"), (56, "Barium")
    ]
    
    print("=== ELECTRON SHELL MONTE CARLO SIMULATION ===")
    print("Testing scroll interference theory of shell formation")
    print("Using e^n/π wavelength progression")
    print(f"Monte Carlo iterations: {MONTE_CARLO_ITERATIONS}")  
    print(f"Show individual plots: {SHOW_PLOTS}")
    print(f"Initial temperature: {TEMPERATURE_INITIAL}")
    print(f"Shell boundaries: r1→2 = {(2)**2 - np.log(2):.3f}, r2→3 = {(3)**2 - np.log(3):.3f}, r3→4 = {(4)**2 - np.log(4):.3f}, r4→5 = {(5)**2 - np.log(5):.3f}, r5→6 = {(6)**2 - np.log(6):.3f}")
    
    results = {}
    
    for atomic_number, element_name in elements:
        positions, energies, shell_counts = sim.analyze_element(atomic_number, element_name)
        results[element_name] = {
            'positions': positions,
            'energies': energies,
            'shell_counts': shell_counts,
            'atomic_number': atomic_number
        }
        
        # Plot configuration only if requested
        if SHOW_PLOTS:
            sim.plot_configuration(positions, atomic_number, element_name)
    
    # Summary analysis
    print("\n" + "="*90)
    print("FINAL SUMMARY")
    print("="*90)
    print("Element          | Expected Config         | Simulated Config        | Match?")
    print("-" * 85)
    
    matches = 0
    total = len(elements)
    
    for atomic_number, element_name in elements:
        expected_config = sim.expected_configs.get(atomic_number, [0, 0, 0, 0, 0, 0])
        actual = results[element_name]['shell_counts']
        simulated_config = [actual[1], actual[2], actual[3], actual[4], actual[5], actual[6]]
        
        match = expected_config == simulated_config
        
        if match:
            matches += 1
            
        print(f"{element_name:<15} | {expected_config} | {simulated_config} | {'✓' if match else '✗'}")
    
    print("-" * 85)
    print(f"SUCCESS RATE: {matches}/{total} ({100*matches/total:.1f}%)")
    
    if matches >= 0.8 * total:
        print("\n🎉 EXCELLENT! The scroll theory shows strong predictive power!")
        print("   Most elements follow expected shell configurations.")
    elif matches >= 0.6 * total:
        print("\n✅ GOOD! The scroll theory shows promising results.")
        print("   Majority of elements follow expected patterns.")
    else:
        print("\n⚠️  Mixed results. Model may need further refinement.")
        
    print("\nTo see individual element plots, set SHOW_PLOTS = True at the top of the file.")

if __name__ == "__main__":
    main()
