"""
Module 2 - Machine Learning Preprocessing Foundation.

This module prepares the Titanic dataset for machine-learning tasks
while preventing data leakage.

Important design rules:
1. Read the committed Titanic CSV rather than loading Seaborn again.
2. Separate features and target before the train/test split.
3. Perform a stratified train/test split before fitting preprocessing.
4. Build preprocessing transformers but do NOT fit them here.
5. Model pipelines will fit preprocessing only on the training data.
"""

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# -------------------------------------------------------------
# Project paths
# -------------------------------------------------------------

ANALYTICS_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ANALYTICS_DIR / "data"

TITANIC_CSV_PATH = DATA_DIR / "titanic.csv"


# -------------------------------------------------------------
# Modeling configuration
# -------------------------------------------------------------

TARGET_COLUMN = "survived"

# Features selected for the machine-learning models.
#
# Leakage and redundant columns are intentionally excluded.
FEATURE_COLUMNS = [
    "pclass",
    "sex",
    "age",
    "sibsp",
    "parch",
    "fare",
    "embarked",
]

NUMERIC_FEATURES = [
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare",
]

CATEGORICAL_FEATURES = [
    "sex",
    "embarked",
]

TEST_SIZE = 0.20
RANDOM_STATE = 42


# -------------------------------------------------------------
# Data loading
# -------------------------------------------------------------

def load_modeling_data() -> pd.DataFrame:
    """
    Load the committed Titanic CSV for machine learning.

    No call to seaborn.load_dataset() is made here.
    """

    if not TITANIC_CSV_PATH.exists():
        raise FileNotFoundError(
            f"Titanic CSV not found: {TITANIC_CSV_PATH}"
        )

    return pd.read_csv(TITANIC_CSV_PATH)


# -------------------------------------------------------------
# Feature selection
# -------------------------------------------------------------

def select_features_and_target(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Select the modeling features and target.

    Target:
        survived

    Features:
        pclass
        sex
        age
        sibsp
        parch
        fare
        embarked

    Excluded columns:

        alive
            Direct representation of the survival target and therefore
            would cause target leakage.

        class
            Duplicate representation of pclass.

        who
            Derived passenger grouping.

        adult_male
            Derived from other passenger attributes.

        alone
            Derived family-status variable.

        deck
            Very high missingness and removed during EDA.

        embark_town
            Duplicate location information represented by embarked.
    """

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required modeling columns are missing: "
            + ", ".join(missing_columns)
        )

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    return X, y


# -------------------------------------------------------------
# Stratified train/test split
# -------------------------------------------------------------

def split_data(
    X: pd.DataFrame,
    y: pd.Series,
) -> Tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.Series,
    pd.Series,
]:
    """
    Perform the stratified train/test split.

    The split occurs BEFORE preprocessing is fitted.

    Stratification preserves the target-class distribution between
    the training and test sets.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    return X_train, X_test, y_train, y_test


# -------------------------------------------------------------
# Preprocessing pipeline
# -------------------------------------------------------------

def build_preprocessor() -> ColumnTransformer:
    """
    Build the preprocessing transformer.

    Numeric features:
        Median imputation
        StandardScaler

    Categorical features:
        Most-frequent imputation
        OneHotEncoder

    IMPORTANT:
        This function only constructs the transformer.
        It does NOT fit the transformer.

    The transformer will later be placed inside a complete
    sklearn Pipeline with a classifier or regressor. The complete
    pipeline will be fitted using training data only.
    """

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
    )

    return preprocessor


# -------------------------------------------------------------
# Preparation helper
# -------------------------------------------------------------

def prepare_modeling_data():
    """
    Prepare the modeling data.

    Steps:
        1. Load the committed Titanic CSV.
        2. Select features and target.
        3. Perform stratified train/test split.
        4. Build an unfitted preprocessing transformer.

    Returns
    -------
    tuple
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor

    The preprocessor is intentionally UNFITTED.
    """

    df = load_modeling_data()

    X, y = select_features_and_target(df)

    X_train, X_test, y_train, y_test = split_data(
        X,
        y,
    )

    preprocessor = build_preprocessor()

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
    )


# -------------------------------------------------------------
# Validation
# -------------------------------------------------------------

def validate_preprocessing_setup() -> None:
    """
    Validate the machine-learning preprocessing foundation.

    No model is trained in this module.

    The validation checks:
        - Correct source CSV
        - Correct feature selection
        - Target separation
        - Stratified split
        - Numeric preprocessing
        - Categorical preprocessing
        - Target leakage prevention
    """

    df = load_modeling_data()

    X, y = select_features_and_target(df)

    X_train, X_test, y_train, y_test = split_data(
        X,
        y,
    )

    preprocessor = build_preprocessor()

    print("\n--- MODELING DATASET ---")
    print(f"Original rows: {len(df)}")
    print(f"Feature columns: {FEATURE_COLUMNS}")
    print(f"Target column: {TARGET_COLUMN}")

    print("\n--- SELECTED FEATURES ---")
    print(X.dtypes.to_string())

    print("\n--- STRATIFIED TRAIN/TEST SPLIT ---")
    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")

    print("\n--- TARGET CLASS DISTRIBUTION ---")

    print("Overall:")
    print(
        y.value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
        .to_string()
    )

    print("\nTraining:")
    print(
        y_train.value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
        .to_string()
    )

    print("\nTesting:")
    print(
        y_test.value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
        .to_string()
    )

    print("\n--- PREPROCESSING CONFIGURATION ---")

    print("Numeric features:")
    print(NUMERIC_FEATURES)

    print("\nCategorical features:")
    print(CATEGORICAL_FEATURES)

    print("\nNumeric preprocessing:")
    print("  Median imputation -> StandardScaler")

    print("\nCategorical preprocessing:")
    print("  Most-frequent imputation -> OneHotEncoder")

    print("\nPreprocessor fitting:")
    print("  NOT FITTED in preprocessing.py")
    print("  Will be fitted only through model pipelines on X_train.")

    print("\n--- LEAKAGE CHECK ---")

    leakage_columns = {
        "survived",
        "alive",
    }

    selected_columns = set(FEATURE_COLUMNS)

    found_leakage = selected_columns.intersection(
        leakage_columns
    )

    if found_leakage:
        raise AssertionError(
            "Potential target leakage detected: "
            + ", ".join(sorted(found_leakage))
        )

    print("Target leakage check: PASS")
    print(
        "The target column and 'alive' are not model features."
    )


# -------------------------------------------------------------
# Main execution
# -------------------------------------------------------------

def main() -> None:
    """
    Validate the machine-learning preprocessing foundation.

    No model is trained in this module.
    """

    validate_preprocessing_setup()


if __name__ == "__main__":
    main()
