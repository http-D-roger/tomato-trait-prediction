import pandas as pd
import matplotlib.pyplot as plt
import joblib


geno = pd.read_csv(
"outputs/clean_genotype.csv"
)


pheno = pd.read_csv(
"outputs/clean_phenotype.csv"
)


model = joblib.load(
"outputs/LightGBM_model.pkl"
)


X = geno.iloc[:,1:]

y = pheno["BILs FW(gr)"]


valid = y.notna()

X=X[valid]

y=y[valid]


pred=model.predict(X)



plt.figure(figsize=(6,6))


plt.scatter(
    y,
    pred
)


plt.xlabel(
    "Actual Fruit Weight (g)"
)


plt.ylabel(
    "Predicted Fruit Weight (g)"
)


plt.title(
"LightGBM Predicted vs Actual Fruit Weight"
)


plt.plot(
[y.min(),y.max()],
[y.min(),y.max()]
)


plt.savefig(
"outputs/predicted_vs_actual.png",
dpi=300,
bbox_inches="tight"
)


plt.show()