import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

print("=" * 60)
print("STEP 3 - GWAS")
print("=" * 60)

# ==================================================
# LOAD FILES
# ==================================================

geno = pd.read_csv(r"outputs\clean_genotype.csv")
pheno = pd.read_csv(r"outputs\clean_phenotype.csv")
pca = pd.read_csv(r"outputs\PCA_coordinates.csv")

print("Files loaded")

# ==================================================
# REMOVE DUPLICATE PLANT IDs
# ==================================================

geno = geno.drop_duplicates(subset="PlantID", keep="first")
pheno = pheno.drop_duplicates(subset="PlantID", keep="first")
pca = pca.drop_duplicates(subset="PlantID", keep="first")

# ==================================================
# SORT DATA
# ==================================================

geno = geno.sort_values("PlantID").reset_index(drop=True)
pheno = pheno.sort_values("PlantID").reset_index(drop=True)
pca = pca.sort_values("PlantID").reset_index(drop=True)

print("\nAfter removing duplicates:")
print("Genotype rows :", len(geno))
print("Phenotype rows:", len(pheno))
print("PCA rows      :", len(pca))

# ==================================================
# PHENOTYPE COLUMN
# ==================================================

print("\nPhenotype Columns:")
print(pheno.columns.tolist())

trait = "BILs FW(gr)"

print("\nTarget Trait:", trait)

# ==================================================
# FIND COMMON IDS
# ==================================================

common_ids = set(geno["PlantID"]) \
    .intersection(set(pheno["PlantID"])) \
    .intersection(set(pca["PlantID"]))

print("\nCommon IDs:", len(common_ids))

# ==================================================
# KEEP ONLY COMMON SAMPLES
# ==================================================

geno = geno[geno["PlantID"].isin(common_ids)]
pheno = pheno[pheno["PlantID"].isin(common_ids)]
pca = pca[pca["PlantID"].isin(common_ids)]

geno = geno.sort_values("PlantID").reset_index(drop=True)
pheno = pheno.sort_values("PlantID").reset_index(drop=True)
pca = pca.sort_values("PlantID").reset_index(drop=True)

print("Genotype samples :", len(geno))
print("Phenotype samples:", len(pheno))
print("PCA samples      :", len(pca))

# ==================================================
# FINAL CHECK
# ==================================================

if not (
    len(geno) == len(pheno) == len(pca)
):
    raise ValueError(
        "Sample counts still do not match."
    )

# ==================================================
# TARGET VARIABLE
# ==================================================

y = pheno[trait].values

# Remove phenotype NA values

valid_mask = ~pd.isna(y)

y = y[valid_mask]

geno = geno.loc[valid_mask].reset_index(drop=True)
pheno = pheno.loc[valid_mask].reset_index(drop=True)
pca = pca.loc[valid_mask].reset_index(drop=True)

print("\nSamples after NA removal:", len(y))

# ==================================================
# PCA COVARIATES
# ==================================================

pc1 = pca["PC1"].values
pc2 = pca["PC2"].values
pc3 = pca["PC3"].values

# ==================================================
# SNP LIST
# ==================================================

snp_cols = geno.columns[1:]

print("Total SNPs:", len(snp_cols))

# ==================================================
# GWAS LOOP
# ==================================================

results = []

for i, snp in enumerate(snp_cols):

    try:

        snp_values = pd.to_numeric(
            geno[snp],
            errors="coerce"
        )

        snp_values = snp_values.fillna(
            snp_values.mean()
        )

        X = pd.DataFrame({
            "SNP": snp_values.values,
            "PC1": pc1,
            "PC2": pc2,
            "PC3": pc3
        })

        X = sm.add_constant(X)

        model = sm.OLS(
            y,
            X
        ).fit()

        pvalue = model.pvalues["SNP"]

        results.append([
            snp,
            pvalue
        ])

        if i % 500 == 0:
            print(
                f"Processed {i}/{len(snp_cols)} SNPs"
            )

    except Exception as e:

        print(f"Failed SNP: {snp}")
        print(e)

# ==================================================
# RESULTS
# ==================================================

gwas_results = pd.DataFrame(
    results,
    columns=[
        "SNP",
        "P_value"
    ]
)

print(
    "\nSuccessful SNP tests:",
    len(gwas_results)
)

if len(gwas_results) == 0:
    raise ValueError(
        "No GWAS results generated"
    )

# ==================================================
# -LOG10(P)
# ==================================================

gwas_results["minus_log10_p"] = (
    -np.log10(gwas_results["P_value"])
)

# ==================================================
# SORT RESULTS
# ==================================================

gwas_results = gwas_results.sort_values(
    "P_value"
)

# ==================================================
# SAVE GWAS TABLE
# ==================================================

gwas_results.to_csv(
    r"outputs\GWAS_results.csv",
    index=False
)

print("GWAS_results.csv saved")

# ==================================================
# TOP 100 SNPs
# ==================================================

top100 = gwas_results.head(100)

top100.to_csv(
    r"outputs\Top100_SNPs.csv",
    index=False
)

print("Top100_SNPs.csv saved")

# ==================================================
# MANHATTAN PLOT
# ==================================================

plt.figure(figsize=(14, 6))

plt.scatter(
    range(len(gwas_results)),
    gwas_results["minus_log10_p"],
    s=8
)

plt.xlabel("SNP Index")
plt.ylabel("-log10(P)")
plt.title("GWAS Manhattan Plot")

plt.tight_layout()

plt.savefig(
    r"outputs\Manhattan_FW.png",
    dpi=300
)

plt.close()

print("Manhattan_FW.png saved")

# ==================================================
# QQ PLOT
# ==================================================

observed = np.sort(
    gwas_results["P_value"]
)

expected = np.arange(
    1,
    len(observed) + 1
) / (len(observed) + 1)

plt.figure(figsize=(6, 6))

plt.scatter(
    -np.log10(expected),
    -np.log10(observed),
    s=8
)

max_val = max(
    -np.log10(expected)
)

plt.plot(
    [0, max_val],
    [0, max_val]
)

plt.xlabel("Expected -log10(P)")
plt.ylabel("Observed -log10(P)")
plt.title("QQ Plot")

plt.tight_layout()

plt.savefig(
    r"outputs\QQ_FW.png",
    dpi=300
)

plt.close()

print("QQ_FW.png saved")

print("\nTop 10 SNPs:")
print(gwas_results.head(10))

print("\nSTEP 3 COMPLETED")
print("=" * 60)