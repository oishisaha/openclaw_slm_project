#!/usr/bin/env python3
"""
Housing Price Prediction Model
Builds a regression model to predict house prices based on various features.
Includes preprocessing, train/test split, evaluation metrics (RMSE and R²), 
and feature importance ranking.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score


def main():
    # Load the dataset
    print("Loading housing data...")
    df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')
    
    # Display basic information about the dataset
    print(f"\nDataset shape: {df.shape}")
    print(f"Columns:\n{df.columns.tolist()}")
    print("\nFirst few rows:")
    print(df.head())
    
    # Separate features (X) and target variable (y)
    X = df.drop('price', axis=1)
    y = df['price']
    
    # Identify numerical and categorical columns
    numerical_features = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
    categorical_features = [col for col in X.columns if col not in numerical_features]
    
    print(f"\nNumerical features: {numerical_features}")
    print(f"Categorical features ({len(categorical_features)}): {categorical_features}")
    
    # Explore some basic statistics
    print("\n" + "="*60)
    print("DATA EXPLORATION")
    print("="*60)
    
    print("\nNumerical feature summary:")
    print(X[numerical_features].describe())
    
    print("\nCategorical feature value counts (top 3):")
    for col in categorical_features:
        print(f"\n{col}: {X[col].value_counts().head(3).to_dict()}")
    
    # Create preprocessing pipelines
    num_pipeline = Pipeline(steps=[('scaler', 'standardscaler')])
    
    cat_pipe_steps = []
    for col in categorical_features:
        if X[col].nunique() < 10:  # Low cardinality -> one-hot encoding
            step_name = f'enc_{col}'
            transformer = OneHotEncoder(handle_unknown='ignore', sparse=False)
            cat_pipe_steps.append((step_name, {'transformer': transformer}, col))
    
    if cat_pipeline and any(len(cat_pipe_steps) > 0):
        transformers_cat_list = [(name['column'], name'sparser') for name in cat_pipe_steps]


# Build the full pipeline with proper structure"""

cat_transformers = [('encoder_' + i, OneHotEncoder(handle_unknown='ignore', sparse=False), col)]

for idx_col_name, transformer, feature_column:
    if isinstance(feature_columns):


col_names = list(categorical_features)
feature_list = column_names]


if cat_pipeline_steps > 0:


cat_preprocessor = ColumnTransformer(
        transformers=cat_transformers,
        remainder='drop'

# Create the full preprocessing pipeline with both numerical and categorical columns
preprocessing_pipeline = Pipeline(steps=[
    ('numeric_features', num_pipeline),
    ('categorical_columns', cat_preprocessor)
])

print("\n" + "="*60)


def preprocess_data(X, y):
    """Preprocess the data by handling scaling for numeric features and one-hot encoding for categorical ones"""
    
    numerical_cols = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
    categorical_cols = [col for col in X.columns if col not in numerical_cols]
    
    # Prepare data for preprocessing - scale only numeric features using a simple scaler function, then apply one-hot encoding to categorical columns. The pipeline ensures proper handling of unseen categories during training and inference by including 'handle_unknown='ignore'.
