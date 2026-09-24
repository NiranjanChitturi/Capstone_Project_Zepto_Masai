"""
Module 2 - Titanic Classification Models.

Trains and evaluates Logistic Regression, Decision Tree, and
Random Forest classifiers using the same stratified train/test split
and the same training-only preprocessing pipeline.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier

from preprocessing import (
    RANDOM_STATE,
    build_preprocessor,
    load_modeling_data,
    select_features_and_target,
    split_data,
)


ANALYTICS_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ANALYTICS_DIR / "outputs" / "classification"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_models() -> dict:
    """Build the three required classifiers."""

    return {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE,
        ),
        "Decision Tree": DecisionTreeClassifier(
            random_state=RANDOM_STATE,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            oob_score=True,
        ),
    }


def build_pipeline(model) -> Pipeline:
    """Create a complete preprocessing + model pipeline."""

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("model", model),
        ]
    )


def evaluate_model(name, pipeline, X_test, y_test) -> dict:
    """Evaluate one fitted classifier on the untouched test set."""

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]

    return {
        "model": name,
        "accuracy": accuracy_score(y_test, predictions),
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


def save_confusion_matrix(
    name,
    pipeline,
    X_test,
    y_test,
    filename,
) -> None:
    """Save a confusion matrix for a fitted classifier."""

    predictions = pipeline.predict(X_test)
    matrix = confusion_matrix(y_test, predictions)

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=["Did not survive", "Survived"],
    )

    display.plot()
    plt.title(f"Confusion Matrix - {name}")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close()


def save_decision_tree_visualization(
    pipeline,
    X_test,
) -> None:
    """Save the required Decision Tree visualization."""

    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    transformed_feature_names = (
        preprocessor.get_feature_names_out()
    )

    plt.figure(figsize=(24, 12))

    plot_tree(
        model,
        feature_names=transformed_feature_names,
        class_names=["Did not survive", "Survived"],
        filled=True,
        rounded=True,
        max_depth=4,
        fontsize=8,
    )

    plt.title("Decision Tree - Titanic Survival")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "decision_tree.png",
        dpi=150,
    )
    plt.close()


def save_roc_curves(
    fitted_models,
    X_test,
    y_test,
) -> None:
    """Save ROC curves for all three classifiers."""

    plt.figure(figsize=(9, 7))

    for name, pipeline in fitted_models.items():
        probabilities = pipeline.predict_proba(X_test)[:, 1]
        false_positive_rate, true_positive_rate, _ = roc_curve(
            y_test,
            probabilities,
        )
        auc_value = roc_auc_score(
            y_test,
            probabilities,
        )

        plt.plot(
            false_positive_rate,
            true_positive_rate,
            label=f"{name} (AUC={auc_value:.3f})",
        )

    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        label="Random baseline",
    )

    plt.title("ROC Curves - Titanic Classifiers")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "roc_curves.png",
        dpi=150,
    )
    plt.close()


def main() -> None:
    """Train and evaluate all required baseline classifiers."""

    df = load_modeling_data()
    X, y = select_features_and_target(df)

    X_train, X_test, y_train, y_test = split_data(X, y)

    models = build_models()

    fitted_models = {}
    results = []

    print("\n--- CLASSIFICATION DATA ---")
    print(f"Training rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")

    print("\n--- CLASS BALANCE ---")
    print(
        y.value_counts()
        .sort_index()
        .rename(index={0: "Did not survive", 1: "Survived"})
        .to_string()
    )

    for name, model in models.items():
        print(f"\n--- TRAINING: {name} ---")

        pipeline = build_pipeline(model)

        # The complete pipeline is fitted only on X_train/y_train.
        pipeline.fit(X_train, y_train)

        fitted_models[name] = pipeline

        metrics = evaluate_model(
            name,
            pipeline,
            X_test,
            y_test,
        )
        results.append(metrics)

        predictions = pipeline.predict(X_test)

        print(
            classification_report(
                y_test,
                predictions,
                target_names=[
                    "Did not survive",
                    "Survived",
                ],
                zero_division=0,
            )
        )

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

        safe_name = name.lower().replace(" ", "_")

        save_confusion_matrix(
            name,
            pipeline,
            X_test,
            y_test,
            f"confusion_matrix_{safe_name}.png",
        )

    save_decision_tree_visualization(
        fitted_models["Decision Tree"],
        X_test,
    )

    save_roc_curves(
        fitted_models,
        X_test,
        y_test,
    )

    comparison = pd.DataFrame(results)

    comparison.to_csv(
        OUTPUT_DIR / "classifier_comparison.csv",
        index=False,
    )

    print("\n--- CLASSIFIER COMPARISON ---")
    print(comparison.round(4).to_string(index=False))

    print("\nClassification analysis completed successfully.")


if __name__ == "__main__":
    main()
