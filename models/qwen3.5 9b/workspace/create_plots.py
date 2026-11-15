#!/usr/bin/env python3\n"""\nGenerate housing price visualisations from dataset CSV file.\nCreates three plots showing factors affecting house prices:\n1. Price distribution histogram \n2. Area vs price scatter plot with furnishing status coloring  \n3. Average price by furnishing status bar chart\nEach saved as PNG to workspace/data/ directory for easy access and sharing.
"""\nimport pandas as pd, matplotlib.pyplot as plt, numpy as np\nfrom pathlib import Path

output_dir = Path('data') 
output_dir.mkdir(exist_ok=True)\ndata_path = output_dir / 'housing_dataset.csv'\ndf = pd.read_csv(data_path)\nn = len(df)  

print("=" * 60 + "\nHOUSING PRICE VISUALISATIONS\n") \nprint(f"Loaded {n} records. Price range: ${df['price'].min():,.2f}-${df['price'].max():,.2f}\")

