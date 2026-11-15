import csv
import math

file_path = '/home/mosh/.openclaw/workspace/data/housing_data.csv'

prices = []
areas = []

with open(file_path, mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            p_str = row.get('price', '').strip()
            a_str = row.get('area', '').strip()
            
            if not p_str or not a_str:
                continue
                
            p = float(p_str)
            a = float(a_str)
            
            prices.append(p)
            areas.append(a)
        except (ValueError, TypeError):
            continue

n = len(prices)
if n < 2:
    print("Not enough data")
else:
    sum_x = sum(prices)
    sum_y = sum(areas)
    sum_x_sq = sum(x*x for x in prices)
    sum_y_sq = sum(y*y for y in areas)
    sum_xy = sum(x*y for x, y in zip(prices, areas))
    
    numerator = (n * sum_xy) - (sum_x * sum_y)
    denominator = math.sqrt((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))
    
    if denominator == 0:
        print("0.00")
    else:
        correlation = numerator / denominator
        print(f"{correlation:.2f}")
