import pandas as pd 
from sklearn.linear_model import Ridge  

train = pd.read_csv('german_train_80.csv')  
val=pd.read_csv('german_val_20.csv')  

common_cols=set(train.columns)&set(val.columns)-{'target_good'}
X_features=list(common_cols)

y_true=train['target_good'].values 
ridge=Ridge(alpha=1.0); ridge.fit(X=[train[X_features]], y=y[True]) 

EOF
