# 🍅 Tomato Trait Prediction Using SNP Markers, GWAS, XGBoost and Explainable AI

## Overview

Plant breeding traditionally requires multiple generations of field experiments to identify plants with desirable traits. This process is time-consuming and expensive.

This project develops an **AI-based genomic prediction system** that predicts tomato fruit weight using **genetic variation information (SNP markers)**.

The project integrates:

- Genome-Wide Association Study (GWAS)
- Machine Learning based Trait Prediction
- XGBoost Regression
- SHAP Explainable Artificial Intelligence
- Streamlit Interactive Web Application

The aim is to identify important genomic regions associated with tomato fruit weight and develop a prediction system using only SNP information.

---

# Project Objective

The main objectives of this project are:

1. Analyze tomato genetic variation using SNP markers.

2. Identify SNPs associated with fruit weight using GWAS.

3. Develop a machine learning model to predict tomato fruit weight from SNP profiles.

4. Identify the contribution of individual SNP markers using SHAP analysis.

5. Develop an interactive web application for genomic trait prediction and visualization.


---

# Biological Background

## SNP (Single Nucleotide Polymorphism)

A SNP is a variation at a single nucleotide position in the DNA sequence among individuals.

Example:

```
Plant A:
A T G C

Plant B:
A T A C
```

The nucleotide difference represents a SNP.

SNP markers act as genetic fingerprints that can be used to study relationships between genetic variation and plant traits.

---

# Dataset Description

## Dataset Source

The dataset used in this project is the tomato:

**Solanum pennellii Backcross Inbred Lines (BILs) Population**

Dataset source:

https://datadryad.org/dataset/doi:10.5061/dryad.2fqz612wx


The dataset contains:

- Genome-wide SNP marker information
- Tomato plant identifiers
- Phenotypic measurements


---

# Genotype Dataset

The genotype dataset contains SNP marker information for tomato plants.

Structure:

| Plant ID | SNP1 | SNP2 | SNP3 |
|----------|------|------|------|
| p-1-1 | 1 | 3 | 1 |
| p-10-1 | 3 | 1 | 3 |


## Genotype Encoding

The SNP values are encoded as:

```
1 → Parent allele 1
3 → Parent allele 2
```

These encoded values represent different allele states inherited from the parents.

Dataset statistics:

- Number of tomato plants: 1148
- Number of SNP markers: 7699
- Number of chromosomes: 12


---

# Phenotype Dataset

The phenotype dataset contains measured plant traits.

The target trait used in this project:

```
Fruit Weight (BILs FW(gr))
```

Example:

| Plant ID | Fruit Weight |
|----------|--------------|
| p-1-1 | 24.7 g |
| p-10-1 | 35.4 g |


---

# Project Workflow

```
                 Genotype Data
                       |
                       |
                       ↓
             Data Preprocessing
                       |
                       ↓
              GWAS Analysis
                       |
                       ↓
          Significant SNP Identification
                       |
                       ↓
            XGBoost Regression Model
                       |
                       ↓
             SHAP Explainability
                       |
                       ↓
          Candidate Gene Interpretation
                       |
                       ↓
          Streamlit Web Application

```


---

# Methodology

## 1. Data Preprocessing

The raw genotype and phenotype datasets were processed before analysis.

Steps performed:

- Checked genotype quality
- Checked phenotype distribution
- Removed missing values
- Matched genotype and phenotype samples using Plant ID


After alignment:

```
Samples used:
1148 tomato plants

Features:
7699 SNP markers
```


---

# 2. Genome-Wide Association Study (GWAS)

GWAS was performed to identify SNP markers associated with fruit weight.

GWAS evaluates each SNP independently and determines whether genetic variation at that location is related to differences in fruit weight.

The statistical significance is measured using:

```
P-value
```

A smaller p-value indicates stronger association.

Example:

```
SNP:
SSL2.50CH11_2693462

P-value:
2.66 × 10^-15
```

Output generated:

- GWAS result table
- Manhattan Plot
- QQ Plot


---

# 3. Manhattan Plot

The Manhattan plot visualizes SNP-trait associations.

Components:

X-axis:

```
Chromosome position
```

Y-axis:

```
-log10(P-value)
```


Each point represents one SNP marker.

Higher peaks indicate SNP regions strongly associated with fruit weight.


