import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

print("="*60)
print("STEP 2 - PCA POPULATION STRUCTURE ANALYSIS")
print("="*60)

# --------------------------------------------------
# LOAD CLEAN GENOTYPE DATA
# --------------------------------------------------

geno = pd.read_csv(
    r"outputs\clean_genotype.csv"
)

print("Loaded genotype data")

print("Shape:", geno.shape)

# --------------------------------------------------
# SEPARATE IDs AND SNPs
# --------------------------------------------------

plant_ids = geno["PlantID"]

X = geno.drop(
    columns=["PlantID"]
)

print("SNP Matrix Shape:", X.shape)

# --------------------------------------------------
# STANDARDIZE DATA
# --------------------------------------------------

print("\nStandardizing SNP data...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("Standardization complete")

# --------------------------------------------------
# RUN PCA
# --------------------------------------------------

print("\nRunning PCA...")

pca = PCA(n_components=10)

pcs = pca.fit_transform(X_scaled)

print("PCA completed")

# --------------------------------------------------
# CREATE PCA DATAFRAME
# --------------------------------------------------

pca_df = pd.DataFrame(
    pcs,
    columns=[
        "PC1","PC2","PC3","PC4","PC5",
        "PC6","PC7","PC8","PC9","PC10"
    ]
)

pca_df.insert(
    0,
    "PlantID",
    plant_ids
)

# --------------------------------------------------
# SAVE PCA COORDINATES
# --------------------------------------------------

pca_df.to_csv(
    r"outputs\PCA_coordinates.csv",
    index=False
)

print("PCA coordinates saved")

# --------------------------------------------------
# EXPLAINED VARIANCE
# --------------------------------------------------

variance = pca.explained_variance_ratio_

variance_df = pd.DataFrame({
    "PC":[
        "PC1","PC2","PC3","PC4","PC5",
        "PC6","PC7","PC8","PC9","PC10"
    ],
    "Variance":variance
})

variance_df.to_csv(
    r"outputs\PCA_variance.csv",
    index=False
)

print("\nExplained Variance")

for i,v in enumerate(variance):
    print(
        f"PC{i+1}: {v*100:.2f}%"
    )

# --------------------------------------------------
# PCA SCATTER PLOT
# --------------------------------------------------

plt.figure(figsize=(8,6))

sns.scatterplot(
    x=pca_df["PC1"],
    y=pca_df["PC2"]
)

plt.title(
    "Population Structure PCA"
)

plt.xlabel(
    f"PC1 ({variance[0]*100:.2f}%)"
)

plt.ylabel(
    f"PC2 ({variance[1]*100:.2f}%)"
)

plt.tight_layout()

plt.savefig(
    r"outputs\PCA_structure.png",
    dpi=300
)

plt.close()

print("PCA structure plot saved")

# --------------------------------------------------
# SCREE PLOT
# --------------------------------------------------

plt.figure(figsize=(8,5))

plt.plot(
    range(1,11),
    variance,
    marker="o"
)

plt.xlabel(
    "Principal Component"
)

plt.ylabel(
    "Explained Variance Ratio"
)

plt.title(
    "Scree Plot"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    r"outputs\Scree_plot.png",
    dpi=300
)

plt.close()

print("Scree plot saved")

print("\nSTEP 2 COMPLETED")

print("="*60)