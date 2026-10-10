#!/usr/bin/env python3
"""
Nuclear Crystal Simulator - Computational Validation of the Crystal Particle Hypothesis

Implementation of James Freeman's theory that atomic nuclei form geometric crystals
based on angular redirection and wave interference principles.

Authors: Dr. James Freeman (Theory), Suman Pokhrel (Implementation)
Date: August 2025
"""

import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu
import moderngl
import pygame
import sys
import math
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum

# Physics constants
class PhysicsConstants:
    """Physical constants for nuclear simulation"""
    COULOMB_CONSTANT = 0.8  # MeV*fm (in natural units)
    NUCLEAR_RADIUS = 1.2     # fm per nucleon^(1/3)
    HBAR_C = 197.327         # MeV*fm
    PROTON_MASS = 938.272    # MeV/c^2
    NEUTRON_MASS = 939.565   # MeV/c^2
    ELECTRON_MASS = 0.511    # MeV/c^2
    
    # James's angular redirection parameters
    REDIRECTION_STRENGTH = 1.0  # Neutron's angular deflection factor
    STRONG_FORCE_RANGE = 1.5   # fm - effective range of strong interaction
    RESONANCE_FREQUENCY = math.e  # Base frequency for e^n/π progression

class NucleonType(Enum):
    """Types of nucleons"""
    PROTON = "proton"
    NEUTRON = "neutron"

@dataclass
class Nucleon:
    """Represents a single nucleon (proton or neutron)"""
    type: NucleonType
    position: np.ndarray  # 3D position in fm
    velocity: np.ndarray  # 3D velocity
    charge: float         # Electric charge
    mass: float          # Mass in MeV/c^2
    id: int              # Unique identifier
    
    def __post_init__(self):
        if self.position is None:
            self.position = np.zeros(3)
        if self.velocity is None:
            self.velocity = np.zeros(3)

class NuclearForceModel:
    """
    Implementation of James Freeman's Angular Redirection Model
    
    The core principle: neutrons don't just add attraction - they redirect
    electrostatic repulsion into stable orbital motion through geometric
    interference patterns.
    """
    
    def __init__(self):
        self.constants = PhysicsConstants()
        
    def coulomb_force(self, nucleon1: Nucleon, nucleon2: Nucleon) -> np.ndarray:
        """Calculate Coulomb repulsion between charged nucleons"""
        r_vec = nucleon2.position - nucleon1.position
        r_mag = np.linalg.norm(r_vec)
        
        if r_mag < 1e-10:  # Avoid division by zero
            return np.zeros(3)
            
        # Coulomb force: F = k * q1 * q2 / r^2
        force_mag = (self.constants.COULOMB_CONSTANT * 
                    nucleon1.charge * nucleon2.charge / (r_mag**2))
        
        # Force direction (repulsive for like charges)
        force_direction = r_vec / r_mag
        
        return force_mag * force_direction
    
    def angular_redirection_force(self, proton: Nucleon, neutron: Nucleon, 
                                other_proton: Nucleon) -> np.ndarray:
        """
        James's key insight: neutrons redirect proton-proton repulsion
        into angular orbital motion rather than direct expulsion.
        """
        # Vector from neutron to proton
        r_np = proton.position - neutron.position
        r_np_mag = np.linalg.norm(r_np)
        
        # Vector from neutron to other proton
        r_np2 = other_proton.position - neutron.position
        r_np2_mag = np.linalg.norm(r_np2)
        
        if r_np_mag < 1e-10 or r_np2_mag < 1e-10:
            return np.zeros(3)
            
        # Calculate angle between the two protons as seen from neutron
        cos_angle = np.dot(r_np, r_np2) / (r_np_mag * r_np2_mag)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        
        # Angular redirection strength depends on geometry
        # Maximum redirection when protons are on opposite sides of neutron
        redirection_factor = (1.0 - cos_angle) / 2.0
        
        # Perpendicular component creates orbital motion
        # Cross product gives perpendicular direction
        perp_direction = np.cross(r_np, r_np2)
        perp_mag = np.linalg.norm(perp_direction)
        
        if perp_mag < 1e-10:
            return np.zeros(3)
            
        perp_direction = perp_direction / perp_mag
        
        # Force magnitude depends on neutron's "shielding" effect
        force_mag = (self.constants.REDIRECTION_STRENGTH * 
                    redirection_factor / (r_np_mag * r_np2_mag))
        
        return force_mag * perp_direction
    
    def strong_nuclear_force(self, nucleon1: Nucleon, nucleon2: Nucleon) -> np.ndarray:
        """
        Residual strong force - short range attractive force between all nucleons
        Modeled as exponentially decaying Yukawa potential
        """
        r_vec = nucleon2.position - nucleon1.position
        r_mag = np.linalg.norm(r_vec)
        
        if r_mag < 1e-10:
            return np.zeros(3)
            
        # Yukawa potential: V = -g * exp(-r/range) / r
        # Force is negative gradient of potential
        exp_factor = np.exp(-r_mag / self.constants.STRONG_FORCE_RANGE)
        
        # Attractive force (negative for attractive)
        force_mag = -(self.constants.COULOMB_CONSTANT * exp_factor / r_mag**2) * \
                   (1.0 + r_mag / self.constants.STRONG_FORCE_RANGE)
        
        force_direction = r_vec / r_mag
        
        return force_mag * force_direction

