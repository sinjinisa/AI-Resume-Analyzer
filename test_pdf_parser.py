
from pathlib import Path
from resume_parser import extract_resume_text

# Step 1: Specify the PDF file location
pdf_path = Path("sample_resumes/demo_resume.pdf")

# Step 2: Extract the text using our parser
extracted_text = extract_resume_text(pdf_path)

# Step 3: Display the extracted text
print("EXTRACTED PDF RESUME TEXT:")
print(extracted_text)

# Step 4: Check whether important text was found
if "Python" in extracted_text:
    print("\nPDF extraction test PASSED!")
else:
    print("\nPDF extraction needs further checking.")
