import pandas as pd

print("="*50)
print("STEP 6 - SNP ANNOTATION")
print("="*50)

# Load SHAP results
shap_df = pd.read_csv(
    "outputs/Top20_SNPs_SHAP.csv"
)

annotations = []

for snp in shap_df["SNP"]:

    try:

        parts = snp.split("_")

        chrom = (
            parts[0]
            .replace("SSL2.50CH","")
        )

        position = int(parts[1])

        annotations.append([
            snp,
            chrom,
            position
        ])

    except:

        annotations.append([
            snp,
            "Unknown",
            None
        ])

annotation_df = pd.DataFrame(
    annotations,
    columns=[
        "SNP",
        "Chromosome",
        "Position"
    ]
)

result = pd.merge(
    shap_df,
    annotation_df,
    on="SNP"
)

print(result)

result.to_csv(
    "outputs/Annotated_SHAP_SNPs.csv",
    index=False
)

print("\nSaved:")
print("outputs/Annotated_SHAP_SNPs.csv")