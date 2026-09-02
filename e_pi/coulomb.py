import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

class Figure8ChargeSystem:
    def __init__(self, separation=0.0):
        """
        Two touching circles with electron in figure-8 (interlocked gear motion) and protons tracking.
        """
        self.k = 1.0  # Coulomb's constant (normalized)
        self.radius = 1.0
        
        # Circle centers - touching circles plus additional separation
        center_distance = 2.0 * self.radius + separation
        self.center_left = np.array([-center_distance/2, 0])
        self.center_right = np.array([center_distance/2, 0])
        self.separation = separation
        
        # Dynamic electron path radius - expands so electron path circles touch
        # When separation = 0: electron_radius = 1.0 (same as circles)
        # When separation > 0: electron_radius expands so electron path circles touch
        self.electron_radius = self.radius + separation/2
        
        # Starting positions: ALL at touching point
        self.theta_left = 0.0      # 3 o'clock on left circle (touch point)
        self.theta_right = np.pi   # 9 o'clock on right circle (touch point)
        
        # Velocities for physics-based motion
        self.omega_left = 0.0   # Angular velocity of left proton
        self.omega_right = 0.0  # Angular velocity of right proton
        
        # Electron orbit parameters
        self.orbit_time = 0.0
        self.orbit_speed = 1.2
        
        # Charge mass (same for both electron and proton in this simulation)
        self.charge_mass = 1.0
        
        # For analysis
        self.force_history = []
        self.net_force_history = []
        
    def get_proton_positions(self):
        """Get current positions of protons on their circle circumferences."""
        pos_left = self.center_left + self.radius * np.array([np.cos(self.theta_left), np.sin(self.theta_left)])
        pos_right = self.center_right + self.radius * np.array([np.cos(self.theta_right), np.sin(self.theta_right)])
        return pos_left, pos_right
    
    def get_electron_position(self, t):
        """
        Electron follows figure-8 like interlocked gears:
        Left circle: CLOCKWISE (down → left → up → right → down)
        Right circle: COUNTERCLOCKWISE (down → right → up → left → down)
        """
        # Complete cycle is 4π (2π for each circle)
        phase = (t * self.orbit_speed) % (4 * np.pi)
        
        if phase < 2 * np.pi:
            # Left circle: CLOCKWISE from touch point (0°)
            angle = -phase  # Negative for clockwise rotation
            center = self.center_left
            orbiting_left = True
        else:
            # Right circle: COUNTERCLOCKWISE from touch point (π on right circle)
            angle = (phase - 2 * np.pi) + np.pi  # Continue counterclockwise from π
            center = self.center_right
            orbiting_left = False
            
        # Position exactly on electron path circumference (expanded radius)
        x = center[0] + self.electron_radius * np.cos(angle)
        y = center[1] + self.electron_radius * np.sin(angle)
        
        return np.array([x, y]), phase, orbiting_left, angle
    
    def coulomb_force(self, q1, pos1, q2, pos2):
        """Calculate Coulomb force on q1 due to q2."""
        r_vec = pos1 - pos2  # Vector FROM q2 TO q1
        r_mag = np.linalg.norm(r_vec)
        if r_mag < 1e-10:
            return np.array([0.0, 0.0])
        
        r_hat = r_vec / r_mag
        force_mag = self.k * abs(q1 * q2) / (r_mag**2)
        
        # Force direction based on charge signs
        if q1 * q2 < 0:  # Opposite charges - ATTRACTIVE
            force = -force_mag * r_hat  # Force points TOWARD q2 (opposite of r_vec)
        else:  # Same charges - REPULSIVE
            force = force_mag * r_hat   # Force points AWAY from q2 (same as r_vec)
            
        return force
    
    def update_proton_positions(self, dt=0.01):
        """
        Update proton positions with perfect tracking for orbited circle.
        Non-orbited proton moves based on attraction.
        """
        electron_pos, phase, orbiting_left, electron_angle = self.get_electron_position(self.orbit_time)
        pos_left, pos_right = self.get_proton_positions()
        
        # Calculate forces
        force_left_from_electron = self.coulomb_force(1, pos_left, -1, electron_pos)
        force_right_from_electron = self.coulomb_force(1, pos_right, -1, electron_pos)
        force_left_from_right = self.coulomb_force(1, pos_left, 1, pos_right)
        force_right_from_left = self.coulomb_force(1, pos_right, 1, pos_left)
        
        # Total forces
        total_force_left = force_left_from_electron + force_left_from_right
        total_force_right = force_right_from_electron + force_right_from_left
        
        # Angular acceleration function
        def get_angular_acceleration(force, center, current_theta):
            tangent_dir = np.array([-np.sin(current_theta), np.cos(current_theta)])
            tangential_force = np.dot(force, tangent_dir)
            return tangential_force / self.radius
        
        if orbiting_left:
            # LEFT CIRCLE: Perfect tracking - same angle as electron
            self.theta_left = electron_angle
            self.omega_left = -self.orbit_speed
            
            # RIGHT CIRCLE: F = ma physics
            # 1. Force (attraction to electron)
            force = force_right_from_electron
            # 2. Acceleration = F/m
            acceleration = force / self.charge_mass
            # 3. Only tangential component moves proton around circle
            tangent_dir = np.array([-np.sin(self.theta_right), np.cos(self.theta_right)])
            tangential_accel = np.dot(acceleration, tangent_dir)
            # 4. Angular acceleration = tangential_accel / radius
            angular_accel = tangential_accel / self.radius
            # 5. Integrate: angular velocity, then position
            self.omega_right += angular_accel * dt
            self.omega_right *= 0.98  # Light damping
            self.theta_right += self.omega_right * dt
            
        else:
            # RIGHT CIRCLE: Perfect tracking - same angle as electron  
            self.theta_right = electron_angle  
            self.omega_right = self.orbit_speed
            
            # LEFT CIRCLE: F = ma physics
            # 1. Force (attraction to electron)
            force = force_left_from_electron
            # 2. Acceleration = F/m
            acceleration = force / self.charge_mass
            # 3. Only tangential component moves proton around circle
            tangent_dir = np.array([-np.sin(self.theta_left), np.cos(self.theta_left)])
            tangential_accel = np.dot(acceleration, tangent_dir)
            # 4. Angular acceleration = tangential_accel / radius
            angular_accel = tangential_accel / self.radius
            # 5. Integrate: angular velocity, then position
            self.omega_left += angular_accel * dt
            self.omega_left *= 0.98  # Light damping
            self.theta_left += self.omega_left * dt
        
        # Normalize angles
        self.theta_left = self.theta_left % (2 * np.pi)
        self.theta_right = self.theta_right % (2 * np.pi)
        
        # Store data for analysis
        self.force_history.append({
            'electron_pos': electron_pos.copy(),
            'proton_left': pos_left.copy(),
            'proton_right': pos_right.copy(),
            'force_left_from_electron': force_left_from_electron.copy(),
            'force_right_from_electron': force_right_from_electron.copy(),
            'force_left_from_right': force_left_from_right.copy(),
            'force_right_from_left': force_right_from_left.copy(),
            'phase': phase,
            'orbiting_left': orbiting_left,
            'electron_angle': electron_angle,
            'theta_left': self.theta_left,
            'theta_right': self.theta_right,
            'omega_left': self.omega_left,
            'omega_right': self.omega_right
        })
        
        return total_force_left, total_force_right
    
    def calculate_net_force_between_centers(self):
        """Calculate net force between circle centers due to proton repulsion."""
        pos_left, pos_right = self.get_proton_positions()
        force_vector = self.coulomb_force(1, pos_left, 1, pos_right)
        
        center_separation_vec = self.center_right - self.center_left
        if np.linalg.norm(center_separation_vec) > 1e-10:
            center_hat = center_separation_vec / np.linalg.norm(center_separation_vec)
            net_force_magnitude = np.dot(force_vector, center_hat)
        else:
            net_force_magnitude = 0.0
            
        self.net_force_history.append(net_force_magnitude)
        return net_force_magnitude
    
    def simulate_step(self, dt=0.01):
        """Perform one simulation step."""
        self.update_proton_positions(dt)
        net_force = self.calculate_net_force_between_centers()
        self.orbit_time += dt
        return net_force

