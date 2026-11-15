import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('data/housing_dataset.csv')

print("=" * 60)
print("HOUSING DATASET EXPLORATION REPORT")
print("=" * 60)

print("\n--- FILE METADATA ---")
rows, cols = df.shape

file_size_bytes = (df.memory_usage(deep=True).sum()) / (1024**2)):.2f
print(f"File path: data/housing_dataset.csv")
print(f"Number of rows (records): {num_rows:,}")
print(f"Number of columns (features): {cols,}")
print(f"\nColumn Names:")

for i in range(1)]])


column_info = []

missing_values_summary = []

# Analyze each column
total_missing_values_count = 0)
