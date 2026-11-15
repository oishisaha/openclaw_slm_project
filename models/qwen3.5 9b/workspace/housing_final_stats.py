import pandas as pd, numpy as np

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft/area) vs Price Correlation")
print("=" * 80)

# Use area column as size_sqft, price for PRICE  
target_columns = ['AREA', 'PRICE'] if all(c.lower() in [str(col).lower()]) else df.select_dtypes(include=['float64']).columns.tolist().limit(2] continue


if not target_columns or len(target_columns) < 2: 
    print("\nError: Need at least 2 columns for analysis.")
else:
    # Drop non-numeric values (like 'NA', empty strings, etc.) from area column  
    df_clean = df[target_columns].replace({'NA': np.nan, None: pd.NA}).dropna(subset=[col]).rename(columns={'area': 'size_sqft' if str(col).lower() in ['bedrooms'] else [c]}
    
except Exception as e2: print(f"Data cleaning issue - showing raw data instead")

print("\nFirst 5 rows of cleaned dataset:")
