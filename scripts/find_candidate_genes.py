import pandas as pd

snps = pd.read_csv(
    "outputs/Annotated_SHAP_SNPs.csv"
)

genes = pd.read_csv(
    "outputs/Known_Tomato_Genes.csv"
)

results = []

for _, snp in snps.iterrows():

    same_chr = genes[
        genes["Chromosome"]
        == int(snp["Chromosome"])
    ]

    if len(same_chr) == 0:
        continue

    same_chr["Distance"] = (
        abs(
            same_chr["Position"]
            - snp["Position"]
        )
    )

    nearest = same_chr.sort_values(
        "Distance"
    ).iloc[0]

    results.append({

        "SNP": snp["SNP"],
        "Chromosome": snp["Chromosome"],
        "SNP_Position": snp["Position"],
        "Nearest_Gene": nearest["Gene"],
        "Gene_Position": nearest["Position"],
        "Distance": nearest["Distance"]
    })

candidate_df = pd.DataFrame(results)

print(candidate_df)

candidate_df.to_csv(
    "outputs/Candidate_Genes.csv",
    index=False
)

print("\nSaved:")
print("outputs/Candidate_Genes.csv")