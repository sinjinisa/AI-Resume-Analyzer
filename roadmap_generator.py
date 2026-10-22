
# LESSON 7: LEARNING ROADMAP GENERATOR


# STEP 1: Define learning activities for skills

LEARNING_TASKS = {

    "python": (
        "Practice functions, data structures, "
        "file handling, and small Python programs."
    ),

    "sql": (
        "Learn SELECT, WHERE, JOIN, GROUP BY, "
        "and database queries."
    ),

    "excel": (
        "Learn formulas, data cleaning, "
        "pivot tables, and charts."
    ),

    "pandas": (
        "Learn DataFrames, filtering, grouping, "
        "and handling missing values."
    ),

    "power bi": (
        "Learn data import, visualization, "
        "and interactive dashboards."
    ),

    "machine learning": (
        "Study supervised learning, model training, "
        "evaluation, and overfitting."
    ),

    "scikit-learn": (
        "Practice train-test splitting, preprocessing, "
        "model fitting, and evaluation."
    ),

    "fastapi": (
        "Build REST API endpoints using Python "
        "and FastAPI."
    ),

    "docker": (
        "Learn containers, Dockerfiles, "
        "image building, and application packaging."
    ),

    "deep learning": (
        "Study neural networks, backpropagation, "
        "and basic model training."
    ),

    "llm": (
        "Learn language model concepts, prompting, "
        "and structured outputs."
    ),

    "rag": (
        "Learn embeddings, retrieval, "
        "vector search, and grounded responses."
    ),

    "apis": (
        "Learn HTTP methods, JSON, REST APIs, "
        "and API testing."
    ),

    "nlp": (
        "Learn tokenization, text representation, "
        "classification, and NLP evaluation."
    ),

    "transformers": (
        "Study attention, transformer architecture, "
        "and pretrained language models."
    ),

    "hugging face": (
        "Practice loading pretrained models "
        "and using inference pipelines."
    ),

    "opencv": (
        "Learn image loading, resizing, "
        "color conversion, and image processing."
    ),

    "cnn": (
        "Study convolutional neural networks "
        "and basic image classification."
    ),

    "yolo": (
        "Learn object detection concepts "
        "and experiment with YOLO models."
    )
}


# STEP 2: Define a mini-project for each job role

ROLE_PROJECTS = {

    "Data Analyst": (
        "Analyze a dataset using Python or SQL "
        "and present the results in a dashboard."
    ),

    "Machine Learning Engineer": (
        "Train a machine learning model, "
        "create a prediction API, "
        "and package the application."
    ),

    "AI Engineer": (
        "Build a small AI question-answering "
        "application using retrieval."
    ),

    "NLP Engineer": (
        "Create a text classification project "
        "and evaluate its predictions."
    ),

    "Computer Vision Engineer": (
        "Create a basic computer vision "
        "application using image processing."
    )
}


# STEP 3: Create the roadmap function

def generate_roadmap(job_role, missing_skills):

    # Validate inputs
    if not isinstance(job_role, str):
        raise TypeError("Job role must be a string.")

    if not isinstance(missing_skills, list):
        raise TypeError("Missing skills must be a list.")

    # Remove duplicates while preserving order
    unique_skills = []
    seen = set()

    for skill in missing_skills:

        if not isinstance(skill, str):
            raise TypeError("Each skill must be a string.")

        skill = skill.strip()
        normalized = skill.casefold()

        if skill and normalized not in seen:
            unique_skills.append(skill)
            seen.add(normalized)

    # No detected skill gaps
    if not unique_skills:
        return []

    roadmap = []

    # Distribute missing skills across three weeks
    weekly_skills = [[], [], []]

    for index, skill in enumerate(unique_skills):
        weekly_skills[index % 3].append(skill)

    # STEP 4: Generate the first three weeks
    for week_number in range(1, 4):

        skills_for_week = weekly_skills[week_number - 1]

        activities = []

        if skills_for_week:

            for skill in skills_for_week:

                task = LEARNING_TASKS.get(
                    skill.casefold(),
                    f"Study {skill} fundamentals "
                    "and complete a practical exercise."
                )

                activities.append(
                    f"{skill}: {task}"
                )

            focus = ", ".join(skills_for_week)

        else:

            focus = "Practice and reinforcement"

            activities.append(
                "Review previously studied skills "
                "and complete hands-on exercises."
            )

        roadmap.append({
            "week": week_number,
            "focus": focus,
            "activities": activities
        })

    # STEP 5: Generate the fourth week
    project = ROLE_PROJECTS.get(
        job_role,
        f"Build a small project related to {job_role}."
    )

    roadmap.append({
        "week": 4,
        "focus": "Mini Project and Portfolio",
        "activities": [
            project,
            "Test and document the project.",
            "Update your resume only with skills "
            "you can genuinely demonstrate."
        ]
    })

    return roadmap
