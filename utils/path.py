from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()

ROOT_DIR = CURRENT_FILE.parent.parent  
SNAPSHOT_DIR = ROOT_DIR / "data/snapshots"