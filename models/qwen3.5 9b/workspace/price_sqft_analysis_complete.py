

import csv

print("Housing Price Analysis - Calculating Price Per Square Foot")
print("=" * 80)

with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)
    
    # Print header showing column mapping (area -> square feet)  
    print(f"{'Price':>15,} | {'Square Feet (area)':>20,} | Price Per Sq Ft")
