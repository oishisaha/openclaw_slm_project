#!/usr/bin/env python3
"""Comprehensive analysis: How furnishing status affects housing prices."""

import pandas as pd

# Load data with error handling
try:
    df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')
except FileNotFoundError:
    print(f"ERROR: Cannot find file at /home/vboxuser/.openclaw/workspace/data/housing_dataset.csv")
    exit(1)

print("Loading housing dataset... ✓")
df.head()  # Preview first few rows for verification
total_count = len(df)
print("=" * 80 + "\n" + f"HOW FURNISHING STATUS AFFECTS HOUSING PRICES\nTotal houses analyzed: {total_count:,}")
print("=" * 80 + "\n")

# Get unique furnishing categories and count per category
furnishing_categories = sorted(df['furnishingstatus'].unique())
print("Categories Found:")
for cat in furnishing_categories:
    print(f"  • {cat}: {int(len(df[df['furnishingstatus'] == cat])):,} houses")

# Calculate average prices by category with full breakdown
avg_prices_by_furniture = {}

print("\n\n" + "=" * 80)
print("AVERAGE PRICES BY FURNISHING CATEGORY (DETAILED BREAKDOWN)")
for furnishing_cat in sorted(furnishing_categories):
    subset = df[df['furnishingstatus'] == furnishing_cat]
    
    avg_price = round(subset['price'].mean(), 2)
    median_price = round(subset['price'].median(), 2)
    std_dev = round(subset['price'].std()) if len(subset) > 1 else None
    