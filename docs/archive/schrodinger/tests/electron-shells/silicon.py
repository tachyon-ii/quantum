import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

class NuclearPackingSimulation:
    def __init__(self, num_nucleons=28, particle_radius=1.0, exclusion_zone=True):
        self.num_nucleons = num_nucleons
        self.particle_radius = particle_radius
        self.exclusion_zone = exclusion_zone
        self.exclusion_radius = particle_radius if exclusion_zone else 0.0
        
        # Lennard-Jones-like potential parameters
        self.sigma = 2.0 * particle_radius  # Equilibrium distance
        self.epsilon = 1.0  # Energy depth
        
        # Initialize random positions
        self.positions = self.initialize_positions()
        
        # Tracking
        self.energy_history = []
        self.best_energy = float('inf')
        self.best_positions = None
        
    def initialize_positions(self):
        """Initialize nucleons in random positions avoiding exclusion zone"""
        positions = []
        max_attempts = 1000
        
        for i in range(self.num_nucleons):
            attempts = 0
            while attempts < max_attempts:
                # Random position in sphere of radius 5
                r = np.random.uniform(self.exclusion_radius + self.particle_radius, 5.0)
                theta = np.random.uniform(0, 2*np.pi)
                phi = np.random.uniform(0, np.pi)
                
                x = r * np.sin(phi) * np.cos(theta)
                y = r * np.sin(phi) * np.sin(theta)
                z = r * np.cos(phi)
                
                new_pos = np.array([x, y, z])
                
                # Check if position is valid (not too close to existing nucleons)
                valid = True
                for existing_pos in positions:
                    distance = np.linalg.norm(new_pos - existing_pos)
                    if distance < 1.5 * self.particle_radius:
                        valid = False
                        break
                
                # Check exclusion zone
                if self.exclusion_zone:
                    center_distance = np.linalg.norm(new_pos)
                    if center_distance < self.exclusion_radius + self.particle_radius:
                        valid = False
                
                if valid:
                    positions.append(new_pos)
                    break
                    
                attempts += 1
            
            if attempts >= max_attempts:
                print(f"Warning: Could not place nucleon {i+1} in valid position")
                # Place it anyway at a random location
                r = np.random.uniform(3.0, 5.0)
                theta = np.random.uniform(0, 2*np.pi)
                phi = np.random.uniform(0, np.pi)
                x = r * np.sin(phi) * np.cos(theta)
                y = r * np.sin(phi) * np.sin(theta)
                z = r * np.cos(phi)
                positions.append(np.array([x, y, z]))
        
        return np.array(positions)
    
    def lennard_jones_potential(self, r):
        """Modified Lennard-Jones potential for nuclear forces"""
        if r <= 0:
            return float('inf')
        
        # Attractive at optimal distance, repulsive when too close
        sigma_r = self.sigma / r
        potential = 4 * self.epsilon * (sigma_r**12 - sigma_r**6)
        
        # Add additional short-range repulsion to prevent overlap
        if r < self.particle_radius * 1.8:
            potential += 100 * (self.particle_radius * 1.8 / r)**24
            
        return potential
    
    def calculate_total_energy(self):
        """Calculate total potential energy of the system"""
        total_energy = 0.0
        
        for i in range(self.num_nucleons):
            for j in range(i + 1, self.num_nucleons):
                distance = np.linalg.norm(self.positions[i] - self.positions[j])
                total_energy += self.lennard_jones_potential(distance)
        
        return total_energy
    
    def calculate_forces(self):
        """Calculate forces on each nucleon"""
        forces = np.zeros_like(self.positions)
        
        for i in range(self.num_nucleons):
            for j in range(self.num_nucleons):
                if i != j:
                    r_vec = self.positions[i] - self.positions[j]
                    r = np.linalg.norm(r_vec)
                    
                    if r > 0:
                        # Derivative of Lennard-Jones potential
                        sigma_r = self.sigma / r
                        force_magnitude = 4 * self.epsilon * (12 * sigma_r**12 / r - 6 * sigma_r**6 / r)
                        
                        # Additional short-range repulsion force
                        if r < self.particle_radius * 1.8:
                            force_magnitude += 100 * 24 * (self.particle_radius * 1.8)**24 / r**25
                        
                        force_vec = force_magnitude * r_vec / r
                        forces[i] += force_vec
        
        return forces
    
    def monte_carlo_step(self, temperature=1.0):
        """Perform one Monte Carlo step"""
        # Select random nucleon
        nucleon_idx = random.randint(0, self.num_nucleons - 1)
        
        # Store original position
        original_pos = self.positions[nucleon_idx].copy()
        
        # Calculate original energy
        original_energy = self.calculate_total_energy()
        
        # Generate random displacement
        max_displacement = 0.5
        displacement = np.random.uniform(-max_displacement, max_displacement, 3)
        new_pos = original_pos + displacement
        
        # Check exclusion zone constraint
        if self.exclusion_zone:
            center_distance = np.linalg.norm(new_pos)
            if center_distance < self.exclusion_radius + self.particle_radius:
                return False  # Reject move
        
        # Apply new position temporarily
        self.positions[nucleon_idx] = new_pos
        
        # Calculate new energy
        new_energy = self.calculate_total_energy()
        
        # Accept or reject based on Metropolis criterion
        energy_diff = new_energy - original_energy
        
        if energy_diff < 0 or random.random() < np.exp(-energy_diff / temperature):
            # Accept move
            if new_energy < self.best_energy:
                self.best_energy = new_energy
                self.best_positions = self.positions.copy()
            return True
        else:
            # Reject move - restore original position
            self.positions[nucleon_idx] = original_pos
            return False
    
    def molecular_dynamics_step(self, dt=0.001, damping=0.95):
        """Perform one molecular dynamics step with damping"""
        forces = self.calculate_forces()
        
        # Simple Euler integration with damping
        self.positions += forces * dt
        self.positions *= damping  # Add damping to reach equilibrium
        
        # Apply exclusion zone constraint
        if self.exclusion_zone:
            for i in range(self.num_nucleons):
                center_distance = np.linalg.norm(self.positions[i])
                if center_distance < self.exclusion_radius + self.particle_radius:
                    # Push nucleon outside exclusion zone
                    direction = self.positions[i] / center_distance
                    self.positions[i] = direction * (self.exclusion_radius + self.particle_radius + 0.1)
    
    def simulate(self, steps=10000, method='monte_carlo'):
        """Run the simulation"""
        print(f"Starting simulation: {self.num_nucleons} nucleons, exclusion_zone={self.exclusion_zone}")
        print(f"Method: {method}, Steps: {steps}")
        
        for step in range(steps):
            if method == 'monte_carlo':
                # Decrease temperature over time (simulated annealing)
                temperature = 10.0 * np.exp(-step / (steps / 5))
                self.monte_carlo_step(temperature)
            else:  # molecular_dynamics
                self.molecular_dynamics_step()
            
            # Record energy every 100 steps
            if step % 100 == 0:
                current_energy = self.calculate_total_energy()
                self.energy_history.append(current_energy)
                
                if step % 1000 == 0:
                    print(f"Step {step}: Energy = {current_energy:.2f}")
        
        final_energy = self.calculate_total_energy()
        print(f"Final energy: {final_energy:.2f}")
        print(f"Best energy found: {self.best_energy:.2f}")
        
        return self.best_positions if self.best_positions is not None else self.positions
    
    def analyze_structure(self):
        """Analyze the final structure"""
        positions = self.best_positions if self.best_positions is not None else self.positions
        
        # Calculate all pairwise distances
        distances = []
        for i in range(self.num_nucleons):
            for j in range(i + 1, self.num_nucleons):
                distance = np.linalg.norm(positions[i] - positions[j])
                distances.append(distance)
        
        distances = np.array(distances)
        
        print(f"\nStructural Analysis:")
        print(f"Mean interparticle distance: {np.mean(distances):.3f}")
        print(f"Std deviation: {np.std(distances):.3f}")
        print(f"Min distance: {np.min(distances):.3f}")
        print(f"Max distance: {np.max(distances):.3f}")
        
        # Look for common distances (potential shell structure)
        hist, bin_edges = np.histogram(distances, bins=20)
        peak_bins = np.where(hist > np.max(hist) * 0.3)[0]
        
        print(f"\nPotential shell radii (common distances):")
        for bin_idx in peak_bins:
            bin_center = (bin_edges[bin_idx] + bin_edges[bin_idx + 1]) / 2
            print(f"  Distance ~{bin_center:.3f}: {hist[bin_idx]} pairs")
        
        return distances
    
    def plot_results(self):
        """Plot the simulation results"""
        positions = self.best_positions if self.best_positions is not None else self.positions
        
        fig = plt.figure(figsize=(15, 5))
        
        # 3D structure plot
        ax1 = fig.add_subplot(131, projection='3d')
        ax1.scatter(positions[:, 0], positions[:, 1], positions[:, 2], 
                   c='red', s=100, alpha=0.7)
        
        # Draw exclusion zone
        if self.exclusion_zone:
            u = np.linspace(0, 2 * np.pi, 50)
            v = np.linspace(0, np.pi, 50)
            x_sphere = self.exclusion_radius * np.outer(np.cos(u), np.sin(v))
            y_sphere = self.exclusion_radius * np.outer(np.sin(u), np.sin(v))
            z_sphere = self.exclusion_radius * np.outer(np.ones(np.size(u)), np.cos(v))
            ax1.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.2, color='blue')
        
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title(f'3D Structure (Exclusion Zone: {self.exclusion_zone})')
        
        # Energy history
        ax2 = fig.add_subplot(132)
        ax2.plot(self.energy_history)
        ax2.set_xlabel('Step (x100)')
        ax2.set_ylabel('Total Energy')
        ax2.set_title('Energy vs Time')
        ax2.grid(True)
        
        # Distance distribution
        ax3 = fig.add_subplot(133)
        distances = self.analyze_structure()
        ax3.hist(distances, bins=30, alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Interparticle Distance')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Distance Distribution')
        ax3.grid(True)
        
        plt.tight_layout()
        plt.show()

