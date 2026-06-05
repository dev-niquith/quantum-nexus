import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from backend.descriptor_engine import extract_descriptors


ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT / "datasets" / "raw" / "esol.csv"

MODEL_DIR = ROOT / "models" / "trained"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


def build_dataset():

    df = pd.read_csv(DATA_PATH)

    descriptors = []

    for smiles in df["smiles"]:
        descriptors.append(
            extract_descriptors(smiles)
        )

    descriptor_df = pd.DataFrame(descriptors)

    target = df[
        "measured log solubility in mols per litre"
    ]

    return descriptor_df, target


def train():

    X, y = build_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
    )

    model.fit(
        X_train_scaled,
        y_train,
    )

    feature_importance = {
        feature: float(importance)
        for feature, importance in zip(
            X.columns,
            model.feature_importances_
        )
    }


    predictions = model.predict(
        X_test_scaled
    )

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    mse = mean_squared_error(
        y_test,
        predictions,
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions,
    )

    metrics = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "feature_importance": feature_importance
    }

    joblib.dump(
        model,
        MODEL_DIR / "rf_esol.pkl",
    )

    joblib.dump(
        scaler,
        MODEL_DIR / "scaler.pkl",
    )

    with open(
        MODEL_DIR / "metrics.json",
        "w",
    ) as f:
        json.dump(
            metrics,
            f,
            indent=4,
        )

    print("\nTraining Complete\n")

    print(metrics)


if __name__ == "__main__":
    train()








