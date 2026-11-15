#!/usr/bin/env python3
"""Comprehensive analysis: How furnishing status affects housing prices."""

import pandas as pd

# Load data
print("Loading housing dataset...")
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')

print(f"Total houses in dataset: {len(df):,}")
print("=" * 80)
print()

# Get unique furnishing categories and count per category
furnishing_categories = sorted(df['furnishingstatus'].unique())
total_count_per_cat = {}
for cat in furnishing_categories:
    total_count_per_cat[cat] = int(len(df[df['furnishingstatus'] == cat]))

print("=" * 80)
print("SUMMARY BY FURNISHING STATUS")
print("-" * 40 + "\n".join([f"{str(f):>12}: {count:>6} houses\n".format(f, c=total_count_per_cat[f]) for f in furnishing_categories]))

# Calculate average prices by category with full breakdown
avg_prices_by_furniture = {}

print("=" * 80)
print("\nDETAILED BREAKDOWN FOR EACH FURNISHING CATEGORY")
for furnishing_cat in sorted(furnishing_categories):
    subset = df[df['furnishingstatus'] == furnishing_cat]
    
    avg_price = round(subset['price'].mean(), 2)
    median_price = round(subset['price'].median(), 2)
    std_dev = round(subset['price'].std(), 2) if len(subset) > 1 else 0
    
    avg_prices_by_furniture[furnishing_cat] = {
        'avg': avg_price,
        'median': median_price,
        'count': len(subset),
        'min': int(subset['price'].min()) if not subset.empty else None,
        'max': int(subset['price'].max()) if not subset.empty else None,
        'sum': round(subset['price'].sum(), 2) if not subset.empty else 0,
        'std': std_dev
    }
    
    print(f"\n{'─' * 45}")
    print(f"{furnishing_cat.upper()} ({len(subset)} houses)")
    print("-" * 80)
