

import pandas as pd

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')
price_col = 'price'

correlations = {}
for feature in df.columns:
    if feature != price_col:
        corr_value = round(df[feature].corr(df['price']), 4)
        correlations[feature] = corr_value
    
sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)

print("=" * 70 + " HOUSING DATA CORRELATION ANALYSIS") 
for rank, (feature_name, correlation_val) in enumerate(sorted_correlations[:12], start=1):
    print(f"{rank}. {str(feature).strip():35} Correlation: ", end=''))
