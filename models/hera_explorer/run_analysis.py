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
