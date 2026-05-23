import pandas as pd
import numpy as np

def clean_campus_billing_data(df):
    """
    Clean and standardize synthetic campus utility billing data.
    
    Real-world challenges handled with synthetic data:
    1. Date format inconsistencies
    2. Department name variations
    3. Missing values
    """
    
    # Step 1: Date format normalization
    # Handle three different date formats commonly found in institutional data
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
        'Xinxi Xueyuan': 'School of Information Science',
        'Computer Science': 'School of Computer Science',
        'CS': 'School of Computer Science',
        'Business School': 'School of Business',
        'Business': 'School of Business',
        'Economics Management': 'School of Economics and Management',
        'Library': 'Library',
        'Lib': 'Library',
        'Administration': 'Administration Building',
        'Admin': 'Administration Building',
    }
    
    df['department'] = df['department'].replace(department_mapping)
    
    # Step 3: Handle missing values conservatively
    # For gas bills, use median as a stopgap
    numeric_cols = ['electricity_kwh', 'gas_m3', 'water_tons']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    
    # Step 4: Calculate carbon using Hubei provincial grid factor
    OM_FACTOR = 0.4364  # kgCO2/kWh, Hubei provincial grid, MEE 2022 bulletin
    
    df['electricity_co2_kg'] = df['electricity_kwh'] * OM_FACTOR
    
    return df

def generate_synthetic_data():
    """Generate synthetic campus billing data with intentional messiness."""
    synthetic_data = {
        'date': ['2024-01-15', '2024/02/20', '15/03/2024', '2024-04-10', '2024/05/05', '01-Jun-2024'],
        'department': ['Xinxi Xueyuan', 'Info. Sci.', 'CS', 'Business', 'Library', 'Admin'],
        'electricity_kwh': [12000, 8500, np.nan, 9200, 6800, np.nan],
        'gas_m3': [450, np.nan, 380, 520, np.nan, 310],
        'water_tons': [120, 95, 110, np.nan, 88, 105]
    }
    return pd.DataFrame(synthetic_data)

def main():
    """Example usage of the data cleaning pipeline with synthetic data"""
    print("=== Synthetic Campus Billing Data Simulation ===")
    print("Note: Data is synthetically generated for prototype validation.\n")
    
    # Generate synthetic messy data
    raw_df = generate_synthetic_data()
    print("Original synthetic messy data:")
    print(raw_df)
    print("\n" + "="*60 + "\n")
    
    # Apply cleaning pipeline
    cleaned_df = clean_campus_billing_data(raw_df)
    
    print("Cleaned and standardized data:")
    print(cleaned_df)
    print(f"\n✓ Hubei provincial grid factor applied: {0.4364} kgCO2/kWh (MEE 2022 bulletin)")
    print("✓ Data source: Synthetic generation for prototype validation")

if __name__ == "__main__":
    main()