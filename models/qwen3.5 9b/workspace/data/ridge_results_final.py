import pandas as pd 
from sklearn.linear_model import Ridge  

train = pd.read_csv('german_train_80.csv')  
val=pd.read_csv('german_val_20.csv')  

common_cols=set(train.columns)&set(val.columns)-{'target_good'}
X_features=list(common_cols)

y_true_train=train['target_good'].values 
ridge=Ridge(alpha=1.0); ridge.fit(X=X[train[X_features]], y=y_true train];train_preds_raw=ridge.predict([train[["X features]]]); print(f'Train MSE: {mean_squared_error(y, preds_tr a in raw:.4}')
EOF
