

import csv



# Read housing dataset and calculate price per square foot for each property  
print("Housing Price Analysis - Calculating Price Per Square Foot")
print("=" * 80)

with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as input_file:
    reader = csv.DictReader(input_file)
    
    # Print header showing column mapping (area -> square feet)  
    print("{:>15} | {:>20}".format("Price", "Square Feet"))

ENDSCRIPT