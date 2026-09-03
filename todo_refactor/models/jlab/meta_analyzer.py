#!/usr/bin/env python3
"""
Meta-analysis of EMC data - combines multiple nuclei to find common periodic structures
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate, signal

def load_data(filename):
    """Load EMC data"""
    if filename.endswith('.xlsx'):
        df = pd.read_excel(filename, sheet_name=0, header=0)
    else:
        df = pd.read_csv(filename, sep='\t')
    
    df.columns = df.columns.str.strip()
    for col in ['A', 'Z', 'x', 'Ratio', 'TotalError(abs)']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def normalize_nucleus(data, A):
    """Normalize one nucleus to its mean"""
    nucleus_data = data[data['A'] == A].copy()
    if len(nucleus_data) < 10:
        return None
    
    nucleus_data = nucleus_data.sort_values('x')
    mean_ratio = nucleus_data['Ratio'].mean()
    
    # Normalize to mean = 1
    nucleus_data['normalized_ratio'] = nucleus_data['Ratio'] / mean_ratio
    nucleus_data['normalized_error'] = nucleus_data['TotalError(abs)'] / mean_ratio if 'TotalError(abs)' in nucleus_data else 0.01
    
    return nucleus_data

def combine_nuclei(data, nuclei_list):
    """Combine multiple nuclei into meta-dataset"""
    combined_data = []
    
    for A in nuclei_list:
        norm_data = normalize_nucleus(data, A)
        if norm_data is not None:
            combined_data.append(norm_data)
    
    if not combined_data:
        return None
    
    # Combine all normalized data
    meta_data = pd.concat(combined_data, ignore_index=True)
    meta_data = meta_data.sort_values('x')
    
    return meta_data

def bin_analysis(meta_data, bin_width=0.0214):  # Use irrational number like pi/147
    """Bin the combined data for better structure visibility"""
    x_min, x_max = meta_data['x'].min(), meta_data['x'].max()
    bins = np.arange(x_min, x_max + bin_width, bin_width)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    
    binned_means = []
    binned_errors = []
    binned_counts = []
    
    for i in range(len(bins)-1):
        mask = (meta_data['x'] >= bins[i]) & (meta_data['x'] < bins[i+1])
        bin_data = meta_data[mask]
        
        if len(bin_data) > 0:
            # Weighted mean if errors available
            if 'normalized_error' in bin_data.columns:
                weights = 1.0 / (bin_data['normalized_error']**2 + 1e-10)
                mean = np.average(bin_data['normalized_ratio'], weights=weights)
                error = 1.0 / np.sqrt(np.sum(weights))
            else:
                mean = bin_data['normalized_ratio'].mean()
                error = bin_data['normalized_ratio'].std() / np.sqrt(len(bin_data))
            
            binned_means.append(mean)
            binned_errors.append(error)
            binned_counts.append(len(bin_data))
        else:
            binned_means.append(np.nan)
            binned_errors.append(np.nan)
            binned_counts.append(0)
    
    # Remove empty bins
    valid = ~np.isnan(binned_means)
    
    return {
        'x': bin_centers[valid],
        'mean': np.array(binned_means)[valid],
        'error': np.array(binned_errors)[valid],
        'count': np.array(binned_counts)[valid]
    }

def spectral_analysis_meta(binned):
    """Perform spectral analysis on binned meta-data"""
    x = binned['x']
    y = binned['mean']
    
    # Detrend
    poly = np.polyfit(x, y, 2)
    baseline = np.polyval(poly, x)
    detrended = y - baseline
    
    # Test periods from 0.05 to 0.3
    test_periods = np.linspace(0.05, 0.3, 500)
    powers = []
    
    for period in test_periods:
        # Test sine and cosine
        freq = 2 * np.pi / period
        sin_comp = np.sum(detrended * np.sin(freq * x))
        cos_comp = np.sum(detrended * np.cos(freq * x))
        power = np.sqrt(sin_comp**2 + cos_comp**2) / len(x)
        powers.append(power)
    
    powers = np.array(powers)
    
    return test_periods, powers

def plot_meta_analysis(meta_data, binned, periods, powers, bin_width=0.0214):
    """Create comprehensive meta-analysis plots"""
    fig = plt.figure(figsize=(15, 10))
    
    # Plot 1: All normalized data points
    ax1 = plt.subplot(2, 3, 1)
    for A in meta_data['A'].unique():
        nucleus_data = meta_data[meta_data['A'] == A]
        ax1.scatter(nucleus_data['x'], nucleus_data['normalized_ratio'], 
                   alpha=0.3, s=10, label=f'A={int(A)}')
    ax1.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax1.axvline(x=0.167, color='red', linestyle=':', alpha=0.5)
    ax1.axvline(x=0.333, color='red', linestyle=':', alpha=0.5)
    ax1.axvline(x=0.5, color='red', linestyle=':', alpha=0.5)
    ax1.axvline(x=0.667, color='red', linestyle=':', alpha=0.5)
    ax1.set_xlabel('Bjorken x')
    ax1.set_ylabel('Normalized EMC Ratio')
    ax1.set_title('All Data (Normalized)')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Binned data with error bars
    ax2 = plt.subplot(2, 3, 2)
    ax2.errorbar(binned['x'], binned['mean'], yerr=binned['error'], 
                fmt='o-', capsize=3, alpha=0.7)
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    for x_val in [0.167, 0.333, 0.5, 0.667, 0.833]:
        ax2.axvline(x=x_val, color='red', linestyle=':', alpha=0.5)
    ax2.set_xlabel('Bjorken x')
    ax2.set_ylabel('Binned Ratio')
    ax2.set_title(f'Binned Meta-Data ({len(binned["x"])} bins)')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Detrended binned data
    ax3 = plt.subplot(2, 3, 3)
    poly = np.polyfit(binned['x'], binned['mean'], 2)
    baseline = np.polyval(poly, binned['x'])
    detrended = binned['mean'] - baseline
    ax3.plot(binned['x'], detrended, 'b.-', alpha=0.7)
    ax3.axhline(y=0, color='gray', linestyle='--')
    for x_val in [0.167, 0.333, 0.5, 0.667, 0.833]:
        ax3.axvline(x=x_val, color='red', linestyle=':', alpha=0.5)
    ax3.set_xlabel('Bjorken x')
    ax3.set_ylabel('Detrended')
    ax3.set_title('Detrended Binned Data')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Spectral analysis
    ax4 = plt.subplot(2, 3, 4)
    ax4.plot(periods, powers / np.max(powers), 'k-', linewidth=2)
    ax4.axvline(x=0.167, color='red', linestyle='--', linewidth=2, label='1/6')
    ax4.axvline(x=0.333, color='blue', linestyle='--', alpha=0.5, label='1/3')
    ax4.fill_betweenx([0, 1], 0.15, 0.18, alpha=0.2, color='red')
    ax4.set_xlabel('Period in x')
    ax4.set_ylabel('Normalized Power')
    ax4.set_title('Meta-Analysis Spectrum')
    ax4.set_xlim([0.05, 0.35])
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Plot 5: Phase-folded at 1/6
    ax5 = plt.subplot(2, 3, 5)
    phase = (meta_data['x'] % 0.167) / 0.167  # Phase from 0 to 1
    ax5.scatter(phase, meta_data['normalized_ratio'], alpha=0.2, s=5)
    
    # Bin the phase-folded data with irrational bin width
    n_phase_bins = 31  # Prime number to avoid aliasing
    phase_bins = np.linspace(0, 1, n_phase_bins)
    phase_means = []
    phase_weights = []
    
    for i in range(len(phase_bins)-1):
        mask = (phase >= phase_bins[i]) & (phase < phase_bins[i+1])
        if np.sum(mask) > 0:
            phase_means.append(meta_data[mask]['normalized_ratio'].mean())
            phase_weights.append(np.sum(mask))  # Weight by number of points
        else:
            phase_means.append(np.nan)
            phase_weights.append(0)
    
    phase_centers = (phase_bins[:-1] + phase_bins[1:]) / 2
    valid = ~np.isnan(phase_means)
    phase_centers_valid = phase_centers[valid]
    phase_means_valid = np.array(phase_means)[valid]
    phase_weights_valid = np.array(phase_weights)[valid]
    
    # Apply smooth interpolation instead of connected lines
    from scipy.interpolate import UnivariateSpline
    
    # Use weights in the spline fitting
    if len(phase_centers_valid) > 3:  # Need at least 4 points for cubic spline
        # Create smooth spline with weighted fitting
        spline = UnivariateSpline(phase_centers_valid, phase_means_valid, 
                                 w=np.sqrt(phase_weights_valid), s=0.001)
        
        # Evaluate spline at many points for smooth curve
        phase_smooth = np.linspace(0, 1, 200)
        ratio_smooth = spline(phase_smooth)
        
        # Plot smooth curve
        ax5.plot(phase_smooth, ratio_smooth, 'r-', linewidth=2, label='Smooth fit')
        
        # Find peaks in the smooth curve
        from scipy.signal import find_peaks
        peaks, properties = find_peaks(ratio_smooth, prominence=0.005)
        
        # Mark the peaks
        if len(peaks) > 0:
            peak_phases = phase_smooth[peaks]
            peak_values = ratio_smooth[peaks]
            ax5.plot(peak_phases, peak_values, 'go', markersize=8, label='Peaks')
            
            # Calculate inter-peak distances
            if len(peak_phases) > 1:
                inter_peak_distances = np.diff(peak_phases)
                
                # Print peak information
                print("\n" + "="*50)
                print("PHASE-FOLDED PEAK ANALYSIS (Period = 0.167)")
                print("="*50)
                print(f"Number of peaks found: {len(peaks)}")
                print(f"Bin width used: {bin_width:.4f} (irrational)")
                print(f"Phase bins: {n_phase_bins} (prime number)")
                print("\nPeak positions (phase):")
                for i, p in enumerate(peak_phases):
                    print(f"  Peak {i+1}: phase = {p:.3f} (x equivalent = {p*0.167:.4f})")
                
                print("\nInter-peak distances:")
                for i, d in enumerate(inter_peak_distances):
                    print(f"  Peak {i+1} to {i+2}: {d:.3f} phase units ({d*0.167:.4f} in x)")
                
                print(f"\nMean inter-peak distance: {np.mean(inter_peak_distances):.3f} phase units")
                print(f"                         = {np.mean(inter_peak_distances)*0.167:.4f} in x units")
                print(f"Std dev of spacings: {np.std(inter_peak_distances):.3f} phase units")
                
                # Expected for hexagonal: 6 peaks per period would give spacing of 1/6 = 0.167
                expected_spacing = 1.0 / 6.0
                print(f"\nExpected for 6-fold symmetry: {expected_spacing:.3f} phase units")
                print(f"Observed/Expected ratio: {np.mean(inter_peak_distances)/expected_spacing:.2f}")
    else:
        # Fall back to simple line plot if not enough points
        ax5.plot(phase_centers_valid, phase_means_valid, 'r.-', linewidth=2)
    
    ax5.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax5.set_xlabel('Phase (period = 0.167)')
    ax5.set_ylabel('Normalized Ratio')
    ax5.set_title('Phase-folded at 1/6')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Summary statistics
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    
    # Find peak near 1/6
    mask_16 = np.abs(periods - 0.167) < 0.02
    if np.any(mask_16):
        power_16 = np.max(powers[mask_16])
        period_16 = periods[mask_16][np.argmax(powers[mask_16])]
    else:
        power_16 = 0
        period_16 = 0
    
    # Count data by nucleus
    nucleus_counts = meta_data.groupby('A').size()
    
    # Get values at key points safely
    val_16 = binned['mean'][np.argmin(np.abs(binned['x']-0.167))] if len(binned['x']) > 0 else 0
    val_13 = binned['mean'][np.argmin(np.abs(binned['x']-0.333))] if len(binned['x']) > 0 else 0
    val_12 = binned['mean'][np.argmin(np.abs(binned['x']-0.500))] if len(binned['x']) > 0 else 0
    val_23 = binned['mean'][np.argmin(np.abs(binned['x']-0.667))] if len(binned['x']) > 0 else 0
    
    summary = f"""Meta-Analysis Summary
{'='*30}

