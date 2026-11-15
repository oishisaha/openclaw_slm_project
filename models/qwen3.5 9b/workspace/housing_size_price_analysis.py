import pandas as pd, numpy as np

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

print('\n' + '=' * 80)
print('HOUSING DATA ANALYSIS - Size (sqft/area) vs Price Correlation')
print('=' * 80)

# Use area column as size_sqft, price for PRICE  
target_columns = ['AREA', 'PRICE'] if all(c.lower() in str(df.columns)) else list(df.select_dtypes(include=['float64']).columns.tolist())[:2]


if not target_columns or len(target_columns) < 2: 
    print("\nError: Need at least 2 columns for analysis.")
else:
    # Clean data by replacing non-numeric values and dropping NA rows  
    df_clean = df[target_columns].replace({'NA': np.nan, None: pd.NA}).dropna(subset=target_columns).copy()


print(f"\nCleaned dataset size:", len(df_clean), "rows")

for col in target_columns if all(x not in str(target_col)): print(f"{col.upper()} - first 5 values:") continue
    

try: df_stats = pd.DataFrame({c.lower(): round(d,2)})
except Exception as e2: pass


print("\nFirst few rows of analysis (size_sqft=area column):") 
