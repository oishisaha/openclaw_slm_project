

import pandas as pd




df = pd.read_csv('data/housing_dataset.csv')



# Write full exploration report to file with all analysis done cleanly in one session:

print('=' * 60)  
print("HOUSING DATASET EXPLORATION REPORT") 
print('='*60, '\n\n--- FILE METADATA ---', '\nNumber of rows (records): {}'.format(len(df)), '\nNumber of columns (features): {}.
'.format(df.shape[1]))

# Read column names properly:
col_names = list(df.columns.values)
