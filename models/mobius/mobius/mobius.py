import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

class MobiusFigure8:
    def __init__(self):
        """Initialize the Figure-8 Möbius strip with specified properties."""
        self.width = 0.3  # Start with sensible default
        self.ortho_amplitude = 0.5  # Amplitude for orthogonal line
        self.parallel_amplitude = 0.5  # Amplitude for parallel line
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        
        # Resolution
        self.u_res = 400  # High resolution for smooth twist
        self.v_res = 30
        
    def generate_surface(self):
        """Generate the figure-8 Möbius strip surface."""
        # The surface path is 4π (twice around the 2π centerline)
        u = np.linspace(0, 4 * np.pi, self.u_res)
        v = np.linspace(-self.width/2, self.width/2, self.v_res)
        U, V = np.meshgrid(u, v)
        
        # Map surface parameter to centerline parameter
        # Surface goes 0->4π, centerline goes 0->2π (traversed twice)
        t = np.mod(U, 2 * np.pi)  # Centerline parameter
        
        # Lemniscate parametrization for centerline - REDUCED SIZE BY 25%
        scale = 4.5  # Reduced from 6 to 4.5 (75% of original)
        a = scale * np.sqrt(2)
        
        # Standard lemniscate: x = a*cos(t)/(1+sin²(t)), y = a*sin(t)*cos(t)/(1+sin²(t))
        denominator = 1 + np.sin(t)**2
        cx = a * np.cos(t) / denominator
        cy = a * np.sin(t) * np.cos(t) / denominator
        cz = np.zeros_like(cx)
        
        # Calculate tangent vectors along centerline
        dt = 0.01  # Increased from 0.001 to avoid numerical issues
        t_plus = np.mod(t + dt, 2 * np.pi)
        t_minus = np.mod(t - dt, 2 * np.pi)
        
        denom_plus = 1 + np.sin(t_plus)**2
        denom_minus = 1 + np.sin(t_minus)**2
        
        cx_plus = a * np.cos(t_plus) / denom_plus
        cy_plus = a * np.sin(t_plus) * np.cos(t_plus) / denom_plus
        
        cx_minus = a * np.cos(t_minus) / denom_minus
        cy_minus = a * np.sin(t_minus) * np.cos(t_minus) / denom_minus
        
        # Tangent vector
        tx = (cx_plus - cx_minus) / (2 * dt)
        ty = (cy_plus - cy_minus) / (2 * dt)
        tz = np.zeros_like(tx)
        
        # Normalize tangent with safety check
        t_mag = np.sqrt(tx**2 + ty**2 + tz**2)
        t_mag = np.where(t_mag < 1e-10, 1.0, t_mag)  # Avoid division by zero
        tx /= t_mag
        ty /= t_mag
        tz /= t_mag
        
        # Initial normal vector (perpendicular to tangent, starting vertical)
        nx_init = np.zeros_like(tx)
        ny_init = np.zeros_like(ty)
        nz_init = np.ones_like(tz)
        
        # Make perpendicular to tangent using Gram-Schmidt
        dot = tx * nx_init + ty * ny_init + tz * nz_init
        nx_init -= dot * tx
        ny_init -= dot * ty
        nz_init -= dot * tz
        
        # Normalize with safety check
        n_mag = np.sqrt(nx_init**2 + ny_init**2 + nz_init**2)
        n_mag = np.where(n_mag < 1e-10, 1.0, n_mag)  # Avoid division by zero
        nx_init /= n_mag
        ny_init /= n_mag
        nz_init /= n_mag
        
        # Calculate binormal (perpendicular to both tangent and normal)
        bx = ty * nz_init - tz * ny_init
        by = tz * nx_init - tx * nz_init
        bz = tx * ny_init - ty * nx_init
        
        # CRITICAL: Total twist is π over 2π centerline = 0.5 radians per unit
        # But we need to account for the fact that U goes from 0 to 4π
        # When U=0 to 2π: first traversal with twist from 0 to π
        # When U=2π to 4π: second traversal with twist from π to 2π
        twist = U * 0.5  # This gives 2π total twist over 4π path
        
        cos_twist = np.cos(twist)
        sin_twist = np.sin(twist)
        
        # Rotate the normal vector around the tangent by the twist angle
        # This gives us the normal to the surface (ribbon width direction)
        nx = cos_twist * nx_init + sin_twist * bx
        ny = cos_twist * ny_init + sin_twist * by
        nz = cos_twist * nz_init + sin_twist * bz
        
        # Create the surface by displacing from centerline along twisted normal
        X = cx + V * nx
        Y = cy + V * ny
        Z = cz + V * nz
        
        # Create centerline for visualization (just one loop)
        t_line = np.linspace(0, 2 * np.pi, 200)
        denom_line = 1 + np.sin(t_line)**2
        centerline_x = a * np.cos(t_line) / denom_line
        centerline_y = a * np.sin(t_line) * np.cos(t_line) / denom_line
        centerline_z = np.zeros_like(centerline_x)
        
        # Create lines for full 4π path
        u_lines = np.linspace(0, 4 * np.pi, self.u_res)
        t_lines = np.mod(u_lines, 2 * np.pi)
        
        # Get centerline positions for lines
        denom_lines = 1 + np.sin(t_lines)**2
        cx_lines = a * np.cos(t_lines) / denom_lines
        cy_lines = a * np.sin(t_lines) * np.cos(t_lines) / denom_lines
        cz_lines = np.zeros_like(cx_lines)
        
        # Calculate directions at each point (same process as above)
        dt = 0.01
        t_plus_l = np.mod(t_lines + dt, 2 * np.pi)
        t_minus_l = np.mod(t_lines - dt, 2 * np.pi)
        
        denom_plus_l = 1 + np.sin(t_plus_l)**2
        denom_minus_l = 1 + np.sin(t_minus_l)**2
        
        cx_plus_l = a * np.cos(t_plus_l) / denom_plus_l
        cy_plus_l = a * np.sin(t_plus_l) * np.cos(t_plus_l) / denom_plus_l
        cx_minus_l = a * np.cos(t_minus_l) / denom_minus_l
        cy_minus_l = a * np.sin(t_minus_l) * np.cos(t_minus_l) / denom_minus_l
        
        tx_l = (cx_plus_l - cx_minus_l) / (2 * dt)
        ty_l = (cy_plus_l - cy_minus_l) / (2 * dt)
        tz_l = np.zeros_like(tx_l)
        
        t_mag_l = np.sqrt(tx_l**2 + ty_l**2 + tz_l**2)
        t_mag_l = np.where(t_mag_l < 1e-10, 1.0, t_mag_l)
        tx_l /= t_mag_l
        ty_l /= t_mag_l
        tz_l /= t_mag_l
        
        # Initial normal for lines
        nx_init_l = np.zeros_like(tx_l)
        ny_init_l = np.zeros_like(ty_l)
        nz_init_l = np.ones_like(tz_l)
        
        dot_l = tx_l * nx_init_l + ty_l * ny_init_l + tz_l * nz_init_l
        nx_init_l -= dot_l * tx_l
        ny_init_l -= dot_l * ty_l
        nz_init_l -= dot_l * tz_l
        
        n_mag_l = np.sqrt(nx_init_l**2 + ny_init_l**2 + nz_init_l**2)
        n_mag_l = np.where(n_mag_l < 1e-10, 1.0, n_mag_l)
        nx_init_l /= n_mag_l
        ny_init_l /= n_mag_l
        nz_init_l /= n_mag_l
        
        bx_l = ty_l * nz_init_l - tz_l * ny_init_l
        by_l = tz_l * nx_init_l - tx_l * nz_init_l
        bz_l = tx_l * ny_init_l - ty_l * nx_init_l
        
        # Apply same twist to get ribbon normal
        twist_l = u_lines * 0.5
        cos_twist_l = np.cos(twist_l)
        sin_twist_l = np.sin(twist_l)
        
        nx_l = cos_twist_l * nx_init_l + sin_twist_l * bx_l
        ny_l = cos_twist_l * ny_init_l + sin_twist_l * by_l
        nz_l = cos_twist_l * nz_init_l + sin_twist_l * bz_l
        
        # PARALLEL lines - displaced along the ribbon normal (width direction)
        # Two lines: one at +amplitude and one at -amplitude
        parallel_x_pos = cx_lines + self.parallel_amplitude * nx_l
        parallel_y_pos = cy_lines + self.parallel_amplitude * ny_l
        parallel_z_pos = cz_lines + self.parallel_amplitude * nz_l
        
        parallel_x_neg = cx_lines - self.parallel_amplitude * nx_l
        parallel_y_neg = cy_lines - self.parallel_amplitude * ny_l
        parallel_z_neg = cz_lines - self.parallel_amplitude * nz_l
        
        # LADDER RUNGS - lines across the width of the strip
        # Sample points along the 4π path for rungs
        n_rungs = 90  # Tripled from 30 to 90
        u_rungs = np.linspace(0, 4 * np.pi, n_rungs)
        t_rungs = np.mod(u_rungs, 2 * np.pi)
        
        # Get positions and directions for each rung
        rungs_x = []
        rungs_y = []
        rungs_z = []
        
        for i in range(n_rungs):
            # Get centerline position for this rung
            t_pt = t_rungs[i]
            denom_pt = 1 + np.sin(t_pt)**2
            cx_pt = a * np.cos(t_pt) / denom_pt
            cy_pt = a * np.sin(t_pt) * np.cos(t_pt) / denom_pt
            cz_pt = 0
            
            # Calculate tangent at this point
            denom_plus_pt = 1 + np.sin(t_pt + dt)**2
            denom_minus_pt = 1 + np.sin(t_pt - dt)**2
            
            cx_plus_pt = a * np.cos(t_pt + dt) / denom_plus_pt
            cy_plus_pt = a * np.sin(t_pt + dt) * np.cos(t_pt + dt) / denom_plus_pt
            cx_minus_pt = a * np.cos(t_pt - dt) / denom_minus_pt
            cy_minus_pt = a * np.sin(t_pt - dt) * np.cos(t_pt - dt) / denom_minus_pt
            
            tx_pt = (cx_plus_pt - cx_minus_pt) / (2 * dt)
            ty_pt = (cy_plus_pt - cy_minus_pt) / (2 * dt)
            tz_pt = 0
            
            # Normalize
            t_mag_pt = np.sqrt(tx_pt**2 + ty_pt**2 + tz_pt**2)
            if t_mag_pt < 1e-10:
                t_mag_pt = 1.0
            tx_pt /= t_mag_pt
            ty_pt /= t_mag_pt
            tz_pt /= t_mag_pt
            
            # Initial normal
            nx_init_pt = 0
            ny_init_pt = 0
            nz_init_pt = 1
            
            # Gram-Schmidt
            dot_pt = tx_pt * nx_init_pt + ty_pt * ny_init_pt + tz_pt * nz_init_pt
            nx_init_pt -= dot_pt * tx_pt
            ny_init_pt -= dot_pt * ty_pt
            nz_init_pt -= dot_pt * tz_pt
            
            # Normalize
            n_mag_pt = np.sqrt(nx_init_pt**2 + ny_init_pt**2 + nz_init_pt**2)
            if n_mag_pt < 1e-10:
                n_mag_pt = 1.0
            nx_init_pt /= n_mag_pt
            ny_init_pt /= n_mag_pt
            nz_init_pt /= n_mag_pt
            
            # Binormal
            bx_pt = ty_pt * nz_init_pt - tz_pt * ny_init_pt
            by_pt = tz_pt * nx_init_pt - tx_pt * nz_init_pt
            bz_pt = tx_pt * ny_init_pt - ty_pt * nx_init_pt
            
            # Apply twist
            twist_pt = u_rungs[i] * 0.5
            cos_twist_pt = np.cos(twist_pt)
            sin_twist_pt = np.sin(twist_pt)
            
            # The normal across the width (ribbon direction)
            nx_pt = cos_twist_pt * nx_init_pt + sin_twist_pt * bx_pt
            ny_pt = cos_twist_pt * ny_init_pt + sin_twist_pt * by_pt
            nz_pt = cos_twist_pt * nz_init_pt + sin_twist_pt * bz_pt
            
            # Create rung from -parallel_amplitude to +parallel_amplitude along the ribbon normal
            # This connects the two yellow parallel lines
            rung_x = [cx_pt + self.parallel_amplitude * nx_pt, cx_pt - self.parallel_amplitude * nx_pt]
            rung_y = [cy_pt + self.parallel_amplitude * ny_pt, cy_pt - self.parallel_amplitude * ny_pt]
            rung_z = [cz_pt + self.parallel_amplitude * nz_pt, cz_pt - self.parallel_amplitude * nz_pt]
            
            rungs_x.append(rung_x)
            rungs_y.append(rung_y)
            rungs_z.append(rung_z)
        
        # ORTHOGONAL line - perpendicular to the surface plane
        # Cross product of tangent and ribbon normal
        ortho_x_dir = ty_l * nz_l - tz_l * ny_l
        ortho_y_dir = tz_l * nx_l - tx_l * nz_l
        ortho_z_dir = tx_l * ny_l - ty_l * nx_l
        
        # Normalize
        ortho_mag = np.sqrt(ortho_x_dir**2 + ortho_y_dir**2 + ortho_z_dir**2)
        ortho_mag = np.where(ortho_mag < 1e-10, 1.0, ortho_mag)
        ortho_x_dir /= ortho_mag
        ortho_y_dir /= ortho_mag
        ortho_z_dir /= ortho_mag
        
        # Create orthogonal line displaced by amplitude (only positive)
        ortho_x = cx_lines + self.ortho_amplitude * ortho_x_dir
        ortho_y = cy_lines + self.ortho_amplitude * ortho_y_dir
        ortho_z = cz_lines + self.ortho_amplitude * ortho_z_dir
        
        # Apply rotations
        X, Y, Z = self.apply_rotations(X, Y, Z)
        centerline_x, centerline_y, centerline_z = self.apply_rotations(
            centerline_x, centerline_y, centerline_z
        )
        parallel_x_pos, parallel_y_pos, parallel_z_pos = self.apply_rotations(
            parallel_x_pos, parallel_y_pos, parallel_z_pos
        )
        parallel_x_neg, parallel_y_neg, parallel_z_neg = self.apply_rotations(
            parallel_x_neg, parallel_y_neg, parallel_z_neg
        )
        ortho_x, ortho_y, ortho_z = self.apply_rotations(
            ortho_x, ortho_y, ortho_z
        )
        
        # Apply rotations to rungs
        rotated_rungs_x = []
        rotated_rungs_y = []
        rotated_rungs_z = []
        
        for i in range(len(rungs_x)):
            rx, ry, rz = self.apply_rotations(
                np.array(rungs_x[i]),
                np.array(rungs_y[i]),
                np.array(rungs_z[i])
            )
            rotated_rungs_x.append(rx)
            rotated_rungs_y.append(ry)
            rotated_rungs_z.append(rz)
        
        self.centerline = (centerline_x, centerline_y, centerline_z)
        self.parallel_line_pos = (parallel_x_pos, parallel_y_pos, parallel_z_pos)
        self.parallel_line_neg = (parallel_x_neg, parallel_y_neg, parallel_z_neg)
        self.orthogonal_line = (ortho_x, ortho_y, ortho_z)
        self.rungs = (rotated_rungs_x, rotated_rungs_y, rotated_rungs_z)
        self.normals = (nx, ny, nz)
        
        return X, Y, Z
    
    def apply_rotations(self, x, y, z):
        """Apply rotation transformations."""
        # X rotation
        if self.rotation_x != 0:
            cos_x = np.cos(self.rotation_x)
            sin_x = np.sin(self.rotation_x)
            y_new = y * cos_x - z * sin_x
            z_new = y * sin_x + z * cos_x
            y, z = y_new, z_new
        
        # Y rotation
        if self.rotation_y != 0:
            cos_y = np.cos(self.rotation_y)
            sin_y = np.sin(self.rotation_y)
            x_new = x * cos_y + z * sin_y
            z_new = -x * sin_y + z * cos_y
            x, z = x_new, z_new
        
        # Z rotation
        if self.rotation_z != 0:
            cos_z = np.cos(self.rotation_z)
            sin_z = np.sin(self.rotation_z)
            x_new = x * cos_z - y * sin_z
            y_new = x * sin_z + y * cos_z
            x, y = x_new, y_new
        
        return x, y, z

