# Diabetes Hospital Dataset

## Data Dictionary and Mapping Guide

Written in ASD-STE100 Simplified Technical English

## 1. Description of the dataset

This guide gives the definition of each column in the file diabetic_data.csv. It also shows how the ID codes in that file link to the file IDS_mapping.csv. All counts and percentages in this guide come directly from the two supplied files. The data is the public dataset “Diabetes 130-US Hospitals for Years 1999-2008” from the UCI Machine Learning Repository1. The data comes from 130 US hospitals and integrated delivery networks. It covers ten years of clinical care. The primary purpose of the data is to find which diabetic patients go back into hospital less than 30 days after discharge. Each row is one hospital stay (an “encounter”). Each encounter agrees with all five of these conditions1:

1. The encounter is an inpatient admission.

2. The diagnosis of the patient includes a type of diabetes.

3. The stay is a minimum of 1 day and a maximum of 14 days.

4. The hospital did laboratory tests during the stay.

5. The hospital gave medications during the stay.

#### Table 1. Size of the supplied files

| Item | Value |
| --- | --- |
| Rows (encounters) | 101,766 |
| Columns | 50 |
| Unique patients (patient_nbr) | 71,518 |
| Patients with more than one encounter | 16,773 (one patient has 40 encounters) |

Source paper: Strack B., DeShazo J., Gennings C., Olmo J., Ventura S., Cios K., Clore J. “Impact of HbA1c Measurement on Hospital Readmission Rates: Analysis of 70,000 Clinical Database Patient Records.” BioMed Research International, 20143. Dataset DOI: 10.24432/C5230J2.

## 2. Relation between the two files

Only three columns in diabetic_data.csv use the mapping file. The other columns contain readable values, or they use codes that this guide explains.

#### Table 2. Links from the data file to the mapping file

| Column in diabetic_data.csv | Table in IDS_mapping.csv | Result of the lookup |
| --- | --- | --- |
| admission_type_id | Table 1: admission_type_id | Description of the admission type |
| discharge_disposition_id | Table 2: discharge_disposition_id | Description of the discharge disposition |
| admission_source_id | Table 3: admission_source_id | Description of the admission source |

The file IDS_mapping.csv is not one usual table. It contains three small tables, one above the other. A row with only a comma (,) divides each table from the next table. Each table has its own header line, for example admission_type_id,description. If you load the file into pandas, Excel, or SQL as one table, the result is not correct. Divide the file into three lookup tables before you use it. The mapping file also has these problems:

- Many descriptions for admission_source_id start with a space, for example “ Emergency Room”. Remove this space before you compare or show the values.

- In the discharge table, code 30 is between code 26 and code 27. Thus, the rows are not in numerical sequence.

- Some codes mean “unknown”: NULL, Not Available, Not Mapped, and Unknown/Invalid. Use all of these codes as missing values.

- The source file has a spelling error: “Transfer from critial access hospital”. The correct word is “critical

## 3. Missing values

#### Table 3. Markers for missing values

| Marker | Location | Meaning |
| --- | --- | --- |
| ? | race, weight, payer_code, medical_specialty, diag_1/2/3 | The value is not recorded. |
| None | max_glu_serum, A1Cresult | The hospital did not do the test. This is real information. It is not a missing value. |
| Unknown/Invalid | gender | The value is not recorded or is not valid (3 rows). |
| 5, 6, 8 (admission type) and other ID codes | ID columns | The codes map to NULL, Not Available, or Not Mapped. |

By default, pandas reads the text None as a missing value. To keep “test not done” as a separate category, use keep_default_na=False together with na_values=['?'].

#### Table 4. Columns with the most missing data

| Column | Missing (?) | % of rows |
| --- | --- | --- |
| weight | 98,569 | 96.9% |
| medical_specialty | 49,949 | 49.1% |
| payer_code | 40,256 | 39.6% |
| race | 2,273 | 2.2% |
| diag_3 | 1,423 | 1.4% |
| diag_2 | 358 | 0.4% |
| diag_1 | 21 | <0.1% |

## 4. Column definitions

### 4.1 Identifiers

