# Module 2 — Titanic Analytics, Exploratory Data Analysis & Machine Learning

## 1. Module Overview

Module 2 uses the Titanic dataset to perform:

* Exploratory Data Analysis (EDA)
* Missing-value analysis and cleaning
* Outlier analysis
* Survival analysis
* Correlation analysis
* Multivariate visualization
* Exploratory feature standardization
* Leakage-safe machine-learning preprocessing
* Binary classification
* Class-imbalance experiments
* Random Forest hyperparameter tuning
* Multivariate linear regression
* Model persistence and raw-input prediction

The module uses the Titanic dataset loaded from Seaborn **once** and then works from the committed local CSV for all subsequent analysis and modeling.

---

## 2. Dataset

The Titanic dataset is loaded once by:

```text
analytics/src/data_loader.py
```

and immediately saved as:

```text
analytics/data/titanic.csv
```

### Original Dataset

| Property   |                        Value |
| ---------- | ---------------------------: |
| Rows       |                          891 |
| Columns    |                           15 |
| Source     |      Seaborn Titanic dataset |
| Local copy | `analytics/data/titanic.csv` |

All subsequent EDA and ML code reads the local CSV rather than calling `sns.load_dataset()` again.

---

## 3. Running Module 2

Activate the project virtual environment first.

From the repository root:

### Step 1 — Save the Titanic dataset

```powershell
python analytics\src\data_loader.py
```

### Step 2 — Run EDA

```powershell
python analytics\src\eda.py
```

### Step 3 — Validate ML preprocessing

```powershell
python analytics\src\preprocessing.py
```

If direct execution produces no console output in a particular Windows/Python invocation, the validation function can also be called explicitly:

```powershell
python -c "import analytics.src.preprocessing as p; p.main()"
```

### Step 4 — Run baseline classifiers

```powershell
python analytics\src\classification.py
```

### Step 5 — Run imbalance experiments and Random Forest tuning

```powershell
python analytics\src\classification_tuning.py
```

### Step 6 — Run regression

```powershell
python analytics\src\regression.py
```

### Step 7 — Verify model persistence

```powershell
python analytics\src\model_persistence.py
```

---

# 4. Exploratory Data Analysis

## Dataset inspection

The EDA reports:

* `df.shape`
* `df.info()`
* `df.describe()`
* Missing-value counts
* Missing-value percentages

Original dataset:

```text
Rows: 891
Columns: 15
Shape: (891, 15)
```

---

## 5. Missing-Value Analysis

The original dataset contains missing values in four columns.

| Column        | Missing | Percentage | Treatment          |
| ------------- | ------: | ---------: | ------------------ |
| `age`         |     177 |     19.87% | Median imputation  |
| `embarked`    |       2 |      0.22% | Drop affected rows |
| `deck`        |     688 |     77.22% | Drop column        |
| `embark_town` |       2 |      0.22% | Drop affected rows |

### Cleaning strategy

### Age

`age` has 19.87% missing values.

Because this falls within the 5–30% missingness range, missing ages are replaced with the median of the available Age values.

### Embarked

`embarked` has only 2 missing values, or 0.22%.

Because this is below 5%, the affected rows are removed.

### Embark Town

`embark_town` also has 2 missing values, or 0.22%.

The affected rows are removed using the same low-missingness rule.

### Deck

`deck` has approximately 77.22% missing values.

Because the missingness is very high, the column is dropped rather than attempting to impute such a large proportion.

### Cleaned result

```text
Rows: 889
Columns: 14
Remaining missing values: 0
```

Saved to:

```text
analytics/data/titanic_cleaned.csv
```

---

# 6. Age and Fare Analysis

Generated visualizations:

```text
analytics/outputs/age_histogram.png
analytics/outputs/fare_histogram.png
analytics/outputs/age_boxplot.png
analytics/outputs/fare_boxplot.png
```

## IQR outlier counts

| Variable | IQR Outliers |
| -------- | -----------: |
| Age      |           65 |
| Fare     |          114 |

The IQR method identifies observations below:

```text
Q1 - 1.5 × IQR
```

or above:

```text
Q3 + 1.5 × IQR
```

as potential outliers.

The outliers are retained for exploratory analysis rather than automatically removed.

---

# 7. Fare Statistics

