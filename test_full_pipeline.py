
from pathlib import Path

# Import our three existing modules
from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import extract_skills


def main():

    # STEP 1: Locate the project folder
    project_folder = Path(__file__).resolve().parent

    # STEP 2: Locate the sample resume
    resume_path = (
        project_folder
        / "sample_resumes"
        / "demo_resume_v2.docx"
    )

    # STEP 3: Verify the file exists
    if not resume_path.is_file():
        print("ERROR: Resume file not found!")
        print("Expected location:", resume_path)
        return

    print("Resume found:", resume_path.name)

    # STEP 4: Extract raw resume text
    raw_text = extract_resume_text(resume_path)

    print("\n========== RAW RESUME TEXT ==========")
    print(raw_text)

    # STEP 5: Clean the extracted text
    cleaned_text = clean_resume_text(raw_text)

    print("\n========== CLEANED TEXT ==========")
    print(cleaned_text)

    # STEP 6: Extract technical skills
    detected_skills = extract_skills(cleaned_text)

    print("\n========== DETECTED SKILLS ==========")

    if detected_skills:
        for skill in detected_skills:
            print("-", skill)
    else:
        print("No matching skills found.")

    # STEP 7: Count detected skills
    print("\nTotal skills detected:", len(detected_skills))

    # STEP 8: Confirm successful execution
    print("\nFull NLP pipeline executed successfully!")


if __name__ == "__main__":
    main()
