import pandas as pd

# Load the dataset
df = pd.read_csv('data/housing_data.csv')

# 1. Encode furnishingstatus: furnished=2, semi-furnished=1, unfurnished=0
status_map = {'furnished': 2, 'semi-furnished': 1, 'unfurnished': 0}
df['furnishingstatus'] = df['furnishingstatus'].map(status_map)

# 2. Encode all yes/no columns as binary (yes=1, no=0)
# Identify yes/no columns
yes_no_cols = [col for col in df.columns if df[col].dtype == 'object' and set(df[col].unique()).issubset({'yes', 'no'})]

for col in yes_no_cols:
    df[col] = df[col].map({'yes': 1, 'no': 0})

# 3. Normalize price and area columns using min-max scaling
def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())

df['price'] = min_max_scale(df['price'])
df['area'] = min_max_scale(df['area'])

# Calculate means
mean_norm_price = df['price'].mean()
mean_norm_area = df['area'].mean()

print(f"mean_norm_price: {mean_norm_price:.4f}")
print(f"mean_norm_area: {mean_norm_area:.4f}")
