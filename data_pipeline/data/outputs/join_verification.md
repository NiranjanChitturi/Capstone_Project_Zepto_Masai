# SQL JOIN vs pandas.merge() Verification

The SQL JOIN result was independently reproduced using `pandas.merge()` on the `books` and `categories` DataFrames.

## SQL JOIN

- Source query: `query_05_category_join`
- Rows returned: 93

## pandas.merge()

- Join method: `pd.merge(..., how="inner")`
- Rows returned: 93

## Verification Result

- SQL JOIN and pandas JOIN match: **True**
