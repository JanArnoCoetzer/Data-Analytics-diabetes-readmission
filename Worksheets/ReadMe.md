# Predicting 30-Day Hospital Readmission for Diabetic Patients

Data Analytics CA2 project, following the CRISP-DM methodology. The model ranks discharged diabetic patients by their risk of readmission within 30 days, so discharge-planning staff can choose who gets targeted follow-up care.

- **Dataset:** Diabetes 130-US Hospitals for Years 1999–2008 (Clore et al., 2014), UCI Machine Learning Repository, CC BY 4.0. <https://doi.org/10.24432/C5230J>
- **Source paper:** Strack et al. (2014), BioMed Research International. <https://doi.org/10.1155/2014/781670>
- **Deadline:** Friday 4 December 2026

## Software

| Software | Purpose |
| --- | --- |
| [IntelliJ IDEA](https://www.jetbrains.com/idea/) (2025.3 or later, unified edition) | Main IDE for notebooks, Python code, Markdown and Git |
| [Python](https://www.python.org/downloads/) 3.12 | Programming language for the analysis |
| Python virtual environment (`venv`) | Isolated, reproducible set of packages for this project |
| [Jupyter](https://jupyter.org/) | Notebook environment, run inside IntelliJ |
| [Git](https://git-scm.com/) | Version control |
| [GitHub](https://github.com/JanArnoCoetzer/Data-Analytics-diabetes-readmission) | Remote repository for submission |

The Ultimate subscription is free for students through the [JetBrains educational licence](https://www.jetbrains.com/community/education/#students). Use it if notebook features are not available in the free version of IntelliJ IDEA.

## IntelliJ IDEA plugins

| Plugin | Purpose |
| --- | --- |
| [Python](https://plugins.jetbrains.com/plugin/631-python) | Python language support, interpreter and virtual environment management, code completion and debugging |
| [Jupyter](https://plugins.jetbrains.com/plugin/22814-jupyter) | Create, run and debug `.ipynb` notebooks inside the IDE ([docs](https://www.jetbrains.com/help/idea/jupyter-notebook-support.html)) |
| Markdown (bundled) | Edit and preview the paper, worksheets and data dictionary |
| Git (bundled) | Commit, push and view history from the IDE |

## Python libraries

### Core

| Library | Use in this project |
| --- | --- |
| `pandas` | Load `diabetic_data.csv`, split `IDS_mapping.csv` into three lookup tables, clean data, group ICD-9 codes |
| `numpy` | Numerical operations |
| `matplotlib` | Plots for Data Understanding and the paper |
| `seaborn` | Statistical plots, for example readmission rate by feature |
| `scikit-learn` | Patient-level split, preprocessing pipelines, baseline and models, evaluation metrics |
| `jupyter` / `ipykernel` | Run notebooks in IntelliJ IDEA |

### Optional

| Library | Use in this project |
| --- | --- |
| `fairlearn` | Compare model performance across `race` and `payer_code` for the bias discussion |
| `imbalanced-learn` | Resampling (for example SMOTE) on the training data only, if class weights are not enough |
| `ydata-profiling` | Automatic data profile report as a check during Data Understanding |
| `shap` | Explain which features drive the predictions |

### scikit-learn components

| Component | Purpose |
| --- | --- |
| `GroupShuffleSplit`, `StratifiedGroupKFold` | Split by `patient_nbr` to prevent leakage between train and test |
| `Pipeline`, `ColumnTransformer`, `OneHotEncoder` | Apply the same preprocessing to train and test data |
| `DummyClassifier` | Baseline model |
| `LogisticRegression`, `DecisionTreeClassifier` | Classification models, with `class_weight='balanced'` |
| `recall_score`, `precision_score`, `average_precision_score` | Evaluation metrics suited to an 11% positive class |
| `PrecisionRecallDisplay`, `ConfusionMatrixDisplay` | Evaluation figures |

## Setup

1. Install IntelliJ IDEA, Python 3.15.2 and Git.
2. In IntelliJ IDEA, go to **Settings → Plugins** and install the **Python** and **Jupyter** plugins.
3. Clone the repository:
   ```bash
   git clone https://github.com/JanArnoCoetzer/Data-Analytics-diabetes-readmission.git
   ```
4. Create and activate a virtual environment in the project folder:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   ```
5. Install the libraries:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn jupyter ipykernel
   pip install fairlearn imbalanced-learn ydata-profiling shap   # optional
   ```
6. In IntelliJ IDEA, set `.venv` as the project interpreter (**File → Project Structure → SDK**).
7. Open or create a `.ipynb` file and run a cell. IntelliJ IDEA starts the Jupyter server automatically.

### Loading the data correctly

```python
import pandas as pd

df = pd.read_csv("Data/diabetic_data.csv", keep_default_na=False, na_values=["?"])
```

`keep_default_na=False` keeps the value `None` in `max_glu_serum` and `A1Cresult` as "test not done" instead of a missing value.

## Repository structure

```
Data/
  diabetic_data.csv                     Main dataset (101,766 encounters, 50 columns)
  IDS_mapping.csv                       Lookup tables for admission and discharge IDs
  Data_Dictionary_and_Mapping_Guide.md  Column definitions and mapping guide
Paper/
  Topic_Proposal.md                     Topic selection and reasoning
  CA2_Research_Report.md                Four-page conference-style paper
Worksheets/
  Understanding_the_Problem.md          Business Understanding worksheet
```
