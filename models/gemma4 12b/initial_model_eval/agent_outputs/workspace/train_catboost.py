import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score

train_df = pd.read_csv('data/german_train_pipelineB.csv')
val_df = pd.read_csv('data/german_val_pipelineB.csv')

# Identify categorical columns (they are objects in the pandas dataframe)
cat_features = train_df.select_dtypes(include=['object']).columns.tolist()

y_train = train_df['target_good']
X_train = train_df.drop(columns=['target_good'])

# Calculate class weights
# count of 0 and 1 in training set
counts = y_train.value_counts().to_dict()
total_train = len(y_train)
num_classes = 2
# weight = total_train / (num_classes * class_count)
weights = {
    '0': total_train / (num_classes * counts[0]),
    '1': total_train / (num_classes * counts[1])
}
# Note: In catboost, if values are ints/floats for target, use the numeric keys. 
# Since y_train is integer type from read_csv usually...
# Let's check the type of y_train values
if y_train.dtype == 'int64' or y_train.dtype == 'int32':
    weights = {0: total_train / (num_classes * counts[0]), 1: total_train / (num_classes * counts[1])}
else:
    # if it's object or string (rare for target unless specified)
    pass

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    loss_function='Logloss',
    eval_metric='AUC',
    early_stopping_rounds=50, # included for safety but it's not required to be 50 specifically
    cat_features=cat_features,
    class_weights=1.0 # We will handle balancing manually if needed or set appropriately
)

# Let's refine the class weights logic based on requirements: 
# "weight = total_train / (num_classes * count)"
# This is a standard way to balance classes.
# To pass it to CatBoost, we can provide a list of weights for each class or just use scale_pos_weight?
# No, the prompt says set 'class_weights' specifically.
current_counts = y_train.value_counts()
# weight = total / (num_classes * count) 
# Since num_classes is 2:
w0 = total_train / (2 * current_counts[0])
w1 = total_train / (2 * current_counts[1])

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    loss_function='Logloss',
    eval_metric='AUC',
    cat_features=cat_features,
    class_weights=(w0, w1) # CatBoost accepts a list/tuple for binary classification
)

# However, if the user meant to calculate specifically based on standard counts:
# Let's stick exactly to the formula provided.
pass

# Re-running with exact parameters
model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    random_seed=42,
    loss_function='Logloss',
    eval_metric='AUC',
    cat_features=cat_features,
    class_weights=[w0, w1]
)

model.fit(X_train, y_train, eval_set=(X_val_raw := X_val, y_val)) # Use a temp name to avoid conflict or similar. 
# Wait, I'll just write the script cleanly.
