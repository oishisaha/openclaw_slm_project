

#!/usr/bin/env python3
"""Calculate correlation of numerical features with house price."""
import pandas as pd

# Read the dataset
print("=" * 70)
print("HOUSING DATA CORRELATION ANALYSIS")
print("=" * 70)
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')

print(f"\nDataset shape: {df.shape[0]} rows × {df.shape[1]} columns\n")

# Get all features except price column  
price_col = 'price'
all_features = [col for col in df.columns if col != price_col]

# Calculate correlation of each feature with house_price
correlations = {}
for feature in all_features:
    corr_value = round(df[feature].corr(df['price']), 4)
    correlations[feature] = corr_value
    
# Sort by absolute correlation value (strength of relationship, highest first)
sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)

print("\n" + "=" * 70)
print("NUMERICAL FEATURES RANKED BY CORRELATION STRENGTH WITH PRICE")
print("=" * 70)
print(f"\n{'Rank':<6} {'Feature Name':<35} {'Correlation Coeff.':<18}")

for rank, (feature_name, correlation_value) in enumerate(sorted_correlations, start=1): 
    direction = "positive" if correlation_value > 0 else "negative"
    
print(f"{rank:<6}{feature_name:<42.5f}", end='')  
