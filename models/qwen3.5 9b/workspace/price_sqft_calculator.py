

import csv


def calculate_price_per_square_foot(price_str, area_str):

    price = float(price_str) if price_str != '' else 0.0
    area = float(area_str) if area_str.replace('.', '').isdigit() else 1.0
    
    

if __name__ == "__main__":
    