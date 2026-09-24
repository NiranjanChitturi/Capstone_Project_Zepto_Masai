"""
Module 1 - Data Pipeline
------------------------
SQL analysis and pandas verification utilities.

This module is responsible for:
1. Defining the required SQL analysis queries.
2. Executing SQL queries against the SQLite database.
3. Reading SQL results into pandas DataFrames.
4. Saving query results as CSV files.
5. Documenting SQL queries and their outputs.
6. Reproducing the SQL JOIN independently using pandas.merge().
7. Verifying that the SQL JOIN and pandas JOIN produce equivalent results.
"""

import sqlite3
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "database"
    / "books.db"
)

OUTPUT_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "outputs"
)


# ---------------------------------------------------------------------------
# Required SQL queries
# ---------------------------------------------------------------------------

QUERIES = {
    "query_01_select_where": """
        SELECT title, price_gbp, rating
        FROM books
        WHERE rating >= 4
        ORDER BY rating DESC, price_gbp DESC
    """,

    "query_02_order_limit": """
        SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10
    """,

    "query_03_distinct_categories": """
        SELECT DISTINCT category_name
        FROM categories
        ORDER BY category_name
    """,

    "query_04_between": """
        SELECT title, price_gbp, rating
        FROM books
        WHERE price_gbp BETWEEN 20 AND 40
        ORDER BY price_gbp
    """,

    "query_05_category_join": """
        SELECT
            b.title,
            b.price_gbp,
            b.rating,
            c.category_name
        FROM books AS b
        INNER JOIN categories AS c
            ON b.category_id = c.category_id
        ORDER BY c.category_name, b.title
    """,
}


# ---------------------------------------------------------------------------
# SQL execution
# ---------------------------------------------------------------------------

