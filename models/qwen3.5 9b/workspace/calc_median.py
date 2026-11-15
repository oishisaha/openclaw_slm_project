import csv

areas = []
with open('data/housing_dataset.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            area = float(row['area'])
            areas.append(area)
        except (ValueError, KeyError):
            continue

areas.sort()
n = len(areas)
if n % 2 == 0:
    median = (areas[n//2 - 1] + areas[n//2]) / 2
else:
    median = areas[n // 2]

print(f"@median_area[{round(median, 2)}]")