import pandas as pd, numpy as np

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft/area) vs Price Correlation")
print("=" * 80)


# Use area column as size_sqft, price for PRICE  
numeric_cols = ['AREA', 'PRICE'] if all(c.lower() in str(df.columns)) else list(df.select_dtypes(include=['float64']).columns.tolist())[:2]

if len(numeric_cols): 
    print("\nNumeric columns found:", ", ".join([str(col) for col in numeric_cols]))
    
print("First 10 rows of size_sqft (area, price)")

