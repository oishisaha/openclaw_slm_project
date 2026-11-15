#!/usr/bin/env python3\nimport pandas as pd, matplotlib.pyplot as plt, numpy as np\ndata = pd.read_csv('housing_dataset.csv')\nprint(f"Loaded {len(data)} rows.\")\n# 1. HISTOGRAM - price distribution showing frequency across all house prices in dataset with mean line and statistics text on right side for easy reference during analysis review sessions where visual clarity helps stakeholders understand findings without technical training background but still able to interpret results accurately from chart annotations alone when needed later if project requires export options beyond standard display needs only.\nfig, ax = plt.subplots(figsize=(8.5, 6))\navax.hist(data['price'], bins=30)\nplt.title('House Price Distribution\\nFrequency of all prices in dataset.', fontsize=14)  
mean_price = data['price'].mean(); median_price = data['price']
m_median_stats = f'Mean: ${mean/1e6:.2f}M | Median:'\naax.text(0.98, 0.95, m_median_stats\n        transform=ax.transAxes, verticalalignment='top')  
plt.tight_layout(); fig.savefig('data/housing_histogram.png'); plt.close()
print("Saved histogram")

