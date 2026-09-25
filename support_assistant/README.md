# Zepto Support Assistant

Module 3 of the Masai AI/ML Capstone Project.

This module implements a local, policy-grounded customer support assistant using the eight required Zepto policy documents provided in the assignment.

The implementation is designed to run locally without requiring a paid external LLM service. The default execution path uses deterministic mock responses.

---

## 1. Objective

Build a local customer support assistant that can:

- Load the eight required Zepto policy documents.
- Create document-level chunks.
- Generate local embeddings using `all-MiniLM-L6-v2`.
- Store embeddings and documents in ChromaDB.
- Retrieve the top-3 relevant policy chunks for policy questions.
- Classify questions into policy and general questions.
- Use a LangGraph workflow with conditional routing.
- Produce deterministic structured responses using Pydantic.
- Expose the assistant through a FastAPI `/ask` endpoint.
- Run the complete application inside Docker.

No paid external LLM service is required for the default implementation.

---

## 2. Architecture

The overall data flow is:

```text
                    KNOWLEDGE-BASE INGESTION
                              |
                              v
                   Eight Policy Documents
                              |
                              v
                       Document Loading
                              |
                              v
                    One Chunk per Document
                              |
                              v
                 all-MiniLM-L6-v2 Embeddings
                              |
                              v
                         ChromaDB
                              |
                              v
                         USER QUERY
                              |
                              v
                    FastAPI POST /ask
                              |
                              v
                     LangGraph Workflow
                              |
                              v
                     classify_intent
                       /            \
                      /              \
                     v                v
          policy_question      general_question
                  |                    |
                  v                    v
       retrieve_and_answer       direct_answer
                  |                    |
                  v                    |
             ChromaDB                  |
             top-3 retrieval            |
                  |                    |
                  +---------+----------+
                            |
                            v
                    Structured Response
                            |
                            v
                    Pydantic Validation
                            |
                            v
                         JSON
```

---

## 3. Knowledge Base

The knowledge base contains exactly eight policy documents:

```text
knowledge_base/docs/
├── doc_01.txt
├── doc_02.txt
├── doc_03.txt
├── doc_04.txt
├── doc_05.txt
├── doc_06.txt
├── doc_07.txt
└── doc_08.txt
```

The documents are copied from the required Module 3 corpus in the assignment.

The implementation uses one chunk per document because the supplied policy documents are short and the assignment permits simple per-document chunking.

---

## 4. Embeddings and ChromaDB

Embedding model:

```text
all-MiniLM-L6-v2
```

The model runs locally using Sentence Transformers.

ChromaDB is used as the persistent vector store.

The ingestion process:

1. Loads all eight policy documents.
2. Validates that exactly eight documents are present.
3. Creates one chunk per document.
4. Generates embeddings locally.
5. Stores the documents, metadata, and embeddings in ChromaDB.

Run ingestion with:

```powershell
python support_assistant\src\ingest.py
```

Expected result:

```text
Documents loaded: 8
Documents/chunks stored in ChromaDB: 8
Embedding model: all-MiniLM-L6-v2
Knowledge-base ingestion completed successfully.
```

The generated ChromaDB directory is intentionally not committed to Git.
It can be recreated from the eight corpus documents.

---

## 5. Source Files and Responsibilities

### `src/ingest.py`

Responsible for:

- Loading the eight policy documents.
- Creating document chunks.
- Initializing ChromaDB.
- Configuring `all-MiniLM-L6-v2`.
- Storing documents and metadata.

### `src/retrieve.py`

Responsible for:

- Loading the persistent ChromaDB collection.
- Embedding the incoming query.
- Performing semantic retrieval.
- Returning the top-3 results.

Example test:

```powershell
python support_assistant\src\retrieve.py
```

The implementation was verified using:

```text
What is the delivery fee for orders below INR 149?
```

The top result was:

```text
doc_01
```

### `src/prompt_template.py`

Contains the structured prompt template.

The prompt includes:

1. Role
2. Context
3. Task
4. Format
5. Length

It also contains:

- An explicit negative constraint.
- A few-shot example.

The prompt is designed to keep policy answers grounded in the supplied retrieved context.

Run the prompt demonstration with:

```powershell
python support_assistant\src\prompt_template.py
```

