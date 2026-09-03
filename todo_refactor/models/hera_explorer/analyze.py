import pandas as pd
import numpy as np

df = pd.read_csv('outputs/results.csv')

# Count successful analyses
analyzed = df[df['n_points'].notna()]
print(f"Analyzed: {len(analyzed)}/46 Q² slices")
print(f"Q² range analyzed: {analyzed['q2'].min():.2f} - {analyzed['q2'].max():.1f} GeV²")

# Check fit results
has_fit = df['fit_amplitude'].notna()
print(f"\nSlices with fits: {has_fit.sum()}")
print(f"Fits at amplitude bound (>0.099): {(df['fit_amplitude'] > 0.099).sum()}")

# Look at the distribution of fitted periods
periods = df['fit_period'].dropna()
if len(periods) > 0:
    print(f"\nFitted periods range: {periods.min():.3f} - {periods.max():.3f}")
    print(f"Most common period range: 0.02-0.09 (count: {((periods >= 0.02) & (periods <= 0.09)).sum()})")
