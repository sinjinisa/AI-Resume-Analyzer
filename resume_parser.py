
from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_resume_text(file_path):
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError("Resume file not found.")

    extension = path.suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(str(path))

        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)

    elif extension == ".docx":
        document = Document(str(path))

        text_parts = []

        for paragraph in document.paragraphs:
            text_parts.append(paragraph.text)

    else:
        raise ValueError("Only PDF and DOCX files are supported.")

    return "\n".join(text_parts).strip()
