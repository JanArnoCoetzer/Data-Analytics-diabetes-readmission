from pathlib import Path
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = REPO_ROOT / "Data" / "processed_diabetic_data.csv"   # output of 1.clean_missing_and_categories
OUTPUT_FILE = REPO_ROOT / "Data" / "cleaned_diabetic_data.csv"

# Drugs prescribed in fewer than this share of stays are merged into one column
RARE_DRUG_THRESHOLD = 0.01                 # 1%

# Number of medical specialties to keep; the rest become "Other"
TOP_SPECIALTIES = 10

# The diabetes drug columns (examide and citoglipton were dropped in step 1)
DRUG_COLUMNS = [
    "metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride",
    "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone",
    "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide",
    "insulin", "glyburide-metformin", "glipizide-metformin",
    "glimepiride-pioglitazone", "metformin-rosiglitazone", "metformin-pioglitazone",
]

df = pd.read_csv(
    INPUT_FILE,
    dtype={
        "diag_1": str, "diag_2": str, "diag_3": str,  # keep codes like V57, 250.83
        "payer_code": str,                            # text codes, many missing
    },
)
print("Loaded:", df.shape)

# Rows to remove

# 1. Patients who died or went to hospice cannot be readmitted
died_or_hospice = df["discharge_disposition"].str.startswith(("Expired", "Hospice"), na=False)
df = df[~died_or_hospice]
print(f"Removed {died_or_hospice.sum():,} stays where the patient died or went to hospice")

# 2. Keep only the first stay of each patient, so no patient appears twice
before = len(df)
df = df.sort_values("encounter_id").drop_duplicates(subset="patient_nbr", keep="first")
print(f"Removed {before - len(df):,} repeat stays (kept the first stay per patient)")

# 3. Gender not recorded
unknown_gender = df["gender"].eq("Unknown/Invalid")
df = df[~unknown_gender]
print(f"Removed {unknown_gender.sum():,} stays with unknown gender")



# Columns to drop or merge


# 4. weight is 97% missing; payer_code is 40% missing and is not clinical
df = df.drop(columns=["weight", "payer_code"])
print("Dropped columns: weight, payer_code")

# 5. medical_specialty: missing -> "Unknown"; keep the top specialties, rest -> "Other"
df["medical_specialty"] = df["medical_specialty"].fillna("Unknown")
top = df["medical_specialty"].value_counts().drop("Unknown", errors="ignore").head(TOP_SPECIALTIES).index
df.loc[~df["medical_specialty"].isin([*top, "Unknown"]), "medical_specialty"] = "Other"
print(f"medical_specialty: kept the top {TOP_SPECIALTIES}, grouped the rest as Other")

# 6. Rare drugs: merge into one column "other_drugs", then drop them
drug_columns = [c for c in DRUG_COLUMNS if c in df.columns]
prescribed_share = df[drug_columns].ne("Not_Prescribed").mean()
rare_drugs = prescribed_share[prescribed_share < RARE_DRUG_THRESHOLD].index.tolist()
any_rare = df[rare_drugs].ne("Not_Prescribed").any(axis=1)
df["other_drugs"] = any_rare.map({True: "Prescribed", False: "Not_Prescribed"})
df = df.drop(columns=rare_drugs)
print(f"Merged {len(rare_drugs)} rare drugs into other_drugs: {rare_drugs}")

# 7. Drop any column that now has the same value in every row
no_data_columns = df.columns[df.nunique(dropna=True) <= 1]
df = df.drop(columns=no_data_columns)
if len(no_data_columns):
    print("Dropped columns with no data:", list(no_data_columns))



# Save
df.to_csv(OUTPUT_FILE, index=False, na_rep="")
print("Saved:", OUTPUT_FILE, df.shape)
print(df["readmitted"].value_counts(normalize=True).round(3))