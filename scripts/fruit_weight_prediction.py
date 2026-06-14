import pandas as pd
import numpy as np
import joblib

from xgboost import XGBRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error

print("=" * 60)
print("STEP 4 - XGBOOST GENOMIC PREDICTION")
print("=" * 60)

# =====================================================
# LOAD DATA
# =====================================================

geno = pd.read_csv(r"outputs\clean_genotype.csv")
pheno = pd.read_csv(r"outputs\clean_phenotype.csv")

print("Files Loaded")

# =====================================================
# REMOVE DUPLICATES
# =====================================================

geno = geno.drop_duplicates(subset="PlantID")
pheno = pheno.drop_duplicates(subset="PlantID")

# =====================================================
# KEEP COMMON SAMPLES
# =====================================================

common_ids = set(geno["PlantID"]).intersection(
    set(pheno["PlantID"])
)

geno = geno[geno["PlantID"].isin(common_ids)]
pheno = pheno[pheno["PlantID"].isin(common_ids)]

geno = geno.sort_values("PlantID").reset_index(drop=True)
pheno = pheno.sort_values("PlantID").reset_index(drop=True)

# =====================================================
# TARGET TRAIT
# =====================================================

trait = "BILs FW(gr)"

y = pheno[trait]

mask = ~y.isna()

y = y[mask]
geno = geno.loc[mask].reset_index(drop=True)

# =====================================================
# ALL SNPs
# =====================================================

X = geno.iloc[:, 1:]

# Convert to numeric
X = X.apply(pd.to_numeric, errors="coerce")

# Fill missing values
X = X.fillna(X.mean())

print("Feature Matrix Shape:", X.shape)

# =====================================================
# XGBOOST MODEL
# =====================================================

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

# =====================================================
# 5-FOLD CROSS VALIDATION
# =====================================================

kf = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    model,
    X,
    y,
    cv=kf,
    scoring="r2"
)

print("\nFold R² Scores:")
print(scores)

print("\nMean R²:")
print(scores.mean())

print("\nStd R²:")
print(scores.std())

# =====================================================
# TRAIN FINAL MODEL ON ALL DATA
# =====================================================

print("\nTraining Final Model...")

model.fit(X, y)

print("Model Training Complete")

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(
    model,
    r"outputs\XGBoost_model.pkl"
)

print("\nModel Saved:")
print(r"outputs\XGBoost_model.pkl")

print("\nSTEP 4 COMPLETED")
print("=" * 60)