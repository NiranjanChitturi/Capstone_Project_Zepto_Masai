"""
Module 1 - Data Pipeline
------------------------
SQLite database utilities.

This module is responsible for:
1. Creating the SQLite database.
2. Creating the normalized categories and books tables.
3. Loading the cleaned book dataset.
4. Maintaining the required primary-key and foreign-key relationships.
5. Rebuilding the database safely when existing data is present.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import sqlite3
from pathlib import Path


# ---------------------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------------------

# Store the SQLite database in a dedicated database folder.
DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "database"
    / "books.db"
)


# ---------------------------------------------------------------------------
# Table Creation
# ---------------------------------------------------------------------------

def create_tables(connection: sqlite3.Connection) -> None:
    """
    Create the normalized categories and books tables.

    Schema:

        categories
            category_id INTEGER PRIMARY KEY
            category_name TEXT UNIQUE

        books
            book_id INTEGER PRIMARY KEY
            title TEXT
            price_gbp REAL
            price_inr REAL
            rating INTEGER
            in_stock INTEGER
            category_id INTEGER FOREIGN KEY
    """

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
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
        """
    )

    connection.commit()


# ---------------------------------------------------------------------------
# Database Connection
# ---------------------------------------------------------------------------

def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.

    Foreign-key enforcement is enabled explicitly because SQLite does not
    enforce foreign keys by default.
    """

    # Create the database directory automatically if it does not exist.
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign-key enforcement for this connection.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ---------------------------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------------------------

def initialize_database() -> None:
    """
    Create the SQLite database and required tables if they do not exist.
    """

    connection = get_connection()

    try:
        create_tables(connection)
    finally:
        connection.close()


# ---------------------------------------------------------------------------
# Category Loading
# ---------------------------------------------------------------------------

def insert_categories(
    connection: sqlite3.Connection,
    categories: list[str],
) -> None:
    """
    Insert unique category names into the categories table.

    The caller controls the transaction and commit.
    """

    connection.executemany(
        """
        INSERT OR IGNORE INTO categories (category_name)
        VALUES (?)
        """,
        [(category,) for category in categories],
    )


# ---------------------------------------------------------------------------
# Book Loading
# ---------------------------------------------------------------------------

def insert_books(
    connection: sqlite3.Connection,
    books: list[tuple],
) -> None:
    """
    Insert cleaned books into the books table.

    The caller controls the transaction and commit.

    Each tuple must contain:

        title,
        price_gbp,
        price_inr,
        rating,
        in_stock,
        category_id
    """

    connection.executemany(
        """
        INSERT INTO books (
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        books,
    )


# ---------------------------------------------------------------------------
# DataFrame Transformation
# ---------------------------------------------------------------------------

def prepare_books_for_database(
    dataframe,
    connection: sqlite3.Connection,
) -> list[tuple]:
    """
    Transform a cleaned DataFrame into tuples suitable for books insertion.

    The category name from the DataFrame is replaced by the corresponding
    category_id from the categories table.
    """

    category_rows = connection.execute(
        """
        SELECT category_id, category_name
        FROM categories
        """
    ).fetchall()

    category_lookup = {
        category_name: category_id
        for category_id, category_name in category_rows
    }

    books = []

    for row in dataframe.itertuples(index=False):
        category_id = category_lookup.get(row.category)

        if category_id is None:
            raise ValueError(
                f"Category not found in database: {row.category!r}"
            )

        books.append(
            (
                row.title,
                row.price_gbp,
                row.price_inr,
                row.rating,
                int(row.in_stock),
                category_id,
            )
        )

    return books


# ---------------------------------------------------------------------------
# End-to-End Database Load
# ---------------------------------------------------------------------------

def load_books_to_database(dataframe) -> None:
    """
    Load the cleaned books DataFrame into the SQLite database.

    If existing book data is present:
    - Delete books first.
    - Delete categories second.
    - Reload the complete dataset.

    If the database is empty:
    - Load the dataset directly.

    The complete rebuild is handled as one transaction so that a failure
    can be rolled back without leaving the database in a partial state.
    """

    connection = get_connection()

    try:
        # ---------------------------------------------------------------
        # Check whether existing book data is present.
        # ---------------------------------------------------------------
        existing_books = connection.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

        if existing_books > 0:
            # Books must be deleted before categories because
            # books.category_id references categories.category_id.
            connection.execute("DELETE FROM books")
            connection.execute("DELETE FROM categories")

        # ---------------------------------------------------------------
        # Extract unique categories from the cleaned DataFrame.
        # ---------------------------------------------------------------
        categories = sorted(
            dataframe["category"].dropna().unique().tolist()
        )

        # ---------------------------------------------------------------
        # Insert categories first so their IDs are available to books.
        # ---------------------------------------------------------------
        insert_categories(
            connection,
            categories,
        )

        # ---------------------------------------------------------------
        # Convert DataFrame rows into normalized book records.
        # ---------------------------------------------------------------
        books = prepare_books_for_database(
            dataframe,
            connection,
        )

        # ---------------------------------------------------------------
        # Insert normalized book records.
        # ---------------------------------------------------------------
        insert_books(
            connection,
            books,
        )

        # ---------------------------------------------------------------
        # Commit the complete database rebuild as one transaction.
        # ---------------------------------------------------------------
        connection.commit()

    except Exception:
        # Roll back the complete operation if anything fails.
        connection.rollback()
        raise

    finally:
        # Always close the database connection.
        connection.close()