# Topic Selection: Predictive Analytics on Real-World Healthcare Data

This document presents the topic selection for the Data Analytics CRISP-DM project (CA2). The project applies the CRISP-DM methodology to a real analytics problem, culminating in a notebook, a GitHub repository and a four-page conference-style paper. Because the assessment brief requires each project to begin with a clearly stated decision or problem rather than a technique, every candidate topic below is framed around the decision it would support, with the method following from the problem and the data.

The candidate topics are drawn from healthcare, a domain in which open, well-documented datasets are plentiful and present genuine data-quality challenges that give the Data Understanding and Data Preparation phases real substance. Real clinical data typically exhibits three properties that make preparation demanding. These properties, which motivated the shortlist, are defined below.

Key Properties of Real-World Clinical Data

1. High dimensionality

A dataset with high dimensionality contains a large number of variables or features for the analysis (IBM, 2024). High-dimensional clinical data demands careful feature selection and grouping before modelling.

2. Heterogeneity

Heterogeneity is a lack of uniformity in the data. For example, data can occur in different formats, which may be structured, semi-structured, or unstructured (IBM, 2017). Heterogeneous data must be reconciled into a single, consistent form before analysis.

3. Unstructured data

Unstructured data is information that does not follow a predefined format or a fixed database schema (IBM, 2025). Free-text clinical notes and open survey responses are common examples.

# Data Sources

All candidate datasets are openly available from the UCI Machine Learning Repository (archive.ics.uci.edu), Kaggle (www.kaggle.com), or Mendeley Data (data.mendeley.com). Each source is public, lawful to use for academic purposes, and published with identifiable provenance, satisfying the brief’s requirement for a lawful, ethical and appropriately attributed data source. The dataset selected for the final project will be cited with its published source paper and repository identifier.

# Candidate Topics

The project will use one topic from this list. Each topic is stated with the decision it would support and its dataset.

1.Prediction of 30-day hospital readmission for diabetic patients.

- Supports the decision of which discharged diabetic patients should receive targeted follow-up care to reduce costly early readmission.

- Dataset: UCI Machine Learning Repository.

2.Diagnosis of heart disease from clinical test results.

- Supports the decision of whether heart disease can be ruled in or out from non-invasive clinical tests.

- Dataset: UCI Machine Learning Repository.

3.Prediction of stroke risk.

- Supports the identification of patients at elevated stroke risk from clinical and lifestyle factors.

- Dataset: Kaggle.

4.Prediction of early sepsis in ICU patients.

- Supports the early flagging of deteriorating ICU patients from bedside measurements.

- Dataset: Kaggle.

5.Workplace factors in mental health outcomes for tech workers.

- Supports the identification of workplace factors associated with mental health outcomes in survey data.

- Dataset: Mendeley Data.

# Scope and Timeline

The project must be complete by Friday 4 December 2026. The selected topic must present a genuine preparation challenge that can be investigated and documented, but the scope must remain bounded so the project finishes on time alongside other subjects. Each candidate was therefore assessed not only on how interesting its data is, but on whether the preparation work has a clear finish line.

# AI Recommendation and Reasoning(Directly Pasted)

1.Predicting 30-day hospital readmission for diabetic patients.

This topic offers the strongest overall candidate. The decision problem is genuine and well documented: early readmission of diabetic patients is costly and partly preventable, and hospitals must decide which discharged patients to target with follow-up care (Strack et al., 2014). The dataset contains 101,766 inpatient encounters and 47 features drawn from 130 US hospitals, giving the Data Understanding phase substantial material, with one encounter as a clear unit of analysis and a well-defined classification target. The preparation challenge is genuine but bounded: missing values coded as "?", ICD-9 diagnosis codes that need grouping, ID-mapping tables to join, and a positive class of roughly 11% that requires imbalance-aware evaluation using recall, precision or AUPRC rather than accuracy. A classification method such as a decision tree or logistic regression, both covered in the module, matches the target and variables.

2.Diagnosis of heart disease from clinical test results.

