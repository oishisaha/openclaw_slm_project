import csv
from math import isfinite

# Read the CSV file and calculate price per square foot
with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    results = []
    for row in reader:
        try:
            price = float(row['price'])
            area = float(row['area'])  # Using 'area' column (likely square feet)
            
            if isfinite(area) and area > 0:
                price_per_sqft = round(price / area, 2)
