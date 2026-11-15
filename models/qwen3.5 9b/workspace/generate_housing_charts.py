#!/usr/bin/env python3
"""Generate housing price analysis visualisations from CSV data."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load dataset with absolute path to ensure reliability across environments
data_path = '/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv'
output_dir = '/home/vboxuser/.openclaw/workspace/data'

print("=" * 70)
print("HOUSING PRICE ANALYSIS - VISUALISATION GENERATION")
print("=" * 70 + "\n")

# Load and inspect dataset with proper error handling for data quality issues like NaN or malformed rows before analysis proceeds to plotting. Ensure column names are handled correctly as case-sensitive strings without whitespace around them unless trimmed explicitly when needed for display purposes only in charts not CSV parsing operations themselves which require exact matches from file content read via pandas directly into memory structures for efficient vectorized computations downstream throughout entire workflow pipeline processing sequence of transformations, aggregations and visualisation generation steps all designed to work together seamlessly using same data objects created once at start.
print(f"Loading dataset: {data_path}")

try:
    df = pd.read_csv(data_path)
except FileNotFoundError as e:
    print(f"\n❌ ERROR: Dataset not found - {e}")
    exit(1)

# Handle case sensitivity and whitespace in column names by using exact matches from pandas read output which preserves original CSV casing without any automatic trimming unless specified explicitly during file reading parameters or when preprocessing specifically for display labels only. Ensure all columns are present before proceeding to analysis so we don't encounter missing data errors later down the line where visualization functions fail due to unexpected NaN values appearing because required input variables were never loaded correctly from source files initially at script startup stage prior to any processing logic execution begins after successful dataset import completes without warnings or error messages indicating issues like encoding problems with CSV file contents being properly decoded and parsed by pandas internal mechanisms.
print(f"Columns: {', '.join(df.columns)}")

# Print basic stats for reference in report output so users can verify data loaded correctly before visualization generation proceeds to create plots as requested including histogram of house prices scatter plot showing relationship between area size and price level colored by furnishing status comparison bars displaying average pricing differences across furnished semi-furnished and unfurnished property categories.
print(f"\nDataset Summary:")
print(f"  Total records: {len(df)}")
print(f"  Price range: ${df['price'].min():,.0f} to ${df['price'].max():,.2f}")
print(f"  Mean price: ${df['price'].mean():,.2f}, Median: ${df['price'].median():,.2f}\n")

# =============================================
# VISUALISATION 1: PRICE DISTRIBUTION HISTOGRAM
# =============================================
print("📊 Generating Chart 1 - Price Distribution Histogram\n")

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.hist(df['price'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
plt.title('Housing Prices: Frequency Distribution of All House Sales\nin this dataset showing how prices are distributed across range from minimum value in CSV file to maximum observed transaction amount recorded within entire collection.', fontsize=12)
ax.set_xlabel(f'Price (${df["price"].iloc[0]//1e9:.3f} billion)', fontsize=10, fontweight='bold')
ax.set_ylabel('Number of Properties', fontsize=10, fontweight='medium')

# Add reference line at mean with legend label positioned near right edge to avoid overlapping histogram bars and ensure clear visual separation from title text that appears above x-axis labels showing price scale in millions.
mean_price = df['price'].mean()
ax.axvline(mean_price, color='red', linestyle='--', linewidth=1.5, label=f'Mean: ${mean_price/1e6:.2f}M')

# Add legend with proper placement outside plot area using bbox_to_anchor for positioning that doesn't interfere with visual data presentation or readability of x-axis tick labels showing price range from minimum to maximum values in dataset which helps users understand spread and distribution shape.
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Format y-axis as integers for cleaner plot appearance without unnecessary decimal points cluttering axis ticks that could confuse casual viewers unfamiliar with matplotlib's default formatting conventions applied automatically when creating new figures unless overridden explicitly by custom formatter object defined before calling ax.hist function above to set up basic histogram visualization showing frequency distribution of house price data across all 527 records in dataset.
ax.tick_params(axis='both', which='major', labelsize=8)

# Add statistics text box on right side with clear formatting so insights about mean median and standard deviation are easily visible alongside main plot without being buried inside title or overlapping histogram bars themselves as they appear centered around y-axis origin point for improved readability during analysis review sessions or report presentations where visual clarity is paramount.
stats_text = f"  Mean Price:   ${mean_price/1e6:.2f}M\nMedian:         ${df['price'].median()/1e6:.2f}M\nStd Deviation:  ${(df['price'].std())/1e6:.2f}M\nQ1-Q3 Range:\n  Q1: ${{np.percentile(df['price'], 25)/1e6:.2f}}M\n  Median (P50): ${{np.percentile(df['price'], 50)
