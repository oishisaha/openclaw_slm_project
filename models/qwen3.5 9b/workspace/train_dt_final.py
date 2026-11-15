import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from collections import Counter

# Load data - files are at workspace root (not subdirectory)
train = pd.read_csv('german_train_80.csv')
val = pd.read_csv('german_val_20.csv')

target_col = 'target_good'
y_train = train[target_col]
X_train = train.drop(columns=[target_col])
y_val = val[target_col]
X_val = val.drop(columns=[target_col])

# Train Decision Tree Classifier  
dt_model = DecisionTreeClassifier(
    random_state=42,
    max_depth=4,
    min_samples_leaf=20,
    criterion='gini'
)
dt_model.fit(X_train, y_train)

# Get validation predictions (probabilities of class 1)
y_val_pred_prob = dt_model.predict_proba(X_val)[:, 1]

def binary_gini(p):
    """Binary classification Gini impurity: 2 * p * (1 - p)."""
    return 2 * p * (1 - p)

# Compute validation set gini as mean of 2p(1-p) using predicted class-1 probabilities
val_gini_values = [binary_gini(p) for p in y_val_pred_prob]
val_logloss_mean_of_2p1pm = sum(val_gini_values) / len(y_val_pred_prob)

print(f"Validation Gini (mean of 2p(1-p)): {val_logloss_mean_of_2p1pm:.4f}")

# Compute training set weighted average gini
y_train_proba = dt_model.predict_proba(X_train)[:, 1] 
train_gini_values = [binary_gini(p) for p in y_train_proba]
train_weighted_avg_gini = sum(train_gini_values) / len(y_train)

print(f"Training Weighted Average Gini: {train_weighted_avg_gini:.4f}")

# Compute validation AUC from predicted probabilities and true labels (y=1 is bad/default, y_val contains 0/1 for good vs bad):
from sklearn.metrics import roc_auc_score
val_auc = roc_auc_score(y_val, y_val_pred_prob)
print(f"Validation AUC: {val_auc:.4f}")
