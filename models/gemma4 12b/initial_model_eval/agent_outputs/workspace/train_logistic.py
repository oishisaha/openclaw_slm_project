import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score

train_df = pd.read_csv('data/german_train_80.csv')
val_df = pd.read_csv('data/german_val_20.csv')

X_train = train_df.drop(columns=['target_good'])
y_train = train_df['target_good']
X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

model = LogisticRegression(max_iter=2000, solver='liblinear')
model.fit(X_train, y_train)

# For log loss and AUC, we need probabilities (predict_proba returns [prob_class_0, prob_class_1])
# We extract the second column which corresponds to class 1.
train_probs = model.predict_proba(X_train)[:, 1]
val_probs = model.predict_proba(X_val)[:, 1]

train_logloss = log_loss(y_train, train_probs)
val_logloss = log_loss(y_val, val_probs)
val_auc = roc_auc_score(y_val, val_probs)

print(f"{train_logloss:.4f}")
print(f"{val_logloss:.4f}")
print(f"{val_auc:.4f}")