| Statistic |   Value |
| --------- | ------: |
| Mean      | 32.0967 |
| Median    | 14.4542 |
| Mode      |  8.0500 |

The ordering:

```text
Mean > Median > Mode
```

indicates a right-skewed Fare distribution.

---

# 8. Boolean Masking

The analysis demonstrates both `&` and `|`.

### AND

Female passengers in first class:

```python
(df["sex"] == "female") & (df["pclass"] == 1)
```

Result:

```text
92 passengers
```

### OR

Passengers in first or second class:

```python
(df["pclass"] == 1) | (df["pclass"] == 2)
```

Result:

```text
398 passengers
```

---

# 9. Survival Analysis

## Survival by sex

| Sex    | Survival Rate |
| ------ | ------------: |
| Female |        74.04% |
| Male   |        18.89% |

## Survival by passenger class

| Passenger Class | Survival Rate |
| --------------: | ------------: |
|               1 |        62.62% |
|               2 |        47.28% |
|               3 |        24.24% |

## Survival by sex and passenger class

| Sex    | Class | Survival Rate |
| ------ | ----: | ------------: |
| Female |     1 |        96.74% |
| Female |     2 |        92.11% |
| Female |     3 |        50.00% |
| Male   |     1 |        36.89% |
| Male   |     2 |        15.74% |
| Male   |     3 |        13.54% |

These are descriptive statistics from the Titanic dataset and are not causal conclusions.

---

# 10. Correlation Analysis

The required correlation matrix contains exactly:

```text
survived
pclass
age
sibsp
parch
fare
```

`adult_male` and `alone` are intentionally excluded.

## Correlation matrix

```text
            survived  pclass     age   sibsp   parch    fare
survived    1.0000 -0.3355 -0.0698 -0.0340  0.0832  0.2553
pclass     -0.3355  1.0000 -0.3365  0.0817  0.0168 -0.5482
age        -0.0698 -0.3365  1.0000 -0.2325 -0.1715  0.0937
sibsp      -0.0340  0.0817 -0.2325  1.0000  0.4145  0.1609
parch       0.0832  0.0168 -0.1715  0.4145  1.0000  0.2175
fare        0.2553 -0.5482  0.0937  0.1609  0.2175  1.0000
```

The two strongest absolute off-diagonal correlations are:

1. `pclass` vs `fare`: **-0.5482**
2. `sibsp` vs `parch`: **+0.4145**

Correlation describes linear association and does not establish causation.

Outputs:

```text
analytics/outputs/correlation_matrix.csv
analytics/outputs/correlation_heatmap.png
```

---

# 11. Multivariate Visualizations

Four multivariate visualizations are generated.

### Chart 1 — Survival Rate by Sex and Passenger Class

```text
analytics/outputs/survival_by_sex_pclass.png
```

The chart examines survival jointly across sex and passenger class. The combined groups show substantial differences in observed survival rates.

### Chart 2 — Age, Fare, and Survival

```text
analytics/outputs/age_fare_survival.png
```

The scatter plot combines age and fare while distinguishing observations according to survival outcome. It provides a multivariate view of survival across age and fare.

### Chart 3 — Family Relationships and Survival

```text
analytics/outputs/family_survival_heatmap.png
```

The heatmap examines survival jointly across `sibsp` and `parch`. Some combinations contain relatively few observations, so rates in small cells should be interpreted cautiously.

### Chart 4 — Family Size, Fare, and Survival

```text
analytics/outputs/family_size_fare_survival.png
```

Family size is calculated as:

```text
sibsp + parch + 1
```

The chart combines family size, fare, and survival outcome.

Written interpretations for all four charts are maintained in:

```text
analytics/outputs/eda_interpretations.md
```

---

# 12. Exploratory Standardization

Age and Fare are standardized on the **full cleaned dataset** for exploratory analysis.

Output:

```text
analytics/outputs/age_fare_standardized.csv
```

Columns:

```text
age_standardized
fare_standardized
```

This standardization is exploratory only.

It is **not used as input to the machine-learning pipeline**.

The modeling pipeline independently fits transformations on the training data to prevent data leakage.

---

# 13. Machine-Learning Preprocessing

The modeling stage reads:

```text
analytics/data/titanic.csv
```

rather than repeatedly loading the dataset from Seaborn.

