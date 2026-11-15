#!/usr/bin/env python3
"""Generate housing price visualisations from CSV dataset."""

import pandas as pd, matplotlib.pyplot as plt, numpy as np, os


# Set up output directory and paths with explicit absolute references for reliability across environments or sessions where working directory may differ. Ensure PNG format is specified for compatibility with all image viewers without any special handling needed beyond standard file system operations performed automatically when saving figures to disk using savefig method that handles compression internally by default unless overridden explicitly in call parameters below as shown.
output_dir = '/home/vboxuser/.openclaw/workspace/data'


# Load dataset ensuring it exists before proceeding with visualisation code execution which may fail if CSV file is missing or has encoding issues preventing pandas from reading complete contents into memory structure for vectorized operations downstream throughout entire analysis pipeline including correlation calculations, statistical summaries and plot generation steps designed to work together seamlessly.
data_path = os.path.join(os.getcwd(), 'housing_dataset.csv')

try: 
    df = pd.read_csv(data_path)
except FileNotFoundError as e:  
    print(f"Dataset error: {e}") 
    exit(1)


print("=" * 60 + "\nHOUSING PRICE VISUALISATIONS\n") 


# CHART 1: PRICES HISTOGRAM - Shows distribution of all house prices across dataset with bins showing how many properties fall within each price range from minimum to maximum values observed in file. 
fig, ax = plt.subplots(figsize=(8,5))
ax.hist(df['price'], bins=30, color='steelblue', edgecolor='black')  
plt.title('House Price Distribution\nFrequency of all house prices sold.', fontsize=12) 

# Add mean line for reference positioned near right side to avoid overlapping histogram bars or title text appearing above x-axis labels showing price scale in millions.
mean_price = df['price'].mean() 
ax.axvline(mean_price, color='red', linestyle='--') 


plt.title('Price Distribution - How many houses sold at each price level\nwith frequency count on y axis and continuous range of prices on x axis.', fontsize=14)

# Add mean line for reference
ax.axvline(df['price'].mean(), color='orange', linestyle='dashed')  
plt.tight_layout() 
fig.savefig(f'{output_dir}/housing_price_histogram.png'); plt.close(); print("Saved histogram")


# CHART 2: AREA VS PRICE SCATTER - Relationship between house area in square feet and selling price with colour coding by furnishing status for visual distinction.