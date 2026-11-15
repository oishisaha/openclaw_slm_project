import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings

warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('data/housing_dataset.csv')

# Preprocess categorical variables
categorical_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']
le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

# Features and target
X = df.drop('price', axis=1)
y = df['price']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model (RandomForestRegressor is good for capturing non-linear relationships and providing feature importance)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Feature Importance
importances = model.feature_importances_
feature_names = X.columns
feature_ranking = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)

# Prepare results file
with open('model_results.txt', 'w') as f:
    f.write("Housing Market Prediction Results\n")
    f.write("===============================\n\n")
    f.write(f"RMSE: {rmse:.2f}\n")
    f.write(f"R^2 Score: {r2:.4f}\n\n")
    f.write("Feature Importance Ranking:\n")
    for name, imp in feature_ranking:
        f.write(f"{name}: {imp:.4f}\n")

print(f"Model training complete.")
print(f"RMSE: {rmse}")
print(f"R2: {r2}")
