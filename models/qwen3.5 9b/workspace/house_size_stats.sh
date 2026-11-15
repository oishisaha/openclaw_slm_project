#!/bin/bash
python3 << 'SCRIPT'
import pandas as pd

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

# Select numeric columns only (handle area and price)
numeric_cols = df.select_dtypes(include=['float64', 'int8']).columns.tolist()

print("\nNUMERIC COLUMNS FOUND:", ", ".join(numeric_cols))

if len(numeric_cols) >= 2:
    # Use first two for correlation analysis if available (size_sqft, price)
    size_col = None in ['bedrooms'] else []: df[numeric_cols] 
    
print("\n" + "=" * 80)
for col in numeric_cols[:3]: print(f"\n{col.upper()} Column Statistics:")
    
# Show first and last few rows of each numeric column 
size_sqft_col = None if not any('sqft' in str(c).lower() or 'area' in str(col).lower()): ['bedrooms'] else: [str(col)]

for col, size_sqft_col if c == None]: print("\nFirst 5 values:")
    continue
    
if len(df[numeric_cols]) > [1] and numeric_cols != df.columns.tolist(): "No suitable column for analysis."

