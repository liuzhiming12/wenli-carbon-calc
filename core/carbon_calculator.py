import pandas as pd

def calculate_carbon_emissions(
    df: pd.DataFrame,
    electricity_factor: float = 0.4364,   # kg CO2/kWh, Hubei Grid OM factor 2022
    water_factor: float = 0.28,         # kg CO2/吨
    gas_factor: float = 2.17            # kg CO2/m³
) -> pd.DataFrame:
    """
    Calculate carbon emissions from energy consumption data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned energy data with columns: 电力(kWh), 用水量, 燃气(m3)
    electricity_factor : float, default 0.4364
        Carbon intensity for electricity in kg CO2/kWh (Hubei provincial grid factor (MEE 2022 bulletin)
    water_factor : float, default 0.28
        Carbon intensity for water in kg CO2/ton
    gas_factor : float, default 2.17
        Carbon intensity for natural gas in kg CO2/m³
    
    Returns
    -------
    pd.DataFrame
        Original dataframe with additional carbon emission columns
    """
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
