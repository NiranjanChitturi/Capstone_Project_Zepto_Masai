"""
Module 2 - Exploratory Data Analysis.

Loads the committed Titanic CSV, cleans the data using the
documented missing-value strategy, and performs the required
exploratory analysis.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# -------------------------------------------------------------
# Project paths
# -------------------------------------------------------------

ANALYTICS_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ANALYTICS_DIR / "data"
OUTPUT_DIR = ANALYTICS_DIR / "outputs"

TITANIC_CSV_PATH = DATA_DIR / "titanic.csv"
CLEANED_CSV_PATH = DATA_DIR / "titanic_cleaned.csv"


# -------------------------------------------------------------
# Data loading
# -------------------------------------------------------------

def load_data() -> pd.DataFrame:
    """Load the committed Titanic CSV."""

    return pd.read_csv(TITANIC_CSV_PATH)


# -------------------------------------------------------------
# Dataset overview and missing-value analysis
# -------------------------------------------------------------

def print_dataset_overview(df: pd.DataFrame) -> None:
    """
    Print the required dataset structure and descriptive statistics.

    This runs on the original committed Titanic CSV before cleaning so
    the missing-value analysis reflects the source dataset.
    """

    print("\n--- DATASET SHAPE ---")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Shape: {df.shape}")

    print("\n--- DATASET INFO ---")
    df.info()

    print("\n--- DESCRIPTIVE STATISTICS ---")
    print(df.describe(include="all").to_string())

    print("\n--- MISSING VALUE PERCENTAGES ---")
    missing_counts = df.isna().sum()
    missing_percentages = (missing_counts / len(df) * 100).round(2)

    missing_summary = pd.DataFrame(
        {
            "missing_count": missing_counts,
            "missing_percentage": missing_percentages,
        }
    )

    missing_summary = missing_summary[
        missing_summary["missing_count"] > 0
    ]

    if missing_summary.empty:
        print("No columns contain missing values.")
    else:
        print(missing_summary.to_string())


# -------------------------------------------------------------
# Data cleaning
# -------------------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Titanic dataset using the documented
    missing-value strategy.

    Strategy:
    - age: approximately 19.87% missing -> median imputation.
    - embarked: approximately 0.22% missing -> drop affected rows.
    - deck: approximately 77.22% missing -> drop column.
    - embark_town: approximately 0.22% missing -> drop affected rows.
    """

    cleaned_df = df.copy()

    # Very high missingness: remove the deck column.
    cleaned_df = cleaned_df.drop(columns=["deck"])

    # Low missingness: remove rows missing these categorical values.
    cleaned_df = cleaned_df.dropna(
        subset=["embarked", "embark_town"]
    )

    # Moderate missingness: median-impute age.
    cleaned_df["age"] = cleaned_df["age"].fillna(
        cleaned_df["age"].median()
    )

    return cleaned_df


