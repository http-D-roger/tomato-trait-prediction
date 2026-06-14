import pandas as pd
import numpy as np

from xgboost import XGBRegressor

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

print("=" * 50)
print("XGBOOST USING TOP 100 GWAS SNPs")
print("=" * 50)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

geno = pd.read_csv(
    "outputs/clean_genotype.csv"
)

pheno = pd.read_csv(
    "outputs/clean_phenotype.csv"
)

gwas = pd.read_csv(
    "outputs/top1000_snps.csv"
)

print("Files Loaded")

# --------------------------------------------------
# SELECT TOP SNPs
# --------------------------------------------------

selected_snps = gwas["SNP"].tolist()

print(
    f"Selected SNPs: {len(selected_snps)}"
)

# --------------------------------------------------
# FEATURE MATRIX
# --------------------------------------------------

X = geno[selected_snps]

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

X = X.fillna(
    X.mean()
)

# --------------------------------------------------
# TARGET TRAIT
# --------------------------------------------------

y = pheno["BILs FW(gr)"]

mask = y.notna()

X = X.loc[mask]

y = y.loc[mask]

print(
    f"Feature Matrix Shape: {X.shape}"
)

# --------------------------------------------------
# MODEL
# --------------------------------------------------

model = XGBRegressor(
    n_estimators=1000,
    max_depth=4,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# --------------------------------------------------
# CROSS VALIDATION
# --------------------------------------------------

cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="r2"
)

print("\nFold R² Scores:")
print(scores)

print("\nMean R²:")
print(scores.mean())

print("\nSTEP COMPLETE")
print("=" * 50)