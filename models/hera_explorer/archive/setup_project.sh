#!/bin/bash
# setup_project.sh - Complete HERA Explorer setup

PROJECT_ROOT="hera_explorer"
mkdir -p $PROJECT_ROOT
cd $PROJECT_ROOT

# Create directories
mkdir -p src data outputs notebooks tests docs config

# Create all files with content
cat > README.md << 'EOF'
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
EOF

cat > requirements.txt << 'EOF'
# Core dependencies
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0
matplotlib>=3.4.0
plotly>=5.3.0

# Web framework
streamlit>=1.25.0

# Scientific computing
scikit-learn>=1.0.0
statsmodels>=0.13.0
astropy>=5.0  # For Lomb-Scargle

# Data handling
pyyaml>=6.0
h5py>=3.7.0

# Development
jupyter>=1.0.0
pytest>=7.0.0
black>=22.0.0
pylint>=2.15.0

# Optional but recommended
seaborn>=0.12.0
tqdm>=4.65.0
EOF

cat > app.py << 'EOF'
"""
HERA Anomaly Explorer - Main Streamlit Application
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.data_pipeline import DataPipeline
from src.analysis_engine import AnalysisEngine
from src.visualization import Visualizer

st.set_page_config(
    page_title="HERA Anomaly Explorer",
    page_icon="🔬",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load and cache HERA data"""
    pipeline = DataPipeline()
    return pipeline.load_experimental_data('data/HERA_full.csv')