This topic is very manageable in scope because the dataset is small, with 920 records and 13 features, and merging the four hospital source files gives a reasonable heterogeneity story. However, that smallness is also its weakness: the Data Understanding and Data Preparation phases would feel thin, and missing values concentrated in a small number of columns are not enough of a preparation challenge to satisfy the brief. It is a safe backup but a weaker choice than topic 1.

3.Prediction of stroke risk.

This is the easiest topic on the list, with 5,110 rows and 12 attributes, so the workload risk is minimal. The problem is the opposite of topic 2’s: it is too easy. The preparation challenge amounts to 201 missing BMI values, some "Unknown" smoking statuses, and class imbalance, which is not enough documented preprocessing for the emphasis of this project. It could be finished comfortably, but at the cost of marks.

4.Early sepsis prediction in ICU patients.

This topic fits the high-dimensionality theme well with a large set of clinical features, but it carries two real risks. The data is synthetic, which weakens the provenance and data-quality discussion the rubric rewards, and treating hourly ICU measurements means time-series feature engineering that can expand without a natural finish line. For the project window shared with other subjects, the scope risk is too high.

5.Workplace factors in mental health outcomes for tech workers.

This is the most distinctive topic and the only one that matches all three defined properties, since the survey data is high-dimensional, heterogeneous across years, and contains free-text answers. That same richness is the risk: harmonising five survey years with inconsistent questions, heavy missingness, and open-text fields is open-ended work that could easily consume the entire project window. It suits the theme best but the schedule worst.

Overall, topic 1 is recommended because it is the only topic where the decision problem, the data scale and the preparation challenge are all strong while the work remains bounded, with topic 5 kept as the alternative if a more distinctive project is preferred.

# My chosen topic and reasoning behind the topic

Topic 1 supports a real decision: when a diabetic patient is discharged, staff must decide who gets targeted follow-up care, such as a phone call or an early clinic appointment, to prevent an early readmission. The intended users are discharge-planning and ward staff.

Since only about 11% of encounters end in a readmission within 30 days, accuracy is the wrong measure. I will compare my model against a simple baseline and judge it on recall and precision instead. In practice the model would rank patients so staff can focus on the high-risk ones, and a missed readmission is a worse error than an unnecessary phone call.

The data is de-identified and openly licensed under CC BY 4.0, so privacy is covered, but it includes race and payer code, so bias must be discussed in the evaluation. Some patients appear in more than one encounter, so I will split the data by patient to avoid leakage. The data is from US hospitals between 1999 and 2008, so it will not transfer directly to current practice.

If topic 1 goes wrong, I will first cut its scope, for example a simpler target or fewer features, instead of switching datasets, because changing domain late would restart the work and need re-approval. Topic 3 stays my backup because it is simple and fast to complete, but I accept that this costs depth in Data Understanding and Data Preparation.

I will write my Data Analytics assignment on Prediction of 30-day hospital readmission for diabetic patients using the dataset found at archive.ics.uci.edu/dataset/296 (Clore et al., 2014). The dataset is published under CC BY 4.0 and is described in the source paper by Strack et al. (2014).

# References

Clore, J., Cios, K., DeShazo, J. and Strack, B. (2014) 'Diabetes 130-US Hospitals for Years 1999-2008' [Dataset]. UCI Machine Learning Repository. Available at: https://doi.org/10.24432/C5230J (Accessed: 6 November 2026).

IBM (2017) 'Storing IoT data, analyzing IoT data, and applying rules to IoT data'. IBM Developer, 18 December. Available at: https://developer.ibm.com/tutorials/iot-lp301-iot-manage-data/ (Accessed: 6 November 2026).

IBM (2024) 'What is dimensionality reduction?'. IBM Think, 5 January. Available at: https://www.ibm.com/think/topics/dimensionality-reduction (Accessed: 6 November 2026).

IBM (2025) 'What is unstructured data?'. IBM Think, 28 April. Available at: https://www.ibm.com/think/topics/unstructured-data (Accessed: 6 November 2026).

Strack, B., DeShazo, J.P., Gennings, C., Olmo, J.L., Ventura, S., Cios, K.J. and Clore, J.N. (2014) 'Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records'. BioMed Research International, 2014, Article 781670. Available at: https://doi.org/10.1155/2014/781670 (Accessed: 6 November 2026).
