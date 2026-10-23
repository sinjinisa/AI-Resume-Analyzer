
from upload_validator import (
    validate_resume_upload,
    ResumeValidationError
)

import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from resume_parser import extract_resume_text
from text_cleaner import clean_resume_text
from skill_extractor import extract_skills
from job_matcher import load_job_roles, match_resume_to_jobs
from roadmap_generator import generate_roadmap
from report_generator import generate_pdf_report

# ==========================================
# STEP 1: CONFIGURE THE DASHBOARD
# ==========================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Temporary Streamlit deployment diagnostics
from pathlib import Path

DEBUG_ROOT = Path(__file__).resolve().parent
DEBUG_DATA = DEBUG_ROOT / "data"
DEBUG_JOBS = DEBUG_DATA / "job_roles.csv"

st.subheader("Cloud Deployment Diagnostics")

st.write("Application directory:", str(DEBUG_ROOT))

st.write(
    "Files and folders at application root:",
    sorted(item.name for item in DEBUG_ROOT.iterdir())
)

st.write(
    "Locations of job_roles.csv:",
    sorted(
        str(item.relative_to(DEBUG_ROOT))
        for item in DEBUG_ROOT.rglob("job_roles.csv")
        if item.is_file()
    )
)

st.write("Data folder exists:", DEBUG_DATA.is_dir())

st.write("job_roles.csv exists:", DEBUG_JOBS.is_file())

if DEBUG_DATA.is_dir():
    st.write(
        "Files found inside data:",
        sorted(file.name for file in DEBUG_DATA.iterdir())
    )
else:
    st.error("The cloud server cannot find the data folder.")


# ==========================================
# PROFESSIONAL DASHBOARD HEADER
# ==========================================

st.title("📄 AI Resume Analyzer")

st.subheader("Job Recommendation & Skill-Gap Analysis")

st.write(
    "Analyze your resume, discover relevant technical "
    "job roles, identify missing skills, and generate "
    "a personalized learning roadmap."
)

st.caption(
    "Powered by Python, NLP, TF-IDF and cosine similarity."
)

st.divider()


st.write(
    "Upload your resume to explore suitable job roles, "
    "identify technical skill gaps, and generate a "
    "personalized learning roadmap."
)

st.caption(
    "Results are educational estimates, not hiring decisions."
)


# ==========================================
# STEP 2: LOAD JOB ROLES
# ==========================================

try:
    jobs = load_job_roles()

except Exception as error:
    st.error(f"Could not load job roles: {error}")
    st.stop()

role_names = [
    job["job_role"]
    for job in jobs
]


# ==========================================
# STEP 3: CREATE SIDEBAR
# ==========================================

st.sidebar.header("Analysis Settings")

target_role = st.sidebar.selectbox(
    "Select Your Target Job Role",
    role_names
)

st.sidebar.info(
    "Choose a role to view its required skills, "
    "match score, and learning roadmap."
)



# ==========================================
# STEP 4: SECURE RESUME UPLOAD
# ==========================================

st.subheader("1. Upload Your Resume")

st.write(
    "Upload a PDF or DOCX resume for analysis."
)

st.caption(
    "Supported formats: PDF and DOCX. "
    "Maximum file size: 5 MB."
)

uploaded_file = st.file_uploader(
    label="Choose a PDF or DOCX resume",
    type=["pdf", "docx"],
    max_upload_size=5,
    help="Upload one PDF or DOCX file, up to 5 MB."
)

# Stop until a resume is uploaded
if uploaded_file is None:

    st.info(
        "Please upload a resume to begin the analysis."
    )

    st.stop()


# ==========================================
# STEP 5: SECURITY VALIDATION
# ==========================================

# Read uploaded document as bytes
file_bytes = uploaded_file.getvalue()

try:

    # Validate file extension, size, format,
    # document structure and resource limits.
    extension = validate_resume_upload(
        uploaded_file.name,
        file_bytes
    )

except ResumeValidationError as error:

    st.error(
        f"Resume validation failed: {error}"
    )

    st.stop()

# Display success only after validation
st.success(
    "Resume validated and uploaded successfully!"
)

st.caption(
    f"Validated document format: "
    f"{extension.upper()}"
)

# ==========================================
# STEP 6: PROCESS THE RESUME
# ==========================================

