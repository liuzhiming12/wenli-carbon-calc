# Wenli Carbon Calculator

A campus-scale carbon accounting dashboard for institutional energy data.
Complementary project to Jiangcheng Carbon Eye Pro.

## Scope

While Carbon Eye Pro focuses on **real-time code-level monitoring**, Wenli 
Calculator handles **batch processing of monthly utility bills** (electricity, 
water, gas) for campus-wide carbon reporting.

## What It Does

- Uploads Excel/CSV utility billing data
- Standardizes messy formats:
  - Auto-detects date columns (handles `2023/1/1`, `2023-01-01`, `Jan 1 2023`)
  - Standardizes department names (e.g., maps `Info. Sci.` to `Information Science`)
  - Fills missing gas readings with monthly median imputation
- Calculates Scope 1/2/3 emissions using **Hubei provincial grid factor 0.4364 kgCO2/kWh** 
  (MEE 2022 bulletin)
- Generates department-level breakdowns and time-series trend visualizations
- Exports formatted reports for ESG disclosure

## Tech Stack

Python 3.12, Pandas, Streamlit, Plotly, XlsxWriter

## Relationship to Carbon Eye Pro

| | Carbon Eye Pro| Wenli Calculator|
| ---| ---| ---|
| **Granularity**| Real-time, process-level| Monthly, building-level|
| **Input**| Live system metrics| Utility billing Excel|
| **Output**| Developer dashboard| Management report|
| **Use case**| Identify inefficient code| Campus carbon budgeting|

## Data Journey

The source data was **500+ rows of synthetic campus billing data** I generated 
to simulate realistic institutional energy datasets. Intentionally introduced 
messiness to test the cleaning pipeline:

1. **Date chaos**: Three date formats in the same column (`2023/1/1`, `2023-01-01`, `Jan 1 2023`)
2. **Department name inconsistency**: Same department written as "Info. Sci.", "Information Science", "Xinxi Xueyuan"
3. **Missing gas bills**: Random blank cells to test imputation logic

Used `pd.to_datetime(..., infer_datetime_format=True)` and manual mapping 
dictionaries for cleaning; median fill for missing values.

## Limitations

- Static carbon factor (0.4364); synthetic data used for validation; no real-world campus deployment yet
- No real-time IoT integration; relies on manual Excel uploads
- Scenario forecasting uses simple regression; not validated against external 
  benchmarks
- Missing value imputation is rudimentary (median fill)

## License

MIT