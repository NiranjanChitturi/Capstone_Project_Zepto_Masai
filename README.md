# Zepto Data & AI Platform

Masai School AI/ML Capstone Project

This repository contains an end-to-end data engineering, analytics, machine learning, and AI support assistant project developed as part of the Masai School capstone.

The project is organized into three major modules:

1. **Data Pipeline**
2. **Analytics & Machine Learning**
3. **RAG Support Assistant**

The implementation is designed to be reproducible, documented, and executable from a clean Python environment.

---

## Project Objectives

The project demonstrates:

- Web data collection and scraping
- Data cleaning and validation
- Currency conversion
- Relational database design
- SQL analysis
- Pandas-based data analysis
- Exploratory data analysis
- Machine learning classification and regression
- Model evaluation and comparison
- Retrieval-Augmented Generation (RAG)
- Local vector database usage
- LangGraph workflow orchestration
- Pydantic structured-output validation
- FastAPI API development
- Docker-based local execution

---

# Repository Structure

```text
Capstone_Project_Zepto_Masai/
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
│
├── data_pipeline/
│   ├── README.md
│   ├── src/
│   │   ├── scraper.py
│   │   ├── cleaner.py
│   │   ├── database.py
│   │   ├── queries.py
│   │   └── pipeline.py
│   └── data/
│       ├── database/
│       │   └── books.db
│       ├── raw/
│       │   └── books_raw.csv
│       ├── processed/
│       │   └── books_cleaned.csv
│       └── outputs/
│
├── analytics/
│   ├── README.md
│   ├── data/
│   │   └── titanic.csv
│   ├── notebooks/
│   ├── outputs/
│   └── src/
│
└── support_assistant/
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
    │   └── chroma_db/          # generated locally; not committed
    └── src/
        ├── api.py
        ├── ingest.py
        ├── prompt_template.py
        ├── retrieve.py
        ├── schema.py
        └── workflow.py
```

---

# Installation

## Prerequisites

- Python 3.12
- Git
- Docker Desktop for Docker testing

The project was developed and tested with Python 3.12.

## Create the Python environment

From the repository root:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

The root `requirements.txt` contains the dependencies used across the three modules.

---

# Module 1 — Data Pipeline

## Objective

The Data Pipeline module demonstrates an end-to-end workflow:

```text
Web Scraping
     ↓
Raw CSV
     ↓
Data Cleaning & Validation
     ↓
Processed CSV
     ↓
SQLite Database
     ↓
SQL Analysis
     ↓
Pandas JOIN Verification
```

## Dataset

The scraper uses:

```text
https://books.toscrape.com/
```

The implementation processes:

- **93 books**
- **3 categories**

Selected categories:

- Mystery — 32 books
- Historical Fiction — 26 books
- Romance — 35 books

Total:

```text
32 + 26 + 35 = 93 books
```

The required minimum is 60 books and 3 categories.

## Required Fields

The scraper collects:

- `title`
- `price`
- `star_rating`
- `availability`
- `category`

## Data Cleaning

The raw fields are transformed into:

| Raw Field | Cleaned Field |
|---|---|
| `price` | `price_gbp` |
| `star_rating` | `rating` |
| `availability` | `in_stock` |
| `category` | `category` |

The cleaned dataset additionally contains:

```text
price_inr
```

A fixed artificial conversion rate is used:

```text
1 GBP = 105.50 INR
```

Therefore:

```text
price_inr = price_gbp × 105.50
```

No external currency API is used.

## SQLite Database

The database is:

```text
data_pipeline/data/database/books.db
```

It contains two normalized tables:

### `categories`

```text
category_id      INTEGER PRIMARY KEY
category_name    TEXT UNIQUE
```

### `books`

```text
book_id          INTEGER PRIMARY KEY
title            TEXT
price_gbp        REAL
price_inr        REAL
rating           INTEGER
in_stock         INTEGER
category_id      INTEGER FOREIGN KEY
```

