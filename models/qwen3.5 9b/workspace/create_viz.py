import pandas as pd, matplotlib.pyplot as plt, numpy as np

data = pd.read_csv('housing_dataset.csv')  # Load data from CSV in workspace. 
n_rows = len(data)  
mean_p = df['price'].mean() if hasattr(df,'mean') else None 
