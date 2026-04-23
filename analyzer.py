import pandas as pd

def analyze_carbon_emissions(
    df: pd.DataFrame,
    analysis_type: str = "all",  # "time", "department", "all"
    time_granularity: str = "month"  # "month", "quarter", "year"
) -> dict:
    """
    Analyze carbon emissions data.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with carbon emission data
    analysis_type : str, default "all"
        Type of analysis to perform: "time", "department", or "all"
    time_granularity : str, default "month"
        Time granularity for trend analysis: "month", "quarter", or "year"
    
    Returns
    -------
    dict
        Analysis results including time trends, department comparison, and energy type analysis
    """
    # Initialize results dictionary
    results = {
        "time_trend": None,
        "department_comparison": None,
        "energy_type_analysis": None,
        "key_metrics": {}
    }
    
    # Check if dataframe is empty
    if df.empty:
        print("Warning: Empty dataframe returned")
        return results
    
    # Energy type analysis (always performed)
    if analysis_type in ["all", "energy"]:
        energy_analysis = _analyze_energy_types(df)
        results["energy_type_analysis"] = energy_analysis
    
    # Time trend analysis
    if analysis_type in ["all", "time"] and "日期" in df.columns:
        time_trend = _analyze_time_trend(df, time_granularity)
        results["time_trend"] = time_trend
        
        # Add key metrics
        if time_trend is not None and not time_trend.empty:
            max_emission_period = time_trend.loc[time_trend['总碳排放(吨)'].idxmax()]
            results["key_metrics"]["highest_emission_period"] = {
                "period": max_emission_period.name,
                "emission": float(max_emission_period['总碳排放(吨)'])
            }
    
    # Department comparison analysis
    if analysis_type in ["all", "department"]:
        # Check if department column exists
        department_col = None
        for col in df.columns:
            if '部门' in col:
                department_col = col
                break
        
        if department_col:
            dept_analysis = _analyze_departments(df, department_col)
            results["department_comparison"] = dept_analysis
            
            # Add key metrics
            if dept_analysis is not None and not dept_analysis.empty:
                max_emission_dept = dept_analysis.loc[dept_analysis['总碳排放(吨)'].idxmax()]
                results["key_metrics"]["highest_emission_department"] = {
                    "department": max_emission_dept.name,
                    "emission": float(max_emission_dept['总碳排放(吨)']),
                    "percentage": float(max_emission_dept['占比(%)'])
                }
        else:
            results["department_comparison"] = "No department data available"
    
    return results

def _analyze_time_trend(df: pd.DataFrame, granularity: str) -> pd.DataFrame:
    """
    Analyze time trends of carbon emissions.
    """
    # Create a copy to avoid modifying original dataframe
    df_copy = df.copy()
    
    # Set date as index
    df_copy['日期'] = pd.to_datetime(df_copy['日期'])
    df_copy.set_index('日期', inplace=True)
    
    # Resample based on granularity
    if granularity == "month":
        resampled = df_copy.resample('M')
    elif granularity == "quarter":
        resampled = df_copy.resample('Q')
    elif granularity == "year":
        resampled = df_copy.resample('Y')
    else:
        raise ValueError(f"Invalid granularity: {granularity}")
    
    # Aggregate data
    trend_df = resampled.agg({
        '电力(kWh)': 'sum',
        '水(吨)': 'sum',
        '燃气(m3)': 'sum',
        '电力碳排放(吨)': 'sum',
        '水碳排放(吨)': 'sum',
        '燃气碳排放(吨)': 'sum',
        '总碳排放(吨)': 'sum'
    })
    
    # Calculate month-over-month change
    trend_df['环比变化(%)'] = trend_df['总碳排放(吨)'].pct_change() * 100
    
    # Calculate year-over-year change if data spans multiple years
    if len(trend_df) > 12:
        trend_df['同比变化(%)'] = trend_df['总碳排放(吨)'].pct_change(periods=12) * 100
    
    return trend_df

def _analyze_departments(df: pd.DataFrame, department_col: str) -> pd.DataFrame:
    """
    Analyze carbon emissions by department.
    """
    # Group by department
    dept_df = df.groupby(department_col).agg({
        '电力(kWh)': 'sum',
        '水(吨)': 'sum',
        '燃气(m3)': 'sum',
        '电力碳排放(吨)': 'sum',
        '水碳排放(吨)': 'sum',
        '燃气碳排放(吨)': 'sum',
        '总碳排放(吨)': 'sum'
    })
    
    # Calculate percentage of total
    total_emission = dept_df['总碳排放(吨)'].sum()
    dept_df['占比(%)'] = (dept_df['总碳排放(吨)'] / total_emission) * 100
    
    # Sort by total emission
    dept_df = dept_df.sort_values('总碳排放(吨)', ascending=False)
    
    return dept_df

def _analyze_energy_types(df: pd.DataFrame) -> dict:
    """
    Analyze carbon emissions by energy type.
    """
    # Calculate total emissions by energy type
    total_electricity = df['电力碳排放(吨)'].sum()
    total_water = df['水碳排放(吨)'].sum()
    total_gas = df['燃气碳排放(吨)'].sum()
    total_emission = df['总碳排放(吨)'].sum()
    
    # Calculate percentages
    if total_emission > 0:
        electricity_percent = (total_electricity / total_emission) * 100
        water_percent = (total_water / total_emission) * 100
        gas_percent = (total_gas / total_emission) * 100
    else:
        electricity_percent = 0
        water_percent = 0
        gas_percent = 0
    
    # Calculate total energy consumption
    total_electricity_kwh = df['电力(kWh)'].sum()
    total_water_ton = df['水(吨)'].sum()
    total_gas_m3 = df['燃气(m3)'].sum()
    
    return {
        "emissions": {
            "电力": float(total_electricity),
            "水": float(total_water),
            "燃气": float(total_gas),
            "总": float(total_emission)
        },
        "percentages": {
            "电力": float(electricity_percent),
            "水": float(water_percent),
            "燃气": float(gas_percent)
        },
        "consumption": {
            "电力(kWh)": float(total_electricity_kwh),
            "水(吨)": float(total_water_ton),
            "燃气(m3)": float(total_gas_m3)
        }
    }