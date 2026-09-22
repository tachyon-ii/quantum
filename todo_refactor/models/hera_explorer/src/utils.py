"""
Utility functions for HERA Explorer
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any
import json
import yaml

def export_results(results: List[Dict], output_path: str, format: str = 'csv'):
    """
    Export analysis results to file
    
    Args:
        results: List of result dictionaries
        output_path: Output file path
        format: Output format ('csv', 'json', 'latex')
    """
    df = pd.DataFrame(results)
    
    if format == 'csv':
        df.to_csv(output_path, index=False)
    elif format == 'json':
        df.to_json(output_path, orient='records', indent=2)
    elif format == 'latex':
        latex_str = df.to_latex(index=False, float_format="%.3e")
        with open(output_path, 'w') as f:
            f.write(latex_str)
    else:
        raise ValueError(f"Unknown format: {format}")

def calculate_statistics(residuals: np.ndarray) -> Dict[str, float]:
    """
    Calculate summary statistics for residuals
    
    Args:
        residuals: Array of residual values
        
    Returns:
        Dictionary of statistics
    """
    return {
        'mean': np.mean(residuals),
        'std': np.std(residuals),
        'skewness': calculate_skewness(residuals),
        'kurtosis': calculate_kurtosis(residuals),
        'min': np.min(residuals),
        'max': np.max(residuals),
        'rms': np.sqrt(np.mean(residuals**2))
    }

def calculate_skewness(x: np.ndarray) -> float:
    """Calculate skewness of distribution"""
    mean = np.mean(x)
    std = np.std(x)
    return np.mean(((x - mean) / std) ** 3)

def calculate_kurtosis(x: np.ndarray) -> float:
    """Calculate excess kurtosis of distribution"""
    mean = np.mean(x)
    std = np.std(x)
    return np.mean(((x - mean) / std) ** 4) - 3

# Simple fix for src/utils.py - replace the generate_report function
def generate_report(results: List[Dict], output_path: str):
    """
    Generate analysis report

    Args:
        results: Analysis results
        output_path: Report output path
    """
    df = pd.DataFrame(results)

    # Filter out NaN values for statistics
    valid_peaks = df.dropna(subset=['peak_significance'])

    report = f"""# HERA Analysis Report

## Summary Statistics

- Number of Q² slices analyzed: {len(df)}
- Q² range: {df['q2'].min():.1f} - {df['q2'].max():.1f} GeV²
- Valid peaks found: {len(valid_peaks)}

## Peak Analysis

"""

    if len(valid_peaks) > 0:
        report += f"""- Mean peak period: {valid_peaks['peak_period'].mean():.3f} ± {valid_peaks['peak_period'].std():.3f}
- Maximum significance: {valid_peaks['peak_significance'].max():.2f}
- Significant peaks (>3σ): {(valid_peaks['peak_significance'] > 3).sum()}

## Top Candidates

| Q² | Period (Δx) | Significance |
|----|------------|--------------|
"""
        for _, row in valid_peaks.nlargest(min(5, len(valid_peaks)), 'peak_significance').iterrows():
            report += f"| {row['q2']:.1f} | {row['peak_period']:.3f} | {row['peak_significance']:.2f} |\n"
    else:
        report += "No significant peaks detected in any Q² slice.\n"

    report += f"""

## Interpretation

The Lomb-Scargle periodogram found {'no clear periodic signals' if len(valid_peaks) == 0 else f'{len(valid_peaks)} potential signals'} in the HERA data.

Generated: {pd.Timestamp.now()}
"""

    with open(output_path, 'w') as f:
        f.write(report)
