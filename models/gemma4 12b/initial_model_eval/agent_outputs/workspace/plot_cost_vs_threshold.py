import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from catboost import CatBoostClassifier, CatBoostRegressor

# Load data
train_df = pd.read_csv('data/german_train_80.csv')
val_df = pd.read_csv('data/german_val_20.csv')

X_train = train_df.drop(columns=['target_good'])
y_train = train_df['target_good']
X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

# Define models (same as previous)
cat_clf = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    loss_function='Logloss',
    eval_metric='AUC',
    cat_features=X_train.select_dtypes(include=['object', 'category']).columns.tolist(),
    verbose=False
)

cat_reg = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    loss_function='RMSE',
    eval_metric='RMSE',
    cat_features=X_train.select_dtypes(include=['object', 'category']).columns.tolist(),
    verbose=False
)

# Fit models
cat_clf.fit(X_train, y_train)
cat_reg.fit(X_train, y_train)

def get_cost_curve(probs, y_true):
    thresholds = np.arange(0.01, 1.0, 0.01)
    costs = []
    for t in thresholds:
        preds = (probs >= t).astype(int)
        fn = np.sum((y_true == 1) & (preds == 0))
        fp = np.sum((y_true == 0) & (preds == 1))
        cost = (5 * fn) + (1 * fp)
        costs.append(cost)
    return thresholds, costs

# Get curves for both models
t_clf, costs_clf = get_cost_curve(cat_clf.predict_proba(X_val)[:, 1], y_val)
# For regressor, we clip the raw scores to [0, 1] as they represent "probability-like" values
preds_reg = np.clip(cat_reg.predict(X_val), 0, 1)
t_reg, costs_reg = get_cost_curve(preds_reg, y_val)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t_clf, costs_clf, label='CatBoost Logloss (C11)', color='blue')
plt.plot(t_reg, costs_reg, label='Cat_Reg/L2 (C12)', color='orange')

# Find and mark minima
for t_arr, c_arr, label, color in [
    (t_clf, costs_clf, 'CatBoost Logloss', 'blue'), 
    (t_reg, costs_reg, 'Cat_Reg/L2', 'orange')
]:
    min_idx = np.argmin(c_arr)
    plt.plot(t_arr[min_idx], c_arr[min_idx], marker='o', markersize=10, 
               color=color, label=f'Min {label}')

plt.title('Cost per Sample vs Threshold')
plt.xlabel('Threshold')
plt.ylabel('Total Cost (5*FN + 1*FP)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('cost_vs_threshold.png')
