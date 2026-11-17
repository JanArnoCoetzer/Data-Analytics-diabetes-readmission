# Prioritising Follow-Up Care: Predicting 30-Day Readmission of Diabetic Patients from Hospital Encounter Data

Jan Arno Coetzer • T00206990 • Computing with Games Development

Data Analytics-49295 (DBMS71008) |  Andrew Shields |  4 December 2026

GitHub repository: https://github.com/JanArnoCoetzer/Data-Analytics-diabetes-readmission

## Abstract

> [GUIDANCE: Write the abstract last. In approximately 150–200 words, state the problem, data, method, principal result, main limitation and conclusion. Do not include citations, code or detailed background.]

[Replace this text with the abstract. The abstract should stand alone and allow a reader to understand what was investigated, how it was investigated, what was found and what can reasonably be concluded.]

Keywords: [four to six terms, separated by commas]

## Using This Template

> [GUIDANCE: This is an ACM-inspired module template, not the official ACM publication template. Retain the section structure unless the lecturer approves a change. The paper complements the CRISP-DM notebook; it should not reproduce the notebook, preparation log or code.]

| Paper should contain | Notebook / repository should contain |
| --- | --- |
| Problem, method, selected evidence, evaluation, limitations and recommendations | Code, detailed exploration, complete preparation decisions, extended outputs and development history |
| A small number of purposeful tables and figures | Additional diagnostic charts, experiments and supporting evidence |
| Concise explanation of reproducible method | Runnable implementation and environment/data-access instructions |

## 1. Introduction and Business Context
[GUIDANCE: Explain the domain, specific problem, intended users or stakeholders, why the problem matters, the analytical objective and the contribution of the project. State the research or analytical question clearly. Do not begin with the chosen algorithm.]
[Write the introduction and business context here. Recommended focus: problem, stakeholders, practical objective, analytics objective, scope and contribution.]

An early readmission after a hospital stay costs money and can cause harm to the patient. In the United States, the Hospital Readmissions Reduction Program decreases Medicare payments to hospitals that have too many readmissions. The maximum decrease is 3% [1]. Patients with diabetes have a higher risk. Studies show a 30-day readmission rate of 14.4–22.7% for patients with diabetes and 8.5–13.5% for all patients [2].

This project supports one decision: which diabetic patients must get follow-up care after discharge. Examples of follow-up care are a telephone call, a medication review or an early clinic visit. The users are discharge-planning teams and diabetes care teams. These teams have limited resources. A model that sorts patients by risk can help the teams to give care to the patients with the highest risk. The model gives support to the decision, but it does not replace clinical judgment.

The analytical objective is to predict, at discharge, if a diabetic inpatient will return to hospital in 30 days. The data is the Diabetes 130-US Hospitals dataset [3]. The task is binary classification, and the positive class is rare. For technical success, the model must have better recall and average precision than a majority-class baseline. For practical success, the model must flag a manageable number of patients and find a useful part of the early readmissions.

The project uses the CRISP-DM process [4]. This version of the paper shows Business Understanding, Data Understanding and Data Preparation. Modelling and evaluation are not complete.

## 2. Background and Related Work
[GUIDANCE: Synthesize a small number of credible sources relevant to the domain, data and analytical method. Explain how prior work informs this investigation. Do not write a source-by-source annotated list. Verify every reference, including references suggested by AI tools.]
[Introduce and compare the most relevant literature. Use numbered citations such as [1], [2] and [3]. Explain the gap or rationale for the present investigation.]

Strack et al. [5] first used this dataset. They examined if HbA1c measurement has an effect on readmission. They kept only the first encounter of each patient, so that each row is independent. They also removed encounters that ended in death or discharge to a hospice. The result was 69,984 encounters.

In these encounters, the hospital measured HbA1c in only 18.4%. The relation between HbA1c measurement and readmission changed with the primary diagnosis [5]. Thus, a model of this data must include the diagnosis. 
Strack et al. also removed weight (97% missing) and payer code. They kept medical specialty and added a “missing” value [5]. This project uses the same cohort rules, so that its results are comparable with the source study.

Kansagara et al. [6] reviewed 26 readmission risk models. Most models had poor performance. The c-statistics were between 0.55 and 0.83, and only six studies had a value above 0.70. Few models used illness severity, functional status or social determinants of health [6].
This dataset also does not have these variables. Thus, the expected discrimination is moderate.

