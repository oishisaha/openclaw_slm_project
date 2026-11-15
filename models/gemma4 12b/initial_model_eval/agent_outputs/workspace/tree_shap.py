import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
import shap
import warnings
warnings.filterwarnings('ignore')

# Load data (Note: The user refers to the champion model from C11, 
# which was trained on Pipeline A 'german_train_80.csv'
# and evaluated on Pipeline A 'german_val_20.csv').
# However, they specifically mention "Pipeline B validation set".
# Since Pipeline B (raw categorical) data usually has different columns than Pipeline A 
# (one-hot encoded), I will check the file contents first to confirm if it's a naming mismatch or if the model handles both.

train_df = pd.read_csv('data/german_train_80.csv')
val_df = pd.read_csv('data/german_val_20.csv')

X_train = train_df.drop(columns=['target_good'])
y_train = train_df['target_good']
# In this context, I will assume the user meant "the validation set used for C11" 
# or that the pipeline labels are consistent in terms of features if it's a shared project.

X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

# Re-implementing champion CatBoost Logloss (C11)
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

cat_clf.fit(X_train, y_train)

# TreeSHAP for CatBoost
# For CatBoost specifically, we use the explainer to compute SHAP values.
explainer = shap.TreeExplainer(cat_clf)
shap_values = explainer.shap_values(X_val)

# If it's a binary classification (common in CatBoost), 
# shap_values might be a list of 2 arrays or a single array for the probability/score.
if isinstance(shap_values, list):
    # Use values for class 1
    vals = shap_values[1]
else:
    vals = shap_values

# Calculate mean absolute SHAP value per feature
# Note: If multiple features were one-hot encoded, they will appear as individual columns.
mean_abs_shap = np.abs(vals).mean(axis=0)

feature_names = X_val.columns.tolist()
results = []
for name, val in zip(feature_names, mean_abs_shap):
    results.append((name, val))

# Sort by value descending and pick top 3
sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

for i in range(3):
    print(f"{sorted_results[i][0]}:{sorted_results[i][1]:.2f}")
