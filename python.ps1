# Activate virtual environment
if (Test-Path ".\.venv\Scripts\activate.ps1") {
    . .\.venv\Scripts\activate.ps1
} else {
    Write-Host "❌ Virtual environment not found. Run setup.ps1 first."
    exit 1
}

# Forward all arguments to Python inside the venv
& .\.venv\Scripts\python.exe @Args
