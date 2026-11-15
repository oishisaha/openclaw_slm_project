

python3 << 'PYTHON_SCRIPT'
import pandas as pd

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_preprocessed.csv')
price_col = 'price'

correlations = {}
for feature in df.columns:
    if str(feature) != price_col:
        corr_value = round(df[feature].corr(df['price']), 4)
        correlations[str(feature)] = corr_value
    
sorted_correlations = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)[:20]

print('=' * 75 + '\nHOUSING DATA CORRELATION ANALYSIS\n' + '=' * 75)  
for rank, (feature_name, correlation_val) in enumerate(sorted_correlations[:8], start=1):
    feature_clean = str(feature_name).strip()
    
print(f"{'Rank':<6} | {feature:35s}: r={corr_value:+.4f}")
