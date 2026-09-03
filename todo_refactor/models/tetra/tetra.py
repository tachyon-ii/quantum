import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import math

class TetrahedralFieldSimulator:
    def __init__(self, edge_length=2.0, field_strength=1.0):
        self.edge_length = edge_length
        self.field_strength = field_strength
        
        # Define tetrahedral vertices (regular tetrahedron)
        h = edge_length * np.sqrt(2/3)
        self.vertices = np.array([
            [edge_length/2, -edge_length/(2*np.sqrt(3)), -h/4],      # vertex 0
            [-edge_length/2, -edge_length/(2*np.sqrt(3)), -h/4],     # vertex 1
            [0, edge_length/np.sqrt(3), -h/4],                       # vertex 2
            [0, 0, 3*h/4]                                             # vertex 3 (apex)
        ])
        
        self.centroid = np.mean(self.vertices, axis=0)
        
        # Define the four faces of the tetrahedron
        self.faces = [
            [0, 1, 2],  # base triangle
            [0, 1, 3],  # face opposite vertex 2
            [1, 2, 3],  # face opposite vertex 0
            [0, 2, 3]   # face opposite vertex 1
        ]
        
        # Calculate face centers and normal vectors
        self.face_centers = []
        self.face_normals = []
        
        for face in self.faces:
            # Face center
            center = np.mean(self.vertices[face], axis=0)
            self.face_centers.append(center)
            
            # Face normal (outward pointing)
            v1 = self.vertices[face[1]] - self.vertices[face[0]]
            v2 = self.vertices[face[2]] - self.vertices[face[0]]
            normal = np.cross(v1, v2)
            
            # Ensure normal points outward from centroid
            to_centroid = self.centroid - center
            if np.dot(normal, to_centroid) > 0:
                normal = -normal
            
            normal = normal / np.linalg.norm(normal)
            self.face_normals.append(normal)
        
        self.face_centers = np.array(self.face_centers)
        self.face_normals = np.array(self.face_normals)
        
        # Rotation parameters
        self.rotation_angle = 0.0
        self.rotation_axis = self.calculate_symmetry_axis()
        
        print(f"Tetrahedron initialized with {len(self.faces)} faces")
        print(f"Face centers: {self.face_centers.shape}")
        print(f"Rotation axis: {self.rotation_axis}")
    
    def calculate_symmetry_axis(self):
        """Calculate one of the tetrahedral symmetry axes (vertex to face center)"""
        # Axis from apex vertex (3) to center of opposite face (base triangle)
        apex = self.vertices[3]
        base_center = np.mean(self.vertices[0:3], axis=0)
        axis = base_center - apex
        return axis / np.linalg.norm(axis)
    
    def rotate_tetrahedron(self, angle):
        """Rotate tetrahedron around symmetry axis by given angle"""
        # Rodrigues' rotation formula
        axis = self.rotation_axis
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        
        K = np.array([
            [0, -axis[2], axis[1]],
            [axis[2], 0, -axis[0]],
            [-axis[1], axis[0], 0]
        ])
        
        R = np.eye(3) + sin_a * K + (1 - cos_a) * np.dot(K, K)
        
        # Rotate vertices around centroid
        rotated_vertices = []
        for vertex in self.vertices:
            relative_pos = vertex - self.centroid
            rotated_pos = np.dot(R, relative_pos)
            rotated_vertices.append(rotated_pos + self.centroid)
        
        self.vertices = np.array(rotated_vertices)
        
        # Recalculate face centers and normals
        self.face_centers = []
        self.face_normals = []
        
        for face in self.faces:
            center = np.mean(self.vertices[face], axis=0)
            self.face_centers.append(center)
            
            v1 = self.vertices[face[1]] - self.vertices[face[0]]
            v2 = self.vertices[face[2]] - self.vertices[face[0]]
            normal = np.cross(v1, v2)
            
            to_centroid = self.centroid - center
            if np.dot(normal, to_centroid) > 0:
                normal = -normal
            
            normal = normal / np.linalg.norm(normal)
            self.face_normals.append(normal)
        
        self.face_centers = np.array(self.face_centers)
        self.face_normals = np.array(self.face_normals)
    
    def calculate_field_intensity(self, points):
        """Calculate electronegative field intensity at given points"""
        field_intensity = np.zeros(len(points))
        
        for face_idx in range(len(self.faces)):
            face_center = self.face_centers[face_idx]
            face_normal = self.face_normals[face_idx]
            
            for i, point in enumerate(points):
                # Vector from face center to point
                to_point = point - face_center
                distance = np.linalg.norm(to_point)
                
                if distance > 0:
                    # Direction from face to point
                    direction = to_point / distance
                    
                    # Check if point is in the "beam" direction (collimated field)
                    alignment = np.dot(direction, face_normal)
                    
                    # Only consider points in the forward hemisphere of the face
                    if alignment > 0:
                        # Collimated beam: intensity depends on alignment and distance
                        # Higher alignment = stronger field
                        # Exponential decay with distance
                        beam_intensity = self.field_strength * (alignment ** 2) * np.exp(-distance / 2.0)
                        field_intensity[i] += beam_intensity
        
        return field_intensity
    
    def create_field_grid(self, grid_size=50, extent=3.0):
        """Create a 3D grid for field calculation"""
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        z = np.linspace(-extent, extent, grid_size)
        
        # Create grid points
        points = []
        for xi in x:
            for yi in y:
                for zi in z:
                    points.append([xi, yi, zi])
        
        return np.array(points), x, y, z
    
    def visualize_field_slice(self, z_slice=0.0, grid_size=100, extent=3.0):
        """Create 2D heat map of field intensity at a given z-slice"""
        # Create 2D grid at specified z-level
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Calculate field intensity
        points = []
        for i in range(grid_size):
            for j in range(grid_size):
                points.append([X[i, j], Y[i, j], z_slice])
        
        field_values = self.calculate_field_intensity(np.array(points))
        field_grid = field_values.reshape(grid_size, grid_size)
        
        # Create heat map
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Custom colormap for electronegative field
        colors = ['black', 'darkblue', 'blue', 'cyan', 'yellow', 'orange', 'red']
        n_bins = 256
        cmap = LinearSegmentedColormap.from_list('electronegative', colors, N=n_bins)
        
        im = ax.imshow(field_grid, extent=[-extent, extent, -extent, extent], 
                      origin='lower', cmap=cmap, alpha=0.8)
        
        # Add contour lines
        contours = ax.contour(X, Y, field_grid, levels=10, colors='white', alpha=0.5, linewidths=0.5)
        ax.clabel(contours, inline=True, fontsize=8, colors='white')
        
        # Project tetrahedron onto the slice
        self.draw_tetrahedron_projection(ax, z_slice)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Field Intensity', fontsize=12, weight='bold')
        
        ax.set_xlabel('X Position', fontsize=12)
        ax.set_ylabel('Y Position', fontsize=12)
        ax.set_title(f'Electronegative Field Heat Map (z = {z_slice:.1f})\n' +
                    f'Rotation angle: {self.rotation_angle * 180/np.pi:.1f}°', 
                    fontsize=14, weight='bold')
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        return fig, ax, field_grid
    
    def draw_tetrahedron_projection(self, ax, z_slice):
        """Draw tetrahedron projection on 2D plot"""
        # Project vertices onto the slice plane
        proj_vertices = []
        for vertex in self.vertices:
            proj_vertices.append([vertex[0], vertex[1]])
        proj_vertices = np.array(proj_vertices)
        
        # Draw edges
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        for edge in edges:
            start, end = edge
            ax.plot([proj_vertices[start, 0], proj_vertices[end, 0]], 
                   [proj_vertices[start, 1], proj_vertices[end, 1]], 
                   'white', linewidth=2, alpha=0.8)
        
        # Draw vertices
        ax.scatter(proj_vertices[:, 0], proj_vertices[:, 1], 
                  c='white', s=100, alpha=1.0, edgecolors='black', linewidth=2, zorder=5)
        
        # Draw face centers and field directions
        colors = ['red', 'blue', 'green', 'orange']
        for i, (center, normal, color) in enumerate(zip(self.face_centers, self.face_normals, colors)):
            # Project face center
            ax.scatter(center[0], center[1], c=color, s=150, alpha=0.9, 
                      edgecolors='white', linewidth=2, marker='s', zorder=5)
            
            # Draw field direction arrow
            arrow_length = 0.5
            arrow_end = center[:2] + arrow_length * normal[:2]
            ax.arrow(center[0], center[1], arrow_end[0] - center[0], arrow_end[1] - center[1],
                    head_width=0.1, head_length=0.08, fc=color, ec='white', 
                    linewidth=2, alpha=0.9, zorder=4)
            
            ax.text(center[0] + 0.2, center[1] + 0.2, f'F{i}', 
                   color='white', fontsize=10, weight='bold', zorder=6)
    
    def create_3d_field_visualization(self, grid_size=30, extent=2.5):
        """Create 3D visualization of field intensity"""
        fig = plt.figure(figsize=(15, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create 3D grid (reduced resolution for performance)
        x = np.linspace(-extent, extent, grid_size)
        y = np.linspace(-extent, extent, grid_size)
        z = np.linspace(-extent, extent, grid_size)
        
        # Sample points more sparsely for 3D visualization
        sample_points = []
        step = max(1, grid_size // 15)  # Sample every few points
        
        for i in range(0, grid_size, step):
            for j in range(0, grid_size, step):
                for k in range(0, grid_size, step):
                    sample_points.append([x[i], y[j], z[k]])
        
        sample_points = np.array(sample_points)
        field_values = self.calculate_field_intensity(sample_points)
        
        # Filter points with significant field intensity
        threshold = np.max(field_values) * 0.1
        significant_points = sample_points[field_values > threshold]
        significant_values = field_values[field_values > threshold]
        
        # Create 3D scatter plot with color mapping
        if len(significant_points) > 0:
            scatter = ax.scatter(significant_points[:, 0], 
                               significant_points[:, 1], 
                               significant_points[:, 2],
                               c=significant_values, cmap='plasma', 
                               s=significant_values * 50, alpha=0.6)
            
            plt.colorbar(scatter, ax=ax, shrink=0.8, label='Field Intensity')
        
        # Draw tetrahedron structure
        self.draw_tetrahedron_3d(ax)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'3D Electronegative Field Distribution\nRotation: {self.rotation_angle * 180/np.pi:.1f}°', 
                    fontsize=14, weight='bold')
        
        return fig, ax
    
    def draw_tetrahedron_3d(self, ax):
        """Draw the tetrahedron with face normal vectors"""
        # Draw edges
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        for edge in edges:
            start, end = edge
            ax.plot3D(*zip(self.vertices[start], self.vertices[end]), 
                     'white', linewidth=3, alpha=0.8)
        
        # Draw vertices
        ax.scatter(self.vertices[:, 0], self.vertices[:, 1], self.vertices[:, 2], 
                  c='white', s=150, alpha=1.0, edgecolors='black', linewidth=2)
        
        # Draw face centers and field direction arrows
        colors = ['red', 'blue', 'green', 'orange']
        for i, (center, normal, color) in enumerate(zip(self.face_centers, self.face_normals, colors)):
            # Face center
            ax.scatter(*center, c=color, s=200, alpha=0.9, 
                      edgecolors='white', linewidth=2, marker='s')
            
            # Field direction arrow
            arrow_end = center + normal * 0.5
            ax.plot3D(*zip(center, arrow_end), color=color, linewidth=4, alpha=0.9)
            
            # Arrow head (simplified)
            ax.scatter(*arrow_end, c=color, s=100, marker='>', alpha=0.9)
            
            ax.text(center[0], center[1], center[2] + 0.2, f'Face {i}', 
                   color=color, fontsize=10, weight='bold')
    
    def create_animated_heat_map(self, num_frames=120, z_slices=[-0.5, 0.0, 0.5]):
        """Create animated heat maps showing rotation"""
        fig, axes = plt.subplots(1, len(z_slices), figsize=(18, 6))
        if len(z_slices) == 1:
            axes = [axes]
        
        # Store initial state
        initial_vertices = self.vertices.copy()
        
        def animate(frame):
            # Calculate rotation angle
            angle = 2 * np.pi * frame / num_frames
            
            # Reset to initial state and rotate
            self.vertices = initial_vertices.copy()
            self.rotate_tetrahedron(angle)
            self.rotation_angle = angle
            
            # Clear and redraw all subplots
            for ax in axes:
                ax.clear()
            
            # Create heat maps for each z-slice
            max_intensity = 0
            field_grids = []
            
            for i, z_slice in enumerate(z_slices):
                fig_temp, ax_temp, field_grid = self.visualize_field_slice(
                    z_slice=z_slice, grid_size=80, extent=2.5)
                field_grids.append(field_grid)
                max_intensity = max(max_intensity, np.max(field_grid))
                plt.close(fig_temp)  # Close temporary figure
            
            # Draw heat maps with consistent color scale
            for i, (z_slice, field_grid) in enumerate(zip(z_slices, field_grids)):
                extent = 2.5
                
                # Custom colormap
                colors = ['black', 'darkblue', 'blue', 'cyan', 'yellow', 'orange', 'red']
                cmap = LinearSegmentedColormap.from_list('electronegative', colors, N=256)
                
                im = axes[i].imshow(field_grid, extent=[-extent, extent, -extent, extent], 
                                  origin='lower', cmap=cmap, alpha=0.8, 
                                  vmin=0, vmax=max_intensity)
                
                # Add contours
                x = np.linspace(-extent, extent, field_grid.shape[1])
                y = np.linspace(-extent, extent, field_grid.shape[0])
                X, Y = np.meshgrid(x, y)
                contours = axes[i].contour(X, Y, field_grid, levels=8, colors='white', alpha=0.4, linewidths=0.5)
                
                # Project tetrahedron
                self.draw_tetrahedron_projection(axes[i], z_slice)
                
                axes[i].set_xlabel('X Position')
                axes[i].set_ylabel('Y Position')
                axes[i].set_title(f'z = {z_slice:.1f}\nAngle: {angle * 180/np.pi:.1f}°')
                axes[i].set_aspect('equal')
                axes[i].grid(True, alpha=0.3)
            
            # Add main title
            fig.suptitle(f'Rotating Tetrahedral Electronegative Field (Frame {frame+1}/{num_frames})', 
                        fontsize=16, weight='bold')
            
            plt.tight_layout()
            return axes
        
        anim = animation.FuncAnimation(fig, animate, frames=num_frames, interval=100, blit=False)
        return fig, anim
    
    def demonstrate_field_system(self):
        """Run complete demonstration"""
        print("=== TETRAHEDRAL ELECTRONEGATIVE FIELD SIMULATION ===")
        
        # Analyze geometry
        print(f"\nSystem Properties:")
        print(f"• Edge length: {self.edge_length:.2f}")
        print(f"• Field strength: {self.field_strength:.2f}")
        print(f"• Number of faces: {len(self.faces)}")
        print(f"• Rotation axis: {self.rotation_axis}")
        
        print(f"\nFace Analysis:")
        for i, (center, normal) in enumerate(zip(self.face_centers, self.face_normals)):
            print(f"• Face {i}: center={center}, normal={normal}")
        
        # Static visualization at different z-levels
        print(f"\n1. Creating static field visualizations...")
        z_levels = [-0.8, 0.0, 0.8]
        
        for z in z_levels:
            fig, ax, field_grid = self.visualize_field_slice(z_slice=z, grid_size=100)
            plt.show()
        
        # 3D field visualization
        print(f"\n2. Creating 3D field visualization...")
        fig_3d, ax_3d = self.create_3d_field_visualization()
        plt.show()
        
        # Rotation demonstration
        print(f"\n3. Demonstrating rotation effects...")
        original_angle = self.rotation_angle
        
        rotation_angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        for angle in rotation_angles:
            print(f"\nRotation angle: {angle * 180/np.pi:.1f}°")
            self.rotate_tetrahedron(angle - self.rotation_angle)
            self.rotation_angle = angle
            
            fig, ax, field_grid = self.visualize_field_slice(z_slice=0.0, grid_size=80)
            plt.show()
        
        return True
    
    def create_rotation_study(self):
        """Study how field pattern changes with rotation"""
        print(f"\n=== ROTATION FIELD STUDY ===")
        
        angles = np.linspace(0, 2*np.pi, 8)
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        axes = axes.flatten()
        
        # Store original state
        original_vertices = self.vertices.copy()
        
        for i, angle in enumerate(angles):
            # Reset and rotate
            self.vertices = original_vertices.copy()
            self.rotate_tetrahedron(angle)
            self.rotation_angle = angle
            
            # Calculate field at z=0
            extent = 2.5
            grid_size = 60
            x = np.linspace(-extent, extent, grid_size)
            y = np.linspace(-extent, extent, grid_size)
            X, Y = np.meshgrid(x, y)
            
            points = []
            for xi in range(grid_size):
                for yi in range(grid_size):
                    points.append([X[xi, yi], Y[xi, yi], 0.0])
            
            field_values = self.calculate_field_intensity(np.array(points))
            field_grid = field_values.reshape(grid_size, grid_size)
            
            # Plot
            colors = ['black', 'darkblue', 'blue', 'cyan', 'yellow', 'orange', 'red']
            cmap = LinearSegmentedColormap.from_list('electronegative', colors, N=256)
            
            im = axes[i].imshow(field_grid, extent=[-extent, extent, -extent, extent], 
                              origin='lower', cmap=cmap, alpha=0.8)
            
            self.draw_tetrahedron_projection(axes[i], 0.0)
            
            axes[i].set_title(f'{angle * 180/np.pi:.0f}°', fontsize=12, weight='bold')
            axes[i].set_aspect('equal')
            
            if i % 4 == 0:
                axes[i].set_ylabel('Y Position')
            if i >= 4:
                axes[i].set_xlabel('X Position')
        
        plt.suptitle('Electronegative Field Evolution During 360° Rotation\n(z = 0.0 slice)', 
                    fontsize=16, weight='bold')
        plt.tight_layout()
        
        return fig, axes

# Run the simulation
if __name__ == "__main__":
    # Create the field simulator
    field_sim = TetrahedralFieldSimulator(edge_length=1.8, field_strength=2.0)
    
    # Run demonstrations
    field_sim.demonstrate_field_system()
    
    # Create rotation study
    fig_rotation, axes_rotation = field_sim.create_rotation_study()
    plt.show()
    
    # Create animated version (uncomment to see animation)
    print(f"\n4. Creating animated heat map...")
    fig_anim, anim = field_sim.create_animated_heat_map(num_frames=60, z_slices=[0.0])
    plt.show()
    
    print(f"\n" + "="*60)
    print("✅ TETRAHEDRAL FIELD SIMULATION COMPLETE")
    print("• Collimated electronegative fields from each face")  
    print("• Heat map visualization with proper intensity decay")
    print("• Rotation around tetrahedral symmetry axis")
    print("• Beautiful interference patterns as tetrahedron spins!")
    print("="*60)