## Modeling features

```text
pclass
sex
age
sibsp
parch
fare
embarked
```

Target:

```text
survived
```

The following columns are intentionally excluded from the modeling features:

```text
alive
class
who
adult_male
alone
deck
embark_town
```

This avoids target leakage and redundant representations.

## Train/test split

The split uses:

```text
test_size = 0.20
random_state = 42
stratify = y
```

Results:

```text
Training rows: 712
Testing rows: 179
```

Class distribution:

| Dataset  | Did Not Survive | Survived |
| -------- | --------------: | -------: |
| Overall  |          61.62% |   38.38% |
| Training |          61.66% |   38.34% |
| Testing  |          61.45% |   38.55% |

The close distributions demonstrate that the stratified split preserved the target proportions.

---

# 14. Training-Only Preprocessing

The preprocessing configuration is:

### Numeric features

```text
pclass
age
sibsp
parch
fare
```

Pipeline:

```text
Median imputation → StandardScaler
```

### Categorical features

```text
sex
embarked
```

Pipeline:

```text
Most-frequent imputation → OneHotEncoder
```

The preprocessing transformer is **not fitted in `preprocessing.py`**.

Each model pipeline fits preprocessing using the training data only.

This prevents test-set information from influencing preprocessing parameters.

---

# 15. Classification Models

Three baseline classifiers were trained on the same stratified train/test split:

1. Logistic Regression
2. Decision Tree
3. Random Forest

## Baseline results

| Model               | Accuracy | Precision | Recall |     F1 | ROC-AUC |
| ------------------- | -------: | --------: | -----: | -----: | ------: |
| Logistic Regression |   0.8045 |    0.7931 | 0.6667 | 0.7244 |  0.8437 |
| Decision Tree       |   0.8156 |    0.7903 | 0.7101 | 0.7481 |  0.7904 |
| Random Forest       |   0.8156 |    0.8000 | 0.6957 | 0.7442 |  0.8300 |

The results demonstrate that accuracy alone does not fully describe model behavior because precision, recall, F1, and ROC-AUC differ across the models.

---

# 16. Classification Outputs

Generated classification outputs:

```text
analytics/outputs/classification/
├── classifier_comparison.csv
├── class_balance.png
├── confusion_matrix_decision_tree.png
├── confusion_matrix_logistic_regression.png
├── confusion_matrix_random_forest.png
├── decision_tree.png
├── imbalance_comparison.csv
└── roc_curves.png
```

The decision-tree visualization uses the transformed feature names and class names.

---

# 17. Class Imbalance Analysis

The training data contains:

```text
Did not survive: 549
Survived:        342
```

Three Random Forest approaches were compared:

* Baseline
* `class_weight="balanced"`
* SMOTE

## Imbalance comparison

| Approach    | Accuracy | Precision | Recall |     F1 | ROC-AUC |
| ----------- | -------: | --------: | -----: | -----: | ------: |
| RF Baseline |   0.8156 |    0.8000 | 0.6957 | 0.7442 |  0.8300 |
| RF Balanced |   0.8045 |    0.7500 | 0.7391 | 0.7445 |  0.8227 |
| RF SMOTE    |   0.8101 |    0.7612 | 0.7391 | 0.7500 |  0.8300 |

SMOTE is applied within the training pipeline so synthetic samples are not generated from the test set.

---

# 18. Random Forest Hyperparameter Tuning

GridSearchCV was used with 5-fold cross-validation.

Search parameters:

```text
n_estimators: [100, 200, 300]
max_depth: [None, 5, 10, 15]
max_features: ["sqrt", "log2"]
```

Scoring metric:

```text
ROC-AUC
```

## Best parameters

```text
max_depth     = 5
max_features = sqrt
n_estimators  = 200
```

Best cross-validation ROC-AUC:

```text
0.8721
```

## Tuned Random Forest test metrics

| Metric    |  Value |
| --------- | -----: |
| Accuracy  | 0.8101 |
| Precision | 0.8723 |
| Recall    | 0.5942 |
| F1        | 0.7069 |
| ROC-AUC   | 0.8465 |

Random Forest OOB score:

```text
0.8301
```

Outputs:

```text
analytics/outputs/tuning/rf_gridsearch_results.csv
analytics/outputs/tuning/rf_tuning_summary.csv
```

