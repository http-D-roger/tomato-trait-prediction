import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

import joblib


print("="*60)
print("RANDOM FOREST GENOMIC PREDICTION")
print("="*60)


# ===============================
# LOAD DATA
# ===============================

geno = pd.read_csv(
    "outputs/clean_genotype.csv"
)

pheno = pd.read_csv(
    "outputs/clean_phenotype.csv"
)


print("Files Loaded")


# ===============================
# PREPARE FEATURES
# ===============================

# Select SNP features
X = geno.iloc[:,1:]

# Target trait
y = pheno["BILs FW(gr)"]


# Remove samples where fruit weight is missing
valid = y.notna()

X = X[valid]
y = y[valid]


print("After removing missing values:")
print("Features:", X.shape)
print("Target:", y.shape)


print("Feature Matrix Shape:")
print(X.shape)


# ===============================
# RANDOM FOREST MODEL
# ===============================

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    max_features="sqrt",
    n_jobs=-1
)


# ===============================
# CROSS VALIDATION
# ===============================

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


# ===============================
# TRAIN FINAL MODEL
# ===============================

print("\nTraining Final Random Forest Model...")

model.fit(
    X,
    y
)


print("Training Complete")


# ===============================
# SAVE MODEL
# ===============================

joblib.dump(
    model,
    "outputs/RandomForest_model.pkl"
)


print("\nModel Saved:")
print("outputs/RandomForest_model.pkl")


print("="*60)
print("STEP COMPLETE")
print("="*60)