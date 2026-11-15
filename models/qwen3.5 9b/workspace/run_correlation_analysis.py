

import pandas as pd  

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')  
print("=" * 90 + "\nHOUSING DATA CORRELATION ANALYSIS\n"

cols_list = [str(c) for c in df.columns if str(c) != 'price']
corr_values_list = [] 
for i, c in enumerate(cols_list):
    corr_val = round(df[c].corr(df['price']), 4))  
    corr_values_list.append((i+1, c, r

