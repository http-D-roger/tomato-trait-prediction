import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="Tomato Trait Prediction System",
    layout="wide"
)

st.title("🍅 Tomato Trait Prediction System")

# ====================================
# PATHS
# ====================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUTS = BASE_DIR / "outputs"

GENO_PATH = OUTPUTS / "clean_genotype.csv"
PHENO_PATH = OUTPUTS / "clean_phenotype.csv"
MODEL_PATH = OUTPUTS / "XGBoost_model.pkl"
SHAP_PATH = OUTPUTS / "Top20_SNPs_SHAP.csv"
GENE_PATH = OUTPUTS / "Candidate_Genes.csv"

MANHATTAN_PATH = OUTPUTS / "Manhattan_Plot_Correct.png"
QQ_PATH = OUTPUTS / "QQ_FW.png"

# ====================================
# LOAD DATA
# ====================================

@st.cache_data
def load_data():

    geno = pd.read_csv(GENO_PATH)

    pheno = pd.read_csv(PHENO_PATH)

    shap_df = pd.read_csv(SHAP_PATH)

    genes_df = pd.read_csv(GENE_PATH)

    return geno, pheno, shap_df, genes_df


geno, pheno, shap_df, genes_df = load_data()

model = joblib.load(MODEL_PATH)

# ====================================
# TABS
# ====================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Trait Prediction",
        "Manhattan Plot",
        "QQ Plot",
        "SHAP Dashboard",
        "Genome Explorer"
    ]
)

# ====================================
# TAB 1
# ====================================

with tab1:

    st.subheader("Predict Tomato Traits")

    plant_id = st.selectbox(
        "Select Plant ID",
        pheno["PlantID"].tolist()
    )

    if st.button("Predict Traits"):

        idx = pheno[
            pheno["PlantID"] == plant_id
        ].index[0]

        X = geno.iloc[idx, 1:]

        prediction = model.predict([X])[0]

        actual_fw = pheno.loc[
            idx,
            "BILs FW(gr)"
        ]

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Actual Fruit Weight",
                f"{actual_fw:.2f} g"
            )

        with col2:

            st.metric(
                "Predicted Fruit Weight",
                f"{prediction:.2f} g"
            )

        st.markdown("---")

        st.subheader(
            "Top Important SNPs (SHAP)"
        )

        st.dataframe(
            shap_df.head(10),
            width="stretch"
        )

        st.markdown("---")

        st.subheader(
            "Candidate Genes"
        )

        if "Nearest_Gene" in genes_df.columns:

            st.dataframe(
                genes_df[
                    ["SNP", "Nearest_Gene"]
                ],
                width="stretch"
            )

        else:

            st.dataframe(
                genes_df,
                width="stretch"
            )

        st.markdown("---")

        st.subheader(
            "Biological Interpretation"
        )

        st.success(
            """
            The prediction is influenced by SNPs
            identified through GWAS and SHAP analysis.

            Important SNPs are located near
            candidate tomato fruit-size genes.

            These genomic regions may contribute
            to variation in fruit weight.
            """
        )

# ====================================
# TAB 2
# ====================================

with tab2:

    st.subheader(
        "GWAS Manhattan Plot"
    )

    if MANHATTAN_PATH.exists():

        st.image(
            str(MANHATTAN_PATH),
            caption="GWAS Manhattan Plot",
            width="stretch"
        )

    else:

        st.error(
            f"File not found:\n{MANHATTAN_PATH}"
        )

    st.markdown(
        """
### Interpretation

- Each dot represents a SNP marker.
- X-axis represents chromosome locations.
- Y-axis represents −log10(P-value).
- Higher peaks indicate stronger association with fruit weight.
"""
    )

# ====================================
# TAB 3
# ====================================

with tab3:

    st.subheader(
        "GWAS QQ Plot"
    )

    if QQ_PATH.exists():

        st.image(
            str(QQ_PATH),
            caption="GWAS QQ Plot",
            width="stretch"
        )

    else:

        st.error(
            f"File not found:\n{QQ_PATH}"
        )

    st.markdown(
        """
### Interpretation

- Compares expected and observed P-values.
- Points close to the diagonal indicate good calibration.
- Large upward deviations indicate significant SNP associations.
"""
    )

    # ====================================
# TAB 4
# ====================================

with tab4:

    st.subheader("SHAP Explanation Dashboard")

    st.write(
        """
        SHAP (SHapley Additive exPlanations) identifies
        which SNPs contribute most to fruit weight prediction.
        """
    )

    st.subheader("Top SNPs by SHAP Importance")

    st.dataframe(
        shap_df,
        width="stretch"
    )

    st.subheader("Top 10 SNPs")

    chart_df = (
        shap_df
        .head(10)
        .set_index("SNP")
    )

    st.bar_chart(
        chart_df["Mean_SHAP"]
    )

    selected_snp = st.selectbox(
        "Select SNP",
        shap_df["SNP"].tolist(),
        key="shap_snp"
    )

    row = shap_df[
        shap_df["SNP"] == selected_snp
    ].iloc[0]

    st.metric(
        "Mean SHAP Score",
        f"{row['Mean_SHAP']:.4f}"
    )

    st.info(
        f"""
Selected SNP:
{selected_snp}

SHAP Importance:
{row['Mean_SHAP']:.4f}

A larger SHAP score indicates a stronger
influence on fruit weight prediction.
"""
    )

# ====================================
# TAB 5
# ====================================

with tab5:

    st.subheader("Genome Explorer")

    if genes_df.empty:

        st.warning(
            "Candidate_Genes.csv is empty."
        )

    else:

        selected_gene_snp = st.selectbox(
            "Select SNP Marker",
            genes_df["SNP"].tolist(),
            key="genome_snp"
        )

        result = genes_df[
            genes_df["SNP"] == selected_gene_snp
        ].iloc[0]

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            if "Chromosome" in genes_df.columns:

                st.metric(
                    "Chromosome",
                    result["Chromosome"]
                )

            if "Position" in genes_df.columns:

                st.metric(
                    "Position",
                    result["Position"]
                )

        with col2:

            if "Nearest_Gene" in genes_df.columns:

                st.metric(
                    "Nearest Gene",
                    result["Nearest_Gene"]
                )

        st.markdown("---")

        st.subheader("SNP Information")

        st.dataframe(
            pd.DataFrame([result]),
            width="stretch"
        )

        st.markdown("---")

        st.subheader(
            "Biological Interpretation"
        )

        gene_name = (
            result["Nearest_Gene"]
            if "Nearest_Gene" in genes_df.columns
            else "Unknown"
        )

        st.success(
            f"""
SNP Marker:
{selected_gene_snp}

Nearest Gene:
{gene_name}

This SNP was identified as a significant
genomic region associated with tomato
fruit weight.

Such SNPs can be used as candidate
markers for marker-assisted breeding.
"""
        )