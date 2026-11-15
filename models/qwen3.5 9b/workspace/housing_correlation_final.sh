python3 << 'PYTHONSCRIPT'
import pandas as pd, numpy as np

print("\n" + "=" * 80)
print("HOUSING DATA ANALYSIS - Size (sqft) vs Price Correlation")
print("=" * 80)

try:
    df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv')
except Exception as e:
    print(f"Error reading CSV: {e}")
PYTHONSCRIPT
