
import csv

from skill_extractor import SKILL_FILE, extract_skills
from text_cleaner import clean_resume_text
from test_job_dataset import load_job_roles


def main():

    print("DATASET ALIGNMENT TEST")
    print("----------------------")

    # STEP 1: Open the skill dictionary
    with open(
        SKILL_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(
            line for line in file if line.strip()
        )

        # STEP 2: Validate the CSV columns
        required_columns = {
            "skill",
            "category",
            "aliases"
        }

        if reader.fieldnames is None:
            raise ValueError("Skill dictionary is empty.")

        reader.fieldnames = [
            name.strip().lower()
            for name in reader.fieldnames
        ]

        if not required_columns.issubset(
            set(reader.fieldnames)
        ):
            raise ValueError(
                f"Invalid CSV columns: {reader.fieldnames}"
            )

        # STEP 3: Load all dictionary skills
        dictionary_skills = set()

        for row in reader:

            if None in row:
                raise ValueError(
                    f"Malformed skill dictionary row: {row}"
                )

            skill_name = (row["skill"] or "").strip()

            if skill_name:
                dictionary_skills.add(skill_name.casefold())

    # STEP 4: Load job-role dataset
    jobs = load_job_roles()

    print("Dictionary skills:", len(dictionary_skills))
    print("Job roles:", len(jobs))

    # STEP 5: Check every job role
    all_missing = []

    for job in jobs:

        role_name = job["job_role"]

        required = job["required_skills"]

        missing = [
            skill
            for skill in required
            if skill.strip().casefold()
            not in dictionary_skills
        ]

        print("\n------------------------------")
        print("Job Role:", role_name)
        print("Required skills:", len(required))

        if missing:
            print("Missing skills:", missing)
            all_missing.extend(missing)

        else:
            print("Status: ALIGNED")

    # STEP 6: Verify minimum job count
    assert len(jobs) >= 5, (
        "At least five job roles are required."
    )

    # STEP 7: Verify dictionary alignment
    assert not all_missing, (
        f"Missing skills in dictionary: {all_missing}"
    )

    print("\nAll job-role datasets are aligned!")

    # STEP 8: Test the eight newly added skills
    sample_text = """
    I have experience with LLM, RAG, REST APIs,
    Transformers, Hugging Face, OpenCV,
    CNN and YOLO.
    """

    # STEP 9: Clean sample text
    cleaned_text = clean_resume_text(sample_text)

    # STEP 10: Extract skills
    detected_skills = extract_skills(cleaned_text)

    # STEP 11: Define expected skills
    expected_skills = {
        "LLM",
        "RAG",
        "APIs",
        "Transformers",
        "Hugging Face",
        "OpenCV",
        "CNN",
        "YOLO"
    }

    print("\nDETECTED NEW SKILLS:")
    print("----------------------")

    for skill in sorted(detected_skills):
        print("-", skill)

    # STEP 12: Check extraction accuracy
    missing_detected = expected_skills - set(
        detected_skills
    )

    assert not missing_detected, (
        f"Skills not detected: {missing_detected}"
    )

    print("\nNew skill extraction test PASSED!")

    print("\nALL DATASET ALIGNMENT TESTS PASSED!")


if __name__ == "__main__":
    main()
