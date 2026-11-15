import pandas as pd 
from sklearn.linear_model import Ridge  
from sklearn.metrics import mean_squared_error, roc_auc_score  
import numpy as np

# Load datasets 
train = pd.read_csv('german_train_80.csv')  
val = pd.read_csv('german_val_20.csv')  

common_cols = set(train.columns) & set(val.columns) - {'target_good'}
X_features = list(common_cols)

y_true_train = train['target_good'].values  
y_true_val = val['target_good'].values  

# Train Ridge regression with alpha=1.0 
ridge = Ridge(alpha=1.0) 
ridge.fit(train[X_features], y_true_train)

train_preds_raw = ridge.predict(train[X_features]) 

print(f"Train MSE: {mean_squared_error(y, train_preds raw)}")  
val_preds_raw = ridge.predict(val[X_features])