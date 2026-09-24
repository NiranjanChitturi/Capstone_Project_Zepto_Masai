# Module 1 — Data Pipeline

This module implements the complete data engineering pipeline for the Masai School AI/ML capstone.

The workflow collects book data from the selected categories of Books to Scrape, cleans and validates the data, converts GBP prices to INR using a fixed conversion rate, stores the normalized data in SQLite, executes SQL analysis queries, and independently verifies the SQL JOIN using pandas.

---

# Objective

The Data Pipeline module must demonstrate:

* Automated web scraping
* At least 60 books
* At least 3 categories
* Required field extraction
* Data cleaning
* Correct data types
* GBP → INR conversion
* Normalized relational database design
* SQL analysis
* Pandas SQL-result verification
* Independent pandas JOIN verification
* Reproducible execution
* Safe reruns

---

# Data Source

The scraper uses:

```text
https://books.toscrape.com/
```

No manual copy/paste of book information is required.

The current implementation scrapes these categories:

```text
Mystery
Historical Fiction
Romance
```

---

# Dataset

The current pipeline produces:

| Category           |  Books |
| ------------------ | -----: |
| Mystery            |     32 |
| Historical Fiction |     26 |
| Romance            |     35 |
| **Total**          | **93** |

The assignment requires:

```text
Minimum books: 60
Minimum categories: 3
```

Current validation:

```text
Books: 93
Required minimum books: 60 → PASS

Categories: 3
Required minimum categories: 3 → PASS
```

The pipeline intentionally retains all 93 books rather than reducing the dataset to exactly 60.

---

# Module Structure

```text
data_pipeline/
│
├── README.md
│
├── src/
│   ├── scraper.py
│   ├── cleaner.py
│   ├── database.py
│   ├── queries.py
│   └── pipeline.py
│
└── data/
    ├── database/
    │   └── books.db
    │
    ├── raw/
    │   └── books_raw.csv
    │
    ├── processed/
    │   └── books_cleaned.csv
    │
    └── outputs/
        ├── query_01_select_where.csv
        ├── query_02_order_limit.csv
        ├── query_03_distinct_categories.csv
        ├── query_04_between.csv
        ├── query_05_category_join.csv
        ├── query_summary.md
        └── join_verification.md
```

---

# Source Fields

The scraper collects:

```text
title
price
star_rating
availability
category
```

Example raw structure:

```text
title
price
star_rating
availability
category
```

The raw dataset is saved to:

```text
data/raw/books_raw.csv
```

---

# Data Cleaning

The raw fields are converted into analysis-ready fields.

| Raw Field      | Cleaned Field | Type    |
| -------------- | ------------- | ------- |
| `price`        | `price_gbp`   | float   |
| `star_rating`  | `rating`      | integer |
| `availability` | `in_stock`    | boolean |
| `category`     | `category`    | string  |

An additional calculated field is created:

```text
price_inr
```

The final processed CSV contains:

```text
title
price_gbp
price_inr
rating
in_stock
category
```

The processed dataset is saved to:

```text
data/processed/books_cleaned.csv
```

---

# Price Cleaning

Website price text is converted into a numeric GBP value.

For example:

```text
£55.53
```

becomes:

```text
55.53
```

The implementation also handles encoding artifacts around the currency symbol.

Invalid price values cause validation to fail rather than silently producing incorrect numeric data.

---

# Rating Cleaning

The website's star-rating words are converted to integers.

```text
One   → 1
Two   → 2
Three → 3
Four  → 4
Five  → 5
```

The cleaned rating must be between:

```text
1 and 5
```

---

# Availability Cleaning

Availability is converted to a boolean:

```text
In stock     → True
Out of stock → False
```

The `out of stock` condition is checked before `in stock` because the phrase `out of stock` contains the words `in stock`.

---

# Currency Conversion

A fixed artificial exchange rate is used:

```text
1 GBP = 105.50 INR
```

The conversion is:

```text
price_inr = price_gbp × 105.50
```

No external currency API is used.

The fixed rate is intentionally used to keep the capstone deterministic and reproducible.

---

# Validation

The pipeline validates both raw and cleaned data.

Validation includes:

* Required fields exist
* Dataset is not empty
* Titles are not missing
* Categories are not missing
* Numeric price fields are valid
* Ratings are between 1 and 5
* Availability values are boolean
* GBP → INR conversion is consistent
* Minimum book count is satisfied
* Minimum category count is satisfied

---

# SQLite Database

The normalized SQLite database is:

```text
data/database/books.db
```

The database contains two tables.

## Categories

```sql
categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
)
```

## Books

```sql
books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL NOT NULL,
    price_inr REAL NOT NULL,
    rating INTEGER NOT NULL,
    in_stock INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
)
```

Relationship:

```text
categories.category_id
        │
        │
        ▼
books.category_id
```

SQLite foreign-key enforcement is enabled explicitly.

---

# Database Rerun Behavior

The database is rebuilt deterministically on every pipeline execution.

The process is:

```text
Ensure tables exist
       ↓
Delete books
       ↓
Delete categories
       ↓
Insert current categories
       ↓
Insert current books
       ↓
Commit
```

Books are deleted before categories because `books.category_id` references `categories.category_id`.

The rebuild is handled inside a transaction.

If an error occurs:

```text
ROLLBACK
```

is performed so that the database is not intentionally left in a partially rebuilt state.

Repeated execution does not create duplicate book records.

---

# SQL Analysis

Five SQL queries are implemented in:

```text
src/queries.py
```

## Query 1 — SELECT / WHERE

Demonstrates filtering and ordering.

```sql
SELECT title, price_gbp, rating
FROM books
WHERE rating >= 4
ORDER BY rating DESC, price_gbp DESC
```

Result:

```text
33 rows
```

