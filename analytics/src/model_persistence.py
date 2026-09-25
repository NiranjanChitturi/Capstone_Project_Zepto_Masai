"""
Module 2 - Model Persistence.

Loads the complete fitted Random Forest pipeline saved by the
classification-tuning stage, reloads it with Joblib, and verifies
that raw/unprocessed passenger input can be passed directly to the
reloaded pipeline to obtain a prediction.

The saved pipeline contains both preprocessing and the fitted model.
"""

from pathlib import Path

import joblib
import pandas as pd


ANALYTICS_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ANALYTICS_DIR / "models"

MODEL_PATH = (
    MODELS_DIR
    / "best_random_forest_pipeline.joblib"
)


def load_saved_pipeline():
    """Load the complete fitted pipeline from disk."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Saved model pipeline was not found: "
            f"{MODEL_PATH}. Run classification_tuning.py first."
        )

    return joblib.load(MODEL_PATH)


def create_raw_passenger_input() -> pd.DataFrame:
    """
    Create one raw passenger record.

    These values intentionally use the original feature names and
    human-readable categorical values expected before preprocessing.

    No scaling, encoding, or imputation is performed manually here.
    """

    return pd.DataFrame(
        [
            {
                "pclass": 1,
                "sex": "female",
                "age": 30.0,
                "sibsp": 0,
                "parch": 0,
                "fare": 80.0,
                "embarked": "S",
            }
        ]
    )


def main() -> None:
    """Reload the saved pipeline and verify raw-input prediction."""

    print("\n--- MODEL PERSISTENCE TEST ---")

    pipeline = load_saved_pipeline()

    print(
        f"Loaded fitted pipeline from: {MODEL_PATH}"
    )

    raw_input = create_raw_passenger_input()

    print("\n--- RAW INPUT ---")
    print(raw_input.to_string(index=False))

    prediction = pipeline.predict(raw_input)

    probability = None

    if hasattr(pipeline, "predict_proba"):
        probability = pipeline.predict_proba(
            raw_input
        )[0, 1]

    predicted_class = int(prediction[0])

    print("\n--- RELOADED PIPELINE PREDICTION ---")

    if predicted_class == 1:
        label = "Survived"
    else:
        label = "Did not survive"

    print(
        f"Predicted class: {predicted_class}"
    )
    print(
        f"Prediction label: {label}"
    )

    if probability is not None:
        print(
            f"Predicted survival probability: "
            f"{probability:.4f}"
        )

    print(
        "\nModel persistence validation completed successfully."
    )


if __name__ == "__main__":
    main()