#### Table 5. Identifier columns

| Column | Type | Meaning |
| --- | --- | --- |
| encounter_id | Integer | The unique ID of one hospital stay. Each row has a different value. |
| patient_nbr | Integer | The unique ID of one patient. One patient can have many rows (many stays). |

### 4.2 Patient demographics

#### Table 6. Demographic columns

| Column | Type | Values (count in the file) |
| --- | --- | --- |
| race | Category | Caucasian (76,099), AfricanAmerican (19,210), Hispanic (2,037), Other (1,506), Asian (641), ? (2,273) |
| gender | Category | Female (54,708), Male (47,055), Unknown/Invalid (3) |
| age | 10-year band | From [0-10) to [90-100). The most frequent values are [70-80) (26,068), [60-70) (22,483), [50- 60) (17,256), and [80-90) (17,197). |
| weight | Band, in pounds | From [0-25) to >200. Of the values, 96.9% are missing. Thus, most analyses remove this column. |

Band notation: [70-80) means “70 or more, but less than 80”. A square bracket includes the number. A round bracket does not include the number.

### 4.3 Admission and discharge

These three columns use the lookup tables in IDS_mapping.csv.

#### Table 7. Admission and discharge columns

| Column | Type | Meaning |
| --- | --- | --- |
| admission_type_id | Code (1-8) | The type of admission (for example, emergency or elective). Refer to section 5.1. |
| discharge_disposition_id | Code (1-30) | The location of the patient after discharge (for example, home, a nursing facility, or death). Refer to section 5.2. |
| admission_source_id | Code (1-26) | The location of the patient before admission (for example, the emergency room, a physician referral, or a transfer). Refer to section 5.3. |

### 4.4 The hospital stay

#### Table 8. Columns for the hospital stay

| Column | Type | Range | Meaning |
| --- | --- | --- | --- |
| time_in_hospital | Integer | 1-14 days | The number of days from admission to discharge. |
| payer_code | Category | 17 codes + ? | The organization or person that paid for the stay. Refer to section 6. |
| medical_specialty | Category | 72 specialties + ? | The specialty of the admitting physician (for example, InternalMedicine, Cardiology, or Emergency/Trauma). |
| num_lab_procedures | Integer | 1-132 (average 43.1) | The number of laboratory tests during the stay. |
| num_procedures | Integer | 0-6 | The number of procedures during the stay. This number does not include laboratory tests. |
| num_medications | Integer | 1-81 (average 16.0) | The number of different medications that the patient got during the stay. |

### 4.5 Visits before this stay

These columns give the number of times that the patient used hospital services in the 12 months before this encounter. These columns are among the best indicators of readmission.

#### Table 9. Columns for previous visits

| Column | Range | Meaning |
| --- | --- | --- |
| number_outpatient | 0-42 | Outpatient visits (the patient did not stay in the hospital). |
| number_emergency | 0-76 | Visits to the emergency department. |
| number_inpatient | 0-21 | Previous inpatient admissions. |

### 4.6 Diagnoses

#### Table 10. Diagnosis columns

| Column | Meaning |  |
| --- | --- | --- |
| diag_1 | The primary diagnosi | s (the main cause of the admission). |
| diag_2 | The secondary diagn | osis. |
| diag_3 | An additional second | ary diagnosis. |
| number_diagnoses | The total number of many systems had a | diagnoses in the system for this stay (1-16). The most frequent value is 9, because limit of 9 entries. |

The diagnosis values are ICD-9-CM codes. ICD-9-CM is the US medical code system that was in use before 2015. The codes have three formats:

- Numbers, for example 428 or 250.83. These are standard disease codes.

- Codes that start with V, for example V57. These are other conditions that have an effect on health, for example rehabilitation care or follow-up visits.

- Codes that start with E, for example E888. These are external causes of injury, for example falls or accidents.

#### Table 11. ICD-9 groups (the groups from the source paper)

