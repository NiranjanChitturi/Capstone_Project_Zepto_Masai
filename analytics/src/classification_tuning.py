"""
Module 2 - Classification Tuning and Class-Imbalance Analysis.

This module evaluates:
1. Random Forest baseline
2. Random Forest with class_weight="balanced"
3. Random Forest with SMOTE applied only to training folds
4. Random Forest GridSearchCV
5. Random Forest out-of-bag (OOB) score
"""

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV

from preprocessing import (
    RANDOM_STATE,
    build_preprocessor,
    load_modeling_data,
    select_features_and_target,
    split_data,
)


ANALYTICS_DIR = Path(__file__).resolve().parent.parent
CLASSIFICATION_OUTPUT_DIR = (
    ANALYTICS_DIR / "outputs" / "classification"
)
TUNING_OUTPUT_DIR = ANALYTICS_DIR / "outputs" / "tuning"
MODELS_DIR = ANALYTICS_DIR / "models"

CLASSIFICATION_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
TUNING_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
MODELS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def build_random_forest_pipeline(
    class_weight=None,
    use_smote=False,
) -> ImbPipeline:
    """Build a Random Forest training pipeline."""

    steps = [
        (
            "preprocessor",
            build_preprocessor(),
        )
    ]

    if use_smote:
        steps.append(
            (
                "smote",
                SMOTE(random_state=RANDOM_STATE),
            )
        )

    steps.append(
        (
            "model",
            RandomForestClassifier(
                n_estimators=200,
                random_state=RANDOM_STATE,
                n_jobs=-1,
                class_weight=class_weight,
                oob_score=True,
            ),
        )
    )

    return ImbPipeline(steps=steps)


def evaluate_pipeline(
    name,
    pipeline,
    X_test,
    y_test,
) -> dict:
    """Evaluate a fitted classifier."""

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    return {
        "model": name,
        "accuracy": accuracy_score(
            y_test,
            predictions,
        ),
        "precision": precision_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "f1": f1_score(
            y_test,
            predictions,
            zero_division=0,
        ),
        "roc_auc": roc_auc_score(
            y_test,
            probabilities,
        ),
    }


def save_class_balance_chart(y: pd.Series) -> None:
    """Save the Titanic target-class balance chart."""

    counts = y.value_counts().sort_index()

    plt.figure(figsize=(7, 5))
    plt.bar(
        ["Did not survive", "Survived"],
        counts.values,
    )
    plt.title("Titanic Survival Class Balance")
    plt.ylabel("Passenger Count")
    plt.tight_layout()
    plt.savefig(
        CLASSIFICATION_OUTPUT_DIR / "class_balance.png",
        dpi=150,
    )
    plt.close()


def run_imbalance_comparison(
    X_train,
    X_test,
    y_train,
    y_test,
) -> pd.DataFrame:
    """
    Compare baseline, class-weight-balanced, and SMOTE models.

    SMOTE is inside the pipeline, so it is applied only to the
    training data during fit and never to the held-out test data.
    """

    configurations = {
        "Random Forest Baseline": {
            "class_weight": None,
            "use_smote": False,
        },
        "Random Forest Balanced": {
            "class_weight": "balanced",
            "use_smote": False,
        },
        "Random Forest SMOTE": {
            "class_weight": None,
            "use_smote": True,
        },
    }

    results = []

    for name, configuration in configurations.items():

        print(f"\n--- {name} ---")

        pipeline = build_random_forest_pipeline(
            class_weight=configuration["class_weight"],
            use_smote=configuration["use_smote"],
        )

        pipeline.fit(
            X_train,
            y_train,
        )

        metrics = evaluate_pipeline(
            name,
            pipeline,
            X_test,
            y_test,
        )

        results.append(metrics)

        print(
            f"Accuracy:  {metrics['accuracy']:.4f}"
        )
        print(
            f"Precision: {metrics['precision']:.4f}"
        )
        print(
            f"Recall:    {metrics['recall']:.4f}"
        )
        print(
            f"F1:        {metrics['f1']:.4f}"
        )
        print(
            f"ROC-AUC:   {metrics['roc_auc']:.4f}"
        )

    comparison = pd.DataFrame(results)

    comparison.to_csv(
        CLASSIFICATION_OUTPUT_DIR
        / "imbalance_comparison.csv",
        index=False,
    )

    return comparison


