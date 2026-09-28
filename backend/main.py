from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
from pathlib import Path

RAG_DIR = Path(__file__).resolve().parent / "app" / "rag"
LLM_DIR = Path(__file__).resolve().parent / "app" / "llm"

sys.path.insert(0, str(RAG_DIR))
sys.path.insert(0, str(LLM_DIR))

from pipeline import generate_answer, get_course_data


app = FastAPI(
    title="Student Counselling AI",
    version="0.1.0",
    description="AI-powered Student Counselling Assistant"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


conversation_history = []


def get_course_from_question(question):
    question_normalized = question.lower().strip()
    df = get_course_data()

    for _, row in df.iterrows():
        course_name = str(row["Course Name"]).strip()
        course_normalized = course_name.lower()

        if course_normalized in question_normalized:
            return course_name

        base_name = course_name.split("(")[0].strip()
        base_normalized = base_name.lower()

        if base_normalized and base_normalized in question_normalized:
            return course_name

    return None

def is_follow_up_question(question):
    question_lower = question.lower().strip()

    follow_up_phrases = [
        "its ",
        "it's ",
        "it ",
        "it?",
        "it.",
        "this course",
        "that course",
        "the course",
        "after graduation",
        "how long is it",
        "how long does it",
        "what about its",
        "what about it",
    ]

    return any(
        phrase in question_lower
        for phrase in follow_up_phrases
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    original_question = request.message
    current_question = original_question
    current_course = get_course_from_question(original_question)

    if (
        is_follow_up_question(original_question)
        and conversation_history
    ):
        previous_course = conversation_history[-1].get("course")

        if previous_course:
            current_question = (
                f"{original_question} for {previous_course}"
            )
            current_course = previous_course

        else:
            return {
                "reply": (
                    "ℹ️ Course information is not available.\n\n"
                    "Please mention the course name so I can "
                    "provide the correct information."
                )
            }

    answer = generate_answer(current_question)

    conversation_history.append({
        "user": original_question,
        "assistant": answer,
        "course": current_course
    })

    if len(conversation_history) > 20:
        conversation_history.pop(0)

    return {"reply": answer}


@app.get("/")
def home():
    return {
        "message": "Student Counselling AI Backend is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }