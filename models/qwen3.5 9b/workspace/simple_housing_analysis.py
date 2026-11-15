import pandas as pd

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft) vs Price")
print("=" * 80)

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

# Identify size_sqft column and price column from dataset 
target_cols = ['bedrooms', 'price'] if all(str(col).lower() in df.columns): [str(c)] else []: print("Columns:", ", ".join(target_cols)) continue
    
if not target_cols or len([c]) < 2: "Need at least 2 columns for correlation analysis." except Exception as e

df['bedrooms'].describe().T
print("\nFirst 10 rows (size_sqft, price):")
