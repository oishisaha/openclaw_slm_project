

import csv

with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        try:
            price = float(row['price'])