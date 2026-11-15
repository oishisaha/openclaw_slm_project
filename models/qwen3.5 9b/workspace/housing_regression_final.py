

import pandas as pd  
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler, OneHotEncoder   
from sklearn.compose import ColumnTransformer    
from sklearn.pipeline import Pipeline    

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')

print("=" * 70)
print("HOUSING PRICE PREDICTION MODEL - BUILD AND EVALUATE")


## STEP 1: DATA EXPLORATION ##  
numeric_cols = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']   
