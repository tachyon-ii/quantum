import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the CSV data
df = pd.read_csv('test_results/mobius_geometry_data.csv')

# Create 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the centerline path
ax.plot(df['position_x'], df['position_y'], df['position_z'], 'b-', linewidth=2)

# Plot wave vectors as arrows at selected points
for i in range(0, len(df), 10):  # Every 10th point
    ax.quiver(df.iloc[i]['position_x'], df.iloc[i]['position_y'], df.iloc[i]['position_z'],
              df.iloc[i]['wave_direction_x']*0.1, df.iloc[i]['wave_direction_y']*0.1, 
              df.iloc[i]['wave_direction_z']*0.1, color='red', alpha=0.7)

ax.set_xlabel('X')
ax.set_ylabel('Y') 
ax.set_zlabel('Z')
plt.title('Möbius Strip Centerline with Wave Vectors')
plt.show()