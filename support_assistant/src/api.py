"""
Module 3 - FastAPI Support Assistant API

Exposes the LangGraph Zepto support assistant through:

    POST /ask

Request:
    {
        "query": "..."
    }

Response:
    {
        "answer": "...",
        "sources": ["..."],
        "confidence": 0.9
    }

The default behavior is deterministic and offline through MOCK_LLM.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .schema import create_mock_response
from .workflow import build_workflow


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline Zepto policy support assistant using LangGraph and ChromaDB.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Request schema
# ---------------------------------------------------------------------------

class AskRequest(BaseModel):
    """
    Request body accepted by POST /ask.
    """

    query: str = Field(
        min_length=1,
        description="User's Zepto support question.",
    )


# ---------------------------------------------------------------------------
# Response schema
# ---------------------------------------------------------------------------

class AskResponse(BaseModel):
    """
    Response returned by POST /ask.
    """

    answer: str
    sources: list[str]
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------

workflow = build_workflow()


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

@app.get("/")
def root() -> dict[str, str]:
    """
    Basic API health/status endpoint.
    """
    return {
        "status": "ok",
        "service": "Zepto Support Assistant",
    }


# ---------------------------------------------------------------------------
# Ask endpoint
# ---------------------------------------------------------------------------

@app.post(
    "/ask",
    response_model=AskResponse,
)
def ask(request: AskRequest) -> AskResponse:
    """
    Answer a Zepto support question using the LangGraph workflow.
    """
    result = workflow.invoke(
        {
            "query": request.query,
        }
    )

    response = create_mock_response(
        answer=result["answer"],
        source_ids=result.get("source_ids", []),
    )

    return AskResponse(
        answer=response.answer,
        sources=response.sources,
        confidence=response.confidence,
    )