| Group | ICD-9 codes | Examples |
| --- | --- | --- |
| Circulatory | 390-459, 785 | 428 = heart failure; 414 = coronary artery disease; 410 = heart attack |
| Respiratory | 460-519, 786 | 486 = pneumonia; 786 = chest pain or respiratory symptoms |
| Digestive | 520-579, 787 | — |
| Diabetes | 250.xx | 250.01, 250.83 (the decimal digits give the type of diabetes and the complication) |
| Injury | 800-999 | — |
| Musculoskeletal | 710-739 | 715 = osteoarthritis |
| Genitourinary | 580-629, 788 | 599 = urinary tract disorder |
| Neoplasms (cancer) | 140-239 | — |
| Other | All other codes, including V and E codes | 276 = fluid or electrolyte disorder; 401 = high blood pressure |

#### Table 12. Most frequent primary diagnoses (diag_1) in the file

| Code | Diagnosis | Rows |
| --- | --- | --- |
| 428 | Heart failure | 6,862 |
| 414 | Coronary artery disease | 6,581 |
| 786 | Chest pain or respiratory symptoms | 4,016 |
| 410 | Heart attack | 3,614 |
| 486 | Pneumonia | 3,508 |

Diabetes codes have the format 250.xy. The fourth digit (x) gives the complication. The fifth digit (y) gives the type of diabetes and the level of control.

#### Table 13. How to read diabetes codes 250.xy

| Digit | Value | Meaning |
| --- | --- | --- |
| x (4th) | 0 | No complication |
| x (4th) | 1 | Ketoacidosis |
| x (4th) | 4 | Kidney |
| x (4th) | 5 | Eye |
| x (4th) | 6 | Nerve |
| x (4th) | 7 | Circulation |
| x (4th) | 8 | Other |
| y (5th) | 0 | Type 2 |
| y (5th) | 1 | Type 1 |
| y (5th) | 2 | Type 2, not controlled |
| y (5th) | 3 | Type 1, not controlled |

### 4.7 Laboratory test results Table 14.

Laboratory test columns

| Column | Value | Count | Meaning |
| --- | --- | --- | --- |
| max_glu_serum | None | 96,420 | The hospital did not do the blood glucose test. |
|  | Norm | 2,597 | Normal result. |
|  | >200 | 1,485 | More than 200 mg/dL. |
|  | >300 | 1,264 | More than 300 mg/dL. |
| A1Cresult | None | 84,748 | The hospital did not do the HbA1c test. |
|  | Norm | 4,990 | Less than 7% (normal, good control). |
|  | >7 | 3,812 | From 7% to 8%. |
|  | >8 | 8,216 | More than 8% (bad control). |

The two tests give this information:

- The glucose serum test shows the blood sugar level at one time.

- The HbA1c test shows the average blood sugar level for the last 2 to 3 months. The source paper examined if the hospital measured HbA1c or not.

### 4.8 Diabetes medications (23 columns)

Each medication column shows what occurred to that medication during this stay.

#### Table 15. Values in the medication columns

| Value | Meaning |
| --- | --- |
| No | The physician did not prescribe the medication. |
| Steady | The physician prescribed the medication. The dose did not change. |
| Up | The dose increased. |
| Down | The dose decreased. |

#### Table 16. Medication columns

| Column | Medication class |
| --- | --- |
| insulin | Insulin |
| metformin | Biguanide |
| glipizide | Sulfonylurea |
| glyburide | Sulfonylurea |
| pioglitazone | Thiazolidinedione |
| rosiglitazone | Thiazolidinedione |
| glimepiride | Sulfonylurea |
| repaglinide | Meglitinide |
| glyburide-metformin | Combination |
| nateglinide | Meglitinide |
| acarbose | Alpha-glucosidase inhibitor |
| chlorpropamide | Sulfonylurea (old type) |
| tolazamide | Sulfonylurea (old type) |
| miglitol | Alpha-glucosidase inhibitor |
| tolbutamide | Sulfonylurea (old type) |
| glipizide-metformin | Combination |
| troglitazone | Thiazolidinedione (removed from the market in 2000) |
| metformin-rosiglitazone | Combination |
| acetohexamide | Sulfonylurea (old type) |
| glimepiride-pioglitazone | Combination |
| metformin-pioglitazone | Combination |
| examide | The name is in the source data. |
| citoglipton | The name is in the source data. It is possibly a spelling error for sitagliptin. |

