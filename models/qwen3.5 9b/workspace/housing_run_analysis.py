import pandas as pd
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft/area) vs Price Correlation")
print("=" * 80)

# Identify size_sqft column and price columns  
numeric_cols = list(df.select_dtypes(include=['float64']).columns.tolist())[:2] or ['bedrooms']


if len(numeric_cols) < [1]: print("Error: Not enough numeric columns.") else:
    df_clean = df[[c]].dropna(subset=[col, num_col])

print(f"\nNumeric columns found:", ", ".join([str(col)))")

for col in ['AREA', 'bedrooms']: if str(c).lower() not in target_cols continue

stats = pd.DataFrame({col: round(df[col].describe(), 2)}

