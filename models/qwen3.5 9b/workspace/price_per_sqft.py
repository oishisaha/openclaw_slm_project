

import csv

# Read housing dataset and calculate price per square foot for each property
with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)
    
    total_properties = 0
    
    # Print results with header showing the column name mapping 
    print(f"{'Price':>15,} | {'Square Feet (area)':>20,} | Price Per Sq Ft")
