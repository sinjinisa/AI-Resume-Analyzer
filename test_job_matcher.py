
from pathlib import Path

from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import extract_skills
from job_matcher import match_resume_to_jobs


def main():

    # STEP 1: Locate the project directory
    project_folder = Path(__file__).resolve().parent

    # STEP 2: Locate a sample resume
    resume_path = (
        project_folder
        / "sample_resumes"
        / "demo_resume_v2.docx"
    )

    # Use the previously tested PDF if needed
    if not resume_path.is_file():
        resume_path = (
            project_folder
            / "sample_resumes"
            / "demo_resume.pdf"
        )

    if not resume_path.is_file():
        print("ERROR: Sample resume not found.")
        return

    print("RESUME:", resume_path.name)

    # STEP 3: Extract text
    raw_text = extract_resume_text(resume_path)

    # STEP 4: Clean text
    cleaned_text = clean_resume_text(raw_text)

    # STEP 5: Extract technical skills
    candidate_skills = extract_skills(cleaned_text)

    print("\nDETECTED SKILLS:")

    for skill in candidate_skills:
        print("-", skill)

    # STEP 6: Calculate job matches
    results = match_resume_to_jobs(candidate_skills)

    # STEP 7: Check result count
    assert len(results) == 5

    # STEP 8: Display all job similarities
    print("\nJOB MATCHING RESULTS")
    print("--------------------")

    for result in results:

        print("\nJob:", result["job_role"])

        print(
            "Cosine similarity:",
            result["similarity"]
        )

        print(
            "Skill coverage:",
            result["skill_coverage_percent"],
            "%"
        )

        print(
            "Matched skills:",
            result["matched_skills"]
        )

        print(
            "Missing skills:",
            result["missing_skills"]
        )

    # STEP 9: Recommend up to three roles
    # Only include roles sharing a detected skill
    recommendations = [
        result
        for result in results
        if result["matched_skills"]
    ][:3]

    print("\nTOP JOB RECOMMENDATIONS")
    print("-----------------------")

    if not recommendations:
        print(
            "No job-role skill overlap detected."
        )
        print(
            "A recommendation cannot be made yet."
        )

    else:
        for index, result in enumerate(
            recommendations, start=1
        ):
            print(
                f"{index}. {result['job_role']}"
            )

            print(
                f"   Similarity: "
                f"{result['similarity']:.4f}"
            )

            print(
                f"   Coverage: "
                f"{result['skill_coverage_percent']:.1f}%"
            )

    print("\nJob matching test completed!")


if __name__ == "__main__":
    main()
