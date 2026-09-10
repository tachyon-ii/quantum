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
