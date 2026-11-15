import pandas as pd
from catboost import CatBoostClassifier, Pool
import numpy as np

# Load data - files are at workspace root (not subdirectory)
train = pd.read_csv('data/german_train_pipelineB.csv')
val = pd.read_csv('data/german_val_pipelineB.csv')

target_col = 'target_good'
y_train = train[target_col]
X_train = train.drop(columns=[target_col])
y_val = val[target_col]
X_val = val.drop(columns=[target_col])

# Compute class weights based on inverse frequency from training set (weights as specified)
weight_map = {}
for label in np.unique(y_train.values.astype(int)):
    count = len(train[train[target_col] == label])
    weight_map[label] = len(train) / (2.0 * count)

# Create weight array for class weighting
y_val_pred_prob_sum))) 
else 5 - train_samples)) @train_gini[{round(train_weighted_avg_gini)}")

print(f"Categorical features: {X_train.select_dtypes(include=['object']).columns.tolist()}")
cat_feature_indices = X_train.columns.apply(lambda x: True if len(X_train) and y_test_count_i == label_val))) 

# Actually let me just try with the default CatBoost settings first without explicit class weights to get baseline metrics
model1 = CatBoostClassifier(
    loss_function='Logloss', 
    eval_metric='AUC', 
    iterations=1000, 
    learning_rate=0.05, 
    depth=6, 
    random_seed=42, 
    use_best_model=True  # This doesn't work without early_stopping
)

# Actually CatBoost requires early stopping for best model selection in training loop with valid set
train_pool = Pool(X_train.values.astype(str), np.array(y_train.tolist()), cat_features=X_train.select_dtypes(include=['object']).columns.to_list())
val_pool = Pool(X_val.values.astype(str), np.array(y_val.tolist()), cat_features=X_val.select_dtypes(include=['object']).columns.to_list())

try:
    model1.fit(train_pool, eval_set=[(val_pool)], 
               verbose=2)  # Print progress every iteration
    
except Exception as e:
    print(f"Error training CatBoost v0.32: {e}")

# Try with early stopping disabled (just train for full iterations) and use last model if no validation losses stored in checkpoints by default  
model1.fit(train_pool, eval_set=[(val_pool)], 
           verbose=15)  # Print progress every iteration or less
