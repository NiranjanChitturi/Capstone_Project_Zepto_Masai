"""
Module 1 - Data Pipeline
------------------------
End-to-end pipeline runner.

This module provides one reproducible entry point for:
1. Scraping the selected book categories.
2. Saving the raw dataset.
3. Cleaning and validating the dataset.
4. Saving the processed dataset.
5. Loading the cleaned data into SQLite.
6. Running the required SQL analysis.
7. Verifying the SQL JOIN independently with pandas.

The pipeline can therefore be regenerated without manual
copy/paste between individual steps.
"""

from pathlib import Path

import pandas as pd

from .cleaner import (
    clean_books_dataframe,
    save_cleaned_books,
    validate_cleaned_books,
)
from .database import load_books_to_database
from .queries import run_sql_analysis
from .scraper import (
    save_raw_books,
    scrape_books,
    validate_scraped_books,
)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DATA_DIRECTORY = (
    Path(__file__).resolve().parent.parent / "data"
)

RAW_DATA_PATH = DATA_DIRECTORY / "raw" / "books_raw.csv"

PROCESSED_DATA_PATH = (
    DATA_DIRECTORY / "processed" / "books_cleaned.csv"
)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline() -> None:
    """
    Run the complete Module 1 data pipeline.

    The workflow is:

        Scrape
          ↓
        Validate raw data
          ↓
        Save raw CSV
          ↓
        Clean
          ↓
        Validate cleaned data
          ↓
        Save processed CSV
          ↓
        Load SQLite database
          ↓
        Run SQL analysis
          ↓
        Verify SQL JOIN with pandas
    """

    print("Starting Module 1 data pipeline...")

    # ----------------------------------------------------------------------
    # Step 1: Scrape
    # ----------------------------------------------------------------------
    print("\n[1/6] Scraping books...")

    selected_categories = [
    "Mystery",
    "Historical Fiction",
    "Romance"]

    books = scrape_books(selected_categories)

    validate_scraped_books(books)

    raw_dataframe = pd.DataFrame(books)

    save_raw_books(
        books,
        RAW_DATA_PATH,
    )

    print(f"Scraped books: {len(raw_dataframe)}")
    print(f"Raw dataset: {RAW_DATA_PATH}")

    # ----------------------------------------------------------------------
    # Step 2: Clean and validate
    # ----------------------------------------------------------------------
    print("\n[2/6] Cleaning and validating data...")

    cleaned_dataframe = clean_books_dataframe(
        raw_dataframe
    )

    validate_cleaned_books(
        cleaned_dataframe
    )

    save_cleaned_books(
        cleaned_dataframe,
        PROCESSED_DATA_PATH,
    )

    print(
        f"Cleaned books: {len(cleaned_dataframe)}"
    )
    print(
        f"Processed dataset: {PROCESSED_DATA_PATH}"
    )

    # ----------------------------------------------------------------------
    # Step 3: Load SQLite database
    # ----------------------------------------------------------------------
    print("\n[3/6] Loading SQLite database...")

    load_books_to_database(
        cleaned_dataframe
    )

    print("SQLite database loaded successfully.")

    # ----------------------------------------------------------------------
    # Step 4: Run SQL analysis
    # ----------------------------------------------------------------------
    print("\n[4/6] Running SQL analysis...")

    run_sql_analysis()

    print("SQL analysis completed successfully.")

    # ----------------------------------------------------------------------
    # Step 5: Final summary
    # ----------------------------------------------------------------------
    category_count = (
        cleaned_dataframe["category"]
        .nunique()
    )

    print("\n[5/6] Final validation summary")
    print(f"Books: {len(cleaned_dataframe)}")
    print(f"Categories: {category_count}")
    print(
        "Required minimum books: "
        f"{60} -> "
        f"{'PASS' if len(cleaned_dataframe) >= 60 else 'FAIL'}"
    )
    print(
        "Required minimum categories: "
        f"{3} -> "
        f"{'PASS' if category_count >= 3 else 'FAIL'}"
    )

    print("\n[6/6] Module 1 pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()

    