import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

def generate_wave_time_series(wave_type='standing'):
    """
    Generate a time series of wave interference patterns following λ = e^n/π
    
    Parameters:
    wave_type: 'standing' for standing waves, 'traveling' for traveling waves
    """
    
    # Parameters
    num_frames = 20
    x_range = np.linspace(-50, 50, 1000)  # Spatial range
    time_steps = np.linspace(0, np.pi, num_frames)  # Time evolution
    
    # Wave colors for each n (RGB tuples)
    colors = [
        '#ff0044',  # n=0 - red
        '#ff4400',  # n=1 - orange-red  
        '#ffaa00',  # n=2 - orange
        '#88ff00',  # n=3 - yellow-green
        '#0088ff',  # n=4 - blue
        '#4400ff',  # n=5 - purple
        '#ff00aa'   # n=6 - magenta
    ]
    
    def get_wavelength(n):
        """Calculate wavelength for given n"""
        return np.exp(n) / np.pi
    
    def get_amplitude(n):
        """Get normalized amplitude (decreasing with n for visibility)"""
        return 1.0 / (1.5 ** n)
    
    # Create output directories
    os.makedirs(f'wave_frames_{wave_type}', exist_ok=True)
    os.makedirs(f'wave_frames_individual_{wave_type}', exist_ok=True)
    
    # Generate frames in simple sequential order
    for frame_idx, t in enumerate(time_steps):
        # Generate composite version
        generate_frame(frame_idx, t, x_range, colors, wave_type, show_composite=True)
        
        # Generate individual waves version
        generate_frame(frame_idx, t, x_range, colors, wave_type, show_composite=False)
        
        print(f"Generated frame {frame_idx + 1}/{num_frames}")
    
    print(f"\nGenerated {num_frames} frames in 'wave_frames_{wave_type}/' and 'wave_frames_individual_{wave_type}/' directories")
    print(f"Composite version: convert -delay 20 wave_frames_{wave_type}/*.png wave_animation_{wave_type}.gif")
    print(f"Individual version: convert -delay 20 wave_frames_individual_{wave_type}/*.png wave_individual_{wave_type}.gif")
    
    # Create contact sheets for both versions
    create_contact_sheet(num_frames, f'wave_frames_{wave_type}', f'wave_contact_sheet_{wave_type}.png', f'Composite {wave_type.title()}')
    create_contact_sheet(num_frames, f'wave_frames_individual_{wave_type}', f'wave_contact_sheet_individual_{wave_type}.png', f'Individual {wave_type.title()}')

