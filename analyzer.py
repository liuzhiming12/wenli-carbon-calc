import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def analyze_carbon_emissions(
    df: pd.DataFrame,
    analysis_type: str = "all",
    time_granularity: str = "month"
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
    results = {
        "time_trend": None,
        "department_comparison": None,
        "energy_type_analysis": None,
        "key_metrics": {}
    }

    if df.empty:
        print("Warning: Empty dataframe returned")
        return results

    if analysis_type in ["all", "energy"]:
        energy_analysis = _analyze_energy_types(df)
        results["energy_type_analysis"] = energy_analysis

    if analysis_type in ["all", "time"] and "日期" in df.columns:
        time_trend = _analyze_time_trend(df, time_granularity)
        results["time_trend"] = time_trend

        if time_trend is not None and not time_trend.empty:
            max_emission_period = time_trend.loc[time_trend['总碳排放(吨)'].idxmax()]
            results["key_metrics"]["highest_emission_period"] = {
                "period": str(max_emission_period.name),
                "emission": float(max_emission_period['总碳排放(吨)'])
            }

    if analysis_type in ["all", "department"]:
        department_col = None
        for col in df.columns:
            if '部门' in col:
                department_col = col
                break

        if department_col:
            dept_analysis = _analyze_departments(df, department_col)
            results["department_comparison"] = dept_analysis

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

def calculate_intensity_metrics(
    df: pd.DataFrame,
    total_population: int = None,
    total_area: float = None
) -> dict:
    """
    Calculate per-capita and per-area carbon emission intensity metrics.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with carbon emission data
    total_population : int, optional
        Total campus population (students + staff)
    total_area : float, optional
        Total building area in square meters

    Returns
    -------
    dict
        Intensity metrics including per-capita and per-area emissions
    """
    total_emission = df['总碳排放(吨)'].sum()

    intensity_results = {
        "total_emission": float(total_emission),
        "per_capita": {},
        "per_area": {},
        "available_metrics": []
    }

    if total_population and total_population > 0:
        per_capita = (total_emission * 1000) / total_population
        intensity_results["per_capita"] = {
            "value": float(per_capita),
            "unit": "kg CO2/person",
            "population": total_population
        }
        intensity_results["available_metrics"].append("per_capita")

    if total_area and total_area > 0:
        per_area = (total_emission * 1000) / total_area
        intensity_results["per_area"] = {
            "value": float(per_area),
            "unit": "kg CO2/m2",
            "area": float(total_area)
        }
        intensity_results["available_metrics"].append("per_area")

    return intensity_results

def predict_future_emissions(
    df: pd.DataFrame,
    energy_savings_rate: float = 0.0,
    prediction_months: int = 12
) -> dict:
    """
    Predict future carbon emissions based on historical trends and energy savings rate.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with carbon emission data
    energy_savings_rate : float, default 0.0
        Expected energy savings rate (0.0 to 1.0)
    prediction_months : int, default 12
        Number of months to predict

    Returns
    -------
    dict
        Prediction results including projected emissions and savings
    """
    if df.empty or '日期' not in df.columns:
        return {"error": "Insufficient data for prediction"}

    df_copy = df.copy()
    df_copy['日期'] = pd.to_datetime(df_copy['日期'])
    df_copy = df_copy.sort_values('日期')

    monthly_emissions = df_copy.set_index('日期').resample('M')['总碳排放(吨)'].sum()

    if len(monthly_emissions) < 3:
        return {"error": "Need at least 3 months of data for prediction"}

    X = np.arange(len(monthly_emissions)).reshape(-1, 1)
    y = monthly_emissions.values

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.arange(len(monthly_emissions), len(monthly_emissions) + prediction_months).reshape(-1, 1)
    future_predictions = model.predict(future_X)

    future_predictions = future_predictions * (1 - energy_savings_rate)

    last_date = monthly_emissions.index[-1]
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=prediction_months, freq='M')

    predicted_df = pd.DataFrame({
        '日期': future_dates,
        '预测碳排放(吨)': future_predictions
    })
    predicted_df.set_index('日期', inplace=True)

    baseline_total = future_predictions.sum()
    savings_total = baseline_total * energy_savings_rate / (1 - energy_savings_rate) if energy_savings_rate < 1 else 0

    return {
        "predictions": predicted_df,
        "baseline_total": float(baseline_total),
        "with_savings_total": float(baseline_total * (1 - energy_savings_rate)),
        "savings_total": float(savings_total),
        "energy_savings_rate": float(energy_savings_rate),
        "trend_slope": float(model.coef_[0]),
        "trend_direction": "increasing" if model.coef_[0] > 0 else "decreasing"
    }

