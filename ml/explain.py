import numpy as np
import shap

def build_explainer(model, X_background, model_type_hint: str | None = None):
    # Try to auto-detect by available attributes
    # Tree models usually have feature_importances_ or are in ensemble
    is_tree_like = hasattr(model, "feature_importances_") or model.__class__.__name__.lower().find("forest") >= 0

    if is_tree_like:
        return shap.TreeExplainer(model)
    # fallback generic (works for linear/logistic reasonably)
    return shap.Explainer(model, X_background)

def explain_one(explainer, X_row):
    # X_row: 2D array (1, n_features)
    shap_values = explainer(X_row)
    return shap_values

def top_drivers(shap_values, feature_names, top_k=5):
    # shap_values.values shape: (1, n_features)
    vals = shap_values.values[0]
    abs_vals = np.abs(vals)
    idx = np.argsort(abs_vals)[::-1][:top_k]
    drivers = [(feature_names[i], float(vals[i])) for i in idx]
    return drivers
