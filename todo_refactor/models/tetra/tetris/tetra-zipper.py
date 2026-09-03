import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def create_equilateral_base(side_length=1):
    """Create vertices of an equilateral triangle base in xy-plane"""
    # Centered at origin
    angles = np.array([0, 2*np.pi/3, 4*np.pi/3])
    radius = side_length / np.sqrt(3)
    
    vertices = []
    for angle in angles:
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        vertices.append([x, y, 0])
    
    return np.array(vertices)

def create_three_triangles(base_vertices, peak_height, zipper_factor):
    """
    Create 3 equilateral triangles attached to the base edges
    that meet at a common peak point above the centroid
    
    peak_height: Height of the peak above the base plane
    zipper_factor: 0 = flat/open, 1 = fully zipped together
    """
    
    # Calculate base centroid
    centroid = np.mean(base_vertices, axis=0)
    
    # Peak point - directly above centroid
    peak = centroid + np.array([0, 0, peak_height])
    
    # Edge lengths
    edge_length = np.linalg.norm(base_vertices[1] - base_vertices[0])
    
    triangles = []
    fold_lines = []
    
    for i in range(3):
        # Get base edge vertices
        v1 = base_vertices[i]
        v2 = base_vertices[(i + 1) % 3]
        
        # Midpoint of base edge
        edge_mid = (v1 + v2) / 2
        
        # For an equilateral triangle, the third vertex would be at height √3/2 * edge_length
        # from the base edge, in the plane perpendicular to the edge
        
        # Direction from edge midpoint to centroid (for initial flat position)
        to_center = centroid - edge_mid
        to_center_2d = to_center.copy()
        to_center_2d[2] = 0  # Project to xy plane
        to_center_2d = to_center_2d / np.linalg.norm(to_center_2d)
        
        # Initial position of triangle apex (flat configuration)
        flat_height = edge_length * np.sqrt(3) / 2
        flat_apex = edge_mid + to_center_2d * flat_height
        
        # Interpolate between flat position and peak position based on zipper_factor
        # As we zip, the apex moves from flat position to the common peak
        current_apex = (1 - zipper_factor) * flat_apex + zipper_factor * peak
        
        # Create the triangle
        triangle = [v1, v2, current_apex]
        triangles.append(triangle)
        
        # Add fold/ridge lines (from base vertices to peak)
        if zipper_factor > 0.1:
            fold_lines.append([v1, current_apex])
            fold_lines.append([v2, current_apex])
    
    # Add center fold lines (from peak to base vertices) when mostly zipped
    if zipper_factor > 0.5:
        for v in base_vertices:
            fold_lines.append([v, peak])
    
    return triangles, peak, fold_lines

def visualize_star_face():
    """Create interactive visualization of a single star face"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Initial parameters
    init_height = 0.8
    init_zipper = 0.0
    init_rotation = 0
    
    def update(val=None):
        ax.clear()
        
        # Remove grid and axes
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.xaxis.line.set_visible(False)
        ax.yaxis.line.set_visible(False)
        ax.zaxis.line.set_visible(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('none')
        ax.yaxis.pane.set_edgecolor('none')
        ax.zaxis.pane.set_edgecolor('none')
        
        # Get slider values
        peak_height = slider_height.val
        zipper = slider_zipper.val
        rotation = slider_rotation.val
        
        # Create base triangle
        base_vertices = create_equilateral_base()
        
        # Apply rotation around z-axis
        rot_angle = np.radians(rotation)
        rot_matrix = np.array([
            [np.cos(rot_angle), -np.sin(rot_angle), 0],
            [np.sin(rot_angle), np.cos(rot_angle), 0],
            [0, 0, 1]
        ])
        base_vertices = (rot_matrix @ base_vertices.T).T
        
        # Create the 3 triangles
        triangles, peak, fold_lines = create_three_triangles(base_vertices, peak_height, zipper)
        
        # Draw base triangle
        base_poly = Poly3DCollection([base_vertices], alpha=0.3, 
                                    facecolor='gray', edgecolor='black', linewidth=2)
        ax.add_collection3d(base_poly)
        
        # Draw the 3 triangles with different colors
        colors = ['red', 'green', 'blue']
        for i, triangle in enumerate(triangles):
            poly = Poly3DCollection([triangle], alpha=0.4, 
                                   facecolor=colors[i], edgecolor='black', linewidth=1.5)
            ax.add_collection3d(poly)
        
        # Draw fold/ridge lines
        for line in fold_lines:
            line_array = np.array(line)
            ax.plot(line_array[:, 0], line_array[:, 1], line_array[:, 2], 
                   'k--', linewidth=1, alpha=0.5)
        
        # Mark the peak point
        ax.scatter([peak[0]], [peak[1]], [peak[2]], c='gold', s=100, marker='*')
        
        # Mark base vertices
        ax.scatter(base_vertices[:, 0], base_vertices[:, 1], base_vertices[:, 2], 
                  c='black', s=50, marker='o')
        
        # Mark the centroid
        centroid = np.mean(base_vertices, axis=0)
        ax.scatter([centroid[0]], [centroid[1]], [centroid[2]], 
                  c='purple', s=30, marker='o', alpha=0.5)
        
        # Draw vertical line from centroid to peak
        ax.plot([centroid[0], peak[0]], [centroid[1], peak[1]], [centroid[2], peak[2]], 
               'purple', linewidth=1, alpha=0.3)
        
        # Set equal aspect ratio and limits
        max_range = 1.2
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([0, max_range])
        ax.set_box_aspect([1, 1, 1])
        
        # Set viewing angle
        ax.view_init(elev=25, azim=45)
        
        # Add status text
        if zipper < 0.1:
            status = "Open: 3 equilateral triangles attached to base edges"
        elif zipper < 0.9:
            status = f"Zipping: {zipper*100:.0f}% - edges coming together"
        else:
            status = "Fully zipped: Tetrahedral star point formed"
        
        ax.text2D(0.5, 0.95, status, transform=ax.transAxes, 
                 ha='center', fontsize=12, weight='bold')
        
        # Add description of what we're seeing
        if zipper > 0.7:
            ax.text2D(0.5, 0.90, "Edges meet to form ridges (inward folds)", 
                     transform=ax.transAxes, ha='center', fontsize=10, style='italic')
        
        plt.draw()
    
    # Create sliders
    plt.subplots_adjust(bottom=0.25)
    
    ax_height = plt.axes([0.2, 0.15, 0.6, 0.03])
    ax_zipper = plt.axes([0.2, 0.10, 0.6, 0.03])
    ax_rotation = plt.axes([0.2, 0.05, 0.6, 0.03])
    
    slider_height = Slider(ax_height, 'Peak Height', 0.1, 1.5, valinit=init_height, 
                          valstep=0.01, color='gold')
    slider_zipper = Slider(ax_zipper, 'Zipper', 0, 1, valinit=init_zipper, 
                          valstep=0.01, valfmt='%.2f', color='green')
    slider_rotation = Slider(ax_rotation, 'Rotation', 0, 360, valinit=init_rotation, 
                           valstep=1, valfmt='%d°', color='purple')
    
    slider_height.on_changed(update)
    slider_zipper.on_changed(update)
    slider_rotation.on_changed(update)
    
    # Add explanation text
    fig.text(0.5, 0.02, '3 equilateral triangles → 1 tetrahedral star point', 
             ha='center', fontsize=11, weight='bold')
    
    # Initial plot
    update()
    
    plt.show()

if __name__ == "__main__":
    visualize_star_face()
