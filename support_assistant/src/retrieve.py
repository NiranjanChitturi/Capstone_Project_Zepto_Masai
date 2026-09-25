"""
Module 3 - Policy Retrieval

Loads the persistent ChromaDB collection created by ingest.py and
retrieves the most relevant policy chunks for a user query.

The retrieval layer is independent of the MOCK_LLM setting because
embeddings and ChromaDB retrieval are required to run in both mock
and optional real-LLM modes.
"""

from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions


# ---------------------------------------------------------------------------
# Paths and configuration
# ---------------------------------------------------------------------------

SUPPORT_ASSISTANT_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = SUPPORT_ASSISTANT_DIR / "data" / "chroma_db"

COLLECTION_NAME = "zepto_policies"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ---------------------------------------------------------------------------
# ChromaDB connection
# ---------------------------------------------------------------------------

def get_collection():
    """
    Connect to the persistent ChromaDB collection.

    Returns:
        The existing Zepto policy collection.
    """
    if not CHROMA_DIR.exists():
        raise FileNotFoundError(
            f"ChromaDB directory not found: {CHROMA_DIR}. "
            "Run ingest.py first."
        )

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    embedding_function = (
        embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
    )

    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_function,
        )
    except Exception as exc:
        raise RuntimeError(
            f"ChromaDB collection '{COLLECTION_NAME}' was not found. "
            "Run ingest.py first."
        ) from exc

    return collection


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def retrieve_documents(
    query: str,
    top_k: int = 3,
) -> dict:
    """
    Retrieve the top-k most similar policy chunks.

    Args:
        query: User's policy question.
        top_k: Number of chunks to retrieve.

    Returns:
        ChromaDB query result containing documents, IDs, metadata,
        and distances.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    collection = get_collection()

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    return results


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Demonstrate policy retrieval using a delivery-policy question.
    """
    query = "What is the delivery fee for orders below INR 149?"

    print("Policy retrieval test")
    print("-" * 60)
    print(f"Query: {query}")
    print()

    results = retrieve_documents(query, top_k=3)

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for index, (
        document_id,
        document,
        metadata,
        distance,
    ) in enumerate(
        zip(ids, documents, metadatas, distances),
        start=1,
    ):
        print(f"Result {index}")
        print(f"  ID: {document_id}")
        print(f"  Document: {metadata['document_name']}")
        print(f"  Distance: {distance:.4f}")
        print(f"  Content: {document}")
        print()

    print("Policy retrieval test completed successfully.")


if __name__ == "__main__":
    main()