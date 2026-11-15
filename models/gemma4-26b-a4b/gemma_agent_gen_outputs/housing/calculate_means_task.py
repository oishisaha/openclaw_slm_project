import csv

def calculate_means(file_path):
    prices_by_status = {'furnished': [], 'semi-furnished': [], 'unfurnished': []}
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                status = row['furnishingstatus'].strip().lower()
                price = float(row['price'])
                if status in prices_by_status:
                    prices_by_status[status].append(price)
        
        means = {}
        for status, prices in prices_by_status.items():
            if prices:
                means[status] = round(sum(prices) / len(prices), 2)
            else:
                means[status] = 0.0
        
        return means
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    results = calculate_means('data/housing_data.csv')
    print(results)
