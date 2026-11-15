import pandas as pd

df = pd.read_csv('data/housing_dataset.csv')

print("=" * 60)
print("HOUSING DATASET EXPLORATION REPORT")
print("=" * 60)

num_rows, num_cols = df.shape
column_names = list(df.columns.values)
