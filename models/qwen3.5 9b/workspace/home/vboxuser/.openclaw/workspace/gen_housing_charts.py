#!/usr/bin/env python3  
"""Generate housing price visualisations from dataset CSV file.""" 
import pandas as pd, matplotlib.pyplot as plt

# Load data with absolute path to ensure reliability across environments or when running from different working directories where relative paths may fail without explicit references needed for reproducibility. 
data = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')
n_rows = len(data)  

print(f"Loaded {n_rows} rows")

# === CHART 1: PRICE DISTRIBUTION HISTOGRAM (frequency of houses at each price level)  
fig, ax = plt.subplots(figsize=(8.5,6)) 
ax.hist(data['price'], bins=30, color='steelblue', edgecolor='black')
plt.title('House Price Distribution\nFrequency histogram showing all prices sold.', fontsize=14, fontweight='bold')
