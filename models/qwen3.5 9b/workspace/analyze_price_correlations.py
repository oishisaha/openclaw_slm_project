

#!/usr/bin/env python3
"""Calculate correlation of numerical features with house price."""
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Read the dataset
print("=" * 70)
print("HOUSING DATA CORRELATION ANALYSIS")
print("=" * 70)
print(f"\nLoading housing data...")
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')

print(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
print("\nColumn types:")
for col in df.columns[:5]:  # Show first few only to save space
    print(f"\t{col}: {str(df[col].dtype)}")

# Identify numerical vs categorical
num_cols = []
cat_cols = []

for col, dtype in df.dtypes.items():
    if pd.api.types.is_numeric_dtype(dtype):
        num_cols.append(col)
    else:
        cat_cols.append(col)

print(f"\nNumerical columns ({len(num_cols)}):\t{num_cols}")
print(f"Categorical columns\t({len(cat_cols)})\t:{cat_cols}\n")    

# Calculate correlation of each numerical feature with price
correlations = {}
for col in num_cols:
    corr = df[col].corr(df['price'])
    correlations[col] = round(corr, 4)

print("\n" + "=" * 70)
print("RANKED CORRELATION COEFFICIENTS WITH HOUSE PRICE")
print("=" * 70)

# Sort by absolute correlation value (strength of relationship)
sorted_corr_abs = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)

print(f"\n{'RANK':<6} {'FEATURE':<25} 'DIRECTION':<10} COEFFICIENT']})  
for i, (col, corr) in enumerate(sorted_corr_abs):
    direction_str = "pos" if corr > 0 else r'neg'"
    
print(f"\n{'+' * 70}")
