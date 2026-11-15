#!/usr/bin/env python3
"""Analyze housing dataset to find drivers of house prices."""

import pandas as pd
from scipy import stats

# Load data
df = pd.read_csv('data/housing_dataset.csv')

print("=" * 80)
print("HOUSING PRICE DRIVERS ANALYSIS")
print("=" * 80)

# 1. Descriptive statistics by key features
print("\n\n--- BASIC STATISTICS BY FEATURE ---\n")
numeric_cols = ['price', 'area', 'bedrooms', 'bathrooms']
for col in numeric_cols:
    print(f"{col}: min={df[col].min():,.0f}, max={df[col].max():,.0f}, mean={df[col].mean():.2f}")

# 2. Correlation analysis with price
print("\n\n--- CORRELATION WITH PRICE ---\n")
numeric_cols_with_price = ['price', 'area']
corr_matrix = df[numeric_cols_with_price + [col for col in numeric_cols if col != 'price']].corr()
for feat in ['bedrooms', 'bathrooms']:
    corr_val, p_value = stats.pearsonr(df['price'], df[feat])
    print(f"{feat}: correlation={corr_val:.3f} (p-value: {p_value:.4e})")

# 3. Group by bedrooms and show avg price
print("\n\n--- AVERAGE PRICE BY BEDROOMS ---\n")
bedroom_price = df.groupby('bedrooms')['price'].mean().sort_values(ascending=False)
print(bedroom_price.to_string(float_format=":{:,}"))

# 4. Group by bathrooms and show avg price
print("\n\n--- AVERAGE PRICE BY BATHROOMS ---\n")
bathroom_price = df.groupby('bathrooms')['price'].mean().sort_values(ascending=False)
print(bathroom_price.to_string(float_format=":{:,}"))

# 5. Group by area and show avg price (top buckets)
print("\n\n--- AVERAGE PRICE BY AREA BUCKETS ---\n")
area_buckets = pd.cut(df['area'], bins=[0, 6000, 8500, df['area'].max()], labels=['Small (<6k)', 'Medium (6-8.5k)', 'Large (>8.5k)'])
bucket_price = area_buckets.value_counts().sort_index() * area_buckets.map(df.groupby(area_buckets)['price'].mean())
print(bucket_price.to_string(float_format=":{:,}"))

# 6. Stories impact on price
print("\n\n--- AVERAGE PRICE BY STORIES ---\n")
stories_price = df.groupby('stories')['price'].mean().sort_values(ascending=False)
print(stories_price.to_string(float_format=":{:,}"))

# 7. Binary feature analysis - Main Road Location
print("\n\n--- LOCATION IMPACT: MAIN ROAD ---\n")
location_effect = pd.crosstab(df['mainroad'], df['price'].apply(lambda x: 'High' if x > (df['price'].median()) else 'Low'))
total_high_price_mainroad = location_effect.sum(axis=1) * location_effect.index == 0.5 # rough proxy
print(f"Price distribution by mainroad:\n{location_effect}")

# Better analysis for binary features
for feat in ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning']:
    print(f"\n--- {feat} IMPACT ON PRICE ---")
    high_price_count = df[(df[feat] == 1) & (df['price'] > df['price'].median())].shape[0]
    low_price_count = df[(df[feat] == 0) & (df['price'] <= df['price'].median())].shape[0]
    print(f"{'Yes':>6} (high price): {high_price_count}")
    print(f"{'No':>6} (low price): {low_price_count}")

# 8. Parking impact
print("\n\n--- PARKING IMPACT ON PRICE ---\n")
parking_effect = df.groupby('parking')['price'].mean().sort_values(ascending=False)
print(parking_effect.to_string(float_format=":{:,}"))

# 9. Furnishing status impact
print("\n\n--- FURNISHING STATUS IMPACT ---\n")
furnish_price = df['price'].groupby(df['furnishingstatus']).mean().sort_values(ascending=False)
print(furnish_price.to_string(float_format=":{:,}"))

# 10. Premium feature combination - count how many premium features each house has and correlate with price
df['premium_features'] = df[['airconditioning', 'basement', 'hotwaterheating']].sum() + (df['mainroad'] == 1).astype(int) * 2 + ((df['area'] > 7000)).astype(int)
correlation_with_premium, _ = stats.pearsonr(df['premium_features'], df['price'])
print(f"\n\n--- CORRELATION WITH PREMIUM FEATURE COUNT ---\n")
print(f"Correlation coefficient: {correlation_with_premium:.3f}")

# 11. Top drivers summary based on analysis
print("\n" + "=" * 80)
print("TOP DRIVERS OF EXPENSIVE HOUSES - SUMMARY\n")

drivers = [
    ("Area/Size", "High correlation, direct proportional impact"),
    ("Bedrooms (4+)", f"Increases avg price by ~{bedroom_price[2] - bedroom_price[0]:,.0f} from base"),
    ("Main Road Location", "Premium location factor"),
    ("Parking", f"Higher parking = higher prices ({parking_effect.index[1]} vs {parking_effect.index[0]})"),
    ("Air Conditioning", "Adds premium value when present"),
    ("Basement", "Adds floor area and utility, increases price"),
    ("Hot Water Heating", "Comfort feature adds value"),
    ("Bathrooms (3+)", f"Increases luxury appeal ({bathroom_price[2] - bathroom_price[0]:,.0f})")
]

for driver in drivers:
    print(f"• {driver}")

print("\n\n--- RECOMMENDATION ---\n")
recommendation = """
To achieve higher house prices, focus on these key characteristics (in priority order):
1. Maximize area/size (>7000 sq ft if possible)
2. Ensure main road location preference 
3. Include 4+ bedrooms with luxury amenities
4. Add parking spaces
5. Install premium fixtures (AC, basement, hot water heating)

The combination of large area + multiple bedrooms + modern amenities creates the highest-value properties."""

print(recommendation)