def calculate_carbon_sink(
    tree_count: int = None,
    forest_area: float = None,
    grass_area: float = None
) -> dict:
    """
    Calculate campus carbon sink capacity from vegetation.

    Parameters
    ----------
    tree_count : int, optional
        Number of trees on campus
    forest_area : float, optional
        Forest area in square meters
    grass_area : float, optional
        Grass area in square meters

    Returns
    -------
    dict
        Carbon sink calculation results
    """
    carbon_sink = {
        "total_absorption": 0.0,
        "unit": "tons CO2/year",
        "components": {},
        "offset_ratio": None,
        "offset_status": "insufficient"
    }

    if tree_count and tree_count > 0:
        tree_absorption = tree_count * 0.021
        carbon_sink["components"]["trees"] = {
            "count": tree_count,
            "absorption": float(tree_absorption),
            "factor": 0.021
        }
        carbon_sink["total_absorption"] += tree_absorption

    if forest_area and forest_area > 0:
        forest_absorption = forest_area * 0.01
        carbon_sink["components"]["forest"] = {
            "area": float(forest_area),
            "absorption": float(forest_absorption),
            "factor": 0.01
        }
        carbon_sink["total_absorption"] += forest_absorption

    if grass_area and grass_area > 0:
        grass_absorption = grass_area * 0.002
        carbon_sink["components"]["grass"] = {
            "area": float(grass_area),
            "absorption": float(grass_absorption),
            "factor": 0.002
        }
        carbon_sink["total_absorption"] += grass_absorption

    carbon_sink["total_absorption"] = float(carbon_sink["total_absorption"])

    return carbon_sink

def compare_emissions_with_sink(
    emission_data: dict,
    sink_data: dict
) -> dict:
    """
    Compare total emissions with carbon sink capacity.

    Parameters
    ----------
    emission_data : dict
        Total emission data
    sink_data : dict
        Carbon sink data from calculate_carbon_sink

    Returns
    -------
    dict
        Comparison results including net emissions and offset ratio
    """
    total_emission = emission_data.get("total_emission", 0)
    total_sink = sink_data.get("total_absorption", 0)

    net_emission = total_emission - total_sink

    if total_emission > 0:
        offset_ratio = (total_sink / total_emission) * 100
    else:
        offset_ratio = 0

    if offset_ratio >= 100:
        status = "carbon_neutral"
        status_text = "已达到碳中和"
    elif offset_ratio >= 50:
        status = "good_progress"
        status_text = "减排效果良好"
    elif offset_ratio > 0:
        status = "partial_offset"
        status_text = "部分抵消"
    else:
        status = "insufficient"
        status_text = "碳汇不足"

    return {
        "total_emission": float(total_emission),
        "total_sink": float(total_sink),
        "net_emission": float(net_emission),
        "offset_ratio": float(offset_ratio),
        "status": status,
        "status_text": status_text,
        "additional_sink_needed": float(max(0, total_emission - total_sink))
    }

def _analyze_time_trend(df: pd.DataFrame, granularity: str) -> pd.DataFrame:
    df_copy = df.copy()

    df_copy['日期'] = pd.to_datetime(df_copy['日期'])
    df_copy.set_index('日期', inplace=True)

    if granularity == "month":
        resampled = df_copy.resample('M')
    elif granularity == "quarter":
        resampled = df_copy.resample('Q')
    elif granularity == "year":
        resampled = df_copy.resample('Y')
    else:
        raise ValueError(f"Invalid granularity: {granularity}")

    trend_df = resampled.agg({
        '电力(kWh)': 'sum',
        '水(吨)': 'sum',
        '燃气(m3)': 'sum',
        '电力碳排放(吨)': 'sum',
        '水碳排放(吨)': 'sum',
        '燃气碳排放(吨)': 'sum',
        '总碳排放(吨)': 'sum'
    })

    trend_df['环比变化(%)'] = trend_df['总碳排放(吨)'].pct_change() * 100

    if len(trend_df) > 12:
        trend_df['同比变化(%)'] = trend_df['总碳排放(吨)'].pct_change(periods=12) * 100

    return trend_df

def _analyze_departments(df: pd.DataFrame, department_col: str) -> pd.DataFrame:
    dept_df = df.groupby(department_col).agg({
        '电力(kWh)': 'sum',
        '水(吨)': 'sum',
        '燃气(m3)': 'sum',
        '电力碳排放(吨)': 'sum',
        '水碳排放(吨)': 'sum',
        '燃气碳排放(吨)': 'sum',
        '总碳排放(吨)': 'sum'
    })

    total_emission = dept_df['总碳排放(吨)'].sum()
    dept_df['占比(%)'] = (dept_df['总碳排放(吨)'] / total_emission) * 100

    dept_df = dept_df.sort_values('总碳排放(吨)', ascending=False)

    return dept_df

def _analyze_energy_types(df: pd.DataFrame) -> dict:
    total_electricity = df['电力碳排放(吨)'].sum()
    total_water = df['水碳排放(吨)'].sum()
    total_gas = df['燃气碳排放(吨)'].sum()
    total_emission = df['总碳排放(吨)'].sum()

    if total_emission > 0:
        electricity_percent = (total_electricity / total_emission) * 100
        water_percent = (total_water / total_emission) * 100
        gas_percent = (total_gas / total_emission) * 100
    else:
        electricity_percent = 0
        water_percent = 0
        gas_percent = 0

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