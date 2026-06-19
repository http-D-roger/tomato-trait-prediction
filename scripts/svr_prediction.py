import pandas as pd
import numpy as np

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.model_selection import KFold, cross_val_score

import joblib


print("="*60)
print("SVR GENOMIC PREDICTION")
print("="*60)


# ==================================
# LOAD DATA
# ==================================

geno = pd.read_csv(
    "outputs/clean_genotype.csv"
)

pheno = pd.read_csv(
    "outputs/clean_phenotype.csv"
)


print("Files Loaded")


# ==================================
# PREPARE DATA
# ==================================

X = geno.iloc[:,1:]

y = pheno["BILs FW(gr)"]


# Remove missing phenotype values

valid = y.notna()

X = X[valid]

y = y[valid]


print("\nAfter removing missing values:")

print("Features:")
print(X.shape)

print("Target:")
print(y.shape)



# ==================================
# SVR MODEL
# ==================================

model = Pipeline([

    ("scaler", StandardScaler()),

    ("svr", SVR(
        kernel="rbf",
        C=100,
        gamma="scale",
        epsilon=0.1
    ))

])


# ==================================
# CROSS VALIDATION
# ==================================

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



# ==================================
# TRAIN FINAL MODEL
# ==================================

print("\nTraining Final SVR Model...")


model.fit(
    X,
    y
)


print("Training Complete")



# ==================================
# SAVE MODEL
# ==================================

joblib.dump(
    model,
    "outputs/SVR_model.pkl"
)


print("\nModel Saved:")

print(
    "outputs/SVR_model.pkl"
)


print("="*60)
print("STEP COMPLETE")
print("="*60)