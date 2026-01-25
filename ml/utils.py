import json
from pathlib import Path

def save_json(obj, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def risk_label_from_proba(p: float) -> str:
    if p < 0.35:
        return "Low"
    if p <= 0.65:
        return "Medium"
    return "High"
