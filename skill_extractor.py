
import csv
import re
from pathlib import Path


# Locate the project folder
PROJECT_FOLDER = Path(__file__).resolve().parent

# Locate the skill dictionary
SKILL_FILE = (
    PROJECT_FOLDER / "data" / "skill_dictionary.csv"
)


def extract_skills(text):

    # STEP 1: Validate input
    if not isinstance(text, str):
        raise TypeError("Resume text must be a string.")

    detected_skills = []

    # STEP 2: Verify the CSV exists
    if not SKILL_FILE.is_file():
        raise FileNotFoundError(
            f"Skill dictionary not found: {SKILL_FILE}"
        )

    # STEP 3: Open the CSV file
    with open(
        SKILL_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        # STEP 4: Create the CSV reader
        reader = csv.DictReader(file)

        # STEP 5: Check for an empty CSV
        if reader.fieldnames is None:
            raise ValueError(
                "Skill dictionary is empty."
            )

        # STEP 6: Normalize column names
        reader.fieldnames = [
            name.strip().lower()
            for name in reader.fieldnames
        ]

        # STEP 7: Validate required columns
        required_columns = {
            "skill",
            "category",
            "aliases"
        }

        if not required_columns.issubset(
            set(reader.fieldnames)
        ):
            raise ValueError(
                f"Invalid CSV columns: {reader.fieldnames}"
            )

        # STEP 8: Read each skill
        for row in reader:

            skill_name = (row["skill"] or "").strip()

            if not skill_name:
                continue

            # STEP 9: Get alternative spellings
            aliases = (row["aliases"] or "").split("|")
            aliases.append(skill_name)

            # STEP 10: Search for matching skills
            for alias in aliases:

                alias = alias.strip()

                if not alias:
                    continue

                pattern = (
                    r"(?<![a-z0-9])"
                    + re.escape(alias)
                    + r"(?![a-z0-9])"
                )

                if re.search(
                    pattern,
                    text,
                    re.IGNORECASE
                ):
                    detected_skills.append(skill_name)
                    break

    # STEP 11: Remove duplicates and sort
    detected_skills = sorted(
        set(detected_skills),
        key=str.lower
    )

    return detected_skills

