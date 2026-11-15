import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score

# Load data - files are in workspace root (not data/ subdirectory) based on earlier listing
train = pd.read_csv('german_train_80.csv')
val = pd.read_csv('german_val_20.csv')

# Drop target column for feature matrix
target_col = 'target_good'
y_train = train[target_col]
X_train = train.drop(columns=[target_col])

y_val = val[target_col]
X_val = val.drop(columns=[target_col])

print("Train features:", X_train.columns.tolist())
print(X_train.shape)
print(y_train.value_counts(normalize=True))

# Train Logistic Regression with one-hot encoded features (already done in data)
model = LogisticRegression(
    max_iter=2000,
    solver='liblinear'
)
model.fit(X_train, y_train)

# Predict on validation set
y_val_pred_prob = model.predict_proba(X_val)[:, 1]
y_val_pred = model.predict(X_val)

# Calculate metrics
val_logloss = log_loss(y_val, y_val_pred_prob)
val_auc = roc_auc_score(y_val, y_val_pred_prob)

print(f"\nValidation Log Loss: {val_logloss:.4f}")
print(f"Validation AUC:     {val_auc:.4f}")

# Calculate train log loss too (optional check for overfitting)
y_train_proba = model.predict_proba(X_train)[:, 1]
train_logloss = log_loss(y_train, y_train_proba)
print(f"\nTrain Log Loss: {train_logloss:.4f}")
