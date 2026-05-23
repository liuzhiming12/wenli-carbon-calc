import pandas as pd

def calculate_carbon_emissions(
    df: pd.DataFrame,
    electricity_factor: float = 0.4364,   # kg COâ‚?kWh, Hubei Grid OM factor 2022
    water_factor: float = 0.28,         # kg COâ‚?å?
    gas_factor: float = 2.17            # kg COâ‚?mÂ³
) -> pd.DataFrame:
    """
    Calculate carbon emissions from energy consumption data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned energy data with columns: ç”µåŠ›(kWh), æ°?å?, ç‡ƒæ°”(m3)
    electricity_factor : float, default 0.4364
        Carbon intensity for electricity in kg COâ‚?kWh (Hubei provincial grid factor (MEE 2022 bulletin)
    water_factor : float, default 0.28
        Carbon intensity for water in kg COâ‚?ton
    gas_factor : float, default 2.17
        Carbon intensity for natural gas in kg COâ‚?mÂ³
    
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
    required_columns = ['ç”µåŠ›(kWh)', 'æ°?å?', 'ç‡ƒæ°”(m3)']
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
    result_df['ç”µåŠ›ç¢³æ’æ”?å?'] = result_df['ç”µåŠ›(kWh)'] * electricity_factor / 1000
    result_df['æ°´ç¢³æ’æ”¾(å?'] = result_df['æ°?å?'] * water_factor / 1000
    result_df['ç‡ƒæ°”ç¢³æ’æ”?å?'] = result_df['ç‡ƒæ°”(m3)'] * gas_factor / 1000
    
    # Calculate total carbon emissions
    result_df['æ€»ç¢³æ’æ”¾(å?'] = (
        result_df['ç”µåŠ›ç¢³æ’æ”?å?'] + 
        result_df['æ°´ç¢³æ’æ”¾(å?'] + 
        result_df['ç‡ƒæ°”ç¢³æ’æ”?å?']
    )
    
    return result_df
