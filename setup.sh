#!/usr/bin/env bash
# One-shot setup: install dependencies, generate the synthetic corpus, build index.
set -euo pipefail

echo "==> Installing dependencies"
pip install -r requirements.txt

echo "==> Generating synthetic enterprise datasets"
python -m data.generate_data

echo "==> Building the vector index (smoke test)"
python -m src.cli --build

echo "==> Setup complete. Try:"
echo "    python run_demo.py"
echo "    uvicorn src.api.main:app --reload"
