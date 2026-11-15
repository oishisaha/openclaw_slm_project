import csv

file_path = '/home/mosh/.openclaw/workspace/data/housing_data.csv'
count = 0
total = 0

with open(file_path, mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += 1
        if row['airconditioning'] == 'yes':
            count += 1

if total > 0:
    proportion = count / total
    print(f"{proportion:.2f}")
else:
    print("0.00")