def create_interactive_simulation():
    """Create simulation with interlocked gear figure-8 motion."""
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
    
    # Main simulation plot
    ax_main = fig.add_subplot(gs[0:2, 0:2])
    ax_force = fig.add_subplot(gs[2, 0])
    ax_velocity = fig.add_subplot(gs[2, 1]) 
    ax_separation = fig.add_subplot(gs[0:2, 2])
    
    # Initialize system
    system = Figure8ChargeSystem(separation=0.0)
    
    # Draw circles (proton constraints)
    circle_left = plt.Circle(system.center_left, system.radius, fill=False, color='blue', linewidth=4, alpha=0.8)
    circle_right = plt.Circle(system.center_right, system.radius, fill=False, color='blue', linewidth=4, alpha=0.8)
    ax_main.add_patch(circle_left)
    ax_main.add_patch(circle_right)
    
    # Draw electron path circles (larger when separated)
    electron_circle_left = plt.Circle(system.center_left, system.electron_radius, fill=False, color='green', linewidth=2, alpha=0.6, linestyle='--')
    electron_circle_right = plt.Circle(system.center_right, system.electron_radius, fill=False, color='green', linewidth=2, alpha=0.6, linestyle='--')
    ax_main.add_patch(electron_circle_left)
    ax_main.add_patch(electron_circle_right)
    
    # Draw interlocked gear figure-8 path 
    t_path = np.linspace(0, 4*np.pi/system.orbit_speed, 400)
    path_x, path_y = [], []
    for t in t_path:
        pos, _, _, _ = system.get_electron_position(t)
        path_x.append(pos[0])
        path_y.append(pos[1])
    
    ax_main.plot(path_x, path_y, 'g-', alpha=0.7, linewidth=3)
    
    # Charge markers - RED PROTONS LARGER, BLUE ELECTRON SMALLER
    pos_left, pos_right = system.get_proton_positions()
    electron_pos, _, _, _ = system.get_electron_position(0)
    
    # LARGE RED PROTONS (so they show under smaller electron)
    proton_left, = ax_main.plot(pos_left[0], pos_left[1], 'ro', markersize=20, zorder=4)
    proton_right, = ax_main.plot(pos_right[0], pos_right[1], 'ro', markersize=20, zorder=4)
    
    # SMALL BLUE ELECTRON (half size to expose red underneath)
    electron, = ax_main.plot(electron_pos[0], electron_pos[1], 'bs', markersize=10, zorder=6)
    
    # Center markers and touch point
    ax_main.plot(system.center_left[0], system.center_left[1], 'b+', markersize=12, markeredgewidth=3)
    ax_main.plot(system.center_right[0], system.center_right[1], 'b+', markersize=12, markeredgewidth=3)
    touching_point = (system.center_left + system.center_right) / 2
    ax_main.plot(touching_point[0], touching_point[1], 'go', markersize=10, zorder=5)
    
    # Force vectors - FROM proton TO electron (correct directions)
    force_left_to_e, = ax_main.plot([], [], 'r-', linewidth=3, alpha=0.8)
    force_right_to_e, = ax_main.plot([], [], 'r-', linewidth=3, alpha=0.8)
    
    # Proton-proton repulsion
    force_proton_to_proton, = ax_main.plot([], [], 'orange', linewidth=3, alpha=0.8)
    
    # Electron trail
    trail_length = 30
    electron_trail_x = []
    electron_trail_y = []
    electron_trail, = ax_main.plot([], [], 'g-', alpha=0.9, linewidth=4)
    
    # Direction arrows to show clockwise/counterclockwise - REMOVED
    
    ax_main.set_xlim(-3.5, 3.5)
    ax_main.set_ylim(-2.5, 2.5)
    ax_main.set_aspect('equal')
    ax_main.grid(True, alpha=0.3)
    # ax_main.legend() - REMOVED
    ax_main.set_title('Dynamic Figure-8 with Linear Physics Integration', 
                     fontsize=14, fontweight='bold')
    
    # Fixed scale plots
    force_line, = ax_force.plot([], [], 'purple', linewidth=2, label='Net Center Force')
    attraction_left_line, = ax_force.plot([], [], 'red', linewidth=2, alpha=0.7, label='Left→Electron')
    attraction_right_line, = ax_force.plot([], [], 'blue', linewidth=2, alpha=0.7, label='Right→Electron')
    ax_force.set_xlim(0, 1000)
    ax_force.set_ylim(0, 5)
    ax_force.set_xlabel('Time Steps')
    ax_force.set_ylabel('Force Magnitude')
    ax_force.set_title('Forces (Fixed Scale)')
    ax_force.grid(True, alpha=0.3)
    ax_force.legend()
    
    # Fixed scale velocity plot
    vel_left_line, = ax_velocity.plot([], [], 'r-', linewidth=2, label='Left ω')
    vel_right_line, = ax_velocity.plot([], [], 'b-', linewidth=2, label='Right ω')
    ax_velocity.set_xlim(0, 1000)
    ax_velocity.set_ylim(-10, 10)
    ax_velocity.set_xlabel('Time Steps')
    ax_velocity.set_ylabel('Angular Velocity')
    ax_velocity.set_title('Angular Velocities (Fixed Scale)')
    ax_velocity.grid(True, alpha=0.3)
    ax_velocity.legend()
    ax_velocity.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    # Separation analysis
    sep_line, = ax_separation.plot([], [], 'go-', linewidth=2, markersize=6)
    ax_separation.set_xlabel('Circle Separation')
    ax_separation.set_ylabel('RMS Net Force')
    ax_separation.set_title('Force vs Separation')
    ax_separation.set_xlim(0, 0.5)
    ax_separation.set_ylim(0, 2)
    ax_separation.grid(True, alpha=0.3)
    
    # Slider for separation
    ax_slider = plt.axes([0.1, 0.02, 0.6, 0.03])
    slider = Slider(ax_slider, 'Extra Separation', 0.0, 0.5, valinit=0.0, valfmt='%.3f')
    
    # Animation data
    time_steps = []
    forces = []
    attraction_left_mags = []
    attraction_right_mags = []
    velocities_left = []
    velocities_right = []
    separation_data = {'separations': [], 'rms_forces': []}
    
    def update_simulation(frame):
        # Run simulation steps
        for _ in range(2):
            system.simulate_step()
        
        # Update positions
        pos_left, pos_right = system.get_proton_positions()
        electron_pos, phase, orbiting_left, electron_angle = system.get_electron_position(system.orbit_time)
        
        proton_left.set_data([pos_left[0]], [pos_left[1]])
        proton_right.set_data([pos_right[0]], [pos_right[1]])
        electron.set_data([electron_pos[0]], [electron_pos[1]])
        
        # Update force vectors - FROM proton TO electron
        if len(system.force_history) > 0:
            # Force lines FROM each proton TO electron
            force_left_to_e.set_data([pos_left[0], electron_pos[0]], [pos_left[1], electron_pos[1]])
            force_right_to_e.set_data([pos_right[0], electron_pos[0]], [pos_right[1], electron_pos[1]])
            
            # Proton-proton repulsion line
            force_proton_to_proton.set_data([pos_left[0], pos_right[0]], [pos_left[1], pos_right[1]])
        
        # Update electron trail
        electron_trail_x.append(electron_pos[0])
        electron_trail_y.append(electron_pos[1])
        if len(electron_trail_x) > trail_length:
            electron_trail_x.pop(0)
            electron_trail_y.pop(0)
        electron_trail.set_data(electron_trail_x, electron_trail_y)
        
        # Update plots with fixed scales
        if len(system.force_history) > 0:
            latest = system.force_history[-1]
            
            # Ensure we have valid data before adding to arrays
            if not np.isnan(system.net_force_history[-1]):
                time_steps.append(len(system.force_history))
                forces.append(abs(system.net_force_history[-1]))
                
                # Calculate force magnitudes safely
                left_attraction_mag = np.linalg.norm(latest['force_left_from_electron'])
                right_attraction_mag = np.linalg.norm(latest['force_right_from_electron'])
                
                if not (np.isnan(left_attraction_mag) or np.isnan(right_attraction_mag)):
                    attraction_left_mags.append(left_attraction_mag)
                    attraction_right_mags.append(right_attraction_mag)
                    
                    velocities_left.append(latest['omega_left'])
                    velocities_right.append(latest['omega_right'])
                    
                    # Keep last 1000 points
                    max_points = 1000
                    if len(forces) > max_points:
                        time_steps.pop(0)
                        forces.pop(0)
                        attraction_left_mags.pop(0)
                        attraction_right_mags.pop(0)
                        velocities_left.pop(0)
                        velocities_right.pop(0)
                    
                    # Update plots (no rescaling) - only if we have data
                    if len(time_steps) > 0 and len(forces) > 0:
                        force_line.set_data(time_steps, forces)
                        attraction_left_line.set_data(time_steps, attraction_left_mags)
                        attraction_right_line.set_data(time_steps, attraction_right_mags)
                        vel_left_line.set_data(time_steps, velocities_left)
                        vel_right_line.set_data(time_steps, velocities_right)
        
        return (proton_left, proton_right, electron, electron_trail, 
                force_left_to_e, force_right_to_e, force_proton_to_proton,
                force_line, attraction_left_line, attraction_right_line, 
                vel_left_line, vel_right_line)
    
    def update_separation(val):
        nonlocal system
        new_sep = slider.val
        
        # Store RMS force for current separation
        if len(system.net_force_history) > 100:
            rms_force = np.sqrt(np.mean(np.array(system.net_force_history[-100:])**2))
            separation_data['separations'].append(system.separation)
            separation_data['rms_forces'].append(rms_force)
            
            sep_line.set_data(separation_data['separations'], separation_data['rms_forces'])
        
        # Create new system with new separation
        old_system = system
        system = Figure8ChargeSystem(separation=new_sep)
        
        # Preserve current proton positions to avoid jumps
        system.theta_left = old_system.theta_left
        system.theta_right = old_system.theta_right
        system.omega_left = old_system.omega_left
        system.omega_right = old_system.omega_right
        system.orbit_time = old_system.orbit_time
        
        # Update circle positions and sizes
        circle_left.center = system.center_left  
        circle_right.center = system.center_right
        
        # Update electron path circles - THIS WAS MISSING
        electron_circle_left.center = system.center_left
        electron_circle_left.radius = system.electron_radius
        electron_circle_right.center = system.center_right
        electron_circle_right.radius = system.electron_radius
        
        # Redraw the electron path with new radius
        t_path = np.linspace(0, 4*np.pi/system.orbit_speed, 400)
        path_x, path_y = [], []
        for t in t_path:
            pos, _, _, _ = system.get_electron_position(t)
            path_x.append(pos[0])
            path_y.append(pos[1])
        
        # Update the path plot
        for line in ax_main.lines:
            if line.get_color() == 'g' and line.get_linewidth() == 3:
                line.set_data(path_x, path_y)
                break
        
        # Clear tracking data
        time_steps.clear()
        forces.clear()
        attraction_left_mags.clear()
        attraction_right_mags.clear()
        velocities_left.clear()
        velocities_right.clear()
        electron_trail_x.clear()
        electron_trail_y.clear()
    
    slider.on_changed(update_separation)
    
    # Animation
    ani = animation.FuncAnimation(fig, update_simulation, interval=25, blit=False, cache_frame_data=False)
    
    plt.tight_layout()
    plt.show()
    
    return system, ani

if __name__ == "__main__":
    print("DYNAMIC Figure-8 System")
    print("=" * 24)
    print("Electron Path Behavior:")
    print("✅ Separation = 0: Electron path radius = 1.0 (same as circles)")
    print("✅ Separation > 0: Electron path expands so path circles touch")
    print("✅ Formula: electron_radius = 1.0 + separation/2")
    print()
    print("Result:")
    print("✅ Creates separation between electron and tracking proton")
    print("✅ Non-orbited proton experiences varying force distances")
    print("✅ More realistic orbital mechanics")
    
    system, animation = create_interactive_simulation()
