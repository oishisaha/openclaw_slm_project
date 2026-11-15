#!/usr/bin/env python3
"""Generate housing price analysis visualisations."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
df = pd.read_csv('data/housing_dataset.csv')

print("=" * 60)
print("HOUSING PRICE ANALYSIS - Visualisation Generation")
print("=" * 60)
print(f"\nDataset: {len(df)} housing records loaded.")
print(f"Price range: ${df['price'].min():,.2f} to ${df['price'].max():,.2f}")

# =============================================
# 1. PRICE DISTRIBUTION HISTOGRAM
# =============================================
print("\n📊 Generating Price Distribution Histogram...")

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['price'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
ax.set_title('Housing Prices - Frequency Distribution\nHistogram of all house prices in dataset')
ax.set_xlabel(f'Price ($ {df["price"].iloc[0]//1e9:.3f} billion range)')
ax.set_ylabel('Frequency (Count)')
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Add statistics text box
stats_text = f"Mean Price: ${df['price'].mean():,.2f}\nMedian: ${df['price'].median():,.2f}\nStd Dev: ${df['price'].std():,.2f}"
props = {'color': 'white', 'fontweight': 'bold'}
ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right', bbox=dict(boxstyle="round,pad=0.3", facecolor="rgba(255,255,255,0.8)"), **props)

plt.tight_layout()
plt.savefig('data/housing_price_histogram.png', dpi=150, format='png')
print(f"✅ Saved: data/housing_price_histogram.png")
plt.close()

# =============================================
# 2. AREA VS PRICE SCATTER PLOT
# =============================================
print("\n📈 Generating Area vs Price Scatter Plot...")

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df['area'], df['price'] / 1e7, c=df['furnishingstatus'].map({
    'unfurnished': '#d32f2f',   # Red for unfurnished
    'semi-furnished': '#fb8c00','# Green for furnished
}).fillna('#9e9e9e'), alpha=0.6, edgecolors='k')

ax.set_xlabel(f'House Area (sq ft) - Mean: {df["area"].mean():,.1f}')
ax.set_ylabel('Price ($ millions)', color='#333')
plt.title('House Price vs Living Area\nColored by Furnishing Status', fontweight='bold')

# Add trend lines for each furnishing status using numpy polyfit
for furn, label in sorted(df['furnishingstatus'].unique()):
    subset = df[df['furnishingstatus'] == furn]
    if len(subset) > 2:
        z = np.polyfit(subset['area'], subset['price']/1e7, 1)
        p = z[0]*subset['area'] + z[1]
        ax.plot(min(df['area']), min(p), max(df['area']], max(p], 
                '--', alpha=0.5, color='#69b3a2')

# Add correlation and stats text box on the left side with a neutral background for better readability
ax.text(0.01, 0.98, f'Trend: Larger areas command higher prices\nTrend lines shown across all furnishing statuses', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left', bbox=dict(boxstyle="round,pad=0.3", facecolor="#f5f5dc"), alpha=0.9)

plt.grid(True, alpha=0.3)
ax.set_rasterized=True  # Smooth the scatter for performance with many points
fig.colorbar(scatter, ax=ax, label='Furnishing Status')
plt.tight_layout()
plt.savefig('data/housing_area_price_scatter.png', dpi=150, format='png')
print(f"✅ Saved: data/housing_area_price_scatter.png")
plt.close()

# =============================================
# 3. BAR CHART OF AVERAGE PRICE BY FURNISHING STATUS
# =============================================
print("\n📊 Generating Bar Chart - Average Price by Furnishing Status...")

avg_prices = df.groupby('furnishingstatus')['price'].mean().sort_values(ascending=False)
colors = {'unfurnished': '#d32f2f', 'semi-furnished': '#fb8c00', 'furnished': '#4caf50'}

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(avg_prices.index.str.title(), avg_prices.values / 1e7, color=[colors[s] for s in avg_prices.index], edgecolor='black', alpha=0.8)

ax.set_title('Average House Price by Furnishing Status\nComparison across unfurnished, semi-furnished, and furnished properties')
ax.set_xlabel(f'Furnishing Status (Mean Area: {df["area"].mean():,.1f} sq ft)\nHigher-priced furnishes indicate more premium positioning.')
ax.set_ylabel('Price ($ millions)')
plt.xticks(rotation=45, ha='right')

# Add value labels on bars with precise formatting for clarity
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x(), height + 0.18 / len(df['price']), f'${height:.2f}M', 
            ha='center', va='bottom', color='black', fontsize=9, fontweight='bold')

# Add mean price statistics text on top-right with clear label and value
stats_text = f'Mean Price by Status: Unfurnished ${avg_prices["Unfurnished"].mean():,.2f} vs Furnished ${avg_prices["Furnished"].mean():,.2f}'
props = {'color': 'white', 'fontweight': 'bold'}
ax.text(0.98, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top', horizontalalignment='right', bbox=dict(boxstyle="round,pad=0.3", facecolor="rgba(255,255,255,0.7)"), **props)

plt.tight_layout()
plt.savefig('data/housing_furnishing_avg_price.png', dpi=150, format='png')
print(f"✅ Saved: data/housing_furnishing_avg_price.png")
plt.close()

# =============================================
# SUMMARY AND INSIGHTS
# =============================================
print("\n📝 KEY INSIGHTS FROM VISUALISATIONS:\n")
print("1. PRICE DISTRIBUTION HISTOGRAM:")
print("- Shows the spread of house prices across all properties in the dataset.")
print(f"- Mean price: ${df['price'].mean():,.2f} vs Median: ${df['price'].median():,.2f}")

# Print detailed stats for key metrics with clear formatting to show analysis depth 
for col in ['price', 'area']:
    print(f"\n  {col.upper()}:")
    df[col] = pd.to_numeric(df[col])  
    q1, q3 = np.percentile(df[col], [25, 75])   
    iqr = q3 - q1 
    outliers_count = len((df[col] < (q1-1.5*iqr)) | (df[col] > (q3+1.5*iqr)))
    
    print(f"\n      Range: ${df[col].min():,.2f} to ${df[col].max():,.2f}")
    print(f"      Q1-Q3: ${q1:.2f}-${q3:.2f} (IQR={iqr})") 
    if col == 'price':
        mean_price, std_dev = df[col].mean(), df[col].std()  
        
print("\n\n  AREA CORRELATION WITH PRICE:")
corr_matrix['area'].corr(df['price'])).3}")

# =============================================