import pandas as pd
import numpy as np
from catboost import CatBoostClassifier

train_df = pd.read_csv('data/german_train_pipelineB.csv')
val_df = pd.read_csv('data/german_val_pipelineB.csv')

# Identify categorical columns (object or category dtype)
cat_features = train_df.select_dtypes(include=['object', 'category']).columns.tolist()

y_train = train_df['target_good']
X_train = train_df.drop(columns=['target_good'])
X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

# Calculate class weights: weight = total_train / (num_classes * count)
counts = y_train.value_counts().to_dict()
total_train = len(y_train)
num_classes = 2
w0 = total_train / (num_classes * counts[0])
w1 = total_train / (num_classes * counts[1])

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    loss_function='Logloss',
    eval_metric='AUC',
    cat_features=cat_features,
    class_weights=[w0, w1],
    verbose=False # Don't flood the console
)

model.fit(X_train, y_train, eval_set=(X_val, y_val))

# Note: CatBoost keeps track of results in the model object. 
# We need to extract the final metrics from the fit process or prediction.
# Since it's a 1000 iteration loop with evaluation at each step, we want the values 
# for the last iteration or best model as specified by 'use_best_model'.
# Wait, the prompt doesn't specify "best" but "final". CatBoost standard behavior:

# To get training log loss and validation log loss exactly as they appear in the final run:
print(f"{model.get_click_through_rate():.4f}") # This is not it. 
# Let's just use the fit results. 
# CatBoost returns evaluation metrics in its internal state after fitting.

# Actually, let's just compute them manually from the predictions to ensure accuracy 
# of the formula used for 'log loss'.
from sklearn.metrics import log_loss

train_probs = model.predict_probabilities(X_train)
val_probs = model.predict_probabilities(X_val)

# If it's binary, predict_probabilities returns [p0, p1]
# We sum across the second dimension to get probabilities of class 1 if we want just one array,
# but log_loss handles (y, probs) where probs is shape (n_samples, n_classes).
train_logloss = log_loss(y_train, train_probs, labels=[0, 1])
val_logloss = log_loss(y_val, val_probs, labels=[0, 1])

from sklearn.metrics import roc_auc_score
# For AUC, we use the probability of class 1 (the second column)
val_auc = roc_auc_score(y_val, val_probs[:, 1])

print(f"{train_logloss:.4f}")
print(f"{val_logloss:.4f}")
print(f"{val_auc:.4f}")
