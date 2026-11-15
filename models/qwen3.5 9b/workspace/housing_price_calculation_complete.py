

import csv

print("Calculating Price Per Square Foot for housing data...")
print("=" * 80)

# Read the CSV file and calculate price per square foot for each property
with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)
    
    # Print header with new column showing original mapping  
    print(f"{'Price':>15,} | {'Area (Square Feet)':>20,} | Price Per Sq Ft")
