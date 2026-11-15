import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, roc_auc_score

train_df = pd.read_csv('data/german_train_pipelineB.csv')
val_df = pd.read_csv('data/german_val_pipelineB.csv')

# Identify categorical columns
cat_features = train_df.select_dtypes(include=['object', 'category']).columns.tolist()

y_train = train_df['target_good']
X_train = train_df.drop(columns=['target_good'])
X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

model = CatBoostRegressor(
    loss_function='RMSE',
    eval_metric='RMSE',
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    cat_features=cat_features,
    verbose=False
)

model.fit(X_train, y_train, eval_set=(X_val, y_val))

# Predictions for RMSE (Raw values)
train_preds = model.predict(X_train)
val_preds = model.predict(X_val)

train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))
val_rmse = np.sqrt(mean_squared_error(y_val, val_preds))

# For AUC, clip predictions to [0, 1] as probability-like scores
val_probs = np.clip(val_preds, 0, 1)
val_auc = roc_auc_score(y_val, val_probs)

print(f"{train_rmse:.4f}")
print(f"{val_rmse:.4f}")
print(f"{val_auc:.4f}")
