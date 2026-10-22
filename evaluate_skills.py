
import csv
from pathlib import Path

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    multilabel_confusion_matrix
)

from text_cleaner import clean_resume_text
from skill_extractor import extract_skills


# ==========================================
# STEP 1: DEFINE PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

SKILL_FILE = BASE_DIR / "data" / "skill_dictionary.csv"

EVALUATION_FILE = (
    BASE_DIR / "data" / "skill_evaluation.csv"
)

REPORTS_DIR = BASE_DIR / "reports"


# ==========================================
# STEP 2: LOAD THE SKILL DICTIONARY
# ==========================================

def load_skill_names():

    with open(
        SKILL_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames or (
            "skill" not in reader.fieldnames
        ):
            raise ValueError(
                "Skill dictionary must contain "
                "a 'skill' column."
            )

        skills = {
            row["skill"].strip()
            for row in reader
            if row.get("skill")
        }

    if not skills:
        raise ValueError("Skill dictionary is empty.")

    return sorted(skills)


# ==========================================
# STEP 3: LOAD LABELED EVALUATION DATA
# ==========================================

def load_evaluation_data():

    records = []

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        required_columns = {
            "id",
            "text",
            "expected_skills"
        }

        if not reader.fieldnames or not (
            required_columns.issubset(
                set(reader.fieldnames)
            )
        ):
            raise ValueError(
                "Evaluation CSV must contain "
                "id,text,expected_skills"
            )

        for row in reader:

            text = (row.get("text") or "").strip()

            if not text:
                continue

            expected_text = (
                row.get("expected_skills") or ""
            )

            expected = {
                skill.strip()
                for skill in expected_text.split("|")
                if skill.strip()
            }

            records.append({
                "id": (row.get("id") or "").strip(),
                "text": text,
                "expected": expected
            })

    if not records:
        raise ValueError(
            "No evaluation records were found."
        )

    return records


# ==========================================
# STEP 4: RUN SKILL EXTRACTION
# ==========================================

def evaluate():

    all_skills = load_skill_names()

    known_skills = set(all_skills)

    records = load_evaluation_data()

    print("Evaluation samples:", len(records))
    print("Dictionary skills:", len(all_skills))

    y_true = []
    y_pred = []

    detailed_results = []

    for record in records:

        # Read manually labeled skills
        expected = record["expected"]

        # Clean fictional resume text
        cleaned = clean_resume_text(
            record["text"]
        )

        # Extract predicted skills
        predicted = set(
            extract_skills(cleaned)
        )

        # Check dataset label validity
        unknown_expected = (
            expected - known_skills
        )

        if unknown_expected:
            raise ValueError(
                f"Unknown ground-truth skills "
                f"in {record['id']}: "
                f"{sorted(unknown_expected)}"
            )

        unknown_predicted = (
            predicted - known_skills
        )

        if unknown_predicted:
            raise ValueError(
                f"Extractor returned unknown skills: "
                f"{sorted(unknown_predicted)}"
            )

        # Compare expected vs predicted
        correct = expected & predicted

        false_positives = predicted - expected

        false_negatives = expected - predicted

        # Convert skill sets to binary vectors
        true_vector = [
            int(skill in expected)
            for skill in all_skills
        ]

        pred_vector = [
            int(skill in predicted)
            for skill in all_skills
        ]

        y_true.append(true_vector)
        y_pred.append(pred_vector)

        # Store results for inspection
        detailed_results.append({
            "ID": record["id"],
            "Text": record["text"],
            "Expected Skills": "|".join(
                sorted(expected)
            ),
            "Predicted Skills": "|".join(
                sorted(predicted)
            ),
            "True Positives": len(correct),
            "False Positives": len(false_positives),
            "False Negatives": len(false_negatives),
            "Extra Skills": "|".join(
                sorted(false_positives)
            ),
            "Missed Skills": "|".join(
                sorted(false_negatives)
            ),
            "Exact Match": expected == predicted
        })

    # ======================================
    # STEP 5: CALCULATE EVALUATION METRICS
    # ======================================

    precision = precision_score(
        y_true,
        y_pred,
        average="micro",
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        average="micro",
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        average="micro",
        zero_division=0
    )

    exact_match = accuracy_score(
        y_true,
        y_pred
    )

    # ======================================
    # STEP 6: COUNT TP, FP, FN, TN
    # ======================================

    tp = 0
    fp = 0
    fn = 0
    tn = 0

    for actual_row, predicted_row in zip(
        y_true,
        y_pred
    ):

        for actual, predicted in zip(
            actual_row,
            predicted_row
        ):

            if actual == 1 and predicted == 1:
                tp += 1

            elif actual == 0 and predicted == 1:
                fp += 1

            elif actual == 1 and predicted == 0:
                fn += 1

            else:
                tn += 1

    # ======================================
    # STEP 7: DISPLAY OVERALL RESULTS
    # ======================================

    print("\n========== EVALUATION RESULTS ==========")

    print(f"True Positives:  {tp}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"True Negatives:  {tn}")

    print(f"\nMicro Precision: {precision:.4f}")
    print(f"Micro Recall:    {recall:.4f}")
    print(f"Micro F1-score:  {f1:.4f}")

    print(
        f"Exact-Match Accuracy: "
        f"{exact_match:.4f}"
    )

    # ======================================
    # STEP 8: DISPLAY MICRO CONFUSION MATRIX
    # ======================================

    print("\nMICRO CONFUSION MATRIX")

    print("Rows = Actual, Columns = Predicted")
    print("                 Absent    Present")

    print(
        f"Actual absent   {tn:6d}    {fp:6d}"
    )

    print(
        f"Actual present  {fn:6d}    {tp:6d}"
    )

    # ======================================
    # STEP 9: SHOW ONE SKILL CONFUSION MATRIX
    # ======================================

    skill_matrices = multilabel_confusion_matrix(
        y_true,
        y_pred
    )

    python_index = all_skills.index("Python")

    python_matrix = skill_matrices[python_index]

    print("\nPYTHON SKILL CONFUSION MATRIX")
    print(python_matrix)

    # ======================================
    # STEP 10: SAVE EVALUATION REPORTS
    # ======================================

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    detail_df = pd.DataFrame(
        detailed_results
    )

    detail_path = (
        REPORTS_DIR / "skill_evaluation_cases.csv"
    )

    detail_df.to_csv(
        detail_path,
        index=False
    )

    summary_df = pd.DataFrame([
        {
            "Samples": len(records),
            "Dictionary Skills": len(all_skills),
            "TP": tp,
            "FP": fp,
            "FN": fn,
            "TN": tn,
            "Micro Precision": precision,
            "Micro Recall": recall,
            "Micro F1": f1,
            "Exact Match Accuracy": exact_match
        }
    ])

    summary_path = (
        REPORTS_DIR / "skill_evaluation_summary.csv"
    )

    summary_df.to_csv(
        summary_path,
        index=False
    )

    # ======================================
    # STEP 11: SHOW PER-EXAMPLE MISTAKES
    # ======================================

    print("\nEXAMPLES WITH ERRORS")

    errors = detail_df[
        detail_df["Exact Match"] == False
    ]

    if errors.empty:

        print("No errors on this evaluation set.")

    else:

        for _, row in errors.iterrows():

            print(f"\nExample: {row['ID']}")
            print("Text:", row["Text"])
            print("Extra skills:", row["Extra Skills"])
            print("Missed skills:", row["Missed Skills"])

    print("\nSaved:", detail_path)
    print("Saved:", summary_path)

    print("\nEvaluation completed successfully!")


# ==========================================
# STEP 12: RUN THE EVALUATION
# ==========================================

if __name__ == "__main__":
    evaluate()
