# Data Preparation

This document gives each data preparation action for the file `Data/diabetic_data.csv` and the reason for it. The actions follow the Data Preparation phase of CRISP-DM. The two scripts must run in sequence.

| | Step 1 | Step 2 |
| --- | --- | --- |
| Script | `ipynb/DataPrep/AlignNone.py` | `ipynb/DataPrep/02_remove_rows_and_columns.py` |
| Input | `Data/DataMainTable/diabetic_data.csv` | `Data/processed_diabetic_data.csv` |
| Output | `Data/processed_diabetic_data.csv` | `Data/cleaned_diabetic_data.csv` |
| Rows | 101,766 → 101,766 | 101,766 → 69,987 |
| Columns | 50 → 48 | 48 → 34 |

## Step 1: Clean values and labels

Step 1 does not remove rows. It makes the values clear and correct.

### 01. Mark missing values

**Action:** Change the `?` marker to an empty cell in all columns.

**Why:**

- The original file uses `?` when a value is not recorded.
- pandas reads `?` as normal text. Then `?` counts as a real category, and missing-value counts are wrong.
- An empty cell is the usual marker for a missing value. All tools read it correctly.

**Result:**

| Column | Missing values |
| --- | --- |
| weight | 98,569 |
| medical_specialty | 49,949 |
| payer_code | 40,256 |
| race | 2,273 |
| diag_3 | 1,423 |
| diag_2 | 358 |
| diag_1 | 21 |

### 02. Rename "No" in the drug columns

**Action:** In the 23 drug columns, change `No` to `Not_Prescribed`. The values `Steady`, `Up` and `Down` do not change.

**Why:**

- `No` is not clear. It can mean "no change" or "not given". In this data it means that the physician did not prescribe the drug.
- `Not_Prescribed` gives the correct meaning.
- The dose change (`Steady`, `Up`, `Down`) is kept, because a dose change can be a sign of a less stable patient.

**Result:** Example, `insulin`: Not_Prescribed 47,383, Steady 30,849, Down 12,218, Up 11,316.

### 03. Rename "None" in the lab test columns

**Action:** In `max_glu_serum` and `A1Cresult`, change `None` to `Not_Tested`.

**Why:**

- `None` means that the hospital did not do the test. This is real information, not a missing value.
- pandas reads the text `None` as a missing value by default. Then this information is lost.
- The source paper (Strack et al., 2014) found that "HbA1c measured or not" has a relation to readmission. Thus, we must keep this category.

**Result:**

| Column | Not_Tested | Test results |
| --- | --- | --- |
| max_glu_serum | 96,420 | Norm 2,597; >200 1,485; >300 1,264 |
| A1Cresult | 84,748 | >8 8,216; Norm 4,990; >7 3,812 |

### 04. Replace admission type codes with descriptions

**Action:** Replace the codes in `admission_type_id` with the descriptions from table 1 of `IDS_mapping.csv`. Codes 5 (Not Available), 6 (NULL) and 8 (Not Mapped) become empty cells.

**Why:**

- A number such as `1` has no meaning without the mapping file. `Emergency` is easy to read in tables and charts.
- A model must not use the codes as numbers. Code 3 is not "more" than code 1.
- Codes 5, 6 and 8 all mean "unknown". If they stay as three categories, they look like real admission types.

**Result:** Emergency 53,990; Elective 18,869; Urgent 18,480; Trauma Center 21; Newborn 10; empty (unknown) 10,396.

### 05. Replace discharge codes with short descriptions

**Action:** Replace the codes in `discharge_disposition_id` with short descriptions from table 2 of `IDS_mapping.csv`. Codes 18 (NULL), 25 (Not Mapped) and 26 (Unknown/Invalid) become empty cells.

**Why:**

- The original descriptions are very long, for example "Discharged/transferred to home with home health service". Short labels such as `Home Health Service` are easier to use in tables and charts.
- The short labels keep the meaning. Standard abbreviations stay: SNF (Skilled Nursing Facility), ICF (Intermediate Care Facility), AMA (Against Medical Advice).
- The labels that start with `Expired` or `Hospice` make the next step (remove stays that cannot have a readmission) easy.

**Result:** Home 60,234; SNF 13,954; Home Health Service 12,902; empty (unknown) 4,680.

### 06. Replace admission source codes with short descriptions

**Action:** Replace the codes in `admission_source_id` with short descriptions from table 3 of `IDS_mapping.csv`. Codes 9 and 15 (Not Available), 17 (NULL), 20 (Not Mapped) and 21 (Unknown/Invalid) become empty cells.

**Why:**

- The reasons are the same as for the admission type: readable labels, no false number order, and one marker for "unknown".
- Some descriptions in the mapping file start with a space or have a spelling error ("critial"). The new labels do not have these problems.

