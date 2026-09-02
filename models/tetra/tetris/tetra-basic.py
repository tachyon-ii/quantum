import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons
from mpl_toolkits.mplot3d import Axes3D

def create_regular_hexagon():
    """Create vertices of a regular hexagon centered at origin in xy-plane"""
    angles = np.linspace(0, 2*np.pi, 7)[:-1]  # 6 vertices
    x = np.cos(angles)
    y = np.sin(angles)
    z = np.zeros_like(x)
    return np.column_stack([x, y, z])

def create_tetrahedron():
    """Create vertices of a regular tetrahedron"""
    # Regular tetrahedron vertices
    vertices = np.array([
        [1, 1, 1],
        [1, -1, -1],
        [-1, 1, -1],
        [-1, -1, 1]
    ]) / np.sqrt(3)
    
    # Define the 4 triangular faces (indices into vertices)
    faces = [
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ]
    
    return vertices, faces

def rotation_matrix(x_angle, y_angle, z_angle):
    """Create combined rotation matrix from X, Y, Z angles (in degrees)"""
    # Convert to radians
    rx = np.radians(x_angle)
    ry = np.radians(y_angle)
    rz = np.radians(z_angle)
    
    # Rotation around X axis
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(rx), -np.sin(rx)],
                   [0, np.sin(rx), np.cos(rx)]])
    
    # Rotation around Y axis
    Ry = np.array([[np.cos(ry), 0, np.sin(ry)],
                   [0, 1, 0],
                   [-np.sin(ry), 0, np.cos(ry)]])
    
    # Rotation around Z axis
    Rz = np.array([[np.cos(rz), -np.sin(rz), 0],
                   [np.sin(rz), np.cos(rz), 0],
                   [0, 0, 1]])
    
    # Combined rotation: Z * Y * X
    return Rz @ Ry @ Rx

def rotate_around_center(vertices, center, rot_matrix):
    """Rotate vertices around a specific center point"""
    # Translate to origin
    translated = vertices - center
    # Rotate
    rotated = (rot_matrix @ translated.T).T
    # Translate back
    return rotated + center

def map_hexagon_to_tetrahedron_face(triangle_vertices, hexagon_factor, distortion_factor, star_factor, tet_center):
    """
    Map a hexagon onto a triangular face of the tetrahedron.
    Every 2nd vertex of the hexagon maps to a vertex of the triangle.
    
    hexagon_factor: -1 = outward (hexagon), 0 = on edges (triangle), +1 = inward toward face center
    distortion_factor: -1 = toward tetrahedron center, 0 = on face, +1 = outward from face
    star_factor: 0 = normal hexagon, +1 = star shape (pull intermediate vertices from hexagon center)
    """
    
    # Get triangle vertices - THESE ARE FIXED
    v0, v1, v2 = triangle_vertices
    
    # Calculate face center and normal
    face_center = (v0 + v1 + v2) / 3
    face_normal = np.cross(v1 - v0, v2 - v0)
    face_normal = face_normal / np.linalg.norm(face_normal)
    
    # Make sure normal points outward from tetrahedron
    to_center = tet_center - face_center
    if np.dot(face_normal, to_center) > 0:
        face_normal = -face_normal
    
    distorted = np.zeros((6, 3))
    
    # FIXED vertices: hexagon vertices 0, 2, 4 -> triangle vertices (NEVER MOVE)
    distorted[0] = v0
    distorted[2] = v1
    distorted[4] = v2
    
    # Calculate intermediate vertex positions
    if hexagon_factor != 0:
        # Calculate the direction for each edge
        # Positive hexagon_factor: push toward face center
        # Negative hexagon_factor: push away from face center (forming hexagon)
        
        # Vertex 1: between v0 and v1
        edge_01_mid = (v0 + v1) / 2
        to_center_01 = face_center - edge_01_mid
        to_center_01 = to_center_01 - np.dot(to_center_01, face_normal) * face_normal  # Project onto face plane
        to_center_01 = to_center_01 / np.linalg.norm(to_center_01)
        
        # Calculate push distance for hexagon shape
        edge_length = np.linalg.norm(v1 - v0)
        push_distance = edge_length * np.tan(np.pi/6) / 2
        
        # Vertex 3: between v1 and v2
        edge_23_mid = (v1 + v2) / 2
        to_center_23 = face_center - edge_23_mid
        to_center_23 = to_center_23 - np.dot(to_center_23, face_normal) * face_normal
        to_center_23 = to_center_23 / np.linalg.norm(to_center_23)
        
        # Vertex 5: between v2 and v0
        edge_45_mid = (v2 + v0) / 2
        to_center_45 = face_center - edge_45_mid
        to_center_45 = to_center_45 - np.dot(to_center_45, face_normal) * face_normal
        to_center_45 = to_center_45 / np.linalg.norm(to_center_45)
        
        # Apply hexagon_factor:
        # Negative: push outward from center (form hexagon)
        # Positive: push inward toward center
        # The push distance is scaled by abs(hexagon_factor)
        distorted[1] = edge_01_mid + to_center_01 * push_distance * hexagon_factor
        distorted[3] = edge_23_mid + to_center_23 * push_distance * hexagon_factor
        distorted[5] = edge_45_mid + to_center_45 * push_distance * hexagon_factor
        
    else:
        # hexagon_factor = 0, just place on edge midpoints (triangle shape)
        distorted[1] = (v0 + v1) / 2
        distorted[3] = (v1 + v2) / 2
        distorted[5] = (v2 + v0) / 2
    
    # Calculate initial hexagon centroid
    hex_centroid = np.mean(distorted, axis=0)
    
    # Apply star distortion: move the CENTROID outward from face
    if star_factor != 0:
        # Move centroid outward along face normal
        centroid_displacement = face_normal * star_factor * 0.5
        hex_centroid = hex_centroid + centroid_displacement
        
        # The intermediate vertices (1, 3, 5) also move with the centroid displacement
        # This creates the star effect - they're pulled along as the center pushes out
        for i in [1, 3, 5]:
            distorted[i] += centroid_displacement
    
    # Apply face distortion ONLY to intermediate vertices (1, 3, 5)
    # Vertices 0, 2, 4 remain FIXED at tetrahedron vertices
    if distortion_factor != 0:
        for i in [1, 3, 5]:  # Only move intermediate vertices
            if distortion_factor < 0:
                # Negative: move toward tetrahedron center
                to_tet_center = tet_center - distorted[i]
                move_distance = np.linalg.norm(to_tet_center) * abs(distortion_factor) * 0.5
                move_direction = to_tet_center / np.linalg.norm(to_tet_center)
            else:
                # Positive: move outward from face
                move_distance = distortion_factor * 0.5
                move_direction = face_normal
            
            distorted[i] += move_direction * move_distance
    
    # Return both the distorted hexagon and its centroid
    return distorted, hex_centroid

