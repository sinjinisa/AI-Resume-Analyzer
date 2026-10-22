
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, BadZipFile, is_zipfile

from pypdf import PdfReader


# ==========================================
# SECURITY CONFIGURATION
# ==========================================

MAX_UPLOAD_BYTES = 5 * 1024 * 1024

MAX_PDF_PAGES = 30

MAX_DOCX_ENTRIES = 300

MAX_DOCX_UNCOMPRESSED_BYTES = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


# ==========================================
# CUSTOM VALIDATION EXCEPTION
# ==========================================

class ResumeValidationError(ValueError):
    """Raised when an uploaded resume is invalid."""
    pass


# ==========================================
# FUNCTION 1: VALIDATE PDF
# ==========================================

def validate_pdf(file_bytes):
    """
    Validate PDF signature, readability,
    encryption status and page count.
    """

    # Check PDF signature
    if not file_bytes.startswith(b"%PDF-"):
        raise ResumeValidationError(
            "The uploaded file is not a valid PDF."
        )

    try:
        # Read PDF from memory
        reader = PdfReader(
            BytesIO(file_bytes),
            strict=False
        )

        # Reject encrypted PDFs
        if reader.is_encrypted:
            raise ResumeValidationError(
                "Password-protected PDFs are not supported."
            )

        # Count PDF pages
        page_count = len(reader.pages)

        # Reject empty PDFs
        if page_count == 0:
            raise ResumeValidationError(
                "The PDF does not contain any pages."
            )

        # Reject excessively long PDFs
        if page_count > MAX_PDF_PAGES:
            raise ResumeValidationError(
                f"PDF cannot exceed {MAX_PDF_PAGES} pages."
            )

    except ResumeValidationError:
        raise

    except Exception as error:
        raise ResumeValidationError(
            "PDF is corrupted or cannot be read."
        ) from error

    return True


# ==========================================
# FUNCTION 2: VALIDATE DOCX
# ==========================================

def validate_docx(file_bytes):
    """
    Validate basic DOCX archive structure,
    encryption flags and resource limits.
    """

    # DOCX files use a ZIP-based format
    if not is_zipfile(BytesIO(file_bytes)):
        raise ResumeValidationError(
            "The uploaded file is not a valid DOCX archive."
        )

    try:
        with ZipFile(BytesIO(file_bytes)) as archive:

            members = archive.infolist()

            # Limit the number of archive entries
            if len(members) > MAX_DOCX_ENTRIES:
                raise ResumeValidationError(
                    "DOCX contains too many internal files."
                )

            # Get internal filenames
            filenames = {
                member.filename.lower()
                for member in members
            }

            # Required components of a DOCX
            required_files = {
                "[content_types].xml",
                "word/document.xml"
            }

            if not required_files.issubset(filenames):
                raise ResumeValidationError(
                    "DOCX structure is invalid."
                )

            # Check total declared uncompressed size
            total_size = sum(
                member.file_size
                for member in members
            )

            if total_size > MAX_DOCX_UNCOMPRESSED_BYTES:
                raise ResumeValidationError(
                    "DOCX uncompressed content is too large."
                )

            # Check internal files
            for member in members:

                # Reject encrypted ZIP entries
                if member.flag_bits & 1:
                    raise ResumeValidationError(
                        "Encrypted DOCX entries are not supported."
                    )

                # Reject embedded VBA macro project files
                if member.filename.lower().endswith(
                    "/vbaproject.bin"
                ):
                    raise ResumeValidationError(
                        "Macro-containing files are not supported."
                    )

    except ResumeValidationError:
        raise

    except (BadZipFile, OSError, ValueError) as error:
        raise ResumeValidationError(
            "DOCX archive is corrupted or unreadable."
        ) from error

    return True


# ==========================================
# FUNCTION 3: MAIN VALIDATOR
# ==========================================

def validate_resume_upload(filename, file_bytes):
    """
    Validate an uploaded resume.

    Parameters:
        filename: Name of uploaded file.
        file_bytes: Complete binary file contents.

    Returns:
        File extension, either '.pdf' or '.docx'.

    Raises:
        ResumeValidationError for invalid uploads.
    """

    # STEP 1: Validate filename
    if not isinstance(filename, str) or not filename:
        raise ResumeValidationError(
            "A valid filename is required."
        )

    # STEP 2: Extract extension
    extension = Path(filename).suffix.lower()

    # STEP 3: Check allowed extension
    if extension not in ALLOWED_EXTENSIONS:
        raise ResumeValidationError(
            "Only PDF and DOCX files are allowed."
        )

    # STEP 4: Check binary content type
    if not isinstance(file_bytes, bytes):
        raise ResumeValidationError(
            "Uploaded content must be bytes."
        )

    # STEP 5: Reject empty files
    if len(file_bytes) == 0:
        raise ResumeValidationError(
            "The uploaded file is empty."
        )

    # STEP 6: Check file-size limit
    if len(file_bytes) > MAX_UPLOAD_BYTES:
        raise ResumeValidationError(
            "File size cannot exceed 5 MB."
        )

    # STEP 7: Validate PDF
    if extension == ".pdf":
        validate_pdf(file_bytes)

    # STEP 8: Validate DOCX
    elif extension == ".docx":
        validate_docx(file_bytes)

    # STEP 9: Return validated file type
    return extension

