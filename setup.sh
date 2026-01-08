#!/usr/bin/env bash
set -e  # Stop on error

echo "=== Creating virtual environment (.venv) ==="
python3 -m venv .venv

echo "=== Activating virtual environment ==="
source .venv/bin/activate

echo "=== Installing dependencies from requirements.txt ==="
pip install -r requirements.txt

echo "=== Installing project in editable mode ==="
pip install -e .

echo "=== Setup complete ==="
echo "To activate the environment manually:"
echo "    source .venv/bin/activate"
