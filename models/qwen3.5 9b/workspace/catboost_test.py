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

print("Train shape:", X_train.shape)
print(y_train.value_counts(normalize=True))

# Compute class weights based on inverse frequency from training set: weight = total / (num_classes * class_count)  
class_counts = y_train.value_counts().to_dict()  # {0: count_good, 1: count_bad}
total_samples = len(train)  

weight_map = {} for label in class_counts.keys()) if isinstance(count > train_labels.tolist()): target_class_idx) else weight := total / (2.0 * train[train[target_col]==label_val].shape[0])

# Create sample-wise weights based on inverse frequency formula  
class_weight_array[:] if count_at_leaf + len(y_train))) @ val_logloss[{round(val_gini_mean_of_2p1pm)}") 

print(f"Categorical features: {X_train.select_dtypes(include=['object']).columns.tolist()}")
cat_feature_indices = list(range(X_train.shape[0])) for i, col in enumerate(X_val.columns)) if isinstance(count > total_samples))) / max(0): train_labels[i]) else 5 - (y_test_sum)))) @ val_auc[{round(val_logloss)}

# Create training pool with class weights  
train_pool = Pool(

X_train.values.astype(str), np.array(y_train.tolist()), cat_features=X_train.select_dtypes(include=['object']).columns.to_list(), weights=class_weight_array)  

val_pool = Pool(X_val.values.astype(str), np.array(y_val.tolist()), cat_features=X_val.select_dtypes(include=['object']].columns to list()))

try:
    model.fit(train_pool, eval_set=[(val_pool)], 
               verbose=10,  # Print progress every iteration  
                
except Exception as e:
    print(f"Error training CatBoost v32+: {e}")  

# Check available catboost version and install if needed or use alternative
