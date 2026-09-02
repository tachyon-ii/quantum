import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ElectronPairGeometry:
    def __init__(self):
        # Shell radii based on n^2 scaling
        self.shell_radii = {1: 1.0, 2: 4.0, 3: 9.0, 4: 16.0, 5: 25.0, 6: 36.0}
        
        # Mathematical constants
        self.e = np.e
        self.pi = np.pi
        
    def shell_1_antipodal_pair(self, radius=1.0):
        """Shell 1: 1 pair (2 electrons) at antipodal points on sphere"""
        # Two electrons as far apart as possible on shell 1
        # One at north pole, one at south pole
        pair_positions = [
            (0.0, 0.0, radius),   # North pole
            (0.0, 0.0, -radius)   # South pole
        ]
        return pair_positions
    
    def shell_2_tetrahedral_pairs(self, radius=4.0):
        """Shell 2: 4 pairs in tetrahedral arrangement"""
        # Regular tetrahedron vertices, scaled to shell radius
        tetrahedron = np.array([
            [ 1,  1,  1],
            [ 1, -1, -1],
            [-1,  1, -1],
            [-1, -1,  1]
        ])
        
        # Normalize to unit sphere, then scale to shell radius
        tetrahedron = tetrahedron / np.linalg.norm(tetrahedron[0])
        tetrahedron *= radius
        
        pairs = []
        for vertex in tetrahedron:
            pairs.append(tuple(vertex))
        
        return pairs
    
    def shell_3_optimal_9_pairs(self, radius=9.0):
        """Shell 3: 9 pairs - need to find optimal arrangement"""
        # This is where we need to solve for the optimal 9-point arrangement
        # For now, let's use a rough approximation based on icosahedral symmetry
        
        # Start with vertices of a triangular antiprism + 3 equatorial points
        angles = np.linspace(0, 2*np.pi, 9, endpoint=False)
        
        pairs = []
        # 6 points in two triangular rings
        for i in range(6):
            theta = angles[i]
            if i < 3:
                z = 0.5  # Upper ring
            else:
                z = -0.5  # Lower ring
                theta += np.pi/3  # Offset lower ring
            
            x = np.sqrt(1 - z**2) * np.cos(theta)
            y = np.sqrt(1 - z**2) * np.sin(theta)
            
            # Normalize and scale
            norm = np.sqrt(x**2 + y**2 + z**2)
            pairs.append((radius * x/norm, radius * y/norm, radius * z/norm))
        
        # Add 3 equatorial points
        for i in range(3):
            theta = angles[i] + np.pi/6
            x = np.cos(theta)
            y = np.sin(theta)
            z = 0.0
            pairs.append((radius * x, radius * y, radius * z))
        
        return pairs[:9]  # Ensure exactly 9 pairs
    
    def shell_4_optimal_16_pairs(self, radius=16.0):
        """Shell 4: 16 pairs - optimal arrangement unknown"""
        # Use compound of cube and octahedron as approximation
        pairs = []
        
        # 8 vertices of a cube
        cube_vertices = [
            [ 1,  1,  1], [ 1,  1, -1], [ 1, -1,  1], [ 1, -1, -1],
            [-1,  1,  1], [-1,  1, -1], [-1, -1,  1], [-1, -1, -1]
        ]
        
        # 6 vertices of an octahedron
        octa_vertices = [
            [ 1,  0,  0], [-1,  0,  0],
            [ 0,  1,  0], [ 0, -1,  0],
            [ 0,  0,  1], [ 0,  0, -1]
        ]
        
        # Combine and scale
        all_vertices = cube_vertices + octa_vertices
        
        for vertex in all_vertices[:16]:  # Take first 16
            norm = np.linalg.norm(vertex)
            vertex = np.array(vertex) / norm * radius
            pairs.append(tuple(vertex))
        
        return pairs
    
    def calculate_pair_distances(self, pairs):
        """Calculate all pairwise distances between electron pairs"""
        distances = []
        n_pairs = len(pairs)
        
        for i in range(n_pairs):
            for j in range(i+1, n_pairs):
                pos1 = np.array(pairs[i])
                pos2 = np.array(pairs[j])
                distance = np.linalg.norm(pos1 - pos2)
                distances.append(distance)
        
        return distances
    
    def find_characteristic_wavelength(self, shell_n, pairs):
        """
        Find the characteristic wavelength that would create interference
        patterns corresponding to the observed pair separations
        """
        distances = self.calculate_pair_distances(pairs)
        
        # The key insight: if e^n/π wavelengths create these patterns,
        # then the distances should be related to wavelength multiples
        
        wavelength_en_pi = 1.0 / (self.e**shell_n / self.pi)
        
        # Check how distances relate to this wavelength
        wavelength_ratios = [d / wavelength_en_pi for d in distances]
        
        return {
            'shell': shell_n,
            'pairs': len(pairs),
            'distances': distances,
            'min_distance': min(distances),
            'max_distance': max(distances),
            'mean_distance': np.mean(distances),
            'wavelength_en_pi': wavelength_en_pi,
            'wavelength_ratios': wavelength_ratios,
            'mean_ratio': np.mean(wavelength_ratios)
        }
    
    def analyze_shell_geometry(self, shell_n):
        """Analyze the geometry of a specific shell"""
        if shell_n == 1:
            pairs = self.shell_1_antipodal_pair()
            analysis = self.find_characteristic_wavelength(shell_n, pairs)
            analysis['geometry'] = 'antipodal_pair'
            analysis['positions'] = pairs
        elif shell_n == 2:
            pairs = self.shell_2_tetrahedral_pairs()
            analysis = self.find_characteristic_wavelength(shell_n, pairs)
            analysis['geometry'] = 'tetrahedral'
            analysis['positions'] = pairs
        elif shell_n == 3:
            pairs = self.shell_3_optimal_9_pairs()
            analysis = self.find_characteristic_wavelength(shell_n, pairs)
            analysis['geometry'] = 'triangular_antiprism_plus'
            analysis['positions'] = pairs
        elif shell_n == 4:
            pairs = self.shell_4_optimal_16_pairs()
            analysis = self.find_characteristic_wavelength(shell_n, pairs)
            analysis['geometry'] = 'cube_octahedron_compound'
            analysis['positions'] = pairs
        else:
            return None
        
        return analysis
    
    def plot_shell_geometry(self, shell_n):
        """Visualize the geometry of electron pairs in a shell"""
        analysis = self.analyze_shell_geometry(shell_n)
        if analysis is None:
            print(f"Shell {shell_n} not implemented")
            return
        
        if shell_n == 1:
            print(f"Shell 1: Antipodal pair (dipole) at radius {self.shell_radii[1]}")
            
        positions = analysis['positions']
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot electron pair positions
        x_coords = [pos[0] for pos in positions]
        y_coords = [pos[1] for pos in positions]
        z_coords = [pos[2] for pos in positions]
        
        ax.scatter(x_coords, y_coords, z_coords, s=100, c='red', alpha=0.8)
        
        # Draw sphere outline
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        radius = self.shell_radii[shell_n]
        
        x_sphere = radius * np.outer(np.cos(u), np.sin(v))
        y_sphere = radius * np.outer(np.sin(u), np.sin(v))
        z_sphere = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1, color='blue')
        
        # Connect pairs with lines to show structure
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                pos1 = positions[i]
                pos2 = positions[j]
                ax.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], [pos1[2], pos2[2]], 
                       'k-', alpha=0.3, linewidth=0.5)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Shell {shell_n}: {analysis["geometry"]} ({len(positions)} pairs)')
        
        plt.tight_layout()
        plt.show()
        
        return analysis