def execute_query(
    connection: sqlite3.Connection,
    query: str,
) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a pandas DataFrame.

    pandas.read_sql_query() is intentionally used here because the
    assignment requires SQL query results to be read into pandas.
    """
    return pd.read_sql_query(query, connection)


# ---------------------------------------------------------------------------
# Output handling
# ---------------------------------------------------------------------------

def prepare_output_directory() -> None:
    """Create the SQL output directory if it does not already exist."""
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)


def save_query_result(
    dataframe: pd.DataFrame,
    query_name: str,
) -> Path:
    """
    Save a SQL query result as a CSV file.

    Existing files are intentionally overwritten so that every pipeline
    execution produces results from the current database state.

    pandas manages opening and closing the output file internally.
    """
    prepare_output_directory()

    output_path = OUTPUT_DIRECTORY / f"{query_name}.csv"

    dataframe.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
        mode="w",
    )

    return output_path


# ---------------------------------------------------------------------------
# Query documentation
# ---------------------------------------------------------------------------

def reset_query_documentation() -> Path:
    """
    Create or overwrite the SQL query documentation file.

    Each pipeline execution starts with a fresh documentation file so
    previous query results are not duplicated.
    """
    prepare_output_directory()

    documentation_path = OUTPUT_DIRECTORY / "query_summary.md"

    with documentation_path.open("w", encoding="utf-8") as file:
        file.write("# SQL Query Results\n\n")
        file.write(
            "This file documents the SQL queries executed against "
            "the SQLite database and references their saved outputs.\n\n"
        )

    return documentation_path


def save_query_documentation(
    query_name: str,
    query: str,
    row_count: int,
    output_path: Path,
) -> None:
    """
    Append one SQL query's documentation to query_summary.md.

    The documentation includes:
    - Query name
    - SQL statement
    - Number of rows returned
    - Saved CSV filename
    """
    prepare_output_directory()

    documentation_path = OUTPUT_DIRECTORY / "query_summary.md"

    with documentation_path.open("a", encoding="utf-8") as file:
        file.write(f"## {query_name}\n\n")

        file.write("### SQL\n\n")
        file.write("```sql\n")
        file.write(query.strip())
        file.write("\n```\n\n")

        file.write("### Output\n\n")
        file.write(f"- Rows returned: {row_count}\n")
        file.write(f"- CSV file: `{output_path.name}`\n\n")


# ---------------------------------------------------------------------------
# Required SQL query execution
# ---------------------------------------------------------------------------

def run_all_queries() -> None:
    """
    Execute all required SQL queries and save their outputs.

    For each query:
    1. Execute the SQL against SQLite.
    2. Convert the result to a pandas DataFrame.
    3. Save the result as a CSV file.
    4. Save the SQL and output details in query_summary.md.
    """
    prepare_output_directory()
    reset_query_documentation()

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        for query_name, query in QUERIES.items():
            result = execute_query(connection, query)

            output_path = save_query_result(
                result,
                query_name,
            )

            save_query_documentation(
                query_name,
                query,
                len(result),
                output_path,
            )

    finally:
        connection.close()


# ---------------------------------------------------------------------------
# Pandas JOIN verification
# ---------------------------------------------------------------------------

def verify_join_with_pandas() -> bool:
    """
    Reproduce the SQL JOIN independently using pandas.merge().

    The function performs two independent operations:

    1. Reads the required SQL JOIN result using pd.read_sql_query().
    2. Reads the books and categories tables separately into pandas and
       reproduces the JOIN using pd.merge().

    The two resulting DataFrames are normalized into the same column order
    and compared.

    Returns:
        True if the SQL JOIN and pandas JOIN produce identical results.
        Raises ValueError if they do not match.
    """
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        # ------------------------------------------------------------------
        # Step 1: Read the SQL JOIN result into pandas.
        # ------------------------------------------------------------------
        sql_join_df = pd.read_sql_query(
            QUERIES["query_05_category_join"],
            connection,
        )

        # ------------------------------------------------------------------
        # Step 2: Read the normalized tables independently into pandas.
        # No SQL JOIN is used for this step.
        # ------------------------------------------------------------------
        books_df = pd.read_sql_query(
            """
            SELECT
                book_id,
                title,
                price_gbp,
                rating,
                category_id
            FROM books
            """,
            connection,
        )

        categories_df = pd.read_sql_query(
            """
            SELECT
                category_id,
                category_name
            FROM categories
            """,
            connection,
        )

    finally:
        connection.close()

    # ----------------------------------------------------------------------
    # Step 3: Reproduce the JOIN independently using pandas.merge().
    # ----------------------------------------------------------------------
    pandas_join_df = pd.merge(
        books_df,
        categories_df,
        on="category_id",
        how="inner",
    )

    # Keep exactly the same columns as the SQL JOIN.
    pandas_join_df = pandas_join_df[
        [
            "title",
            "price_gbp",
            "rating",
            "category_name",
        ]
    ]

    # Apply the same ordering as the SQL query.
    pandas_join_df = pandas_join_df.sort_values(
        by=["category_name", "title"],
        ascending=[True, True],
    ).reset_index(drop=True)

    sql_join_df = sql_join_df.reset_index(drop=True)

    # ----------------------------------------------------------------------
    # Step 4: Compare SQL and pandas results.
    # ----------------------------------------------------------------------
    results_match = sql_join_df.equals(pandas_join_df)

    if not results_match:
        raise ValueError(
            "SQL JOIN result and pandas.merge() result do not match."
        )

    # ----------------------------------------------------------------------
    # Step 5: Save a verification report.
    # ----------------------------------------------------------------------
    prepare_output_directory()

    verification_path = (
        OUTPUT_DIRECTORY / "join_verification.md"
    )

    with verification_path.open("w", encoding="utf-8") as file:
        file.write("# SQL JOIN vs pandas.merge() Verification\n\n")

        file.write(
            "The SQL JOIN result was independently reproduced using "
            "`pandas.merge()` on the `books` and `categories` DataFrames.\n\n"
        )

        file.write("## SQL JOIN\n\n")
        file.write(
            "- Source query: `query_05_category_join`\n"
        )
        file.write(
            f"- Rows returned: {len(sql_join_df)}\n"
        )

        file.write("\n## pandas.merge()\n\n")
        file.write(
            "- Join method: `pd.merge(..., how=\"inner\")`\n"
        )
        file.write(
            f"- Rows returned: {len(pandas_join_df)}\n"
        )

        file.write("\n## Verification Result\n\n")
        file.write(
            f"- SQL JOIN and pandas JOIN match: **{results_match}**\n"
        )

    return results_match


# ---------------------------------------------------------------------------
# SQL + pandas verification entry point
# ---------------------------------------------------------------------------

def run_sql_analysis() -> None:
    """
    Run the complete SQL analysis and pandas JOIN verification workflow.
    """
    run_all_queries()

    if not verify_join_with_pandas():
        raise ValueError(
            "JOIN verification failed."
        )