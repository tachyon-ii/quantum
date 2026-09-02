import numpy as np
import matplotlib.pyplot as plt

# Physical constants in natural units (simplified)
e_squared = 1.44  # MeV*fm (fine structure constant in MeV*fm units)
m_p = 938.272  # Proton mass in MeV/c^2 (unused here but conceptually important)

# Simulation parameters
r_pp_range = np.linspace(0.5, 5.0, 200)  # fm between protons
r_pn = 1.0  # distance from proton to neutron (orthogonal placement, fm)
theta_range = np.linspace(0.01, np.pi / 2, 200)  # angular offset from direct repulsion line

results = []

for r_pp in r_pp_range:
    for theta in theta_range:
        # Electrostatic repulsion between protons
        F_rep = e_squared / r_pp**2

        # Distance from proton to neutron (assumed constant offset)
        d = np.sqrt((r_pp / 2)**2 + r_pn**2)
        F_attr = e_squared / d**2

        # Components of neutron's attractive force
        F_parallel = F_attr * np.cos(theta)
        F_perpendicular = F_attr * np.sin(theta)

        # Required centripetal force for orbital stability (approximation)
        r_orbit = r_pp / 2
        # We approximate orbital velocity v ~ sqrt(F/m), so Fc = mv^2/r = F
        F_c_required = F_perpendicular

        stable = F_parallel > F_rep and F_perpendicular > 0.1 * F_rep  # crude stability check

        if stable:
            results.append((r_pp, theta, F_rep, F_parallel, F_perpendicular))

# Convert to numpy array for plotting
results = np.array(results)

# Plotting the stability zone
plt.figure(figsize=(10, 6))
if len(results) > 0:
    plt.scatter(results[:, 0], results[:, 1] * 180 / np.pi, c=results[:, 4], cmap='viridis', s=10)
    plt.colorbar(label='F_perpendicular (MeV/fm)')
    plt.xlabel('Proton-Proton Distance r_pp (fm)')
    plt.ylabel('Theta (degrees)')
    plt.title('Stability Zone for Angular Redirection (Scroll Orbital Binding)')
else:
    plt.text(0.5, 0.5, 'No stable regions found under given parameters.', ha='center', va='center')
plt.grid(True)
plt.tight_layout()
plt.show()

