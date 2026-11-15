

import pandas as pd  
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')  

correlations_list = [] 
for col in df.columns:
    if str(col) != 'price':
        corr_val = round(df[col].corr(df['price']), 4)

sorted_correlations_list = sorted(correlations_list, key=lambda x[1])

