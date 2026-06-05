from pathlib import Path

import joblib
import pandas as pd

from backend.descriptor_engine import (
    extract_descriptors,
)

ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = ROOT / "models" / "trained"

MODEL_PATH = MODEL_DIR / "rf_esol.pkl"

SCALER_PATH = MODEL_DIR / "scaler.pkl"


model = joblib.load(MODEL_PATH)

scaler = joblib.load(SCALER_PATH)


def predict_smiles(smiles: str):

    descriptors = extract_descriptors(
        smiles
    )

    if descriptors is None:

        return {
            "error":
            "Invalid SMILES string"
        }

    df = pd.DataFrame(
        [descriptors]
    )

    scaled = scaler.transform(df)

    prediction = model.predict(
        scaled
    )[0]

    return {
    "smiles": smiles,
    "prediction": float(prediction),
    "descriptors": descriptors
}


if __name__ == "__main__":

    result = predict_smiles(
        "CCO"
    )

    print(result)