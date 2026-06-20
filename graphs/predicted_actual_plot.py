import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os


os.makedirs(
    "outputs/graphs",
    exist_ok=True
)


# Load data

geno = pd.read_csv(
    "outputs/clean_genotype.csv"
)

pheno = pd.read_csv(
    "outputs/clean_phenotype.csv"
)


X = geno.iloc[:,1:]

y = pheno["BILs FW(gr)"]


# Remove missing values

data = pd.concat(
    [X,y],
    axis=1
)

data = data.dropna()


X = data.iloc[:,:-1]

y = data.iloc[:,-1]


models = {

    "XGBoost":
    "outputs/XGBoost_model.pkl",

    "Random Forest":
    "outputs/RandomForest_model.pkl",

    "SVR":
    "outputs/SVR_model.pkl",

    "LightGBM":
    "outputs/LightGBM_model.pkl"

}



for name,path in models.items():

    print(
        "Generating:",
        name
    )


    model = joblib.load(path)


    predictions = model.predict(X)


    plt.figure(
        figsize=(7,6)
    )


    plt.scatter(
        y,
        predictions
    )


    # Perfect prediction line

    minimum = min(
        y.min(),
        predictions.min()
    )

    maximum = max(
        y.max(),
        predictions.max()
    )


    plt.plot(
        [minimum,maximum],
        [minimum,maximum]
    )


    plt.xlabel(
        "Actual Fruit Weight (g)"
    )


    plt.ylabel(
        "Predicted Fruit Weight (g)"
    )


    plt.title(
        f"{name}: Predicted vs Actual Fruit Weight"
    )


    plt.grid()


    filename = (
        name
        .lower()
        .replace(" ","_")
        +
        "_predicted_actual.png"
    )


    plt.savefig(
        f"outputs/{filename}",
        dpi=300,
        bbox_inches="tight"
    )


    plt.close()


print(
    "All graphs generated successfully"
)