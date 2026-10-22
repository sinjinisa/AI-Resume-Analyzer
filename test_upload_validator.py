
from io import BytesIO
from zipfile import ZipFile

import pytest

from docx import Document
from reportlab.pdfgen import canvas

from upload_validator import (
    MAX_UPLOAD_BYTES,
    ResumeValidationError,
    validate_resume_upload
)


# ==========================================
# HELPER FUNCTION 1: CREATE SAMPLE PDF
# ==========================================

def create_sample_pdf():

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.drawString(
        72,
        720,
        "Fictional Resume: Python and SQL"
    )

    pdf.save()

    return buffer.getvalue()


# ==========================================
# HELPER FUNCTION 2: CREATE SAMPLE DOCX
# ==========================================

def create_sample_docx():

    buffer = BytesIO()

    document = Document()

    document.add_paragraph(
        "Fictional Resume: Python and SQL"
    )

    document.save(buffer)

    return buffer.getvalue()


# ==========================================
# TEST 1: VALID PDF
# ==========================================

def test_valid_pdf():

    pdf_bytes = create_sample_pdf()

    result = validate_resume_upload(
        "sample.pdf",
        pdf_bytes
    )

    assert result == ".pdf"


# ==========================================
# TEST 2: VALID DOCX
# ==========================================

def test_valid_docx():

    docx_bytes = create_sample_docx()

    result = validate_resume_upload(
        "sample.docx",
        docx_bytes
    )

    assert result == ".docx"


# ==========================================
# TEST 3: REJECT UNSUPPORTED FILE TYPE
# ==========================================

def test_reject_txt():

    with pytest.raises(
        ResumeValidationError,
        match="Only PDF and DOCX"
    ):

        validate_resume_upload(
            "resume.txt",
            b"Python and SQL"
        )


# ==========================================
# TEST 4: REJECT EMPTY FILE
# ==========================================

def test_reject_empty_file():

    with pytest.raises(
        ResumeValidationError,
        match="empty"
    ):

        validate_resume_upload(
            "empty.pdf",
            b""
        )


# ==========================================
# TEST 5: REJECT OVERSIZED FILE
# ==========================================

def test_reject_oversized_file():

    large_data = b"A" * (MAX_UPLOAD_BYTES + 1)

    with pytest.raises(
        ResumeValidationError,
        match="5 MB"
    ):

        validate_resume_upload(
            "large.pdf",
            large_data
        )


# ==========================================
# TEST 6: REJECT FAKE PDF
# ==========================================

def test_reject_fake_pdf():

    fake_data = b"This is not a PDF file."

    with pytest.raises(
        ResumeValidationError
    ):

        validate_resume_upload(
            "fake.pdf",
            fake_data
        )


# ==========================================
# TEST 7: REJECT CORRUPTED PDF
# ==========================================

def test_reject_damaged_pdf():

    damaged_data = b"%PDF-invalid-document"

    with pytest.raises(
        ResumeValidationError
    ):

        validate_resume_upload(
            "damaged.pdf",
            damaged_data
        )


# ==========================================
# TEST 8: REJECT INVALID DOCX
# ==========================================

def test_reject_fake_docx():

    buffer = BytesIO()

    # Create a ZIP file that is not a DOCX
    with ZipFile(buffer, "w") as archive:

        archive.writestr(
            "ordinary_file.txt",
            "Not a Microsoft Word document."
        )

    fake_docx = buffer.getvalue()

    with pytest.raises(
        ResumeValidationError,
        match="structure"
    ):

        validate_resume_upload(
            "fake.docx",
            fake_docx
        )


# ==========================================
# TEST 9: REJECT DOUBLE EXTENSION
# ==========================================

def test_reject_double_extension():

    pdf_bytes = create_sample_pdf()

    with pytest.raises(
        ResumeValidationError,
        match="Only PDF and DOCX"
    ):

        validate_resume_upload(
            "resume.pdf.exe",
            pdf_bytes
        )

