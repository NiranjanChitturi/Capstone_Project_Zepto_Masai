"""
Module 3 - Structured Prompt Template

Defines the structured prompt required for the Zepto support assistant.

The prompt contains:
    1. Role
    2. Context
    3. Task
    4. Format
    5. Length

It also includes:
    - An explicit negative constraint
    - A few-shot example

The template is designed for the optional real-LLM path.
The default MOCK_LLM path remains deterministic and does not depend
on an external LLM service.
"""


# ---------------------------------------------------------------------------
# Structured prompt template
# ---------------------------------------------------------------------------

PROMPT_TEMPLATE = """
ROLE:
You are a Zepto customer support assistant that answers questions
about Zepto policies using the retrieved knowledge-base context.

CONTEXT:
The following context was retrieved from the Zepto policy knowledge base:

{retrieved_context}

USER QUESTION:
{query}

TASK:
Answer the user's question using only the retrieved Zepto policy context.
If the retrieved context does not contain enough information to answer
the question, clearly state that the available policy context does not
provide enough information.

FORMAT:
Return a concise answer followed by the relevant source document IDs.
Use this structure:

Answer: <answer>
Sources: <comma-separated document IDs>

LENGTH:
Keep the answer concise and within 2 sentences unless additional detail
is required to accurately answer the question.

NEGATIVE CONSTRAINT:
Do not invent, assume, or add Zepto policies, fees, conditions, or
information that are not supported by the retrieved context.

FEW-SHOT EXAMPLE:

Example question:
What is the delivery fee for an order below INR 149?

Example context:
Zepto delivers grocery and household essentials to serviceable pin codes
within 10 to 30 minutes of order confirmation, depending on the customer's
delivery zone and current order volume. Standard delivery is free on orders
over INR 149; orders below this threshold incur a flat INR 25 delivery fee.

Example answer:
Answer: Orders below INR 149 incur a flat INR 25 standard delivery fee.
Sources: doc_01
"""


def build_prompt(
    query: str,
    retrieved_context: str,
) -> str:
    """
    Build the structured prompt using the user query and retrieved context.

    Args:
        query: User's question.
        retrieved_context: Retrieved policy text supplied to the prompt.

    Returns:
        A formatted structured prompt.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if not retrieved_context.strip():
        raise ValueError("Retrieved context cannot be empty.")

    return PROMPT_TEMPLATE.format(
        query=query.strip(),
        retrieved_context=retrieved_context.strip(),
    )


# ---------------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Demonstrate construction of the structured prompt.
    """
    query = "What is the delivery fee for an order below INR 149?"

    retrieved_context = (
        "Zepto delivers grocery and household essentials to serviceable "
        "pin codes within 10 to 30 minutes of order confirmation, depending "
        "on the customer's delivery zone and current order volume. Standard "
        "delivery is free on orders over INR 149; orders below this threshold "
        "incur a flat INR 25 delivery fee."
    )

    prompt = build_prompt(
        query=query,
        retrieved_context=retrieved_context,
    )

    print("Structured prompt test")
    print("-" * 60)
    print(prompt)
    print("-" * 60)
    print("Structured prompt test completed successfully.")


if __name__ == "__main__":
    main()