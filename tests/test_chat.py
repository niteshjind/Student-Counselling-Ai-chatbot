import sys
from pathlib import Path

import pytest

# ===========================================================
# PROJECT PATH SETUP
# ===========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAG_DIR = PROJECT_ROOT / "backend" / "app" / "rag"

sys.path.insert(0, str(RAG_DIR))

from pipeline import generate_answer


# ============================================================
# BASIC RESPONSE TESTS
# ============================================================

def test_response_is_not_empty():
    answer = generate_answer("Hello")

    assert answer
    assert len(answer.strip()) > 0


def test_general_help():
    answer = generate_answer("What can you help me with?")

    assert answer
    assert len(answer.strip()) > 20


def test_general_admission():
    answer = generate_answer("Tell me about admission.")

    assert "Admission" in answer


# ============================================================
# BBA TESTS
# ============================================================

def test_bba_information():
    answer = generate_answer("Tell me about BBA.")

    assert "BBA" in answer


def test_bba_eligibility():
    answer = generate_answer("What is the eligibility for BBA?")

    assert "BBA" in answer
    assert "Eligibility" in answer


def test_bba_fee():
    answer = generate_answer("What is the fee for BBA?")

    assert "BBA" in answer
    assert "Fee" in answer or "Fees" in answer


def test_bba_duration():
    answer = generate_answer("What is the duration of BBA?")

    assert "BBA" in answer
    assert "Duration" in answer


def test_bba_admission():
    answer = generate_answer(
        "What is the admission process for BBA?"
    )

    assert "BBA" in answer
    assert "Admission" in answer


def test_bba_admission_mode():
    answer = generate_answer(
        "What is the admission mode for BBA?"
    )

    assert "BBA" in answer


def test_bba_contact():
    answer = generate_answer(
        "What is the contact information for BBA?"
    )

    assert "BBA" in answer


# ============================================================
# M.COM TESTS
# ============================================================

def test_mcom_information():
    answer = generate_answer("Tell me about M.Com.")

    assert "M.Com" in answer or "M.Com." in answer


def test_mcom_eligibility():
    answer = generate_answer(
        "What is the eligibility for M.Com?"
    )

    assert "Eligibility" in answer


def test_mcom_duration():
    answer = generate_answer(
        "How long is M.Com?"
    )

    assert "Duration" in answer or "M.Com" in answer


def test_mcom_seats():
    answer = generate_answer(
        "How many seats are there in M.Com?"
    )

    assert "M.Com" in answer or "Seats" in answer


def test_mcom_hod():
    answer = generate_answer(
        "Who is the HOD of M.Com?"
    )

    assert (
        "HOD" in answer
        or "Chairperson" in answer
        or "M.Com" in answer
    )


# ============================================================
# ALL COURSE TESTS
# ============================================================

def test_course_count():
    answer = generate_answer(
        "How many courses are offered by the university?"
    )

    assert answer
    assert (
        "course" in answer.lower()
        or "courses" in answer.lower()
    )


def test_available_courses():
    answer = generate_answer(
        "What courses are available?"
    )

    assert answer
    assert "course" in answer.lower()


def test_course_list():
    answer = generate_answer(
        "Give me the list of courses."
    )

    assert answer
    assert "course" in answer.lower()


def test_all_course_seats():
    answer = generate_answer(
        "How many seats are there in all courses?"
    )

    assert answer
    assert "seat" in answer.lower()


def test_all_course_fees():
    answer = generate_answer(
        "Show me the fee structure."
    )

    assert answer
    assert "fee" in answer.lower()


def test_course_durations():
    answer = generate_answer(
        "What are the durations of courses?"
    )

    assert answer
    assert "duration" in answer.lower()


# ============================================================
# UNKNOWN COURSE PROTECTION
# ============================================================

def test_unknown_bca():
    answer = generate_answer(
        "What is the eligibility for BCA?"
    )

    assert "Information Not Available" in answer


def test_unknown_llb():
    answer = generate_answer(
        "Is LLB available?"
    )

    assert answer
    assert (
        "not available" in answer.lower()
        or "information not available" in answer.lower()
        or "course" in answer.lower()
    )


def test_unknown_course_fee():
    answer = generate_answer(
        "What is the fee for XYZ Engineering?"
    )

    assert answer
    assert (
        "not available" in answer.lower()
        or "information not available" in answer.lower()
    )


def test_unknown_course_duration():
    answer = generate_answer(
        "How long is XYZ course?"
    )

    assert answer


# ============================================================
# UNSUPPORTED / OUT-OF-DOMAIN QUESTIONS
# ============================================================

def test_prime_minister_question():
    answer = generate_answer(
        "Who is the Prime Minister of India?"
    )

    assert answer

    # The bot should not pretend university data contains
    # political information.
    assert (
        "not available" in answer.lower()
        or "university data" in answer.lower()
    )


def test_joke_question():
    answer = generate_answer(
        "Tell me a joke."
    )

    assert answer
    assert (
        "not available" in answer.lower()
        or "joke" in answer.lower()
    )


def test_hostel_question():
    answer = generate_answer(
        "What are the hostel facilities?"
    )

    assert answer
    assert (
        "not available" in answer.lower()
        or "university data" in answer.lower()
        or "hostel" in answer.lower()
    )


# ============================================================
# DIFFERENT QUESTION FORMATS
# ============================================================

def test_lowercase_question():
    answer = generate_answer(
        "what is the eligibility for bba?"
    )

    assert answer
    assert "BBA" in answer or "eligibility" in answer.lower()


def test_uppercase_question():
    answer = generate_answer(
        "WHAT IS THE ELIGIBILITY FOR BBA?"
    )

    assert answer


def test_question_with_punctuation():
    answer = generate_answer(
        "What is the fee for BBA???"
    )

    assert answer


def test_natural_language_question():
    answer = generate_answer(
        "Can you tell me how long the BBA course is?"
    )

    assert answer


# ============================================================
# NO HALLUCINATION / DATA-GROUNDING TESTS
# ============================================================

def test_unknown_course_does_not_give_random_details():
    answer = generate_answer(
        "Tell me everything about ABC123 course."
    )

    assert answer

    assert (
        "not available" in answer.lower()
        or "information not available" in answer.lower()
        or "provided university data" in answer.lower()
    )


def test_random_fee_question():
    answer = generate_answer(
        "What is the fee of Harvard University?"
    )

    assert answer
    assert (
        "not available" in answer.lower()
        or "university data" in answer.lower()
    )


# ============================================================
# PARAMETRIZED GENERAL TESTS
# ============================================================

@pytest.mark.parametrize(
    "question",
    [
        "Hello",
        "Hi",
        "What can you help me with?",
        "Tell me about the university.",
        "What courses are offered?",
        "Show available courses.",
    ],
)
def test_common_questions_return_answer(question):
    answer = generate_answer(question)

    assert answer
    assert len(answer.strip()) > 0


@pytest.mark.parametrize(
    "question",
    [
        "What is the eligibility for BBA?",
        "What are the fees for BBA?",
        "How long is BBA?",
        "What is the admission process for BBA?",
        "Who is the HOD of BBA?",
    ],
)
def test_bba_question_variations(question):
    answer = generate_answer(question)

    assert answer
    assert len(answer.strip()) > 10


@pytest.mark.parametrize(
    "question",
    [
        "What is the eligibility for BCA?",
        "Is LLB available?",
        "What is the fee for XYZ course?",
        "Tell me about ABC123.",
    ],
)
def test_unknown_course_questions(question):
    answer = generate_answer(question)

    assert answer
    assert len(answer.strip()) > 10
