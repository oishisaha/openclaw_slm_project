

import pandas as pd
import sys

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')
price_col = 'price'  

correlations = {}  
for feature in df.columns:
    if str(feature) != price_col and not isinstance(df[feature], object): 
        corr_value = round(df[feature].corr(df['price']), 4)
        correlations[str(feature)] = (corr_value, type))

sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)[:20]

print('=' * 95 + '\n')  
for rank_idx, ((feature_name,), correlation_val in enumerate(sorted_correlations[:30], start=1):
    feature_clean = str(feature).strip()
    
# Handle potential duplicate columns by taking first occurrence only