def compare_simulations():
    """Compare simulations with and without exclusion zone"""
    print("="*60)
    print("SILICON-28 NUCLEAR PACKING SIMULATION")
    print("="*60)
    
    # Simulation with exclusion zone
    print("\n" + "="*40)
    print("SIMULATION 1: WITH EXCLUSION ZONE")
    print("="*40)
    sim1 = NuclearPackingSimulation(num_nucleons=28, exclusion_zone=True)
    final_pos1 = sim1.simulate(steps=8000, method='monte_carlo')
    sim1.plot_results()
    
    # Simulation without exclusion zone
    print("\n" + "="*40)
    print("SIMULATION 2: WITHOUT EXCLUSION ZONE")
    print("="*40)
    sim2 = NuclearPackingSimulation(num_nucleons=28, exclusion_zone=False)
    final_pos2 = sim2.simulate(steps=8000, method='monte_carlo')
    sim2.plot_results()
    
    print("\n" + "="*40)
    print("COMPARISON SUMMARY")
    print("="*40)
    print(f"Best energy with exclusion zone: {sim1.best_energy:.2f}")
    print(f"Best energy without exclusion zone: {sim2.best_energy:.2f}")
    
    if sim1.best_energy < sim2.best_energy:
        print("➜ Exclusion zone configuration is more stable")
    else:
        print("➜ No exclusion zone configuration is more stable")

if __name__ == "__main__":
    compare_simulations()
