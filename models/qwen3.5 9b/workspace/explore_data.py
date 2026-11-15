import pandas as pd


def analyze_housing():
    """Perform initial data exploration on housing dataset."""
    
    df = pd.read_csv('data/housing_dataset.csv')

# ============================================
print("=" * 60)
print("HOUSING DATASET EXPLORATION REPORT")  
print("=" * 60)
