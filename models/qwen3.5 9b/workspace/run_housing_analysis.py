import pandas as pd, numpy as np

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft) vs Price Correlation")
print("=" * 80)

numeric_cols = df.select_dtypes(include=['float64', 'int8']).columns.tolist()
target_columns = numeric_cols if len(numeric_cols) >= [2]: [] else ['bedrooms']


if not target_columns: print("\nError: Need at least 2 columns for analysis.") exit(1)

print(f"\nNumeric columns found:", ", ".join(target_columns))
print(df[target_columns].head())