def save_cleaned_data(df: pd.DataFrame) -> None:
    """
    Save the cleaned Titanic dataset.

    The same filename is intentionally overwritten on reruns
    so the output always represents the current cleaning logic.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        CLEANED_CSV_PATH,
        index=False
    )

    print(f"Cleaned dataset saved to: {CLEANED_CSV_PATH}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")


# -------------------------------------------------------------
# Age and Fare analysis
# -------------------------------------------------------------

def calculate_iqr_outliers(
    df: pd.DataFrame,
    column: str
) -> int:
    """
    Calculate the number of IQR-based outliers.

    A value is considered an outlier when it is below
    Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR.
    """

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    outliers = df[
        (df[column] < lower_bound)
        | (df[column] > upper_bound)
    ]

    return len(outliers)


def analyze_age_and_fare(df: pd.DataFrame) -> None:
    """
    Analyze Age and Fare distributions.

    Generates:
    - Age histogram
    - Fare histogram
    - Age boxplot
    - Fare boxplot

    Also calculates:
    - IQR outlier counts
    - Fare mean
    - Fare median
    - Fare mode
    - Basic skewness interpretation
    """

    # Create output directory if it does not exist.
    # Safe to rerun because exist_ok=True.
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------------------------
    # Age histogram
    # ---------------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["age"],
        bins=20
    )

    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "age_histogram.png",
        dpi=150
    )

    plt.close()

    # ---------------------------------------------------------
    # Fare histogram
    # ---------------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["fare"],
        bins=20
    )

    plt.title("Fare Distribution")
    plt.xlabel("Fare")
    plt.ylabel("Frequency")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "fare_histogram.png",
        dpi=150
    )

    plt.close()

    # ---------------------------------------------------------
    # Age boxplot
    # ---------------------------------------------------------

    plt.figure(figsize=(8, 4))

    plt.boxplot(
        df["age"]
    )

    plt.title("Age Boxplot")
    plt.ylabel("Age")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "age_boxplot.png",
        dpi=150
    )

    plt.close()

    # ---------------------------------------------------------
    # Fare boxplot
    # ---------------------------------------------------------

    plt.figure(figsize=(8, 4))

    plt.boxplot(
        df["fare"]
    )

    plt.title("Fare Boxplot")
    plt.ylabel("Fare")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "fare_boxplot.png",
        dpi=150
    )

    plt.close()

    # ---------------------------------------------------------
    # IQR outlier counts
    # ---------------------------------------------------------

    age_outliers = calculate_iqr_outliers(
        df,
        "age"
    )

    fare_outliers = calculate_iqr_outliers(
        df,
        "fare"
    )

    print("\n--- IQR OUTLIER COUNTS ---")
    print(f"Age outliers: {age_outliers}")
    print(f"Fare outliers: {fare_outliers}")

    # ---------------------------------------------------------
    # Fare statistics
    # ---------------------------------------------------------

    fare_mean = df["fare"].mean()
    fare_median = df["fare"].median()
    fare_mode = df["fare"].mode().iloc[0]

    print("\n--- FARE STATISTICS ---")
    print(f"Mean: {fare_mean:.4f}")
    print(f"Median: {fare_median:.4f}")
    print(f"Mode: {fare_mode:.4f}")

    # ---------------------------------------------------------
    # Basic skewness interpretation
    # ---------------------------------------------------------

    if fare_mean > fare_median > fare_mode:
        skewness = "Right-skewed"

    elif fare_mean < fare_median < fare_mode:
        skewness = "Left-skewed"

    else:
        skewness = (
            "Not clearly determined from "
            "mean/median/mode ordering"
        )

    print(
        f"Skewness interpretation: {skewness}"
    )


# -------------------------------------------------------------
# Survival analysis
# -------------------------------------------------------------

def analyze_survival_patterns(
    df: pd.DataFrame
) -> None:
    """
    Analyze survival patterns using boolean masking
    and grouped survival rates.

    Demonstrates:
    - Boolean masking with &
    - Boolean masking with |
    - Survival rate by sex
    - Survival rate by passenger class
    - Survival rate by sex and passenger class
    """

    # ---------------------------------------------------------
    # Boolean masking using AND (&)
    #
    # Example:
    # Female passengers AND first-class passengers.
    # ---------------------------------------------------------

    female_first_class = df[
        (df["sex"] == "female")
        & (df["pclass"] == 1)
    ]

    # ---------------------------------------------------------
    # Boolean masking using OR (|)
    #
    # Example:
    # First-class OR second-class passengers.
    # ---------------------------------------------------------

    first_or_second_class = df[
        (df["pclass"] == 1)
        | (df["pclass"] == 2)
    ]

    print("\n--- BOOLEAN MASKING ---")

    print(
        "Female passengers in first class:",
        len(female_first_class)
    )

    print(
        "Passengers in first or second class:",
        len(first_or_second_class)
    )

    # ---------------------------------------------------------
    # Survival rate by sex
    # ---------------------------------------------------------

    survival_by_sex = (
        df.groupby(
            "sex",
            observed=True
        )["survived"]
        .mean()
        .mul(100)
        .round(2)
    )

    print("\n--- SURVIVAL RATE BY SEX (%) ---")
    print(
        survival_by_sex.to_string()
    )

    # ---------------------------------------------------------
    # Survival rate by passenger class
    # ---------------------------------------------------------

    survival_by_pclass = (
        df.groupby(
            "pclass"
        )["survived"]
        .mean()
        .mul(100)
        .round(2)
    )

    print("\n--- SURVIVAL RATE BY PCLASS (%) ---")
    print(
        survival_by_pclass.to_string()
    )

    # ---------------------------------------------------------
    # Survival rate by sex + passenger class
    # ---------------------------------------------------------

    survival_by_sex_pclass = (
        df.groupby(
            ["sex", "pclass"],
            observed=True
        )["survived"]
        .mean()
        .mul(100)
        .round(2)
    )

    print(
        "\n--- SURVIVAL RATE BY SEX + PCLASS (%) ---"
    )

    print(
        survival_by_sex_pclass.to_string()
    )


# -------------------------------------------------------------
# Correlation analysis
# -------------------------------------------------------------

def analyze_correlations(
    df: pd.DataFrame
) -> None:
    """
    Calculate the required six-column correlation matrix.

    Required columns:
    - survived
    - pclass
    - age
    - sibsp
    - parch
    - fare

    adult_male and alone are intentionally excluded.
    """

    correlation_columns = [
        "survived",
        "pclass",
        "age",
        "sibsp",
        "parch",
        "fare"
    ]

    # Calculate correlations using exactly the required
    # six numeric variables.
    correlation_matrix = (
        df[correlation_columns]
        .corr()
    )

    print("\n--- CORRELATION MATRIX ---")

    print(
        correlation_matrix
        .round(4)
        .to_string()
    )

    # ---------------------------------------------------------
    # Save correlation matrix
    # ---------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    correlation_matrix.to_csv(
        OUTPUT_DIR / "correlation_matrix.csv"
    )

    # ---------------------------------------------------------
    # Find two strongest absolute off-diagonal correlations.
    # ---------------------------------------------------------

    absolute_matrix = (
        correlation_matrix
        .abs()
    )

    # Ignore the diagonal.
    #
    # We intentionally use pandas .loc instead of
    # np.fill_diagonal() because the underlying NumPy array
    # can be read-only with some pandas/NumPy combinations.
    for column in absolute_matrix.columns:
        absolute_matrix.loc[
            column,
            column
        ] = float("nan")

    correlation_pairs = (
        absolute_matrix
        .stack()
        .sort_values(
            ascending=False
        )
    )

    selected_pairs = []
    seen_pairs = set()

    for (
        column_a,
        column_b
    ), absolute_value in correlation_pairs.items():

        # frozenset makes A-B and B-A equivalent.
        pair = frozenset(
            [column_a, column_b]
        )

        if pair in seen_pairs:
            continue

        seen_pairs.add(pair)

        selected_pairs.append(
            (
                (column_a, column_b),
                absolute_value
            )
        )

        if len(selected_pairs) == 2:
            break

    print(
        "\n--- TWO STRONGEST ABSOLUTE "
        "OFF-DIAGONAL CORRELATIONS ---"
    )

    for (
        (column_a, column_b),
        absolute_value
    ) in selected_pairs:

        actual_value = correlation_matrix.loc[
            column_a,
            column_b
        ]

        print(
            f"{column_a} vs {column_b}: "
            f"{actual_value:.4f} "
            f"(absolute = {absolute_value:.4f})"
        )

    # ---------------------------------------------------------
    # Correlation heatmap
    # ---------------------------------------------------------

    plt.figure(
        figsize=(8, 6)
    )

    plt.imshow(
        correlation_matrix,
        interpolation="nearest"
    )

    plt.colorbar()

    plt.xticks(
        range(len(correlation_columns)),
        correlation_columns,
        rotation=45,
        ha="right"
    )

    plt.yticks(
        range(len(correlation_columns)),
        correlation_columns
    )

    plt.title(
        "Titanic Correlation Matrix"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "correlation_heatmap.png",
        dpi=150
    )

    plt.close()

def create_survival_by_sex_pclass_chart(
    df: pd.DataFrame
) -> None:
    """
    Create a multivariate chart showing survival rate
    by sex and passenger class.
    """

    survival_rates = (
        df.groupby(
            ["sex", "pclass"],
            observed=True
        )["survived"]
        .mean()
        .mul(100)
        .reset_index(name="survival_rate")
    )

    plt.figure(figsize=(9, 6))

    for sex in survival_rates["sex"].unique():
        subset = survival_rates[
            survival_rates["sex"] == sex
        ]

        plt.plot(
            subset["pclass"],
            subset["survival_rate"],
            marker="o",
            label=sex
        )

    plt.title(
        "Survival Rate by Sex and Passenger Class"
    )

    plt.xlabel("Passenger Class")
    plt.ylabel("Survival Rate (%)")
    plt.xticks([1, 2, 3])
    plt.legend(title="Sex")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "survival_by_sex_pclass.png",
        dpi=150
    )

    plt.close()

    print("\n--- MULTIVARIATE CHART 1 ---")
    print(
        "Survival rate varies across both sex and "
        "passenger class. The chart shows the joint "
        "pattern rather than examining either variable alone."
    )


def create_age_fare_survival_chart(
    df: pd.DataFrame
) -> None:
    """
    Create a multivariate scatter plot showing the relationship
    between age, fare, and survival status.
    """

    plt.figure(figsize=(9, 6))

    for survival_status in sorted(
        df["survived"].unique()
    ):
        subset = df[
            df["survived"] == survival_status
        ]

        label = (
            "Survived"
            if survival_status == 1
            else "Did not survive"
        )

        plt.scatter(
            subset["age"],
            subset["fare"],
            alpha=0.5,
            label=label
        )

    plt.title(
        "Age, Fare, and Survival"
    )

    plt.xlabel("Age")
    plt.ylabel("Fare")
    plt.legend(title="Outcome")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "age_fare_survival.png",
        dpi=150
    )

    plt.close()

    print("\n--- MULTIVARIATE CHART 2 ---")
    print(
        "The chart compares passenger age and fare while "
        "separating observations by survival outcome. "
        "It helps identify whether survival patterns appear "
        "to vary across different age and fare ranges."
    )


def create_family_survival_chart(
    df: pd.DataFrame
) -> None:
    """
    Create a multivariate heatmap showing survival rate
    by number of siblings/spouses and parents/children.
    """

    survival_rates = (
        df.pivot_table(
            index="sibsp",
            columns="parch",
            values="survived",
            aggfunc="mean"
        )
        .mul(100)
    )

    plt.figure(figsize=(9, 6))

    plt.imshow(
        survival_rates,
        aspect="auto",
        interpolation="nearest"
    )

    plt.colorbar(
        label="Survival Rate (%)"
    )

    plt.xticks(
        range(len(survival_rates.columns)),
        survival_rates.columns
    )

    plt.yticks(
        range(len(survival_rates.index)),
        survival_rates.index
    )

    plt.xlabel(
        "Parents / Children Aboard"
    )

    plt.ylabel(
        "Siblings / Spouses Aboard"
    )

    plt.title(
        "Survival Rate by Family Relationships"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "family_survival_heatmap.png",
        dpi=150
    )

    plt.close()

    print("\n--- MULTIVARIATE CHART 3 ---")
    print(
        "The chart examines survival rates jointly across "
        "siblings/spouses and parents/children aboard. "
        "It helps reveal how survival varies across different "
        "family-relationship combinations."
    )

def create_family_size_fare_chart(
    df: pd.DataFrame
) -> None:
    """
    Create a multivariate scatter plot showing the relationship
    between family size, fare, and survival status.

    Family size is calculated as:
    sibsp + parch + 1
    """

    chart_df = df.copy()

    # Calculate total family size including the passenger.
    chart_df["family_size"] = (
        chart_df["sibsp"]
        + chart_df["parch"]
        + 1
    )

    plt.figure(figsize=(9, 6))

    for survival_status in sorted(
        chart_df["survived"].unique()
    ):
        subset = chart_df[
            chart_df["survived"] == survival_status
        ]

        label = (
            "Survived"
            if survival_status == 1
            else "Did not survive"
        )

        plt.scatter(
            subset["family_size"],
            subset["fare"],
            alpha=0.5,
            label=label
        )

    plt.title(
        "Family Size, Fare, and Survival"
    )

    plt.xlabel("Family Size")
    plt.ylabel("Fare")
    plt.legend(title="Outcome")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "family_size_fare_survival.png",
        dpi=150
    )

    plt.close()

    print("\n--- MULTIVARIATE CHART 4 ---")
    print(
        "The chart examines fare in relation to family size "
        "while separating passengers by survival outcome. "
        "It provides a combined view of family structure, "
        "ticket fare, and survival."
    )

# -------------------------------------------------------------
# Exploratory standardization
# -------------------------------------------------------------

def exploratory_standardization(df: pd.DataFrame) -> None:
    """
    Standardize Age and Fare for exploratory analysis only.

    The standardization is performed on the full cleaned dataset as
    required for exploratory analysis. These standardized columns are
    saved separately and are NOT used by the future ML modeling
    pipeline.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    standardized_df = df[["age", "fare"]].copy()

    for column in ["age", "fare"]:
        mean_value = standardized_df[column].mean()
        std_value = standardized_df[column].std()

        standardized_df[f"{column}_standardized"] = (
            standardized_df[column] - mean_value
        ) / std_value

    output_path = OUTPUT_DIR / "age_fare_standardized.csv"
    standardized_df.to_csv(output_path, index=False)

    print("\n--- EXPLORATORY STANDARDIZATION ---")
    print("Standardized columns: age, fare")
    print("Standardization scope: full cleaned dataset")
    print("Purpose: exploratory analysis only")
    print("Modeling pipeline usage: NOT USED")
    print(f"Saved standardized exploratory data to: {output_path}")

