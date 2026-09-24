# Zepto Data & AI Platform

## Masai School — Certificate Program in Artificial Intelligence and Machine Learning

This repository contains the capstone project for the **Masai School Certificate Program in Artificial Intelligence and Machine Learning**.

The project implements one connected Zepto-style Data & AI platform consisting of three internally linked modules:

1. **Data Pipeline** — web scraping, data cleaning, currency conversion, SQLite storage, SQL querying, and pandas analysis.
2. **Analytics Pipeline** — Titanic dataset profiling, exploratory data analysis, predictive modeling, model evaluation, hyperparameter tuning, and regression.
3. **Support Assistant** — document ingestion, local embeddings, ChromaDB retrieval, LangGraph orchestration, structured responses, FastAPI, and Docker.

All three modules are contained in this **single public GitHub repository**, as required by the capstone specification.

---

## Project Structure

```text
Capstone_Project_Zepto_Masai/
│
├── data_pipeline/
│
├── analytics/
│
├── support_assistant/
│
├── README.md
└── .gitignore
```

---

# Module 1 — Data Pipeline

Location:

```text
/data_pipeline
```

The data pipeline implements an end-to-end raw-to-relational workflow:

```text
books.toscrape.com
        ↓
Web Scraping
        ↓
Data Cleaning
        ↓
Currency Conversion
        ↓
Pandas DataFrame
        ↓
Normalized SQLite Database
        ↓
SQL Queries
        ↓
Pandas Analysis
```

The module will use:

* `requests`
* `BeautifulSoup`
* `pandas`
* Python `sqlite3`

The required project-defined currency conversion rate is:

```text
1 GBP = 105.50 INR
```

This is a fixed assignment-defined conversion rate and does not require a live currency API.

The completed module will contain the scraping and cleaning implementation, SQLite database/schema, SQL queries and outputs, pandas query results, and documentation of design decisions.

---

# Module 2 — Analytics Pipeline

Location:

```text
/analytics
```

The analytics pipeline uses the Titanic dataset to demonstrate a complete analyst-to-data-scientist workflow.

The pipeline covers:

* Dataset profiling
* Missing-value analysis
* Missing-value handling
* Univariate analysis
* Bivariate analysis
* Multivariate analysis
* Correlation analysis
* Outlier detection
* Standardization checks
* Stratified train/test splitting
* Train-only preprocessing
* Logistic Regression
* Decision Tree
* Random Forest
* Classification evaluation
* ROC/AUC analysis
* Class imbalance handling
* SMOTE
* Random Forest hyperparameter tuning
* Out-of-bag evaluation
* Multivariate linear regression
* Regression evaluation
* Residual analysis
* Complete model pipeline persistence using `joblib`

The raw Titanic dataset will be loaded once and saved as:

```text
/analytics/titanic.csv
```

This committed CSV provides the required offline fallback for subsequent modeling work.

---

# Module 3 — Support Assistant

Location:

```text
/support_assistant
```

The support assistant implements a grounded question-answering service over eight Zepto policy documents.

The overall architecture is:

```text
Policy Documents
       ↓
Document Chunking
       ↓
Local Embeddings
       ↓
ChromaDB
       ↓
User Query
       ↓
LangGraph Intent Classification
       ↓
 ┌───────────────┐
 │               │
Policy        General
Question      Question
 │               │
 ↓               ↓
Retrieve       Direct
Context        Answer
 │               │
 └───────┬───────┘
         ↓
Structured Pydantic Response
         ↓
FastAPI
```

The module will use:

* Sentence Transformers
* `all-MiniLM-L6-v2`
* ChromaDB
* LangGraph
* Pydantic
* FastAPI
* Uvicorn
* Docker

The graded baseline uses deterministic offline mock behavior controlled by:

```text
MOCK_LLM
```

The required implementation does not depend on a paid LLM service or an LLM API key.

---

# Technology Stack

## Programming

* Python 3.12

## Data Engineering

* requests
* BeautifulSoup
* pandas
* SQLite
* sqlite3

## Data Science / Machine Learning

* NumPy
* pandas
* Seaborn
* Matplotlib
* scikit-learn
* imbalanced-learn
* joblib

## Generative AI / RAG

* Sentence Transformers
* ChromaDB
* LangGraph
* Pydantic

## API / Deployment

* FastAPI
* Uvicorn
* Docker

---

# Python Environment

The project is developed using a dedicated Python virtual environment.

Recommended Python version:

```text
Python 3.12
```

Local virtual environment:

```text
.venv/
```

The virtual environment is intentionally excluded from Git using `.gitignore`.

---

# Installation

A consolidated root `requirements.txt` will be used for the project.

The complete dependency list and installation commands will be documented once the required project dependencies have been finalized.

---

# Running the Project

Detailed end-to-end execution instructions will be added as each module is implemented and tested.

## Data Pipeline

See:

```text
data_pipeline/README.md
```

## Analytics Pipeline

See:

```text
analytics/README.md
```

## Support Assistant

See:

```text
support_assistant/README.md
```

---

# Design Decisions

Each module will document its implementation and design decisions in its respective module README and, where appropriate, within notebook Markdown cells.

Important design decisions will include:

* Data cleaning and parsing strategies
* Missing-value handling
* Database normalization
* SQL query design
* Train/test separation
* Prevention of preprocessing leakage
* Class imbalance handling
* Model selection and evaluation
* RAG architecture
* Mock LLM behavior
* Structured output validation
* API and Docker configuration

---

# Git Workflow

This repository follows a feature-branch workflow.

The project history will include:

```text
main
  │
  └── feature branch
        │
        ├── commit 1
        │
        ├── commit 2
        │
        └── merge back into main
```

This satisfies the capstone requirement for demonstrating a feature branch with at least two commits followed by a merge into `main`.

---

# Academic Integrity

This project is implemented as an original capstone submission.

Official documentation for Python libraries, frameworks, databases, machine-learning tools, and related technologies may be consulted for technical reference.

The implementation, analysis, interpretations, design decisions, and written explanations are authored specifically for this project.

---

# Project Status

| Component               | Status         |
| ----------------------- | -------------- |
| Repository Setup        | ✅ Complete     |
| Python 3.12 Environment | ✅ Complete     |
| Git Configuration       | ✅ Complete     |
| Project Structure       | ✅ Complete     |
| Data Pipeline           | 🚧 In Progress |
| Analytics Pipeline      | ⏳ Pending      |
| Support Assistant       | ⏳ Pending      |
| Integration Testing     | ⏳ Pending      |
| Final Rubric Audit      | ⏳ Pending      |
| GitHub Submission       | ⏳ Pending      |

---

# Final Submission

The final submission will consist of **one public GitHub repository** containing:

```text
/data_pipeline
/analytics
/support_assistant
README.md
```

All three modules will be implemented, tested, documented, and verified against the Masai capstone acceptance criteria before submission.
