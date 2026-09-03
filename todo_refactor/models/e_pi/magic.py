import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import gaussian_kde
import seaborn as sns

class RealNuclearDataAnalysis:
    def __init__(self, filename='binding-energy3.txt'):
        """Load real nuclear binding energy data from file"""
        print("Loading REAL experimental nuclear data...")
        print(f"Source: {filename}")
        print("=" * 60)
        
        self.df = self.load_nuclear_data(filename)
        self.process_data()
        
        print(f"Loaded {len(self.df)} isotopes")
        print(f"Elements covered: Z={self.df['protons'].min()} to Z={self.df['protons'].max()}")
        print(f"Mass range: A={self.df['mass_number'].min()} to A={self.df['mass_number'].max()}")
        print(f"Experimental data points: {len(self.df[~self.df['is_estimate']])}")
        print(f"Estimated data points: {len(self.df[self.df['is_estimate']])}")
        print("=" * 60)
    
    def load_nuclear_data(self, filename):
        """Load the TSV nuclear data file"""
        try:
            # Read the TSV file
            df = pd.read_csv(filename, sep='\t', comment='#')
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Rename columns for consistency
            df = df.rename(columns={
                'Z': 'protons',
                'A': 'mass_number', 
                'EL': 'element',
                'Binding Energy': 'binding_energy_total'
            })
            
            return df
            
        except FileNotFoundError:
            print(f"ERROR: File {filename} not found!")
            print("Creating sample data structure for demonstration...")
            
            # Sample data structure based on the format you provided
            sample_data = [
                [1, 1, 'H', 0],
                [1, 2, 'H', 1112.2831],
                [1, 3, 'H', 2827.2654],
                [2, 3, 'He', 2572.68044],
                [3, 3, 'Li', -2267], # Marked as estimate
                [1, 4, 'H', 1720.4491],
                [2, 4, 'He', 7073.9156],
                [3, 4, 'Li', 1153.7603],
                [1, 5, 'H', 1336.3592],
                [2, 5, 'He', 5512.1325],
                [3, 5, 'Li', 5266.1325],
                [4, 5, 'Be', 18], # Marked as estimate
                [1, 6, 'H', 961.6395],
                [2, 6, 'He', 4878.5199],
                [3, 6, 'Li', 5332.3312],
                [4, 6, 'Be', 4487.2478],
                [5, 6, 'B', -467], # Marked as estimate
                [1, 7, 'H', 940], # Marked as estimate
                [2, 7, 'He', 4123.0578],
            ]
            
            df = pd.DataFrame(sample_data, columns=[
                'protons', 'mass_number', 'element', 'binding_energy_total'
            ])
            
            return df
    
    def process_data(self):
        """Process and calculate derived quantities"""
        # Check for estimates (negative values or very small positive values that seem unrealistic)
        self.df['is_estimate'] = (
            (self.df['binding_energy_total'] < 0) |  # Negative binding energies are clearly estimates
            ((self.df['binding_energy_total'] > 0) & (self.df['binding_energy_total'] < 100) & 
             (self.df['mass_number'] > 4))  # Very low values for heavy nuclei are suspicious
        )
        
        # Calculate derived quantities
        self.df['neutrons'] = self.df['mass_number'] - self.df['protons']
        self.df['binding_energy_per_nucleon'] = self.df['binding_energy_total'] / self.df['mass_number']
        self.df['N_to_P_ratio'] = self.df['neutrons'] / self.df['protons']
        
        # Replace infinite N/P ratios (when protons = 0) with NaN
        self.df['N_to_P_ratio'] = self.df['N_to_P_ratio'].replace([np.inf, -np.inf], np.nan)
        
        # Filter out estimates for main analysis (but keep them for comparison)
        self.df_real = self.df[~self.df['is_estimate']].copy()
        
        print(f"After filtering estimates: {len(self.df_real)} real data points")
    
    def plot_binding_energy_patterns(self):
        """Plot binding energy patterns to reveal magic numbers - 4 sequential plots"""
        real_data = self.df_real
        estimates = self.df[self.df['is_estimate']]
        
        # Plot 1: Binding Energy per Nucleon vs Atomic Number
        plt.figure(figsize=(14, 8))
        plt.scatter(real_data['protons'], real_data['binding_energy_per_nucleon'], 
                   c='red', s=30, alpha=0.8, label='Experimental data', edgecolors='none')
        if len(estimates) > 0:
            plt.scatter(estimates['protons'], estimates['binding_energy_per_nucleon'], 
                       c='gray', s=20, alpha=0.5, label='Estimates (ignored)', 
                       edgecolors='black', linewidth=0.5, marker='x')
        
        # Mark traditional magic proton numbers
        magic_protons = [2, 8, 20, 28, 50, 82]
        for mp in magic_protons:
            if mp <= real_data['protons'].max():
                plt.axvline(mp, color='green', linestyle='--', alpha=0.6, linewidth=2)
                plt.text(mp, plt.ylim()[1]*0.95, f'Z={mp}', 
                        color='green', ha='center', fontweight='bold', fontsize=10)
        
        plt.xlabel('Atomic Number (Protons)', fontsize=12)
        plt.ylabel('Binding Energy per Nucleon (MeV)', fontsize=12)
        plt.title('Nuclear Stability vs Atomic Number (Real Data)', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Plot 2: Binding Energy per Nucleon vs Mass Number
        plt.figure(figsize=(14, 8))
        plt.scatter(real_data['mass_number'], real_data['binding_energy_per_nucleon'], 
                   c='blue', s=30, alpha=0.8, label='Experimental data', edgecolors='none')
        if len(estimates) > 0:
            plt.scatter(estimates['mass_number'], estimates['binding_energy_per_nucleon'], 
                       c='gray', s=20, alpha=0.5, label='Estimates (ignored)', 
                       edgecolors='black', linewidth=0.5, marker='x')
        
        # Mark our predicted magic total nucleon numbers
        magic_total = [2, 4, 8, 16, 20, 28, 50, 82, 126]
        for mt in magic_total:
            if mt <= real_data['mass_number'].max():
                plt.axvline(mt, color='purple', linestyle='--', alpha=0.6, linewidth=2)
                plt.text(mt, plt.ylim()[1]*0.95, f'A={mt}', 
                        color='purple', ha='center', fontweight='bold', fontsize=10)
        
        plt.xlabel('Mass Number (Total Nucleons)', fontsize=12)
        plt.ylabel('Binding Energy per Nucleon (MeV)', fontsize=12)
        plt.title('Nuclear Stability vs Total Nucleons (Our Geometric Hypothesis)', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Plot 3: Total Binding Energy vs Mass Number
        plt.figure(figsize=(14, 8))
        plt.scatter(real_data['mass_number'], real_data['binding_energy_total'], 
                   c='darkgreen', s=30, alpha=0.8, edgecolors='none', label='Experimental data')
        
        # Mark our magic numbers
        magic_total = [2, 4, 8, 16, 20, 28, 50, 82, 126]
        for mt in magic_total:
            if mt <= real_data['mass_number'].max():
                plt.axvline(mt, color='orange', linestyle='--', alpha=0.6, linewidth=2)
                plt.text(mt, plt.ylim()[1]*0.95, f'A={mt}', 
                        color='orange', ha='center', fontweight='bold', fontsize=10)
        
        plt.xlabel('Mass Number (A)', fontsize=12)
        plt.ylabel('Total Binding Energy (keV)', fontsize=12)
        plt.title('Total Binding Energy vs Mass Number', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Plot 4: Neutron-Proton Chart
        plt.figure(figsize=(12, 10))
        scatter = plt.scatter(real_data['protons'], real_data['neutrons'], 
                             c=real_data['binding_energy_per_nucleon'], 
                             s=40, cmap='viridis', alpha=0.8)
        
        # Add N=Z line
        max_z = real_data['protons'].max()
        plt.plot([0, max_z], [0, max_z], 'r--', alpha=0.7, linewidth=2, label='N=Z line')
        
        # Mark magic numbers
        magic_numbers = [2, 8, 20, 28, 50, 82]
        for mn in magic_numbers:
            if mn <= max_z:
                plt.axhline(mn, color='red', linestyle=':', alpha=0.5, linewidth=1.5)
                plt.axvline(mn, color='red', linestyle=':', alpha=0.5, linewidth=1.5)
                plt.text(-1, mn, f'N={mn}', color='red', fontweight='bold', fontsize=9)
                plt.text(mn, -2, f'Z={mn}', color='red', fontweight='bold', fontsize=9, rotation=90)
        
        plt.xlabel('Protons (Z)', fontsize=12)
        plt.ylabel('Neutrons (N)', fontsize=12)
        plt.title('Nuclear Chart: Neutrons vs Protons (Colored by Binding Energy)', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        
        cbar = plt.colorbar(scatter, label='Binding Energy/Nucleon (MeV)')
        cbar.set_label('Binding Energy/Nucleon (MeV)', fontsize=11)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def analyze_magic_numbers(self):
        """Detailed analysis of magic number predictions"""
        print("\n" + "="*70)
        print("MAGIC NUMBER ANALYSIS - REAL EXPERIMENTAL DATA")
        print("="*70)
        
        predicted_magic = [2, 4, 8, 16, 20, 28, 50, 82, 126]
        real_data = self.df_real
        
        print("\nOur Geometric Predictions vs Reality:")
        print("-" * 50)
        
        magic_results = []
        
        for mn in predicted_magic:
            # Find isotopes at this mass number
            isotopes_at_mass = real_data[real_data['mass_number'] == mn]
            
            if not isotopes_at_mass.empty:
                max_binding = isotopes_at_mass['binding_energy_per_nucleon'].max()
                avg_binding = isotopes_at_mass['binding_energy_per_nucleon'].mean()
                count = len(isotopes_at_mass)
                
                magic_results.append({
                    'mass': mn,
                    'count': count,
                    'max_binding': max_binding,
                    'avg_binding': avg_binding,
                    'isotopes': isotopes_at_mass
                })
                
                print(f"\nMass Number A={mn}:")
                print(f"  Isotopes found: {count}")
                print(f"  Max binding energy/nucleon: {max_binding:.3f} MeV")
                print(f"  Avg binding energy/nucleon: {avg_binding:.3f} MeV")
                
                print("  Specific isotopes:")
                for _, isotope in isotopes_at_mass.iterrows():
                    be_per_nucleon = isotope['binding_energy_per_nucleon']
                    print(f"    {isotope['element']}-{isotope['mass_number']} " +
                          f"({isotope['protons']}p + {isotope['neutrons']}n): " +
                          f"{be_per_nucleon:.3f} MeV/nucleon")
                
                # Highlight exceptional stability
                if max_binding > 7.0:
                    print(f"  ✓ HIGH STABILITY: {mn} shows exceptional binding energy!")
                elif max_binding > 5.0:
                    print(f"  ✓ MODERATE STABILITY: {mn} shows good binding energy")
                else:
                    print(f"  ? Low binding energy at mass {mn}")
            else:
                print(f"\nMass Number A={mn}: No experimental data available")
        
        return magic_results
    
    def find_actual_peaks(self):
        """Find actual binding energy peaks in the data"""
        print("\n" + "="*70)
        print("ACTUAL BINDING ENERGY PEAKS IN EXPERIMENTAL DATA")
        print("="*70)
        
        real_data = self.df_real
        
        # Group by mass number and find the best binding energy for each mass
        mass_groups = real_data.groupby('mass_number').agg({
            'binding_energy_per_nucleon': ['max', 'mean', 'count'],
            'element': lambda x: list(x),
            'protons': lambda x: list(x),
            'neutrons': lambda x: list(x)
        }).round(3)
        
        # Flatten column names
        mass_groups.columns = ['max_binding', 'avg_binding', 'isotope_count', 'elements', 'protons', 'neutrons']
        
        # Find local maxima in binding energy
        masses = sorted(mass_groups.index)
        peaks = []
        
        for i, mass in enumerate(masses):
            if i == 0 or i == len(masses) - 1:
                continue
            
            current_binding = mass_groups.loc[mass, 'max_binding']
            
            # Check neighbors
            prev_mass = masses[i-1]
            next_mass = masses[i+1]
            prev_binding = mass_groups.loc[prev_mass, 'max_binding']
            next_binding = mass_groups.loc[next_mass, 'max_binding']
            
            # Local maximum criteria
            if (current_binding > prev_binding and 
                current_binding > next_binding and 
                current_binding > 2.0):  # Minimum threshold
                
                peaks.append({
                    'mass': mass,
                    'binding': current_binding,
                    'elements': mass_groups.loc[mass, 'elements'],
                    'isotope_count': mass_groups.loc[mass, 'isotope_count']
                })
        
        # Sort by binding energy (highest first)
        peaks = sorted(peaks, key=lambda x: x['binding'], reverse=True)
        
        print("\nActual stability peaks found in experimental data:")
        print("(Local maxima with binding energy > 2.0 MeV/nucleon)")
        print("-" * 60)
        
        for i, peak in enumerate(peaks[:15]):  # Show top 15 peaks
            mass = peak['mass']
            binding = peak['binding']
            elements = set(peak['elements'])
            count = peak['isotope_count']
            
            print(f"{i+1:2d}. Mass A={mass:3d}: {binding:.3f} MeV/nucleon " +
                  f"({count} isotopes: {', '.join(sorted(elements))})")
            
            # Check if this matches our predictions
            if mass in [2, 4, 8, 16, 20, 28, 50, 82, 126]:
                print(f"     ★ MATCHES our geometric prediction!")
        
        return peaks
    
    def calculate_regional_average(self):
        """Calculate centered 3-point moving average for ALL mass numbers A=1 to A_max"""
        real_data = self.df_real
        
        # Get maximum binding energy for each mass number (fill gaps with interpolation/NaN)
        mass_binding = real_data.groupby('mass_number')['binding_energy_per_nucleon'].max().reset_index()
        mass_binding = mass_binding.sort_values('mass_number')
        
        # Create complete mass number range from 1 to max
        min_mass = 1
        max_mass = int(mass_binding['mass_number'].max())
        
        # Create DataFrame with ALL mass numbers
        all_masses = pd.DataFrame({'mass_number': range(min_mass, max_mass + 1)})
        
        # Merge with actual data (this will create NaN for missing mass numbers)
        complete_data = all_masses.merge(mass_binding, on='mass_number', how='left')
        
        # Forward fill and backward fill to handle some gaps
        complete_data['binding_energy_per_nucleon'] = complete_data['binding_energy_per_nucleon'].interpolate(method='linear')
        
        # Calculate centered moving average: (E(A-1) + E(A) + E(A+1)) / 3
        regional_averages = []
        mass_numbers = []
        raw_bindings = []
        
        for i, row in complete_data.iterrows():
            current_mass = row['mass_number']
            current_binding = row['binding_energy_per_nucleon']
            
            # Skip if current binding is NaN
            if pd.isna(current_binding):
                continue
            
            # Get neighbors with bounds checking
            prev_binding = None
            next_binding = None
            
            if i > 0:
                prev_binding = complete_data.iloc[i-1]['binding_energy_per_nucleon']
            if i < len(complete_data) - 1:
                next_binding = complete_data.iloc[i+1]['binding_energy_per_nucleon']
            
            # Calculate average (handle NaN neighbors)
            values = [current_binding]
            if not pd.isna(prev_binding):
                values.append(prev_binding)
            if not pd.isna(next_binding):
                values.append(next_binding)
            
            regional_avg = np.mean(values)
            regional_averages.append(regional_avg)
            mass_numbers.append(current_mass)
            raw_bindings.append(current_binding)
        
        return mass_numbers, regional_averages, raw_bindings
    
    def plot_peak_analysis(self, peaks):
        """Plot the peak analysis results with regional averaging"""
        # Calculate regional averages
        mass_numbers, regional_averages, mass_binding = self.calculate_regional_average()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Peak comparison
        peak_masses = [p['mass'] for p in peaks[:15]]
        peak_bindings = [p['binding'] for p in peaks[:15]]
        
        bars = ax1.bar(peak_masses, peak_bindings, alpha=0.7, color='darkblue', width=0.8)
        
        # Highlight our predictions
        predicted_magic = [2, 4, 8, 16, 20, 28, 50, 82, 126]
        for i, (mass, binding) in enumerate(zip(peak_masses, peak_bindings)):
            if mass in predicted_magic:
                bars[i].set_color('red')
                bars[i].set_alpha(0.9)
                ax1.text(mass, binding + 0.1, '★', ha='center', va='bottom', 
                        fontsize=12, color='red', fontweight='bold')
        
        ax1.set_xlabel('Mass Number (A)')
        ax1.set_ylabel('Binding Energy per Nucleon (MeV)')
        ax1.set_title('Top 15 Actual Stability Peaks\n(Red = Our Predictions)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Raw data points + Regional average trend line
        predicted_masses = []
        predicted_found = []
        predicted_bindings = []
        
        for mass in predicted_magic:
            if mass <= self.df_real['mass_number'].max():
                isotopes = self.df_real[self.df_real['mass_number'] == mass]
                if not isotopes.empty:
                    predicted_masses.append(mass)
                    predicted_found.append(True)
                    predicted_bindings.append(isotopes['binding_energy_per_nucleon'].max())
                else:
                    predicted_masses.append(mass)
                    predicted_found.append(False)
                    predicted_bindings.append(0)
        
        # Plot raw data points
        colors = ['green' if found else 'red' for found in predicted_found]
        bars2 = ax2.bar(predicted_masses, predicted_bindings, alpha=0.6, color=colors, width=0.8,
                       label='Raw Data Points')
        
    def plot_peak_analysis(self, peaks):
        """Plot the peak analysis results with smooth regional averaging"""
        # Calculate regional averages for ALL mass numbers
        mass_numbers, regional_averages, raw_bindings = self.calculate_regional_average()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Plot 1: Peak comparison (unchanged)
        peak_masses = [p['mass'] for p in peaks[:15]]
        peak_bindings = [p['binding'] for p in peaks[:15]]
        
        bars = ax1.bar(peak_masses, peak_bindings, alpha=0.7, color='darkblue', width=0.8)
        
        # Highlight our predictions
        predicted_magic = [2, 4, 8, 16, 20, 28, 50, 82, 126]
        for i, (mass, binding) in enumerate(zip(peak_masses, peak_bindings)):
            if mass in predicted_magic:
                bars[i].set_color('red')
                bars[i].set_alpha(0.9)
                ax1.text(mass, binding + 0.1, '★', ha='center', va='bottom', 
                        fontsize=12, color='red', fontweight='bold')
        
        ax1.set_xlabel('Mass Number (A)')
        ax1.set_ylabel('Binding Energy per Nucleon (MeV)')
        ax1.set_title('Top 15 Actual Stability Peaks\n(Red = Our Predictions)')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Complete trend analysis with smooth regional average
        # Plot the complete smooth trend line first
        ax2.plot(mass_numbers, regional_averages, 'b-', linewidth=2, alpha=0.7, 
                label='Regional Average (Complete A=1 to A_max)', color='navy')
        
        # Plot raw data points for all available masses (small points)
        ax2.scatter(mass_numbers, raw_bindings, alpha=0.3, s=10, color='lightblue', 
                   label='Raw Data Points (All Masses)')
        
        # Now highlight our predicted magic numbers
        predicted_masses = []
        predicted_found = []
        predicted_bindings = []
        predicted_regional_avgs = []
        
        for mass in predicted_magic:
            if mass <= max(mass_numbers):
                # Find if this mass exists in our data
                if mass in mass_numbers:
                    idx = mass_numbers.index(mass)
                    predicted_masses.append(mass)
                    predicted_found.append(True)
                    predicted_bindings.append(raw_bindings[idx])
                    predicted_regional_avgs.append(regional_averages[idx])
                else:
                    # Mass not in data
                    predicted_masses.append(mass)
                    predicted_found.append(False)
                    predicted_bindings.append(0)
                    predicted_regional_avgs.append(0)
        
        # Plot our predictions as larger points
        for mass, binding, found, regional_avg in zip(predicted_masses, predicted_bindings, 
                                                     predicted_found, predicted_regional_avgs):
            if found and binding > 0:
                # Raw data point (large)
                ax2.scatter(mass, binding, s=120, color='red', alpha=0.8, 
                           edgecolors='darkred', linewidth=2, zorder=5)
                # Regional average point
                ax2.scatter(mass, regional_avg, s=80, color='gold', alpha=0.9, 
                           edgecolors='darkorange', linewidth=2, zorder=4, marker='s')
                # Connect with line to show difference
                ax2.plot([mass, mass], [regional_avg, binding], 'k--', alpha=0.5, linewidth=1)
                
                # Labels
                ax2.text(mass, binding + 20, f'{binding:.0f}', 
                        ha='center', va='bottom', fontweight='bold', 
                        color='darkred', fontsize=9)
                ax2.text(mass, regional_avg - 30, f'{regional_avg:.0f}', 
                        ha='center', va='top', fontweight='bold', 
                        color='darkorange', fontsize=8)
        
        ax2.set_xlabel('Mass Number (A)')
        ax2.set_ylabel('Binding Energy per Nucleon (MeV)')
        ax2.set_title('Complete Nuclear Stability Landscape\nRed=Our Predictions, Gold=Regional Average')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Set reasonable axis limits
        if predicted_masses:
            ax2.set_xlim(0, max(predicted_masses) + 2)
        
        plt.tight_layout()
        plt.show()
        
        # Print detailed regional average analysis
        print("\n" + "="*70)
        print("REGIONAL AVERAGE ANALYSIS")
        print("="*70)
        print("Smooth centered 3-point moving average calculated for A=1 to A_max")
        print("Formula: (E(A-1) + E(A) + E(A+1)) / 3")
        print()
        
        valid_predictions = [(m, b, r) for m, b, r in zip(predicted_masses, predicted_bindings, predicted_regional_avgs) 
                           if b > 0]
        
        for mass, raw_binding, regional_avg in valid_predictions:
            difference = raw_binding - regional_avg
            percentage = (difference / regional_avg) * 100 if regional_avg > 0 else 0
            significance = "PEAK" if difference > 50 else "NORMAL" if difference > -50 else "VALLEY"
            
            print(f"Mass A={mass:2d}: Raw={raw_binding:5.1f} MeV, Regional={regional_avg:5.1f} MeV, "
                  f"Diff={difference:+6.1f} MeV ({percentage:+5.1f}%) [{significance}]")
        
        return mass_numbers, regional_averages, valid_predictions
    
    def comprehensive_analysis(self):
        """Run the complete analysis"""
        print("Starting comprehensive nuclear stability analysis...")
        
        # Generate all plots
        self.plot_binding_energy_patterns()
        
        # Analyze magic numbers
        magic_results = self.analyze_magic_numbers()
        
        # Find actual peaks
        peaks = self.find_actual_peaks()
        
        # Plot peak analysis
        self.plot_peak_analysis(peaks)
        
        # Summary
        print("\n" + "="*70)
        print("ANALYSIS SUMMARY")
        print("="*70)
        print(f"Total experimental data points: {len(self.df_real)}")
        print(f"Mass range: A={self.df_real['mass_number'].min()} to A={self.df_real['mass_number'].max()}")
        print(f"Stability peaks found: {len(peaks)}")
        
        # Check how many of our predictions have data
        predicted_magic = [2, 4, 8, 16, 20, 28, 50, 82, 126]
        predictions_with_data = 0
        
        for mass in predicted_magic:
            if mass <= self.df_real['mass_number'].max():
                isotopes = self.df_real[self.df_real['mass_number'] == mass]
                if not isotopes.empty:
                    predictions_with_data += 1
        
        print(f"Our predictions with experimental data: {predictions_with_data}/{len(predicted_magic)}")
        
        return self.df_real, peaks, magic_results

# Main execution
def main():
    analyzer = RealNuclearDataAnalysis('binding-energy3.txt')
    df, peaks, magic_results = analyzer.comprehensive_analysis()
    
    print("\nAnalysis complete! Use the plots and results to evaluate the geometric magic number hypothesis.")
    return analyzer

if __name__ == "__main__":
    analyzer = main()