### `src/workflow.py`

Contains the LangGraph workflow.

The state is defined using `TypedDict`.

The workflow contains three required nodes:

```text
classify_intent
retrieve_and_answer
direct_answer
```

The graph is:

```text
START
  |
  v
classify_intent
  |
  +-------------------------+
  |                         |
  v                         v
retrieve_and_answer    direct_answer
  |                         |
  v                         v
 END                       END
```

#### `classify_intent`

The mock classifier uses the following keywords:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

If any keyword occurs in the lower-case query, the intent is:

```text
policy_question
```

Otherwise:

```text
general_question
```

#### `retrieve_and_answer`

For a policy question:

1. Retrieves the top-3 documents from ChromaDB.
2. Takes the first retrieved chunk.
3. Uses approximately the first 200 characters.
4. Produces the deterministic mock response:

```text
Based on the retrieved context: <top chunk snippet>
```

#### `direct_answer`

For a general question, the deterministic mock response is:

```text
I can only answer questions about Zepto policies right now.
```

The general-question route does not perform retrieval.

---

## 6. MOCK_LLM Behavior

The application defaults to deterministic mock mode.

The environment variable is interpreted as:

```text
MOCK_LLM=1
```

or when the variable is not set.

The implementation treats:

```text
MOCK_LLM != 0
```

as mock mode.

Therefore the default execution does not require an external LLM, API key, or paid service.

The routing logic itself is independent of the toggle.

The assignment allows an optional real-LLM implementation, but the current project implementation uses the deterministic mock path.

Setting:

```text
MOCK_LLM=0
```

The assignment does not require a real LLM provider for grading.

---

## 7. Structured Response Schema

The response is validated using Pydantic.

Schema:

```text
answer       : string
sources      : list[string]
confidence   : float between 0 and 1
```

Example policy response:

```json
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc_01",
    "doc_05",
    "doc_03"
  ],
  "confidence": 0.9
}
```

Example general response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 0.5
}
```

The validation layer allows the validation operation to be retried up to two additional times when validation fails.

---

## 8. FastAPI

The API is implemented in:

```text
src/api.py
```

Start the API locally with:

```powershell
uvicorn support_assistant.src.api:app --reload
```

The application runs on:

```text
http://127.0.0.1:8000
```

The endpoint is:

```text
POST /ask
```

Request:

```json
{
  "query": "What is the delivery fee for orders below INR 149?"
}
```

---

## 9. API Demonstration 1 - Policy Question

Request:

```powershell
(Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8000/ask" -Method Post -ContentType "application/json" -Body '{"query":"What is the delivery fee for orders below INR 149?"}').Content
```

Verified response:

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard del",
  "sources": [
    "doc_01",
    "doc_05",
    "doc_03"
  ],
  "confidence": 0.9
}
```

The response demonstrates the policy-question path:

```text
Query
  ↓
classify_intent
  ↓
policy_question
  ↓
retrieve_and_answer
  ↓
ChromaDB top-3
  ↓
structured response
```

---

## 10. API Demonstration 2 - General Question

Request:

```powershell
(Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8000/ask" -Method Post -ContentType "application/json" -Body '{"query":"What is the capital of India?"}').Content
```

Verified response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 0.5
}
```

The response demonstrates the direct-answer path:

```text
Query
  ↓
classify_intent
  ↓
general_question
  ↓
direct_answer
  ↓
