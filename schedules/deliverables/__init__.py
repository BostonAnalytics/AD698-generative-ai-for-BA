import json
from pathlib import Path


def load_deliverables(mode: str):
    path = Path(__file__).parent / "deliverables.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[mode]