The columns examide and citoglipton have only one value. Thus, they give no information, and you can remove them. Many other medication columns also contain almost no data.

### 4.9 Medication summary flags

#### Table 17. Medication summary columns

| Column | Values (count) | Meaning |
| --- | --- | --- |
| change | Ch (47,011), No (54,755) | Ch means that one or more diabetes medications or doses changed during the stay. |
| diabetesMed | Yes (78,363), No (23,403) | Shows if the physician prescribed one or more diabetes medications. |

### 4.10 Target variable: readmission

#### Table 18. Values of the target column

| readmitted value | Count | % | Meaning |
| --- | --- | --- | --- |
| NO | 54,864 | 53.9% | There is no record of readmission. |
| >30 | 35,545 | 34.9% | Readmission more than 30 days after discharge. |
| <30 | 11,357 | 11.2% | Readmission less than 30 days after discharge (the primary outcome of interest). |

Most studies use this column as a yes/no value. <30 is 1 (early readmission). >30 and NO are 0.

## 5. ID mapping tables (from IDS_mapping.csv)

The “Rows” column shows the number of encounters in diabetic_data.csv that use each code. The descriptions are the initial text from the mapping file. This guide adds “(missing)” to the codes that mean “unknown”.

### 5.1 admission_type_id: type of admission

#### Table 19. admission_type_id codes

| ID | Description | Rows |
| --- | --- | --- |
| 1 | Emergency | 53,990 |
| 2 | Urgent | 18,480 |
| 3 | Elective | 18,869 |
| 4 | Newborn | 10 |
| 5 | Not Available (missing) | 4,785 |
| 6 | NULL (missing) | 5,291 |
| 7 | Trauma Center | 21 |
| 8 | Not Mapped (missing) | 320 |

Codes 5, 6, and 8 all mean “unknown”. These codes are in approximately 10% of the rows.

### 5.2 discharge_disposition_id: location of the patient after the stay

#### Table 20. discharge_disposition_id codes

| ID | Description | Rows |
| --- | --- | --- |
| 1 | Discharged to home | 60,234 |
| 2 | Discharged/transferred to another short term hospital | 2,128 |
| 3 | Discharged/transferred to SNF (Skilled Nursing Facility) | 13,954 |
| 4 | Discharged/transferred to ICF (Intermediate Care Facility) | 815 |
| 5 | Discharged/transferred to another type of inpatient care institution | 1,184 |
| 6 | Discharged/transferred to home with home health service | 12,902 |
| 7 | Left AMA (Against Medical Advice) | 623 |
| 8 | Discharged/transferred to home under care of Home IV provider | 108 |
| 9 | Admitted as an inpatient to this hospital | 21 |
| 10 | Neonate discharged to another hospital for neonatal aftercare | 6 |
| 11 | Expired (died) | 1,642 |
| 12 | Still patient or expected to return for outpatient services | 3 |
| 13 | Hospice / home | 399 |
| 14 | Hospice / medical facility | 372 |
| 15 | Discharged/transferred within this institution to Medicare approved swing bed | 63 |
| 16 | Discharged/transferred/referred to another institution for outpatient services | 11 |
| 17 | Discharged/transferred/referred to this institution for outpatient services | 14 |
| 18 | NULL (missing) | 3,691 |
| 19 | Expired at home. Medicaid only, hospice. | 8 |
| 20 | Expired in a medical facility. Medicaid only, hospice. | 2 |
| 21 | Expired, place unknown. Medicaid only, hospice. | 0 |
| 22 | Discharged/transferred to another rehab facility, including rehab units of a hospital | 1,993 |
| 23 | Discharged/transferred to a long term care hospital | 412 |
| 24 | Discharged/transferred to a nursing facility certified under Medicaid but not Medicare | 48 |
| 25 | Not Mapped (missing) | 989 |
| 26 | Unknown/Invalid (missing) | 0 |
| 27 | Discharged/transferred to a federal health care facility | 5 |
| 28 | Discharged/transferred/referred to a psychiatric hospital or psychiatric unit of a hospital | 139 |
| 29 | Discharged/transferred to a Critical Access Hospital (CAH) | 0 |
| 30 | Discharged/transferred to another type of health care institution not defined elsewhere | 0 |

