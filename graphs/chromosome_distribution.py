import pandas as pd
import matplotlib.pyplot as plt
import os


os.makedirs(
    "outputs/graphs",
    exist_ok=True
)


# Load GWAS result

gwas = pd.read_csv(
    "outputs/GWAS_results_fixed.csv"
)


print("Columns available:")
print(gwas.columns)


# Detect chromosome column automatically

possible_cols = [
    "Chr",
    "CHR",
    "Chromosome",
    "chromosome",
    "chr"
]


chr_column = None


for col in possible_cols:
    if col in gwas.columns:
        chr_column = col
        break


if chr_column is None:
    raise Exception(
        "Chromosome column not found in GWAS file"
    )


print(
    "Using chromosome column:",
    chr_column
)


# Count SNPs per chromosome

count = (
    gwas[chr_column]
    .value_counts()
    .sort_index()
)


# Plot

plt.figure(
    figsize=(10,5)
)


plt.bar(
    count.index.astype(str),
    count.values
)


plt.xlabel(
    "Chromosome"
)


plt.ylabel(
    "Number of SNPs"
)


plt.title(
    "Distribution of SNP Markers Across Tomato Chromosomes"
)


plt.savefig(
    "outputs/graphs/chromosome_SNP_distribution.png",
    dpi=300,
    bbox_inches="tight"
)


plt.show()