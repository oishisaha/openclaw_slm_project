import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the data
df = pd.read_csv('data/housing_dataset.csv')

# Select only the relevant columns for our model
features_df = df[['price', 'area', 'bedrooms', 'bathrooms', 'stories']]

# Ignore rows with missing values in any of these columns
cleaned_df = features_df.dropna()

X = cleaned_df[['area', 'bedrooms', 'bathrooms', 'stories']]
y = cleaned_df['price']

print(f"Total data points: {len(features_df)}")
print(f"Clean data points (no missing values): {len(cleaned_df)}")

# Split the data 80/20 with random_state=42
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on test set
y_pred = model.predict(X_test)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"\nModel coefficients:")
for feature, coef in zip(['area', 'bedrooms', 'bathrooms', 'stories'], model.coef_):
    print(f"  {feature}: {coef:.2f}")
print(f"\nIntercept: {model.intercept_:.2f}")

# Report the answer
print(f"@model_rmse[{rmse:.2f}]")