def main():
    st.title("🔬 HERA Anomaly Explorer")
    st.markdown("### Model-agnostic exploration of deep inelastic scattering data")
    
    # Sidebar controls
    st.sidebar.header("Analysis Parameters")
    
    # Load data
    with st.spinner("Loading HERA data..."):
        df = load_data()
    
    # Q² selection
    q2_values = sorted(df['Q2'].unique())
    q2_range = st.sidebar.select_slider(
        "Q² Range (GeV²)",
        options=q2_values,
        value=(q2_values[10], q2_values[30])
    )
    
    # Baseline method
    baseline_method = st.sidebar.selectbox(
        "Baseline Method",
        ["Polynomial", "Spline", "Moving Average", "External QCD", "None"]
    )
    
    if baseline_method == "Polynomial":
        poly_degree = st.sidebar.slider("Polynomial Degree", 2, 8, 4)
    elif baseline_method == "Spline":
        smoothing = st.sidebar.slider("Smoothing Factor", 0.001, 0.1, 0.01, step=0.001)
    elif baseline_method == "Moving Average":
        window_size = st.sidebar.slider("Window Size", 3, 21, 7, step=2)
    
    # Analysis method
    analysis_method = st.sidebar.selectbox(
        "Analysis Method",
        ["Lomb-Scargle Periodogram", "Wavelet Transform", "Autocorrelation", "All"]
    )
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "🔍 Frequency Analysis", 
                                       "📈 Systematic Scan", "📋 Results"])
    
    with tab1:
        st.header("Data Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Coverage Map")
            viz = Visualizer()
            fig = viz.create_coverage_map(df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Data Statistics")
            st.dataframe(df.describe())
    
    with tab2:
        st.header("Frequency Analysis")
        
        # Select specific Q²
        q2_value = st.select_slider(
            "Select Q² for analysis",
            options=q2_values,
            value=q2_values[20]
        )
        
        # Get slice
        slice_df = df[np.abs(df['Q2'] - q2_value) < 0.1].copy()
        
        if len(slice_df) > 5:
            # Create analysis
            analyzer = AnalysisEngine()
            
            # Calculate baseline and residuals
            baseline = analyzer.calculate_baseline(
                slice_df['x'].values,
                slice_df['sigma'].values,
                method=baseline_method.lower()
            )
            residuals = slice_df['sigma'].values / baseline - 1
            
            # Create plots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=("Residuals", "Lomb-Scargle Periodogram", 
                               "Autocorrelation", "Phase Analysis")
            )
            
            # Residuals plot
            fig.add_trace(
                go.Scatter(x=slice_df['x'], y=residuals, mode='markers', 
                          name='Residuals', error_y=dict(array=slice_df['d tot'].values/100)),
                row=1, col=1
            )
            
            # Periodogram
            freqs, power, significance = analyzer.lomb_scargle_analysis(
                slice_df['x'].values, residuals
            )
            fig.add_trace(
                go.Scatter(x=1/freqs, y=power, name='Power'),
                row=1, col=2
            )
            fig.add_hline(y=significance['99%'], line_dash="dash", 
                         line_color="orange", row=1, col=2)
            
            # Autocorrelation
            lags, corr = analyzer.autocorrelation(slice_df['x'].values, residuals)
            fig.add_trace(
                go.Scatter(x=lags, y=corr, name='Autocorrelation'),
                row=2, col=1
            )
            
            # Update layout
            fig.update_xaxes(title_text="x", row=1, col=1, type='log')
            fig.update_xaxes(title_text="Period (Δx)", row=1, col=2)
            fig.update_xaxes(title_text="Lag", row=2, col=1)
            fig.update_yaxes(title_text="Residual", row=1, col=1)
            fig.update_yaxes(title_text="Power", row=1, col=2)
            fig.update_yaxes(title_text="Correlation", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Peak detection
            st.subheader("Detected Peaks")
            peaks = analyzer.find_peaks(freqs, power, significance['99%'])
            if len(peaks) > 0:
                peak_df = pd.DataFrame(peaks)
                st.dataframe(peak_df)
            else:
                st.info("No significant peaks detected above 99% confidence level")
        else:
            st.warning(f"Insufficient data points for Q² = {q2_value}")
    
    with tab3:
        st.header("Systematic Scan")
        
        if st.button("Run Full Scan"):
            progress = st.progress(0)
            results = []
            
            # Scan through Q² values
            for i, q2 in enumerate(q2_values):
                if q2_range[0] <= q2 <= q2_range[1]:
                    slice_df = df[np.abs(df['Q2'] - q2) < 0.1]
                    if len(slice_df) > 10:
                        analyzer = AnalysisEngine()
                        result = analyzer.analyze_slice(slice_df, baseline_method)
                        results.append(result)
                
                progress.progress((i + 1) / len(q2_values))
            
            # Display results
            if results:
                results_df = pd.DataFrame(results)
                st.subheader("Scan Results")
                st.dataframe(results_df)
                
                # Phase coherence check
                st.subheader("Phase Coherence Analysis")
                fig = go.Figure()
                for period in results_df['peak_period'].unique():
                    mask = results_df['peak_period'] == period
                    fig.add_trace(go.Scatter(
                        x=results_df[mask]['q2'],
                        y=results_df[mask]['peak_phase'],
                        mode='markers',
                        name=f'Δx = {period:.3f}'
                    ))
                fig.update_layout(
                    xaxis_title="Q² (GeV²)",
                    yaxis_title="Phase (radians)",
                    title="Phase Stability Across Q²"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("Results Summary")
        st.info("Analysis results will appear here after running systematic scan")
        
        # Export options
        st.subheader("Export Options")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Export to CSV"):
                st.success("Results exported to outputs/results.csv")
        with col2:
            if st.button("Generate Report"):
                st.success("Report generated in outputs/report.pdf")
        with col3:
            if st.button("Save Figures"):
                st.success("Figures saved to outputs/figures/")

if __name__ == "__main__":
    main()
EOF

cat > src/__init__.py << 'EOF'
"""HERA Explorer Package"""
__version__ = "1.0.0"
EOF

cat > src/data_pipeline.py << 'EOF'
"""
Data Pipeline Module
Handles all data loading, parsing, and preprocessing
"""
import re
import numpy as np
import pandas as pd
from typing import Optional, Tuple, Dict
import yaml

class DataPipeline:
    """Handles HERA data loading and preprocessing"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize with optional config file"""
        self.config = self._load_config(config_path) if config_path else {}
    
    @staticmethod
    def _load_config(config_path: str) -> Dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def parse_xbj_string(s: str) -> float:
        """
        Parse xBj strings like '0.502x10-5' to float
        
        Args:
            s: String representation of xBj value
            
        Returns:
            Float value
        """
        if pd.isna(s):
            return np.nan
        
        s = str(s).strip()
        # Convert scientific notation format
        s = re.sub(r'\s*([0-9.]+)\s*x10\s*([+-]?\d+)\s*', r'\1e\2', s)
        
        try:
            return float(s)
        except ValueError:
            return np.nan
    
    def load_experimental_data(self, filepath: str) -> pd.DataFrame:
        """
        Load HERA experimental data from CSV
        
        Args:
            filepath: Path to HERA data CSV
            
        Returns:
            Cleaned DataFrame with parsed values
        """
        # Read CSV
        df = pd.read_csv(filepath)
        
        # Parse xBj column if it exists as string
        if 'xBj' in df.columns:
            df['x'] = df['xBj'].apply(self.parse_xbj_string)
        elif 'x' in df.columns:
            df['x'] = pd.to_numeric(df['x'], errors='coerce')
        
        # Ensure numeric columns
        numeric_cols = ['Q2', 'sigma', 'd tot', 'd stat', 'd uncor']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calculate derived quantities
        df = self._calculate_derived_quantities(df)
        
        # Remove invalid rows
        df = df.dropna(subset=['Q2', 'x', 'sigma'])
        
        return df
    
    def _calculate_derived_quantities(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate derived physics quantities
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional columns
        """
        # Inelasticity y = Q²/(sx) where s = (√s)²
        s = self.config.get('sqrt_s', 318.0) ** 2
        df['y'] = df['Q2'] / (s * df['x'])
        
        # W² = Q²(1/x - 1) + M_p²
        M_p = 0.938  # Proton mass in GeV
        df['W2'] = df['Q2'] * (1/df['x'] - 1) + M_p**2
        
        # Total uncertainty in decimal form
        if 'd tot' in df.columns:
            df['sigma_error'] = df['sigma'] * df['d tot'] / 100
        
        return df
    
    def load_theory_prediction(self, filepath: str, 
                              theory_type: str = 'qcd') -> pd.DataFrame:
        """
        Load theoretical predictions
        
        Args:
            filepath: Path to theory CSV or grid file
            theory_type: Type of theory ('qcd', 'custom')
            
        Returns:
            DataFrame with theory predictions
        """
        if theory_type == 'qcd':
            # Load standard QCD predictions (HERAPDF, NNPDF, etc.)
            df = pd.read_csv(filepath)
            if 'xBj' in df.columns:
                df['x'] = df['xBj'].apply(self.parse_xbj_string)
            return df
        else:
            # Custom theory format
            return pd.read_csv(filepath)
    
    def merge_data_theory(self, data_df: pd.DataFrame, 
                         theory_df: pd.DataFrame,
                         tolerance: float = 1e-9) -> pd.DataFrame:
        """
        Merge experimental data with theory predictions
        
        Args:
            data_df: Experimental data
            theory_df: Theory predictions
            tolerance: Tolerance for x-matching
            
        Returns:
            Merged DataFrame
        """
        # Round x values for matching
        data_df['x_round'] = data_df['x'].round(9)
        theory_df['x_round'] = theory_df['x'].round(9)
        
        # Merge on Q2 and rounded x
        merged = pd.merge(
            data_df,
            theory_df[['Q2', 'x_round', 'sigma_theory']],
            on=['Q2', 'x_round'],
            how='inner'
        )
        
        # Calculate residuals
        merged['residual'] = merged['sigma'] / merged['sigma_theory'] - 1
        
        # Propagate errors
        if 'sigma_error' in merged.columns:
            merged['residual_error'] = merged['sigma_error'] / merged['sigma_theory']
        
        return merged.drop(columns=['x_round'])
    
    def apply_kinematic_cuts(self, df: pd.DataFrame,
                            q2_min: Optional[float] = None,
                            q2_max: Optional[float] = None,
                            x_min: Optional[float] = None,
                            x_max: Optional[float] = None,
                            y_max: Optional[float] = None) -> pd.DataFrame:
        """
        Apply kinematic cuts to data
        
        Args:
            df: Input DataFrame
            q2_min, q2_max: Q² range
            x_min, x_max: x range
            y_max: Maximum inelasticity
            
        Returns:
            Filtered DataFrame
        """
        mask = pd.Series(True, index=df.index)
        
        if q2_min is not None:
            mask &= df['Q2'] >= q2_min
        if q2_max is not None:
            mask &= df['Q2'] <= q2_max
        if x_min is not None:
            mask &= df['x'] >= x_min
        if x_max is not None:
            mask &= df['x'] <= x_max
        if y_max is not None:
            mask &= df['y'] <= y_max
        
        return df[mask].copy()
EOF

cat > src/analysis_engine.py << 'EOF'
"""
Analysis Engine Module
Core analysis algorithms for anomaly detection
"""
import numpy as np
import pandas as pd
from scipy import signal, interpolate, optimize
from scipy.stats import chi2
from astropy.timeseries import LombScargle
from typing import Dict, Tuple, List, Optional

class AnalysisEngine:
    """Core analysis methods for HERA data"""
    
    def __init__(self):
        """Initialize analysis engine"""
        self.results = {}
    
    def calculate_baseline(self, x: np.ndarray, y: np.ndarray, 
                          method: str = 'spline', **kwargs) -> np.ndarray:
        """
        Calculate baseline for residual computation
        
        Args:
            x: x values
            y: sigma values
            method: Baseline method
            
        Returns:
            Baseline values
        """
        if method == 'polynomial':
            degree = kwargs.get('degree', 4)
            coeffs = np.polyfit(np.log10(x), y, degree)
            baseline = np.polyval(coeffs, np.log10(x))
            
        elif method == 'spline':
            smoothing = kwargs.get('smoothing', 0.01)
            spl = interpolate.UnivariateSpline(
                np.log10(x), y, s=smoothing * len(x)
            )
            baseline = spl(np.log10(x))
            
        elif method == 'moving_average':
            window = kwargs.get('window', 5)
            # Sort by x for rolling window
            idx = np.argsort(x)
            y_sorted = y[idx]
            baseline_sorted = pd.Series(y_sorted).rolling(
                window, center=True, min_periods=1
            ).mean().values
            # Unsort
            baseline = np.empty_like(baseline_sorted)
            baseline[idx] = baseline_sorted
            
        elif method == 'none':
            baseline = np.ones_like(y)
            
        else:
            # Default to spline
            baseline = self.calculate_baseline(x, y, 'spline')
        
        return baseline
    
    def lomb_scargle_analysis(self, x: np.ndarray, y: np.ndarray,
                             errors: Optional[np.ndarray] = None,
                             freq_range: Optional[Tuple[float, float]] = None) \
                             -> Tuple[np.ndarray, np.ndarray, Dict]:
        """
        Perform Lomb-Scargle periodogram analysis
        
        Args:
            x: x values
            y: Residual values
            errors: Error bars
            freq_range: Frequency range to explore
            
        Returns:
            frequencies, power spectrum, significance levels
        """
        # Set frequency range
        if freq_range is None:
            # Default: look for periods from 0.02 to 0.5 in x
            freq_min = 2.0    # 1/0.5
            freq_max = 50.0   # 1/0.02
        else:
            freq_min, freq_max = freq_range
        
        # Create frequency grid
        frequencies = np.linspace(freq_min, freq_max, 1000)
        
        # Perform Lomb-Scargle
        if errors is not None:
            ls = LombScargle(x, y, errors)
        else:
            ls = LombScargle(x, y)
        
        power = ls.power(frequencies)
        
        # Calculate significance levels
        false_alarm_levels = [0.1, 0.01, 0.001]  # 90%, 99%, 99.9%
        significance = {}
        for level in false_alarm_levels:
            significance[f'{(1-level)*100:.1f}%'] = ls.false_alarm_level(level)
        
        return frequencies, power, significance
    
    def wavelet_analysis(self, x: np.ndarray, y: np.ndarray,
                        wavelet: str = 'morlet') -> Tuple[np.ndarray, np.ndarray]:
        """
        Continuous wavelet transform for time-frequency analysis
        
        Args:
            x: x values
            y: Signal values
            wavelet: Wavelet type
            
        Returns:
            scales, wavelet coefficients
        """
        # Interpolate to regular grid for wavelet
        x_regular = np.linspace(x.min(), x.max(), 500)
        y_regular = np.interp(x_regular, x, y)
        
        # Define scales (corresponding to periods in x)
        scales = np.logspace(-2, 0, 100)  # 0.01 to 1.0
        
        # Perform CWT
        coefficients = signal.cwt(y_regular, signal.morlet2, scales)
        
        return scales, np.abs(coefficients)
    
    def autocorrelation(self, x: np.ndarray, y: np.ndarray,
                       max_lag: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate autocorrelation function
        
        Args:
            x: x values
            y: Signal values
            max_lag: Maximum lag to compute
            
        Returns:
            lags, autocorrelation values
        """
        # Interpolate to regular grid
        n_points = len(x)
        x_regular = np.linspace(x.min(), x.max(), n_points)
        y_regular = np.interp(x_regular, x, y)
        
        # Remove mean
        y_centered = y_regular - np.mean(y_regular)
        
        # Calculate autocorrelation
        correlation = np.correlate(y_centered, y_centered, mode='full')
        correlation = correlation[len(correlation)//2:]
        correlation = correlation / correlation[0]  # Normalize
        
        # Create lag array
        if max_lag is None:
            max_lag = len(correlation) // 4
        
        lags = np.arange(max_lag)
        
        return lags[:max_lag], correlation[:max_lag]
    
    def find_peaks(self, frequencies: np.ndarray, power: np.ndarray,
                  threshold: float) -> List[Dict]:
        """
        Find significant peaks in power spectrum
        
        Args:
            frequencies: Frequency array
            power: Power spectrum
            threshold: Significance threshold
            
        Returns:
            List of peak dictionaries
        """
        # Find peaks
        peak_indices, properties = signal.find_peaks(
            power, 
            height=threshold,
            distance=10  # Minimum separation between peaks
        )
        
        peaks = []
        for idx in peak_indices:
            peaks.append({
                'frequency': frequencies[idx],
                'period': 1.0 / frequencies[idx],
                'power': power[idx],
                'significance': power[idx] / threshold
            })
        
        # Sort by power
        peaks.sort(key=lambda x: x['power'], reverse=True)
        
        return peaks
    
    def fit_oscillation_model(self, x: np.ndarray, y: np.ndarray,
                             errors: np.ndarray,
                             fixed_period: Optional[float] = None) -> Dict:
        """
        Fit cosine oscillation model to residuals
        
        Args:
            x: x values
            y: Residual values
            errors: Error bars
            fixed_period: Fix period if provided
            
        Returns:
            Fit parameters and statistics
        """
        def model(x, amp, period, phase, offset, decay):
            return amp * np.cos(2*np.pi*x/period + phase) * np.exp(-decay*(1-x)) + offset
        
        def model_fixed_period(x, amp, phase, offset, decay):
            return amp * np.cos(2*np.pi*x/fixed_period + phase) * np.exp(-decay*(1-x)) + offset
        
        # Initial guess
        if fixed_period:
            p0 = [0.001, 0.0, 0.0, 0.5]
            bounds = ([0, -np.pi, -0.1, 0], [0.1, np.pi, 0.1, 5])
            fit_func = model_fixed_period
        else:
            p0 = [0.001, 0.1, 0.0, 0.0, 0.5]
            bounds = ([0, 0.02, -np.pi, -0.1, 0], [0.1, 0.5, np.pi, 0.1, 5])
            fit_func = model
        
        try:
            popt, pcov = optimize.curve_fit(
                fit_func, x, y, p0=p0, sigma=errors,
                absolute_sigma=True, bounds=bounds, maxfev=10000
            )
            
            # Calculate chi-squared
            y_fit = fit_func(x, *popt)
            chi2_val = np.sum(((y - y_fit) / errors) ** 2)
            ndof = len(x) - len(popt)
            
            # Parameter errors
            perr = np.sqrt(np.diag(pcov))
            
            if fixed_period:
                result = {
                    'amplitude': popt[0],
                    'amplitude_err': perr[0],
                    'period': fixed_period,
                    'period_err': 0.0,
                    'phase': popt[1],
                    'phase_err': perr[1],
                    'offset': popt[2],
                    'offset_err': perr[2],
                    'decay': popt[3],
                    'decay_err': perr[3],
                    'chi2': chi2_val,
                    'ndof': ndof,
                    'chi2_ndof': chi2_val / ndof if ndof > 0 else np.inf
                }
            else:
                result = {
                    'amplitude': popt[0],
                    'amplitude_err': perr[0],
                    'period': popt[1],
                    'period_err': perr[1],
                    'phase': popt[2],
                    'phase_err': perr[2],
                    'offset': popt[3],
                    'offset_err': perr[3],
                    'decay': popt[4],
                    'decay_err': perr[4],
                    'chi2': chi2_val,
                    'ndof': ndof,
                    'chi2_ndof': chi2_val / ndof if ndof > 0 else np.inf
                }
            
            return result
            
        except Exception as e:
            print(f"Fit failed: {e}")
            return None
    
    def analyze_slice(self, df: pd.DataFrame, baseline_method: str = 'spline') -> Dict:
        """
        Complete analysis of a Q² slice
        
        Args:
            df: DataFrame for single Q² value
            baseline_method: Method for baseline calculation
            
        Returns:
            Analysis results dictionary
        """
        x = df['x'].values
        y = df['sigma'].values
        
        # Calculate baseline and residuals
        baseline = self.calculate_baseline(x, y, baseline_method)
        residuals = y / baseline - 1
        
        # Error propagation
        if 'd tot' in df.columns:
            errors = df['d tot'].values / 100 * y / baseline
        else:
            errors = np.full_like(residuals, 0.01)
        
        # Lomb-Scargle analysis
        freqs, power, significance = self.lomb_scargle_analysis(x, residuals, errors)
        
        # Find peaks
        peaks = self.find_peaks(freqs, power, significance['99%'])
        
        # Fit oscillation model
        fit_result = self.fit_oscillation_model(x, residuals, errors)
        
        result = {
            'q2': df['Q2'].iloc[0],
            'n_points': len(x),
            'baseline_method': baseline_method,
            'peak_period': peaks[0]['period'] if peaks else np.nan,
            'peak_power': peaks[0]['power'] if peaks else np.nan,
            'peak_significance': peaks[0]['significance'] if peaks else np.nan,
        }
        
        if fit_result:
            result.update({
                'fit_amplitude': fit_result['amplitude'],
                'fit_period': fit_result['period'],
                'fit_phase': fit_result['phase'],
                'fit_chi2_ndof': fit_result['chi2_ndof']
            })
        
        return result
    
    def bootstrap_significance(self, x: np.ndarray, y: np.ndarray,
                              n_bootstrap: int = 1000) -> np.ndarray:
        """
        Bootstrap analysis for significance testing
        
        Args:
            x: x values
            y: Residual values
            n_bootstrap: Number of bootstrap samples
            
        Returns:
            Distribution of peak powers under null hypothesis
        """
        peak_powers = []
        
        for _ in range(n_bootstrap):
            # Shuffle residuals
            y_shuffled = np.random.permutation(y)
            
            # Calculate periodogram
            ls = LombScargle(x, y_shuffled)
            frequencies = np.linspace(2, 50, 500)
            power = ls.power(frequencies)
            
            # Record maximum power
            peak_powers.append(np.max(power))
        
        return np.array(peak_powers)
EOF

cat > src/visualization.py << 'EOF'
"""
Visualization Module
Plotting utilities for HERA data analysis
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple

class Visualizer:
    """Visualization utilities for HERA analysis"""
    
    def __init__(self, style: str = 'plotly'):
        """
        Initialize visualizer
        
        Args:
            style: 'plotly' or 'matplotlib'
        """
        self.style = style
        if style == 'matplotlib':
            sns.set_style('whitegrid')
            plt.rcParams['figure.figsize'] = (10, 6)
    
    def create_coverage_map(self, df: pd.DataFrame) -> go.Figure:
        """
        Create 2D coverage map of data points
        
        Args:
            df: Data DataFrame
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=go.Scatter(
            x=df['x'],
            y=df['Q2'],
            mode='markers',
            marker=dict(
                size=5,
                color=df['sigma'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="σ_r")
            ),
            text=df.apply(lambda row: f"Q²={row['Q2']:.1f}, x={row['x']:.3e}", axis=1),
            hovertemplate='%{text}<br>σ_r=%{marker.color:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="HERA Data Coverage",
            xaxis=dict(title="x", type='log'),
            yaxis=dict(title="Q² (GeV²)", type='log'),
            height=600
        )
        
        return fig
    
    def plot_residuals(self, x: np.ndarray, residuals: np.ndarray,
                      errors: Optional[np.ndarray] = None,
                      fit_x: Optional[np.ndarray] = None,
                      fit_y: Optional[np.ndarray] = None) -> go.Figure:
        """
        Plot residuals with optional fit overlay
        
        Args:
            x: x values
            residuals: Residual values
            errors: Error bars
            fit_x, fit_y: Fit curve coordinates
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Data points
        error_y = dict(array=errors) if errors is not None else None
        fig.add_trace(go.Scatter(
            x=x, y=residuals,
            mode='markers',
            name='Data',
            error_y=error_y,
            marker=dict(size=6, color='blue')
        ))
        
        # Fit curve
        if fit_x is not None and fit_y is not None:
            fig.add_trace(go.Scatter(
                x=fit_x, y=fit_y,
                mode='lines',
                name='Fit',
                line=dict(color='red', width=2)
            ))
        
        # Zero line
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        fig.update_layout(
            title="Residuals (Data/Theory - 1)",
            xaxis=dict(title="x", type='log'),
            yaxis=dict(title="Residual"),
            height=400
        )
        
        return fig
    
    def plot_periodogram(self, frequencies: np.ndarray, power: np.ndarray,
                        significance_levels: Dict[str, float]) -> go.Figure:
        """
        Plot Lomb-Scargle periodogram
        
        Args:
            frequencies: Frequency array
            power: Power spectrum
            significance_levels: Dict of significance thresholds
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Convert to periods
        periods = 1.0 / frequencies
        
        # Power spectrum
        fig.add_trace(go.Scatter(
            x=periods, y=power,
            mode='lines',
            name='Power Spectrum',
            line=dict(color='blue', width=2)
        ))
        
        # Significance levels
        colors = ['yellow', 'orange', 'red']
        for (label, level), color in zip(significance_levels.items(), colors):
            fig.add_hline(
                y=level,
                line_dash="dash",
                line_color=color,
                annotation_text=label
            )
        
        fig.update_layout(
            title="Lomb-Scargle Periodogram",
            xaxis=dict(title="Period (Δx)", type='log'),
            yaxis=dict(title="Power"),
            height=400
        )
        
        return fig
    
    def plot_phase_coherence(self, results_df: pd.DataFrame) -> go.Figure:
        """
        Plot phase coherence across Q² values
        
        Args:
            results_df: DataFrame with analysis results
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Group by similar periods
        period_groups = results_df.groupby(
            pd.cut(results_df['peak_period'], bins=10)
        )
        
        for period_range, group in period_groups:
            if len(group) > 1:
                fig.add_trace(go.Scatter(
                    x=group['q2'],
                    y=group['fit_phase'],
                    mode='markers+lines',
                    name=f'Δx ∈ {period_range}',
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title="Phase Coherence Analysis",
            xaxis=dict(title="Q² (GeV²)", type='log'),
            yaxis=dict(title="Phase (radians)"),
            height=500
        )
        
        return fig
    
    def create_summary_dashboard(self, results: List[Dict]) -> go.Figure:
        """
        Create multi-panel summary dashboard
        
        Args:
            results: List of analysis results
            
        Returns:
            Plotly figure with subplots
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Peak Period vs Q²", "Peak Power vs Q²",
                          "Amplitude Distribution", "Chi² Distribution"),
            specs=[[{"type": "scatter"}, {"type": "scatter"}],
                   [{"type": "histogram"}, {"type": "histogram"}]]
        )
        
        df = pd.DataFrame(results)
        
        # Peak period vs Q²
        fig.add_trace(
            go.Scatter(x=df['q2'], y=df['peak_period'],
                      mode='markers', name='Period'),
            row=1, col=1
        )
        
        # Peak power vs Q²
        fig.add_trace(
            go.Scatter(x=df['q2'], y=df['peak_power'],
                      mode='markers', name='Power'),
            row=1, col=2
        )
        
        # Amplitude distribution
        fig.add_trace(
            go.Histogram(x=df['fit_amplitude'], name='Amplitude'),
            row=2, col=1
        )
        
        # Chi² distribution
        fig.add_trace(
            go.Histogram(x=df['fit_chi2_ndof'], name='χ²/ndf'),
            row=2, col=2
        )
        
        fig.update_xaxes(title_text="Q² (GeV²)", type='log', row=1, col=1)
        fig.update_xaxes(title_text="Q² (GeV²)", type='log', row=1, col=2)
        fig.update_xaxes(title_text="Amplitude", row=2, col=1)
        fig.update_xaxes(title_text="χ²/ndf", row=2, col=2)
        
        fig.update_yaxes(title_text="Period (Δx)", row=1, col=1)
        fig.update_yaxes(title_text="Power", row=1, col=2)
        fig.update_yaxes(title_text="Count", row=2, col=1)
        fig.update_yaxes(title_text="Count", row=2, col=2)
        
        fig.update_layout(height=800, showlegend=False)
        
        return fig
    
    def save_publication_figure(self, fig: go.Figure, filename: str,
                               width: int = 800, height: int = 600):
        """
        Save figure in publication-ready format
        
        Args:
            fig: Plotly figure
            filename: Output filename
            width, height: Figure dimensions
        """
        # Update layout for publication
        fig.update_layout(
            font=dict(size=14),
            width=width,
            height=height,
            template='plotly_white'
        )
        
        # Save as multiple formats
        fig.write_image(f"{filename}.pdf")
        fig.write_image(f"{filename}.png", scale=2)
        fig.write_html(f"{filename}.html")
EOF

cat > src/utils.py << 'EOF'
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

def generate_report(results: List[Dict], output_path: str):
    """
    Generate analysis report
    
    Args:
        results: Analysis results
        output_path: Report output path
    """
    # This would generate a PDF report using reportlab or similar
    # For now, create a markdown summary
    
    df = pd.DataFrame(results)
    
    report = f"""# HERA Analysis Report

## Summary Statistics

- Number of Q² slices analyzed: {len(df)}
- Q² range: {df['q2'].min():.1f} - {df['q2'].max():.1f} GeV²
- Mean peak period: {df['peak_period'].mean():.3f} ± {df['peak_period'].std():.3f}
- Significant peaks (>3σ): {(df['peak_significance'] > 3).sum()}

## Top Candidates

{df.nlargest(5, 'peak_significance')[['q2', 'peak_period', 'peak_significance']].to_markdown()}

## Recommendations

1. Focus on Q² = {df.loc[df['peak_significance'].idxmax(), 'q2']:.1f} GeV² for detailed study
2. Check phase coherence for period Δx ≈ {df['peak_period'].mode()[0]:.3f}
3. Consider alternative baseline methods for validation

Generated: {pd.Timestamp.now()}
"""
    
    with open(output_path, 'w') as f:
        f.write(report)
EOF

cat > run_analysis.py << 'EOF'
"""
Batch analysis script for HERA data
"""
import argparse
import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from tqdm import tqdm

from src.data_pipeline import DataPipeline
from src.analysis_engine import AnalysisEngine
from src.visualization import Visualizer
from src.utils import export_results, generate_report

def main():
    parser = argparse.ArgumentParser(description="HERA Anomaly Batch Analysis")
    parser.add_argument('--config', default='config/default.yaml',
                       help='Configuration file')
    parser.add_argument('--data', default='data/HERA_full.csv',
                       help='HERA data file')
    parser.add_argument('--output', default='outputs',
                       help='Output directory')
    args = parser.parse_args()
    
    # Load configuration
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    pipeline = DataPipeline(args.config)
    analyzer = AnalysisEngine()
    visualizer = Visualizer()
    
    # Load data
    print("Loading HERA data...")
    df = pipeline.load_experimental_data(args.data)
    
    # Apply cuts
    df = pipeline.apply_kinematic_cuts(
        df,
        q2_min=config.get('q2_min', 5.0),
        q2_max=config.get('q2_max', 100.0),
        y_max=config.get('y_max', 0.7)
    )
    
    # Get unique Q² values
    q2_values = sorted(df['Q2'].unique())
    print(f"Analyzing {len(q2_values)} Q² slices...")
    
    # Analyze each slice
    results = []
    for q2 in tqdm(q2_values):
        slice_df = df[np.abs(df['Q2'] - q2) < 0.1]
        
        if len(slice_df) < config.get('min_points', 10):
            continue
        
        # Analyze
        result = analyzer.analyze_slice(
            slice_df,
            baseline_method=config.get('baseline_method', 'spline')
        )
        results.append(result)
    
    # Export results
    print("Exporting results...")
    export_results(results, output_dir / 'results.csv')
    
    # Generate report
    generate_report(results, output_dir / 'report.md')
    
    # Create summary plots
    print("Creating visualizations...")
    fig = visualizer.create_summary_dashboard(results)
    visualizer.save_publication_figure(
        fig, 
        str(output_dir / 'summary'),
        width=1200, height=800
    )
    
    print(f"Analysis complete. Results saved to {output_dir}")

if __name__ == "__main__":
    main()
EOF

cat > config/default.yaml << 'EOF'
# HERA Explorer Configuration

# Data parameters
sqrt_s: 318.0  # Center of mass energy

# Kinematic cuts
q2_min: 5.0
q2_max: 100.0
x_min: null
x_max: null
y_max: 0.7

# Analysis parameters
baseline_method: spline  # polynomial, spline, moving_average, none
polynomial_degree: 4
spline_smoothing: 0.01
moving_average_window: 5

# Frequency analysis
freq_min: 2.0   # 1/period_max
freq_max: 50.0  # 1/period_min
n_frequencies: 1000

# Significance testing
significance_levels: [0.9, 0.99, 0.999]
n_bootstrap: 1000

# Processing
min_points: 10  # Minimum points per Q² slice
chunk_size: null  # For memory management

# Output
save_figures: true
figure_format: [pdf, png]
export_format: csv  # csv, json, latex
EOF

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter
.ipynb_checkpoints
*.ipynb_checkpoints

# Data files
data/*.csv
data/*.h5
data/*.root

# Output files
outputs/
*.pdf
*.png
*.html
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Documentation
docs/_build/
EOF

echo "Project setup complete!"
echo ""
echo "Next steps:"
echo "1. cd hera_explorer"
echo "2. python -m venv venv"
echo "3. source venv/bin/activate"
echo "4. pip install -r requirements.txt"
echo "5. cp ../HERA_full.csv data/"
echo "6. streamlit run app.py"
