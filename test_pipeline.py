
from pathlib import Path

from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text


def main():
    # STEP 1: Find the project folder
    project_folder = Path(__file__).resolve().parent

    # STEP 2: Specify the resume file
    resume_path = (
        project_folder
        / "sample_resumes"
        / "demo_resume_v2.docx"
    )

    # STEP 3: Check whether the resume exists
    print("Looking for resume at:", resume_path)
    print("File exists:", resume_path.is_file())

    if not resume_path.is_file():
        print("ERROR: Resume file not found!")
        return

    # STEP 4: Extract raw text from the resume
    try:
        raw_text = extract_resume_text(resume_path)
    except Exception as error:
        print("ERROR while extracting resume:", error)
        return

    # STEP 5: Check whether text was extracted
    if not raw_text.strip():
        print("ERROR: No readable text was extracted.")
        return

    # STEP 6: Clean the extracted text
    cleaned_text = clean_resume_text(raw_text)

    # STEP 7: Display the original text
    print("\n========== RAW RESUME TEXT ==========")
    print(raw_text)

    # STEP 8: Display the cleaned text
    print("\n========== CLEANED RESUME TEXT ==========")
    print(cleaned_text)

    # STEP 9: Confirm successful execution
    print("\nPipeline executed successfully!")


if __name__ == "__main__":
    main()


