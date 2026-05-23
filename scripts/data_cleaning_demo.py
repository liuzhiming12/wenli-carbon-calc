import pandas as pd
import numpy as np

def clean_campus_billing_data(file_path):
    """
    Clean and standardize campus utility billing data from messy Excel files.
    
    Real-world challenges handled:
    1. Date format inconsistencies
    2. Department name variations
    3. Missing values
    """
    
    # Load raw data
    df = pd.read_excel(file_path)
    
    # Step 1: Date format normalization
    # Handle three different date formats commonly found in campus billing
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True, errors='coerce')
    
    # Fallback for problematic dates using regex
    mask = df['date'].isna()
    if mask.any():
        df.loc[mask, 'date'] = pd.to_datetime(
            df.loc[mask, 'date'].astype(str).str.extract(r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})')[0],
            errors='coerce'
        )
    
    # Step 2: Department name standardization
    department_mapping = {
        'Info. Sci.': 'School of Information Science',
        'Information Science': 'School of Information Science',
        '信息学院': 'School of Information Science',
        '计算机学院': 'School of Computer Science',
        'CS': 'School of Computer Science',
        '商学院': 'School of Business',
        'Business': 'School of Business',
        '经管学院': 'School of Economics and Management',
        '图书馆': 'Library',
        'Lib': 'Library',
        '行政楼': 'Administration Building',
        'Admin': 'Administration Building',
    }
    
    df['department'] = df['department'].replace(department_mapping)
    
    # Step 3: Handle missing values conservatively
    # For gas bills, use median as a stopgap
    numeric_cols = ['electricity_kwh', 'gas_m3', 'water_tons']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    
    # Step 4: Calculate carbon using Hubei Grid OM factor
    OM_FACTOR = 0.562  # kgCO2/kWh, Hubei 2022 provincial bulletin
    
    df['electricity_co2_kg'] = df['electricity_kwh'] * OM_FACTOR
    
    return df

def main():
    """Example usage of the data cleaning pipeline"""
    # Note: This is a demo. Replace with actual file path.
    # cleaned_df = clean_campus_billing_data('campus_billing_2024.xlsx')
    
    # For demonstration, create sample messy data
    sample_data = {
        'date': ['2024-01-15', '2024/02/20', '15/03/2024', '2024-04-10'],
        'department': ['信息学院', 'Info. Sci.', 'CS', '商学院'],
        'electricity_kwh': [12000, 8500, np.nan, 9200],
        'gas_m3': [450, np.nan, 380, 520],
        'water_tons': [120, 95, 110, np.nan]
    }
    
    df = pd.DataFrame(sample_data)
    print("Original messy data:")
    print(df)
    print("\n" + "="*50 + "\n")
    
    # Apply cleaning
    cleaned_df = pd.DataFrame(sample_data)
    cleaned_df['date'] = pd.to_datetime(cleaned_df['date'], infer_datetime_format=True)
    
    department_mapping = {
        '信息学院': 'School of Information Science',
        'Info. Sci.': 'School of Information Science',
        'CS': 'School of Computer Science',
        '商学院': 'School of Business',
    }
    cleaned_df['department'] = cleaned_df['department'].replace(department_mapping)
    
    cleaned_df['electricity_kwh'] = cleaned_df['electricity_kwh'].fillna(cleaned_df['electricity_kwh'].median())
    cleaned_df['gas_m3'] = cleaned_df['gas_m3'].fillna(cleaned_df['gas_m3'].median())
    cleaned_df['water_tons'] = cleaned_df['water_tons'].fillna(cleaned_df['water_tons'].median())
    
    OM_FACTOR = 0.562
    cleaned_df['electricity_co2_kg'] = cleaned_df['electricity_kwh'] * OM_FACTOR
    
    print("Cleaned and standardized data:")
    print(cleaned_df)
    print(f"\n✓ Hubei Grid OM factor applied: {OM_FACTOR} kgCO2/kWh")

if __name__ == "__main__":
    main()