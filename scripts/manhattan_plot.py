import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

gwas = pd.read_csv(
    "outputs/GWAS_results_fixed.csv"
)

gwas = gwas.sort_values(
    ["Chromosome", "Position"]
)

gwas["index"] = range(
    len(gwas)
)

colors = [
    "blue",
    "orange",
    "green",
    "red",
    "purple",
    "brown",
    "pink",
    "gray",
    "olive",
    "cyan",
    "magenta",
    "black"
]

plt.figure(figsize=(14,6))

for chrom in sorted(
    gwas["Chromosome"].unique()
):

    subset = gwas[
        gwas["Chromosome"] == chrom
    ]

    plt.scatter(
        subset["index"],
        subset["minus_log10_p"],
        s=10,
        color=colors[
            chrom % len(colors)
        ],
        label=f"Chr{chrom}"
    )

threshold = -np.log10(
    0.05 / len(gwas)
)

plt.axhline(
    threshold,
    color="red",
    linestyle="--"
)

plt.xlabel("Chromosome")
plt.ylabel("-log10(P)")
plt.title("GWAS Manhattan Plot")

plt.tight_layout()

plt.savefig(
    "outputs/Manhattan_Plot_Correct.png",
    dpi=300
)

plt.show()