structured response
```

No policy retrieval is performed for the general-question route.

---

## 11. Docker

A Dockerfile is provided at the project root:

```text
Dockerfile
```

A Module 3-specific dependency file is provided at:

```text
support_assistant/docker-requirements.txt
```

The Docker requirements use the CPU PyTorch package source to avoid installing the unnecessary CUDA dependency stack.

### Build

From the project root:

```powershell
docker build -t zepto-support-assistant:latest .
```

### Run

```powershell
docker run --name zepto-support-assistant -p 8000:8000 zepto-support-assistant:latest
```

The container starts FastAPI on:

```text
http://127.0.0.1:8000
```

### Docker Verification

The image was successfully built and the container was successfully started.

Both required API paths were tested inside the Dockerized application:

```text
Policy question     -> retrieval response       PASS
General question    -> direct response          PASS
```

The test container exited normally with:

```text
Exited (0)
```

---

## 12. Local Execution Order

For a fresh local setup, use:

### Step 1 - Install dependencies

From the repository root:

```powershell
pip install -r requirements.txt
```

### Step 2 - Build the knowledge base

```powershell
python support_assistant\src\ingest.py
```

### Step 3 - Test retrieval

```powershell
python support_assistant\src\retrieve.py
```

### Step 4 - Test the structured prompt

```powershell
python support_assistant\src\prompt_template.py
```

### Step 5 - Test the LangGraph workflow

```powershell
python -m support_assistant.src.workflow
```

### Step 6 - Test Pydantic validation

```powershell
python support_assistant\src\schema.py
```

### Step 7 - Start FastAPI

```powershell
uvicorn support_assistant.src.api:app --reload
```

### Step 8 - Call the API

Use the `/ask` endpoint with a JSON request containing `query`.

---

## 13. Component Summary

| Component | Responsibility |
|---|---|
| `knowledge_base/docs` | Required Zepto policy corpus |
| `ingest.py` | Document loading, chunking and ChromaDB ingestion |
| `retrieve.py` | Semantic top-3 policy retrieval |
| `prompt_template.py` | Structured prompt construction |
| `workflow.py` | LangGraph state and routing |
| `classify_intent` | Policy/general classification |
| `retrieve_and_answer` | Retrieval and policy response |
| `direct_answer` | General-question response |
| `schema.py` | Pydantic structured output and validation |
| `api.py` | FastAPI `/ask` endpoint |
| `docker-requirements.txt` | Docker-specific Module 3 dependencies |
| `Dockerfile` | Container build and FastAPI startup |

---

## 14. Design Decisions

### One chunk per document

The supplied policy documents are short. One chunk per document keeps the implementation simple and preserves document-level source identification.

### Local embeddings

`all-MiniLM-L6-v2` is used locally so that the application does not depend on an external embedding API.

### ChromaDB

ChromaDB provides local persistent vector storage and semantic retrieval.

### Deterministic mock responses

The default mock path makes the application reproducible and usable without API credentials.

### LangGraph

LangGraph explicitly represents the workflow and conditional routing required by the assignment.

### Pydantic

Pydantic provides deterministic validation of the final structured response.

### FastAPI

FastAPI provides a simple HTTP interface for testing and demonstration.

### Docker

Docker packages the Module 3 application and its local knowledge-base generation process into a reproducible runtime environment.

---

## 15. Repository Structure

```text
support_assistant/
├── README.md
├── docker-requirements.txt
├── knowledge_base/
│   └── docs/
│       ├── doc_01.txt
│       ├── doc_02.txt
│       ├── doc_03.txt
│       ├── doc_04.txt
│       ├── doc_05.txt
│       ├── doc_06.txt
│       ├── doc_07.txt
│       └── doc_08.txt
├── data/
│   └── chroma_db/              # generated locally, not committed
└── src/
    ├── api.py
    ├── ingest.py
    ├── prompt_template.py
    ├── retrieve.py
    ├── schema.py
    └── workflow.py
```

---

## 16. Module 3 Completion Status

```text
Eight policy documents                         [x]
Local all-MiniLM-L6-v2 embeddings             [x]
ChromaDB knowledge base                        [x]
Structured prompt                              [x]
Negative prompt constraint                      [x]
Few-shot example                               [x]
LangGraph StateGraph                           [x]
TypedDict state                                 [x]
Three workflow nodes                           [x]
Conditional routing                             [x]
Top-3 retrieval                                 [x]
Deterministic mock policy answer                [x]
Deterministic mock direct answer                [x]
Pydantic response schema                        [x]
Validation retry logic                          [x]
FastAPI /ask                                    [x]
Policy API demonstration                        [x]
General API demonstration                       [x]
Dockerfile                                      [x]
Docker build                                    [x]
Docker runtime test                             [x]
Architecture documentation                      [x]
```

---

## 17. Notes

The generated ChromaDB database is a runtime artifact and is intentionally excluded from Git. Running `ingest.py` recreates the local vector database from the required policy documents.

The default execution mode is offline and deterministic. No paid external LLM service is required.
