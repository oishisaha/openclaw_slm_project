import csv


def calculate_price_per_sqft(price, area):
    if float(area) > 0 and not (float('nan') in price or inf):

        return round(float(price) / float(area), 2)
    
    

if __name__ == "__main__":
    # Read the CSV file 
    with open('/home/vboxuser/.openclaw/workspace/data/housing_dataset_chatgpt.csv', 'r') as f:
        
reader = csv.DictReader(f)
