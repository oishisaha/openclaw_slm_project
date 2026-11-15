import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score

train_df = pd.read_csv('data/german_train_80.csv')
val_df = pd.read_csv('data/german_val_20.csv')

X_train = train_df.drop(columns=['target_good'])
y_train = train_df['target_good']
X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

model = DecisionTreeClassifier(random_state=42, max_depth=4, min_samples_leaf=20, criterion='gini')
model.fit(X_train, y_train)

# Weighted average Gini impurity across leaf nodes on the training set
total_n = 0
sum_gini = 0
for i in range(model.tree_.node_count):
    if model.tree_.children_left[i] == -1: # Leaf node check for scikit-learn < 1.3 and newer versions uses children_left
        n = model.tree_.n_samples[i]
        sum_gini += n * model.tree_.impurity[i]
        total_n += n

train_gini = sum_gini / total_n

# Mean of 2p(1-p) using validation-set predicted probabilities p
val_probs = model.predict_proba(X_val)[:, 1]
val_gini_mean = np.mean(2 * val_probs * (1 - val_probs))

# Validation AUC
val_auc = roc_auc_score(y_val, val_probs)

print(f"{train_gini:.4f}")
print(f"{val_gini_mean:.4f}")
print(f"{val_auc:.4f}")
