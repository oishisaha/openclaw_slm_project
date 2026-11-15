#!/bin/bash\n# Generate housing price visualisations\ncd /home/vboxuser/.openclaw/workspace && python3 << 'EOF'\nimport pandas as pd, matplotlib.pyplot as plt, numpy as np

df = pd.read_csv('data/housing_dataset.csv')  
print(f\"Loaded {len(df)} records. Price: ${df['price'].min():,.0f}-${df['price'].max():,.0f}\")\n\n# 1. HISTOGRAM - frequency distribution of all house prices across dataset with mean line and statistics displayed on right side for easy reference during analysis review.\
fig, ax = plt.subplots(figsize=(8,5)) \
ax.hist(df['price'], bins=30, color='steelblue', edgecolor='black')\nplt.title('House Price Distribution\nFrequency of all prices in dataset.', fontsize=14)\nav=ax.axvline(df['price'].mean(), linestyle='--', label=f'Mean ${df[\"price\"].mean()/1e6:.2f}M'); ax.legend(); \nstax.text(0.98, 0.97,f\"Mean: ${{df['price'].mean()
