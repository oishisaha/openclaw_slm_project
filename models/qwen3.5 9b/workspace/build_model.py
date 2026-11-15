
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge


# Load the dataset with absolute path. The CSV file is located in data/ directory."""

df = pd.read_csv('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv')



print("=" * 70)
print("HOUSING PRICE PREDICTION MODEL - BUILD AND EVALUATE")


# STEP 1: DATA EXPLORATION ##


"""

X_all_columns all the way to y_all_rows in a pandas DataFrame object. The shape of this dataset is {df_shape}. This contains columns named 'area', etc."""



num_cols = ['area']
cat_features.append(col)

numerical_features.append(num_column_list):


# Split into train/test sets (80/20 split with random_state for reproducibility.)"""

X_train, X_test, y_train, y_test = None).copy()]
