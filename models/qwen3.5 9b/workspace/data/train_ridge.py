import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, roc_auc_score
import numpy as np

# Load datasets
train = pd.read_csv('german_train_80.csv')
val = pd.read_csv('german_val_20.csv')

print(f"Train shape: {train.shape}")
print(f"Val shape: {val.shape}")
print(f"\nCommon columns between train and val:")
common_cols = set(train.columns) & set(val.columns) - {'target_good'}
print(common_cols)

# Use only common columns for both sets (excluding target)
X_train_features = [col for col in common_cols]
y = train['target_good']

# Train Ridge regression with alpha=1.0
ridge = Ridge(alpha=1.0)
ridge.fit(train[X_train_features], y)

# Predictions on training set - use raw predictions (not probabilities yet)
preds_train_raw = ridge.predict(train[X_train_features])

# Clip for numerical stability in sigmoid
def safe_sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

probabilities_train = safe_sigmoid(preds_train_raw)

train_mse = mean_squared_error(y.values.flatten(), preds_train_raw)

# Predictions on validation set  
preds_val_raw = ridge.predict(val[X_train_features])
val_probs = safe_sigmoid(preds_val_raw)
val_mse = mean_squared_error(val['target_good'].values, preds_val_raw)

# Calculate AUC (use probabilities for ROC curve since target is 0/1 classification)
print(f"\nY values in val: {sorted([y_true])}")  
unique_targets = sorted(list(set(val['target_good'])))
if len(unique_targets) == 2 and min(unique_targets)==0 and max(unique_targets)==1:
    print("Valid binary labels for AUC calculation")
else:    
    # If only one target class exists, we need to handle this differently
    if (val['target_good'].sum() > 0):  # Bad credit present 
        auc_score = roc_auc_score(val['target_good'].values.values(), val_probs)  
        print(f"Val AUC: {auc_score}")
    
# Final output format

print("\nResults:")
print("@train_mse[{}] @val_mse[{}] @val_auc[{:.4f}]\n".format(trainmse, .{},{}, auc_ score[:5] f")
