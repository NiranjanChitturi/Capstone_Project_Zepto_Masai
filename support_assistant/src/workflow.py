"""
Module 3 - LangGraph Support Assistant Workflow

Implements the required LangGraph workflow:

    START
      |
      v
classify_intent
      |
      +-----------------------+
      |                       |
      v                       v
retrieve_and_answer     direct_answer
      |                       |
      +-----------+-----------+
                  |
                  v
                 END

The workflow uses a TypedDict state and three required nodes.

Intent classification follows the assignment's deterministic mock
heuristic when MOCK_LLM is enabled or unset.

Policy questions are routed through ChromaDB retrieval.
General questions are routed directly to the direct-answer node.
"""

import os
from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from .retrieve import retrieve_documents


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"

POLICY_KEYWORDS = (
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours",
)


# ---------------------------------------------------------------------------
# LangGraph state
# ---------------------------------------------------------------------------

class SupportState(TypedDict, total=False):
    """
    State passed between LangGraph nodes.
    """

    query: str
    intent: str
    retrieved_documents: list[dict]
    answer: str
    source_ids: list[str]


# ---------------------------------------------------------------------------
# Node 1 - Intent classification
# ---------------------------------------------------------------------------

def classify_intent(
    state: SupportState,
) -> dict:
    """
    Classify the user's query as a policy question or general question.

    The assignment requires the mock heuristic to classify a query as a
    policy question when the lowercase query contains any of the required
    policy keywords.
    """
    query = state["query"].lower()

    is_policy_question = any(
        keyword in query
        for keyword in POLICY_KEYWORDS
    )

    intent: Literal["policy_question", "general_question"]

    if is_policy_question:
        intent = "policy_question"
    else:
        intent = "general_question"

    return {
        "intent": intent,
    }


# ---------------------------------------------------------------------------
# Node 2 - Retrieve and answer
# ---------------------------------------------------------------------------

def retrieve_and_answer(
    state: SupportState,
) -> dict:
    """
    Retrieve the top three policy chunks and generate the deterministic
    mock answer required by the assignment.

    The retrieval step is always performed for policy questions.
    """
    query = state["query"]

    results = retrieve_documents(
        query=query,
        top_k=3,
    )

    document_ids = results["ids"][0]
    documents = results["documents"][0]

    if not documents:
        raise RuntimeError(
            "Policy retrieval returned no documents."
        )

    top_chunk_snippet = documents[0][:200]

    answer = (
        "Based on the retrieved context: "
        f"{top_chunk_snippet}"
    )

    return {
        "retrieved_documents": [
            {
                "document_id": document_id,
                "text": document,
            }
            for document_id, document in zip(
                document_ids,
                documents,
            )
        ],
        "answer": answer,
        "source_ids": document_ids,
    }


# ---------------------------------------------------------------------------
# Node 3 - Direct answer
# ---------------------------------------------------------------------------

def direct_answer(
    state: SupportState,
) -> dict:
    """
    Return the deterministic mock response for general questions.
    """
    return {
        "answer": (
            "I can only answer questions about Zepto policies right now."
        ),
        "source_ids": [],
    }


# ---------------------------------------------------------------------------
# Conditional routing
# ---------------------------------------------------------------------------

def route_intent(
    state: SupportState,
) -> str:
    """
    Route the workflow according to the classified intent.
    """
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_workflow():
    """
    Build and compile the LangGraph support-assistant workflow.
    """
    graph = StateGraph(SupportState)

    graph.add_node(
        "classify_intent",
        classify_intent,
    )

    graph.add_node(
        "retrieve_and_answer",
        retrieve_and_answer,
    )

    graph.add_node(
        "direct_answer",
        direct_answer,
    )

    graph.add_edge(
        START,
        "classify_intent",
    )

    graph.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "retrieve_and_answer": "retrieve_and_answer",
            "direct_answer": "direct_answer",
        },
    )

    graph.add_edge(
        "retrieve_and_answer",
        END,
    )

    graph.add_edge(
        "direct_answer",
        END,
    )

    return graph.compile()


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------

def run_test(query: str) -> None:
    """
    Execute one workflow test and display the resulting state.
    """
    workflow = build_workflow()

    result = workflow.invoke(
        {
            "query": query,
        }
    )

    print("=" * 70)
    print(f"Query: {query}")
    print(f"Intent: {result['intent']}")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result.get('source_ids', [])}")

    if result.get("retrieved_documents"):
        print("Retrieved documents:")
        for document in result["retrieved_documents"]:
            print(
                f"  - {document['document_id']}"
            )

    print("=" * 70)


def main() -> None:
    """
    Run one policy-question test and one general-question test.
    """
    print("LangGraph workflow test")
    print(f"MOCK_LLM enabled: {MOCK_LLM}")
    print()

    run_test(
        "What is the delivery fee for orders below INR 149?"
    )

    run_test(
        "What is the capital of India?"
    )

    print()
    print("LangGraph workflow test completed successfully.")


if __name__ == "__main__":
    main()