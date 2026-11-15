import csv

def calculate_mean_price(filename):
    prices = []
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                price_str = row.get('price')
                if price_str and price_str.strip():
                    try:
                        price = float(price_str)
                        prices.append(price)
                    except ValueError:
                        continue
        
        if not prices:
            print("No valid prices found.")
            return

        mean_price = sum(prices) / len(prices)
        print(f"{mean_price:.2f}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    calculate_mean_price('data/housing_data.csv')
