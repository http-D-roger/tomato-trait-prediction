import pandas as pd

gwas = pd.read_csv(
    "outputs/GWAS_results.csv"
)

chromosomes = []
positions = []

for snp in gwas["SNP"]:

    parts = snp.split("_")

    chrom = (
        parts[0]
        .replace("SSL2.50CH", "")
    )

    pos = int(parts[1])

    chromosomes.append(
        int(chrom)
    )

    positions.append(pos)

gwas["Chromosome"] = chromosomes
gwas["Position"] = positions

gwas.to_csv(
    "outputs/GWAS_results_fixed.csv",
    index=False
)

print("Saved:")
print("outputs/GWAS_results_fixed.csv")