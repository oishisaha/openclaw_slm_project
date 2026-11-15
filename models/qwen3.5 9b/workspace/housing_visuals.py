#!/usr/bin/env python3\nimport pandas as pd, matplotlib.pyplot as plt, numpy as np\ndata = pd.read_csv('housing_dataset.csv')  # Load dataset with CSV file from data folder in workspace directory structure relative to script location shown here.\nprint(f"Loaded {len(data)} housing records.") \nfurnishing_order = ['unfurnished', 'semi-furnished', 'furnished']