Patients who died (codes 11, 19, 20, and 21) cannot go back into hospital. Patients in hospice care (codes 13 and 14) will possibly not go back into hospital. Most studies remove these rows before they make a model. The source paper also removed these rows.

### 5.3 admission_source_id: location of the patient before the stay

The mapping has no code 16. Codes 9, 15, 17, 20, and 21 all mean “unknown”.

#### Table 21. admission_source_id codes

| ID | Description | Rows |
| --- | --- | --- |
| 1 | Physician Referral | 29,565 |
| 2 | Clinic Referral | 1,104 |
| 3 | HMO Referral | 187 |
| 4 | Transfer from a hospital | 3,187 |
| 5 | Transfer from a Skilled Nursing Facility (SNF) | 855 |
| 6 | Transfer from another health care facility | 2,264 |
| 7 | Emergency Room | 57,494 |
| 8 | Court/Law Enforcement | 16 |
| 9 | Not Available (missing) | 125 |
| 10 | Transfer from critical access hospital | 8 |
| 11 | Normal Delivery | 2 |
| 12 | Premature Delivery | 0 |
| 13 | Sick Baby | 1 |
| 14 | Extramural Birth (born outside the hospital) | 2 |
| 15 | Not Available (missing) | 0 |
| 17 | NULL (missing) | 6,781 |
| 18 | Transfer From Another Home Health Agency | 0 |
| 19 | Readmission to Same Home Health Agency | 0 |
| 20 | Not Mapped (missing) | 161 |
| 21 | Unknown/Invalid (missing) | 0 |
| 22 | Transfer from hospital inpatient / same facility, resulting in a separate claim | 12 |
| 23 | Born inside this hospital | 0 |
| 24 | Born outside this hospital | 0 |
| 25 | Transfer from Ambulatory Surgery Center | 2 |
| 26 | Transfer from Hospice | 0 |

## 6. Payer codes (not in the mapping file)

The file IDS_mapping.csv does not give a definition for payer_code. The dataset authors did not publish an official lookup table. The source paper gives only some examples (Blue Cross/Blue Shield, Medicare, and self-pay). The meanings in the table below are the meanings that most users accept. They come from standard US insurance abbreviations. The meanings with low confidence are not certain. Use them with care.

#### Table 22. payer_code values

| Code | Probable meaning | Rows | Confidence |
| --- | --- | --- | --- |
| MC | Medicare | 32,439 | High |
| HM | HMO (Health Maintenance Organization) | 6,274 | High |
| SP | Self-pay | 5,007 | High |
| BC | Blue Cross / Blue Shield | 4,655 | High |
| MD | Medicaid | 3,532 | High |
| CP | Commercial or private insurance | 2,533 | Medium |
| UN | Uninsured or United Healthcare | 2,448 | Low |
| CM | Commercial or Medicare managed care | 1,937 | Low |
| OG | Other government | 1,033 | Medium |
| PO | PPO (Preferred Provider Organization) or other private | 592 | Low |
| DM | Disability or Medicaid managed care | 549 | Low |
| CH | CHAMPUS (US military health) | 146 | Medium |
| WC | Workers’ compensation | 135 | High |
| OT | Other | 95 | High |
| MP | Medicare / Medicaid plan | 79 | Low |
| SI | Self-insured | 55 | Low |
| FR | Free or charity care | 1 | Low |
| ? | Missing | 40,256 | — |

## References

## 1. UCI Machine Learning Repository, “Diabetes 130-US Hospitals for Years 1999-2008”:

https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008

## 2. Dataset DOI: https://doi.org/10.24432/C5230J

## 3. Strack et al., “Impact of HbA1c Measurement on Hospital Readmission Rates,” BioMed Research International, 2014.

This is the introductory paper on the UCI page: https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008 All counts and percentages come from the supplied files diabetic_data.csv and IDS_mapping.csv.
