# Contributing

## Environment Setup

```bash
conda activate quantum-nexus
pip install -r requirements.txt


## Run Application

streamlit run frontend/chemistry_app.py

## Train Model

python -m backend.train_model

## Run Tests

pytest



---

## My Final Repository Layout

```text
Quantum-Nexus/

README.md

docs/
├── PROJECT_STATUS.md
├── PRODUCT_REQUIREMENTS.md
├── ARCHITECTURE.md
├── CHEMISTRY_ENGINE.md
├── ROADMAP.md
├── DATASETS.md
└── CONTRIBUTING.md

backend/
frontend/
models/
datasets/
tests/
reports/
notebooks/