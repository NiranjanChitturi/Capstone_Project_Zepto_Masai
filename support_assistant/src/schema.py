"""
Module 3 - Pydantic Response Schema

Defines and validates the structured response returned by the
Zepto support assistant.

Required fields:
    - answer: str
    - sources: list[str]
    - confidence: float between 0 and 1

The mock response is deterministic.

The validation helper also provides the retry structure required
for the optional real-LLM path: up to two additional attempts
after an initial validation failure.
"""

from pydantic import BaseModel, Field, ValidationError


# ---------------------------------------------------------------------------
# Response schema
# ---------------------------------------------------------------------------

class SupportResponse(BaseModel):
    """
    Validated response returned by the support assistant.
    """

    answer: str

    sources: list[str]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


# ---------------------------------------------------------------------------
# Deterministic mock response
# ---------------------------------------------------------------------------

def create_mock_response(
    answer: str,
    source_ids: list[str],
) -> SupportResponse:
    """
    Create the deterministic response used by MOCK_LLM mode.

    Confidence is deterministic:
        - 0.9 when a source was retrieved
        - 0.5 for a general/direct answer
    """
    confidence = 0.9 if source_ids else 0.5

    return SupportResponse(
        answer=answer,
        sources=source_ids,
        confidence=confidence,
    )


# ---------------------------------------------------------------------------
# Validation with retry support
# ---------------------------------------------------------------------------

def validate_response_with_retry(
    response_data: dict,
    max_retries: int = 2,
) -> SupportResponse:
    """
    Validate response data using Pydantic.

    The assignment requires up to two additional retries after an
    initial validation failure for the optional real-LLM path.

    Args:
        response_data: Candidate response dictionary.
        max_retries: Number of additional validation attempts.

    Returns:
        A validated SupportResponse.

    Raises:
        ValueError: If validation fails after all permitted attempts.
    """
    attempts = 0
    max_attempts = 1 + max_retries

    while attempts < max_attempts:
        attempts += 1

        try:
            return SupportResponse.model_validate(response_data)

        except ValidationError as exc:
            if attempts >= max_attempts:
                raise ValueError(
                    "Response failed Pydantic validation after "
                    f"{max_attempts} attempts."
                ) from exc

            # In the optional real-LLM path, this is where the next
            # corrected LLM response would be requested.
            #
            # The deterministic mock path does not need retries because
            # it always constructs a valid SupportResponse.


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Demonstrate valid mock responses and validation failures.
    """
    print("Pydantic response schema test")
    print("-" * 60)

    # ---------------------------------------------------------------
    # Test 1 - Policy response
    # ---------------------------------------------------------------

    policy_response = create_mock_response(
        answer=(
            "Based on the retrieved context: "
            "orders below this threshold incur a flat INR 25 delivery fee."
        ),
        source_ids=["doc_01", "doc_05", "doc_03"],
    )

    print("Policy response:")
    print(policy_response.model_dump_json(indent=2))
    print()

    # ---------------------------------------------------------------
    # Test 2 - General response
    # ---------------------------------------------------------------

    general_response = create_mock_response(
        answer=(
            "I can only answer questions about Zepto policies right now."
        ),
        source_ids=[],
    )

    print("General response:")
    print(general_response.model_dump_json(indent=2))
    print()

    # ---------------------------------------------------------------
    # Test 3 - Explicit validation
    # ---------------------------------------------------------------

    validated_response = validate_response_with_retry(
        {
            "answer": "Test response",
            "sources": ["doc_01"],
            "confidence": 0.9,
        }
    )

    print("Validated response:")
    print(validated_response.model_dump_json(indent=2))
    print()

    # ---------------------------------------------------------------
    # Test 4 - Invalid confidence
    # ---------------------------------------------------------------

    try:
        validate_response_with_retry(
            {
                "answer": "Invalid response",
                "sources": ["doc_01"],
                "confidence": 1.5,
            }
        )
    except ValueError as exc:
        print("Invalid response correctly rejected:")
        print(exc)
        print()

    print("Pydantic response schema test completed successfully.")


if __name__ == "__main__":
    main()