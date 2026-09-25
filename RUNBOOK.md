# Zepto Masai Capstone Project — Runbook

This runbook explains how to set up, execute, verify, and troubleshoot all three modules of the Zepto Masai capstone project.

## 1. Prerequisites

Install:

- Python 3.12+
- Git
- Docker Desktop (required only for Docker validation)
- Internet connection for initial Python package installation and Module 3 embedding-model download

Verify Python:

```powershell
python --version
```

Verify Git:

```powershell
git --version
```

Verify Docker:

```powershell
docker --version
```

Docker is not required to run Modules 1 and 2 locally.

---

## 2. Clone the Repository

```powershell
git clone https://github.com/NiranjanChitturi/Capstone_Project_Zepto_Masai.git
cd Capstone_Project_Zepto_Masai
```

---

## 3. Create and Activate Virtual Environment

Create the environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Install Python Dependencies

Install all project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Optional import verification:

```powershell
python -c "import pandas, numpy, sklearn, requests, bs4, seaborn, matplotlib, chromadb, sentence_transformers, langgraph, fastapi, pydantic; print('All required imports passed.')"
```

---

# Module 1 — Data Pipeline

## 5. Run Module 1

Run the complete data pipeline from the repository root:

```powershell
python -m data_pipeline.src.pipeline
```

The pipeline performs:

1. Web scraping
2. Data cleaning
3. SQLite database loading
4. SQL analysis
5. Pandas/JOIN verification
6. Final validation

The verified run produced:

```text
Books: 93
Categories: 3
Required minimum books: 60 -> PASS
Required minimum categories: 3 -> PASS
```

### Module 1 output locations

Raw data:

```text
data_pipeline/data/raw/books_raw.csv
```

Cleaned data:

```text
data_pipeline/data/processed/books_cleaned.csv
```

SQLite database:

```text
data_pipeline/data/database/books.db
```

SQL analysis outputs:

```text
data_pipeline/data/outputs/
```

---

# Module 2 — Analytics and Machine Learning

## 6. Load Titanic Dataset

Run:

```powershell
python analytics\src\data_loader.py
```

Expected verified output:

```text
Titanic dataset saved to: analytics\data\titanic.csv
Rows: 891
Columns: 15
```

The dataset is loaded using Seaborn once and saved locally. Subsequent analytics use the local CSV.

---

## 7. Run Exploratory Data Analysis

Run:

```powershell
python analytics\src\eda.py
```

This performs:

- Dataset shape
- Dataset information
- Descriptive statistics
- Missing-value analysis
- Missing-value treatment
- Histograms
- Boxplots
- IQR outlier analysis
- Fare statistics
- Boolean-mask analysis
- Survival analysis
- Correlation matrix
- Correlation heatmap
- Multivariate visualizations
- Exploratory standardization

Cleaned dataset:

```text
analytics/data/titanic_cleaned.csv
```

EDA outputs:

```text
analytics/outputs/
```

---

## 8. Run ML Preprocessing

Run:

```powershell
python analytics\src\preprocessing.py
```

The preprocessing workflow performs:

- Feature/target separation
- Stratified train/test split
- Numeric median imputation
- Numeric standardization
- Categorical most-frequent imputation
- One-hot encoding
- Target leakage validation

The preprocessor is fitted through the model pipelines rather than being fitted on the complete dataset.

---

## 9. Run Baseline Classification

Run:

```powershell
python analytics\src\classification.py
```

Models:

- Logistic Regression
- Decision Tree
- Random Forest

Metrics:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC

Classification outputs:

```text
analytics/outputs/classification/
```

---

## 10. Run Imbalance Experiments and Random Forest Tuning

Run:

```powershell
python analytics\src\classification_tuning.py
```

This evaluates:

- Random Forest baseline
- Class-balanced Random Forest
- SMOTE Random Forest
- Random Forest GridSearchCV

The GridSearchCV searches:

- `n_estimators`
- `max_depth`
- `max_features`

The Random Forest uses:

```text
oob_score=True
```

The fitted tuned pipeline is saved as:

```text
analytics/models/best_random_forest_pipeline.joblib
```

---

## 11. Run Fare Regression

Run:

```powershell
python analytics\src\regression.py
```

Metrics:

- MAE
- RMSE
- R²
- Adjusted R²

The script also performs residual analysis and documents the heteroscedasticity conclusion.

Regression outputs:

```text
analytics/outputs/regression/
```

---

## 12. Validate Model Persistence

Run:

```powershell
python analytics\src\model_persistence.py
```

This:

1. Loads the saved Joblib pipeline
2. Creates a raw passenger input
3. Sends the raw input through the complete fitted pipeline
4. Produces a prediction
5. Produces the survival probability

The verified test produced:

```text
Predicted class: 1
Prediction label: Survived
Predicted survival probability: 0.9721
Model persistence validation completed successfully.
```

