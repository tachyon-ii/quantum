"""
Analysis Engine Module - Fixed version
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
        # Remove any NaN or infinite values
        mask = np.isfinite(x) & np.isfinite(y)
        if errors is not None:
            mask &= np.isfinite(errors)
            errors = errors[mask]
        x = x[mask]
        y = y[mask]
        
        # Check if we have enough points
        if len(x) < 3:
            # Return empty results
            return np.array([]), np.array([]), {'90': 0, '99': 0, '99.9': 0}
        
        # Set frequency range
        if freq_range is None:
            # Default: look for periods from 0.02 to 0.5 in x
            freq_min = 2.0    # 1/0.5
            freq_max = 50.0   # 1/0.02
        else:
            freq_min, freq_max = freq_range
        
        # Create frequency grid
        frequencies = np.linspace(freq_min, freq_max, 1000)
        
        try:
            # Perform Lomb-Scargle
            if errors is not None and len(errors) == len(x):
                ls = LombScargle(x, y, errors)
            else:
                ls = LombScargle(x, y)
            
            power = ls.power(frequencies)
            
            # Handle any NaN or infinite values in power
            if not np.all(np.isfinite(power)):
                power = np.nan_to_num(power, nan=0.0, posinf=0.0, neginf=0.0)
            
            # Calculate significance levels
            significance = {}
            try:
                significance['90'] = ls.false_alarm_level(0.1)
                significance['99'] = ls.false_alarm_level(0.01)
                significance['99.9'] = ls.false_alarm_level(0.001)
            except:
                # If false alarm calculation fails, use simple percentiles
                significance['90'] = np.percentile(power, 90)
                significance['99'] = np.percentile(power, 99)
                significance['99.9'] = np.percentile(power, 99.9)
                
        except Exception as e:
            print(f"Lomb-Scargle failed: {e}")
            # Return empty results on failure
            return np.array([]), np.array([]), {'90': 0, '99': 0, '99.9': 0}
        
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
        peaks = []
        
        # Check for valid inputs
        if len(frequencies) == 0 or len(power) == 0:
            return peaks
        
        # Ensure arrays are finite
        mask = np.isfinite(power) & np.isfinite(frequencies)
        if not np.any(mask):
            return peaks
        
        power = power[mask]
        frequencies = frequencies[mask]
        
        try:
            # Find peaks
            peak_indices, properties = signal.find_peaks(
                power, 
                height=threshold,
                distance=10  # Minimum separation between peaks
            )
            
            if len(peak_indices) > 0:
                for idx in peak_indices:
                    if idx < len(frequencies):  # Safety check
                        peaks.append({
                            'frequency': frequencies[idx],
                            'period': 1.0 / frequencies[idx] if frequencies[idx] > 0 else np.inf,
                            'power': power[idx],
                            'significance': power[idx] / threshold if threshold > 0 else 0
                        })
            
        except Exception as e:
            print(f"Peak finding failed: {e}")
        
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
        
        # Basic result dictionary
        result = {
            'q2': df['Q2'].iloc[0],
            'n_points': len(x),
            'baseline_method': baseline_method,
            'peak_period': np.nan,
            'peak_power': np.nan,
            'peak_significance': np.nan,
            'fit_amplitude': np.nan,
            'fit_period': np.nan,
            'fit_phase': np.nan,
            'fit_chi2_ndof': np.nan
        }
        
        try:
            # Calculate baseline and residuals
            baseline = self.calculate_baseline(x, y, baseline_method)
            
            # Check for valid baseline
            if not np.all(np.isfinite(baseline)) or np.any(baseline <= 0):
                print(f"Invalid baseline for Q² = {result['q2']}")
                return result
                
            residuals = y / baseline - 1
            
            # Error propagation
            if 'd tot' in df.columns:
                errors = df['d tot'].values / 100 * y / baseline
            else:
                errors = np.full_like(residuals, 0.01)
            
            # Ensure finite values
            mask = np.isfinite(residuals) & np.isfinite(errors) & (errors > 0)
            if np.sum(mask) < 3:
                print(f"Insufficient valid points for Q² = {result['q2']}")
                return result
            
            # Lomb-Scargle analysis
            freqs, power, significance = self.lomb_scargle_analysis(
                x[mask], residuals[mask], errors[mask]
            )
            
            # Find peaks
            if len(freqs) > 0 and len(power) > 0:
                peaks = self.find_peaks(freqs, power, significance.get('99', 0))
                
                if peaks:
                    result['peak_period'] = peaks[0]['period']
                    result['peak_power'] = peaks[0]['power']
                    result['peak_significance'] = peaks[0]['significance']
            
            # Fit oscillation model
            if np.sum(mask) >= 5:  # Need at least 5 points for fitting
                fit_result = self.fit_oscillation_model(x[mask], residuals[mask], errors[mask])
                
                if fit_result:
                    result['fit_amplitude'] = fit_result['amplitude']
                    result['fit_period'] = fit_result['period']
                    result['fit_phase'] = fit_result['phase']
                    result['fit_chi2_ndof'] = fit_result['chi2_ndof']
                    
        except Exception as e:
            print(f"Analysis failed for Q² = {result['q2']}: {e}")
        
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
