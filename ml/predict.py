import joblib
import pandas as pd
from pathlib import Path
import logging

from ml.utils import risk_label_from_proba
from ml.validation import validate_patient_data, ValidationError
from ml.config import get_config

logger = logging.getLogger(__name__)
config = get_config()

MODELS_DIR = Path(config.MODELS_DIR)


def _load_artifacts():
    """Load preprocessor and model from disk with error handling."""
    try:
        preprocess = joblib.load(MODELS_DIR / "preprocess.pkl")
        model = joblib.load(MODELS_DIR / "best_model.pkl")
        return preprocess, model
    except FileNotFoundError as e:
        logger.error(f"Model artifacts not found: {e}")
        raise RuntimeError(f"Model files missing: {e}") from e
    except Exception as e:
        logger.error(f"Failed to load model artifacts: {e}")
        raise RuntimeError(f"Failed to load model: {e}") from e


def clean_user_input(user_dict: dict, feature_order: list[str]) -> pd.DataFrame:
    """Ensure correct feature order and handle missing columns."""
    try:
        row = {f: user_dict.get(f, None) for f in feature_order}
        return pd.DataFrame([row])
    except Exception as e:
        logger.error(f"Failed to clean user input: {e}")
        raise RuntimeError(f"Data formatting error: {e}") from e


def predict_risk(user_dict: dict, feature_schema: dict):
    """
    Predict heart disease risk from patient data.
    
    Args:
        user_dict: Dictionary of patient features
        feature_schema: Schema with feature list
        
    Returns:
        Dictionary with proba, label, and cleaned_df
        
    Raises:
        ValidationError: If input data is invalid
        RuntimeError: If prediction fails
    """
    try:
        # Validate input data
        validated_data = validate_patient_data(user_dict)
        logger.info(f"Prediction input validated for features: {list(validated_data.keys())}")
        
        # Load artifacts
        preprocess, model = _load_artifacts()
        
        # Prepare data
        feature_order = feature_schema["features"]
        df = clean_user_input(validated_data, feature_order)
        
        # Transform and predict
        X = preprocess.transform(df)
        proba = float(model.predict_proba(X)[:, 1][0])
        
        # Ensure proba is in valid range
        if not (0.0 <= proba <= 1.0):
            logger.warning(f"Probability out of expected range: {proba}")
            proba = max(0.0, min(1.0, proba))
        
        label = risk_label_from_proba(proba)
        
        logger.info(f"Prediction successful: proba={proba:.3f}, label={label}")
        
        return {
            "proba": proba,
            "label": label,
            "cleaned_df": df
        }
        
    except ValidationError as e:
        logger.warning(f"Input validation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise RuntimeError(f"Prediction error: {e}") from e
