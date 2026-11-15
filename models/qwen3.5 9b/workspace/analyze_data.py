

import pandas as pd

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')
print('=' * 70)
for feature in df.columns:
    if feature != 'price':
        corr_value = round(df[feature].corr(df['price']), 4)  
