import pandas as pd
import numpy as np
import shap
import joblib
import matplotlib.pyplot as plt

print("=" * 60)
print("STEP 5 - SHAP INTERPRETABILITY")
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
# ALIGN SAMPLES
# =====================================================

common_ids = set(geno["PlantID"]).intersection(
    set(pheno["PlantID"])
)

geno = geno[geno["PlantID"].isin(common_ids)]
pheno = pheno[pheno["PlantID"].isin(common_ids)]

geno = geno.sort_values("PlantID").reset_index(drop=True)
pheno = pheno.sort_values("PlantID").reset_index(drop=True)

# =====================================================
# TARGET
# =====================================================

trait = "BILs FW(gr)"

y = pheno[trait]

mask = ~y.isna()

y = y[mask]

geno = geno.loc[mask].reset_index(drop=True)

# =====================================================
# FEATURE MATRIX
# =====================================================

X = geno.iloc[:,1:]

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

X = X.fillna(
    X.mean()
)

print("Feature Matrix Shape:", X.shape)

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load(
    r"outputs\XGBoost_model.pkl"
)

print("Model Loaded")

# =====================================================
# SHAP EXPLAINER
# =====================================================

print("Calculating SHAP values...")

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(X)

print("SHAP Complete")

# =====================================================
# SHAP SUMMARY PLOT
# =====================================================

plt.figure()

shap.summary_plot(
    shap_values,
    X,
    show=False
)

plt.tight_layout()

plt.savefig(
    r"outputs\SHAP_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Saved SHAP_summary.png")

# =====================================================
# SHAP BAR PLOT
# =====================================================

plt.figure()

shap.summary_plot(
    shap_values,
    X,
    plot_type="bar",
    show=False
)

plt.tight_layout()

plt.savefig(
    r"outputs\SHAP_bar.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Saved SHAP_bar.png")

# =====================================================
# TOP SNPs
# =====================================================

importance = np.abs(
    shap_values
).mean(axis=0)

importance_df = pd.DataFrame({
    "SNP": X.columns,
    "Mean_SHAP": importance
})

importance_df = importance_df.sort_values(
    "Mean_SHAP",
    ascending=False
)

top20 = importance_df.head(20)

top20.to_csv(
    r"outputs\Top20_SNPs_SHAP.csv",
    index=False
)

print("\nTOP 20 SNPs")

print(top20)

print("\nSaved:")
print("outputs\\Top20_SNPs_SHAP.csv")

print("\nSTEP 5 COMPLETED")
print("=" * 60)