"""
Module 1 - Data Pipeline
------------------------
Data cleaning and transformation utilities.

This module is responsible for converting the raw scraped book data
into a clean, typed dataset suitable for database storage and analysis.

Cleaning responsibilities will include:
1. Price conversion from text to numeric GBP.
2. Star-rating conversion from words to integers.
3. Availability conversion to an in-stock indicator.
4. Validation of required fields.
5. GBP-to-INR price conversion using the project rate.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Project Configuration
# ---------------------------------------------------------------------------

# Fixed artificial exchange rate required by the capstone assignment.
# No external currency API is used.
GBP_TO_INR_RATE = 105.50

# ---------------------------------------------------------------------------
# Price Data Cleaning
# ---------------------------------------------------------------------------

def clean_price(price_text: str) -> float:
    """
    Convert a raw price string into a numeric GBP value.

    Example:
        "£47.82" -> 47.82

    The source website may return an encoding artifact such as "Â£".
    Removing all non-numeric currency characters keeps the function
    robust against that representation.
    """

    if not isinstance(price_text, str):
        raise ValueError("Price must be provided as a string.")

    # Keep digits and the decimal point only.
    cleaned_price = "".join(
        character
        for character in price_text
        if character.isdigit() or character == "."
    )

    if not cleaned_price:
        raise ValueError(f"Unable to parse price: {price_text!r}")

    return float(cleaned_price)

# ---------------------------------------------------------------------------
# Star Rating Cleaning
# ---------------------------------------------------------------------------

def clean_rating(rating_text: str) -> int:
    """
    Convert the website's textual star rating into an integer.

    Example:
        "One"   -> 1
        "Three" -> 3
        "Five"  -> 5
    """

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    if not isinstance(rating_text, str):
        raise ValueError("Star rating must be provided as a string.")

    rating_text = rating_text.strip()

    if rating_text not in rating_map:
        raise ValueError(f"Unable to parse star rating: {rating_text!r}")

    return rating_map[rating_text]


# ---------------------------------------------------------------------------
# Availability Cleaning
# ---------------------------------------------------------------------------

def clean_availability(availability_text: str) -> bool:
    """
    Convert the raw availability text into an in-stock boolean.

    Example:
        "In stock" -> True
        "Out of stock" -> False
    """

    if not isinstance(availability_text, str):
        raise ValueError("Availability must be provided as a string.")

    normalized = availability_text.strip().lower()

    # Check the more specific "out of stock" condition first.
    if normalized == "out of stock":
        return False

    if normalized == "in stock":
        return True

    raise ValueError(
        f"Unable to parse availability: {availability_text!r}"
    )

# ---------------------------------------------------------------------------
# Currency Conversion
# ---------------------------------------------------------------------------

def convert_gbp_to_inr(price_gbp: float) -> float:
    """
    Convert a GBP price into INR using the fixed project exchange rate.

    Project requirement:
        1 GBP = 105.50 INR

    No external currency API is used.
    """

    if not isinstance(price_gbp, (int, float)):
        raise ValueError("GBP price must be numeric.")

    return round(price_gbp * GBP_TO_INR_RATE, 2)


# ---------------------------------------------------------------------------
# DataFrame Cleaning
# ---------------------------------------------------------------------------

def clean_books_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw books DataFrame and create analysis-ready columns.

    Transformations:
    - price -> price_gbp
    - star_rating -> rating
    - availability -> in_stock
    - price_gbp -> price_inr

    The original raw columns are retained until validation is complete.
    """

    required_columns = {
        "title",
        "price",
        "star_rating",
        "availability",
        "category",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    cleaned_df = df.copy()

    # Convert raw price text into numeric GBP.
    cleaned_df["price_gbp"] = cleaned_df["price"].apply(clean_price)

    # Convert textual star rating into integer rating.
    cleaned_df["rating"] = cleaned_df["star_rating"].apply(clean_rating)

    # Convert availability text into boolean stock status.
    cleaned_df["in_stock"] = cleaned_df["availability"].apply(
        clean_availability
    )

    # Convert GBP price into INR using the fixed project rate.
    cleaned_df["price_inr"] = cleaned_df["price_gbp"].apply(
        convert_gbp_to_inr
    )

    return cleaned_df

# ---------------------------------------------------------------------------
# Cleaning Validation
# ---------------------------------------------------------------------------

def validate_cleaned_books(df: pd.DataFrame) -> None:
    """
    Validate the cleaned book dataset before database storage.

    Raises:
        ValueError: If any required validation rule fails.
    """

    required_columns = {
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing cleaned columns: {sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError("Cleaned dataset must not be empty.")

    if df["title"].isna().any():
        raise ValueError("Book titles must not contain missing values.")

    if df["category"].isna().any():
        raise ValueError("Book categories must not contain missing values.")

    if not df["rating"].between(1, 5).all():
        raise ValueError("Ratings must contain values from 1 to 5.")

    if not df["price_gbp"].notna().all():
        raise ValueError("price_gbp must not contain missing values.")

    if not df["price_inr"].notna().all():
        raise ValueError("price_inr must not contain missing values.")

    if not df["in_stock"].isin([True, False]).all():
        raise ValueError("in_stock must contain only True or False.")

    # Verify the required fixed exchange-rate calculation.
    # expected_price_inr = (
    # df["price_gbp"] * GBP_TO_INR_RATE
    # ).round(2)

    # if not np.isclose(
    #     df["price_inr"],
    #     expected_price_inr,
    #     rtol=1e-9,
    #     atol=1e-9,
    # ).all():
    #     raise ValueError(
    #         "price_inr does not match the required GBP-to-INR rate."
    #     )
    
    
    # Verify the required fixed exchange-rate calculation.
    
    expected_price_inr = df["price_gbp"].apply(
    convert_gbp_to_inr
    )

    if not np.isclose(
        df["price_inr"],
        expected_price_inr,
        rtol=1e-9,
        atol=1e-9,
    ).all():
        raise ValueError(
            "price_inr does not match the required GBP-to-INR rate."
        )

# ---------------------------------------------------------------------------
# Processed Dataset Export and Save
# ---------------------------------------------------------------------------

def save_cleaned_books(
    df: pd.DataFrame,
    output_path: str,
) -> None:
    """
    Save the validated cleaned book dataset as a CSV file.

    Only the columns required for downstream database processing
    are retained.
    """

    output_columns = [
        "title",
        "price_gbp",
        "price_inr",
        "rating",
        "in_stock",
        "category",
    ]

    missing_columns = set(output_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns required for export: {sorted(missing_columns)}"
        )

    cleaned_output = df[output_columns].copy()

    cleaned_output.to_csv(
        output_path,
        index=False,
        encoding="utf-8",
    )