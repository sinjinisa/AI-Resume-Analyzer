
import csv
from pathlib import Path


# STEP 1: Locate the project folder
PROJECT_FOLDER = Path(__file__).resolve().parent

# STEP 2: Locate the job-role dataset
JOB_FILE = PROJECT_FOLDER / "data" / "job_roles.csv"


def load_job_roles():

    # STEP 3: Check whether the CSV exists
    if not JOB_FILE.is_file():
        raise FileNotFoundError(
            f"Job-role dataset not found: {JOB_FILE}"
        )

    # STEP 4: Open the CSV
    with open(
        JOB_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(
    line for line in file if line.strip()
)

        # STEP 5: Check the CSV headings
        expected_columns = [
            "job_role",
            "required_skills",
            "description"
        ]

        if reader.fieldnames != expected_columns:
            raise ValueError(
                f"Invalid CSV columns: {reader.fieldnames}"
            )

        # STEP 6: Read all job-role records
        jobs = []

        for row in reader:

            # Detect incorrectly formatted records
            if None in row:
                raise ValueError(
                    f"Malformed CSV row: {row}"
                )

            job_name = row["job_role"].strip()

            # Convert the skills string into a list
            required_skills = [
                skill.strip()
                for skill in row["required_skills"].split("|")
                if skill.strip()
            ]

            description = row["description"].strip()

            # Validate the record
            if not job_name or not required_skills or not description:
                raise ValueError(
                    f"Incomplete job record: {row}"
                )

            # Create a structured Python dictionary
            job_data = {
                "job_role": job_name,
                "required_skills": required_skills,
                "description": description
            }

            jobs.append(job_data)

    return jobs


def main():

    # STEP 7: Load the dataset
    jobs = load_job_roles()

    print("JOB ROLE DATASET LOADED SUCCESSFULLY!")

    print("\nTotal job roles:", len(jobs))

    # STEP 8: Display job details
    for index, job in enumerate(jobs, start=1):

        print("\n------------------------------")
        print("Job Number:", index)
        print("Job Role:", job["job_role"])
        print("Required Skills:", job["required_skills"])
        print("Description:", job["description"])

    # STEP 9: Verify the minimum role count
    assert len(jobs) >= 5, (
        "At least five job roles are required."
    )

    print("\nJob-role dataset test PASSED!")


if __name__ == "__main__":
    main()
