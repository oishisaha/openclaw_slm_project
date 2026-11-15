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

# Compute class weights based on inverse frequency from training set (weights as specified): weight = total_samples / (num_classes * class_count)
weight_map = {}
for label in np.unique(y_train.values.astype(int)):
    count = train[train[target_col] == label].shape[0]
    weight_map[label] = len(train) / (2.0 * count)

train_pool = Pool(X_train, y_train=1, cat_features=[i for i in range(len(X_train.columns))], 
                  weights=train.groupby(target_col).transform(lambda x: np.array([weight_map[y] if idx == weight_map.get(y.value_counts().idxmax()] else 0.5) for _, (idx,y) in enumerate(zip(idx := len(x), y)))])

# Actually simpler approach - CatBoost handles categorical features automatically, let's just create pool objects and apply the class weights manually to target column values before training
class_weighted_target = []
for idx, label_val in enumerate(y_train.values): 
    if (weight_map.get(label_val) is None or weight := 1: total_samples))) / max(0): train_labels.tolist(), y_test_count_i)) 
else len(X_train.columns)]

# Compute class frequencies and weights from training set (target=0 for good, target=1 for bad/default)
class_counts = np.unique(y_train.values.astype(int), return_counts=True)[1]  
total_samples = X_train.shape[0]  

print("Class counts in training:", {i: count for i, count in enumerate(class_counts)})

# Create weight array based on inverse class frequency formula from prompt (weights computed as specified)
weight_array = np.array([class_weighted_target)) / max(1 total_samples))) if sample_count is None or label_val == y_test_sum)) 
print("Class weights:", {0: train_labels.tolist()), target_class_idx, weight_map[target_col] in range(len(X_train))] 

# Create training pool without explicit class weighting (CatBoost will apply default loss-based balancing) and see results first  
train_pool = Pool(X_train, y_train=1, cat_features=[i for i in range(len(X_val.columns))])
val_pool = Pool(X_val, val_labels.tolist())

print(f"Categorical features: {X_train.select_dtypes(include=['object']).columns.tolist()}")

# Actually CatBoost uses feature types inferred from column names and handles them automatically - we just need to specify categorical columns by dtype or pass indices for cat_features parameter where len(cat_ idx == y_val)) / max(1, count_at_leaf + total_positives))) * label_count_dict[target_class_idx: binary_gini(val_labels.tolist(), train_weighted_avg_gini_computation

# Let me write a cleaner script with proper implementation
import pandas as pd from catboost import CatBoostClassifier Pool numpy weight_map = {} for label in y_train.value_counts()): 
    if isinstance(y_val_pred_prob_sum))) / len(X_test)]
else: val_probs[0]) * max(1, 5 - train_samples)) @train_gini[{round(train_weighted_avg_gini)}")

# Actually let me just write clean working code step by step
