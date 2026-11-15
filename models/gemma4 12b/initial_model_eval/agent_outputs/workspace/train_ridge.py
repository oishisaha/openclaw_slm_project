import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, roc_auc_score

train_df = pd.read_csv('data/german_train_80.csv')
val_df = pd.read_csv('data/german_val_20.csv')

X_train = train_df.drop(columns=['target_good'])
y_train = train_df['target_good']
X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

model = Ridge(alpha=1.0)
model.fit(X_train, y_train)

train_preds = model.predict(X_train)
val_preds = model.predict(X_val)

train_mse = mean_squared_error(y_train, train_preds)
val_mse = mean_squared_error(y_val, val_preds)

# For AUC, convert to probabilities using sigmoid
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

val_probs = sigmoid(val_preds)
val_auc = roc_auc_score(y_val, val_probs)

print(f"{train_mse:.4f}")
print(f"{val_mse:.4f}")
print(f"{val_auc:.4f}")
