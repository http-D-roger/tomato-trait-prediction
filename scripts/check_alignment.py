import pandas as pd

geno = pd.read_csv("outputs/clean_genotype.csv")
pheno = pd.read_csv("outputs/clean_phenotype.csv")

print("Genotype IDs:")
print(geno.iloc[:10,0].tolist())

print("\nPhenotype IDs:")
print(pheno.iloc[:10,0].tolist())