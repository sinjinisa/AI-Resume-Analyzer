
import csv
import shutil
from pathlib import Path

# Step 1: Locate the CSV file
project_folder = Path(__file__).resolve().parent

csv_path = (
    project_folder / "data" / "skill_dictionary.csv"
)

# Step 2: Read the CSV records
with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file)
    rows = list(reader)

print("Original number of records:", len(rows))
print("First records:", rows[:3])

# Step 3: Remove empty records
rows = [
    row for row in rows
    if row and any(cell.strip() for cell in row)
]

# Step 4: Find the correct header
expected_header = ["skill", "category", "aliases"]

header_index = None

for index, row in enumerate(rows):
    cleaned_row = [cell.strip().lower() for cell in row]

    if cleaned_row == expected_header:
        header_index = index
        break

if header_index is None:
    raise ValueError("Correct CSV header not found.")

# Step 5: Keep the header and skill records
clean_rows = rows[header_index:]

# Step 6: Validate the number of columns
for row in clean_rows:
    if len(row) != 3:
        raise ValueError(f"Invalid CSV row: {row}")

# Step 7: Create a backup before changing the file
backup_path = (
    project_folder / "data" / "skill_dictionary_backup.csv"
)

shutil.copy2(csv_path, backup_path)

# Step 8: Save the corrected CSV
with open(csv_path, "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(clean_rows)

print("\nCSV repaired successfully!")
print("Columns:", clean_rows[0])
print("Total skills:", len(clean_rows) - 1)
print("Backup saved:", backup_path)
