import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from ml.utils import save_json

DEFAULT_FEATURES = [
    "age","sex","cp","trestbps","chol","fbs","restecg",
    "thalach","exang","oldpeak","slope","ca","thal"
]

TARGET_COLS = ["target", "num", "output", "HeartDisease", "heart_disease"]

def pick_target_column(df: pd.DataFrame) -> str:
    # 1) direct matches
    for c in TARGET_COLS:
        if c in df.columns:
            return c

    # 2) auto-detect: choose a column that looks like a binary label (0/1)
    binary_candidates = []
    for c in df.columns:
        s = df[c].dropna()
        if len(s) == 0:
            continue
        # try numeric conversion
        try:
            vals = pd.to_numeric(s, errors="coerce").dropna().unique()
        except Exception:
            continue

        if len(vals) > 0 and set(vals).issubset({0, 1}):
            binary_candidates.append(c)

    if len(binary_candidates) == 1:
        return binary_candidates[0]

    # 3) fallback: if last column looks like label
    last = df.columns[-1]
    s = pd.to_numeric(df[last], errors="coerce").dropna().unique()
    if len(s) > 0 and set(s).issubset({0, 1, 2, 3, 4}):
        return last

    raise ValueError(
        f"Target column not found. Columns are: {list(df.columns)}. "
        f"Expected one of {TARGET_COLS} or a binary-looking label column."
    )

def main(csv_path: str, out_dir: str):
    df = pd.read_csv(csv_path)

    target_col = pick_target_column(df)

    # If dataset uses num with values 0..4, convert to binary (>=1 => disease)
    y_raw = df[target_col].copy()
    if y_raw.dropna().nunique() > 2:
        y = (y_raw.astype(float) >= 1).astype(int)
    else:
        y = y_raw.astype(int)

    # Ensure all expected fields exist
    missing = [c for c in DEFAULT_FEATURES if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing columns: {missing}")

    X = df[DEFAULT_FEATURES].copy()

    # Define types (you can tune)
    numeric_features = ["age","trestbps","chol","thalach","oldpeak"]
    categorical_features = [c for c in DEFAULT_FEATURES if c not in numeric_features]

    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocess = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop"
    )

    # Models to try quickly
    models = {
        "LogisticRegression": LogisticRegression(max_iter=2000),
        "RandomForest": RandomForestClassifier(n_estimators=300, random_state=42),
        "SVM_RBF": SVC(probability=True)
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    results = {}
    best_name, best_auc, best_pipe = None, -1, None

    for name, model in models.items():
        pipe = Pipeline(steps=[
            ("preprocess", preprocess),
            ("model", model)
        ])
        pipe.fit(X_train, y_train)
        proba = pipe.predict_proba(X_test)[:, 1]
        pred = (proba >= 0.5).astype(int)

        auc = roc_auc_score(y_test, proba)
        results[name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "precision": float(precision_score(y_test, pred, zero_division=0)),
            "recall": float(recall_score(y_test, pred, zero_division=0)),
            "f1": float(f1_score(y_test, pred, zero_division=0)),
            "roc_auc": float(auc),
            "confusion_matrix": confusion_matrix(y_test, pred).tolist()
        }

        if auc > best_auc:
            best_auc = auc
            best_name = name
            best_pipe = pipe

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Save preprocess + model separately (as you requested)
    # We can extract the fitted parts from the pipeline
    fitted_preprocess = best_pipe.named_steps["preprocess"]
    fitted_model = best_pipe.named_steps["model"]

    joblib.dump(fitted_preprocess, out / "preprocess.pkl")
    joblib.dump(fitted_model, out / "best_model.pkl")

    schema = {
        "features": DEFAULT_FEATURES,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features
    }
    save_json(schema, out / "feature_schema.json")

    metrics_payload = {
        "best_model": best_name,
        "all_models": results
    }
    save_json(metrics_payload, out / "metrics.json")

    print("✅ Training complete")
    print(f"Best model: {best_name} (ROC-AUC={best_auc:.4f})")
    print(f"Saved to: {out.resolve()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to dataset CSV")
    parser.add_argument("--out", default="models", help="Output directory for saved artifacts")
    args = parser.parse_args()

    main(args.csv, args.out)

