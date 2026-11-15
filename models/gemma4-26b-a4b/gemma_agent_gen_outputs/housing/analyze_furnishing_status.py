import pandas as pd

def analyze_furnishing_status(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Calculate average price by furnishingstatus
        avg_prices = df.groupby('furnishingstatus')['price'].mean().reset_index()
        avg_prices.columns = ['Furnishing Status', 'Average Price']
        
        # Sort by price for better presentation
        avg_prices = avg_prices.sort_values(by='Average Price', ascending=False)
        
        print("Average Housing Prices by Furnishing Status:")
        for index, row in avg_prices.iterrows():
            print(f"- {row['Furnishing Status']}: {row['Average Price']:,.2f}")
        
        # Calculate counts to provide context
        counts = df['furnishingstatus'].value_counts().reset_index()
        counts.columns = ['Furnishing Status', 'Count']
        
        print("\nCounts of Houses per Furnishing Status:")
        for index, row in counts.iterrows():
            print(f"- {row['Furnishing Status']}: {row['Count']}")
        
        return avg_prices, counts

    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    csv_file = 'data/housing_data.csv'
    avg_prices, counts = analyze_furnishing_status(csv_file)