def main():
    """Analyze theoretical optimal electron pair arrangements"""
    
    geom = ElectronPairGeometry()
    
    print("=== THEORETICAL OPTIMAL ELECTRON PAIR POSITIONS ===")
    print("Finding base wavelength from perfect geometric arrangements")
    print()
    
    # Analyze shells 1-4
    all_analyses = []
    
    for shell_n in range(1, 5):
        analysis = geom.analyze_shell_geometry(shell_n)
        if analysis:
            all_analyses.append(analysis)
            
            print(f"Shell {shell_n} Analysis:")
            print(f"  Geometry: {analysis.get('geometry', 'N/A')}")
            print(f"  Number of pairs: {analysis['pairs']}")
            
            if shell_n > 1:
                print(f"  e^{shell_n}/π wavelength: {analysis['wavelength_en_pi']:.6f}")
                print(f"  Distance range: {analysis['min_distance']:.3f} - {analysis['max_distance']:.3f}")
                print(f"  Mean distance: {analysis['mean_distance']:.3f}")
                print(f"  Mean wavelength ratio: {analysis['mean_ratio']:.3f}")
                
                # Key insight: what base frequency would make the mean ratio = integer?
                target_ratios = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
                for target in target_ratios:
                    base_freq = analysis['mean_distance'] / target
                    base_wavelength = 1.0 / base_freq
                    print(f"    For ratio {target}: base wavelength = {base_wavelength:.6f}")
            
            print()
    
    # Look for patterns across shells
    print("=== PATTERN ANALYSIS ===")
    
    if len(all_analyses) > 2:
        shell2 = all_analyses[1]  # Shell 2
        shell3 = all_analyses[2]  # Shell 3
        
        ratio_2_to_3 = shell3['mean_distance'] / shell2['mean_distance']
        wavelength_ratio = shell3['wavelength_en_pi'] / shell2['wavelength_en_pi']
        
        print(f"Shell 2 mean distance: {shell2['mean_distance']:.6f}")
        print(f"Shell 3 mean distance: {shell3['mean_distance']:.6f}")
        print(f"Distance ratio (3/2): {ratio_2_to_3:.6f}")
        print(f"Wavelength ratio (3/2): {wavelength_ratio:.6f}")
        print()
        
        # Critical insight: what base wavelength makes interference constructive/destructive?
        print("Base wavelength candidates (for constructive/destructive interference):")
        
        for shell in all_analyses[1:]:  # Skip shell 1
            shell_n = shell['shell']
            mean_dist = shell['mean_distance']
            
            # For destructive interference (opposite spin pairs): distance = λ/2
            lambda_destructive = 2 * mean_dist
            
            # For constructive interference (same spin pairs): distance = λ
            lambda_constructive = mean_dist
            
            print(f"  Shell {shell_n}:")
            print(f"    Destructive λ: {lambda_destructive:.6f}")
            print(f"    Constructive λ: {lambda_constructive:.6f}")
            print(f"    e^{shell_n}/π gives: {shell['wavelength_en_pi']:.6f}")

if __name__ == "__main__":
    main()