Output:

```text
data/outputs/query_01_select_where.csv
```

---

## Query 2 — ORDER BY / LIMIT

Returns the 10 most expensive books.

```sql
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 10
```

Result:

```text
10 rows
```

Output:

```text
data/outputs/query_02_order_limit.csv
```

---

## Query 3 — DISTINCT

Returns unique categories.

```sql
SELECT DISTINCT category_name
FROM categories
ORDER BY category_name
```

Result:

```text
3 rows
```

Output:

```text
data/outputs/query_03_distinct_categories.csv
```

---

## Query 4 — BETWEEN

Returns books priced between £20 and £40.

```sql
SELECT title, price_gbp, rating
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp
```

Result:

```text
44 rows
```

Output:

```text
data/outputs/query_04_between.csv
```

---

## Query 5 — INNER JOIN

Demonstrates the normalized relationship between `books` and `categories`.

```sql
SELECT
    b.title,
    b.price_gbp,
    b.rating,
    c.category_name
FROM books AS b
INNER JOIN categories AS c
    ON b.category_id = c.category_id
ORDER BY c.category_name, b.title
```

Result:

```text
93 rows
```

Output:

```text
data/outputs/query_05_category_join.csv
```

---

# SQL Query Documentation

The SQL statements, row counts, and output filenames are documented in:

```text
data/outputs/query_summary.md
```

The CSV files contain the query result headers and data.

SQL statements are kept in the Markdown documentation rather than inserted into the CSV result files.

---

# Pandas SQL Verification

SQL results are read into pandas using:

```python
pd.read_sql_query()
```

This satisfies the requirement to read SQL query results into pandas.

The SQL JOIN is also independently reproduced without performing a SQL JOIN.

---

# Independent pandas JOIN

The implementation reads the two normalized tables separately:

```text
books
categories
```

They are then joined in memory using:

```python
pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner",
)
```

The resulting columns are aligned with the SQL JOIN result:

```text
title
price_gbp
rating
category_name
```

The ordering is also aligned before comparison.

---

# JOIN Verification Result

The current verification produces:

```text
SQL JOIN rows:       93
pandas.merge rows:   93
Results match:       True
```

The verification report is:

```text
data/outputs/join_verification.md
```

This provides an independent confirmation that the normalized database relationship produces the same result through SQL and pandas.

---

# End-to-End Pipeline

The complete pipeline is implemented in:

```text
src/pipeline.py
```

Run the complete Module 1 pipeline from the repository root:

```powershell
python -m data_pipeline.src.pipeline
```

The pipeline performs:

```text
1. Scrape
       ↓
2. Validate raw data
       ↓
3. Save raw CSV
       ↓
4. Clean data
       ↓
5. Validate cleaned data
       ↓
6. Save processed CSV
       ↓
7. Rebuild SQLite database
       ↓
8. Run SQL analysis
       ↓
9. Verify SQL JOIN with pandas
```

---

# Reproducibility

The pipeline is designed so that generated artifacts can be regenerated without manually copying data between steps.

A successful run currently reports:

```text
Scraped books: 93
Cleaned books: 93

Books: 93
Categories: 3

Required minimum books: 60 -> PASS
Required minimum categories: 3 -> PASS

SQL analysis completed successfully.
Module 1 pipeline completed successfully.
```

---

# Rerun Safety

The pipeline can be executed repeatedly.

Generated CSV and Markdown outputs are regenerated.

The SQLite database is rebuilt from the current cleaned DataFrame rather than appending the same records repeatedly.

A database rerun has been tested with:

```text
Books: 93
Categories: 3
Duplicates: 0
```

---

# Installation

From the repository root:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
pip install -r requirements.txt
```

---

# Running Module 1

From the repository root:

```powershell
python -m data_pipeline.src.pipeline
```

The individual components can also be imported and executed independently when debugging or testing specific stages.

---

# Module 1 Outputs

After a successful pipeline execution, the following artifacts are available:

```text
data_pipeline/data/raw/books_raw.csv
data_pipeline/data/processed/books_cleaned.csv
data_pipeline/data/database/books.db

data_pipeline/data/outputs/
├── query_01_select_where.csv
├── query_02_order_limit.csv
├── query_03_distinct_categories.csv
├── query_04_between.csv
├── query_05_category_join.csv
├── query_summary.md
└── join_verification.md
```

---

# Module 1 Acceptance Checklist

| Requirement                | Status   |
| -------------------------- | -------- |
| Automated scraper          | ✅        |
| At least 60 books          | ✅ 93     |
| At least 3 categories      | ✅ 3      |
| Required source fields     | ✅        |
| Cleaned price              | ✅        |
| Numeric rating 1–5         | ✅        |
| Boolean availability       | ✅        |
| Fixed GBP → INR conversion | ✅ 105.50 |
| Normalized SQLite database | ✅        |
| Categories table           | ✅        |
| Books table                | ✅        |
| Foreign-key relationship   | ✅        |
| SELECT / WHERE             | ✅        |
| ORDER BY / LIMIT           | ✅        |
| DISTINCT                   | ✅        |
| BETWEEN                    | ✅        |
| JOIN                       | ✅        |
| Query outputs saved        | ✅        |
| SQL documentation saved    | ✅        |
| `pd.read_sql_query()`      | ✅        |
| Independent `pd.merge()`   | ✅        |
| SQL/pandas JOIN match      | ✅        |
| Reproducible pipeline      | ✅        |
| Rerun-safe database        | ✅        |
| Documentation              | ✅        |

---

# Module 1 Status

**Completed**

The module has been tested end-to-end with:

```text
93 books
3 categories
5 SQL queries
93-row SQL JOIN
93-row pandas JOIN
JOIN match = True
```

The implementation is ready for the next capstone module.
