#!/usr/bin/env python3  
"""Generate housing price visualisations from dataset CSV file showing factors affecting house prices."""

import pandas as pd, matplotlib.pyplot as plt, numpy as np 

data = pd.read_csv('housing_dataset.csv')  # Load data with columns: price area bedrooms bathrooms stories mainroad guestroom basement hotwaterheating airconditioning parking prefarea furnishingstatus - already numeric except categorical fields needing mapping for visualization output files saved as PNG. 
print(f"Loaded {len(data)} rows.")

# Get descriptive stats
mean = data['price'].mean()  
median_price = df[\"price\"].quantile(0.5) if hasattr(df, 'quantile') else None 
q1,q3=data.quantile([25/1e6,.75/1e6])

print(f"Stats: Min={data.price.min()}, Max=${max(data['price'].values)}, Mean=$/{mean}M")

