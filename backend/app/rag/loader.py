import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "courses.csv"


def load_courses():
    df = pd.read_csv(CSV_PATH)

    documents = []

    for _, row in df.iterrows():
        content = f"""
Course Name: {row['Course Name']}
Department: {row['Department']}
Duration: {row['Duration']}
Total Seats: {row['Total Seats']}
Admission Mode: {row['Admission Mode']}
Eligibility Criteria: {row['Eligibility Criteria']}
1st Sem Fee: {row['1st Sem Fee (Rs.)']}
2nd Sem Fee: {row['2nd Sem Fee (Rs.)']}
Chairperson / HOD: {row['Chairperson / HOD']}
Contact & Helpline: {row['Contact & Helpline']}
Admission Process: {row['Admission Process']}
"""

        documents.append(content.strip())

    return documents


if __name__ == "__main__":
    courses = load_courses()

    print("Total courses loaded:", len(courses))

    for i, course in enumerate(courses, start=1):
        print(f"\n--- Course {i} ---")
        print(course)