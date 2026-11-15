#!/usr/bin/env python3
"""Calculate correlation of numerical features with house price."""
from sklearn.preprocessing import StandardScaler

# Read the dataset
print("Loading housing data...")
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')
print(f"Dataset shape: {df.shape}")
print(f"\nColumns in dataset:")
for col in df.columns:
    print(f"  - {col}: dtype={dtype(df[col])}, unique values count = (if categorical)")

# Identify numerical columns (excluding price)
from sklearn.preprocessing import StandardScaler

# Get dtypes for each column
print("\nCategorical features:")
cat_cols = []
num_cols = []

for col in df.columns:
    if df[col].dtype == 'object':
        cat_cols.append(col)
    else:
        num_cols.append(col)

print(f"\nNumerical columns ({len(num_cols)}): {num_cols}")
print(f"Categorical columns ({len(cat_cols)}): {cat_cols}")

# Calculate correlation of each numerical feature with price
correlations = {}
for col in num_cols:
    corr = df[col].corr(df['price'])
    correlations[col] = round(corr, 4)

print("\nCorrelation coefficients (absolute value ranking):\n")
sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)

# Create display table
display_data = []
for col, corr in sorted_corr:
    direction = "positive" if corr > 0 else "negative"
    strength = str(abs(corr))[:3].ljust(5)
    print(f"{col:20s} {direction:>10s} | r={corr:+.4f}")
