

import csv

print("Housing Price Analysis - Calculating Price Per Square Foot")
print("=" * 80)

# Read the CSV file and calculate price per square foot for each property  
with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)
    
    total_rows = sum(1 for _ in reader)
