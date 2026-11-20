# Predicting 30-Day Hospital Readmission for Diabetic Patients

Data Analytics CA2 project, following the CRISP-DM methodology. The model ranks discharged diabetic patients by their risk of readmission within 30 days, so discharge-planning staff can choose who gets targeted follow-up care.

- **Dataset:** Diabetes 130-US Hospitals for Years 1999–2008 (Clore et al., 2014), UCI Machine Learning Repository, CC BY 4.0. <https://doi.org/10.24432/C5230J>
- **Source paper:** Strack et al. (2014), BioMed Research International. <https://doi.org/10.1155/2014/781670>
- **Deadline:** Friday 4 December 2026

## Project status

| CRISP-DM phase | Status | Location |
| --- | --- | --- |
| Business Understanding | In progress | `Worksheets/Understanding_the_Problem.md` |
| Data Understanding | Data dictionary, data checks and visit analysis done | `Data/DataMainTable/Data_Dictionary_and_Mapping_Guide.md`, `NoteBooks/` |
| Data Preparation | Cleaning done; target column and ICD-9 grouping to do | `py/DataPrep/` |
| Modelling | Not started | |
| Evaluation | Not started | |
| Deployment (paper) | Sections 1–3 in progress | `Paper/CA2_Research_Report.md` |

## Software

| Software | Purpose |
| --- | --- |
| [IntelliJ IDEA](https://www.jetbrains.com/idea/) (2025.3 or later, unified edition) | Main IDE for notebooks, Python code, Markdown and Git |
| [Python](https://www.python.org/downloads/) 3.12 or later (developed on 3.15) | Programming language for the analysis |
| Python virtual environment (`venv`) | Isolated, reproducible set of packages for this project |
| [Jupyter](https://jupyter.org/) | Notebook environment, run inside IntelliJ |
| [Git](https://git-scm.com/) | Version control |
| [GitHub](https://github.com/JanArnoCoetzer/Data-Analytics-diabetes-readmission) | Remote repository for submission |

The Ultimate subscription is free for students through the [JetBrains educational licence](https://www.jetbrains.com/community/education/#students). Use it if notebook features are not available in the free version of IntelliJ IDEA.

| Step | Script | Input | Output | Rows × columns |
| --- | --- | --- | --- | --- |
| 1. Clean values and labels | `1.clean_missing_and_categories.py` | `Data/DataMainTable/diabetic_data.csv` | `Data/processed_diabetic_data.csv` | 101,766 × 48 |
| 2. Remove rows and columns | `2.remove_rows_and_columns.py` | `Data/processed_diabetic_data.csv` | `Data/cleaned_diabetic_data.csv` | 69,987 × 34 |

**Step 1** changes `?` to an empty cell, `No` in the drug columns to `Not_Prescribed`, and `None` in the lab test columns to `Not_Tested`. It replaces the admission type, discharge disposition and admission source codes with short descriptions (unknown codes become empty) and removes `_id` from those column names. It also drops columns with no data (`examide`, `citoglipton`).

**Step 2** removes stays that end in death or hospice, keeps only the first stay of each patient, and removes unknown gender. It drops `weight` and `payer_code`, groups `medical_specialty` (top 10, `Unknown`, `Other`), and merges rare drugs into `other_drugs`.

The cleaned file contains no `?` or `None` text. Empty cells are the only missing values, so the default `read_csv` settings are correct. To load the original file, use `keep_default_na=False, na_values=["?"]`, or the value `None` ("test not done") becomes a missing value.

## Notebooks

Run the data preparation scripts first. Then open a notebook in IntelliJ IDEA and use **Restart Kernel → Run All**. Each notebook finds the repository root from the location of `ReadMe.md`.

| Notebook | Purpose |
| --- | --- |
| `NoteBooks/DataCheck.ipynb` | Checks the raw and cleaned data: shapes, missing values, target distribution, cohort steps and readmission rate by category. Ends with a summary of all checks |
| `NoteBooks/VisitsVsReadmission.ipynb` | Exploratory check: do patients with more hospital visits have a higher 30-day readmission rate? Compares each visit group with the average rate. Saves charts to `Paper/figures/` |

**Main result of the visit analysis (training data, average 9.0%):** patients with 3 or more inpatient visits in the year before have a 30-day readmission rate of 26.0% (2.9 × the average). Outpatient visits have almost no effect. The total number of encounters in the dataset is not a permitted model input, because it contains information from the future.

## Repository structure

```
Data/
  DataMainTable/
    diabetic_data.csv                     Original dataset (101,766 encounters, 50 columns)
    IDS_mapping.csv                       Lookup tables for admission and discharge IDs
    Data_Dictionary_and_Mapping_Guide.md  Column definitions and mapping guide
  processed_diabetic_data.csv             Output of data preparation step 1
  cleaned_diabetic_data.csv               Output of data preparation step 2
NoteBooks/
  DataCheck.ipynb                         Data checks and summary
  VisitsVsReadmission.ipynb               Exploratory check: prior visits and readmission
py/
  DataPrep/
    1.clean_missing_and_categories.py     Data preparation step 1
    2.remove_rows_and_columns.py          Data preparation step 2
    Data_Preparation.md                   Each preparation action and the reason for it
Paper/
  figures/                                Charts saved by the notebooks
  Topic_Proposal.md                       Topic selection and reasoning
  CA2_Research_Report.md                  Four-page conference-style paper
Worksheets/
  Understanding_the_Problem.md            Business Understanding worksheet
ReadMe.md                                 This file


## Models to concider
-random forest decision tree
-Support Vector Machine 
-logstic regression
