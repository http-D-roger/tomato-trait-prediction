import pandas as pd
import numpy as np

from lightgbm import LGBMRegressor

from sklearn.model_selection import KFold, cross_val_score

import joblib


print("="*60)
print("LIGHTGBM GENOMIC PREDICTION")
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
# LIGHTGBM MODEL
# ==================================

model = LGBMRegressor(

    n_estimators=500,

    learning_rate=0.03,

    max_depth=6,

    num_leaves=31,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42,

    n_jobs=-1
)



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

print("\nTraining Final LightGBM Model...")


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

    "outputs/LightGBM_model.pkl"

)


print("\nModel Saved:")

print(
    "outputs/LightGBM_model.pkl"
)


print("="*60)
print("STEP COMPLETE")
print("="*60)