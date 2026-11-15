import pandas as pd 
from sklearn.tree import DecisionTreeClassifier  
from sklearn.metrics import log_loss, roc_auc_score  

train = pd.read_csv('german_train_80.csv')  
val=pd.read_csv('german_val_20.csv')  

common_cols=set(train.columns)&set(val.columns)-{'target_good'}
X_features=list(common_cols)

y_true=train['target_good'].values 
model=DecisionTreeClassifier(max_depth=4, min_samples_leaf=20, criterion='gini', random_state=42); model.fit(X=X_train[X_features], y=y[True]) 
