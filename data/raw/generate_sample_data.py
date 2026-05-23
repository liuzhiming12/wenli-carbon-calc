import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate date range
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start_date, end_date, freq='D')

# Departments
departments = ['行政�?, '教学�?, '宿舍�?, '图书�?, '食堂']

# Base consumption values (higher for teaching buildings and dormitories)
base_consumption = {
    '行政�?: {'电力': 500, '�?: 20, '燃气': 30},
    '教学�?: {'电力': 1200, '�?: 50, '燃气': 20},
    '宿舍�?: {'电力': 1000, '�?: 80, '燃气': 40},
    '图书�?: {'电力': 800, '�?: 30, '燃气': 15},
    '食堂': {'电力': 1500, '�?: 100, '燃气': 200}
}

# Seasonal factors
seasonal_factors = {
    1: {'电力': 1.2, '�?: 0.8, '燃气': 1.5},  # Winter
    2: {'电力': 1.1, '�?: 0.8, '燃气': 1.4},  # Winter
    3: {'电力': 1.0, '�?: 0.9, '燃气': 1.0},  # Spring
    4: {'电力': 0.9, '�?: 1.0, '燃气': 0.8},  # Spring
    5: {'电力': 1.0, '�?: 1.1, '燃气': 0.7},  # Spring
    6: {'电力': 1.3, '�?: 1.2, '燃气': 0.6},  # Summer
    7: {'电力': 0.3, '�?: 0.4, '燃气': 0.3},  # Summer vacation
    8: {'电力': 0.3, '�?: 0.4, '燃气': 0.3},  # Summer vacation
    9: {'电力': 1.1, '�?: 1.1, '燃气': 0.8},  # Fall
    10: {'电力': 1.0, '�?: 1.0, '燃气': 0.9},  # Fall
    11: {'电力': 1.0, '�?: 0.9, '燃气': 1.1},  # Fall
    12: {'电力': 1.2, '�?: 0.8, '燃气': 1.4}   # Winter
}

# Day of week factors (weekends have lower consumption)
day_factors = {
    0: {'电力': 0.7, '�?: 0.6, '燃气': 0.7},  # Sunday
    1: {'电力': 1.0, '�?: 1.0, '燃气': 1.0},  # Monday
    2: {'电力': 1.0, '�?: 1.0, '燃气': 1.0},  # Tuesday
    3: {'电力': 1.0, '�?: 1.0, '燃气': 1.0},  # Wednesday
    4: {'电力': 1.0, '�?: 1.0, '燃气': 1.0},  # Thursday
    5: {'电力': 0.8, '�?: 0.7, '燃气': 0.8},  # Friday
    6: {'电力': 0.7, '�?: 0.6, '燃气': 0.7}   # Saturday
}

# Generate data
data = []

for date in date_range:
    month = date.month
    day_of_week = date.weekday()
    
    for dept in departments:
        # Get base consumption
        base = base_consumption[dept]
        
        # Apply seasonal factor
        season_factor = seasonal_factors[month]
        
        # Apply day of week factor
        day_factor = day_factors[day_of_week]
        
        # Calculate consumption with noise
        electricity = base['电力'] * season_factor['电力'] * day_factor['电力'] * (0.9 + 0.2 * np.random.random())
        water = base['�?] * season_factor['�?] * day_factor['�?] * (0.9 + 0.2 * np.random.random())
        gas = base['燃气'] * season_factor['燃气'] * day_factor['燃气'] * (0.9 + 0.2 * np.random.random())
        
        # Round to integer values
        electricity = int(round(electricity))
        water = int(round(water))
        gas = int(round(gas))
        
        # Add to data
        data.append({
            '日期': date.strftime('%Y-%m-%d'),
            '部门': dept,
            '电力(kWh)': electricity,
            '�?�?': water,
            '燃气(m3)': gas
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
excel_path = 'campus_energy_data.xlsx'
df.to_excel(excel_path, index=False)

print(f"Sample data generated and saved to {excel_path}")
print(f"Data shape: {df.shape}")
print(f"Date range: {df['日期'].min()} to {df['日期'].max()}")
print(f"Departments: {', '.join(df['部门'].unique())}")

# Show summary
print("\nConsumption summary:")
print(df.groupby('部门').agg({
    '电力(kWh)': 'sum',
    '�?�?': 'sum',
    '燃气(m3)': 'sum'
}))
