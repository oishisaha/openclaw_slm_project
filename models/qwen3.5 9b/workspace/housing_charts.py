#!/usr/bin/env python3
"""Generate housing price analysis visualisations."""
import pandas as pd, matplotlib.pyplot as plt, numpy as np

df = pd.read_csv('data/housing_dataset.csv')

# VISUALISATION 1: PRICE DISTRIBUTION HISTOGRAM
fig, ax = plt.subplots(figsize=(8,5))
ax.hist(df['price'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
plt.title('House Price Distribution\nFrequency of all house prices in dataset')
ax.set_xlabel(f'Price ($ {df["price"].iloc[0]//1e9:.2f}B range)\nfrom minimum to maximum values observed.')
ax.set_ylabel('Count')
mean = df['price'].mean(); median = df['price'].median()
stats = f'Mean:\${{mean/1e6:.2f}}M  Median:\${{median/1e6:.2f}}M'
ax.text(0.98, 0.95, stats, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right')

plt.tight_layout()
fig.savefig('data/housing_price_histogram.png'); print("Saved: housing_price_histogram.png"); plt.close()

