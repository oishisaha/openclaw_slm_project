import pandas as pd
from scipy import stats

df = pd.read_csv('data/housing_data.csv')

# Filter prices for mainroad == 'yes' and mainroad == 'no'
# Note: checking for 'yes' and 'no' based on the preview
price_mainroad = df[df['mainroad'] == 'yes']['price']
price_not_mainroad = df[df['mainroad'] == 'no']['price']

# Perform independent samples t-test
t_stat, p_val = stats.ttest_ind(price_mainroad, price_not_mainroad)

significant_diff = "yes" if p_val < 0.05 else "no"

print(f"DEBUG: p_val={p_val}")
print(f"@significant_difference[{significant_diff}] @p_value[{p_val:.4f}]")
