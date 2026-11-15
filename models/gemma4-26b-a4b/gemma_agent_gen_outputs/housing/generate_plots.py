import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('data/housing_data.csv')

# Set visual style
sns.set_theme(style="whitegrid")

# 1. Price distribution histogram
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=30, kde=True, color='blue')
plt.title('Distribution of House Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.savefig('price_distribution.png')
plt.close()

# 2. Area vs Price scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='area', y='price', alpha=0.6)
plt.title('Area vs House Price')
plt.xlabel('Area (sq ft)')
plt.ylabel('Price')
plt.savefig('area_vs_price.png')
plt.close()

# 3. Bar chart of average price by furnishing status
plt.figure(figsize=(10, 6))
avg_price_furnishing = df.groupby('furnishingstatus')['price'].mean().reset_index()
sns.barplot(data=avg_price_furnishing, x='furnishingstatus', y='price', palette='viridis')
plt.title('Average Price by Furnishing Status')
plt.xlabel('Furnishing Status')
plt.ylabel('Average Price')
plt.savefig('avg_price_furnishing.png')
plt.close()

print("Visualizations generated successfully.")
