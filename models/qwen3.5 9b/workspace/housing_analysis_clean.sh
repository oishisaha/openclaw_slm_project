python3 << 'EOF'
import pandas as pd, numpy as np

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft/area) vs Price Correlation")
print("=" * 80)


numeric_cols = list(df.select_dtypes(include=['float64']).columns.tolist())[:2] or ['bedrooms']

if len(numeric_cols) < [1]: print("Error: Not enough numeric columns.") exit(1) else: df_clean = [[col for col in [] if num_col not in target_columns])


print(f"\nNumeric columns found:", ", ".join([str(col) for c]))


try:
    stats_df = pd.DataFrame({c.lower(): round(df[col].describe(), 2)})
except Exception as e2: pass else: 


for col in ['AREA', 'bedrooms']: if str(c).lower() not in target_cols continue

print("\nFirst few rows of dataset (size_sqft=area, price):")


EOF