**Result:** Emergency Room 57,494; Physician Referral 29,565; Hospital Transfer 3,187; empty (unknown) 7,067.

### 07. Remove "_id" from the mapped column names

**Action:** Rename `admission_type_id` to `admission_type`, `discharge_disposition_id` to `discharge_disposition`, and `admission_source_id` to `admission_source`.

**Why:**

- After steps 04 to 06, these columns contain text, not ID codes. The name `_id` is then not correct.
- `encounter_id` and `patient_nbr` keep their names, because they are still real IDs.

**Result:** 3 columns renamed.

### 08. Drop columns with no data

**Action:** Drop each column that is empty or that has the same value in all rows. In this data, these columns are `examide` and `citoglipton`.

**Why:**

- `examide` and `citoglipton` are `Not_Prescribed` in all 101,766 rows.
- A column with only one value gives no information to an analysis or a model. It only makes the table larger.
- The script finds these columns from the data. Thus, it also finds new columns of this type after filters.

**Result:** 50 columns become 48 columns.

## Step 2: Remove rows and columns

Step 2 removes the rows and columns that are not correct or not useful for a readmission model.

### 09. Remove stays that end in death or hospice

**Action:** Remove the stays where `discharge_disposition` starts with `Expired` or `Hospice`.

**Why:**

- A patient who died cannot go back into hospital. A patient in hospice care will possibly not go back into hospital.
- If these stays stay in the data, they look like "no readmission". This gives the model false examples.
- The source paper (Strack et al., 2014) also removed these stays.

**Result:** 2,423 stays removed (Expired 1,652; Hospice 771).

### 10. Keep only the first stay of each patient

**Action:** Sort by `encounter_id`. Keep the first stay of each `patient_nbr` and remove the other stays.

**Why:**

- 16,773 patients have more than one stay. One patient has 40 stays.
- Stays of the same patient are not independent. Many statistical tests and models need independent rows.
- If one patient is in the training set and the test set, the test results are too good.
- The file has no dates. The lowest `encounter_id` is the usual replacement for "the first stay". The source paper also used only the first stay of each patient.

**Result:** 29,353 repeat stays removed. Early readmissions (`<30`) go from 11.2% to 9.0% of the rows.

### 11. Remove stays with unknown gender

**Action:** Remove the stays where `gender` is `Unknown/Invalid`.

**Why:**

- Only 3 stays have this value. This is too small to be a useful category.
- If the category stays, an encoded model gets one extra column with almost no data.

**Result:** 3 stays removed.

### 12. Drop weight and payer_code

**Action:** Drop the columns `weight` and `payer_code`.

**Why:**

- `weight` is 97% missing. It is not possible to fill this many values correctly.
- `payer_code` is 40% missing. It shows who paid for the stay, not the health of the patient. The meanings of some codes are not certain.
- The source paper also removed these two columns.

**Result:** 2 columns dropped.

### 13. Group medical_specialty

**Action:** Change empty values in `medical_specialty` to `Unknown`. Keep the 10 most frequent specialties. Change all other specialties to `Other`.

**Why:**

- `medical_specialty` is 49% missing, but the missing values can have a relation to readmission. Thus, `Unknown` is kept as a category, and the column is not dropped.
- There are 72 specialties. Many of them have very few stays. Small categories make a model unstable and give many encoded columns.
- The source paper also kept `Unknown` as a category and grouped the specialties.

**Result:** Unknown 33,652; InternalMedicine 10,641; Other 5,487; Family/GeneralPractice 4,978; Emergency/Trauma 4,393; Cardiology 4,207. The number of specialties to keep is set by `TOP_SPECIALTIES` in the script.

### 14. Merge rare drugs into one column

**Action:** Find the drugs that are prescribed in less than 1% of the stays. Make one new column, `other_drugs` (`Prescribed` or `Not_Prescribed`). Then drop the rare drug columns.

**Why:**

- Many drug columns are almost always `Not_Prescribed`. For example, `acetohexamide` is prescribed in 1 stay.
- Columns with almost no data give no reliable information. They also make the model larger.
- The new column keeps the information that the patient got a less frequent drug.

**Result:** 13 rare drugs merged. 8 drugs keep their own column: metformin, repaglinide, glimepiride, glipizide, glyburide, pioglitazone, rosiglitazone and insulin. `other_drugs` is `Prescribed` in 1,327 stays. The limit is set by `RARE_DRUG_THRESHOLD` in the script.

## Summary
After all actions, early readmissions (`<30`) are 9.0% of the rows. The model must take this class imbalance into account.

## References

- UCI Machine Learning Repository, "Diabetes 130-US Hospitals for Years 1999-2008": https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008
- Strack B. et al. (2014), "Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records", BioMed Research International: https://doi.org/10.1155/2014/781670
