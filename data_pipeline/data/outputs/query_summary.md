# SQL Query Results

This file documents the SQL queries executed against the SQLite database and references their saved outputs.

## query_01_select_where

### SQL

```sql
SELECT title, price_gbp, rating
        FROM books
        WHERE rating >= 4
        ORDER BY rating DESC, price_gbp DESC
```

### Output

- Rows returned: 33
- CSV file: `query_01_select_where.csv`

## query_02_order_limit

### SQL

```sql
SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10
```

### Output

- Rows returned: 10
- CSV file: `query_02_order_limit.csv`

## query_03_distinct_categories

### SQL

```sql
SELECT DISTINCT category_name
        FROM categories
        ORDER BY category_name
```

### Output

- Rows returned: 3
- CSV file: `query_03_distinct_categories.csv`

## query_04_between

### SQL

```sql
SELECT title, price_gbp, rating
        FROM books
        WHERE price_gbp BETWEEN 20 AND 40
        ORDER BY price_gbp
```

### Output

- Rows returned: 44
- CSV file: `query_04_between.csv`

## query_05_category_join

### SQL

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

### Output

- Rows returned: 93
- CSV file: `query_05_category_join.csv`

