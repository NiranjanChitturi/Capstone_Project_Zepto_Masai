"""
Module 2 - Titanic dataset loader.

Loads the Titanic dataset once from Seaborn and immediately
saves a local CSV copy for all subsequent analysis and modeling.
"""

from pathlib import Path

import seaborn as sns


# Project paths
ANALYTICS_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ANALYTICS_DIR / "data"
TITANIC_CSV_PATH = DATA_DIR / "titanic.csv"


def load_and_save_titanic() -> None:
    """Load Titanic data from Seaborn and save it locally."""

    # Create the data directory if it does not already exist.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load the dataset from Seaborn.
    df = sns.load_dataset("titanic")

    # Save the original dataset immediately.
    df.to_csv(TITANIC_CSV_PATH, index=False)

    print(f"Titanic dataset saved to: {TITANIC_CSV_PATH}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")


if __name__ == "__main__":
    load_and_save_titanic()