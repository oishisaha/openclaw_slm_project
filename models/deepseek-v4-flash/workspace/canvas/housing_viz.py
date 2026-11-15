import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Load data ──────────────────────────────────────────────────────────────
df = pd.read_csv("data/housing_dataset.csv")
print(f"Rows: {len(df)}, Columns: {list(df.columns)}")

# ── 1. Price Distribution ───────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

prices = df['price'].values
ax.hist(prices, bins=30, color='steelblue', edgecolor='white', alpha=0.85, density=True)

# KDE manually
from scipy.stats import gaussian_kde
kde = gaussian_kde(prices)
x_grid = np.linspace(prices.min(), prices.max(), 200)
ax.plot(x_grid, kde(x_grid), color='darkblue', lw=2, label='Density (KDE)')

median_price = np.median(prices)
mean_price = np.mean(prices)
ax.axvline(median_price, color='red', ls='--', lw=1.5, label=f'Median: {median_price:,.0f}')
ax.axvline(mean_price, color='darkorange', ls='--', lw=1.5, label=f'Mean: {mean_price:,.0f}')
ax.set_title('House Price Distribution', fontsize=14)
ax.set_xlabel('Price (currency units)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend(fontsize=10)
plt.tight_layout()
fig.savefig('canvas/price_distribution.png')
plt.close()
print("✅ Saved price_distribution.png")

# ── 2. Area vs Price Scatterplot ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

area = df['area'].values
price = df['price'].values
bedrooms = df['bedrooms'].values

scatter = ax.scatter(area, price, c=bedrooms, cmap='viridis', alpha=0.7,
                     edgecolors='w', linewidth=0.3)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Bedrooms')
ax.set_title('Area vs Price (coloured by bedrooms)', fontsize=14)
ax.set_xlabel('Area (sq ft)', fontsize=12)
ax.set_ylabel('Price (currency units)', fontsize=12)

# Trend line
idx = np.argsort(area)
z = np.polyfit(area, price, 1)
p = np.poly1d(z)
ax.plot(area[idx], p(area[idx]), 'r--', lw=2, alpha=0.7, label='Trend line')
ax.legend()
plt.tight_layout()
fig.savefig('canvas/area_vs_price_scatter.png')
plt.close()
print("✅ Saved area_vs_price_scatter.png")

# ── 3. Average Price by Furnishing Status ───────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))

order = ['unfurnished', 'semi-furnished', 'furnished']
grouped = df.groupby('furnishingstatus')['price'].agg(['mean', 'std', 'count'])
grouped = grouped.reindex(order)

colors = ['#e74c3c', '#f39c12', '#2ecc71']
bars = ax.bar(grouped.index, grouped['mean'].values, color=colors, edgecolor='gray', width=0.5)
ax.set_title('Average House Price by Furnishing Status', fontsize=14)
ax.set_xlabel('Furnishing Status', fontsize=12)
ax.set_ylabel('Average Price (currency units)', fontsize=12)

# Annotations
for i, (idx, row) in enumerate(grouped.iterrows()):
    ax.text(i, row['mean'] + 150000, f"{row['mean']:,.0f}\n(n={int(row['count'])})",
            ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
fig.savefig('canvas/avg_price_by_furnishing.png')
plt.close()
print("✅ Saved avg_price_by_furnishing.png")
print("🎉 All done!")