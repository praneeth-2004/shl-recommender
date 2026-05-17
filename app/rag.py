import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os

DATA_PATH = "data/shl_data.json"
CHROMA_PATH = "chroma_db"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    for item in data:
        content = f"{item['title']}. {item['description']}"
        documents.append(Document(page_content=content, metadata=item))

    return documents


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_store():
    documents = load_data()
    embeddings = get_embeddings()

    db = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    db.persist()
    print("Vector DB created!")


def query_rag(query):
    embeddings = get_embeddings()

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    results = db.similarity_search(query, k=3)
    return results

if __name__ == "__main__":
    create_vector_store()

    results = query_rag("I need a math test")

    for r in results:
        print(r.page_content)

def build_vector_db():
    if not os.path.exists(CHROMA_PATH):
        create_vector_store()