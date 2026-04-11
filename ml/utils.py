import json
from pathlib import Path
import re

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


def group_shap_features(shap_dict: dict) -> dict:
    """
    Groups one-hot/processed feature names back to original features.

    Handles patterns like:
      - "num__age"
      - "cat__cp_2"
      - "cat__thal_3"
      - "remainder__xyz" (ignored or grouped as-is)
    """
    grouped = {}

    for feat, val in shap_dict.items():
        base = feat

        # common sklearn ColumnTransformer naming:
        # "num__age", "cat__cp_2"
        if "__" in feat:
            base = feat.split("__", 1)[1]  # remove "num__" or "cat__"

        # one-hot names often have "_" + category at end: "cp_2"
        # convert "cp_2" -> "cp"
        base = re.sub(r"_(\-?\d+|[A-Za-z]+)$", "", base)

        grouped[base] = grouped.get(base, 0.0) + float(val)

    return grouped
