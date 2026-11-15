import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Read the data
df = pd.read_csv('data/housing_dataset.csv')

print("Original data:")
print(df.head())
print(f"\nTotal rows: {len(df)}")

# Encode furnishingstatus column (furnished=2, semi-furnished=1, unfurnished=0)
def encode_furnish(status):
    if status == 'furnished':
        return 2
    elif status == 'semi-furnished':
        return 1
    elif status == 'unfurnished':
        return 0

df['furnishingstatus'] = df['furnishingstatus'].apply(encode_furnish)

# Encode yes/no columns as binary (yes=1, no=0)
for col in ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']:
    if col in df.columns:
        def encode_yes_no(val):
            return 1 if val == 'yes' else 0
        df[col] = df[col].apply(encode_yes_no)

# Normalise price and area columns using min-max scaling (scale to [0,1])
scaler_price = MinMaxScaler()
df['norm_price'] = scaler_price.fit_transform(df[['price']].values).flatten()

scaler_area = MinMaxScaler()
df['norm_area'] = scaler_area.fit_transform(df[['area']].values).flatten()

# Calculate means of normalised columns
mean_norm_price = df['norm_price'].mean()
mean_norm_area = df['norm_area'].mean()

print("\nPreprocessed data:")
print(f"Mean of normalized price: {mean_norm_price:.4f}")
print(f"Mean of normalized area: {mean_norm_area:.4f}")

# Save preprocessed dataframe for reference
df.to_csv('data/housing_preprocessed.csv', index=False)
print("\nPreprocessed data saved to housing_preprocessed.csv")