try:

    # Create a temporary folder for parsing
    with tempfile.TemporaryDirectory() as temp_folder:

        temp_path = (
            Path(temp_folder) / f"resume{extension}"
        )

        temp_path.write_bytes(file_bytes)

        # Extract resume text
        raw_text = extract_resume_text(temp_path)

    # The temporary folder is deleted here

    if not raw_text.strip():
        st.warning(
            "No readable text was found. "
            "Scanned PDFs may require OCR."
        )
        st.stop()

    # Clean text
    cleaned_text = clean_resume_text(raw_text)

    # Extract skills
    detected_skills = extract_skills(cleaned_text)

    # Match candidate against jobs
    results = match_resume_to_jobs(detected_skills)

except Exception as error:
    st.error(
        f"Resume analysis failed: "
        f"{type(error).__name__}: {error}"
    )
    st.stop()


# ==========================================
# STEP 7: DISPLAY DETECTED SKILLS
# ==========================================

st.subheader("2. Detected Technical Skills")

if detected_skills:

    st.write(", ".join(detected_skills))

    st.metric(
        "Total Skills Detected",
        len(detected_skills)
    )

else:
    st.warning(
        "No known technical skills were detected."
    )


# ==========================================
# STEP 8: GET THE SELECTED JOB RESULT
# ==========================================

selected_job = next(
    (
        job for job in results
        if job["job_role"] == target_role
    ),
    None
)

if selected_job is None:
    st.error("Selected job role was not found.")
    st.stop()



# ==========================================
# STEP 9: PROFESSIONAL JOB MATCHING METRICS
# ==========================================

st.subheader("3. Target Job Analysis")

st.write("**Selected job role:**", target_role)

# Create two metric cards
col1, col2 = st.columns(2)

with col1:

    st.metric(
        label="TF-IDF Cosine Similarity",
        value=f"{selected_job['similarity']:.4f}",
        border=True
    )

with col2:

    st.metric(
        label="Required-Skill Coverage",
        value=(
            f"{selected_job['skill_coverage_percent']:.1f}%"
        ),
        border=True
    )

# Show required-skill coverage visually
st.progress(
    selected_job["skill_coverage_percent"] / 100
)

st.caption(
    "The progress bar represents detected required "
    "skills, not a probability of being hired."
)

# Explain the scores
with st.expander("How are these scores calculated?"):

    st.markdown("""
    **TF-IDF Cosine Similarity**

    Measures the similarity between the candidate's
    detected skills and the job's required skills
    using weighted numerical vectors.

    **Required-Skill Coverage**

    Measures the percentage of listed required
    skills detected in the resume.

    **Important limitations**

    - Similarity is not a hiring probability.
    - Missing keywords do not necessarily mean
      missing ability.
    - Results depend on the job-role dataset.
    - The system is intended for educational guidance.
    """)



# ==========================================
# STEP 10: MATCHED AND MISSING SKILLS
# ==========================================

st.subheader("Skill-Gap Analysis")

with st.container(border=True):

    left_column, right_column = st.columns(2)

    with left_column:

        st.markdown("### ✅ Matched Skills")

        if selected_job["matched_skills"]:

            for skill in selected_job["matched_skills"]:
                st.write(f"✓ {skill}")

        else:
            st.info("No matching required skills detected.")

    with right_column:

        st.markdown("### Skills to Develop")

        if selected_job["missing_skills"]:

            for skill in selected_job["missing_skills"]:
                st.write(f"• {skill}")

        else:
            st.success(
                "All listed required skills were detected."
            )

st.caption(
    "A skill not detected in a resume may still be "
    "possessed by the candidate."
)



# ==========================================
# STEP 11: PROFESSIONAL JOB COMPARISON CHART
# ==========================================

st.subheader("4. Job Role Comparison")

# Create comparison dataset
comparison_data = pd.DataFrame([
    {
        "Job Role": result["job_role"],
        "Cosine Similarity": result["similarity"],
        "Skill Coverage (%)": result[
            "skill_coverage_percent"
        ]
    }
    for result in results
])

st.write(
    "Compare the TF-IDF cosine similarities "
    "for all five job roles."
)

# Horizontal bar chart
st.bar_chart(
    comparison_data,
    x="Job Role",
    y="Cosine Similarity",
    horizontal=True,
    sort=False,
    height=320
)

# Display detailed comparison table
with st.expander(
    "View Detailed Job Comparison",
    expanded=True
):

    st.dataframe(
        comparison_data,
        hide_index=True,
        width="stretch"
    )