def run_random_forest_grid_search(
    X_train,
    y_train,
) -> GridSearchCV:
    """
    Tune Random Forest using GridSearchCV.

    Required search parameters:
        n_estimators
        max_depth
        max_features
    """

    pipeline = build_random_forest_pipeline()

    parameter_grid = {
        "model__n_estimators": [
            100,
            200,
            300,
        ],
        "model__max_depth": [
            None,
            5,
            10,
            15,
        ],
        "model__max_features": [
            "sqrt",
            "log2",
        ],
    }

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=parameter_grid,
        scoring="roc_auc",
        cv=5,
        n_jobs=-1,
        return_train_score=True,
    )

    grid_search.fit(
        X_train,
        y_train,
    )

    return grid_search


def main() -> None:
    """Run imbalance analysis and Random Forest tuning."""

    df = load_modeling_data()
    X, y = select_features_and_target(df)

    X_train, X_test, y_train, y_test = split_data(
        X,
        y,
    )

    print("\n--- CLASS BALANCE ---")
    print(
        y.value_counts()
        .sort_index()
        .rename(
            index={
                0: "Did not survive",
                1: "Survived",
            }
        )
        .to_string()
    )

    save_class_balance_chart(y)

    imbalance_results = run_imbalance_comparison(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    print("\n--- IMBALANCE COMPARISON ---")
    print(
        imbalance_results.round(4).to_string(
            index=False
        )
    )

    print("\n--- RANDOM FOREST GRID SEARCH ---")

    grid_search = run_random_forest_grid_search(
        X_train,
        y_train,
    )

    best_pipeline = grid_search.best_estimator_

    print("Best parameters:")
    print(grid_search.best_params_)

    print(
        f"Best CV ROC-AUC: "
        f"{grid_search.best_score_:.4f}"
    )

    best_metrics = evaluate_pipeline(
        "Tuned Random Forest",
        best_pipeline,
        X_test,
        y_test,
    )

    print("\n--- TUNED RANDOM FOREST TEST METRICS ---")

    for metric_name, metric_value in best_metrics.items():
        if metric_name != "model":
            print(
                f"{metric_name}: "
                f"{metric_value:.4f}"
            )

    # The final estimator is the Random Forest inside the complete
    # preprocessing pipeline.
    random_forest = best_pipeline.named_steps["model"]

    print(
        f"\nRandom Forest OOB score: "
        f"{random_forest.oob_score_:.4f}"
    )

    grid_results = pd.DataFrame(
        grid_search.cv_results_
    )

    grid_results[
        [
            "param_model__n_estimators",
            "param_model__max_depth",
            "param_model__max_features",
            "mean_test_score",
            "std_test_score",
            "rank_test_score",
        ]
    ].sort_values("rank_test_score").to_csv(
        TUNING_OUTPUT_DIR
        / "rf_gridsearch_results.csv",
        index=False,
    )

    summary = pd.DataFrame(
        [
            {
                **best_metrics,
                "best_cv_roc_auc": grid_search.best_score_,
                "oob_score": random_forest.oob_score_,
                "best_params": str(
                    grid_search.best_params_
                ),
            }
        ]
    )

    summary.to_csv(
        TUNING_OUTPUT_DIR
        / "rf_tuning_summary.csv",
        index=False,
    )

    # Save the complete fitted pipeline so that preprocessing and
    # the tuned model remain together.
    model_path = (
        MODELS_DIR
        / "best_random_forest_pipeline.joblib"
    )

    joblib.dump(
        best_pipeline,
        model_path,
    )

    print(
        f"\nBest fitted pipeline saved to: "
        f"{model_path}"
    )

    print(
        "\nClassification tuning completed successfully."
    )


if __name__ == "__main__":
    main()
