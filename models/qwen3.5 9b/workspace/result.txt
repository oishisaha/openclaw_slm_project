

import pandas as pd  
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')  

cols_list = [str(c) for c in df.columns if str(c) != 'price']

corr_values_dict = {} 
for col in cols_list:
    corr_val = round(df[col].corr(df['price']), 4))  

