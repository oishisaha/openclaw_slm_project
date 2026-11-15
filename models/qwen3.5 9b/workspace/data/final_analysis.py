import pandas as pd 
from sklearn.linear_model import Ridge  
from sklearn.metrics import mean_squared_error, roc_auc_score  
import numpy as np

train = pd.read_csv('german_train_80.csv')  
val = pd.read_csv('german_val_20.csv')  

common_cols = set(train.columns) & set(val.columns) - {'target_good'}
X_features = list(common_cols)

y_true_train = train['target_good'].values  
ridge = Ridge(alpha=1.0) 
ridge.fit(train[X_features], y_true_train)

train_preds_raw = ridge.predict(X_train[features]])  

print(f"Train MSE: {mean_squared_error(y, preds_train raw:.4}")
val_preds_raw = ridge.predict(val[X_features]) 

# Clip for numerical stability in sigmoid def safe_sigmoid(x): 
    return 1 / (1 + np.exp(-np.clip(x, -500, )))  
probabilities_val = saf e sigmoid( val_preds_raw))

print(f"Val MSE: {mean_squared_error(y_true_val, preds_vals raw:.4}")