# Module 1 — Data Pipeline

## 1. Objective

Build a reproducible Python data pipeline that:

* Scrapes book data from `books.toscrape.com`
* Cleans and transforms the scraped data
* Converts GBP prices to INR
* Stores the data in a normalized SQLite database
* Executes SQL queries for analysis
* Reproduces selected SQL results using pandas
* Verifies that SQL and pandas results are equivalent

---

## 2. Module Structure

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
    ├── raw/
    │   └── .gitkeep
    │
    ├── processed/
    │   └── .gitkeep
    │
    └── outputs/
        └── .gitkeep
```

### Source Code

The `src/` directory contains the Python implementation:

| File          | Responsibility                                        |
| ------------- | ----------------------------------------------------- |
| `scraper.py`  | Scrape book information from the website              |
| `cleaner.py`  | Clean, transform, validate, and type the scraped data |
| `database.py` | Create and populate the SQLite database               |
| `queries.py`  | Define and execute the required SQL queries           |
| `pipeline.py` | Orchestrate the complete end-to-end pipeline          |

### Data

The `data/` directory separates generated data and analysis artifacts from source code.

| Directory    | Purpose                                                          |
| ------------ | ---------------------------------------------------------------- |
| `raw/`       | Raw scraped data before cleaning                                 |
| `processed/` | Cleaned and transformed datasets                                 |
| `outputs/`   | SQL outputs, verification results, and other generated artifacts |

The SQLite database will also be stored within the module's data area as part of the reproducible pipeline.

---

## 3. Data Source

The project uses the public practice website:

**https://books.toscrape.com/**

The website does not require authentication or an API key.

The scraper will collect books across multiple categories/pages and must produce at least:

* **60 books**
* **3 categories**

---

## 4. Scraped Fields

The scraper will collect the following fields:

| Field          | Description                |
| -------------- | -------------------------- |
| `title`        | Book title                 |
| `price_gbp`    | Book price in GBP          |
| `star_rating`  | Original star-rating text  |
| `availability` | Original availability text |
| `category`     | Book category              |

The raw data will initially preserve the source information before cleaning and transformation.

---

## 5. Data Cleaning

The raw scraped data will be transformed into analysis-ready fields.

### Price

The currency symbol will be removed and the value converted to a floating-point number.

Example:

```text
£51.77 → 51.77
```

### Rating

The textual star rating will be converted to an integer:

```text
One   → 1
Two   → 2
Three → 3
Four  → 4
Five  → 5
```

### Availability

The availability text will be converted into an `in_stock` boolean/integer field.

Example:

```text
"In stock (22 available)" → 1
```

### Missing or Invalid Values

Any parsing failures will be identified during execution.

The final missing-value handling strategy will be documented after inspecting the actual scraped dataset.

For numeric fields, the pipeline will either use median imputation or drop affected rows where appropriate. The selected approach and its justification will be documented based on the actual data quality observed during execution.

---

## 6. Currency Conversion

The project uses the required fixed conversion rate:

```text
1 GBP = 105.50 INR
```

The INR price is calculated as:

```text
price_inr = price_gbp × 105.50
```

This is a fixed artificial project rate and does not use a live currency API.

---

## 7. Database Design

The cleaned data will be stored in a normalized SQLite database containing at least two related tables.

### `categories`

```sql
category_id INTEGER PRIMARY KEY
category_name TEXT UNIQUE
```

### `books`

```sql
book_id INTEGER PRIMARY KEY
title TEXT
price_gbp REAL
price_inr REAL
rating INTEGER
in_stock INTEGER
category_id INTEGER REFERENCES categories(category_id)
```

The `category_id` column in `books` establishes the foreign-key relationship with `categories`.

The database will be generated programmatically so that the complete pipeline can be reproduced without manually entering data.

---

## 8. SQL Analysis

The project will execute at least five SQL queries.

The queries will collectively demonstrate:

* `SELECT`
* `WHERE`
* `ORDER BY`
* `LIMIT`
* `DISTINCT`
* `IN` or `BETWEEN`
* `JOIN`

Each query string and its resulting output will be preserved as project artifacts.

The SQL queries will be implemented in:

```text
src/queries.py
```

and generated outputs will be stored under:

```text
data/outputs/
```

---

## 9. Pandas Analysis and Verification

At least two SQL query results will be loaded into pandas using:

```python
pd.read_sql(...)
```

The SQL join will also be independently reproduced using pandas:

```python
pd.merge(...)
```

The SQL and pandas results will then be compared to verify that both approaches produce equivalent results.

The verification output will be preserved as a project artifact.

---

## 10. End-to-End Pipeline

The intended execution flow is:

```text
books.toscrape.com
        │
        ▼
   scraper.py
        │
        ▼
   Raw dataset
        │
        ▼
   cleaner.py
        │
        ▼
 Cleaned dataset
        │
        ├──────────────► data/processed/
        │
        ▼
   database.py
        │
        ▼
   SQLite database
        │
        ▼
   queries.py
        │
        ├──────────────► SQL query outputs
        │
        ▼
    pandas
        │
        ├── pd.read_sql()
        │
        └── pd.merge()
                │
                ▼
        SQL vs pandas verification
