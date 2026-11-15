import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# Load data
train_df = pd.read_csv('data/german_train_80.csv')
val_df = pd.read_csv('data/german_val_20.csv')

X_train = train_df.drop(columns=['target_good'])
y_train = train_df['target_good']
X_val = val_df.drop(columns=['target_good'])
y_val = val_df['target_good']

# Model from C09
model = RandomForestClassifier(
    n_estimators=300,
    criterion='gini',
    max_depth=5,
    min_samples_leaf=5,
    min_samples_split=2,
    random_state=42
)

model.fit(X_train, y_train)

# Threshold sweep
val_probs = model.predict_proba(X_val)[:, 1]
thresholds = np.arange(0.01, 1.0, 0.01)
costs = []

for t in thresholds:
    preds = (val_probs >= t).astype(int)
    fn = np.sum((y_val == 1) & (preds == 0))
    fp = np.sum((y_val == 0) & (preds == 1))
    costs.append(5 * fn + fp)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(thresholds, costs, label='RF Classifier Cost', color='purple')

# Find and mark minimum point
min_idx = np.argmin(costs)
plt.plot(thresholds[min_idx], costs[min_idx], marker='o', markersize=10, 
         color='red', label=f'Min at {thresholds[min_idx]:.2f}')

plt.title('Random Forest Classifier: Cost vs Threshold')
plt.xlabel('Threshold')
plt.ylabel('Cost (5*FN + 1*FP)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('rf_cost_vs_threshold.png')
