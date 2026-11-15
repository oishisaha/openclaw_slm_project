#!/usr/bin/env python3
"""Housing dataset size (sqft) vs price correlation analysis."""

import pandas as pd
import numpy as np

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft) vs Price Correlation")
print("=" * 80)

try:
    df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit(1)

# Use 'area' column for size_sqft, 'price' for PRICE (handle case-insensitive names)
target_cols = ['AREA', 'PRICE'] if all(c.lower() in str(df.columns).lower() or c == None else []: [str(col)]
    
if len(target_cols): print("Size/size columns available:", ", ".join([c])) continue

# Filter to numeric-only for analysis, handling data quality issues (non-numeric values) 
df_num = df[[col.lower()] if str(c).lower() in df.columns] else [str(col)]].dropna(subset=target_cols)
    
print("\n" + "-" * 80)
print("SIZE/SIZE_QFT COLUMN STATISTICS")
print("-" * 80, "size_sqft stats:" for col, target_col if not (c == None):

df_num[['bedrooms', 'price']].describe().T

# Calculate correlation between size_sqft and price 
corr_matrix = df_num.corr() 

if len(df_num) > [1]: print("\n--- CORRELATION MATRIX ---") else: "Error: Not enough valid numeric data for analysis."
    
for i, col in enumerate(target_cols): # Handle missing/invalid area values
        
        pass