class NuclearSimulation:
    """
    Main physics simulation engine implementing James's Crystal Particle Hypothesis
    """
    
    def __init__(self, protons: int, neutrons: int):
        self.protons = protons
        self.neutrons = neutrons
        self.nucleons: List[Nucleon] = []
        self.force_model = NuclearForceModel()
        self.time_step = 0.001  # fm/c units
        self.total_time = 0.0
        self.binding_energy = 0.0
        
        # Initialize nucleons
        self._initialize_nucleons()
        
    def _initialize_nucleons(self):
        """Initialize nucleons in random positions around origin"""
        nucleon_id = 0
        
        # Create protons
        for i in range(self.protons):
            # Random position within nuclear radius
            pos = np.random.normal(0, 2.0, 3)  # fm
            vel = np.random.normal(0, 0.1, 3)  # initial small velocities
            
            nucleon = Nucleon(
                type=NucleonType.PROTON,
                position=pos,
                velocity=vel,
                charge=1.0,
                mass=PhysicsConstants.PROTON_MASS,
                id=nucleon_id
            )
            self.nucleons.append(nucleon)
            nucleon_id += 1
            
        # Create neutrons
        for i in range(self.neutrons):
            pos = np.random.normal(0, 2.0, 3)  # fm
            vel = np.random.normal(0, 0.1, 3)
            
            nucleon = Nucleon(
                type=NucleonType.NEUTRON,
                position=pos,
                velocity=vel,
                charge=0.0,
                mass=PhysicsConstants.NEUTRON_MASS,
                id=nucleon_id
            )
            self.nucleons.append(nucleon)
            nucleon_id += 1
    
    def calculate_forces(self) -> Dict[int, np.ndarray]:
        """Calculate all forces acting on each nucleon"""
        forces = {nucleon.id: np.zeros(3) for nucleon in self.nucleons}
        
        # Calculate pairwise forces
        for i, nucleon1 in enumerate(self.nucleons):
            for j, nucleon2 in enumerate(self.nucleons):
                if i >= j:  # Avoid double counting and self-interaction
                    continue
                    
                # Coulomb force (electrostatic)
                if nucleon1.charge != 0 and nucleon2.charge != 0:
                    coulomb_f = self.force_model.coulomb_force(nucleon1, nucleon2)
                    forces[nucleon1.id] += coulomb_f
                    forces[nucleon2.id] -= coulomb_f  # Newton's 3rd law
                
                # Strong nuclear force (attractive, short range)
                strong_f = self.force_model.strong_nuclear_force(nucleon1, nucleon2)
                forces[nucleon1.id] += strong_f
                forces[nucleon2.id] -= strong_f
        
        # Angular redirection forces (James's key innovation)
        protons = [n for n in self.nucleons if n.type == NucleonType.PROTON]
        neutrons = [n for n in self.nucleons if n.type == NucleonType.NEUTRON]
        
        for neutron in neutrons:
            for i, proton1 in enumerate(protons):
                for j, proton2 in enumerate(protons):
                    if i >= j:
                        continue
                        
                    # Calculate angular redirection for each proton
                    redirect_f1 = self.force_model.angular_redirection_force(
                        proton1, neutron, proton2)
                    redirect_f2 = self.force_model.angular_redirection_force(
                        proton2, neutron, proton1)
                    
                    forces[proton1.id] += redirect_f1
                    forces[proton2.id] += redirect_f2
                    # Neutron experiences reaction force
                    forces[neutron.id] -= (redirect_f1 + redirect_f2)
        
        return forces
    
    def calculate_total_energy(self) -> float:
        """Calculate total energy of the nuclear system"""
        kinetic_energy = 0.0
        potential_energy = 0.0
        
        # Kinetic energy
        for nucleon in self.nucleons:
            v_squared = np.dot(nucleon.velocity, nucleon.velocity)
            kinetic_energy += 0.5 * nucleon.mass * v_squared
        
        # Potential energy (pairwise interactions)
        for i, nucleon1 in enumerate(self.nucleons):
            for j, nucleon2 in enumerate(self.nucleons):
                if i >= j:
                    continue
                    
                r = np.linalg.norm(nucleon2.position - nucleon1.position)
                if r < 1e-10:
                    continue
                
                # Coulomb potential
                if nucleon1.charge != 0 and nucleon2.charge != 0:
                    coulomb_pe = (PhysicsConstants.COULOMB_CONSTANT * 
                                nucleon1.charge * nucleon2.charge / r)
                    potential_energy += coulomb_pe
                
                # Strong force potential (Yukawa)
                strong_pe = -(PhysicsConstants.COULOMB_CONSTANT * 
                            np.exp(-r / PhysicsConstants.STRONG_FORCE_RANGE) / r)
                potential_energy += strong_pe
        
        return kinetic_energy + potential_energy
    
    def update_physics(self):
        """Update nucleon positions and velocities using Verlet integration"""
        forces = self.calculate_forces()
        
        # Verlet integration for better numerical stability
        for nucleon in self.nucleons:
            force = forces[nucleon.id]
            acceleration = force / nucleon.mass
            
            # Update position: x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2
            nucleon.position += (nucleon.velocity * self.time_step + 
                               0.5 * acceleration * self.time_step**2)
            
            # Update velocity: v(t+dt) = v(t) + a(t)*dt
            nucleon.velocity += acceleration * self.time_step
        
        self.total_time += self.time_step
        
        # Apply damping to stabilize system
        damping_factor = 0.999
        for nucleon in self.nucleons:
            nucleon.velocity *= damping_factor
    
    def get_center_of_mass(self) -> np.ndarray:
        """Calculate center of mass of the nuclear system"""
        total_mass = sum(nucleon.mass for nucleon in self.nucleons)
        com = np.zeros(3)
        
        for nucleon in self.nucleons:
            com += nucleon.mass * nucleon.position
        
        return com / total_mass
    
    def recenter_system(self):
        """Move system so center of mass is at origin"""
        com = self.get_center_of_mass()
        for nucleon in self.nucleons:
            nucleon.position -= com
    
    def get_nuclear_radius(self) -> float:
        """Calculate RMS radius of the nuclear system"""
        self.recenter_system()
        
        total_mass = sum(nucleon.mass for nucleon in self.nucleons)
        rms_radius_sq = 0.0
        
        for nucleon in self.nucleons:
            r_sq = np.dot(nucleon.position, nucleon.position)
            rms_radius_sq += nucleon.mass * r_sq
        
        return math.sqrt(rms_radius_sq / total_mass)
    
    def analyze_geometry(self) -> Dict:
        """Analyze the geometric structure of the nucleus"""
        protons = [n for n in self.nucleons if n.type == NucleonType.PROTON]
        neutrons = [n for n in self.nucleons if n.type == NucleonType.NEUTRON]
        
        analysis = {
            'nuclear_radius': self.get_nuclear_radius(),
            'total_energy': self.calculate_total_energy(),
            'proton_count': len(protons),
            'neutron_count': len(neutrons),
            'center_of_mass': self.get_center_of_mass(),
        }
        
        # Check for tetrahedral geometry (Helium-4 case)
        if len(protons) == 2 and len(neutrons) == 2:
            analysis['geometry_type'] = 'tetrahedral_candidate'
            analysis['tetrahedral_score'] = self._calculate_tetrahedral_score()
        
        return analysis
    
    def _calculate_tetrahedral_score(self) -> float:
        """Calculate how close the current configuration is to a perfect tetrahedron"""
        if len(self.nucleons) != 4:
            return 0.0
        
        positions = [nucleon.position for nucleon in self.nucleons]
        
        # Calculate all pairwise distances
        distances = []
        for i in range(4):
            for j in range(i+1, 4):
                dist = np.linalg.norm(positions[j] - positions[i])
                distances.append(dist)
        
        # Perfect tetrahedron has 6 equal edge lengths
        mean_dist = np.mean(distances)
        variance = np.var(distances)
        
        # Score is inversely related to variance (1.0 = perfect tetrahedron)
        if mean_dist > 0:
            tetrahedral_score = 1.0 / (1.0 + variance / mean_dist**2)
        else:
            tetrahedral_score = 0.0
        
        return tetrahedral_score

