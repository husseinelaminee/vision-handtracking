Write-Host "=== Creating virtual environment with Python 3.11 (.venv) ==="
py -3.11 -m venv .venv

Write-Host "=== Activating virtual environment ==="
. .\.venv\Scripts\activate.ps1

Write-Host "=== Installing dependencies ==="
python -m pip install -r requirements.txt

Write-Host "=== Installing project in editable mode ==="
python -m pip install -e .

Write-Host "=== Setup complete! ==="
Write-Host "To activate manually:"
Write-Host "    .\.venv\Scripts\activate"
