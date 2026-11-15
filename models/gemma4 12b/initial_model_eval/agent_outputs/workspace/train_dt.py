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

# The question asks for "weighted average Gini impurity across leaf nodes". 
# This corresponds to the 'entropy' or 'gini' value in common, but specifically 
# in scikit-learn, the tree object holds information about its leaves.
model = DecisionTreeClassifier(random_state=42, max_depth=4, min_samples_leaf=20, criterion='gini')
model.fit(X_train, y_train)

# train_gini: weighted average Gini impurity of the leaf nodes in the tree (the training set).
# Scikit-learn doesn't expose "weighted average" directly as a single metric easily 
# without walking the tree, but we can calculate it from the sample weights.
# However, usually for these tests, they refer to the Gini impurity of the leaves.
# Let's check common implementations or just calculate it by looking at leaf values.

def get_weighted_gini(tree):
    total_samples = 0
    weighted_gini_sum = 0
    # The tree structure is available via the tree object
    # Each node has n_samples, children, left_child, right_child, etc.
    # We only care about leaf nodes (where left and right are -1)
    for node in range(tree.tree_.node_count):
        if tree.tree_.left_child[node] == -1:
            n = tree.tree_.n_samples[node]
            # For a leaf, the Gini is calculated as 2 * p * (1-p) where p is prob of class 1
            # In sklearn's DecisionTree, for a leaf, value is [prob_0, prob_1] if it's multisticlass?
            # No, for binary classification with classes [0, 1], it's usually just the counts.
            # For gini: 1 - sum(p_i^2). If there are 2 classes, and p is prob of class 1,
            # Gini = 1 - (p^2 + (1-p)^2) = 1 - (p^2 + 1 - 2p + p^2) = 1 - (2p^2 - 2p + 1) = 2p - 2p^2 = 2p(1-p).
            # This is exactly the formula for val_gini calculation.
            pass

    # Actually, if the tree uses criterion='gini', it minimizes:
    # Gini = 1 - sum(p_i^2) which is 2*p*(1-p) for binary cases.
    # Let's calculate it directly from leaf samples and proportions.
    for node in range(tree.tree_.node_count):
        if tree.tree_.left_child[node] == -1:
            n = tree.tree_.n_samples[node]
            # Probability of class 1 at this leaf
            p = tree.tree_.ntrees[node] # Wait, ntries? No. 
            # In sklearn's tree, for a binary target with weights=None,
            # the n_samples is the count of samples in that leaf.
            pass

    # Let's re-think: The question asks for "weighted average Gini impurity across leaf nodes".
    # This is sum(weight_i * Gini_i) / total_sum(weights).
    # For binary classification, Gini = 1 - (p^2 + (1-p)^2) = 2*p*(1-p).
    
    total_samples = 0
    weighted_gini_sum = 0
    for node in range(tree.tree_.node_count):
        if tree.tree_.left_child[node] == -1:
            n = tree.tree_.n_samples[node]
            # In a binary classification leaf, the samples are divided by class.
            # However, if we have labels as 0 and 1, sklearn doesn't store p directly 
            # in a way that's easy to fetch unless it's multisticlass?
            # Let's look at tree_ object.
            pass

    # Simpler approach: iterate through all leaf nodes. 
    # In scikit-learn, for a leaf node (where left and right are -1):
    # n_samples is the number of samples in that leaf.
    # For a binary classification problem, p = count(1) / total_in_leaf.
    # But since we don't have 'proportions' in a simple way, let's use 
    # the formula provided for val_gini: 2*p*(1-p).
    pass

# Let's simplify. The "weighted average Gini" on training set is:
# sum(n_samples_at_leaf * gini_of_leaf) / total_samples_in_all_leaves
# For binary classification, the Gini impurity of a leaf is 2*p*(1-p).
# So this calculation is identical to finding the expected value of 2*p*(1-p) over the training data.

# Let's use a helper function to compute it.
def calculate_weighted_gini(tree):
    total_weight = 0
    weighted_sum = 0
    for node in range(tree.tree_.node_count):
        if tree.tree_.left_child[node] == -1: # Leaf node
            n = tree.tree_.n_samples[node]
            # If the target is binary, the probability of class 1 is 
            # (number of items in class 1) / total.
            # In sklearn's DecisionTreeClassifier for binary targets,
            # it uses 'Gini' to mean the impurity of the split.
            # For a leaf node with p = probability of target_good=1:
            # Gini impurity = 1 - (p^2 + (1-p)^2) = 2*p*(1-p).
            pass

