

import csv
from math import isfinite, inf, nan


def calculate_price_per_sqft(price_str, area_str):

    try:
        price = float(price_str) if isinstance(price_str, str) and len(price_str.strip()) > 0 else 0.0
        
        
