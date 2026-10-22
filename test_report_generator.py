
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from job_matcher import match_resume_to_jobs
from roadmap_generator import generate_roadmap
from report_generator import generate_pdf_report


def main():

    # STEP 1: Create fictional candidate skills
    candidate_skills = [
        "Python",
        "SQL",
        "Machine Learning"
    ]

    # STEP 2: Match candidate to jobs
    results = match_resume_to_jobs(
        candidate_skills
    )

    # STEP 3: Select Data Analyst
    target_role = "Data Analyst"

    selected_job = next(
        job
        for job in results
        if job["job_role"] == target_role
    )

    # STEP 4: Get top three recommendations
    recommendations = [
        job for job in results
        if job["matched_skills"]
    ][:3]

    # STEP 5: Generate learning roadmap
    roadmap = generate_roadmap(
        target_role,
        selected_job["missing_skills"]
    )

    # STEP 6: Generate PDF report
    pdf_bytes = generate_pdf_report(
        target_role,
        candidate_skills,
        selected_job,
        recommendations,
        roadmap
    )

    # STEP 7: Verify PDF file signature
    assert pdf_bytes.startswith(b"%PDF-")

    # STEP 8: Check PDF pages
    reader = PdfReader(BytesIO(pdf_bytes))

    assert len(reader.pages) >= 1

    # STEP 9: Extract generated PDF text
    pdf_text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    # STEP 10: Validate PDF contents
    assert "Data Analyst" in pdf_text
    assert "Python" in pdf_text
    assert "Excel" in pdf_text
    assert "Week 4" in pdf_text

    # STEP 11: Save a sample report
    project_folder = Path(__file__).resolve().parent

    reports_folder = project_folder / "reports"

    reports_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = (
        reports_folder / "sample_analysis.pdf"
    )

    report_path.write_bytes(pdf_bytes)

    # STEP 12: Display results
    print("PDF REPORT GENERATED SUCCESSFULLY!")
    print("PDF report test PASSED!")
    print("Total pages:", len(reader.pages))
    print("PDF size:", len(pdf_bytes), "bytes")
    print("Saved at:", report_path)


if __name__ == "__main__":
    main()
