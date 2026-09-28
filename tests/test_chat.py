import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# RAG folder
RAG_DIR = PROJECT_ROOT / "backend" / "app" / "rag"

# Add RAG folder to Python path
sys.path.insert(0, str(RAG_DIR))

# Import chatbot pipeline
from pipeline import generate_answer


def test_course_count():
    answer = generate_answer(
        "How many courses are offered by the university?"
    )

    assert "18" in answer


def test_bba_fee():
    answer = generate_answer(
        "What is the fee for BBA?"
    )

    assert "12402" in answer
    assert "5150" in answer


def test_bba_duration():
    answer = generate_answer(
        "What is the duration of BBA?"
    )

    assert "4 Years" in answer


def test_mcom_seats():
    answer = generate_answer(
        "How many seats are there in M.Com?"
    )

    assert "50" in answer


def test_btech_eligibility():
    answer = generate_answer(
        "What is the eligibility for B.Tech?"
    )

    assert "Eligibility" in answer


def test_unknown_course():
    answer = generate_answer(
        "What is the eligibility for BCA?"
    )

    assert "Information Not Available" in answer


def test_all_course_seats():
    answer = generate_answer(
        "How many seats are there in all courses?"
    )

    assert "Total Seats Across All Courses" in answer


def test_general_admission():
    answer = generate_answer(
        "Tell me about admission."
    )

    assert "Admission Information" in answer


def test_course_overview():
    answer = generate_answer(
        "Tell me about M.Com."
    )

    assert "M.Com" in answer


def test_mcom_duration():
    answer = generate_answer(
        "How long is M.Com?"
    )

    assert "2 Years" in answer


def test_bba_admission_mode():
    answer = generate_answer(
        "What is the admission mode for BBA?"
    )

    assert "BBA" in answer


def test_mcom_hod():
    answer = generate_answer(
        "Who is the HOD of M.Com?"
    )

    assert "Chairperson" in answer or "HOD" in answer


def test_bba_contact():
    answer = generate_answer(
        "What is the contact information for BBA?"
    )

    assert "BBA" in answer
    assert "Contact" in answer