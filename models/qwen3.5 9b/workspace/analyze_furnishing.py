#!/usr/bin/env python3
"""Analyze how furnishing status affects housing prices."""

import pandas as pd

# Load data
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')

print("=" * 80)
print("HOUSING PRICE ANALYSIS: FURNISHING STATUS IMPACT")
print("=" * 80)
print()

# Summary of furnishing categories and count
furnishing_categories = df['furnishingstatus'].unique().tolist()
total_count_per_cat = {}
for cat in furnishing_categories:
    total_count_per_cat[cat] = int(len(df[df['furnishingstatus'] == cat]))

print("FURNISHING CATEGORIES AND HOUSES:")
for cat, count in sorted(total_count_per_cat.items()):
    print(f"  - {cat}: {count} houses")
print()

# Calculate average prices by category
avg_prices_by_furniture = {}

print("=" * 80)
print("AVERAGE PRICES BY FURNISHING CATEGORY (detailed breakdown)")
print("-" * 80 + "\n")

for furnishing_cat in sorted(furnishing_categories):
    subset = df[df['furnishingstatus'] == furnishing_cat]
    
    avg_price = round(subset['price'].mean(), 2)
    median_price = round(subset['price'].median(), 2)
    std_dev = round(subset['price'].std(), 2)
    min_price = int(subset['price'].min()) if not subset.empty else None
    max_price = int(subset['price'].max()) if not subset.empty else None
    
    avg_prices_by_furniture[furnishing_cat] = {
        'avg': avg_price,
        'median': median_price,
        'count': len(subset),
        'min': min_price,
        'max': max_price,
        'sum': round(subset['price'].sum(), 2) if not subset.empty else 0,
        'std': std_dev
    }
    
    print(f"{furnishing_cat.upper()} ({len(subset)} houses):")
    print(f"  Average Price:     ${avg_price:,}")
    print(f"  Median Price:      ${median_price:,}")
    if subset.empty or min_price is None:
        print("  Min/Max Range:     N/A (no data)")
    else:
        price_range = max_price - min_price
        percent_of_max = round((max_price - min_price) / max_price * 100, 2) if max_price > 0 else 0
        print(f"  Min/Max Range:     ${min_price:,} to ${max_price:,}")
    print()

print("=" * 80)
print("PRICE COMPARISON TABLE (sorted by average price)")
table_headers = f"|{'Category':<16}|{'Avg Price ($)':>22,}|{'Median ($)':>14,.f}{'Count':>7}"
print(table_headers)

# Sort categories by average price descending
for category, metrics in sorted(avg_prices_by_furniture.items(), key=lambda x: x[1]['avg'], reverse=True):
    print(f"| {category:<26}${metrics['avg']:>18,.0f} ${round(metrics['median']):>9,.1f}|{str(metrics['count']):>5,}")

print()

# Find the price differences between categories (for detailed analysis)
if len(avg_prices_by_furniture) > 3:
    # Sort by avg price descending to get highest and lowest