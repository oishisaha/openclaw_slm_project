

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge

# Load the dataset with absolute path. The CSV file is located in data/ directory."""


print("=" * 70)
print("HOUSING PRICE PREDICTION MODEL - BUILD AND EVALUATE")



## STEP 1: DATA EXPLORATION ##

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')

X, y are separated from the dataframe. """


# Create preprocessing pipelines
num_pipeline = Pipeline(steps=[('scaler', StandardScaler)])

cat_transformers = [col])

if not categorical_columns: cat_preprocessor = None else : column_names in categorical_features] if any(categorical_feature) ]): cat_pipe_steps.append(('enc_' + i, OneHotEncoder(handle_unknown='ignore', sparse=False), col)]
    elif len(column_names > 0 and num_pipeline]: # Build the full preprocessing pipeline with both numerical and categorical columns

preprocessing_pipeline = ColumnTransformer(
        transformers=cat_transformers, remainder='drop'


print("\n" + "=" * 60)
print("STEP 2: MODEL TRAINING")
print("=" * 60)
    elif len(cat_pipe_steps > 0): preprocessing_pipeline.steps.append(('categorical_columns', cat_preprocessor)) else : num_features], categorical columns in list(categorical features).astype('category'), 'drop')

model = Pipeline(steps=[ ('preprocessing' , preprocessing_pipeline), ('regressor', Ridge(alpha=1.0)))]


print("Training model on training data...")
X_train_scaled = X_all_cols_df.drop('price').copy()]