# Let's just use the formula 2*p*(1-p) for every leaf node where p is 
# the proportion of class 1 in that leaf, and weigh by sample count.
def calculate_weighted_gini_v2(tree):
    total_samples = 0
    sum_of_gini = 0
    for node in range(tree.tree_.node_count):
        if tree.tree_.left_child[node] == -1: # Leaf node
            n = tree.tree_.n_samples[node]
            # For binary classification, we can't easily get p from 
            # just n_samples because it doesn't tell us how many were 'good'.
            # However, in sklearn, if the target is discrete (0,1),
            # then for a leaf node at index i:
            # The Gini impurity of that node is already computed during training.
            # Since we want "weighted average Gini", and 2*p*(1-p) IS the Gini formula 
            # for binary cases, it's just sum(n_leaf * Gini_leaf) / total_samples.
            pass

# Wait, I can use a trick. If we evaluate the probability p at each leaf, 
# and then calculate average of 2*p*(1-p).
def calc_metrics(tree, X_train):
    total_n = 0
    sum_gini = 0
    for node in range(tree.tree_.node_count):
        if tree.tree_.left_child[node] == -1:
            n = tree.tree_.n_samples[node]
            # Note: Since it's a binary classification, if the classifier was 
            # trained on {0, 1}, we can derive p from internal data or just calculate it.
            # Actually, in sklearn for DecisionTreeClassifier with binary targets, 
            # there is no "p" stored explicitly in the same way as multiclass? 
            # No, let's use a trick: to get p, we look at the leaf values if they were converted to probs.
            # But actually, simply put this into a loop:
            pass

# Let me just run a script that calculates exactly what is asked.
# "weighted average Gini impurity across leaf nodes" on train: 
# For each leaf i, let n_i be the number of samples and G_i = 2*p_i*(1-p_i).
# Result = sum(n_i * G_i) / sum(n_i).

import numpy as np
def get_weighted_gini(tree):
    total_samples = 0
    sum_of_ginis = 0
    for node in range(tree.tree_.node_count):
        if tree.tree_.left_child[node] == -1: # Leaf
            n = tree.tree_.n_samples[node]
            # For binary classification, p is the proportion of class 1.
            # In scikit-learn, if target is (0, 1), this can be found from leaf values?
            # No, let's assume a standard interpretation:
            # It refers to the average Gini impurity for all training samples.
            pass

# Actually, I will use the logic that since it's binary classification, 
# the probability p is available if we treat it as such.
# Let's look at the tree_ object in detail.
"""
tree_.n_samples: number of samples at each node
tree_.children_left: index of left child; -1 if leaf
tree_.feature: feature index or -2 if leaf
tree_.impurity: impurity of node (gini, entropy, etc.)
tree_.impurity_score: {0.0, 1.0} is valid for all values in the tree
"""
# For a binary target and criterion='gini', tree_.impurity[node] IS exactly 2*p*(1-p).
# So the "weighted average Gini" over leaves is sum(tree_.n_samples * tree_.impurity) / sum(tree_.n_samples)
# for all nodes where it's a leaf.

# I will write a script to extract this exactly.
"""
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

# weighted average Gini impurity across leaf nodes:
# Sum of (n_samples_at_leaf * gini_of_leaf) for all leaves / total_samples_in_training_set
total_n = 0
sum_gini = 0
for i in range(model.tree_.node_count):
    if model.tree_.left_child[i] == -1: # it's a leaf
        # For binary classification with criterion='gini', 
        # tree_.impurity is 2*p*(1-p)
        n = model.tree_.n_samples[i]
        sum_gini += n * model.tree_.impurity[i]
        total_n += n

train_gini = sum_gini / total_n
print(f"Train Gini: {train_gini:.4f}")

# mean of 2p(1-p) for validation set:
# predict_proba returns [prob_0, prob_1]
val_probs = model.predict_proba(X_val)[:, 1]
# For each sample in val, p = val_probs[i]. Calculation is sum(2*p*(1-p)) / num_samples
val_gini_mean = np.mean(2 * val_probs * (1 - val_probs))
print(f"Val Gini: {val_gini_mean:.4f}")

# AUC
val_auc = roc_auc_score(y_val, val_probs)
print(f"Val AUC: {val_auc:.4f}")
"""
end of logic. Let's run it.
"""
