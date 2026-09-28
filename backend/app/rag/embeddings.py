from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings


if __name__ == "__main__":
    embeddings = get_embeddings()

    test_text = "What courses are available?"

    vector = embeddings.embed_query(test_text)

    print("Embedding created successfully")
    print("Vector length:", len(vector))