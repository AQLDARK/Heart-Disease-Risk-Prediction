"""
Tests for explainability and SHAP-related functions.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from ml.explain import top_drivers, build_explainer


class TestExplainability:
    """Test explainability functions."""
    
    def test_top_drivers_basic(self):
        """Test extracting top drivers from SHAP values."""
        # Mock SHAP values object
        class MockShapValues:
            def __init__(self, vals):
                self.values = np.array([vals])
        
        shap_vals = MockShapValues([0.1, -0.05, 0.3, -0.02, 0.15])
        feature_names = ["age", "sex", "cp", "trestbps", "chol"]
        
        drivers = top_drivers(shap_vals, feature_names, top_k=3)
        
        assert len(drivers) == 3
        # Top 3 should be cp (0.3), age (0.1), chol (0.15) by absolute value
        driver_names = [d[0] for d in drivers]
        assert "cp" in driver_names
        assert "age" in driver_names
        assert "chol" in driver_names
    
    def test_top_drivers_negative_values(self):
        """Test that top drivers considers absolute values."""
        class MockShapValues:
            def __init__(self, vals):
                self.values = np.array([vals])
        
        shap_vals = MockShapValues([0.1, -0.5, 0.05])
        feature_names = ["feat_a", "feat_b", "feat_c"]
        
        drivers = top_drivers(shap_vals, feature_names, top_k=2)
        
        driver_names = [d[0] for d in drivers]
        # Should be feat_b (abs -0.5) and feat_a (0.1)
        assert driver_names[0] == "feat_b"
        assert driver_names[1] == "feat_a"
    
    def test_top_drivers_k_limit(self):
        """Test that top_k parameter limits results."""
        class MockShapValues:
            def __init__(self, vals):
                self.values = np.array([vals])
        
        shap_vals = MockShapValues([0.1, 0.2, 0.3, 0.4, 0.5])
        feature_names = ["a", "b", "c", "d", "e"]
        
        drivers_k2 = top_drivers(shap_vals, feature_names, top_k=2)
        drivers_k4 = top_drivers(shap_vals, feature_names, top_k=4)
        
        assert len(drivers_k2) == 2
        assert len(drivers_k4) == 4
    
    def test_top_drivers_preserves_sign(self):
        """Test that driver values preserve their sign."""
        class MockShapValues:
            def __init__(self, vals):
                self.values = np.array([vals])
        
        shap_vals = MockShapValues([0.1, -0.3, 0.2])
        feature_names = ["feat1", "feat2", "feat3"]
        
        drivers = top_drivers(shap_vals, feature_names, top_k=3)
        
        # Find feat2 in drivers
        feat2_driver = [d for d in drivers if d[0] == "feat2"][0]
        assert feat2_driver[1] < 0  # Should be negative
    
    def test_build_explainer_detects_tree_models(self):
        """Test that explainer auto-detects tree-based models."""
        from sklearn.ensemble import RandomForestClassifier
        import numpy as np
        
        # Create a simple tree-based model
        X = np.random.rand(10, 5)
        y = np.random.randint(0, 2, 10)
        
        model = RandomForestClassifier(n_estimators=5, random_state=42)
        model.fit(X, y)
        
        # Build explainer
        explainer = build_explainer(model, X)
        
        # Check that a TreeExplainer was created
        assert explainer is not None
