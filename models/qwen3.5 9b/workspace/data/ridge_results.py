import pandas as pd
from sklearn.linear_model import Ridge  
from sklearn.metrics import mean_squared_error, roc_auc_score  import numpy as np

# Load datasets 
train = pd.read_csv('german_train_80.csv')  
val = pd.read_csv('german_val_20.csv')  

print(f"Train shape: {train.shape}")
common_cols = set(train.columns) & set(val.columns) - {'target_good'}
X_features = list(common_cols)

y_true_train = train['target_good'].values  
y_true_val = val['target_good'].values  

# Train Ridge regression with alpha=1.0 
ridge = Ridge(alpha=1.0) 
ridge.fit(train[X_features], y_true_train)

# Training predictions (raw for MSE)
preds_train_raw = ridge.predict(X_train[["X_ t rain features]]) 

train_mse= mean_squared_error(y, preds train raw))  

print(f"Train MSE: {trainmse:.4f}")  