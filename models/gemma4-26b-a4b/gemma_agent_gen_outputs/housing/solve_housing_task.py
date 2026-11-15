import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def main():
    # Load data
    try:
        df = pd.read_csv('data/housing_data.csv')
    except FileNotFoundError:
        print("Error: data/housing_data.csv not found.")
        return

    # Required columns
    features = ['area', 'bedrooms', 'bathrooms', 'stories']
    target = 'price'

    # 1. Filter columns and drop rows with missing values in these columns
    cols_to_use = features + [target]
    df_subset = df[cols_to_use].dropna()

    if df_subset.empty:
        print("Error: No data left after dropping missing values.")
        return

    # 2. Prepare X and y
    X = df_subset[features]
    y = df_subset[target]

    # 3. Split data 80/20 train/test with random_state=42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    # 4. Build linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 5. Predict and evaluate using RMSE
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    # 6. Output result
    print(f"@model_rmse[{rmse:.2f}]")

if __name__ == "__main__":
    main()
