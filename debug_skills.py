
import csv
from skill_extractor import SKILL_FILE, extract_skills

print("SKILL DICTIONARY DEBUGGING")
print("---------------------------")

# Step 1: Display CSV location
print("CSV location:", SKILL_FILE)

# Step 2: Check file existence
print("File exists:", SKILL_FILE.is_file())

if SKILL_FILE.is_file():

    # Step 3: Open CSV file
    with open(SKILL_FILE, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)
        rows = list(reader)

        # Step 4: Check CSV structure
        print("CSV columns:", reader.fieldnames)
        print("Total dictionary rows:", len(rows))

        # Step 5: Display sample records
        print("\nFirst 3 dictionary records:")

        for row in rows[:3]:
            print(row)

    # Step 6: Test skill extraction
    print("\nTesting skill extraction:")

    sample = "I know Python, SQL and Docker"
    detected = extract_skills(sample)

    print("Input:", sample)
    print("Detected:", detected)
