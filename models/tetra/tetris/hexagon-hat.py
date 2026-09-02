import numpy as np
import math
import matplotlib.pyplot as plt

def create_hexagon_with_hat():
    """
    Create a hexagon with a triangular hat on top.
    """
    
    # Hexagon base (6 vertices)
    hex_radius = 1.0
    hex_angles = np.linspace(0, 2*np.pi, 7)[:-1]  # 6 vertices
    
    # Rotate so flat edge is at bottom
    #hex_angles += np.pi/6  # 30 degree rotation
    
    hex_x = hex_radius * np.cos(hex_angles)
    hex_y = hex_radius * np.sin(hex_angles)
    
    # Triangle hat on top edge (between vertices 1 and 2)
    # Top edge is between indices 1 and 2
    hat_base_x = [hex_x[1], hex_x[2]]
    hat_base_y = [hex_y[1], hex_y[2]]
    
    # Hat apex - above the midpoint of top edge
    hat_apex_x = np.mean(hat_base_x)
    hat_apex_y = np.mean(hat_base_y) + hex_radius * math.sqrt(3)/2
    
    # Combine coordinates
    # Order: hex vertices (starting from top-left, going clockwise)
    # Then hat apex
    
    coords = {
        'hexagon': list(zip(hex_x, hex_y)),
        'hat_apex': (hat_apex_x, hat_apex_y),
        'hat_base_indices': (1, 2)  # Which hex vertices form hat base
    }
    
    # Print coordinates
    print("Hexagon vertices (x, y):")
    for i, (x, y) in enumerate(coords['hexagon']):
        print(f"  H{i}: ({x:6.3f}, {y:6.3f})")
    
    print(f"\nHat apex: ({coords['hat_apex'][0]:6.3f}, {coords['hat_apex'][1]:6.3f})")
    print(f"Hat connects to hexagon vertices H{coords['hat_base_indices'][0]} and H{coords['hat_base_indices'][1]}")
    
    # Visualize
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Draw hexagon
    hex_x_plot = list(hex_x) + [hex_x[0]]  # Close the shape
    hex_y_plot = list(hex_y) + [hex_y[0]]
    ax.plot(hex_x_plot, hex_y_plot, 'b-', linewidth=2, label='Hexagon')
    
    # Draw hat
    hat_x = [hex_x[1], hat_apex_x, hex_x[2], hex_x[1]]
    hat_y = [hex_y[1], hat_apex_y, hex_y[2], hex_y[1]]
    ax.plot(hat_x, hat_y, 'r-', linewidth=2, label='Hat (T face)')
    
    # Mark vertices
    ax.plot(hex_x, hex_y, 'bo', markersize=8)
    ax.plot(hat_apex_x, hat_apex_y, 'ro', markersize=8)
    
    # Labels
    for i, (x, y) in enumerate(zip(hex_x, hex_y)):
        ax.text(x*1.1, y*1.1, f'H{i}', fontsize=10, ha='center')
    ax.text(hat_apex_x, hat_apex_y+0.1, 'T', fontsize=10, ha='center', color='red')
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('D2 Face: Hexagon with Triangle Hat')
    ax.legend()
    
    plt.show()
    
    return coords

# Run it
coords = create_hexagon_with_hat()

# For 3D D2 structure, we need 6 of these faces arranged around the elongated body
print("\n" + "="*50)
print("D2 has 6 of these hexagon+hat faces")
print("Plus 2 pure triangular faces at the ends")
print("Total: 6H + 8T faces (with 2H hidden in the bond)")