The database enables foreign-key enforcement and is rebuilt transactionally during the pipeline.

## SQL Analysis

Five SQL queries demonstrate:

1. SELECT / WHERE
2. ORDER BY / LIMIT
3. DISTINCT
4. BETWEEN
5. JOIN

Query outputs are stored under:

```text
data_pipeline/data/outputs/
```

The SQL summary is documented in:

```text
data_pipeline/data/outputs/query_summary.md
```

## SQL and Pandas Verification

The SQL JOIN is independently reproduced using:

```python
pandas.merge()
```

The verification confirms that the SQL and pandas JOIN produce the same result.

The verification report is:

```text
data_pipeline/data/outputs/join_verification.md
```

## Run Module 1

From the repository root:

```powershell
python -m data_pipeline.src.pipeline
```

The pipeline performs:

1. Scraping
2. Raw-data validation
3. Raw CSV generation
4. Data cleaning
5. Cleaned-data validation
6. Processed CSV generation
7. SQLite database rebuild
8. SQL analysis
9. Pandas JOIN verification

Detailed documentation:

```text
data_pipeline/README.md
```

### Module 1 Status

**Completed**

---

# Module 2 — Analytics & Machine Learning

## Objective

The Analytics module uses the Titanic dataset to demonstrate exploratory data analysis, visualization, classification, model evaluation, imbalance handling, hyperparameter tuning, and regression.

The dataset is saved locally so the analysis is reproducible without requiring a fresh external dataset download.

Dataset:

```text
analytics/data/titanic.csv
```

## Exploratory Data Analysis

The module covers:

- Dataset shape and structure
- `info()`
- `describe()`
- Missing-value analysis
- Missing-value threshold handling
- Age and fare distributions
- Histograms
- Box plots
- IQR-based outlier analysis
- Fare mean, median, mode, and skew
- Boolean masks
- Survival-rate analysis
- Six-column correlation matrix
- Correlation heatmap
- Strongest absolute correlations
- Multivariate visualizations
- Exploratory feature standardization

## Classification

The module uses a stratified train/test split and train-only preprocessing.

The following models are evaluated:

- Logistic Regression
- Decision Tree
- Random Forest

Evaluation includes:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Confusion matrices
- ROC curves

## Class Imbalance

Random Forest is evaluated using:

- Baseline training
- Balanced class weights
- SMOTE

## Hyperparameter Tuning

Random Forest is tuned using `GridSearchCV`.

The search includes:

- `n_estimators`
- `max_depth`
- `max_features`

The tuned Random Forest also uses:

```text
oob_score=True
```

## Regression

A regression model is used to predict fare.

Evaluation includes:

- MAE
- RMSE
- R²
- Adjusted R²
- Residual analysis

## Model Persistence

The complete fitted preprocessing/model pipeline is saved using `joblib` and can be reloaded for prediction.

## Verified Classification Results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8045 | 0.7931 | 0.6667 | 0.7244 | 0.8437 |
| Decision Tree | 0.8156 | 0.7903 | 0.7101 | 0.7481 | 0.7904 |
| Random Forest | 0.8156 | 0.8000 | 0.6957 | 0.7442 | 0.8300 |

Tuned Random Forest:

```text
Accuracy : 0.8101
Precision: 0.8723
Recall   : 0.5942
F1       : 0.7069
ROC-AUC  : 0.8465
CV AUC   : 0.8721
OOB Score: 0.8301
```

Selected parameters:

```text
n_estimators = 200
max_depth    = 5
max_features = sqrt
```

## Verified Regression Results

```text
MAE          = 20.8977
RMSE         = 30.5328
R²           = 0.3975
Adjusted R²  = 0.3617
```

## Saved Model Prediction Test

A persisted model was reloaded and tested using:

```text
pclass   = 1
sex      = female
age      = 30
sibsp    = 0
parch    = 0
fare     = 80
embarked = S
```

The verified output was:

```text
Predicted class       = 1
Survival probability  = 0.9721
```

## Module 2 Status

**Completed**

