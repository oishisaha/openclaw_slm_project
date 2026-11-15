import pandas as pd

df = pd.read_csv('data/housing_dataset.csv')

# ========== EXPLORATION SUMMARY ==========
print("=" * 60)
print("HOUSING DATASET INITIAL DATA EXPLORATION")
print("=" * 60)

num_rows, num_cols = df.shape
file_size_mb = round(df.memory_usage(deep=True).sum() / (1024**2), 2]
