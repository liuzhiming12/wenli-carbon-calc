import os
from dotenv import load_dotenv

load_dotenv()

# ── API ──
QIANWEN_API_KEY = os.getenv('QIANWEN_API_KEY', '')

# ── Carbon emission factors ──
# Electricity: 0.4044 kgCO2/kWh — Hubei grid OM factor 2023 (MEE 2025 bulletin)
# Water: 0.28 kgCO2/t — urban water supply average
# Gas: 2.17 kgCO2/m³ — natural gas combustion
CARBON_INTENSITY = {
    'electricity': 0.4044,
    'water': 0.28,
    'gas': 2.17,
}
