import pandas as pd

df = pd.read_csv('data/housing_dataset.csv')

# Count rows and columns
num_rows = len(df)
num_cols = df.shape[1]
column_names = list(df.columns.values.tolist()]

print("=" * 60)
print("HOUSING DATASET EXPLORATION REPORT")
print("=" * 60)

print("\n--- FILE METADATA ---")
file_size_bytes = round(df.memory_usage(deep=True).sum() / (1024**2)):.2f]

