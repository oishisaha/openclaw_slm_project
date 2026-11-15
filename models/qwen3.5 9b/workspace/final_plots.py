#!/usr/bin/env python3\n"""Generate housing price visualisations from data/housing_dataset.csv.\nCreates three PNG charts showing main factors affecting house prices:\n1. Price distribution histogram - shows how many houses sell at each price level\n2. Area vs price scatter plot - relationship between size and value, colored by furnishing status  \n3. Average price bar chart comparing furnished/semi-furnished/unfurnished properties\nAll charts saved to workspace/data/ as PNG files for easy viewing.\n"""\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport numpy as np\nfrom pathlib import Path

# Load dataset from local path relative to script location in workspace directory structure \ndata_path = 'data/housing_dataset.csv'\nn_rows, n_cols = len(data), data.columns.shape[0] if hasattr(data, 'columns') else 1\ndf = pd.read_csv('data/housing_dataset.csv', nrows=n_rows)  

print("=" * 60)\nprint("HOUSING PRICE ANALYSIS - VISUALISATION GENERATION")\nprint(f"Loaded {len(df)} records.") \nprint(f"Price range: ${df['price'].min():,.2f} to ${df['price'].max():,.2f}")