Early readmission is rare, so accuracy is not a good measure. A model that always predicts “no readmission” has approximately 91% accuracy on the prepared data. But this model does not help the decision. Thus, the evaluation uses recall, precision and average precision for the positive class.

## 3. Data and Methodology
[GUIDANCE: Summarise the method sufficiently for a technically informed reader to understand and reproduce the approach. Detailed code and the full preparation log belong in the notebook.]

### 3.1 Data Source and Scope
[GUIDANCE: Identify the source, licence or permission, access date, population, time period, geography, sample size and unit of analysis. Define the target and the most important features. Refer to the original data publisher where possible.]

The data is the Diabetes 130-US Hospitals for Years 1999–2008 dataset from the UCI Machine Learning Repository [3]. Clore, Cios, DeShazo and Strack made the dataset. The CC BY 4.0 licence permits use with attribution. The data shows ten years of clinical care at 130 US hospitals.

Each row is one inpatient encounter. Each encounter agrees with five criteria: an inpatient admission, a diabetes diagnosis, a stay of 1–14 days, laboratory tests and medications [3]. The raw file has 101,766 encounters and 50 columns. The columns contain identifiers, demographics, admission data, counts of hospital use, three ICD-9 diagnosis codes, two laboratory results, 23 diabetes medications and the readmission outcome.

A second file, IDS_mapping.csv, gives the descriptions of the admission type, discharge disposition and admission source codes. The data has no names or other direct identifiers. Date of data access: 6 November 2026.
### 3.2 Data Understanding and Quality

> [GUIDANCE: Summarise the most important descriptive findings and quality issues. Quantify missingness, imbalance, inconsistencies, unusual values or representativeness concerns where relevant. Select only findings that affect the project question or method.]

The unit of analysis is important. The 101,766 encounters are from 71,518 patients. Of these patients, 16,773 have more than one encounter, with a maximum of 40. The encounters of one patient are not independent. If they are in the training data and in the test data, the evaluation results are too high.

The dataset uses “?” for missing values. Weight is missing in 96.9% of encounters, medical specialty in 49.1%, payer code in 39.6% and race in 2.2%. The primary, secondary and tertiary diagnoses are missing in 21, 358 and 1,423 encounters. Three encounters have an unknown gender. Some ID codes, for example “NULL”, “Not Mapped” and “Not Available”, are also missing values.

Laboratory tests are not frequent. The hospitals measured HbA1c in 16.7% of encounters and maximum glucose serum in 5.3%. Thus, “None” means “not tested”. It does not mean a normal result. Two medications, examide and citoglipton, have the same value in all rows.

The target is not balanced. Of all encounters, 53.9% had no readmission and 34.9% had a readmission after more than 30 days. Only 11.2% had a readmission in 30 days. Most patients are old: 67.3% of encounters are for patients of 60 years or more. Of the encounters with a recorded race, 76.5% are Caucasian.

### 3.3 Data Preparation

> [GUIDANCE: Explain the preparation decisions that materially affect the analysis. Include selection, cleaning, integration, feature construction, encoding, scaling and leakage prevention where relevant. State important assumptions. Do not paste the complete preparation log.]

[Summarise and justify the principal preparation decisions here.]



### 3.4 Modelling and Evaluation Design

> [GUIDANCE: Explain the task type, baseline, candidate methods, selected method, input features, target, train/test or validation strategy, reproducibility controls, important settings and evaluation measures. Link each decision to the objective and data.]

[Describe and justify the modelling and evaluation design here.]

[Continue writing here]

[Continue writing here]

## 4. Results

> [GUIDANCE: Present the central factual results before extended interpretation. Include baseline performance, model performance and a small number of meaningful figures or tables. All reported values must agree with the final notebook. Do not include screenshots of code.]

[Introduce the results and identify the evidence shown below.]

[Continue writing here]

Table 1. [Concise title describing the comparison]

| Model / baseline | Evaluation measure | Result | Brief note |
| --- | --- | --- | --- |
| [Training-mean baseline] | [MAE] | [value and unit] | [reference point] |
| [Primary model] | [MAE] | [value and unit] | [comparison] |
| [Alternative model, if used] | [measure] | [value and unit] | [comparison] |

> [GUIDANCE: Replace this sample table with project results. Report the evaluation dataset and units. Do not claim that the numerically best result is necessarily practically acceptable.]

[INSERT PURPOSEFUL FIGURE HERE]

Figure 1. [Describe what is shown, the dataset or subset, and any essential units.]

