

import pandas as pd  
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')  

print("\n")

cols_list = [str(c) for c in df.columns if str(c) != 'price']
corr_values_dict = {} 
for i, col in enumerate(cols_list):
    corr_val = round(df[col].corr(df['price']), 4))  
    corr_values_dict[cor] = (r
