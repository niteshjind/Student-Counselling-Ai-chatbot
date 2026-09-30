import sys
import time
from pathlib import Path
from functools import lru_cache

import pandas as pd


# ============================================================
# PATHS
# ============================================================

RAG_DIR = Path(__file__).resolve().parent
LLM_DIR = RAG_DIR.parent / "llm"
PROJECT_ROOT = RAG_DIR.parents[2]

CSV_PATH = PROJECT_ROOT / "data" / "raw" / "courses.csv"


# ============================================================
# IMPORT PATHS
# ============================================================

sys.path.insert(0, str(RAG_DIR))
sys.path.insert(0, str(LLM_DIR))


from retriever import get_retriever
from prompts import build_prompt
from model import get_llm


# ============================================================
# LLM
# ============================================================

llm = get_llm()


# ============================================================
# LOAD COURSE DATA
# ============================================================

@lru_cache(maxsize=1)
def get_course_data():
    return pd.read_csv(CSV_PATH)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    text = str(text).lower()

    for char in [
        ".", ",", "(", ")", "[", "]",
        "{", "}", "-", "_", "/", "\\",
        "&", "'"
    ]:
        text = text.replace(char, " ")

    replacements = {
        "b tech": "btech",
        "m sc": "msc",
        "m com": "mcom",
        "m a": "ma",
        "m p ed": "mped",
        "b p ed": "bped",
        "m b a": "mba",
        "m c a": "mca",
        "b b a": "bba",
        "l l b": "llb",
        "b a": "ba",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = " ".join(text.split())

    return text


# ============================================================
# FIND COURSE
# ============================================================

def find_course(question):
    df = get_course_data()

    question_normalized = normalize_text(question)

    for _, row in df.iterrows():

        course_name = str(row["Course Name"])

        course_normalized = normalize_text(course_name)

        # Full course name
        if course_normalized in question_normalized:
            return row

        # Base course name
        base_name = course_name.split("(")[0].strip()
        base_normalized = normalize_text(base_name)

        if base_normalized and base_normalized in question_normalized:
            return row

    return None


# ============================================================
# COURSE-SPECIFIC QUESTION CHECK
# ============================================================

def is_course_specific_question(question):

    question_lower = question.lower()

    course_keywords = [
        "eligibility",
        "eligible",
        "qualification",
        "qualifications",
        "admission",
        "admission process",
        "fee",
        "fees",
        "fee structure",
        "duration",
        "how long",
        "seats",
        "seat",
        "hod",
        "chairperson",
        "contact",
        "helpline",
        "apply",
        "application process",
        "cost",
    ]

    return any(
        keyword in question_lower
        for keyword in course_keywords
    )


# ============================================================
# UNKNOWN COURSE PROTECTION
# ============================================================

def check_unknown_course(question):

    if not is_course_specific_question(question):
        return None

    question_lower = question.lower()

    # General queries which should not be
    # treated as unknown-course queries
    general_phrases = [
        "all courses",
        "all course",
        "available courses",
        "what courses are available",
        "which courses are available",
        "course list",
        "list of courses",
        "list all courses",

        "fee structure",
        "fee details",
        "fees of all courses",
        "fee of all courses",
        "fees for all courses",
        "all course fees",

        "duration of courses",
        "durations of courses",
        "duration of all courses",
        "durations of all courses",
        "all course duration",

        "total seats",
        "seats available",
        "how many seats",
        "how many courses",
        "how many course",
        "number of courses",
        "number of course",
        "total courses",

        "tell me about admission",
        "about admission",
        "admission information",
        "general admission",
        "admission details",
        "how does admission work",
        "how does admission work in the university",
    ]

    if any(
        phrase in question_lower
        for phrase in general_phrases
    ):
        return None

    # If course exists in CSV,
    # do not return unknown-course message
    course = find_course(question)

    if course is not None:
        return None

    # Phrases indicating a specific course is being discussed
    course_indicators = [
        " for ",
        " about ",
        " of ",
        " in ",
        " is ",
        " are ",
        " on ",
    ]

    padded_question = f" {question_lower} "

    has_course_indicator = any(
        indicator in padded_question
        for indicator in course_indicators
    )

    if has_course_indicator:

        return (
            "ℹ️ Information Not Available\n\n"
            "The course mentioned in your question is not "
            "available in the provided university data."
        )

    return None


# ============================================================
# ALL COURSES
# ============================================================

def get_all_courses():

    df = get_course_data()

    answer = "📚 Available Courses\n\n"

    for _, row in df.iterrows():
        answer += f"🎓 {row['Course Name']}\n"

    return answer.strip()


# ============================================================
# COURSE COUNT
# ============================================================

def get_course_count():

    df = get_course_data()

    total_courses = len(df)

    return (
        "🎓 Total Courses\n\n"
        f"There are {total_courses} courses "
        "offered by the university."
    )


# ============================================================
# ALL COURSE DURATIONS
# ============================================================

def get_all_course_durations():

    df = get_course_data()

    answer = "⏳ Duration of All Courses\n\n"

    for _, row in df.iterrows():

        answer += (
            f"🎓 {row['Course Name']}\n"
            f"⏳ Duration: {row['Duration']}\n\n"
        )

    return answer.strip()


# ============================================================
# ALL COURSE FEES
# ============================================================

def get_all_course_fees():

    df = get_course_data()

    answer = "📊 Fee Structure\n\n"

    for _, row in df.iterrows():

        answer += (
            f"🎓 {row['Course Name']}\n"
            f"💰 1st Sem Fee: ₹{row['1st Sem Fee (Rs.)']}\n"
            f"💰 2nd Sem Fee: ₹{row['2nd Sem Fee (Rs.)']}\n\n"
        )

    return answer.strip()


# ============================================================
# ALL COURSE SEATS
# ============================================================

def get_all_course_seats():

    df = get_course_data()

    answer = "🪑 Seats in All Courses\n\n"

    total_seats = 0

    for _, row in df.iterrows():

        seats = pd.to_numeric(
            row["Total Seats"],
            errors="coerce"
        )

        if pd.notna(seats):
            seats = int(seats)
            total_seats += seats
        else:
            seats = row["Total Seats"]

        answer += (
            f"🎓 {row['Course Name']}: "
            f"{seats}\n"
        )

    answer += (
        f"\n🪑 Total Seats Across All Courses: "
        f"{total_seats}"
    )

    return answer.strip()


# ============================================================
# COURSE COMPARISON
# ============================================================

def get_course_comparison():

    return (
        "🤔 Choosing the Right Course\n\n"

        "There is no single best course for every student.\n\n"

        "📚 Available Information\n\n"

        "The university data can be used to compare courses "
        "using these details:\n\n"

        "🎓 Eligibility\n"
        "⏳ Duration\n"
        "🪑 Total Seats\n"
        "💰 Fees\n"
        "📝 Admission Mode\n\n"

        "Please mention the courses you want to compare."
    )


# ============================================================
# GENERAL ADMISSION INFORMATION
# ============================================================

def get_general_admission_information():

    return (
        "📝 Admission Information\n\n"

        "Admission details vary by course.\n\n"

        "📋 The university data includes:\n\n"

        "• Admission Mode\n"
        "• Eligibility Criteria\n"
        "• Admission Process\n\n"

        "Please mention a course name to get its "
        "specific admission process.\n\n"

        "For example:\n"
        "• What is the admission process for BBA?\n"
        "• What is the admission process for MBA?"
    )


# ============================================================
# COURSE OVERVIEW
# ============================================================

def get_course_overview(question):

    course = find_course(question)

    if course is None:
        return None

    return (
        f"🎓 {course['Course Name']}\n\n"

        f"📚 Department: {course['Department']}\n"
        f"⏳ Duration: {course['Duration']}\n"
        f"🪑 Total Seats: {course['Total Seats']}\n"
        f"📝 Admission Mode: {course['Admission Mode']}\n"
        f"📈 Eligibility: {course['Eligibility Criteria']}\n"
        f"💰 1st Sem Fee: ₹{course['1st Sem Fee (Rs.)']}\n"
        f"💰 2nd Sem Fee: ₹{course['2nd Sem Fee (Rs.)']}\n"
        f"👨‍🏫 Chairperson / HOD: {course['Chairperson / HOD']}\n"
        f"📞 Contact: {course['Contact & Helpline']}\n"
        f"📝 Admission Process: {course['Admission Process']}"
    )


# ============================================================
# COURSE ELIGIBILITY
# ============================================================

def get_course_eligibility(question):

    course = find_course(question)

    if course is None:
        return None

    return (
        f"🎓 {course['Course Name']} Eligibility\n\n"
        f"📋 Eligibility Criteria: "
        f"{course['Eligibility Criteria']}"
    )


# ============================================================
# COURSE FEE
# ============================================================

def get_course_fee(question):

    course = find_course(question)

    if course is None:
        return None

    return (
        f"💰 {course['Course Name']} Fee Structure\n\n"
        f"💰 1st Sem Fee: ₹{course['1st Sem Fee (Rs.)']}\n"
        f"💰 2nd Sem Fee: ₹{course['2nd Sem Fee (Rs.)']}"
    )


# ============================================================
# COURSE DURATION
# ============================================================

def get_course_duration(question):

    course = find_course(question)

    if course is None:
        return None

    return (
        f"⏳ {course['Course Name']} Duration\n\n"
        f"⏳ Duration: {course['Duration']}"
    )


# ============================================================
# COURSE ADMISSION
# ============================================================

def get_course_admission(question):

    course = find_course(question)

    if course is None:
        return None

    return (
        f"📝 {course['Course Name']} Admission Process\n\n"
        f"📋 {course['Admission Process']}"
    )


# ============================================================
# COURSE SEATS
# ============================================================

def get_course_seats(question):

    course = find_course(question)

    if course is None:
        return None

    return (
        f"🪑 {course['Course Name']} Seats\n\n"
        f"🪑 Total Seats: {course['Total Seats']}"
    )


# ============================================================
# COURSE HOD
# ============================================================

def get_course_hod(question):

    course = find_course(question)

    if course is None:
        return None

    return (
        f"👨‍🏫 {course['Course Name']}\n\n"
        f"👨‍🏫 Chairperson / HOD: "
        f"{course['Chairperson / HOD']}"
    )


# ============================================================
# COURSE CONTACT
# ============================================================

def get_course_contact(question):

    course = find_course(question)

    if course is None:
        return None

    return (
        f"📞 {course['Course Name']} Contact Information\n\n"
        f"📞 Contact & Helpline: "
        f"{course['Contact & Helpline']}"
    )


# ============================================================
# MAIN ANSWER GENERATOR
# ============================================================

def generate_answer(question: str):

    total_start = time.perf_counter()

    question_lower = question.lower().strip()


    # --------------------------------------------------------
    # 1. COURSE COUNT
    # --------------------------------------------------------

    count_query = any(
        phrase in question_lower
        for phrase in [
            "how many courses",
            "how many course",
            "number of courses",
            "number of course",
            "total number of courses",
            "total courses",
        ]
    )

    if count_query:
        answer = get_course_count()

        total_time = time.perf_counter() - total_start

        print(
            f"⏱️ Direct response | "
            f"Total: {total_time:.4f} sec"
        )

        return answer


    # --------------------------------------------------------
    # 2. ALL COURSE SEATS
    # --------------------------------------------------------

    all_seats_query = any(
        phrase in question_lower
        for phrase in [
            "seats in all courses",
            "seats are there in all courses",
            "how many seats are there in all courses",
            "total seats of all courses",
            "total seats in all courses",
            "seats of all courses",
            "all course seats",
            "all courses seats",
        ]
    )

    if all_seats_query:
        answer = get_all_course_seats()

        total_time = time.perf_counter() - total_start

        print(
            f"⏱️ Direct response | "
            f"Total: {total_time:.4f} sec"
        )

        return answer


    # --------------------------------------------------------
    # 3. GENERAL ADMISSION
    # --------------------------------------------------------

    general_admission_query = any(
        phrase in question_lower
        for phrase in [
            "tell me about admission",
            "about admission",
            "admission information",
            "general admission",
            "admission details",
            "how does admission work",
            "how does admission work in the university",
        ]
    )

    if general_admission_query:
        answer = get_general_admission_information()

        total_time = time.perf_counter() - total_start

        print(
            f"⏱️ Direct response | "
            f"Total: {total_time:.4f} sec"
        )

        return answer


    # --------------------------------------------------------
    # 4. UNKNOWN COURSE PROTECTION
    # --------------------------------------------------------

    unknown_course_response = check_unknown_course(question)

    if unknown_course_response:

        total_time = time.perf_counter() - total_start

        print(
            f"⏱️ Direct response | "
            f"Total: {total_time:.4f} sec"
        )

        return unknown_course_response


    # --------------------------------------------------------
    # 5. COURSE RECOMMENDATION
    # --------------------------------------------------------

    recommendation_query = any(
        phrase in question_lower
        for phrase in [
            "which course is best",
            "which course should i choose",
            "which course is better",
            "recommend a course",
            "best course for me",
            "course best for me",
            "which course is good for me",
        ]
    )

    if recommendation_query:
        answer = get_course_comparison()

        total_time = time.perf_counter() - total_start

        print(
            f"⏱️ Direct response | "
            f"Total: {total_time:.4f} sec"
        )

        return answer


    # --------------------------------------------------------
    # 6. COURSE LIST
    # --------------------------------------------------------

    course_list_query = any(
        phrase in question_lower
        for phrase in [
            "what courses are available",
            "which courses are available",
            "list all courses",
            "list the courses",
            "available courses",
            "courses offered",
            "what courses do you offer",
            "which courses do you offer",
        ]
    )

    if course_list_query:
        answer = get_all_courses()

        total_time = time.perf_counter() - total_start

        print(
            f"⏱️ Direct response | "
            f"Total: {total_time:.4f} sec"
        )

        return answer


    # --------------------------------------------------------
    # 7. ALL COURSE DURATION
    # --------------------------------------------------------

    duration_query = any(
        phrase in question_lower
        for phrase in [
            "duration of all courses",
            "durations of all courses",
            "duration for all courses",
            "all course duration",
            "duration of courses",
            "durations of courses",
        ]
    )

    if duration_query:
        answer = get_all_course_durations()

        total_time = time.perf_counter() - total_start

        print(
            f"⏱️ Direct response | "
            f"Total: {total_time:.4f} sec"
        )

        return answer


    # --------------------------------------------------------
    # 8. ALL COURSE FEES
    # --------------------------------------------------------

    fee_query = any(
        phrase in question_lower
        for phrase in [
            "fee structure of all courses",
            "fees of all courses",
            "fee of all courses",
            "fees for all courses",
            "all course fees",
            "what is the fee structure",
            "fee structure",
            "fee details",
        ]
    )

    if fee_query:
        answer = get_all_course_fees()

        total_time = time.perf_counter() - total_start

        print(
            f"⏱️ Direct response | "
            f"Total: {total_time:.4f} sec"
        )

        return answer


    # --------------------------------------------------------
    # 9. COURSE ELIGIBILITY
    # --------------------------------------------------------

    eligibility_query = (
        "eligibility" in question_lower
        or "eligible" in question_lower
        or "qualification" in question_lower
        or "qualifications" in question_lower
    )

    if eligibility_query:

        answer = get_course_eligibility(question)

        if answer:

            total_time = time.perf_counter() - total_start

            print(
                f"⏱️ Direct response | "
                f"Total: {total_time:.4f} sec"
            )

            return answer


    # --------------------------------------------------------
    # 10. COURSE FEE
    # --------------------------------------------------------

    fee_specific_query = (
        "fee" in question_lower
        or "fees" in question_lower
        or "cost" in question_lower
    )

    if fee_specific_query:

        answer = get_course_fee(question)

        if answer:

            total_time = time.perf_counter() - total_start

            print(
                f"⏱️ Direct response | "
                f"Total: {total_time:.4f} sec"
            )

            return answer


    # --------------------------------------------------------
    # 11. COURSE DURATION
    # --------------------------------------------------------

    duration_specific_query = (
        "duration" in question_lower
        or "how long" in question_lower
    )

    if duration_specific_query:

        answer = get_course_duration(question)

        if answer:

            total_time = time.perf_counter() - total_start

            print(
                f"⏱️ Direct response | "
                f"Total: {total_time:.4f} sec"
            )

            return answer


    # --------------------------------------------------------
    # 12. COURSE ADMISSION
    # --------------------------------------------------------

    admission_query = (
        "admission" in question_lower
        or "apply" in question_lower
        or "application process" in question_lower
    )

    if admission_query:

        answer = get_course_admission(question)

        if answer:

            total_time = time.perf_counter() - total_start

            print(
                f"⏱️ Direct response | "
                f"Total: {total_time:.4f} sec"
            )

            return answer


    # --------------------------------------------------------
    # 13. COURSE SEATS
    # --------------------------------------------------------

    seats_query = (
        "seats" in question_lower
        or "seat" in question_lower
    )

    if seats_query:

        answer = get_course_seats(question)

        if answer:

            total_time = time.perf_counter() - total_start

            print(
                f"⏱️ Direct response | "
                f"Total: {total_time:.4f} sec"
            )

            return answer


    # --------------------------------------------------------
    # 14. COURSE HOD
    # --------------------------------------------------------

    hod_query = (
        "hod" in question_lower
        or "chairperson" in question_lower
        or "head of department" in question_lower
    )

    if hod_query:

        answer = get_course_hod(question)

        if answer:

            total_time = time.perf_counter() - total_start

            print(
                f"⏱️ Direct response | "
                f"Total: {total_time:.4f} sec"
            )

            return answer


    # --------------------------------------------------------
    # 15. COURSE CONTACT
    # --------------------------------------------------------

    contact_query = (
        "contact" in question_lower
        or "helpline" in question_lower
        or "phone number" in question_lower
    )

    if contact_query:

        answer = get_course_contact(question)

        if answer:

            total_time = time.perf_counter() - total_start

            print(
                f"⏱️ Direct response | "
                f"Total: {total_time:.4f} sec"
            )

            return answer


    # --------------------------------------------------------
    # 16. COURSE OVERVIEW
    # --------------------------------------------------------

    course_overview_query = any(
        phrase in question_lower
        for phrase in [
            "tell me about",
            "information about",
            "details about",
            "details of",
            "information on",
            "give me information",
        ]
    )

    if course_overview_query:

        answer = get_course_overview(question)

        if answer:

            total_time = time.perf_counter() - total_start

            print(
                f"⏱️ Direct response | "
                f"Total: {total_time:.4f} sec"
            )

            return answer


    # --------------------------------------------------------
    # 17. BROAD RAG QUESTION
    # --------------------------------------------------------

    broad_question = any(
        phrase in question_lower
        for phrase in [
            "how many courses",
            "how many course",
            "seats available",
            "total seats",
            "all seats",
        ]
    )


    # --------------------------------------------------------
    # 18. RETRIEVER CREATION
    # --------------------------------------------------------

    retriever_start = time.perf_counter()

    if broad_question:

        retriever = get_retriever(k=18)

    else:

        retriever = get_retriever(k=3)

    retriever_create_time = (
        time.perf_counter() - retriever_start
    )

    print(
        f"⏱️ Retriever Creation: "
        f"{retriever_create_time:.4f} sec"
    )


    # --------------------------------------------------------
    # 19. RETRIEVE CONTEXT
    # --------------------------------------------------------

    retrieval_start = time.perf_counter()

    results = retriever.invoke(question)

    retrieval_time = (
        time.perf_counter() - retrieval_start
    )

    context = [
        result.page_content
        for result in results
    ]


    # --------------------------------------------------------
    # 20. BUILD PROMPT
    # --------------------------------------------------------

    prompt_start = time.perf_counter()

    prompt = build_prompt(
        question,
        context
    )

    prompt_time = (
        time.perf_counter() - prompt_start
    )


    # --------------------------------------------------------
    # 21. LLM RESPONSE
    # --------------------------------------------------------

    llm_start = time.perf_counter()

    response = llm.invoke(prompt)

    llm_time = (
        time.perf_counter() - llm_start
    )


    # --------------------------------------------------------
    # PERFORMANCE BREAKDOWN
    # --------------------------------------------------------

    total_time = time.perf_counter() - total_start

    print("\n" + "=" * 60)
    print("⏱️ PERFORMANCE BREAKDOWN")
    print("=" * 60)
    print(
        f"🔧 Retriever Creation: "
        f"{retriever_create_time:.4f} sec"
    )
    print(
        f"🔎 Retrieval:          "
        f"{retrieval_time:.4f} sec"
    )
    print(
        f"📝 Prompt Build:       "
        f"{prompt_time:.4f} sec"
    )
    print(
        f"🤖 LLM:                "
        f"{llm_time:.4f} sec"
    )
    print(
        f"⏱️ Total:              "
        f"{total_time:.4f} sec"
    )
    print("=" * 60)

    return response.content


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_questions = [
        "How many courses are offered by the university?",
        "How many seats are there in all courses?",
        "What is the eligibility for B.Tech?",
        "What is the fee for BBA?",
        "What is the admission process for MBA?",
    ]

    for question in test_questions:

        print("\n" + "=" * 60)
        print("QUESTION:")
        print(question)

        print("\nANSWER:")

        try:
            answer = generate_answer(question)
            print(answer)

        except Exception as error:
            print("ERROR:")
            print(error)