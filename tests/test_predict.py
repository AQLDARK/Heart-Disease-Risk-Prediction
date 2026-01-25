import sys
from pathlib import Path

# add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from ml.utils import load_json
from ml.predict import predict_risk

def test_predict_outputs():
    schema = load_json("models/feature_schema.json")

    sample = {
        "age": 50, "sex": 1, "cp": 1, "trestbps": 130, "chol": 250,
        "fbs": 0, "restecg": 0, "thalach": 150, "exang": 0,
        "oldpeak": 1.0, "slope": 1, "ca": 0, "thal": 2
    }

    out = predict_risk(sample, schema)
    assert 0.0 <= out["proba"] <= 1.0
    assert out["label"] in ["Low", "Medium", "High"]