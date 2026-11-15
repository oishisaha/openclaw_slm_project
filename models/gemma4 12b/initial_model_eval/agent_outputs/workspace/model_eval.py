import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load data
df = pd.read_csv('data/housing_dataset.csv')

# Features and Target
features = ['area', 'bedrooms', 'bathrooms', 'stories']
target = 'price'

# Drop rows with missing values in the relevant columns
df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

# Split data (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build and fit model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"{rmse:.2f}")