Total data points: {len(meta_data)}
Nuclei included: {len(nucleus_counts)}
x range: [{meta_data['x'].min():.3f}, {meta_data['x'].max():.3f}]

Binned data points: {len(binned['x'])}
Bin width: 0.02

Spectral Analysis:
Peak near 1/6: {period_16:.3f}
Power at peak: {power_16:.3f}

Structure at key points:
x = 1/6: {val_16:.3f}
x = 1/3: {val_13:.3f}
x = 1/2: {val_12:.3f}
x = 2/3: {val_23:.3f}
"""
    
    ax6.text(0.05, 0.95, summary, transform=ax6.transAxes,
            fontsize=10, verticalalignment='top', fontfamily='monospace')
    
    plt.suptitle('EMC Meta-Analysis - Combined Nuclei', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python meta_analyzer.py datafile.xlsx [A1 A2 ...]")
        print("If no A values specified, uses all available nuclei")
        sys.exit(1)
    
    filename = sys.argv[1]
    data = load_data(filename)
    
    # Select nuclei
    if len(sys.argv) > 2:
        nuclei = [int(a) for a in sys.argv[2:]]
    else:
        # Use all nuclei with sufficient data
        nuclei = []
        for A in data['A'].unique():
            if not pd.isna(A) and len(data[data['A'] == A]) >= 20:
                nuclei.append(int(A))
    
    print(f"Combining data from nuclei: {sorted(nuclei)}")
    
    # Combine all nuclei
    meta_data = combine_nuclei(data, nuclei)
    if meta_data is None:
        print("Error: No valid data to combine")
        sys.exit(1)
    
    print(f"Total combined data points: {len(meta_data)}")
    
    # Bin the data with irrational width to avoid aliasing
    bin_width = np.pi / 147  # Approximately 0.0214 - an irrational number
    binned = bin_analysis(meta_data, bin_width=bin_width)
    print(f"Binned into {len(binned['x'])} bins with width {bin_width:.4f}")
    
    # Spectral analysis
    periods, powers = spectral_analysis_meta(binned)
    
    # Find peak near 1/6
    mask = np.abs(periods - 0.167) < 0.02
    if np.any(mask):
        idx = np.argmax(powers[mask])
        peak_period = periods[mask][idx]
        peak_power = powers[mask][idx]
        print(f"\nPeak near 1/6: period = {peak_period:.3f}, relative power = {peak_power/np.max(powers):.3f}")
    
    # Create plots
    fig = plot_meta_analysis(meta_data, binned, periods, powers, bin_width)
    
    plt.show()

if __name__ == "__main__":
    main()
