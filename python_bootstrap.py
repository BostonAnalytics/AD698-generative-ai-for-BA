import sys
from pathlib import Path

# Project root = folder containing pyproject.toml
PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Optional: sanity check (comment out later)
print(f"[bootstrap] Project root added to sys.path: {PROJECT_ROOT}")
