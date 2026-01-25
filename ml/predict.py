import joblib
import pandas as pd
from pathlib import Path

from ml.utils import risk_label_from_proba

MODELS_DIR = Path("models")

def _load_artifacts():
    preprocess = joblib.load(MODELS_DIR / "preprocess.pkl")
    model = joblib.load(MODELS_DIR / "best_model.pkl")
    return preprocess, model

def clean_user_input(user_dict: dict, feature_order: list[str]) -> pd.DataFrame:
    # ensures correct order + missing columns set to None
    row = {f: user_dict.get(f, None) for f in feature_order}
    return pd.DataFrame([row])

def predict_risk(user_dict: dict, feature_schema: dict):
    preprocess, model = _load_artifacts()

    feature_order = feature_schema["features"]
    df = clean_user_input(user_dict, feature_order)

    X = preprocess.transform(df)
    proba = float(model.predict_proba(X)[:, 1][0])
    label = risk_label_from_proba(proba)

    return {
        "proba": proba,
        "label": label,
        "cleaned_df": df
    }
