import pandas as pd

known_genes = pd.DataFrame({

    "Gene":[
        "fw2.2",
        "lc",
        "fas",
        "sun",
        "ovate"
    ],

    "Chromosome":[
        2,
        2,
        11,
        7,
        2
    ],

    "Position":[
        47000000,
        52000000,
        54000000,
        65000000,
        2500000
    ]
})

known_genes.to_csv(
    "outputs/Known_Tomato_Genes.csv",
    index=False
)

print(known_genes)