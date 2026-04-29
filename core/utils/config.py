import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AI API configurations
QIANWEN_API_KEY = os.getenv('QIANWEN_API_KEY', '')

# Carbon intensity factors (kg CO2 per unit)
CARBON_INTENSITY = {
    'electricity': 0.5839,  # Hubei grid carbon intensity
    'water': 0.28,          # Water carbon intensity
    'gas': 2.17             # Natural gas carbon intensity
}

# Seasonal factors for energy consumption
SEASONAL_FACTORS = {
    1: {'electricity': 1.2, 'water': 0.8, 'gas': 1.5},  # Winter
    2: {'electricity': 1.1, 'water': 0.8, 'gas': 1.4},  # Winter
    3: {'electricity': 1.0, 'water': 0.9, 'gas': 1.0},  # Spring
    4: {'electricity': 0.9, 'water': 1.0, 'gas': 0.8},  # Spring
    5: {'electricity': 1.0, 'water': 1.1, 'gas': 0.7},  # Spring
    6: {'electricity': 1.3, 'water': 1.2, 'gas': 0.6},  # Summer
    7: {'electricity': 0.3, 'water': 0.4, 'gas': 0.3},  # Summer vacation
    8: {'electricity': 0.3, 'water': 0.4, 'gas': 0.3},  # Summer vacation
    9: {'electricity': 1.1, 'water': 1.1, 'gas': 0.8},  # Fall
    10: {'electricity': 1.0, 'water': 1.0, 'gas': 0.9}, # Fall
    11: {'electricity': 1.0, 'water': 0.9, 'gas': 1.1}, # Fall
    12: {'electricity': 1.2, 'water': 0.8, 'gas': 1.4}  # Winter
}

# Department base consumption
DEPARTMENT_BASE_CONSUMPTION = {
    '行政楼': {'electricity': 500, 'water': 20, 'gas': 30},
    '教学楼': {'electricity': 1200, 'water': 50, 'gas': 20},
    '宿舍区': {'electricity': 1000, 'water': 80, 'gas': 40},
    '图书馆': {'electricity': 800, 'water': 30, 'gas': 15},
    '食堂': {'electricity': 1500, 'water': 100, 'gas': 200}
}

# Application settings
APP_SETTINGS = {
    'page_title': '文理碳计 - 校园碳足迹计算器',
    'page_icon': '🌍',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Data validation settings
DATA_VALIDATION = {
    'required_columns': ['日期', '电力(kWh)', '水(吨)', '燃气(m3)'],
    'date_format': '%Y-%m-%d',
    'min_rows': 1,
    'max_rows': 10000
}