def create_interactive_plot():
    """Create the interactive plot."""
    mobius = MobiusFigure8()
    
    fig = plt.figure(figsize=(12, 8))  # Reduced height to 80%
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(left=0.1, bottom=0.35)
    
    # Generate initial surface
    X, Y, Z = mobius.generate_surface()
    
    # Lighter grey color for the surface (0.85)
    grey_color = np.ones((X.shape[0], X.shape[1], 4)) * 0.85
    grey_color[:, :, 3] = 0.8  # Alpha channel
    
    # Plot surface in light grey
    surf = ax.plot_surface(X, Y, Z, facecolors=grey_color, 
                           edgecolor='none', shade=True)
    
    # Plot black centerline
    cx, cy, cz = mobius.centerline
    ax.plot(cx, cy, cz, 'k-', linewidth=1.0)
    
    # Check if the attributes exist before plotting
    if hasattr(mobius, 'parallel_line_pos') and hasattr(mobius, 'parallel_line_neg'):
        # Plot parallel lines in yellow (even thinner) - two lines
        px_pos, py_pos, pz_pos = mobius.parallel_line_pos
        px_neg, py_neg, pz_neg = mobius.parallel_line_neg
        ax.plot(px_pos, py_pos, pz_pos, 'y-', linewidth=0.25, alpha=0.7)
        ax.plot(px_neg, py_neg, pz_neg, 'y-', linewidth=0.25, alpha=0.7)
    
    if hasattr(mobius, 'orthogonal_line'):
        # Plot orthogonal line in blue (thinner)
        ox, oy, oz = mobius.orthogonal_line
        ax.plot(ox, oy, oz, 'b-', linewidth=0.5, alpha=0.7)
    
    if hasattr(mobius, 'rungs'):
        # Plot ladder rungs in yellow (even thinner)
        rungs_x, rungs_y, rungs_z = mobius.rungs
        for i in range(len(rungs_x)):
            ax.plot(rungs_x[i], rungs_y[i], rungs_z[i], 'y-', linewidth=0.35, alpha=0.8)
    
    # Remove all grid, labels, and axis elements
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')
    ax.xaxis.line.set_visible(False)
    ax.yaxis.line.set_visible(False)
    ax.zaxis.line.set_visible(False)
    ax.xaxis.pane.set_visible(False)
    ax.yaxis.pane.set_visible(False)
    ax.zaxis.pane.set_visible(False)
    
    # Set aspect ratio
    ax.set_box_aspect([1, 0.6, 0.5])
    
    # Set viewing angle
    ax.view_init(elev=20, azim=45)
    
    # Set initial limits to show full model
    max_range = 6  # Adjusted for 75% model size
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range*0.6, max_range*0.6])
    ax.set_zlim([-max_range*0.5, max_range*0.5])
    
    # Create sliders
    ax_width = plt.axes([0.15, 0.25, 0.7, 0.03])
    ax_parallel = plt.axes([0.15, 0.20, 0.7, 0.03])
    ax_ortho = plt.axes([0.15, 0.15, 0.7, 0.03])
    ax_rotx = plt.axes([0.15, 0.10, 0.7, 0.03])
    ax_roty = plt.axes([0.15, 0.05, 0.7, 0.03])
    ax_rotz = plt.axes([0.15, 0.00, 0.7, 0.03])
    
    slider_width = Slider(ax_width, 'Strip Width', 0.1, 1.0, valinit=mobius.width)
    slider_parallel = Slider(ax_parallel, 'Parallel Line Position', 0.0, 1.0, valinit=mobius.parallel_amplitude)
    slider_ortho = Slider(ax_ortho, 'Orthogonal Height', 0.0, 2.0, valinit=mobius.ortho_amplitude)
    slider_rotx = Slider(ax_rotx, 'Rotation X', -np.pi, np.pi, valinit=0)
    slider_roty = Slider(ax_roty, 'Rotation Y', -np.pi, np.pi, valinit=0)
    slider_rotz = Slider(ax_rotz, 'Rotation Z', -np.pi, np.pi, valinit=0)
    
    def update(val):
        """Update the plot."""
        mobius.width = slider_width.val
        mobius.parallel_amplitude = slider_parallel.val
        mobius.ortho_amplitude = slider_ortho.val
        mobius.rotation_x = slider_rotx.val
        mobius.rotation_y = slider_roty.val
        mobius.rotation_z = slider_rotz.val
        
        ax.clear()
        
        # Regenerate surface
        X, Y, Z = mobius.generate_surface()
        
        # Lighter grey color
        grey_color = np.ones((X.shape[0], X.shape[1], 4)) * 0.85
        grey_color[:, :, 3] = 0.8
        
        ax.plot_surface(X, Y, Z, facecolors=grey_color, 
                       edgecolor='none', shade=True)
        
        # Redraw centerline in black
        cx, cy, cz = mobius.centerline
        ax.plot(cx, cy, cz, 'k-', linewidth=1.0)
        
        # Redraw parallel lines in yellow (even thinner) - two lines
        px_pos, py_pos, pz_pos = mobius.parallel_line_pos
        px_neg, py_neg, pz_neg = mobius.parallel_line_neg
        ax.plot(px_pos, py_pos, pz_pos, 'y-', linewidth=0.25, alpha=0.7)
        ax.plot(px_neg, py_neg, pz_neg, 'y-', linewidth=0.25, alpha=0.7)
        
        # Redraw orthogonal line in blue (thinner)
        ox, oy, oz = mobius.orthogonal_line
        ax.plot(ox, oy, oz, 'b-', linewidth=0.5, alpha=0.7)
        
        # Redraw ladder rungs in yellow (even thinner)
        rungs_x, rungs_y, rungs_z = mobius.rungs
        for i in range(len(rungs_x)):
            ax.plot(rungs_x[i], rungs_y[i], rungs_z[i], 'y-', linewidth=0.35, alpha=0.8)
        
        # Remove all grid and background elements
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_zlabel('')
        ax.xaxis.line.set_visible(False)
        ax.yaxis.line.set_visible(False)
        ax.zaxis.line.set_visible(False)
        ax.xaxis.pane.set_visible(False)
        ax.yaxis.pane.set_visible(False)
        ax.zaxis.pane.set_visible(False)
        
        ax.set_box_aspect([1, 0.6, 0.5])
        
        # Set limits to show full model without truncation
        max_range = 6  # Adjusted for 75% model size
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range*0.6, max_range*0.6])
        ax.set_zlim([-max_range*0.5, max_range*0.5])
        
        fig.canvas.draw_idle()
    
    # Connect sliders
    slider_width.on_changed(update)
    slider_parallel.on_changed(update)
    slider_ortho.on_changed(update)
    slider_rotx.on_changed(update)
    slider_roty.on_changed(update)
    slider_rotz.on_changed(update)
    
    plt.show()

if __name__ == "__main__":
    create_interactive_plot()