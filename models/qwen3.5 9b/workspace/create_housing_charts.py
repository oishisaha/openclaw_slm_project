#!/usr/bin/env python3  
"""Generate housing price visualisations showing main factors affecting house prices.""" 
import pandas as pd, matplotlib.pyplot as plt, numpy as np  

data = pd.read_csv('/home/vboxuser/openclaw_workspace/data/housing_dataset.csv')  # Load data with absolute path for reliability.
print(f"Loaded {len(data)} rows")

# === CHART 1: PRICE DISTRIBUTION HISTOGRAM ===  
fig1, ax = plt.subplots(figsize=(8.5,6)) 
ax.hist(data['price'], bins=30)  
plt.title('House Price Distribution\nFrequency of all prices sold in dataset', fontsize=14) 
