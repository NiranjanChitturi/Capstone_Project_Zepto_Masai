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

## 2. Data Source

The project uses the public practice website:

**https://books.toscrape.com/**

The website does not require authentication or an API key.

The scraper will collect books across multiple categories/pages and must produce at least:

* **60 books**
* **3 categories**

---

## 3. Scraped Fields

The scraper will collect the following fields:

| Field          | Description                |
| -------------- | -------------------------- |
| `title`        | Book title                 |
| `price_gbp`    | Book price in GBP          |
| `star_rating`  | Original star-rating text  |
| `availability` | Original availability text |
| `category`     | Book category              |

---

## 4. Data Cleaning

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

The final missing-value handling strategy will be documented after inspecting the actual scraped dataset. Numeric fields will use median imputation or affected rows will be dropped where appropriate, with the selected approach and justification documented in the final results.

---

## 5. Currency Conversion

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

## 6. Database Design

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

---

## 7. SQL Analysis

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

---

## 8. Pandas Analysis and Verification

At least two SQL query results will be loaded into pandas using:

```python
pd.read_sql(...)
```

The SQL join will also be independently reproduced using pandas:

```python
pd.merge(...)
```

The SQL and pandas results will then be compared to verify that both approaches produce equivalent results.

---

## 9. Reproducibility

The complete pipeline will run from Python source code without manually copying or pasting scraped data.

The database will either be:

1. generated automatically by the pipeline, or
2. included as a reproducible SQLite project artifact.

The repository will contain sufficient instructions for another user to recreate the complete pipeline.

---

## 10. Expected Output

After successful execution, the module will provide:

* Scraped book dataset
* Cleaned dataset
* INR price calculations
* SQLite database
* Normalized `categories` and `books` tables
* SQL queries and outputs
* Pandas query results
* SQL JOIN vs pandas `merge()` verification
* Documented data-cleaning decisions

---

## 11. Module Status

**Status:** In development

The final README will be updated with the actual measured results after the pipeline has been executed, including:

* total number of books scraped
* number of categories
* missing-value statistics
* cleaning decisions
* SQL query results
* pandas verification results
* final validation status
