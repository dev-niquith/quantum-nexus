from pathlib import Path
import sys
import json

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT))

from backend.predict import predict_smiles


# ----------------------------
# Load Metrics
# ----------------------------

METRICS_PATH = (
    ROOT /
    "models" /
    "trained" /
    "metrics.json"
)

with open(METRICS_PATH, "r") as f:
    metrics = json.load(f)

importance_df = pd.DataFrame(
    metrics["feature_importance"].items(),
    columns=["Feature", "Importance"]
)

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

from backend.report_generator import (
    generate_report
)

# ----------------------------
# UI
# ----------------------------

st.title("Quantum Nexus")

st.subheader(
    "Chemistry Intelligence Engine"
)

smiles = st.text_input(
    "Enter SMILES String"
)





if st.button(
    "Analyze Molecule"
):

    result = predict_smiles(
        smiles
    )

    st.session_state["result"] = result

    
    if "result" in st.session_state:

        result = st.session_state["result"]

        if "error" not in result:

            st.success("Analysis Complete")

            st.metric(
                "Predicted Solubility",
                round(result["prediction"], 3)
            )

            st.subheader("Molecule")
            st.code(result["smiles"])

            descriptor_df = pd.DataFrame(
                [result["descriptors"]]
            )

            st.subheader("Descriptors")

            st.dataframe(
                descriptor_df,
                width = "stretch"
            )

            st.subheader("Model Performance")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "R²",
                    round(metrics["r2"], 3)
                )

            with col2:
                st.metric(
                    "MAE",
                    round(metrics["mae"], 3)
                )

            with col3:
                st.metric(
                    "RMSE",
                    round(metrics["rmse"], 3)
                )

            st.subheader(
                "Top Contributing Features"
            )

            st.dataframe(
                importance_df,
                width = "stretch"
            )

            st.bar_chart(
                importance_df.set_index(
                    "Feature"
                )
            )

# ----------------------------
# PDF REPORT SECTION
# ----------------------------

if "result" in st.session_state:

    result = st.session_state["result"]

    st.subheader(
        "Report Generation"
    )

    if st.button(
        "Generate PDF Report"
    ):

        output_path = (
            "molecule_report.pdf"
        )

        generate_report(
            result,
            metrics,
            output_path
        )

        st.success(
            "PDF generated successfully!"
        )

        with open(
            output_path,
            "rb"
        ) as pdf_file:

            pdf_bytes = pdf_file.read()

        st.download_button(
            label="📄 Download PDF",
            data=pdf_bytes,
            file_name="Quantum_Nexus_Report.pdf",
            mime="application/pdf"
        )