import csv
import statistics

filename = 'data/housing_data.csv'
areas = []

with open(filename, mode='r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        area_val = row.get('area')
        if area_val and area_val.strip():
            try:
                areas.append(float(area_val))
            except ValueError:
                continue

if areas:
    median_area = statistics.median(areas)
    print(f"{median_area:.2f}")
else:
    print("No valid area data found.")
