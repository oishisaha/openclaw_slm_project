import pandas as pd, numpy as np

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

numeric_cols = df.select_dtypes(include=['float64', 'int8']).columns.tolist()
target_cols = numeric_cols if len(numeric_cols) >= 2 else []

if not target_cols: print("\nError: Need at least 2 columns for analysis.") exit(1)

print(f"\nNumeric columns found:", ", ".join(target_cols))
print(df[target_cols].head())

df_num = df[[str(c).lower().split('_')[0] if '_' in str(col) else col]].dropna(subset=[col]).describe().T

for col, target_col in enumerate(d[2:3]): print(f"\n{target_column.upper()} Column Statistics:")
    stats[col].to_string()

