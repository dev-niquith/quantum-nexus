# Chemistry Intelligence Engine

## Overview

The Chemistry Engine predicts molecular solubility using RDKit descriptors and machine learning models.

---

## Dataset

ESOL Dataset

Target:

Measured Log Solubility

---

## Features

- Molecular Weight
- MolLogP
- TPSA
- H-Bond Donors
- H-Bond Acceptors
- Rotatable Bonds
- Ring Count

---

## Production Model

Random Forest Regressor

Performance:

R² = 0.862

---

## Feature Importance

| Feature | Importance |
|----------|----------|
| MolLogP | 0.816 |
| MolWt | 0.101 |
| TPSA | 0.043 |

---

## Outputs

- Prediction
- Descriptor Table
- Feature Importance
- PDF Report