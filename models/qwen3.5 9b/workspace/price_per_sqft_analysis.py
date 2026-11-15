

import csv

# Read housing dataset and calculate price per square foot for each property
with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)
    
    results = []
    
    for row in reader:

        try:

            price = float(row['price'])
            area_feet = float(row['area'])  # This is square feet (column named 'area' but contains sq ft values)