> [GUIDANCE: Use a readable figure exported from the notebook, not a screenshot of code. Refer to each figure in the body text and explain the pattern that matters.]

[Report the remaining central results here. Distinguish observed evidence from interpretation.]

[Continue writing here]

[Continue writing here]

## 5. Discussion and Evaluation

> [GUIDANCE: Interpret the results against the analytical objective, technical success criteria and practical success criteria. Compare with the baseline and relevant literature. Discuss error patterns, generalisability, assumptions, ethics, bias, uncertainty and what should not be concluded.]

[Discuss what the results mean, whether the model is useful, how evidence compares with expectations or prior work, and why limitations matter.]

[Continue writing here]

[Continue writing here]

[Continue writing here]

## 6. Recommendations and Deployment Considerations

> [GUIDANCE: Explain how the findings could be used in practice, who would use them, what should remain under human oversight, how performance would be monitored and when the data or model should be reviewed. A live deployed application is not required unless separately instructed.]

[State evidence-based recommendations and a realistic route to use, monitoring and governance.]

[Continue writing here]

[Continue writing here]

## 7. Limitations and Future Work

> [GUIDANCE: Identify specific limitations arising from the data, design, preparation, method and evaluation. Explain their likely effect. Propose realistic future work rather than generic statements such as “collect more data”.]

[Explain the most important limitations and targeted next steps.]

[Continue writing here]

[Continue writing here]

## 8. Conclusion

> [GUIDANCE: Answer the project question directly. Summarise the defensible finding, whether the project met its objectives, the main recommendation and the most important limitation. Do not introduce new evidence.]

[Write a concise conclusion here.]

[Continue writing here]

## Responsible AI Collaboration Statement

> [GUIDANCE: Insert the 300–500 word statement required by the CA2 brief. Identify tools and tasks, explain verification, describe rejected or corrected output, and distinguish AI assistance from student judgement. If the lecturer directs that this statement remain in the notebook only, replace this section with one sentence referring to the notebook.]

[Write the Responsible AI Collaboration Statement here.]

[Continue writing here]

[Continue writing here]

## References

[1] Centers for Medicare & Medicaid Services, “Hospital Readmissions Reduction Program (HRRP).” [Online]. Available: https://www.cms.gov/medicare/payment/prospective-payment-systems/acute-inpatient-pps/hospital-readmissions-reduction-program-hrrp. [Accessed: Nov. 17, 2026].

[2] S. Ostling, J. Wyckoff, S. L. Ciarkowski, C.-W. Pai, H. M. Choe, V. Bahl, and R. Gianchandani, “The relationship between diabetes mellitus and 30-day readmission rates,” Clinical Diabetes and Endocrinology, vol. 3, Art. no. 3, 2017, doi: 10.1186/s40842-016-0040-x.

[3] J. Clore, K. Cios, J. DeShazo, and B. Strack, “Diabetes 130-US Hospitals for Years 1999–2008,” UCI Machine Learning Repository, 2014. [Online]. Available: https://doi.org/10.24432/C5230J. [Accessed: Nov. 17, 2026].

[4] R. Wirth and J. Hipp, “CRISP-DM: Towards a standard process model for data mining,” in Proc. 4th Int. Conf. Practical Applications of Knowledge Discovery and Data Mining, 2000, pp. 29–39.

[5] B. Strack, J. P. DeShazo, C. Gennings, J. L. Olmo, S. Ventura, K. J. Cios, and J. N. Clore, “Impact of HbA1c measurement on hospital readmission rates: Analysis of 70,000 clinical database patient records,” BioMed Research International, vol. 2014, Art. no. 781670, 2014, doi: 10.1155/2014/781670.

[6] D. Kansagara, H. Englander, A. Salanitro, D. Kagen, C. Theobald, M. Freeman, and S. Kripalani, “Risk prediction models for hospital readmission: A systematic review,” JAMA, vol. 306, no. 15, pp. 1688–1698, 2011, doi: 10.1001/jama.2011.1515.



## Final Template Check

| Check | Complete |
| --- | --- |
| All green guidance paragraphs and bracketed placeholders removed | ☐ |
| Title block and repository URL complete | ☐ |
| Paper complements rather than duplicates the notebook | ☐ |
| All figures and tables numbered, captioned and discussed | ☐ |
| Results match the final notebook | ☐ |
| Claims remain within the evidence and avoid unsupported causation | ☐ |
| References verified and consistently formatted | ☐ |
| PDF readable and within the CA2 length limit | ☐ |