# ==========================================
# STEP 12: PROFESSIONAL JOB RECOMMENDATIONS
# ==========================================

st.subheader("5. Top Job Recommendations")

recommendations = [
    result
    for result in results
    if result["matched_skills"]
][:3]

if recommendations:

    for index, job in enumerate(
        recommendations,
        start=1
    ):

        with st.container(border=True):

            st.markdown(
                f"### {index}. {job['job_role']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Cosine Similarity",
                    f"{job['similarity']:.4f}"
                )

            with col2:
                st.metric(
                    "Skill Coverage",
                    f"{job['skill_coverage_percent']:.1f}%"
                )

            st.write(
                "**Matched required skills:**",
                ", ".join(job["matched_skills"])
            )

else:

    st.info(
        "No job-role skill overlap was detected. "
        "A recommendation cannot be made yet."
    )

st.caption(
    "Recommendations are ranked among the five "
    "sample roles in our dataset and should "
    "be reviewed alongside actual job descriptions."
)



# ==========================================
# STEP 13: PROFESSIONAL LEARNING ROADMAP
# ==========================================

st.subheader("6. Personalized Learning Roadmap")

st.caption(
    "A four-week introductory learning plan "
    "based on the selected job role."
)

roadmap = generate_roadmap(
    target_role,
    selected_job["missing_skills"]
)

if roadmap:

    for week in roadmap:

        with st.expander(
            f"Week {week['week']}: {week['focus']}",
            expanded=(week["week"] == 1)
        ):

            for activity in week["activities"]:
                st.write(f"• {activity}")

else:

    st.success(
        "All listed required skills were detected. "
        "Consider completing a portfolio project "
        "to demonstrate your knowledge."
    )

# ==========================================
# STEP 14: CREATE A DOWNLOADABLE TEXT REPORT
# ==========================================

report_lines = [
    "AI RESUME ANALYZER REPORT",
    "=========================",
    "",
    f"Target Role: {target_role}",
    f"Detected Skills: {', '.join(detected_skills)}",
    "",
    f"Cosine Similarity: "
    f"{selected_job['similarity']:.4f}",
    f"Skill Coverage: "
    f"{selected_job['skill_coverage_percent']:.1f}%",
    "",
    "MATCHED SKILLS:",
    ", ".join(selected_job["matched_skills"]),
    "",
    "MISSING SKILLS:",
    ", ".join(selected_job["missing_skills"]),
    "",
    "TOP JOB RECOMMENDATIONS:"
]

for index, job in enumerate(recommendations, start=1):

    report_lines.append(
        f"{index}. {job['job_role']} "
        f"(similarity: {job['similarity']:.4f})"
    )

report_lines.append("")
report_lines.append("LEARNING ROADMAP:")

for week in roadmap:

    report_lines.append(
        f"Week {week['week']}: {week['focus']}"
    )

    for activity in week["activities"]:
        report_lines.append(f"- {activity}")

report_lines.append("")
report_lines.append(
    "Educational guidance only; "
    "not a hiring or eligibility decision."
)

report_text = "\n".join(report_lines)

# ==========================================
# LESSON 9: PDF AND TXT REPORT DOWNLOADS
# ==========================================

st.subheader("7. Download Your Analysis")

st.write(
    "Download your personalized resume analysis "
    "in TXT or PDF format."
)

# STEP 1: Create two columns
col_txt, col_pdf = st.columns(2)


# STEP 2: Add TXT download button
with col_txt:

    st.download_button(
        label="Download TXT Report",
        data=report_text,
        file_name="resume_analysis.txt",
        mime="text/plain"
    )


# STEP 3: Generate the PDF report
try:

    pdf_bytes = generate_pdf_report(
        target_role,
        detected_skills,
        selected_job,
        recommendations,
        roadmap
    )

except Exception as error:

    st.error(
        f"PDF generation failed: {error}"
    )

else:

    # STEP 4: Add PDF download button
    with col_pdf:

        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name="resume_analysis.pdf",
            mime="application/pdf"
        )


# STEP 5: Add a report preview
with st.expander("Preview Analysis Report"):

    st.code(
        report_text,
        language="text"
    )



# ==========================================
# STEP 15: FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Resume Analyzer and Job Recommendation System "
    "| Educational Major Project")
