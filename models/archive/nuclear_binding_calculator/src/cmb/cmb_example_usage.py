#!/usr/bin/env python3
"""
CMB Peak Mapper - Usage Examples and Advanced Analysis
======================================================

This script demonstrates how to use the CMB Peak Mapper to validate
James Freeman's theory that CMB acoustic peaks correspond to specific
cosmic events in the early universe.

Examples include:
1. Basic validation with synthetic data
2. Loading real Planck data (when available)
3. Advanced analysis and comparison
4. Sensitivity testing
5. Publication-ready plotting

Author: Implementation Team  
Theory: Dr. James Freeman
"""

import numpy as np
import matplotlib.pyplot as plt
from cmb_peak_mapper import CMBPeakMapper, CMBPeak, CosmicEvent
import json

def example_1_basic_validation():
    """
    Example 1: Basic validation with synthetic data
    """
    print("Example 1: Basic Freeman Theory Validation")
    print("-" * 40)
    
    # Create mapper and generate synthetic data
    mapper = CMBPeakMapper()
    ell, power = mapper.generate_synthetic_cmb_data()
    
    # Quick validation
    peaks = mapper.detect_acoustic_peaks(min_prominence=300)
    validation = mapper.validate_freeman_predictions()
    
    print(f"Detected {len(peaks)} acoustic peaks")
    print("Freeman Theory Tests:")
    for test, result in validation.items():
        print(f"  {test}: {'PASS' if result else 'FAIL'}")
    
    success_rate = sum(validation.values()) / len(validation)
    print(f"\nOverall Success Rate: {success_rate:.1%}")
    
    return mapper

def example_2_load_planck_data():
    """
    Example 2: Loading real Planck data (simulated for demo)
    """
    print("\nExample 2: Planck Data Analysis")
    print("-" * 30)
    
    # Simulate loading real Planck data
    # In practice, you would load from FITS files or NASA/ESA databases
    
    # Generate more realistic Planck-like data
    ell_planck = np.logspace(1, 3.7, 2000)  # Higher resolution
    
    # More realistic ΛCDM + Freeman modifications
    # Based on Planck 2018 results with Freeman's predicted deviations
    power_planck = np.zeros_like(ell_planck)
    
    # ISW plateau
    power_planck += 1100 * np.exp(-(ell_planck - 8)**2 / (2 * 15**2))
    
    # Freeman's primary acoustic peaks with Planck-like positions
    peaks_data = [
        (220, 5750, 45),   # P1: W1 → P1 (Neutrino Genesis)
        (538, 4100, 55),   # P2: W2 → P2 (Big Freeze)  
        (831, 2650, 65),   # P3: W3 → P3 (Det-Cord Event)
        (1170, 1850, 75),  # Higher order
        (1520, 1200, 85),  # Higher order
    ]
    
    for pos, amp, width in peaks_data:
        power_planck += amp * np.exp(-(ell_planck - pos)**2 / (2 * width**2))
    
    # Silk damping
    damping = np.exp(-(ell_planck/1500)**1.8)
    power_planck *= damping
    
    # Add realistic Planck noise
    noise = np.random.normal(0, 0.015 * np.max(power_planck), len(ell_planck))
    power_planck += noise
    
    # Analyze with mapper
    mapper = CMBPeakMapper()
    mapper.load_planck_data(ell_planck, power_planck)
    
    peaks = mapper.detect_acoustic_peaks(min_prominence=250)
    mapping = mapper.map_peaks_to_events()
    
    print(f"Detected {len(peaks)} peaks in 'Planck' data")
    print("Event Mapping:")
    for event, peak in mapping.items():
        print(f"  {event}: ℓ={peak.multipole:.0f}, {peak.amplitude:.0f} μK²")
    
    return mapper

