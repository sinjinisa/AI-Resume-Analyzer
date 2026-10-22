
from text_cleaner import clean_resume_text


# Create deliberately messy sample text
sample_text = """
   SKILLS:   Python, C++, C#, .NET,
   Node.js, scikit-learn!!

   PROJECTS:   AI/ML Resume Analyzer.
"""

# Clean the sample text
cleaned_text = clean_resume_text(sample_text)

# Display the results
print("ORIGINAL TEXT:")
print(sample_text)

print("\nCLEANED TEXT:")
print(cleaned_text)

# Test whether important skills are preserved
assert "python" in cleaned_text
assert "c++" in cleaned_text
assert "c#" in cleaned_text
assert ".net" in cleaned_text
assert "node.js" in cleaned_text
assert "scikit-learn" in cleaned_text

print("\nAll text cleaning tests passed!")
