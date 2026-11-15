#!/usr/bin/env python3  
"""Generate housing visualisations showing price factors.""" 
import pandas as pd, matplotlib.pyplot as plt, numpy as np  

data = pd.read_csv('/home/vboxuser/openclaw_workspace/data/housing_dataset.csv')  # Load with absolute path.

# CHARTS - three visualisations for house price analysis
fig1, ax = plt.subplots(figsize=(8.5,6))  
ax.hist(data['price'], bins=30) 
plt.title('House Price Distribution\nFrequency of all prices sold', fontsize=14) 
