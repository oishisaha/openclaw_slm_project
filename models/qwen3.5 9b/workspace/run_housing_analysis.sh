#!/bin/bash
python3 << 'PYEOF'
import pandas as pd, numpy as np

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft) vs Price Correlation")
print("=" * 80)

# Get numeric columns and identify relevant ones
num_cols = [c for c in df.columns if str(df[c]).strip().isdigit()] 
if not num_cols:
    num_cols = ['bedrooms', 'parking'] 

print(f"\nNumeric/numeric-like columns found:")
for col in sorted(num_cols): print("  - " + col)

# Calculate mean area, price and statistics for size_sqft analysis (area as size_sqft column) 
df_clean = df.select_dtypes(include=['float64', 'int8']).copy() 

if len(df_clean.columns) > 0:
    target_cols = [col.lower() + " " if any(x in str(col).lower()) for col, x] or ['bedrooms'] else []
    
print(f"\nTarget columns available (size_sqft and related): {', '.join([str(c) for c])}")

# Calculate mean area statistics for size_sqft column analysis 
df_stats = df_clean.mean() 
    
for col in target_cols: try: print("Mean value:", df[col].dropna().mean()) 

PYEOF