```

The `pipeline.py` module will orchestrate the complete workflow.

---

## 11. Reproducibility

The complete pipeline will run from Python source code without manually copying or pasting scraped data.

The pipeline will:

1. Retrieve the source data.
2. Clean and transform the data.
3. Calculate INR prices.
4. Create the normalized SQLite database.
5. Populate the database.
6. Execute the required SQL queries.
7. Save query outputs.
8. Load selected results into pandas.
9. Reproduce the SQL join using `pd.merge()`.
10. Verify equivalent results.

The repository will contain sufficient instructions for another user to recreate the complete pipeline.

---

## 12. Validation Requirements

Before Module 1 is considered complete, the following checks must pass:

### Scraping

* [ ] At least 60 books collected
* [ ] At least 3 categories collected
* [ ] All required source fields captured
* [ ] Scraper runs without manual data entry

### Cleaning

* [ ] Prices converted to numeric `price_gbp`
* [ ] Ratings converted to integers from 1–5
* [ ] Availability converted to `in_stock`
* [ ] Missing/invalid values handled
* [ ] Cleaning decisions documented

### Currency

* [ ] Fixed rate of `1 GBP = 105.50 INR`
* [ ] `price_inr` correctly calculated

### Database

* [ ] SQLite database created
* [ ] `categories` table created
* [ ] `books` table created
* [ ] Primary keys defined
* [ ] Foreign key relationship defined
* [ ] Data successfully inserted

### SQL

* [ ] At least 5 SQL queries
* [ ] `SELECT`
* [ ] `WHERE`
* [ ] `ORDER BY`
* [ ] `LIMIT`
* [ ] `DISTINCT`
* [ ] `IN` or `BETWEEN`
* [ ] `JOIN`
* [ ] Query outputs preserved

### Pandas

* [ ] At least 2 SQL results loaded with `pd.read_sql`
* [ ] SQL JOIN reproduced using `pd.merge`
* [ ] SQL and pandas results verified as equivalent

---

## 13. Expected Output

After successful execution, the module will provide:

* Raw scraped book data
* Cleaned and transformed book data
* INR price calculations
* Normalized SQLite database
* `categories` and `books` tables
* SQL queries and outputs
* Pandas query results
* SQL JOIN vs pandas `merge()` verification
* Documented data-cleaning decisions
* Reproducible end-to-end execution

---

## 14. Final Results

This section will be completed after the pipeline has been executed.

It will document the actual:

* Number of books scraped
* Number of categories
* Data quality and missing-value statistics
* Cleaning decisions
* Database validation results
* SQL query results
* Pandas verification results
* Final acceptance checks

---

## 15. Module Status

**Current status:** Implementation in progress.

The module will be marked complete only after all validation requirements listed above have been successfully verified.
