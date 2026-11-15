import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('data/housing_dataset.csv')

# Filter rows without missing values in price, area, and bathrooms columns
clean_df = df.dropna(subset=['price', 'area', 'bathrooms'])

print(f"Total rows: {len(df)}")
print(f"After filtering (no NaN in price, area, bathrooms): {len(clean_df)}")

# Check for missing values
missing_count = clean_df[['price', 'area', 'bathrooms']].isnull().sum()
print(missing_count)

if len(clean_df) == 0:
    print("No valid rows found after filtering!")
else:
    # Perform multiple linear regression using statsmodels for p-values and R-squared
    try:
        from statsmodels.formula.api import ols
        
        model = ols('price ~ area + bathrooms', data=clean_df).fit()
        
        print("\nModel summary:")
        print(model.summary())
        
        # Get coefficients, p-values for predictors (excluding intercept)
        params = model.params.values[1:]  # Exclude intercept
        pvalues = model.pvalues.values[1:]  # Exclude intercept
        
        areasignificant = 'yes' if pvalues[0] < 0.05 else 'no'
        bathrooms_significant = 'yes' if pvalues[1] < 0.05 else 'no'
        
        print(f"\nArea coefficient: {model.params['area']}, P-value: {pvalues[0]:.6f}")
        print(f"Bathrooms coefficient: {model.params['bathrooms']}, P-value: {pvalues[1]:.6f}")
        
        r_squared = model.rsquared
        
        print(f"\nR-squared value: {r_squared:.4f}")
        
    except ImportError:
        from sklearn.linear_model import LinearRegression
        
        X = clean_df[['area', 'bathrooms']]
        y = clean_df['price']
        
        model = LinearRegression()
        model.fit(X, y)
        
        print(f"\nModel coefficients (intercept={model.intercept_:.2f}, area={model.coef_[0]:.4f}, bathrooms={model.coef_[1]:.4f})")
        
        # For p-values and R-squared with sklearn, we need statsmodels or scipy for inference
        try:
            from statsmodels.api import OLS
        
            ols_model = OLS(y, X).fit()
            
            params = ols_model.params.values[1:]  # Exclude intercept (which is index 0)
            pvalues = ols_model.pvalues.values[1:]  # Exclude intercept
            
            areasignificant = 'yes' if pvalues[0] < 0.05 else 'no'
            bathrooms_significant = 'yes' if pvalues[1] < 0.05 else 'no'
            
            print(f"\nArea coefficient: {ols_model.params['area']}, P-value: {pvalues[0]:.6f}")
            print(f"Bathrooms coefficient: {ols_model.params['bathrooms']}, P-value: {pvalues[1]:.6f}")
            r_squared = ols_model.rsquared
            
        except ImportError:
            # Basic R-squared calculation without p-values available in sklearn alone
            from scipy import stats
            correlations = np.corrcoef(clean_df[['area', 'price']].to_numpy()[:,0], 
                                       clean_df['price']).diagonal()[1]  # Simplified - actually area & price
            
    print(f"\nFormatted output:")
    formatted_area_significant = 'yes' if areasignificant == 'yes' else 'no'  
    formatted_bathrooms_significant = 'yes' if bathrooms_significant == 'yes' else 'no'
    final_r_squared = r_squared
    
# Output in the required format
print(f"\n@significant_predictor[{formatted_area_significant},{formatted_bathrooms_significant}] @r_squared[{final_r_squared:.4f}]")
