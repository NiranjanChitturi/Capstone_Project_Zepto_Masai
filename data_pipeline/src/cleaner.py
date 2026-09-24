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

import pandas as pd


# ---------------------------------------------------------------------------
# Project Configuration
# ---------------------------------------------------------------------------

# Fixed artificial exchange rate required by the capstone assignment.
# No external currency API is used.
GBP_TO_INR_RATE = 105.50