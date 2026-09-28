from pathlib import Path
from functools import lru_cache

from langchain_chroma import Chroma
from embeddings import get_embeddings

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PERSIST_DIRECTORY = str(PROJECT_ROOT / "data" / "chroma_db")


@lru_cache(maxsize=1)
def get_retriever(k=3):
    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name="university_courses"
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    return retriever