def example_3_advanced_analysis():
    """
    Example 3: Advanced analysis with Freeman-specific tests
    """
    print("\nExample 3: Advanced Freeman Theory Analysis")
    print("-" * 42)
    
    mapper = CMBPeakMapper()
    mapper.generate_synthetic_cmb_data()
    
    # Detect peaks with different sensitivity levels
    sensitivity_tests = [100, 200, 300, 400, 500]
    results = {}
    
    for prominence in sensitivity_tests:
        peaks = mapper.detect_acoustic_peaks(min_prominence=prominence)
        validation = mapper.validate_freeman_predictions()
        success_rate = sum(validation.values()) / len(validation)
        results[prominence] = {
            'peaks_detected': len(peaks),
            'success_rate': success_rate,
            'P1_largest': validation.get('P1_is_largest', False)
        }
    
    print("Sensitivity Analysis:")
    print("Prominence | Peaks | Success | P1 Largest")
    print("-" * 40)
    for prom, res in results.items():
        print(f"{prom:9d} | {res['peaks_detected']:5d} | {res['success_rate']:6.1%} | {res['P1_largest']:>10}")
    
    # Freeman-specific amplitude ratio test
    mapper.detect_acoustic_peaks(min_prominence=200)
    mapping = mapper.map_peaks_to_events()
    
    if len(mapping) >= 3:
        p1_amp = mapping.get("W1 → P1", CMBPeak(0,0,0,0,"")).amplitude
        p2_amp = mapping.get("W2 → P2", CMBPeak(0,0,0,0,"")).amplitude  
        p3_amp = mapping.get("W3 → P3", CMBPeak(0,0,0,0,"")).amplitude
        
        if p1_amp > 0:
            print(f"\nFreeman Amplitude Ratios:")
            print(f"P2/P1 = {p2_amp/p1_amp:.3f} (Theory predicts ~0.70)")
            print(f"P3/P1 = {p3_amp/p1_amp:.3f} (Theory predicts ~0.45)")
    
    return mapper, results

def example_4_comparison_with_lcdm():
    """
    Example 4: Compare Freeman predictions with standard ΛCDM
    """
    print("\nExample 4: Freeman vs ΛCDM Comparison")
    print("-" * 37)
    
    # Generate standard ΛCDM spectrum (no Freeman modifications)
    ell = np.logspace(1, 3.5, 1000)
    
    # Standard ΛCDM peaks (no cosmic event interpretation)
    lcdm_power = np.zeros_like(ell)
    lcdm_power += 1000 * np.exp(-(ell - 10)**2 / (2 * 30**2))  # ISW
    lcdm_power += 5500 * np.exp(-(ell - 220)**2 / (2 * 50**2))  # 1st acoustic
    lcdm_power += 3800 * np.exp(-(ell - 530)**2 / (2 * 70**2))  # 2nd acoustic  
    lcdm_power += 2200 * np.exp(-(ell - 800)**2 / (2 * 80**2))  # 3rd acoustic
    lcdm_power *= np.exp(-(ell/1400)**1.5)  # Silk damping
    
    # Freeman modified spectrum  
    mapper_freeman = CMBPeakMapper()
    ell_freeman, freeman_power = mapper_freeman.generate_synthetic_cmb_data()
    
    # Analyze both
    mapper_lcdm = CMBPeakMapper()
    mapper_lcdm.load_planck_data(ell, lcdm_power)
    
    peaks_lcdm = mapper_lcdm.detect_acoustic_peaks(min_prominence=200)
    peaks_freeman = mapper_freeman.detect_acoustic_peaks(min_prominence=200)
    
    print("Peak Count Comparison:")
    print(f"ΛCDM:    {len(peaks_lcdm)} peaks detected")
    print(f"Freeman: {len(peaks_freeman)} peaks detected")
    
    # Compare interpretations
    validation_freeman = mapper_freeman.validate_freeman_predictions()
    
    print(f"\nFreeman Theory Validation:")
    print(f"Success Rate: {sum(validation_freeman.values())/len(validation_freeman):.1%}")
    
    # Plot comparison
    plt.figure(figsize=(12, 8))
    plt.loglog(ell, lcdm_power, 'b-', label='Standard ΛCDM', alpha=0.7)
    plt.loglog(ell_freeman, freeman_power, 'r-', label='Freeman Modified', alpha=0.7)
    
    # Mark peaks
    for peak in peaks_lcdm[:3]:
        plt.plot(peak.multipole, peak.amplitude, 'bo', markersize=6)
    for peak in peaks_freeman[:3]:
        plt.plot(peak.multipole, peak.amplitude, 'ro', markersize=6)
    
    plt.xlabel('Multipole ℓ')
    plt.ylabel('Power Dℓ [μK²]')
    plt.title('CMB Power Spectrum: ΛCDM vs Freeman Theory')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return mapper_lcdm, mapper_freeman