class OpenGLVisualizer:
    """
    3D OpenGL visualization of the nuclear simulation
    """
    
    def __init__(self, simulation: NuclearSimulation):
        self.simulation = simulation
        self.window_width = 1200
        self.window_height = 800
        self.rotation_x = 0.0
        self.rotation_y = 0.0
        self.zoom = -20.0
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_pressed = False
        
        # Initialize Pygame and OpenGL
        pygame.init()
        pygame.display.set_mode((self.window_width, self.window_height), 
                              pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption("Nuclear Crystal Simulator - James Freeman's Theory")
        
        self._init_opengl()
        
        # Simulation control
        self.running = True
        self.paused = False
        self.auto_rotate = True
        
    def _init_opengl(self):
        """Initialize OpenGL settings"""
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Set up lighting
        light_pos = [10.0, 10.0, 10.0, 1.0]
        light_ambient = [0.3, 0.3, 0.3, 1.0]
        light_diffuse = [0.8, 0.8, 0.8, 1.0]
        
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, light_pos)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT, light_ambient)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, light_diffuse)
        
        # Set up perspective
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, self.window_width/self.window_height, 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
    def draw_nucleon(self, nucleon: Nucleon):
        """Draw a single nucleon as a colored sphere"""
        gl.glPushMatrix()
        
        # Translate to nucleon position (scale for visibility)
        scale_factor = 2.0  # Scale positions for better visibility
        gl.glTranslatef(nucleon.position[0] * scale_factor,
                       nucleon.position[1] * scale_factor,
                       nucleon.position[2] * scale_factor)
        
        # Color coding: protons = red, neutrons = blue
        if nucleon.type == NucleonType.PROTON:
            gl.glColor3f(1.0, 0.3, 0.3)  # Red for protons
        else:
            gl.glColor3f(0.3, 0.3, 1.0)  # Blue for neutrons
        
        # Draw sphere
        quadric = glu.gluNewQuadric()
        glu.gluSphere(quadric, 0.5, 20, 20)  # radius, slices, stacks
        glu.gluDeleteQuadric(quadric)
        
        gl.glPopMatrix()
        
    def draw_bonds(self):
        """Draw lines between nucleons to show interaction structure"""
        gl.glDisable(gl.GL_LIGHTING)
        gl.glColor3f(0.7, 0.7, 0.7)
        gl.glLineWidth(1.0)
        
        scale_factor = 2.0
        
        gl.glBegin(gl.GL_LINES)
        for i, nucleon1 in enumerate(self.simulation.nucleons):
            for j, nucleon2 in enumerate(self.simulation.nucleons):
                if i >= j:
                    continue
                    
                # Only draw bonds within nuclear range
                distance = np.linalg.norm(nucleon2.position - nucleon1.position)
                if distance < 4.0:  # fm
                    pos1 = nucleon1.position * scale_factor
                    pos2 = nucleon2.position * scale_factor
                    
                    gl.glVertex3f(pos1[0], pos1[1], pos1[2])
                    gl.glVertex3f(pos2[0], pos2[1], pos2[2])
        
        gl.glEnd()
        gl.glEnable(gl.GL_LIGHTING)
        
    def draw_coordinate_axes(self):
        """Draw coordinate axes for reference"""
        gl.glDisable(gl.GL_LIGHTING)
        gl.glLineWidth(3.0)
        
        gl.glBegin(gl.GL_LINES)
        
        # X axis - Red
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(5.0, 0.0, 0.0)
        
        # Y axis - Green
        gl.glColor3f(0.0, 1.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 5.0, 0.0)
        
        # Z axis - Blue
        gl.glColor3f(0.0, 0.0, 1.0)
        gl.glVertex3f(0.0, 0.0, 0.0)
        gl.glVertex3f(0.0, 0.0, 5.0)
        
        gl.glEnd()
        gl.glEnable(gl.GL_LIGHTING)
        
    def draw_info_overlay(self):
        """Draw simulation information as text overlay"""
        analysis = self.simulation.analyze_geometry()
        
        # Switch to 2D rendering for text
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, self.window_width, 0, self.window_height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_LIGHTING)
        
        # Draw semi-transparent background
        gl.glColor4f(0.0, 0.0, 0.0, 0.7)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(10, self.window_height - 200)
        gl.glVertex2f(300, self.window_height - 200)
        gl.glVertex2f(300, self.window_height - 10)
        gl.glVertex2f(10, self.window_height - 10)
        gl.glEnd()
        
        # Note: For actual text rendering, you'd need to use a library like
        # pygame fonts or freetype. This is a placeholder for the text overlay.
        
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        
        # Restore 3D projection
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
    def render_frame(self):
        """Render a single frame"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        
        # Camera positioning
        gl.glTranslatef(0.0, 0.0, self.zoom)
        gl.glRotatef(self.rotation_x, 1.0, 0.0, 0.0)
        gl.glRotatef(self.rotation_y, 0.0, 1.0, 0.0)
        
        # Draw coordinate axes
        self.draw_coordinate_axes()
        
        # Draw nucleon bonds first (so they appear behind nucleons)
        self.draw_bonds()
        
        # Draw nucleons
        for nucleon in self.simulation.nucleons:
            self.draw_nucleon(nucleon)
        
        # Draw info overlay
        self.draw_info_overlay()
        
        # Auto-rotation
        if self.auto_rotate and not self.paused:
            self.rotation_y += 0.5
        
        pygame.display.flip()
        
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    # Reset simulation
                    self.simulation._initialize_nucleons()
                elif event.key == pygame.K_a:
                    self.auto_rotate = not self.auto_rotate
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.mouse_pressed = True
                    self.mouse_x, self.mouse_y = event.pos
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    dx = event.pos[0] - self.mouse_x
                    dy = event.pos[1] - self.mouse_y
                    
                    self.rotation_y += dx * 0.5
                    self.rotation_x += dy * 0.5
                    
                    self.mouse_x, self.mouse_y = event.pos
                    
            elif event.type == pygame.MOUSEWHEEL:
                self.zoom += event.y * 2.0
                self.zoom = max(-50.0, min(-5.0, self.zoom))
    
    def run(self):
        """Main visualization loop"""
        clock = pygame.time.Clock()
        
        print("Nuclear Crystal Simulator Started")
        print("Controls:")
        print("  SPACE - Pause/Resume simulation")
        print("  R - Reset simulation")
        print("  A - Toggle auto-rotation")
        print("  Mouse - Rotate view")
        print("  Mouse wheel - Zoom")
        print("  ESC - Exit")
        
        while self.running:
            self.handle_events()
            
            if not self.paused:
                # Update physics
                self.simulation.update_physics()
                
                # Recenter system periodically
                if int(self.simulation.total_time * 1000) % 100 == 0:
                    self.simulation.recenter_system()
            
            # Render frame
            self.render_frame()
            
            # Control frame rate
            clock.tick(60)  # 60 FPS
        
        pygame.quit()

def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python nuclear_simulator.py <protons> <neutrons>")
        print("Examples:")
        print("  python nuclear_simulator.py 2 2  # Helium-4")
        print("  python nuclear_simulator.py 3 4  # Lithium-7")
        print("  python nuclear_simulator.py 4 3  # Beryllium-7")
        sys.exit(1)
    
    try:
        protons = int(sys.argv[1])
        neutrons = int(sys.argv[2])
        
        if protons < 1 or neutrons < 0:
            raise ValueError("Invalid nucleon counts")
            
        print(f"Initializing nuclear simulation: {protons} protons, {neutrons} neutrons")
        print("Testing James Freeman's Crystal Particle Hypothesis...")
        
        # Create simulation
        simulation = NuclearSimulation(protons, neutrons)
        
        # Create visualizer and run
        visualizer = OpenGLVisualizer(simulation)
        visualizer.run()
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Simulation error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()