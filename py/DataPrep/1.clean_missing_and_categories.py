from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = REPO_ROOT / "Data" / "DataMainTable" / "diabetic_data.csv"
OUTPUT_FILE = REPO_ROOT / "Data" / "processed_diabetic_data.csv"

# The 23 diabetes drug columns
DRUG_COLUMNS = [
    "metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride",
    "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone",
    "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide",
    "examide", "citoglipton", "insulin", "glyburide-metformin",
    "glipizide-metformin", "glimepiride-pioglitazone",
    "metformin-rosiglitazone", "metformin-pioglitazone",
]

# The 2 lab test columns
LAB_COLUMNS = ["max_glu_serum", "A1Cresult"]

# admission_type_id codes -> descriptions (table 1 in IDS_mapping.csv)
# Codes 5 (Not Available), 6 (NULL) and 8 (Not Mapped) mean unknown,

ADMISSION_TYPES = {
    1: "Emergency",
    2: "Urgent",
    3: "Elective",
    4: "Newborn",
    5: None,
    6: None,
    7: "Trauma Center",
    8: None,
}

# discharge_disposition_id codes -> short descriptions (table 2 in IDS_mapping.csv)
# Codes 18 (NULL), 25 (Not Mapped) and 26 (Unknown/Invalid) mean unknown,

DISCHARGE_DISPOSITIONS = {
    1: "Home",
    2: "Short Term Hospital",
    3: "SNF",                          # Skilled Nursing Facility
    4: "ICF",                          # Intermediate Care Facility
    5: "Other Inpatient Care",
    6: "Home Health Service",
    7: "Left AMA",                     # Against Medical Advice
    8: "Home IV Provider",
    9: "Admitted Inpatient",
    10: "Neonatal Aftercare",
    11: "Expired",
    12: "Outpatient Return",
    13: "Hospice Home",
    14: "Hospice Facility",
    15: "Swing Bed",
    16: "Outpatient Other Institution",
    17: "Outpatient This Institution",
    18: None,
    19: "Expired Home",
    20: "Expired Facility",
    21: "Expired Unknown Place",
    22: "Rehab Facility",
    23: "Long Term Care Hospital",
    24: "Medicaid Nursing Facility",
    25: None,
    26: None,
    27: "Federal Facility",
    28: "Psychiatric Hospital",
    29: "Critical Access Hospital",
    30: "Other Health Care Institution",
}

# admission_source_id codes -> short descriptions (table 3 in IDS_mapping.csv)
# Codes 9 and 15 (Not Available), no code 16, 17 (NULL), 20 (Not Mapped) and
# 21 (Unknown/Invalid) mean unknown
ADMISSION_SOURCES = {
    1: "Physician Referral",
    2: "Clinic Referral",
    3: "HMO Referral",                 # Health Maintenance Organization
    4: "Hospital Transfer",
    5: "SNF Transfer",                 # Skilled Nursing Facility
    6: "Other Facility Transfer",
    7: "Emergency Room",
    8: "Court/Law Enforcement",
    9: None,
    10: "Critical Access Hospital Transfer",
    11: "Normal Delivery",
    12: "Premature Delivery",
    13: "Sick Baby",
    14: "Extramural Birth",
    15: None,
    17: None,
    18: "Other Home Health Agency Transfer",
    19: "Same Home Health Agency Readmission",
    20: None,
    21: None,
    22: "Same Facility Inpatient Transfer",
    23: "Born Inside Hospital",
    24: "Born Outside Hospital",
    25: "Ambulatory Surgery Center Transfer",
    26: "Hospice Transfer",
}

df = pd.read_csv(
    DATA_FILE,
    keep_default_na=False,                # keep "None" as a category
    na_values=["?"],                      # treat "?" as missing
    dtype={
        "diag_1": str, "diag_2": str, "diag_3": str,  # keep codes like V57, 250.83
        "payer_code": str,                            # text codes, many missing
    },
)
print("Loaded:", df.shape)

# Drugs: "No" means not prescribed;
df[DRUG_COLUMNS] = df[DRUG_COLUMNS].replace("No", "Not_Prescribed")

# Lab tests: "None" means the test was not done;
df[LAB_COLUMNS] = df[LAB_COLUMNS].replace("None", "Not_Tested")

# Admission type: replace the code with its description
df["admission_type_id"] = df["admission_type_id"].map(ADMISSION_TYPES)

# Discharge disposition: replace the code with its short description
df["discharge_disposition_id"] = df["discharge_disposition_id"].map(DISCHARGE_DISPOSITIONS)

# Admission source: replace the code with its short description
df["admission_source_id"] = df["admission_source_id"].map(ADMISSION_SOURCES)

# The ID columns now hold descriptions, so drop _id from their names
df = df.rename(columns={
    "admission_type_id": "admission_type",
    "discharge_disposition_id": "discharge_disposition",
    "admission_source_id": "admission_source",
})

# Drop columns with no data: all missing, or the same value in every row
no_data_columns = df.columns[df.nunique(dropna=True) <= 1]
df = df.drop(columns=no_data_columns)
print("Dropped columns with no data:", list(no_data_columns))

# Missing values ("?" in the original file) are written as empty cells: ""
df.to_csv(OUTPUT_FILE, index=False, na_rep="")

print("Saved:", OUTPUT_FILE)
print(df.isna().sum().loc[lambda s: s > 0])
print(df["max_glu_serum"].value_counts())
print(df["A1Cresult"].value_counts())
print(df["admission_type"].value_counts(dropna=False))
print(df["discharge_disposition"].value_counts(dropna=False))
print(df["admission_source"].value_counts(dropna=False))