Detailed documentation:

```text
analytics/README.md
```

---

# Module 3 — RAG Support Assistant

## Objective

The Support Assistant implements a local, policy-grounded customer support system using the eight required policy documents.

The module includes:

- Knowledge-base ingestion
- Document chunking
- Local Sentence Transformer embeddings
- ChromaDB
- Semantic retrieval
- Structured prompt engineering
- LangGraph
- Deterministic `MOCK_LLM`
- Pydantic validation
- FastAPI
- Docker

## Knowledge Base

The exact eight required documents are stored in:

```text
support_assistant/knowledge_base/docs/
```

```text
doc_01.txt
doc_02.txt
doc_03.txt
doc_04.txt
doc_05.txt
doc_06.txt
doc_07.txt
doc_08.txt
```

## Embeddings

The required local model is:

```text
all-MiniLM-L6-v2
```

Documents are embedded locally and stored in ChromaDB.

The implementation uses one chunk per document because the supplied policy documents are short.

## Build the Knowledge Base

Run:

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

The generated ChromaDB directory is intentionally excluded from Git and can be recreated from the corpus.

## Retrieval

Test semantic retrieval with:

```powershell
python support_assistant\src\retrieve.py
```

The implementation retrieves the top-3 relevant policy chunks.

A verified delivery-fee query returned:

```text
doc_01
doc_05
doc_03
```

with `doc_01` as the top result.

## Structured Prompt

The prompt template is implemented in:

```text
support_assistant/src/prompt_template.py
```

It contains the required:

1. Role
2. Context
3. Task
4. Format
5. Length

It also includes:

- An explicit negative constraint
- A few-shot example

Test it with:

```powershell
python support_assistant\src\prompt_template.py
```

## LangGraph Workflow

The workflow uses a `TypedDict` state and three nodes:

```text
classify_intent
retrieve_and_answer
direct_answer
```

Flow:

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

### Intent Classification

The deterministic keyword heuristic checks for:

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

Matching queries are routed to:

```text
policy_question
```

Other queries are routed to:

```text
general_question
```

### Policy Route

The policy route always retrieves the top-3 results from ChromaDB.

The deterministic mock answer uses:

```text
Based on the retrieved context: <top chunk snippet>
```

where the snippet is approximately the first 200 characters of the top retrieved chunk.

### General Route

The deterministic direct answer is:

```text
I can only answer questions about Zepto policies right now.
```

No retrieval is performed for general questions.

## MOCK_LLM

The default behavior is deterministic mock mode.

If `MOCK_LLM` is unset, mock mode is enabled.

Mock mode can explicitly be enabled with:

```text
MOCK_LLM=1
```

The optional real-LLM branch can be selected with:

```text
MOCK_LLM=0
```

The default support-assistant path does not require an external LLM, API key, or paid service.

## Pydantic Response

The response schema contains:

```text
answer       : string
sources      : list[string]
confidence   : float between 0 and 1
```

Mock confidence values are:

```text
Policy question : 0.9
General question: 0.5
```

Validation includes retry handling for invalid responses.

## FastAPI

Start the application with:

```powershell
uvicorn support_assistant.src.api:app --reload
```

Endpoint:

```text
POST /ask
```

Example request:

```json
{
  "query": "What is the delivery fee for orders below INR 149?"
}
```

### Verified Policy Response

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

### Verified General Response

Request:

```json
{
  "query": "What is the capital of India?"
}
```

