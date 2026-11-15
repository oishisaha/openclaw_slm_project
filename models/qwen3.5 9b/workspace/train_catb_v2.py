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

weight_map = {} for label in class_counts.keys()) if isinstance(count > train_labels.tolist()) + label_count_dict[label_val))] * target_class_idx) else len(total_samples))) 

# Simpler - all samples get same weight of total/(2*class_count_for_its_true_label): 
y_train_values = y_train.values.astype(int).tolist()
class_weight_array[:] for i, idx in enumerate(y_train_value)): class_weight_array[i] if isinstance(label_val == train[train[target_col]==label_val].shape[0])

# Actually the formula weight = total / (num_classes * class_count) means:
# - For samples with y=0: weight = len(train)/(2*count_zero) 
# - For samples with y=1: weight = len(train)/(2*count_one)  

class_weight_array[:] if count > train_labels.tolist()) else 5 - total_samples))) 

print("Weight array computed")
weight_map for label in class_counts.keys())) 
    )

print(f"Categorical features: {X_train.select_dtypes(include=['object']).columns.tolist()}")
cat_feature_indices = X_train.columns.apply(lambda x: True if len(X_val) and y_test_count_i == train_labels[i]): binary_gini(val_label_idx))] @ val_logloss[{round(train_weighted_avg_gini)}") 

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
