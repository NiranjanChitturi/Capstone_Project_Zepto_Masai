# Zepto Data & AI Platform

Masai School AI/ML Capstone Project

This repository contains an end-to-end data engineering, analytics, machine learning, and AI assistant project developed as part of the Masai School capstone.

The project is organized into three major modules:

1. **Data Pipeline**
2. **Analytics & Machine Learning**
3. **RAG Support Assistant**

The implementation is designed to be reproducible, documented, and executable from a clean Python environment.

---

## Project Objectives

The project demonstrates the following capabilities:

* Web data collection and scraping
* Data cleaning and validation
* Currency conversion
* Relational database design
* SQL analysis
* Pandas-based data analysis
* Exploratory data analysis
* Machine learning classification and regression
* Model evaluation and comparison
* Retrieval-Augmented Generation (RAG)
* Vector database usage
* LangGraph workflow orchestration
* FastAPI deployment
* Docker-based local execution

---

## Repository Structure

```text
Capstone_Project_Zepto_Masai/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data_pipeline/
│   ├── README.md
│   │
│   ├── src/
│   │   ├── scraper.py
│   │   ├── cleaner.py
│   │   ├── database.py
│   │   ├── queries.py
│   │   └── pipeline.py
│   │
│   └── data/
│       ├── database/
│       │   └── books.db
│       │
│       ├── raw/
│       │   └── books_raw.csv
│       │
│       ├── processed/
│       │   └── books_cleaned.csv
│       │
│       └── outputs/
│           ├── query_01_select_where.csv
│           ├── query_02_order_limit.csv
│           ├── query_03_distinct_categories.csv
│           ├── query_04_between.csv
│           ├── query_05_category_join.csv
│           ├── query_summary.md
│           └── join_verification.md
│
├── analytics/
│   └── ...
│
└── support_assistant/
    └── ...
```

---

# Module 1 — Data Pipeline

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

## Current Module 1 Result

The pipeline currently processes:

* **93 books**
* **3 categories**
* **60 books minimum required**
* **3 categories minimum required**

Selected categories:

* Mystery — 32 books
* Historical Fiction — 26 books
* Romance — 35 books

Total:

```text
32 + 26 + 35 = 93 books
```

The requirement is **at least 60 books**, therefore 93 books satisfies the requirement.

---

## Module 1 Data Source

The scraper uses:

```text
https://books.toscrape.com/
```

The scraper automatically collects the selected categories and does not require manual copy/paste of book information.

Required fields collected from the website:

* `title`
* `price`
* `star_rating`
* `availability`
* `category`

---

## Data Cleaning

The raw website values are transformed into analysis-ready fields:

| Raw Field      | Cleaned Field |
| -------------- | ------------- |
| `price`        | `price_gbp`   |
| `star_rating`  | `rating`      |
| `availability` | `in_stock`    |
| `category`     | `category`    |

The cleaned dataset additionally contains:

```text
price_inr
```

### Currency Conversion

A fixed artificial conversion rate is used:

```text
1 GBP = 105.50 INR
```

No external currency API is used.

The conversion is:

```text
price_inr = price_gbp × 105.50
```

The fixed rate is intentionally documented so that the pipeline remains reproducible.

---

# SQLite Database

The cleaned dataset is stored in:

```text
data_pipeline/data/database/books.db
```

The database uses two normalized tables.

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

The relationship is:

```text
categories
    │
    │ category_id
    ↓
books.category_id
```

SQLite foreign-key enforcement is explicitly enabled.

The database is rebuilt transactionally during the pipeline so that repeated executions do not create duplicate records.

---

# SQL Analysis

Five SQL queries are implemented:

### Query 1 — SELECT / WHERE

Filters books with a rating of at least 4 and orders them by rating and price.

### Query 2 — ORDER BY / LIMIT

Returns the 10 most expensive books.

### Query 3 — DISTINCT

Returns the distinct book categories.

### Query 4 — BETWEEN

Returns books whose GBP price is between £20 and £40.

### Query 5 — JOIN

Joins the normalized `books` and `categories` tables.

All query outputs are saved as CSV files.

The SQL statements, row counts, and output filenames are documented in:

```text
data_pipeline/data/outputs/query_summary.md
```

---

# SQL and Pandas Verification

The SQL JOIN is independently reproduced using:

```python
pandas.merge()
```

The verification performs:

```text
SQL JOIN
   ↓
93 rows

Pandas merge()
   ↓
93 rows

Comparison
   ↓
True
```

The verification report is saved as:

```text
data_pipeline/data/outputs/join_verification.md
```

This demonstrates that the relational SQL JOIN can be independently reproduced using in-memory pandas DataFrames.

---

# Reproducible Pipeline

The complete Module 1 workflow can be executed using:

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

The pipeline is designed to be safely rerunnable.

Existing generated files are regenerated, while the SQLite database is rebuilt transactionally from the current cleaned dataset.

---

# Installation

Create and activate a Python virtual environment.

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# Python Environment

The project was developed and tested using:

```text
Python 3.12
```

The required packages are defined in:

```text
requirements.txt
```

---

# Module Documentation

Detailed documentation for the data pipeline is available in:

```text
data_pipeline/README.md
```

The Analytics and RAG modules will contain their own documentation as their implementations are completed.

---

# Git Workflow

Development is performed using feature branches.

Current development branch:

```text
feature/project-foundation
```

Major implementation stages are committed separately so that the project history clearly shows the progression of the capstone.

---

# Academic Integrity

This project is developed as an academic capstone.

The implementation, code structure, documentation, analysis, and validation are maintained as part of the project development process.

---

# Project Status

## Module 1 — Data Pipeline

**Status: Completed**

Implemented:

* Web scraping
* 93-book dataset
* 3 categories
* Data cleaning
* GBP → INR conversion
* SQLite normalized database
* Five SQL queries
* SQL output files
* Pandas SQL verification
* Independent pandas JOIN verification
* Reproducible end-to-end pipeline
* Rerun-safe database rebuild

## Module 2 — Analytics & Machine Learning

**Status: In Progress**

## Module 3 — RAG Support Assistant

**Status: Planned / In Progress**

---

# Final Submission

The final project will be maintained as one public GitHub repository containing:

* Source code
* Data pipeline
* Analytics and ML work
* RAG assistant
* Documentation
* Configuration files
* Reproducible outputs
* Deployment files
