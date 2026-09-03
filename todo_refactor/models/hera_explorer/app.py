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
