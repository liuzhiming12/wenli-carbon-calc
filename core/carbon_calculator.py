import pandas as pd
import json
import os

def load_carbon_factors(factors_path: str = None) -> dict:
    """
    Load carbon emission factors from JSON configuration file.
    
    Parameters
    ----------
    factors_path : str, optional
        Path to factors.json file. If None, defaults to factors.json in project root.
    
    Returns
    -------
    dict
        Dictionary containing carbon factors for electricity, natural_gas, and water.
    """
    if factors_path is None:
        factors_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "factors.json"
        )
    
    with open(factors_path, 'r', encoding='utf-8') as f:
        factors = json.load(f)
    
    return factors

def calculate_carbon_emissions(
    df: pd.DataFrame,
    factors: dict = None
) -> pd.DataFrame:
    """
    Calculate carbon emissions from energy consumption data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned energy data with columns: 电力(kWh), 用水量, 燃气(m3)
    factors : dict, optional
        Dictionary containing carbon factors. If None, loads from factors.json.
    
    Returns
    -------
    pd.DataFrame
        Original dataframe with additional carbon emission columns
    """
    # Load factors from JSON if not provided
    if factors is None:
        factors = load_carbon_factors()
    
    electricity_factor = factors['electricity']['factor']
    water_factor = factors['water']['factor']
    gas_factor = factors['natural_gas']['factor']
    
    # Check if dataframe is empty
    if df.empty:
        print("Warning: Empty dataframe returned")
        return df
    
    # Check required columns
    required_columns = ['电力(kWh)', '用水量', '燃气(m3)']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Create a copy to avoid modifying original dataframe
    result_df = df.copy()
    
    # Convert negative values to 0
    for col in required_columns:
        result_df[col] = result_df[col].clip(lower=0)
    
    # Calculate carbon emissions
    # Convert kg to tons (1 ton = 1000 kg)
    result_df['电力碳排放(吨)'] = result_df['电力(kWh)'] * electricity_factor / 1000
    result_df['水碳排放(吨)'] = result_df['用水量'] * water_factor / 1000
    result_df['燃气碳排放(吨)'] = result_df['燃气(m3)'] * gas_factor / 1000
    
    # Calculate total carbon emissions
    result_df['总碳排放(吨)'] = (
        result_df['电力碳排放(吨)'] + 
        result_df['水碳排放(吨)'] + 
        result_df['燃气碳排放(吨)']
    )
    
    return result_df
