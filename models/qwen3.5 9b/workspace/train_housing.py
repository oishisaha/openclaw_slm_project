

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

# Separate features (X) and target variable (y)
print(f"\nDataset shape: {df.shape}")
print("Columns:", df.columns.tolist())


numerical_features.append(num_column_list):


cat_preprocessor = ColumnTransformer( transformers=cat_transformers] if cat_pipes else None)



preprocessing_pipeline = Pipeline(steps=[('num', num_pipe), ('cat' , col in categorical features].astype category'], remainder='drop')] model = Ridge()
print(f"\nFeatures: {X.columns.tolist()}")

## STEP 2: TRAINING THE MODEL ##


model.fit(X_train, y_train)
predictions_test = model.predict(X_test)


from sklearn.metrics import mean_squared_error, r2_score


rmse = np.sqrt(mean_squared_error(y_test, predictions_test))
r2 = r2_score(y_test, predictions_test)
