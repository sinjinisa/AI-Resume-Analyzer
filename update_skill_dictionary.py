
import csv
import shutil
from pathlib import Path


# STEP 1: Locate the project folder
PROJECT_FOLDER = Path(__file__).resolve().parent

# STEP 2: Locate the skill dictionary
SKILL_FILE = PROJECT_FOLDER / "data" / "skill_dictionary.csv"

# STEP 3: Define the new skills
new_skills = [
    (
        "LLM",
        "AI and ML",
        "llm|large language model|large language models"
    ),
    (
        "RAG",
        "AI and ML",
        "rag|retrieval augmented generation|retrieval-augmented generation"
    ),
    (
        "APIs",
        "Backend",
        "api|apis|rest api|rest apis"
    ),
    (
        "Transformers",
        "AI and ML",
        "transformers|transformer models"
    ),
    (
        "Hugging Face",
        "AI and ML",
        "hugging face|huggingface|hugging-face"
    ),
    (
        "OpenCV",
        "Computer Vision",
        "opencv|open cv"
    ),
    (
        "CNN",
        "Computer Vision",
        "cnn|convolutional neural network"
    ),
    (
        "YOLO",
        "Computer Vision",
        "yolo|you only look once"
    )
]


def update_dictionary():

    # STEP 4: Check that the file exists
    if not SKILL_FILE.is_file():
        raise FileNotFoundError(
            f"Skill dictionary not found: {SKILL_FILE}"
        )

    # STEP 5: Read the existing CSV
    with open(
        SKILL_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.reader(file)

        # Ignore completely empty records
        rows = [
            row for row in reader
            if any(cell.strip() for cell in row)
        ]

    # STEP 6: Validate the CSV header
    expected_header = ["skill", "category", "aliases"]

    if not rows:
        raise ValueError("Skill dictionary is empty.")

    header = [
        value.strip().lower()
        for value in rows[0]
    ]

    if header != expected_header:
        raise ValueError(
            f"Invalid CSV header: {rows[0]}"
        )

    # STEP 7: Validate existing data
    existing_rows = rows[1:]

    for row in existing_rows:
        if len(row) != 3:
            raise ValueError(
                f"Invalid skill record: {row}"
            )

    # STEP 8: Collect existing skill names
    existing_names = {
        row[0].strip().casefold()
        for row in existing_rows
    }

    # STEP 9: Find skills not already present
    additions = []

    for skill in new_skills:

        name = skill[0].casefold()

        if name not in existing_names:
            additions.append(skill)
            existing_names.add(name)

    # STEP 10: Back up the original dataset
    backup_path = (
        PROJECT_FOLDER
        / "data"
        / "skill_dictionary_before_alignment.csv"
    )

    if not backup_path.exists():
        shutil.copy2(SKILL_FILE, backup_path)

    # STEP 11: Write the updated dictionary
    with open(
        SKILL_FILE,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(expected_header)
        writer.writerows(existing_rows)
        writer.writerows(additions)

    # STEP 12: Display results
    print("SKILL DICTIONARY UPDATED!")

    print("Previous skills:", len(existing_rows))
    print("New skills added:", len(additions))
    print(
        "Total skills:",
        len(existing_rows) + len(additions)
    )

    print("\nNewly added skills:")

    for skill in additions:
        print("-", skill[0])

    print("\nBackup:", backup_path)


if __name__ == "__main__":
    update_dictionary()
