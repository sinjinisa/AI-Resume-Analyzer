
import csv
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# STEP 1: Locate the job dataset
PROJECT_FOLDER = Path(__file__).resolve().parent

JOB_FILE = PROJECT_FOLDER / "data" / "job_roles.csv"


def load_job_roles():

    # STEP 2: Check the file exists
    if not JOB_FILE.is_file():
        raise FileNotFoundError(
            f"Job dataset not found: {JOB_FILE}"
        )

    jobs = []

    # STEP 3: Read the CSV
    with open(
        JOB_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(
            line for line in file if line.strip()
        )

        # STEP 4: Validate the columns
        required_columns = {
            "job_role",
            "required_skills",
            "description"
        }

        if reader.fieldnames is None:
            raise ValueError("Job dataset is empty.")

        reader.fieldnames = [
            name.strip().lower()
            for name in reader.fieldnames
        ]

        if set(reader.fieldnames) != required_columns:
            raise ValueError(
                f"Invalid columns: {reader.fieldnames}"
            )

        # STEP 5: Build job dictionaries
        for row in reader:

            if None in row or any(
                value is None for value in row.values()
            ):
                raise ValueError(
                    f"Invalid CSV row: {row}"
                )

            job_name = row["job_role"].strip()

            skills = [
                skill.strip()
                for skill in row["required_skills"].split("|")
                if skill.strip()
            ]

            description = row["description"].strip()

            if not job_name or not skills or not description:
                raise ValueError(
                    f"Incomplete job record: {row}"
                )

            jobs.append({
                "job_role": job_name,
                "required_skills": skills,
                "description": description
            })

    if not jobs:
        raise ValueError("No job roles found.")

    return jobs


def match_resume_to_jobs(resume_skills):

    # STEP 6: Load the five job roles
    jobs = load_job_roles()

    # STEP 7: Normalize candidate skills
    resume_set = {
        skill.strip().casefold()
        for skill in resume_skills
        if skill.strip()
    }

    # STEP 8: Prepare the job documents
    job_documents = []

    for job in jobs:

        normalized_skills = [
            skill.casefold()
            for skill in job["required_skills"]
        ]

        # Remove duplicate terms, preserving order
        normalized_skills = list(
            dict.fromkeys(normalized_skills)
        )

        job_documents.append(normalized_skills)

    # STEP 9: Create the TF-IDF vectorizer
    # Every complete skill name is one term
    vectorizer = TfidfVectorizer(
        analyzer=lambda terms: terms,
        lowercase=False
    )

    # STEP 10: Learn weights from job requirements
    job_vectors = vectorizer.fit_transform(
        job_documents
    )

    # STEP 11: Vectorize candidate skills
    resume_vector = vectorizer.transform(
        [sorted(resume_set)]
    )

    # STEP 12: Calculate cosine similarities
    similarities = cosine_similarity(
        resume_vector,
        job_vectors
    )[0]

    results = []

    # STEP 13: Analyze every job role
    for job, similarity in zip(jobs, similarities):

        required = job["required_skills"]

        # Find skills already detected
        matched = [
            skill
            for skill in required
            if skill.casefold() in resume_set
        ]

        # Find missing required skills
        missing = [
            skill
            for skill in required
            if skill.casefold() not in resume_set
        ]

        # Calculate skill coverage
        coverage = (
            100 * len(matched) / len(required)
        )

        # STEP 14: Store the analysis
        results.append({
            "job_role": job["job_role"],
            "similarity": round(
                float(similarity), 4
            ),
            "skill_coverage_percent": round(
                coverage, 1
            ),
            "matched_skills": matched,
            "missing_skills": missing
        })

    # STEP 15: Rank roles by similarity
    results.sort(
        key=lambda item: (
            -item["similarity"],
            -item["skill_coverage_percent"],
            item["job_role"]
        )
    )

    return results
