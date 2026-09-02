# HERA Anomaly Explorer

Model-agnostic exploration tool for HERA deep inelastic scattering data, designed to identify periodic structures and anomalies without theoretical bias.

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download HERA data
# Place HERA_full.csv in data/ directory
```

## Quick Start

### 1. Interactive Explorer (Recommended)
```bash
streamlit run app.py
```
Opens browser with interactive dashboard at http://localhost:8501

### 2. Batch Analysis
```bash
python run_analysis.py --config config/default.yaml
```

### 3. Jupyter Exploration
```bash
jupyter notebook notebooks/
```

## Usage Guide

### Data Exploration Workflow

1. **Start with Overview:**
   - Load the Streamlit app
   - Select "Data Overview" tab
   - Check data quality and coverage

2. **Frequency Analysis:**
   - Select Q² slice using slider
   - Choose baseline method (polynomial, spline, or external QCD)
   - View Lomb-Scargle periodogram
   - Note any peaks above significance threshold

3. **Systematic Scan:**
   - Use "Batch Analysis" tab
   - Set Q² range and analysis parameters
   - Run automated anomaly detection
   - Export findings

### Key Explorations to Try

1. **Look for geometric oscillations:**
   ```
   - Q² range: 5-20 GeV²
   - x range: 0.1-0.5
   - Expected period: Δx ~ 0.06-0.12
   ```

2. **Check phase coherence:**
   ```
   - Select multiple adjacent Q² values
   - Compare peak positions in periodograms
   - Look for consistent phase across energy scales
   ```

3. **Test different baselines:**
   ```
   - Polynomial (degrees 3-6)
   - Spline with varying smoothness
   - Moving average with different windows
   ```

4. **Statistical validation:**
   ```
   - Use permutation tests for significance
   - Check false discovery rate
   - Bootstrap confidence intervals
   ```

## Project Structure

```
hera_explorer/
├── app.py                 # Main Streamlit application
├── run_analysis.py        # Batch analysis script
├── src/
│   ├── data_pipeline.py  # Data loading and preprocessing
│   ├── analysis_engine.py # Core analysis algorithms
│   ├── visualization.py   # Plotting utilities
│   └── utils.py           # Helper functions
├── data/
│   └── HERA_full.csv     # Input data (you provide)
├── config/
│   └── default.yaml      # Configuration parameters
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_frequency_analysis.ipynb
│   └── 03_validation.ipynb
└── outputs/              # Results directory
```

## Analysis Methods

### 1. Lomb-Scargle Periodogram
- Optimal for unevenly spaced data
- No interpolation artifacts
- Provides significance levels

### 2. Wavelet Analysis
- Time-frequency localization
- Detects non-stationary signals

### 3. Autocorrelation
- Model-free periodicity detection
- Robust to noise

## Interpreting Results

### Significance Levels
- 3σ (99.7%): Interesting, worth investigating
- 4σ (99.99%): Strong evidence
- 5σ (99.9999%): Discovery threshold

### What to Look For
1. **Fixed period across Q²** - Geometric signature
2. **Q²-dependent period** - QCD evolution effects
3. **Phase coherence** - Real signal vs. noise
4. **Amplitude scaling** - Physical vs. statistical

## Troubleshooting

### Common Issues

1. **Import errors:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Memory issues with large datasets:**
   - Use data chunking in config
   - Reduce Q² range
   - Increase sampling interval

3. **No peaks in periodogram:**
   - Check baseline method
   - Verify data quality
   - Try different x ranges

## References

- HERA Collaboration: [H1 and ZEUS Combined Results](https://www.desy.de/h1zeus/)
- Lomb-Scargle: [VanderPlas 2018](https://arxiv.org/abs/1703.09824)
- Statistical Methods: [Numerical Recipes](http://numerical.recipes/)

## License

MIT License - See LICENSE file

## Contact

For questions or contributions, please open an issue on GitHub.
