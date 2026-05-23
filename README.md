# Wenli Carbon Calculator

A campus-scale carbon accounting dashboard for institutional energy data. 
Complementary project to Jiangcheng Carbon Eye Pro.

## Scope

While Carbon Eye Pro focuses on **real-time code-level monitoring**, Wenli Calculator 
handles **batch processing of monthly utility bills** (electricity, water, gas) for 
campus-wide carbon reporting.

## What It Does

- Uploads Excel/CSV utility billing data
- Standardizes messy formats (auto-detects date columns, handles missing values)
- Calculates Scope 1/2/3 emissions using **Hubei Grid OM factor 0.562 kgCO₂/kWh**
- Generates department-level breakdowns and time trends
- Exports formatted reports for ESG disclosure

## Tech Stack

Python 3.12, Pandas, Streamlit, Plotly, XlsxWriter

## Relationship to Carbon Eye Pro

| | Carbon Eye Pro | Wenli Calculator |
|---|---|---|
| **Granularity** | Real-time, process-level | Monthly, building-level |
| **Input** | Live system metrics | Utility billing Excel |
| **Output** | Developer dashboard | Management report |
| **Use case** | Identify inefficient code | Campus carbon budgeting |

## Limitations

- Static carbon factor (0.562); no dynamic grid mix adjustment
- No real-time IoT integration; relies on manual Excel uploads
- Scenario forecasting uses simple regression; not validated against external benchmarks

## License

MIT