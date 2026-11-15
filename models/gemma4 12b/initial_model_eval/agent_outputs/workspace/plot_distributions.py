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

# Define models
cat_clf = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    loss_function='Logloss',
    eval_metric='AUC',
    cat_features=X_train.select_dtypes(include=['object']).columns.tolist(),
    verbose=False
)

cat_reg = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    loss_function='RMSE',
    eval_metric='RMSE',
    cat_features=X_train.select_dtypes(include=['object']).columns.tolist(),
    verbose=False
)

# Fit models
cat_clf.fit(X_train, y_train)
cat_reg.fit(X_train, y_train)

# Predictions
# Classifier outputs probability of class 1 (Bad)
probs_clf = cat_clf.predict_proba(X_val)[:, 1]
# Regressor output is a raw score; clip to [0, 1] for distribution analysis
preds_reg = np.clip(cat_reg.predict(X_val), 0, 1)

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

# Plot for CatBoost Classifier
for label, color in [('Good', 'blue'), ('Bad', 'orange')]:
    mask = y_val == (0 if label == 'Good' else 1)
    ax1.hist(probs_clf[mask], bins=20, alpha=0.5, label=label, color=color, edgecolor='none')

ax1.set_title('CatBoost Classifier\nProbabilities by Class')
ax1.set_xlabel('Predicted Probability (Bad)')
ax1.set_ylabel('Frequency')
ax1.legend()

# Plot for CatBoost Regressor
for label, color in [('Good', 'blue'), ('Bad', 'orange')]:
    mask = y_val == (0 if label == 'Good' else 1)
    ax2.hist(preds_reg[mask], bins=20, alpha=0.5, label=label, color=color, edgecolor='none')

ax2.set_title('CatBoost Regressor\nClipped Prediction Distribution')
ax2.set_xlabel('Predicted Score (Clip 0-1)')
ax2.legend()

plt.tight_layout()
plt.savefig('predicted_probability_distributions.png')
