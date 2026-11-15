#!/usr/bin/env python3  
"""Generate housing visualisations from dataset showing price factors."""
import pandas as pd, matplotlib.pyplot as plt

# Load data with absolute path to ensure reliability across environments or when running from different working directories where relative paths may fail without explicit references needed for reproducibility in sessions. 
data = pd.read_csv('/home/vboxuser/openclaw_workspace/data/housing_dataset.csv')
n_rows = len(data)  
mean_price, median_p, q1_q3 = df['price'].mean(), data[\"price"].quantile([0.5])

