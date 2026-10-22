
from pathlib import Path

from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import extract_skills
from job_matcher import match_resume_to_jobs
from roadmap_generator import generate_roadmap


def main():

    # STEP 1: Locate the sample resume
    project_folder = Path(__file__).resolve().parent

    resume_path = (
        project_folder
        / "sample_resumes"
        / "demo_resume_v2.docx"
    )

    # Use the PDF if the DOCX is missing
    if not resume_path.is_file():
        resume_path = (
            project_folder
            / "sample_resumes"
            / "demo_resume.pdf"
        )

    if not resume_path.is_file():
        print("ERROR: No sample resume found.")
        return

    # STEP 2: Extract text
    raw_text = extract_resume_text(resume_path)

    # STEP 3: Clean text
    cleaned_text = clean_resume_text(raw_text)

    # STEP 4: Extract skills
    candidate_skills = extract_skills(cleaned_text)

    print("DETECTED SKILLS:")
    print(candidate_skills)

    # STEP 5: Match candidate to job roles
    job_results = match_resume_to_jobs(
        candidate_skills
    )

    # STEP 6: Select target job
    target_role = "Machine Learning Engineer"

    selected_job = next(
        (
            job for job in job_results
            if job["job_role"] == target_role
        ),
        None
    )

    if selected_job is None:
        print("ERROR: Target job not found.")
        return

    # STEP 7: Display job analysis
    print("\nTARGET ROLE:", target_role)

    print(
        "Cosine similarity:",
        selected_job["similarity"]
    )

    print(
        "Skill coverage:",
        selected_job["skill_coverage_percent"],
        "%"
    )

    print(
        "Matched skills:",
        selected_job["matched_skills"]
    )

    print(
        "Missing skills:",
        selected_job["missing_skills"]
    )

    # STEP 8: Generate learning roadmap
    roadmap = generate_roadmap(
        target_role,
        selected_job["missing_skills"]
    )

    print("\nPERSONALIZED LEARNING ROADMAP")
    print("------------------------------")

    if not roadmap:
        print(
            "All listed required skills were detected."
        )

    else:

        for week in roadmap:

            print(
                f"\nWEEK {week['week']}: "
                f"{week['focus']}"
            )

            for activity in week["activities"]:
                print("-", activity)

    # STEP 9: Test roadmap output
    if selected_job["missing_skills"]:
        assert len(roadmap) == 4
    else:
        assert roadmap == []

    print("\nRoadmap generation test PASSED!")


if __name__ == "__main__":
    main()
