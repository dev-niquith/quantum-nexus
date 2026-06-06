from pathlib import Path
import sys
import json

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT))

from backend.predict import predict_smiles

from backend.molecule_lookup import (
    get_molecule_info,
    get_molecule_from_smiles
)

from backend.molecule_visualizer import (
    generate_molecule_image
)


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

#smiles = st.text_input(
    #"Enter SMILES String"
#)

search_type = st.radio(
    "Search Method",
    [
        "Molecule Name",
        "SMILES"
    ]
)

molecule_name = ""
smiles = ""

if search_type == "Molecule Name":

    molecule_name = st.text_input(
        "Enter Molecule Name"
    )

else:

    smiles = st.text_input(
        "Enter SMILES String"
    )



if st.button("Analyze Molecule"):

    molecule_metadata = None

    if search_type == "Molecule Name":

        molecule_metadata = get_molecule_info(
            molecule_name
        )

        if molecule_metadata is None:

            st.error(
                "Molecule not found."
            )

            st.stop()

        smiles = molecule_metadata[
            "smiles"
        ]

    else:

        molecule_metadata = (
            get_molecule_from_smiles(
                smiles
            )
        )

    result = predict_smiles(
        smiles
    )

    st.session_state[
        "result"
    ] = result

    st.session_state[
        "metadata"
    ] = molecule_metadata



    st.session_state["result"] = result

    
    if "result" in st.session_state:

        result = st.session_state["result"]

        metadata = st.session_state.get(
            "metadata"
        )

        if metadata:

            st.subheader(
                "Molecule Information"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Formula",
                    metadata["formula"]
                )

            with col2:

                st.metric(
                    "Molecular Weight",
                    round(
                        float(
                            metadata[
                                "molecular_weight"
                            ]
                        ),
                        2
                    )
                )

            st.write(
                f"**Name:** "
                f"{metadata['name']}"
            )

            st.code(
                metadata["smiles"]
            )







        if "error" not in result:

            st.success("Analysis Complete")

            
            
            if molecule_metadata:

                st.subheader(
                    "Molecule Information"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Molecular Weight",
                        round(
                            molecule_metadata[
                                "molecular_weight"
                            ],
                            2
                        )
                    )

                with col2:

                    st.metric(
                        "Formula",
                        molecule_metadata[
                            "formula"
                        ]
                    )

                st.write(
                    f"**Name:** "
                    f"{molecule_metadata['name']}"
                )

            image = generate_molecule_image(
                result["smiles"]
            )

            if image:

                st.subheader(
                    "2D Molecular Structure"
                )

                st.image(
                    image,
                    width = "stretch"
                )

            








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


