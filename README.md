# AI Resume Analyzer & Job Recommendation System

**Python | NLP | Machine Learning | Streamlit**

## Project Overview

The AI Resume Analyzer and Job Recommendation System is an educational, Python-based application that analyzes technical skills mentioned in PDF and DOCX resumes.

It compares detected skills with predefined job requirements using TF-IDF and cosine similarity, recommends relevant job roles, identifies skill gaps, and generates personalized four-week learning roadmaps.

## Key Features

- PDF and DOCX resume parsing
- Text cleaning and preprocessing
- Dictionary-based technical skill extraction
- TF-IDF and cosine similarity job matching
- Top-three job recommendations
- Matched and missing skill analysis
- Four-week learning roadmaps
- Interactive Streamlit dashboard
- Downloadable PDF and TXT reports
- File-upload validation
- Automated software tests
- Evaluation and responsible-AI documentation

## Technologies Used

**Programming:** Python

**Libraries:** pypdf, python-docx, pandas, scikit-learn, ReportLab, pytest

**Web Framework:** Streamlit

**Techniques:** Regular expressions, TF-IDF, cosine similarity, rule-based skill extraction

## Supported Job Roles

1. Data Analyst
2. Machine Learning Engineer
3. AI Engineer
4. NLP Engineer
5. Computer Vision Engineer

## System Architecture

Resume Upload → Document Validation → Text Extraction → Text Cleaning → Skill Extraction → Job Matching → Skill-Gap Analysis → Learning Roadmap → Streamlit Dashboard → PDF/TXT Report

## Getting Started

Requirements: Python and pip.

Install dependencies from the project directory:

`python -m pip install -r requirements.txt`

Start the application:

`python -m streamlit run app.py`

Open the local URL displayed in the terminal.

Upload a PDF or DOCX resume and select a target job role.

## Testing

Run the automated test suite:

`python -m pytest tests/ -v`

The project passed 25 automated tests covering core functionality, upload validation, and selected consistency and transparency checks.

## Skill Extraction Evaluation

The skill extractor was evaluated using 16 manually labeled fictional resume excerpts and a dictionary containing 38 technical skills.

| Metric | Measured Result |
|---|---:|
| Micro Precision | 74.19% |
| Micro Recall | 100.00% |
| Micro F1-score | 85.19% |
| Exact-Match Accuracy | 56.25% |

These measurements describe performance on a small synthetic evaluation dataset and should not be interpreted as real-world accuracy estimates.

## Known Limitations

The extractor uses rule-based keyword and alias matching. It may incorrectly detect skills in statements expressing negation or learning intentions.

Job matching is restricted to five predefined roles.

Cosine similarity is not a hiring probability, and the application does not independently verify professional competence.

## Responsible AI

This application is intended for educational career exploration, not automated hiring, rejection or employment eligibility decisions.

Its upload validator provides preliminary file-format and resource-limit checks, not comprehensive malware protection.

Refer to `docs/EVALUATION_REPORT.md` and `docs/RESPONSIBLE_AI.md` for further evaluation results and limitations.

## Future Improvements

- Context-aware and negation-aware skill extraction
- More job roles and larger datasets
- Independently labeled evaluation data
- Improved recommendation evaluation
- User confirmation of detected skills
- Additional security and fairness testing

## Project Status

Core application developed, locally tested, and prepared for cloud deployment.
