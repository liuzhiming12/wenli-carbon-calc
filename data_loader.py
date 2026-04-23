import pandas as pd
from typing import Union
from pathlib import Path


def load_campus_energy_data(file_path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
    """
    Load and clean campus energy consumption data from Excel file

    Args:
        file_path: str - Path to excel file
        sheet_name: str or int, dafault 0 - sheet name or index to read

    Returns:
        pd.DataFrame - Cleaned energy data with standardized columns
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path, sheet_name=sheet_name)

    if df.empty:
        print("Warning: Empty dataframe returned")
        return df

    date_col = None
    for col in df.columns:
        try:
            pd.to_datetime(df[col], errors='coerce')
            valid_ratio = df[col].notna().sum() / len(df)
            if valid_ratio > 0.5:
                date_col = col
                break
        except:
            continue

    if date_col is not None:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.rename(columns={date_col: '日期'})
    else:
        raise ValueError("No valid date column found in the data")

    column_mapping = {
        # Electricity patterns
        '电力': '电力(kWh)',
        '用电量': '电力(kWh)',
        '电': '电力(kWh)',
        'electricity': '电力(kWh)',
        'Electricity': '电力(kWh)',
        # Water patterns
        '水': '水(吨)',
        '用水量': '水(吨)',
        'water': '水(吨)',
        'Water': '水(吨)',
        # Gas patterns
        '燃气': '燃气(m3)',
        '天然气': '燃气(m3)',
        'gas': '燃气(m3)',
        'Gas': '燃气(m3)'
    }

    for old_col, new_col in column_mapping.items():
        for col in df.columns:
            if old_col in col:
                df = df.rename(columns={col: new_col})
                break

    required_columns = ['电力(kWh)', '水(吨)', '燃气(m3)']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0
            print(f"Warning: Added missing column '{col}' with 0 values")

    # Handle missing values
    energy_cols = ['电力(kWh)', '水(吨)', '燃气(m3)']
    df[energy_cols] = df[energy_cols].ffill()
    df[energy_cols] = df[energy_cols].fillna(0)

    # Special handling for summer/winter vacations
    df['月份'] = df['日期'].dt.month
    summer_vacation = [7, 8]  # July-August
    winter_vacation = [1, 2]  # January-February

    for month in summer_vacation + winter_vacation:
        non_vacation_data = df[~df['月份'].isin(summer_vacation + winter_vacation)]
        if not non_vacation_data.empty:
            avg_values = non_vacation_data[energy_cols].mean()
            for col in energy_cols:
                df.loc[df['月份'] == month, col] = df.loc[df['月份'] == month, col].replace(0, avg_values[col])

    df = df.drop('月份', axis=1)

    return df