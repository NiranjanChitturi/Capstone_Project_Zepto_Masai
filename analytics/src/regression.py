"""
Module 2 - Multivariate Linear Regression.

Predicts Titanic passenger fare using other available passenger
features and evaluates the regression model with MAE, RMSE, R²,
and adjusted R².

Preprocessing is fitted only on the training data through a complete
scikit-learn Pipeline.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ANALYTICS_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ANALYTICS_DIR / "data"
OUTPUT_DIR = (
    ANALYTICS_DIR
    / "outputs"
    / "regression"
)

TITANIC_CSV_PATH = DATA_DIR / "titanic.csv"

RANDOM_STATE = 42
TEST_SIZE = 0.20

TARGET_COLUMN = "fare"

REGRESSION_FEATURES = [
    "survived",
    "pclass",
    "sex",
    "age",
    "sibsp",
    "parch",
    "embarked",
]

NUMERIC_FEATURES = [
    "survived",
    "pclass",
    "age",
    "sibsp",
    "parch",
]

CATEGORICAL_FEATURES = [
    "sex",
    "embarked",
]


def load_data() -> pd.DataFrame:
    """Load the committed Titanic CSV."""

    if not TITANIC_CSV_PATH.exists():
        raise FileNotFoundError(
            f"Titanic CSV not found: {TITANIC_CSV_PATH}"
        )

    return pd.read_csv(TITANIC_CSV_PATH)


def build_preprocessor() -> ColumnTransformer:
    """Build the regression preprocessing transformer."""

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

    return ColumnTransformer(
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


def adjusted_r2(
    r2: float,
    sample_count: int,
    feature_count: int,
) -> float:
    """Calculate adjusted R-squared."""

    if sample_count <= feature_count + 1:
        return float("nan")

    return 1 - (
        (1 - r2)
        * (sample_count - 1)
        / (sample_count - feature_count - 1)
    )


def main() -> None:
    """Train and evaluate the multivariate fare regression."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = load_data()

    X = df[REGRESSION_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "model",
                LinearRegression(),
            ),
        ]
    )

    # Fit preprocessing and regression model using training data only.
    pipeline.fit(
        X_train,
        y_train,
    )

    predictions = pipeline.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions,
        )
    )

    r2 = r2_score(
        y_test,
        predictions,
    )

    # Determine the number of features after preprocessing.
    preprocessor = pipeline.named_steps[
        "preprocessor"
    ]

    transformed_X_test = preprocessor.transform(
        X_test
    )

    feature_count = transformed_X_test.shape[1]

    adjusted_r2_value = adjusted_r2(
        r2,
        len(y_test),
        feature_count,
    )

    metrics = pd.DataFrame(
        [
            {
                "MAE": mae,
                "RMSE": rmse,
                "R2": r2,
                "Adjusted_R2": adjusted_r2_value,
                "test_rows": len(y_test),
                "model_features_after_encoding": feature_count,
            }
        ]
    )

    metrics.to_csv(
        OUTPUT_DIR / "regression_metrics.csv",
        index=False,
    )

    print("\n--- REGRESSION METRICS ---")
    print(metrics.round(4).to_string(index=False))

    # Residuals are actual minus predicted values.
    residuals = y_test - predictions

    plt.figure(figsize=(9, 6))
    plt.scatter(
        predictions,
        residuals,
        alpha=0.6,
    )
    plt.axhline(
        0,
        linestyle="--",
    )
    plt.title(
        "Fare Regression Residual Plot"
    )
    plt.xlabel("Predicted Fare")
    plt.ylabel("Residual")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "residual_plot.png",
        dpi=150,
    )
    plt.close()

    # A residual pattern with approximately constant spread around
    # zero is more consistent with homoscedasticity. A funnel-shaped
    # or systematically changing spread suggests heteroscedasticity.
    correlation = np.corrcoef(
        predictions,
        np.abs(residuals),
    )[0, 1]

    if abs(correlation) >= 0.30:
        heteroscedasticity_conclusion = (
            "The residual analysis shows evidence consistent "
            "with changing residual spread as predicted fare "
            "increases, suggesting possible heteroscedasticity."
        )
    else:
        heteroscedasticity_conclusion = (
            "The residual analysis does not show strong evidence "
            "of changing residual spread based on the correlation "
            "between predicted values and absolute residuals."
        )

    interpretation = f"""# Fare Regression Interpretation

## Metrics

- MAE: {mae:.4f}
- RMSE: {rmse:.4f}
- R²: {r2:.4f}
- Adjusted R²: {adjusted_r2_value:.4f}

## Residual Analysis

The residual plot compares predicted fare with the difference
between actual and predicted fare.

{heteroscedasticity_conclusion}

The residual plot should be interpreted together with the metric
values rather than using a single diagnostic as the sole measure
of regression quality.
"""

    (
        OUTPUT_DIR / "regression_interpretation.md"
    ).write_text(
        interpretation,
        encoding="utf-8",
    )

    print(
        "\n--- HETEROSCEDASTICITY ANALYSIS ---"
    )
    print(heteroscedasticity_conclusion)

    print(
        "\nRegression analysis completed successfully."
    )


if __name__ == "__main__":
    main()