Response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 0.5
}
```

## Docker

The Module 3 Docker image is built using:

```text
Dockerfile
```

Module-specific Docker dependencies are defined in:

```text
support_assistant/docker-requirements.txt
```

The Docker dependency setup uses CPU PyTorch packages to avoid the unnecessary CUDA dependency stack.

### Build

From the repository root:

```powershell
docker build -t zepto-support-assistant:latest .
```

### Run

```powershell
docker run --name zepto-support-assistant -p 8000:8000 zepto-support-assistant:latest
```

The Dockerized FastAPI application was successfully tested.

Verified:

```text
Policy question  → retrieval response  → PASS
General question → direct response      → PASS
```

Detailed Module 3 documentation:

```text
support_assistant/README.md
```

---

# Design Decisions

## Reproducibility

The project stores required datasets and generated analysis outputs locally where appropriate.

Generated runtime artifacts such as the ChromaDB database are excluded from Git and can be recreated.

## Module Separation

Each capstone requirement is isolated into its own module:

```text
data_pipeline/
analytics/
support_assistant/
```

This keeps the implementation organized and makes each module independently understandable.

## Local-First AI

Module 3 uses local embeddings and ChromaDB.

The default support-assistant path is deterministic and does not require an external LLM service.

## Database Design

Module 1 uses a normalized SQLite schema with separate category and book tables.

## Machine Learning Reproducibility

Module 2 uses train-only preprocessing and persists the complete fitted model pipeline using `joblib`.

## API and Containerization

Module 3 exposes a FastAPI endpoint and provides a Dockerfile for reproducible local execution.

---

# Testing and Verification Summary

## Module 1

Verified:

- 93 books
- 3 categories
- Required book fields
- Cleaned dataset
- SQLite database
- Five SQL queries
- SQL JOIN
- Pandas JOIN verification
- Reproducible pipeline
- Rerun-safe database rebuild

## Module 2

Verified:

- EDA
- Missing-value analysis
- Outlier analysis
- Correlation analysis
- Multivariate visualizations
- Logistic Regression
- Decision Tree
- Random Forest
- Class imbalance handling
- GridSearchCV
- OOB score
- ROC/AUC
- Fare regression
- Model persistence
- Reloaded prediction

## Module 3

Verified:

- Eight policy documents
- Local embeddings
- ChromaDB ingestion
- Semantic top-3 retrieval
- Structured prompt
- Negative constraint
- Few-shot example
- LangGraph StateGraph
- TypedDict state
- Three workflow nodes
- Conditional routing
- Deterministic mock answers
- Pydantic validation
- FastAPI `/ask`
- Policy API call
- General API call
- Docker build
- Docker runtime
- Docker API tests

---

# Git Workflow

Development was performed using the feature branch:

```text
feature/project-foundation
```

The feature branch contains the major implementation commits for the capstone and was merged into `main` using a non-fast-forward merge.

The final submission branch is:

```text
main
```

The Git history preserves the feature-development commits and the merge into the final `main` branch.

---
# Academic Integrity

This project is developed as an academic capstone.

The implementation, code structure, documentation, analysis, and validation are maintained as part of the project development process.

---

# Final Project Status

## Module 1 — Data Pipeline

**Status: Completed**

Implemented:

- Web scraping
- 93-book dataset
- 3 categories
- Data cleaning
- GBP → INR conversion
- SQLite normalized database
- Five SQL queries
- SQL output files
- Pandas SQL verification
- Independent pandas JOIN verification
- Reproducible end-to-end pipeline
- Rerun-safe database rebuild

## Module 2 — Analytics & Machine Learning

**Status: Completed**

Implemented:

- Titanic EDA
- Data quality analysis
- Visualization
- Correlation analysis
- Classification
- Class imbalance handling
- Hyperparameter tuning
- ROC/AUC evaluation
- Regression
- Residual analysis
- Model persistence
- Reloaded prediction

## Module 3 — RAG Support Assistant

**Status: Completed**

Implemented:

- Eight-document policy corpus
- Local embeddings
- ChromaDB
- Structured prompt
- LangGraph workflow
- Deterministic `MOCK_LLM`
- Pydantic validation
- FastAPI
- Docker
- API verification

---

# Final Submission

The final project is maintained as one public GitHub repository containing:

- Source code
- Data pipeline
- Analytics and machine learning work
- RAG support assistant
- Required corpus documents
- Documentation
- Configuration files
- Reproducible outputs
- Docker deployment files

Each module also contains its own detailed README where appropriate.
