import matplotlib.pyplot as plt


models = [
    "XGBoost",
    "Random Forest",
    "SVR",
    "LightGBM"
]


scores = [
    0.244,
    0.276,
    0.258,
    0.277
]


plt.figure(figsize=(8,5))

plt.bar(
    models,
    scores
)


plt.ylabel("Mean R² Score")

plt.title(
    "Comparison of Machine Learning Models for Tomato Trait Prediction"
)


plt.ylim(0,0.35)


for i,v in enumerate(scores):
    plt.text(
        i,
        v+0.005,
        str(round(v,3)),
        ha="center"
    )


plt.savefig(
    "outputs/model_comparison.png",
    dpi=300,
    bbox_inches="tight"
)


plt.show()