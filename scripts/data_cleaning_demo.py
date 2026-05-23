import pandas as pd

raw_data = {
    "date": ["2023/1/1", "2023-02-01", "Mar 1 2023", "2023/4/1"],
    "department": ["Info. Sci.", "Information Science", "Xinxi Xueyuan", "Info. Sci."],
    "electricity_kwh": [1200, 1500, 1300, None],
    "gas_m3": [300, None, 280, 310]
}

df = pd.DataFrame(raw_data)
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)

dept_map = {"Info. Sci.": "Information Science", "Xinxi Xueyuan": "Information Science"}
df["department"] = df["department"].replace(dept_map)

elec_median = df["electricity_kwh"].median()
df["electricity_kwh"] = df["electricity_kwh"].fillna(elec_median)

OM_FACTOR = 0.4364
df["co2_kg"] = df["electricity_kwh"] * OM_FACTOR

print(df)
print(f"Hubei provincial grid factor: {OM_FACTOR} kgCO2/kWh (MEE 2022 bulletin)")