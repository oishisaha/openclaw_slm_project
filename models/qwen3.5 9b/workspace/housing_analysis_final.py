

import csv

# Read the CSV file and calculate price per square foot for each property
with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)
    
    results = []
    
    # Print header with new column name
    print(f"{'Price':>15,} | {'Square Feet (area)':>20,} | Price Per Sq Ft")
