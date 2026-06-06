from pathlib import Path
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
)

from reportlab.platypus import Image

from backend.molecule_visualizer import (
    generate_molecule_image
)

def generate_report(
    result,
    metrics,
    output_path,
):

    doc = SimpleDocTemplate(
        output_path
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Quantum Nexus Scientific Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            f"Generated: {datetime.now()}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            f"SMILES: {result['smiles']}",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Prediction: {result['prediction']:.4f}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Descriptors",
            styles["Heading2"]
        )
    )

    for key, value in result[
        "descriptors"
    ].items():

        elements.append(
            Paragraph(
                f"{key}: {value}",
                styles["Normal"]
            )
        )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Model Metrics",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"R²: {metrics['r2']:.3f}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"MAE: {metrics['mae']:.3f}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"RMSE: {metrics['rmse']:.3f}",
            styles["Normal"]
        )
    )

    molecule_image = generate_molecule_image(
        result["smiles"]
    )

    if molecule_image:

        elements.append(
            Spacer(1, 12)
        )

        elements.append(
            Paragraph(
                "Molecular Structure",
                styles["Heading2"]
            )
        )

        elements.append(
            Image(
                molecule_image,
                width=250,
                height=180
            )
        )


    doc.build(elements)