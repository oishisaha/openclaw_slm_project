import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_csv("data/insurance.csv")
X = df[["age", "bmi", "children"]]
y = df["charges"]

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)

print(f"R-squared: {r2:.2f}")
print(f"@r_squared[{r2:.2f}]")
