import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Slider, RadioButtons
import matplotlib.colors as mcolors

class TetrahedronSimulation:
    def __init__(self, disc_radius=0.5):
        self.disc_radius = disc_radius
        self.render_mode = 'disc'  # 'disc' or 'wireframe'
        self.display_mode = 'both'  # 'centroid', 'edge', or 'both'
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0
        self.opacity_decay_distance = 1.0  # Distance at which opacity becomes 0.01
        self.zoom_factor = 0.5  # Controls the view limits
        
        # Get screen size for window sizing
        from matplotlib import pyplot as plt
        manager = plt.get_current_fig_manager()
        
        # Create figure - 80% of screen height
        self.fig = plt.figure(figsize=(14, 11))
        
        # Try to set window size to 80% of screen height
        try:
            if hasattr(manager, 'window'):
                if hasattr(manager.window, 'wm_geometry'):
                    # For TkAgg backend
                    import tkinter as tk
                    root = tk.Tk()
                    screen_height = root.winfo_screenheight()
                    root.destroy()
                    window_height = int(screen_height * 0.8)
                    window_width = int(window_height * 1.2)  # Maintain aspect ratio
                    manager.window.wm_geometry(f"{window_width}x{window_height}")
        except:
            pass  # If we can't set window size, continue with default
        
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Create tetrahedron vertices
        self.vertices = self.create_regular_tetrahedron()
        self.centroid = np.array([0, 0, 0])  # Centroid at origin
        
        # Calculate edge midpoints
        self.edge_midpoints = self.calculate_edge_midpoints()
        
        # Store disc vertices for each plane
        self.centroid_disc_data = self.calculate_centroid_disc_data()
        self.edge_disc_data = self.calculate_edge_disc_data()
        
        # Initial plot
        self.plot_structure()
        
        # Add UI controls
        self.setup_ui()
        
    def create_regular_tetrahedron(self):
        """Create vertices of a regular tetrahedron with one vertex at (0,1,0)"""
        # Start with one vertex straight up at (0,1,0)
        # For a regular tetrahedron centered at origin with edge length that gives distance 1 from center
        
        # The vertices of a regular tetrahedron with one point at (0,1,0)
        # and centered at origin
        sqrt2 = np.sqrt(2)
        sqrt3 = np.sqrt(3)
        
        vertices = np.array([
            [0, 1, 0],  # Top vertex (straight up)
            [2*sqrt2/3, -1/3, 0],  # Bottom vertices form equilateral triangle
            [-sqrt2/3, -1/3, sqrt2/sqrt3],
            [-sqrt2/3, -1/3, -sqrt2/sqrt3]
        ])
        
        return vertices
    
    def calculate_edge_midpoints(self):
        """Calculate midpoints of all 6 edges"""
        A, B, C, D = self.vertices
        edges = [
            (A, B, 'AB'), (A, C, 'AC'), (A, D, 'AD'),
            (B, C, 'BC'), (B, D, 'BD'), (C, D, 'CD')
        ]
        
        midpoints = []
        for p1, p2, label in edges:
            midpoint = (p1 + p2) / 2
            midpoints.append((midpoint, p1, p2, label))
        
        return midpoints
    
    def get_orthogonal_plane_with_gradient(self, p1, p2, center):
        """Get vertices and opacity values for a gradient disc"""
        # Direction vector from p1 to p2
        direction = p2 - p1
        direction = direction / np.linalg.norm(direction)
        
        # Find two orthogonal vectors in the plane
        if abs(direction[0]) < 0.9:
            v1 = np.array([1, 0, 0])
        else:
            v1 = np.array([0, 1, 0])
        
        # Gram-Schmidt to get orthogonal vectors
        u1 = v1 - np.dot(v1, direction) * direction
        u1 = u1 / np.linalg.norm(u1)
        
        u2 = np.cross(direction, u1)
        u2 = u2 / np.linalg.norm(u2)
        
        # Create disc with radial segments for gradient effect
        n_radial = 10  # Number of radial divisions
        n_angular = 30  # Number of angular divisions
        
        polygons = []
        colors = []
        
        for r_idx in range(n_radial):
            r_inner = (r_idx / n_radial) * self.disc_radius
            r_outer = ((r_idx + 1) / n_radial) * self.disc_radius
            
            # Calculate opacity based on exponential decay
            # opacity(r) = exp(-k * r) where k is chosen such that opacity(decay_distance) = 0.01
            # 0.01 = exp(-k * decay_distance) => k = -ln(0.01) / decay_distance
            k = -np.log(0.01) / self.opacity_decay_distance
            
            # Average radius for this ring
            r_avg = (r_inner + r_outer) / 2
            opacity = np.exp(-k * r_avg)
            
            # Create ring segments
            theta = np.linspace(0, 2*np.pi, n_angular)
            
            for t_idx in range(n_angular - 1):
                # Create a quad for each segment
                t1 = theta[t_idx]
                t2 = theta[t_idx + 1]
                
                # Four corners of the quad
                p1_quad = center + r_inner * (np.cos(t1) * u1 + np.sin(t1) * u2)
                p2_quad = center + r_outer * (np.cos(t1) * u1 + np.sin(t1) * u2)
                p3_quad = center + r_outer * (np.cos(t2) * u1 + np.sin(t2) * u2)
                p4_quad = center + r_inner * (np.cos(t2) * u1 + np.sin(t2) * u2)
                
                polygons.append([p1_quad, p2_quad, p3_quad, p4_quad])
                colors.append((0.5, 0.5, 0.5, opacity * 0.5))  # Gray with varying opacity, scaled by 0.5 for visibility
        
        # Also return outer edge for wireframe mode
        outer_edge = []
        theta = np.linspace(0, 2*np.pi, n_angular)
        for t in theta:
            point = center + self.disc_radius * (np.cos(t) * u1 + np.sin(t) * u2)
            outer_edge.append(point)
        
        return polygons, colors, np.array(outer_edge)
    
    def calculate_centroid_disc_data(self):
        """Pre-calculate disc vertices for centroid planes"""
        A, B, C, D = self.vertices
        
        plane_pairs = [
            (A, B, 'AB'), (A, C, 'AC'), (A, D, 'AD'),
            (B, C, 'BC'), (B, D, 'BD'), (C, D, 'CD')
        ]
        
        disc_data = []
        for p1, p2, label in plane_pairs:
            polygons, colors, edge = self.get_orthogonal_plane_with_gradient(p1, p2, self.centroid)
            disc_data.append((polygons, colors, edge, label))
        
        return disc_data
    
    def calculate_edge_disc_data(self):
        """Pre-calculate disc vertices for edge planes"""
        disc_data = []
        
        for midpoint, p1, p2, label in self.edge_midpoints:
            polygons, colors, edge = self.get_orthogonal_plane_with_gradient(p1, p2, midpoint)
            disc_data.append((polygons, colors, edge, label, midpoint))
        
        return disc_data
    
    def rotate_points(self, points, x_rot, y_rot, z_rot):
        """Apply rotation to points"""
        # Convert degrees to radians
        x_rot = np.radians(x_rot)
        y_rot = np.radians(y_rot)
        z_rot = np.radians(z_rot)
        
        # Rotation matrices
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(x_rot), -np.sin(x_rot)],
            [0, np.sin(x_rot), np.cos(x_rot)]
        ])
        
        Ry = np.array([
            [np.cos(y_rot), 0, np.sin(y_rot)],
            [0, 1, 0],
            [-np.sin(y_rot), 0, np.cos(y_rot)]
        ])
        
        Rz = np.array([
            [np.cos(z_rot), -np.sin(z_rot), 0],
            [np.sin(z_rot), np.cos(z_rot), 0],
            [0, 0, 1]
        ])
        
        # Apply rotations
        R = Rz @ Ry @ Rx
        return (R @ points.T).T
    
    def plot_structure(self):
        """Plot the tetrahedron structure"""
        self.ax.clear()
        
        # Recalculate disc data if opacity distance or disc size changed
        self.centroid_disc_data = self.calculate_centroid_disc_data()
        self.edge_disc_data = self.calculate_edge_disc_data()
        
        # Apply rotations to vertices
        rotated_vertices = self.rotate_points(self.vertices, self.x_rotation, self.y_rotation, self.z_rotation)
        A, B, C, D = rotated_vertices
        
        # Plot lines from vertices to centroid
        for vertex in rotated_vertices:
            self.ax.plot3D([vertex[0], 0], [vertex[1], 0], [vertex[2], 0], 
                          'blue', alpha=0.4, linewidth=1.5)
        
        # Plot vertices as blue globes (no labels)
        self.ax.scatter(*rotated_vertices.T, color='blue', s=150, alpha=0.9, 
                       edgecolors='darkblue', linewidth=2)
        
        # Plot tetrahedron edges (faint)
        edges = [
            (A, B), (A, C), (A, D),
            (B, C), (B, D), (C, D)
        ]
        for edge in edges:
            edge_array = np.array(edge)
            self.ax.plot3D(*edge_array.T, 'gray', alpha=0.2, linewidth=0.5)
        
        # Plot centroid orthogonal planes (if enabled)
        if self.display_mode in ['centroid', 'both']:
            for polygons, colors, edge, label in self.centroid_disc_data:
                if self.render_mode == 'disc':
                    # Render as gradient disc
                    for polygon, color in zip(polygons, colors):
                        # Apply rotation to polygon vertices
                        rotated_polygon = [self.rotate_points(np.array(polygon), 
                                                             self.x_rotation, 
                                                             self.y_rotation, 
                                                             self.z_rotation)]
                        poly3d = Poly3DCollection(rotated_polygon, alpha=color[3], 
                                                facecolor=color[:3], edgecolor='none')
                        self.ax.add_collection3d(poly3d)
                else:  # wireframe
                    # Render as wireframe (outer edge only)
                    rotated_edge = self.rotate_points(edge, self.x_rotation, 
                                                     self.y_rotation, self.z_rotation)
                    self.ax.plot3D(*rotated_edge.T, color='gray', linewidth=1, alpha=0.7)
        
        # Plot edge orthogonal planes (if enabled)
        if self.display_mode in ['edge', 'both']:
            for polygons, colors, edge, label, midpoint in self.edge_disc_data:
                if self.render_mode == 'disc':
                    # Render as gradient disc with different color tint for edge discs
                    for polygon, color in zip(polygons, colors):
                        # Apply rotation to polygon vertices
                        rotated_polygon = [self.rotate_points(np.array(polygon), 
                                                             self.x_rotation, 
                                                             self.y_rotation, 
                                                             self.z_rotation)]
                        # Slightly blue tint for edge discs to distinguish from centroid discs
                        edge_color = (color[0] * 0.7, color[1] * 0.7, color[2] * 1.0, color[3])
                        poly3d = Poly3DCollection(rotated_polygon, alpha=edge_color[3], 
                                                facecolor=edge_color[:3], edgecolor='none')
                        self.ax.add_collection3d(poly3d)
                else:  # wireframe
                    # Render as wireframe (outer edge only)
                    rotated_edge = self.rotate_points(edge, self.x_rotation, 
                                                     self.y_rotation, self.z_rotation)
                    self.ax.plot3D(*rotated_edge.T, color='steelblue', linewidth=1, alpha=0.7)
        
        # Plot centroid
        self.ax.scatter(0, 0, 0, color='red', s=30, alpha=0.8, marker='o')
        
        # Set equal aspect ratio
        self.ax.set_box_aspect([1,1,1])
        
        # Set limits based on zoom factor (smaller zoom = bigger tetrahedron in view)
        limit = 1.5 * self.zoom_factor
        self.ax.set_xlim([-limit, limit])
        self.ax.set_ylim([-limit, limit])
        self.ax.set_zlim([-limit, limit])
        
        # Remove all axes elements
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.ax.grid(False)
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')
        self.ax.set_zlabel('')
        
        # Make panes invisible
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')
        
        # Hide axis lines
        self.ax.xaxis.line.set_color('none')
        self.ax.yaxis.line.set_color('none')
        self.ax.zaxis.line.set_color('none')
        
        # Set viewing angle
        self.ax.view_init(elev=20, azim=45)
        
        plt.draw()
    
    def setup_ui(self):
        """Setup UI controls"""
        # Adjust layout to make room for controls
        plt.subplots_adjust(left=0.15, bottom=0.30, right=0.9, top=0.95)
        
        # Create slider axes
        ax_x_rot = plt.axes([0.2, 0.20, 0.6, 0.025])
        ax_y_rot = plt.axes([0.2, 0.16, 0.6, 0.025])
        ax_z_rot = plt.axes([0.2, 0.12, 0.6, 0.025])
        ax_opacity = plt.axes([0.2, 0.08, 0.6, 0.025])
        ax_disc_size = plt.axes([0.2, 0.04, 0.6, 0.025])
        ax_zoom = plt.axes([0.2, 0.005, 0.6, 0.025])
        
        # Create sliders
        self.slider_x = Slider(ax_x_rot, 'X Rotation', 0, 360, valinit=0, valstep=1)
        self.slider_y = Slider(ax_y_rot, 'Y Rotation', 0, 360, valinit=0, valstep=1)
        self.slider_z = Slider(ax_z_rot, 'Z Rotation', 0, 360, valinit=0, valstep=1)
        self.slider_opacity = Slider(ax_opacity, 'Opacity Decay Distance', 0.5, 10, 
                                    valinit=1.0, valstep=0.1)
        self.slider_disc_size = Slider(ax_disc_size, 'Disc Size', 0.1, 0.9, 
                                      valinit=0.5, valstep=0.05)
        self.slider_zoom = Slider(ax_zoom, 'Zoom', 0.2, 1.5, 
                                valinit=0.5, valstep=0.05)
        
        # Create radio buttons for render mode
        rax_render = plt.axes([0.02, 0.6, 0.12, 0.08])
        self.radio_render = RadioButtons(rax_render, ('Disc', 'Wireframe'))
        
        # Create radio buttons for display mode
        rax_display = plt.axes([0.02, 0.45, 0.12, 0.12])
        self.radio_display = RadioButtons(rax_display, ('Centroid Only', 'Edge Only', 'Both'))
        self.radio_display.set_active(2)  # Set 'Both' as default
        
        # Connect event handlers
        self.slider_x.on_changed(self.update_rotation)
        self.slider_y.on_changed(self.update_rotation)
        self.slider_z.on_changed(self.update_rotation)
        self.slider_opacity.on_changed(self.update_opacity)
        self.slider_disc_size.on_changed(self.update_disc_size)
        self.slider_zoom.on_changed(self.update_zoom)
        self.radio_render.on_clicked(self.update_render_mode)
        self.radio_display.on_clicked(self.update_display_mode)
    
    def update_rotation(self, val):
        """Update rotation based on slider values"""
        self.x_rotation = self.slider_x.val
        self.y_rotation = self.slider_y.val
        self.z_rotation = self.slider_z.val
        self.plot_structure()
    
    def update_opacity(self, val):
        """Update opacity decay distance"""
        self.opacity_decay_distance = self.slider_opacity.val
        self.plot_structure()
    
    def update_disc_size(self, val):
        """Update disc radius"""
        self.disc_radius = self.slider_disc_size.val
        self.plot_structure()
    
    def update_zoom(self, val):
        """Update zoom factor"""
        self.zoom_factor = self.slider_zoom.val
        self.plot_structure()
    
    def update_render_mode(self, label):
        """Update render mode based on radio button selection"""
        self.render_mode = 'disc' if label == 'Disc' else 'wireframe'
        self.plot_structure()
    
    def update_display_mode(self, label):
        """Update display mode based on radio button selection"""
        if label == 'Centroid Only':
            self.display_mode = 'centroid'
        elif label == 'Edge Only':
            self.display_mode = 'edge'
        else:  # 'Both'
            self.display_mode = 'both'
        self.plot_structure()
    
    def show(self):
        """Display the plot"""
        plt.show()

# Run the simulation
if __name__ == "__main__":
    # Initial disc radius
    disc_radius = 0.5
    sim = TetrahedronSimulation(disc_radius=disc_radius)
    sim.show()
