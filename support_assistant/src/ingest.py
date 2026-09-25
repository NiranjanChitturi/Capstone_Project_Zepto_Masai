"""
Module 3 - Knowledge Base Ingestion

Loads the eight Zepto policy documents, creates one chunk per document,
generates local embeddings using all-MiniLM-L6-v2, and stores the
documents and embeddings in a persistent ChromaDB collection.

This implementation uses one chunk per document because the policy
documents are short and the assignment explicitly permits simple
per-document chunking.
"""

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SUPPORT_ASSISTANT_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = SUPPORT_ASSISTANT_DIR / "knowledge_base" / "docs"
CHROMA_DIR = SUPPORT_ASSISTANT_DIR / "data" / "chroma_db"

COLLECTION_NAME = "zepto_policies"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def load_documents() -> list[dict[str, str]]:
    """
    Load all policy documents from the knowledge-base directory.

    Returns:
        A list containing document IDs, names, and text content.
    """
    documents = []

    document_paths = sorted(DOCUMENTS_DIR.glob("doc_*.txt"))

    if len(document_paths) != 8:
        raise ValueError(
            f"Expected exactly 8 policy documents, found {len(document_paths)}."
        )

    for document_path in document_paths:
        text = document_path.read_text(encoding="utf-8").strip()

        if not text:
            raise ValueError(f"Document is empty: {document_path}")

        documents.append(
            {
                "document_id": document_path.stem,
                "document_name": document_path.name,
                "text": text,
            }
        )

    return documents


def create_chroma_collection():
    """
    Create or replace the persistent ChromaDB collection.

    The collection is rebuilt from the source documents each time the
    ingestion script runs, making the process deterministic and rerunnable.
    """
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Delete an existing collection so reruns always reflect the current
    # contents of the knowledge-base documents.
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    embedding_function = (
        embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
    )

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={
            "description": "Zepto policy knowledge base",
            "embedding_model": EMBEDDING_MODEL,
            "hnsw:space": "cosine",
        },
    )

    return collection


def ingest_documents() -> None:
    """
    Execute the complete knowledge-base ingestion process.
    """
    print("Starting Module 3 knowledge-base ingestion...")

    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    collection = create_chroma_collection()

    ids = [document["document_id"] for document in documents]
    texts = [document["text"] for document in documents]
    metadatas = [
        {
            "document_id": document["document_id"],
            "document_name": document["document_name"],
        }
        for document in documents
    ]

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
    )

    stored_count = collection.count()

    print(f"Documents/chunks stored in ChromaDB: {stored_count}")
    print(f"Embedding model: {EMBEDDING_MODEL}")
    print(f"ChromaDB directory: {CHROMA_DIR}")
    print("Knowledge-base ingestion completed successfully.")


# ---------------------------------------------------------------------------
# Script entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ingest_documents()