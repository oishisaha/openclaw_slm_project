import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

def main():
    # Load dataset
    df = pd.read_csv('data/housing_data.csv')
    
    # Handle missing values if any (though none seen in head)
    df = df.dropna()

    # Separate features and target
    X = df.drop('price', axis=1)
    y = df['price']

    # Preprocessing categorical variables
    # Categorical columns: mainroad, guestroom, basement, hotwaterheating, airconditioning, prefarea, furnishingstatus
    categorical_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea', 'furnishingstatus']
    
    # Use LabelEncoder for binary columns and OneHotEncoding for furnishingstatus
    # Or just use pd.get_dummies for simplicity across all
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a regression model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # Feature importance
    importances = model.feature_importances_
    feature_names = X.columns
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    # Prepare results for file
    results = []
    results.append("--- Housing Price Prediction Model Results ---")
    results.append(f"RMSE: {rmse:.2f}")
    results.append(f"R² Score: {r2:.4f}")
    results.append("\n--- Feature Rankings ---")
    for _, row in feature_importance_df.iterrows():
        results.append(f"{row['Feature']}: {row['Importance']:.4f}")

    # Save to file
    with open('model_results.txt', 'w') as f:
        f.write('\n'.join(results))
    
    print("Model training complete. Results saved to model_results.txt.")

if __name__ == "__main__":
    main()
