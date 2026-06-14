import pandas as pd

pheno = pd.read_csv("outputs/clean_phenotype.csv")

trait = "BILs FW(gr)"

print(pheno[trait].describe())