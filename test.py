import os
import pandas
from extract_info_from_html import get_info_from_html

terms = []

for i in range(12, 17):
    for k in ["s", "u", "f"]:
        terms.append(f"term_{i}{k}")

total_rows = 0
for t in terms:
    data_path = t + "_scraped_data.csv"
    evaluation_path = t + "_course_evaluations.csv"
    if os.path.exists(data_path) and os.path.exists(evaluation_path):
        d = len(pandas.read_csv(data_path))
        e = len(pandas.read_csv(evaluation_path))
        total_rows += d
        print(f"{t}: {e}/{d} rows collected ({e/d*100:.1f}%)")
print(total_rows)