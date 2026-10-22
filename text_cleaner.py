
import re


def clean_resume_text(text):

    # Check whether the input is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    # Step 1: Convert text to lowercase
    text = text.lower()

    # Step 2: Standardize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Step 3: Remove common bullet characters
    text = re.sub(r"[•●▪]", " ", text)

    # Step 4: Remove unwanted special characters
    # Preserve +, #, . and - for technical skills
    text = re.sub(r"[^\w\s+#.\-]", " ", text)

    # Step 5: Replace repeated spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Step 6: Remove spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    # Step 7: Remove repeated blank lines
    text = re.sub(r"\n{2,}", "\n", text)

    # Step 8: Remove spaces at the beginning and end
    text = text.strip()

    return text