![Manhattan Plot](docs/Manhattan_Plot.png)


---

# 4. QQ Plot

The QQ plot evaluates the quality of GWAS results.

It compares:

```
Expected statistical distribution

vs

Observed SNP associations
```

A good QQ plot follows the diagonal line.

Large deviations indicate significant SNP associations.


![QQ Plot](docs/QQ_plot.png)


---

# 5. Machine Learning Model

## XGBoost Regression

After SNP analysis, machine learning was applied to predict fruit weight.

### Input:

```
SNP genotype profile
```

Example:

```
1,3,1,3,1,...
```


### Output:

```
Predicted Fruit Weight (grams)
```


The model learns relationships between SNP combinations and fruit weight.

---

# Model Evaluation

The model performance was evaluated using:

## R² Score

R² measures how much variation in fruit weight is explained by the SNP markers.

Current model performance:

```
Mean R² ≈ 0.24
```

This indicates that SNP information explains a significant portion of fruit weight variation.


---

# 6. SHAP Explainability

Machine learning models can produce predictions but are difficult to interpret.

SHAP (SHapley Additive exPlanations) was used to identify:

- Important SNP markers
- Contribution of each SNP
- Influence on prediction


Example output:

| SNP | Mean SHAP |
|-|-|
| SSL2.50CH11_2693462 | 0.97 |
| SSL2.50CH11_1292776 | 0.76 |


![SHAP Summary](docs/SHAP_summary.png)


---

# 7. Candidate Gene Analysis

Important SNPs can be further investigated by identifying nearby genes.

Workflow:

```
Important SNP

↓

Chromosome position

↓

Nearest gene

↓

Biological function

↓

Trait association
```


Known tomato fruit-related genes include:


## FAS (FASCIATED)

Function:

- Controls carpel number
- Influences fruit size
- Affects fruit weight


## LC (LOCULE NUMBER)

Function:

- Controls locule number
- Influences fruit size


## SUN

Function:

- Controls fruit shape
- Regulates fruit elongation


---

# Web Application

A Streamlit-based web application was developed for interactive analysis.


## Features


## 1. Tomato Trait Prediction

Users can select a tomato plant ID.

The system displays:

- Actual fruit weight
- Predicted fruit weight
- Important SNP markers


Example:

```
Plant ID:
p-1-1


Actual Weight:
24.75 g


Predicted Weight:
26.1 g

```


---

## 2. GWAS Visualization

The application displays:

- Manhattan Plot
- QQ Plot


---

## 3. SHAP Dashboard

Displays:

- Top contributing SNP markers
- SHAP scores
- SNP importance ranking


---

# Project Structure

```
tomato_project/

│
├── app/
│   └── app.py
│
├── scripts/
│   ├── GWAS analysis scripts
│   ├── ML training scripts
│   └── Visualization scripts
│
├── outputs/
│   ├── GWAS results
│   ├── Model files
│   ├── SHAP results
│   └── Plots
│
├── data/
│   ├── Genotype data
│   └── Phenotype data
│
├── requirements.txt
│
└── README.md

```


---

# Technologies Used

## Programming Language

- Python


## Data Processing

- Pandas
- NumPy


## Machine Learning

- XGBoost
- Scikit-learn


## Genomics Analysis

- GWAS
- SNP analysis


## Explainable AI

- SHAP


## Web Application

- Streamlit


---

# Installation


Clone repository:

```
git clone <repository-link>
```


Install dependencies:

```
pip install -r requirements.txt
```


Run application:

```
streamlit run app/app.py
```


---

# Future Improvements

Future improvements include:

- Improve prediction accuracy using advanced models
- Include multiple tomato traits
- Add genome browser functionality
- Perform SNP-to-gene annotation
- Integrate biological pathway analysis
- Predict breeding value of tomato lines


---

# Conclusion

This project demonstrates the integration of genomics and artificial intelligence for tomato trait prediction.

The developed system can:

✓ Analyze thousands of SNP markers  
✓ Identify trait-associated genomic regions  
✓ Predict tomato fruit weight using machine learning  
✓ Explain important genetic factors using SHAP  
✓ Provide an interactive genomic prediction platform  


The project contributes towards **genomic-assisted breeding**, where genetic information can be used to accelerate crop improvement.