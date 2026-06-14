import pandas as pd

gwas = pd.read_csv(
    "outputs/GWAS_results.csv"
)

print(gwas.head())

print("\nTotal SNPs:")
print(len(gwas))

top500 = gwas.sort_values(
    "P_value"
).head(1000)

top500.to_csv(
    "outputs/top1000_snps.csv",
    index=False
)

print("\nTop 1000 SNPs saved")