# -------------------------------------------------------------
# Main execution
# -------------------------------------------------------------

def main() -> None:
    """
    Run the Titanic exploratory analysis pipeline.

    All generated CSV and image outputs intentionally use
    deterministic filenames so rerunning this script safely
    regenerates the current results.
    """

    # Load the committed original Titanic CSV.
    df = load_data()

    print(
        f"Original shape: {df.shape}"
    )

    # Print the required original-dataset overview before cleaning.
    print_dataset_overview(df)

    # Clean the data according to the documented strategy.
    cleaned_df = clean_data(df)

    print(
        f"Cleaned shape: {cleaned_df.shape}"
    )

    print(
        "Remaining missing values:",
        cleaned_df.isna().sum().sum()
    )

    # Save the cleaned dataset.
    save_cleaned_data(
        cleaned_df
    )

    # Exploratory standardization is intentionally performed after
    # cleaning and is kept separate from the future ML pipeline.
    exploratory_standardization(cleaned_df)

    # Required EDA analyses.
    analyze_age_and_fare(
        cleaned_df
    )

    analyze_survival_patterns(
        cleaned_df
    )

    analyze_correlations(
        cleaned_df
    )

    create_survival_by_sex_pclass_chart(
        cleaned_df
    )

    create_age_fare_survival_chart(
        cleaned_df
    )

    create_family_survival_chart(
        cleaned_df
    )

    create_family_size_fare_chart(
        cleaned_df
    )

if __name__ == "__main__":
    main()