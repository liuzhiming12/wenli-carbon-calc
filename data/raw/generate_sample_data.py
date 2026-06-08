import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(output_file='campus_energy_data.xlsx'):
    """
    Generate sample campus energy consumption data for testing.
    """
    # Generate date range
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Departments
    departments = ['行政楼', '教学楼', '宿舍楼', '图书馆', '食堂']
    
    data = []
    for date in dates:
        month = date.month
        # Seasonal adjustments
        if month in [7, 8]:  # Summer vacation
            multiplier = 0.3
        elif month in [1, 2]:  # Winter vacation
            multiplier = 0.5
        else:
            multiplier = 1.0
            
        for dept in departments:
            # Base consumption for each department
            base_electricity = {
                '行政楼': 800,
                '教学楼': 2000,
                '宿舍楼': 1500,
                '图书馆': 600,
                '食堂': 1800
            }
            
            base_water = {
                '行政楼': 30,
                '教学楼': 80,
                '宿舍楼': 150,
                '图书馆': 20,
                '食堂': 200
            }
            
            base_gas = {
                '行政楼': 20,
                '教学楼': 10,
                '宿舍楼': 50,
                '图书馆': 5,
                '食堂': 300
            }
            
            electricity = base_electricity[dept] * multiplier * (0.9 + np.random.random() * 0.2)
            water = base_water[dept] * multiplier * (0.9 + np.random.random() * 0.2)
            gas = base_gas[dept] * multiplier * (0.9 + np.random.random() * 0.2)
            
            data.append({
                '日期': date.strftime('%Y-%m-%d'),
                '部门': dept,
                '电力(kWh)': round(electricity, 2),
                '用水量': round(water, 2),
                '燃气(m3)': round(gas, 2)
            })
    
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)
    print(f"Sample data generated: {output_file}")

if __name__ == '__main__':
    generate_sample_data()
