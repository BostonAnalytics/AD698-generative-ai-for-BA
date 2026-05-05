# project_root.py
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

def add_to_path():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

