import csv
from math import isfinite, inf, nan


def calculate_house_prices(input_file):
    results = []
    
    with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as f:

        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                price = float(row['price'])