---

# Module 3 — Support Assistant

## 13. Build the Knowledge Base

Run:

```powershell
python -m support_assistant.src.ingest
```

This:

- Loads the eight required knowledge-base documents
- Chunks the documents
- Generates embeddings using `all-MiniLM-L6-v2`
- Stores the embeddings in ChromaDB
- Uses cosine similarity for retrieval

ChromaDB runtime data:

```text
support_assistant/data/chroma_db/
```

This directory is runtime-generated and ignored by Git.

---

## 14. Test Retrieval

Run:

```powershell
python -m support_assistant.src.retrieve
```

The retrieval test returns the top three matching knowledge-base documents.

---

## 15. Run the LangGraph Workflow

For deterministic grading/testing, enable the mock LLM:

```powershell
$env:MOCK_LLM="1"
```

Then run:

```powershell
python -m support_assistant.src.workflow
```

The workflow contains:

```text
classify_intent
        |
        +---- policy_question ----> retrieve_and_answer
        |
        +---- general_question ---> direct_answer
```

The policy path retrieves the top three knowledge-base documents.

The deterministic mock response uses the retrieved context.

The general-question path returns the fixed direct-answer response.

The current implementation uses the deterministic mock path for reproducible grading. An external real LLM is not required for the graded workflow.

---

## 16. Start the FastAPI Service

Enable deterministic mock mode:

```powershell
$env:MOCK_LLM="1"
```

Start the API:

```powershell
uvicorn support_assistant.src.api:app --host 0.0.0.0 --port 8000
```

Endpoint:

```text
POST /ask
```

FastAPI-generated interactive documentation is available while the service is running.

---

# Module 3 — Docker

## 17. Build the Docker Image

From the repository root:

```powershell
docker build -t zepto-support-assistant:latest .
```

---

## 18. Run the Docker Container

```powershell
docker run --rm -p 8000:8000 -e MOCK_LLM=1 zepto-support-assistant:latest
```

The service listens on:

```text
http://localhost:8000
```

The container performs knowledge-base ingestion during image construction.

---

# 19. Final Verification

After running the modules, check Git status:

```powershell
git status --short
```

Review changed/generated files before committing.

Check repository history:

```powershell
git log --oneline --graph --decorate --all
```

The project history should show the feature branch and merge into `main`.

Verify the current branch:

```powershell
git branch --show-current
```

Expected:

```text
main
```

---

# 20. Expected Project Structure

```text
Capstone_Project_Zepto_Masai/
│
├── analytics/
│   ├── data/
│   ├── models/
│   ├── outputs/
│   ├── src/
│   └── README.md
│
├── data_pipeline/
│   ├── data/
│   ├── src/
│   └── README.md
│
├── support_assistant/
│   ├── data/
│   ├── knowledge_base/
│   ├── src/
│   ├── docker-requirements.txt
│   └── README.md
│
├── Dockerfile
├── requirements.txt
├── RUNBOOK.md
└── README.md
```

---

# 21. Troubleshooting

## `ModuleNotFoundError`

Install the root dependencies again:

```powershell
python -m pip install -r requirements.txt
```

## Module 1 relative-import error

Run Module 1 as a Python module:

```powershell
python -m data_pipeline.src.pipeline
```

Do not run:

```powershell
python data_pipeline\src\pipeline.py
```

because Module 1 source files use package-relative imports.

## Module 3 mock mode

Enable deterministic mock mode:

```powershell
$env:MOCK_LLM="1"
```

Then:

```powershell
python -m support_assistant.src.workflow
```

## Rebuild the Chroma knowledge base

```powershell
python -m support_assistant.src.ingest
```

## Check Docker

```powershell
docker --version
```

Verify the image:

```powershell
docker images zepto-support-assistant
```

---

# 22. Recommended Execution Order

For a complete fresh validation:

```text
1. Install requirements
2. Module 1 pipeline
3. Module 2 data loader
4. Module 2 EDA
5. Module 2 preprocessing
6. Module 2 classification
7. Module 2 classification tuning
8. Module 2 regression
9. Module 2 model persistence
10. Module 3 ingestion
11. Module 3 retrieval
12. Module 3 workflow
13. Module 3 FastAPI
14. Module 3 Docker
15. Git status
16. Git history verification
```

---

# 23. Completion Criteria

The repository is ready for final submission when:

- All three modules execute successfully.
- Required generated datasets and artifacts are present.
- Module 1 produces at least 60 books across at least 3 categories.
- Module 2 completes EDA, classification, imbalance handling, tuning, regression, and model persistence.
- Module 3 completes ingestion, retrieval, LangGraph workflow, API, and Docker validation.
- README files document the implementation and design decisions.
- `RUNBOOK.md` documents reproducible execution.
- Git history contains the required feature-branch work and merge into `main`.
- `git status` has been reviewed before the final commit.
