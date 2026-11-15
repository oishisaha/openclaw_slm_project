import csv

# Read the CSV file and calculate mean price ignoring missing values
prices = []

with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Parse price, ignore rows with missing values
        try:
            price = float(row['price'])
            prices.append(price)
        except (ValueError, KeyError):
            continue

# Calculate mean if there are any valid prices
if len(prices) > 0:
    mean_price = sum(prices) / len(prices)
else:
    mean_price = None

print(f"@mean_price[{round(mean_price, 2)}]") if mean_price else print("@mean_price[null]")
