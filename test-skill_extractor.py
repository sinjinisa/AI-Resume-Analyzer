
from text_cleaner import clean_resume_text
from skill_extractor import extract_skills


# A fictional resume
resume_text = """
I know Python, SQL, Machine Learning,
Pandas, Docker, JavaScript, C++ and React.
"""

# Clean the resume
cleaned_text = clean_resume_text(resume_text)

# Extract technical skills
skills = extract_skills(cleaned_text)

print("CLEANED RESUME:")
print(cleaned_text)

print("\nDETECTED SKILLS:")

for skill in skills:
    print("-", skill)

print("\nTotal skills detected:", len(skills))


# Verify that expected skills were found
expected_skills = {
    "Python",
    "SQL",
    "Machine Learning",
    "Pandas",
    "Docker",
    "JavaScript",
    "C++",
    "React"
}

assert expected_skills.issubset(set(skills))

# JavaScript must not be confused with Java
assert "Java" not in skills

print("\nSkill extraction test PASSED!")
