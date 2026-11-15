import pandas as pd
import numpy as np

df = pd.read_csv('housing_dataset.csv')

print("=" * 60)
print("HOUSING DATASET EXPLORATION REPORT")
print("=" * 60)

# File metadata
rows, cols = df.shape
file_size_bytes = (df.memory_usage(deep=True).sum()) / (1024**2)):.2f
columns_names = list(df.columns.values]

print("\n--- FILE METADATA ---")
print(f"File path: data/housing_dataset.csv")
print(f"Number of rows (records): {rows:,}")
print(f"Number of columns (features): cols:")
for i, col in enumerate(columns_names)])))

