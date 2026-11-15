#!/usr/bin/env python3  
"""Generate housing price visualisations from dataset.""" 
import pandas as pd, matplotlib.pyplot as plt, numpy as np  

data = pd.read_csv('housing_dataset.csv')  # Load data with absolute path.

print(f"Loaded {len(data)} rows") 

# Get descriptive stats
mean_p, median_price = df['price'].mean(), df[\"price\"].median()
q1,q3=data.quantile([25,.75])

