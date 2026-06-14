import pandas as pd

gwas = pd.read_csv("outputs/GWAS_results.csv")

print("Min p-value:")
print(gwas["P_value"].min())

print("\nSNPs with p < 0.05:")
print((gwas["P_value"] < 0.05).sum())

print("\nSNPs with p < 0.01:")
print((gwas["P_value"] < 0.01).sum())