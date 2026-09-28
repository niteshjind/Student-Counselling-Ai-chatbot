from functools import lru_cache
from langchain_ollama import ChatOllama


@lru_cache(maxsize=1)
def get_llm():
    return ChatOllama(
        model="llama3.2",
        temperature=0,
        num_predict=250,
        keep_alive="10m"
    )


if __name__ == "__main__":
    llm = get_llm()

    response = llm.invoke(
        "What is artificial intelligence?"
    )

    print(response.content)