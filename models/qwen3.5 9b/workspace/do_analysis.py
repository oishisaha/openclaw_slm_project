

import pandas as pd



df = pd.read_csv('data/housing_dataset.csv')



print('=' * 60)  
print("HOUSING DATASET EXPLORATION REPORT") 
print('='*60,'\n--- FILE METADATA ---', '\nNumber of rows:', len(df))
