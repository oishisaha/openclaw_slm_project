

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


X, y are separated from the dataframe. """