The complete fitted tuned pipeline is saved as:

```text
analytics/models/best_random_forest_pipeline.joblib
```

---

# 19. Final Classifier Comparison

The measured results show different trade-offs rather than a single universally superior metric profile.

The Decision Tree has the highest baseline accuracy and F1 among the three baseline classifiers, while Logistic Regression has the highest baseline ROC-AUC. The baseline Random Forest has the same accuracy as the Decision Tree and slightly higher precision, while SMOTE increases Random Forest recall and F1 relative to the baseline. The tuned Random Forest achieves the highest precision and a ROC-AUC of 0.8465 on the held-out test set, but its recall and F1 decrease substantially. Therefore, for this assignment's balanced evaluation of classification metrics, the **baseline Decision Tree provides the strongest overall baseline balance of accuracy, recall, and F1**, while Logistic Regression provides a strong ROC-AUC benchmark; the tuned Random Forest remains useful where higher precision is the primary requirement.

---

# 20. Multivariate Fare Regression

A multivariate Linear Regression model predicts:

```text
fare
```

using other available Titanic features.

The regression pipeline handles numeric and categorical features using training-only preprocessing.

## Regression metrics

| Metric                  |   Value |
| ----------------------- | ------: |
| MAE                     | 20.8977 |
| RMSE                    | 30.5328 |
| R²                      |  0.3975 |
| Adjusted R²             |  0.3617 |
| Test rows               |     179 |
| Features after encoding |      10 |

The R² value indicates that the selected predictors explain part, but not all, of the variation in Fare.

---

# 21. Residual Analysis

Residual plot:

```text
analytics/outputs/regression/residual_plot.png
```

The residual analysis shows evidence consistent with changing residual spread as predicted Fare increases, suggesting possible heteroscedasticity.

This indicates that the residual variance may not remain constant across the prediction range.

Regression interpretation:

```text
analytics/outputs/regression/regression_interpretation.md
```

Regression metrics:

```text
analytics/outputs/regression/regression_metrics.csv
```

---

# 22. Model Persistence

The complete fitted Random Forest pipeline is saved using Joblib:

```text
analytics/models/best_random_forest_pipeline.joblib
```

The persistence test reloads the complete pipeline and provides raw input:

```text
pclass    sex  age  sibsp  parch  fare embarked
1         female 30.0  0     0    80.0  S
```

The reloaded pipeline successfully performs preprocessing and prediction without requiring manual transformations.

Verified result:

```text
Predicted class: 1
Prediction label: Survived
Predicted survival probability: 0.9721
```

This demonstrates that preprocessing and the fitted model are persisted together.

---

# 23. Source Code

Current Module 2 source files:

```text
analytics/src/
├── data_loader.py
├── eda.py
├── preprocessing.py
├── classification.py
├── classification_tuning.py
├── regression.py
└── model_persistence.py
```

### `data_loader.py`

Loads the Titanic dataset from Seaborn once and saves the local CSV.

### `eda.py`

Performs dataset inspection, cleaning, EDA, survival analysis, correlation analysis, visualization, and exploratory standardization.

### `preprocessing.py`

Defines the modeling features, target, stratified split, and leakage-safe preprocessing configuration.

### `classification.py`

Trains and evaluates Logistic Regression, Decision Tree, and Random Forest models and generates classification outputs.

### `classification_tuning.py`

Performs class-imbalance experiments, SMOTE, Random Forest GridSearchCV, OOB evaluation, and saves the fitted Random Forest pipeline.

### `regression.py`

Trains the multivariate fare regression model and generates regression metrics and residual analysis.

### `model_persistence.py`

Reloads the saved fitted pipeline and verifies prediction using raw input data.

---

# 24. Generated Output Structure

