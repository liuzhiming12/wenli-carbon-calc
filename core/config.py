import os
from dotenv import load_dotenv

load_dotenv()

QIANWEN_API_KEY = os.getenv('QIANWEN_API_KEY', '')

CARBON_INTENSITY = {
    'electricity': 0.4044,
    'water': 0.28,
    'gas': 2.17
}

SEASONAL_FACTORS = {
    1: {'electricity': 1.2, 'water': 0.8, 'gas': 1.5},
    2: {'electricity': 1.1, 'water': 0.8, 'gas': 1.4},
    3: {'electricity': 1.0, 'water': 0.9, 'gas': 1.0},
    4: {'electricity': 0.9, 'water': 1.0, 'gas': 0.8},
    5: {'electricity': 1.0, 'water': 1.1, 'gas': 0.7},
    6: {'electricity': 1.3, 'water': 1.2, 'gas': 0.6},
    7: {'electricity': 0.3, 'water': 0.4, 'gas': 0.3},
    8: {'electricity': 0.3, 'water': 0.4, 'gas': 0.3},
    9: {'electricity': 1.1, 'water': 1.1, 'gas': 0.8},
    10: {'electricity': 1.0, 'water': 1.0, 'gas': 0.9},
    11: {'electricity': 1.0, 'water': 0.9, 'gas': 1.1},
    12: {'electricity': 1.2, 'water': 0.8, 'gas': 1.4}
}

DEPARTMENT_BASE_CONSUMPTION = {
    '行政': {'electricity': 500, 'water': 20, 'gas': 30},
    '教学': {'electricity': 1200, 'water': 50, 'gas': 20},
    '宿舍': {'electricity': 1000, 'water': 80, 'gas': 40},
    '图书': {'electricity': 800, 'water': 30, 'gas': 15},
    '食堂': {'electricity': 1500, 'water': 100, 'gas': 200}
}

APP_SETTINGS = {
    'page_title': 'Wenli Carbon Calculator',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

DATA_VALIDATION = {
    'required_columns': ['date', 'electricity_kwh', 'water_t', 'gas_m3'],
    'date_format': '%Y-%m-%d',
    'min_rows': 1,
    'max_rows': 10000
}