def visualize_distortion():
    """Create interactive visualization with sliders"""
    fig = plt.figure(figsize=(12, 8))  # Reduced height from 10 to 8
    ax = fig.add_subplot(111, projection='3d')
    
    # Create initial tetrahedron
    tet_vertices, tet_faces = create_tetrahedron()
    tet_center = np.mean(tet_vertices, axis=0)
    
    # Initial parameters
    init_x_rot, init_y_rot, init_z_rot = 0, 0, 0
    init_hex = 0  # Start at 0 (on edges)
    init_dist = 0  # No distortion initially
    init_star = 0  # No star distortion initially
    
    # Face visibility flags
    face_visible = [True, True, True, True]
    
    def update(val=None):
        # Clear axes
        ax.clear()
        
        # Remove grid and axis elements
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
        x_rot = slider_x.val
        y_rot = slider_y.val
        z_rot = slider_z.val
        hex_factor = slider_hex.val / 100.0  # Convert to -1 to 1 range
        dist_factor = slider_dist.val / 100.0  # Convert to -1 to 1 range
        star_factor = slider_star.val / 100.0  # Convert to 0 to 1 range
        
        # Apply rotation around tetrahedron center
        rot_matrix = rotation_matrix(x_rot, y_rot, z_rot)
        rotated_tet_vertices = rotate_around_center(tet_vertices, tet_center, rot_matrix)
        
        # Draw BLACK tetrahedron edges (more prominent)
        for face_idx in tet_faces:
            face_vertices = rotated_tet_vertices[face_idx]
            face_loop = np.vstack([face_vertices, face_vertices[0]])
            ax.plot(face_loop[:, 0], face_loop[:, 1], face_loop[:, 2], 
                   'k-', linewidth=2, alpha=0.8)
        
        # Apply hexagons to each face - TREAT ALL FACES IDENTICALLY
        colors = ['red', 'green', 'blue', 'orange']
        
        for i, face_idx in enumerate(tet_faces):
            # Skip if face is not visible
            if not face_visible[i]:
                continue
                
            face_vertices = rotated_tet_vertices[face_idx]
            
            # Map hexagon to this triangular face
            mapped_hex, hex_centroid = map_hexagon_to_tetrahedron_face(
                face_vertices,
                hex_factor,
                dist_factor,
                star_factor,
                tet_center  # Use original center for distortion direction
            )
            
            # Plot hexagon edges
            hex_plot = np.vstack([mapped_hex, mapped_hex[0]])
            ax.plot(hex_plot[:, 0], hex_plot[:, 1], hex_plot[:, 2], 
                    color=colors[i], linewidth=2.5, alpha=0.9)
            
            # Always draw lines from vertices to centroid and show centroid
            # Draw lines from all 6 vertices to centroid (creating star pattern)
            for j in range(6):
                ax.plot([mapped_hex[j, 0], hex_centroid[0]], 
                       [mapped_hex[j, 1], hex_centroid[1]], 
                       [mapped_hex[j, 2], hex_centroid[2]], 
                       color=colors[i], alpha=0.4, linewidth=1.0)
            
            # Draw the centroid as a vertex (same size as intermediate vertices)
            ax.scatter(hex_centroid[0], hex_centroid[1], hex_centroid[2], 
                     c=colors[i], s=60, marker='o', alpha=0.9)
            
            # Plot intermediate vertices (movable)
            for j in [1, 3, 5]:
                ax.scatter(mapped_hex[j, 0], mapped_hex[j, 1], mapped_hex[j, 2], 
                         c=colors[i], s=60, marker='o', alpha=0.8)
        
        # Draw BLACK dots for the 4 fixed tetrahedron vertices (on top of everything)
        ax.scatter(rotated_tet_vertices[:, 0], rotated_tet_vertices[:, 1], rotated_tet_vertices[:, 2], 
                  c='black', s=150, marker='o', zorder=1000)
        
        # Set equal limits to maintain aspect ratio
        max_range = 1.5
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])
        
        # Set equal aspect ratio
        ax.set_box_aspect([1,1,1])
        
        # Fixed viewing angle
        ax.view_init(elev=20, azim=45)
        
        plt.draw()
    
    def on_check(label):
        """Handle checkbox clicks"""
        index = int(label.split()[-1]) - 1  # Extract face number
        face_visible[index] = not face_visible[index]
        update()
    
    # Create sliders
    plt.subplots_adjust(bottom=0.30, right=0.85)
    
    # Rotation sliders
    ax_x = plt.axes([0.15, 0.22, 0.55, 0.03])
    ax_y = plt.axes([0.15, 0.18, 0.55, 0.03])
    ax_z = plt.axes([0.15, 0.14, 0.55, 0.03])
    
    # Shape sliders
    ax_hex = plt.axes([0.15, 0.10, 0.55, 0.03])
    ax_dist = plt.axes([0.15, 0.06, 0.55, 0.03])
    ax_star = plt.axes([0.15, 0.02, 0.55, 0.03])
    
    slider_x = Slider(ax_x, 'X Rotation', -180, 180, valinit=init_x_rot, valstep=1, valfmt='%d°', color='red')
    slider_y = Slider(ax_y, 'Y Rotation', -180, 180, valinit=init_y_rot, valstep=1, valfmt='%d°', color='green')
    slider_z = Slider(ax_z, 'Z Rotation', -180, 180, valinit=init_z_rot, valstep=1, valfmt='%d°', color='blue')
    
    slider_hex = Slider(ax_hex, 'Hexagon Shape', -100, 100, valinit=init_hex, valstep=1, valfmt='%+d%%', color='purple')
    slider_dist = Slider(ax_dist, 'Face Distortion', -100, 100, valinit=init_dist, valstep=1, valfmt='%+d%%', color='orange')
    slider_star = Slider(ax_star, 'Star Distortion', 0, 100, valinit=init_star, valstep=1, valfmt='%d%%', color='gold')
    
    slider_x.on_changed(update)
    slider_y.on_changed(update)
    slider_z.on_changed(update)
    slider_hex.on_changed(update)
    slider_dist.on_changed(update)
    slider_star.on_changed(update)
    
    # Create checkboxes for face visibility with larger size
    rax = plt.axes([0.75, 0.45, 0.18, 0.25])  # Made taller for larger checkboxes
    labels = ['Face 1', 'Face 2', 'Face 3', 'Face 4']
    check = CheckButtons(rax, labels, [True, True, True, True])
    check.on_clicked(on_check)
    
    # Color the text labels to match face colors
    colors = ['red', 'green', 'blue', 'orange']
    for i, text in enumerate(check.labels):
        text.set_color(colors[i])
        text.set_fontsize(12)  # Larger text
        text.set_weight('bold')
    
    # Try to make checkboxes larger and color them if possible
    try:
        if hasattr(check, 'rectangles'):
            for i, rect in enumerate(check.rectangles):
                rect.set_height(0.05)  # Larger checkbox
                rect.set_width(0.05)
                rect.set_facecolor(colors[i])
                rect.set_alpha(0.2)
        if hasattr(check, 'lines'):
            for i in range(len(labels)):
                if i < len(check.lines[0]):
                    check.lines[0][i].set_color(colors[i])
                    check.lines[0][i].set_linewidth(3)  # Thicker check marks
                if i < len(check.lines[1]):
                    check.lines[1][i].set_color(colors[i])
                    check.lines[1][i].set_linewidth(3)
    except:
        # If styling fails, checkboxes still work with colored text
        pass
    
    # Initial plot
    update()
    
    plt.show()

if __name__ == "__main__":
    visualize_distortion()
