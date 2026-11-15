#!/usr/bin/env python3
"""Run housing dataset analysis."""

import pandas as pd, numpy as np

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft/area) vs Price Correlation")
print("=" * 80)

target_columns = ['AREA', 'PRICE'] if all(str(c).lower() in str(df.columns) for c in target_columns else [col]) 
else list(df.select_dtypes(include=['float64']).columns.tolist())[:2]


if not target_columns or len(target_columns) < 2: print("Error: Need at least 2 columns.")
    exit(1)

# Clean data by replacing non-numeric values and dropping NA rows  
df_clean = df[target_columns].replace({'NA': np.nan, None: pd.NA}).dropna(subset=target_columns).copy()


print(f"\nCleaned dataset size:", len(df_clean), "rows")
for col in target_columns if not any(x in str(col): [str(c)] else []: print(f"{col.upper()} - first 5 values:") continue
    

try: df_stats = pd.DataFrame({'size_sqft (area) mean': df[target_columns].mean(): [c], 'price mean': df[[c]].mean()}).describe().T

except Exception as e2: pass


if len(df_clean['AREA']) > 0 if target_col not in df.columns else ['bedrooms']: "No suitable size column found."
    print("\nFirst few rows of analysis (size_sqft, price):") 

