#!/usr/bin/env python3  
"""Generate housing visualisations showing price factors."""
import pandas as pd, matplotlib.pyplot as plt, numpy as np

data = pd.read_csv('housing_dataset.csv')  # Load CSV from data/ folder. 
print(f"Loaded {len(data)} rows") 

# STATS FOR INSIGHTS  
mean_p, median_price = df['price'].mean(), df[\"price\"].median()
q1,q3=data.quantile([25,.75])
