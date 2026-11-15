import pandas as pd
import numpy as np

def analyze_housing_prices(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'price' not in df.columns:
            print(f"Error: 'price' column not found in {file_path}")
            return

        prices = df['price']

        min_price = prices.min()
        max_price = prices.max()
        avg_price = prices.mean()
        median_price = prices.median()

        # Outlier detection using IQR
        q1 = prices.quantile(0.25)
        q3 = prices.quantile(0.75)
        iqr = q3 - q1
        upper_bound = q3 + 1.5 * iqr
        lower_bound = q1 - 1.5 * iqr

        outliers = prices[prices > upper_bound]
        num_outliers = len(outliers)
        
        print(f"Minimum Price: {min_price:,.2f}")
        print(f"Maximum Price: {max_price:,.2f}")
        print(f"Average Price: {avg_price:,.2f}")
        print(f"Median Price: {median_price:,.2f}")
        print(f"\nOutlier Analysis:")
        print(f"IQR: {iqr:,.2f}")
        print(f"Upper Bound (Q3 + 1.5*IQR): {upper_bound:,.2f}")
        print(f"Number of expensive outliers (> {upper_bound:,.2f}): {num_outliers}")
        
        if num_outliers > 0:
            print("\nTop 5 Expensive Outliers:")
            print(outliers.sort_values(ascending=False).head(5))
            print("\nConclusion: Expensive outliers exist.")
        else:
            print("\nConclusion: No expensive outliers detected based on the IQR method.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    analyze_housing_prices('data/housing_data.csv')