```text
analytics/
├── data/
│   ├── titanic.csv
│   └── titanic_cleaned.csv
│
├── models/
│   └── best_random_forest_pipeline.joblib
│
├── outputs/
│   ├── age_boxplot.png
│   ├── age_fare_standardized.csv
│   ├── age_fare_survival.png
│   ├── age_histogram.png
│   ├── correlation_heatmap.png
│   ├── correlation_matrix.csv
│   ├── eda_interpretations.md
│   ├── family_size_fare_survival.png
│   ├── family_survival_heatmap.png
│   ├── fare_boxplot.png
│   ├── fare_histogram.png
│   ├── survival_by_sex_pclass.png
│   │
│   ├── classification/
│   │   ├── classifier_comparison.csv
│   │   ├── class_balance.png
│   │   ├── confusion_matrix_decision_tree.png
│   │   ├── confusion_matrix_logistic_regression.png
│   │   ├── confusion_matrix_random_forest.png
│   │   ├── decision_tree.png
│   │   ├── imbalance_comparison.csv
│   │   └── roc_curves.png
│   │
│   ├── tuning/
│   │   ├── rf_gridsearch_results.csv
│   │   └── rf_tuning_summary.csv
│   │
│   └── regression/
│       ├── regression_interpretation.md
│       ├── regression_metrics.csv
│       └── residual_plot.png
│
└── src/
    ├── data_loader.py
    ├── eda.py
    ├── preprocessing.py
    ├── classification.py
    ├── classification_tuning.py
    ├── regression.py
    └── model_persistence.py
```

---

# 25. Rerun and Overwrite Behavior

The Module 2 scripts use deterministic output filenames.

Running the scripts again regenerates the corresponding datasets, analysis outputs, model outputs, and persisted model.

Directories are created when required, and deterministic output files are overwritten rather than appended.

The pipeline therefore supports repeatable execution without manually deleting previous generated files.

Python cache directories such as:

```text
__pycache__/
```

are excluded through the repository `.gitignore`.

---

# 26. Module 2 Completion Checklist

### Dataset and EDA

* [x] Titanic dataset loaded once with Seaborn
* [x] Original CSV saved immediately
* [x] Subsequent analysis uses local CSV
* [x] `df.info()`
* [x] `df.describe()`
* [x] `df.shape`
* [x] Missing-value percentages
* [x] Missing-value treatment based on required thresholds
* [x] Cleaned dataset saved
* [x] Age histogram
* [x] Fare histogram
* [x] Age boxplot
* [x] Fare boxplot
* [x] IQR outlier counts
* [x] Fare mean, median, and mode
* [x] Fare skewness interpretation
* [x] Boolean masking with `&`
* [x] Boolean masking with `|`
* [x] Survival by sex
* [x] Survival by passenger class
* [x] Survival by sex and passenger class
* [x] Required six-column correlation matrix
* [x] Correlation heatmap
* [x] Two strongest absolute correlations
* [x] Four multivariate charts
* [x] Written interpretations for all four charts
* [x] Exploratory Age/Fare standardization

### Machine Learning

* [x] Stratified train/test split
* [x] Training-only preprocessing
* [x] Numeric missing-value preprocessing
* [x] Categorical missing-value preprocessing
* [x] Sex encoding
* [x] Embarked encoding
* [x] Numeric scaling
* [x] Logistic Regression
* [x] Decision Tree
* [x] Random Forest
* [x] Decision Tree visualization
* [x] Confusion matrices
* [x] Accuracy
* [x] Precision
* [x] Recall
* [x] F1
* [x] ROC-AUC
* [x] Class-balance analysis
* [x] Baseline vs balanced comparison
* [x] SMOTE comparison
* [x] Random Forest GridSearchCV
* [x] Best hyperparameters
* [x] Random Forest OOB score
* [x] Final classifier comparison
* [x] Metric-based classifier recommendation

### Regression

* [x] Multivariate fare regression
* [x] MAE
* [x] RMSE
* [x] R²
* [x] Adjusted R²
* [x] Residual plot
* [x] Heteroscedasticity analysis
* [x] Heteroscedasticity conclusion

### Model Persistence

* [x] Complete fitted pipeline saved with Joblib
* [x] Pipeline successfully reloaded
* [x] Raw input passed directly to reloaded pipeline
* [x] Prediction successfully generated
* [x] Prediction probability successfully generated

---

# 27. Verification Status

Module 2 source files were syntax-checked successfully using `py_compile`.

The following scripts were executed successfully:

```text
preprocessing.py
classification.py
classification_tuning.py
regression.py
model_persistence.py
```

The EDA stage and generated artifacts were also verified.

Module 2 is therefore **implemented and execution-verified**, with generated datasets, visualizations, model evaluation outputs, regression outputs, and a persisted fitted pipeline.
