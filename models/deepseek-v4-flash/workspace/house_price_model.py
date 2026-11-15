"""
House Price Prediction Pipeline
================================
Dataset: housing_dataset.csv (545 rows, 13 columns)
Target: price

Pipeline steps:
  1. Load & inspect data
  2. Preprocess categorical variables (one-hot encode)
  3. Split train/test (80/20)
  4. Train Linear Regression and XGBoost Regressor
  5. Evaluate on both sets (R², RMSE, MAE, MAPE)
  6. Feature importance analysis (coefficients / gain)
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# ── 1. Load ──────────────────────────────────────────────────────────────────
df = pd.read_csv("data/housing_dataset.csv")
print("=" * 60)
print("HOUSE PRICE PREDICTION — FULL PIPELINE REPORT")
print("=" * 60)
print(f"\nDataset shape: {df.shape}")
print(f"Missing values:\n{df.isnull().sum()}")
print(f"\nTarget distribution (price):")
print(df['price'].describe().to_string())

# ── 2. Preprocess ────────────────────────────────────────────────────────────
# Separate features and target
X = df.drop('price', axis=1)
y = df['price']

# Identify column types
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

print(f"\nNumeric features  ({len(numeric_features)}): {numeric_features}")
print(f"Categorical features ({len(categorical_features)}): {categorical_features}")

# Unique values in each categorical column
for col in categorical_features:
    print(f"  {col}: {X[col].unique()}")

# Build preprocessing: scale numeric, one-hot encode categorical
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Apply preprocessing
X_processed = preprocessor.fit_transform(X)

# Get feature names after encoding
cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
all_feature_names = numeric_features + list(cat_feature_names)

X_processed_df = pd.DataFrame(X_processed, columns=all_feature_names)
print(f"\nProcessed feature matrix: {X_processed_df.shape}")
print(f"Features: {list(X_processed_df.columns)}")

# ── 3. Train/Test Split ──────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_processed_df, y, test_size=0.2, random_state=42
)
print(f"\nTrain size: {len(X_train)} | Test size: {len(X_test)}")

# ── 4. Train Models ──────────────────────────────────────────────────────────
from xgboost import XGBRegressor

models = {
    'Linear Regression': LinearRegression(),
    'XGBoost Regressor': XGBRegressor(
        n_estimators=300, max_depth=6, learning_rate=0.08,
        subsample=0.8, colsample_bytree=0.8,
        random_state=42, verbosity=0
    )
}

results = {}
feature_importances = {}

for name, model in models.items():
    print(f"\n{'─' * 50}")
    print(f"Training: {name}")
    model.fit(X_train, y_train)

    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Metrics
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2  = r2_score(y_test, y_test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse  = np.sqrt(mean_squared_error(y_test, y_test_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae  = mean_absolute_error(y_test, y_test_pred)

    # MAPE (avoid division by zero)
    def mape(y_true, y_pred):
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    train_mape = mape(y_train, y_train_pred)
    test_mape  = mape(y_test, y_test_pred)

    results[name] = {
        'Train R²':  train_r2,
        'Test R²':   test_r2,
        'Train RMSE': train_rmse,
        'Test RMSE':  test_rmse,
        'Train MAE':  train_mae,
        'Test MAE':   test_mae,
        'Train MAPE(%)': train_mape,
        'Test MAPE(%)':  test_mape,
    }

    # Feature importance
    if name == 'Linear Regression':
        coefs = pd.Series(model.coef_, index=all_feature_names)
        fi = coefs.abs().sort_values(ascending=False)
        feature_importances[name] = (coefs, 'Coefficient (absolute)')
    else:
        fi = pd.Series(model.feature_importances_, index=all_feature_names).sort_values(ascending=False)
        feature_importances[name] = (fi, 'Gain')

    print(f"  Train R²:    {train_r2:.4f}   | Test R²:     {test_r2:.4f}")
    print(f"  Train RMSE:  {train_rmse:,.0f} | Test RMSE:   {test_rmse:,.0f}")
    print(f"  Train MAE:   {train_mae:,.0f}  | Test MAE:    {test_mae:,.0f}")
    print(f"  Train MAPE:  {train_mape:.2f}% | Test MAPE:   {test_mape:.2f}%")

# ── 5. Evaluation Summary Table ──────────────────────────────────────────────
metrics_order = ['Train R²', 'Test R²', 'Train RMSE', 'Test RMSE',
                 'Train MAE', 'Test MAE', 'Train MAPE(%)', 'Test MAPE(%)']

eval_table = pd.DataFrame(results, index=metrics_order)
print(f"\n{'=' * 60}")
print("EVALUATION METRICS SUMMARY")
print(f"{'=' * 60}")
print(eval_table.to_string())

# ── 6. Feature Importance ────────────────────────────────────────────────────
print(f"\n{'=' * 60}")
print("FEATURE IMPORTANCE")
print(f"{'=' * 60}")
for name, (fi, label) in feature_importances.items():
    print(f"\n── {name} ── (sorted by |{label}|)")
    for feat, val in fi.head(8).items():
        print(f"  {feat:25s}  {val:>12.4f}")
    if name == 'Linear Regression':
        print(f"\n  Direction (raw coefficient):")
        raw = feature_importances[name][0]
        for feat, val in raw.sort_values(key=abs, ascending=False).head(8).items():
            direction = "+" if val > 0 else "−"
            print(f"  {feat:25s}  {direction}  {abs(val):>10.2f}")

# ── 7. Predicted vs Actual (sample) ──────────────────────────────────────────
best_model = list(models.values())[-1]  # XGBoost
y_test_pred_best = best_model.predict(X_test)
comparison = pd.DataFrame({
    'Actual': y_test.values,
    'Predicted': y_test_pred_best,
    'Abs_Error': np.abs(y_test.values - y_test_pred_best),
    'Error_%': np.abs((y_test.values - y_test_pred_best) / y_test.values) * 100
}).sort_index()

print(f"\n{'=' * 60}")
print("PREDICTED vs ACTUAL (first 10 test samples)")
print(f"{'=' * 60}")
print(comparison.head(10).to_string())
print(f"\n  Average absolute error: {comparison['Abs_Error'].mean():,.0f}")
print(f"  Average error %:        {comparison['Error_%'].mean():.2f}%")

print(f"\n{'=' * 60}")
print("DONE — full pipeline complete")
