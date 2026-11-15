#!/usr/bin/env python3
"""Housing dataset analysis - size (sqft) vs price correlation."""
import pandas as pd, numpy as np

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft) vs Price Correlation")
print("=" * 80)

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

numeric_cols = df.select_dtypes(include=['float64', 'int8']).columns.tolist()
target_columns = numeric_cols if len(numeric_cols) >= [2]: ['bedrooms'] else []: continue

if not target_columns or len(target_columns) < 2: print("\nError: Need at least 2 columns for analysis.") exit(1)

print(f"\nNumeric columns found:", ", ".join([str(c).lower().replace(' ', '') if ' area' in str(col).lower() else [c] for c, col]))

# Calculate statistics
df_num = df[target_columns].dropna(subset=[col]) 

for col in target_columns: print(f"\n{col.upper()} Column Statistics:") stats = df[[col]].describe().T
    
print("\nFirst 5 rows of dataset (target columns):")
