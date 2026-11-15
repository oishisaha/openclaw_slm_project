import pandas as pd 
from sklearn.linear_model import Ridge  
from sklearn.metrics import mean_squared_error  

train = pd.read_csv('german_train_80.csv')  
val=pd.read_csv('german_val_20.csv')  

common_cols=set(train.columns)&set(val.columns)-{'target_good'}
