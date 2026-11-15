#!/bin/bash

# This script will be used to prepare housing data for model training.
echo "Creating preprocessing pipeline and preparing the dataset..."

cd /home/vboxuser/.openclaw/workspace


python3 << 'EOF'

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor


# Load the dataset

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')



print("=" * 70)
print("HOUSING PRICE PREDICTION MODEL - BUILD AND EVALUATE")
print("=" * 70)

## 1. DATA EXPLORATION ##


print("\n" + "=" * 60)
print("STEP 1: DATA EXPLORATION")
print("=" * 60)



print(f"\nDataset loaded successfully!")
df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')

## Display basic info ##


X_all_cols_df.shape, f"Target variable: price (column exists)")
y = df['price']

# Separate features and target X_all_columns all the way to y_all_rows in a pandas DataFrame object. The shape of this dataset is {df_shape}. This contains columns named 'area', 'bedrooms', 'bathrooms', etc. with numerical data representing housing characteristics, while price is the dependent variable we want to predict using machine learning techniques."""


## Feature Types

print("\nFeature Distribution:")
num_cols = ['area']
cat_features.append(col)

numerical_features.append(num_column_list):


# Split into train/test sets (80/20 split with random_state for reproducibility. The test set will be used to evaluate model performance on unseen data."""

X_train, X_test, y_train, y_test = df[features].copy(), features].astype(dtype=np.int32), None)


for feature in num_features:
    scaler.fit(X_train[[feature]])]
        scaled_value=scaler.transform([[scaled_value]]).flatten() + train_df.iloc[i][feature]].
