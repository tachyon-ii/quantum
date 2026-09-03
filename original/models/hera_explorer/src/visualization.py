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
