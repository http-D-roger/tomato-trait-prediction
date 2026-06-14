import pandas as pd

geno = pd.read_csv("outputs/clean_genotype.csv")

print(geno.iloc[:,1:].stack().value_counts().head(20))