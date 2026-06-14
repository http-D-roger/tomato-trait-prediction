import pandas as pd
import numpy as np

print("="*60)
print("TOMATO GWAS PROJECT - STEP 1")
print("DATA CLEANING & PREPROCESSING")
print("="*60)

# --------------------------------------------------
# LOAD FILES
# --------------------------------------------------

geno_path = r"data\Genotypic_DATA.csv"
pheno_path = r"data\Phenotypic_DATA.csv"

print("\nLoading files...")

geno = pd.read_csv(geno_path)
pheno = pd.read_csv(pheno_path)

print("Genotype Shape:", geno.shape)
print("Phenotype Shape:", pheno.shape)

# --------------------------------------------------
# SAVE METADATA ROWS
# --------------------------------------------------

print("\nExtracting chromosome information...")

chromosome_info = geno.iloc[0]
position_info = geno.iloc[1]

chromosome_info.to_csv(
    r"outputs\chromosome_info.csv"
)

position_info.to_csv(
    r"outputs\position_info.csv"
)

print("Metadata saved")

# --------------------------------------------------
# REMOVE FIRST TWO METADATA ROWS
# --------------------------------------------------

print("\nRemoving metadata rows...")

geno_clean = geno.iloc[2:].copy()

print("Genotype shape after cleaning:",
      geno_clean.shape)

# --------------------------------------------------
# RENAME FIRST COLUMN
# --------------------------------------------------

first_col = geno_clean.columns[0]

geno_clean.rename(
    columns={first_col:"PlantID"},
    inplace=True
)

pheno.rename(
    columns={pheno.columns[0]:"PlantID"},
    inplace=True
)

print("Plant ID column renamed")

# --------------------------------------------------
# RESET INDEX
# --------------------------------------------------

geno_clean.reset_index(
    drop=True,
    inplace=True
)

pheno.reset_index(
    drop=True,
    inplace=True
)

# --------------------------------------------------
# CONVERT SNPs TO NUMERIC
# --------------------------------------------------

print("\nConverting SNP markers to numeric...")

snp_columns = geno_clean.columns[1:]

for col in snp_columns:
    geno_clean[col] = pd.to_numeric(
        geno_clean[col],
        errors='coerce'
    )

print("Conversion complete")

# --------------------------------------------------
# CHECK MISSING VALUES
# --------------------------------------------------

missing_before = geno_clean.isna().sum().sum()

print("\nMissing values before filling:",
      missing_before)

# --------------------------------------------------
# FILL MISSING VALUES
# --------------------------------------------------

print("\nFilling missing values...")

geno_clean[snp_columns] = geno_clean[
    snp_columns
].fillna(
    geno_clean[snp_columns].mean()
)

missing_after = geno_clean.isna().sum().sum()

print("Missing values after filling:",
      missing_after)

# --------------------------------------------------
# FIND COMMON PLANT IDs
# --------------------------------------------------

print("\nMatching genotype and phenotype samples...")

common_ids = set(
    geno_clean["PlantID"]
).intersection(
    set(pheno["PlantID"])
)

print("Common samples:",
      len(common_ids))

# --------------------------------------------------
# KEEP ONLY MATCHING SAMPLES
# --------------------------------------------------

geno_clean = geno_clean[
    geno_clean["PlantID"].isin(common_ids)
]

pheno = pheno[
    pheno["PlantID"].isin(common_ids)
]

print("Genotype after matching:",
      geno_clean.shape)

print("Phenotype after matching:",
      pheno.shape)

# --------------------------------------------------
# SORT BY PLANT ID
# --------------------------------------------------

geno_clean = geno_clean.sort_values(
    "PlantID"
)

pheno = pheno.sort_values(
    "PlantID"
)

# --------------------------------------------------
# MERGE
# --------------------------------------------------

print("\nMerging datasets...")

merged = pd.merge(
    geno_clean,
    pheno,
    on="PlantID"
)

print("Merged Shape:",
      merged.shape)

# --------------------------------------------------
# SAVE FILES
# --------------------------------------------------

geno_clean.to_csv(
    r"outputs\clean_genotype.csv",
    index=False
)

pheno.to_csv(
    r"outputs\clean_phenotype.csv",
    index=False
)

merged.to_csv(
    r"outputs\merged_dataset.csv",
    index=False
)

print("\nFiles saved successfully")

print("\nOutput files:")
print("clean_genotype.csv")
print("clean_phenotype.csv")
print("merged_dataset.csv")

print("\nSTEP 1 COMPLETED")
print("="*60)