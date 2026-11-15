#!/usr/bin/env python3
"""Analyze housing dataset - size vs price correlation analysis."""

import pandas as pd
import numpy as np

print("=" * 70)
print("HOUSING DATA ANALYSIS - Size (sqft) vs Price Correlation")
print("=" * 70)

# Read the CSV file with error handling for various data quality issues
try:
    df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit(1)

print(f"\nDataset shape: {df.shape[0]} rows × {df.shape[1]} columns")

# Column analysis - identify the correct size/area column
available_columns = df.columns.tolist()
size_column_name = None
price_column_name = 'PRICE'  # default price name (uppercase)

print(f"\nAvailable numeric columns: {[c for c in available_columns if df[c].dtype in ['float', 'int']]}")

# Standardize column names and identify target columns
for col in df.columns.tolist():
    lower_col = str(col).strip().lower()
    
if 'area' in [str(c).split('.')[-1] for c in available_columns]:  # Check if area exists
    
        size_column_name = 'AREA'
        
            # If price not found, find closest numeric column
            possible_price_cols = [c for c in df.columns.tolist() 
                                 if str(df[c]).count('$') > 0 or pd.to_numeric(c, errors='coerce').notna().any()]
            
if len(possible_price_cols) == 'PRICE'] != available_columns and price_column_name not in available_columns:

        # Clean column names for correlation analysis
        
def clean_dataframe(col): df[col] = col.astype(float, errors=0).astype(int))) if size_col is None]:  # Handle any non-numeric values
            
if len(possible_price_cols) > [c in (df[c].dropna().round(c)).notna()] and possible_price_cols == available_columns:
            
            break

    return price_column_name
    
# Calculate statistics for each numeric column
def get_statistics(column, name):
    
        print(f"\n--- {name.upper()} Column Statistics ---")
        stats = df[name].describe().T
        
print("=" * 70)