def generate_frame(frame_idx, t, x_range, colors, wave_type, show_composite=True):
    """Generate a single frame"""
    
    def get_wavelength(n):
        return np.exp(n) / np.pi
    
    def get_amplitude(n):
        return 1.0 / (1.5 ** n)
    
    fig = plt.figure(figsize=(12, 8))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[3, 1], width_ratios=[1, 1])
    
    # Main wave plot
    ax_main = fig.add_subplot(gs[0, :])
    
    # Set background color
    ax_main.set_facecolor('black')
    bg_color = 'black'
    main_color = 'white'
    
    # Individual wave data storage
    individual_waves = {}
    composite_wave = np.zeros_like(x_range)
    
    # Calculate and plot individual waves
    for n in range(7):  # n=0 to n=6
        wavelength = get_wavelength(n)
        amplitude = get_amplitude(n)
        frequency = 2 * np.pi / wavelength
        
        if wave_type == 'standing':
            # Standing wave: rightward + leftward components
            rightward = np.sin(frequency * x_range - t)
            leftward = np.sin(-frequency * x_range - t)
            wave = amplitude * (rightward + leftward)
        else:  # traveling waves
            # Traveling waves: separate rightward and leftward components
            speed = 1.0  # wave speed
            rightward = np.sin(frequency * (x_range - speed * t))
            leftward = np.sin(frequency * (-x_range - speed * t))
            wave = amplitude * (rightward + leftward)
        
        individual_waves[n] = wave
        composite_wave += wave
        
        if show_composite:
            # Plot individual wave (semi-transparent)
            ax_main.plot(x_range, wave, color=colors[n], alpha=0.4, 
                        linewidth=1.5, label=f'n={n}, λ={wavelength:.2f}')
        else:
            # Plot individual wave (full opacity)
            ax_main.plot(x_range, wave, color=colors[n], alpha=0.9, 
                        linewidth=2, label=f'n={n}, λ={wavelength:.2f}')
    
    if show_composite:
        # Plot composite wave (bold white)
        ax_main.plot(x_range, composite_wave, color='white', linewidth=3, 
                    label='Composite', zorder=10)
        title_suffix = "(Composite)"
    else:
        title_suffix = "(Individual Waves)"
    
    # Formatting main plot
    ax_main.set_xlim(-50, 50)
    ax_main.set_ylim(-3, 3)
    ax_main.set_xlabel('Position (x)', fontsize=12, color=main_color)
    ax_main.set_ylabel('Amplitude', fontsize=12, color=main_color)
    ax_main.set_title(f'{wave_type.title()} Waves: λ = e^n/π {title_suffix} (t = {t:.2f})', 
                     fontsize=14, fontweight='bold', color=main_color)
    ax_main.grid(True, alpha=0.3)
    ax_main.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    ax_main.axvline(x=0, color='gray', linestyle='-', alpha=0.5)
    ax_main.tick_params(colors=main_color)
    
    # Legend
    legend = ax_main.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    legend.get_frame().set_facecolor(bg_color)
    for text in legend.get_texts():
        text.set_color(main_color)
    
    # Wavelength data table
    ax_table = fig.add_subplot(gs[1, 0])
    ax_table.axis('off')
    
    table_data = []
    for n in range(7):
        wavelength = get_wavelength(n)
        amplitude = get_amplitude(n)
        table_data.append([f'n={n}', f'{wavelength:.3f}', f'{amplitude:.3f}'])
    
    table = ax_table.table(cellText=table_data,
                          colLabels=['n', 'λ = e^n/π', 'Amplitude'],
                          cellLoc='center',
                          loc='center',
                          colWidths=[0.2, 0.4, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    
    # Color code the table rows
    for i in range(7):
        table[(i+1, 0)].set_facecolor(colors[i])
        table[(i+1, 0)].set_text_props(weight='bold', color='white')
    
    # Energy spectrum plot
    ax_spectrum = fig.add_subplot(gs[1, 1])
    n_values = np.arange(7)
    wavelengths = [get_wavelength(n) for n in n_values]
    amplitudes = [get_amplitude(n) for n in n_values]
    
    bars = ax_spectrum.bar(n_values, amplitudes, color=colors, alpha=0.8)
    ax_spectrum.set_xlabel('n', fontsize=10, color=main_color)
    ax_spectrum.set_ylabel('Amplitude', fontsize=10, color=main_color)
    ax_spectrum.set_title('Wave Amplitudes', fontsize=11, color=main_color)
    ax_spectrum.set_xticks(n_values)
    ax_spectrum.grid(True, alpha=0.3)
    ax_spectrum.set_facecolor(bg_color)
    ax_spectrum.tick_params(colors=main_color)
    
    plt.tight_layout()
    
    # Save frame to appropriate directory
    if show_composite:
        filename = f'wave_frames_{wave_type}/frame_{frame_idx:03d}.png'
    else:
        filename = f'wave_frames_individual_{wave_type}/frame_{frame_idx:03d}.png'
    
    plt.savefig(filename, dpi=150, bbox_inches='tight', 
               facecolor=bg_color, edgecolor='none')
    plt.close()

def create_contact_sheet(num_frames, frames_dir, output_filename, version_name):
    """Create a contact sheet showing all frames as thumbnails"""
    
    # Calculate grid dimensions
    cols = 5
    rows = (num_frames + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 3*rows))
    fig.suptitle(f'Wave Evolution Time Series: λ = e^n/π ({version_name})', fontsize=16, fontweight='bold')
    
    if rows == 1:
        axes = axes.reshape(1, -1)
    
    # Standard left-to-right, top-to-bottom layout
    for i in range(num_frames):
        row = i // cols  # Which row (0, 1, 2, ...)
        col = i % cols   # Which column within that row (0, 1, 2, 3, 4)
        
        # Load and display the frame
        try:
            img = plt.imread(f'{frames_dir}/frame_{i:03d}.png')
            axes[row, col].imshow(img)
            axes[row, col].set_title(f'Frame {i+1}', fontsize=10)
            axes[row, col].axis('off')
        except FileNotFoundError:
            axes[row, col].text(0.5, 0.5, f'Frame {i+1}\nNot Found', 
                              ha='center', va='center', transform=axes[row, col].transAxes)
            axes[row, col].axis('off')
    
    # Hide unused subplot areas
    for i in range(num_frames, rows * cols):
        row = i // cols
        col = i % cols
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"Created contact sheet: {output_filename}")

if __name__ == "__main__":
    # Generate both standing and traveling wave versions
    print("Generating standing waves...")
    generate_wave_time_series(wave_type='standing')
    
    print("\nGenerating traveling waves...")
    generate_wave_time_series(wave_type='traveling')
