from langchain_chroma import Chroma

from loader import load_courses
from embeddings import get_embeddings
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PERSIST_DIRECTORY = str(PROJECT_ROOT / "data" / "chroma_db")

def create_vector_store():
    courses = load_courses()
    embeddings = get_embeddings()

    vector_store = Chroma.from_texts(
        texts=courses,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="university_courses"
    )

    return vector_store


if __name__ == "__main__":
    vector_store = create_vector_store()

    print("Vector database created successfully")

    results = vector_store.similarity_search(
        "What courses are available?",
        k=3
    )

    print("\nRetrieved documents:\n")

    for i, result in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(result.page_content)