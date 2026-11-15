import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

train_df = pd.read_csv('data/german_train_80.csv')
val_df = pd.read_csv('data/german_val_20.csv')

X_train = train_df.drop(columns=['target_good'])
y_train = train_df['target_good']
X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

model = RandomForestClassifier(
    n_estimators=300,
    criterion='gini',
    max_depth=5,
    min_samples_leaf=5,
    min_samples_split=2,
    random_state=42
)

model.fit(X_train, y_train)

# predict_proba returns [prob_0, prob_1]
val_probs = model.predict_proba(X_val)[:, 1]
val_auc = roc_auc_score(y_val, val_probs)

print(f"{val_auc:.4f}")