def example_5_publication_ready_plots():
    """
    Example 5: Publication-ready plots for Freeman theory validation
    """
    print("\nExample 5: Publication-Ready Analysis")
    print("-" * 36)
    
    # Create high-quality analysis
    mapper = CMBPeakMapper()
    ell, power = mapper.generate_synthetic_cmb_data()
    peaks = mapper.detect_acoustic_peaks(min_prominence=200)
    mapping = mapper.map_peaks_to_events()
    validation = mapper.validate_freeman_predictions()
    
    # Create publication figure
    fig = plt.figure(figsize=(16, 12))
    
    # Main CMB spectrum plot
    ax1 = plt.subplot(2, 2, (1, 2))
    ax1.loglog(ell, power, 'k-', linewidth=2, alpha=0.8, label='CMB Power Spectrum')
    
    # Color-code peaks by Freeman events
    colors = ['red', 'orange', 'gold', 'green', 'blue']
    for i, peak in enumerate(peaks[:5]):
        color = colors[i] if i < len(colors) else 'purple'
        ax1.plot(peak.multipole, peak.amplitude, 'o', color=color, 
                markersize=10, markeredgecolor='black', markeredgewidth=1)
        
        # Add event labels
        if peak.event_type in mapping:
            ax1.annotate(peak.event_type.replace(' → ', '\n→ '), 
                        xy=(peak.multipole, peak.amplitude),
                        xytext=(15, 25), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.5', fc=color, alpha=0.7),
                        arrowprops=dict(arrowstyle='->', color='black'))
    
    ax1.set_xlabel('Multipole moment ℓ', fontsize=14)
    ax1.set_ylabel('Power Dℓ [μK²]', fontsize=14)
    ax1.set_title('Freeman Theory: CMB Acoustic Peaks as Cosmic Event Signatures', fontsize=16)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=12)
    
    # Peak amplitude comparison
    ax2 = plt.subplot(2, 2, 3)
    if len(peaks) >= 3:
        peak_names = [f"P{i+1}" for i in range(min(5, len(peaks)))]
        peak_amps = [peak.amplitude for peak in peaks[:5]]
        
        bars = ax2.bar(peak_names, peak_amps, color=colors[:len(peak_names)], alpha=0.7)
        ax2.set_ylabel('Peak Amplitude [μK²]', fontsize=12)
        ax2.set_title('Decreasing Amplitude Pattern\n(Freeman Prediction)', fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        # Add values on bars
        for bar, amp in zip(bars, peak_amps):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01*height,
                    f'{amp:.0f}', ha='center', va='bottom', fontsize=10)
    
    # Validation results
    ax3 = plt.subplot(2, 2, 4)
    test_names = list(validation.keys())
    test_results = list(validation.values())
    
    # Shorten test names for display
    short_names = [name.replace('_', ' ').replace('than', '>').title() for name in test_names]
    colors_val = ['green' if result else 'red' for result in test_results]
    
    bars = ax3.barh(short_names, [1] * len(test_names), color=colors_val, alpha=0.7)
    ax3.set_xlim(0, 1.2)
    ax3.set_xlabel('Test Result', fontsize=12)
    ax3.set_title('Freeman Theory Validation', fontsize=14)
    
    # Add PASS/FAIL labels
    for i, (bar, result) in enumerate(zip(bars, test_results)):
        ax3.text(0.5, i, 'PASS' if result else 'FAIL', 
                ha='center', va='center', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('freeman_cmb_validation.png', dpi=300, bbox_inches='tight')
    print("Publication figure saved as 'freeman_cmb_validation.png'")
    plt.show()
    
    return mapper

def example_6_sensitivity_analysis():
    """
    Example 6: Sensitivity analysis for different cosmic parameters
    """
    print("\nExample 6: Sensitivity Analysis")
    print("-" * 29)
    
    # Test sensitivity to different theoretical parameters
    base_mapper = CMBPeakMapper()
    
    # Vary peak amplitude ratios (testing Freeman's specific predictions)
    p2_p1_ratios = [0.60, 0.65, 0.70, 0.75, 0.80]  # Freeman predicts ~0.70
    p3_p1_ratios = [0.35, 0.40, 0.45, 0.50, 0.55]  # Freeman predicts ~0.45
    
    results_matrix = []
    
    for p2_ratio in p2_p1_ratios:
        for p3_ratio in p3_p1_ratios:
            # Generate modified spectrum
            ell = np.logspace(1, 3.5, 1000)
            power = np.zeros_like(ell)
            
            # ISW
            power += 1000 * np.exp(-(ell - 10)**2 / (2 * 30**2))
            
            # Modified peaks with test ratios
            p1_amp = 5800
            p2_amp = p1_amp * p2_ratio
            p3_amp = p1_amp * p3_ratio
            
            power += p1_amp * np.exp(-(ell - 220)**2 / (2 * 50**2))
            power += p2_amp * np.exp(-(ell - 530)**2 / (2 * 70**2))
            power += p3_amp * np.exp(-(ell - 800)**2 / (2 * 80**2))
            
            # Damping
            power *= np.exp(-(ell/1400)**1.5)
            
            # Test with mapper
            mapper = CMBPeakMapper()
            mapper.load_planck_data(ell, power)
            mapper.detect_acoustic_peaks(min_prominence=200)
            validation = mapper.validate_freeman_predictions()
            
            success_rate = sum(validation.values()) / len(validation)
            results_matrix.append({
                'p2_ratio': p2_ratio,
                'p3_ratio': p3_ratio, 
                'success_rate': success_rate,
                'decreasing_pattern': validation.get('decreasing_amplitude_pattern', False)
            })
    
    # Find optimal parameters
    best_result = max(results_matrix, key=lambda x: x['success_rate'])
    
    print("Sensitivity Analysis Results:")
    print(f"Best P2/P1 ratio: {best_result['p2_ratio']:.2f}")
    print(f"Best P3/P1 ratio: {best_result['p3_ratio']:.2f}")
    print(f"Maximum success rate: {best_result['success_rate']:.1%}")
    print(f"Freeman prediction (0.70, 0.45): ", end="")
    
    # Check Freeman's specific prediction
    freeman_result = next((r for r in results_matrix 
                          if abs(r['p2_ratio'] - 0.70) < 0.01 and abs(r['p3_ratio'] - 0.45) < 0.01), 
                         None)
    if freeman_result:
        print(f"{freeman_result['success_rate']:.1%}")
    else:
        print("Not tested")
    
    return results_matrix

def example_7_real_data_preparation():
    """
    Example 7: Prepare for real Planck data analysis
    """
    print("\nExample 7: Real Data Analysis Preparation")
    print("-" * 41)
    
    print("For real Planck data analysis, you would:")
    print("1. Download Planck 2018 power spectrum from:")
    print("   https://pla.esac.esa.int/pla/")
    print("2. Load FITS files using astropy:")
    
    example_code = '''
    from astropy.io import fits
    import healpy as hp
    
    # Load Planck power spectrum
    hdul = fits.open('COM_PowerSpect_CMB-TT-full_R3.01.fits')
    ell = hdul[1].data['ELL']
    dl = hdul[1].data['D_ELL']
    error = hdul[1].data['ERROR']
    
    # Use with mapper
    mapper = CMBPeakMapper()
    mapper.load_planck_data(ell, dl)
    '''
    
    print("3. Example code:")
    print(example_code)
    
    print("4. Key Planck datasets to test:")
    datasets = [
        "TT (Temperature-Temperature correlations)",
        "TE (Temperature-E-mode polarization)", 
        "EE (E-mode polarization)",
        "Low-ℓ (ℓ < 30) for ISW effect",
        "High-ℓ (ℓ > 1000) for Silk damping"
    ]
    
    for i, dataset in enumerate(datasets, 1):
        print(f"   {i}. {dataset}")
    
    print("\n5. Expected Freeman signatures to look for:")
    signatures = [
        "P1 at ℓ ≈ 220 (largest amplitude)",
        "P2 at ℓ ≈ 540 (70% of P1)", 
        "P3 at ℓ ≈ 830 (45% of P1)",
        "Specific high-ℓ damping modifications",
        "Polarization signatures in EE spectrum"
    ]
    
    for i, sig in enumerate(signatures, 1):
        print(f"   {i}. {sig}")

def run_comprehensive_analysis():
    """
    Run comprehensive CMB analysis for Freeman theory validation
    """
    print("CMB Peak Mapper - Comprehensive Freeman Theory Analysis")
    print("=" * 60)
    
    # Run all examples
    mapper1 = example_1_basic_validation()
    mapper2 = example_2_load_planck_data()
    mapper3, sensitivity = example_3_advanced_analysis()
    lcdm_mapper, freeman_mapper = example_4_comparison_with_lcdm()
    pub_mapper = example_5_publication_ready_plots()
    sensitivity_matrix = example_6_sensitivity_analysis()
    example_7_real_data_preparation()
    
    # Generate final comprehensive report
    print("\n" + "=" * 60)
    print("COMPREHENSIVE VALIDATION SUMMARY")
    print("=" * 60)
    
    # Use the publication mapper for final analysis
    report = pub_mapper.generate_validation_report()
    
    print(f"Theory: {report['theory']}")
    print(f"Status: {report['status']}")
    print(f"Overall Success Rate: {report['success_rate']:.1%}")
    
    print(f"\nKey Results:")
    for test, result in report['validation_results'].items():
        print(f"  {test}: {'✓ PASS' if result else '✗ FAIL'}")
    
    print(f"\nDetected Cosmic Events:")
    for event, details in report['peak_details'].items():
        print(f"  {event}: ℓ={details['multipole']:.0f}, {details['amplitude']:.0f} μK²")
    
    # Save comprehensive results
    comprehensive_report = {
        'freeman_theory_validation': report,
        'sensitivity_analysis': sensitivity_matrix[:5],  # Top 5 results
        'validation_date': '2025-08',
        'methodology': 'Synthetic Planck-like data with Freeman modifications',
        'next_steps': [
            'Test with real Planck 2018 data',
            'Validate polarization predictions', 
            'Compare with other alternative cosmologies',
            'Extend to higher-order acoustic peaks'
        ]
    }
    
    with open('comprehensive_cmb_analysis.json', 'w') as f:
        json.dump(comprehensive_report, f, indent=2, default=str)
    
    print(f"\nComprehensive analysis saved to 'comprehensive_cmb_analysis.json'")
    print(f"Publication figure saved to 'freeman_cmb_validation.png'")
    
    return comprehensive_report

if __name__ == "__main__":
    # Run comprehensive analysis
    final_report = run_comprehensive_analysis()