import sys
from pathlib import Path

# add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import pytest
from ml.validation import validate_patient_data, validate_email, validate_password, ValidationError


def test_validate_patient_data_valid():
    """Test validation with valid patient data."""
    valid_data = {
        "age": 50, "sex": 1, "cp": 1, "trestbps": 130, "chol": 250,
        "fbs": 0, "restecg": 0, "thalach": 150, "exang": 0,
        "oldpeak": 1.0, "slope": 1, "ca": 0, "thal": 2
    }
    result = validate_patient_data(valid_data)
    assert result["age"] == 50
    assert result["chol"] == 250


def test_validate_patient_data_out_of_range():
    """Test validation catches out-of-range values."""
    invalid_data = {
        "age": 150,  # exceeds max of 120
        "sex": 1, "cp": 1, "trestbps": 130, "chol": 250,
        "fbs": 0, "restecg": 0, "thalach": 150, "exang": 0,
        "oldpeak": 1.0, "slope": 1, "ca": 0, "thal": 2
    }
    with pytest.raises(ValidationError, match="out of range"):
        validate_patient_data(invalid_data)


def test_validate_patient_data_missing_feature():
    """Test validation catches missing required features."""
    incomplete_data = {
        "age": 50, "sex": 1, "cp": 1,
        # missing other required features
    }
    with pytest.raises(ValidationError, match="Missing required feature"):
        validate_patient_data(incomplete_data)


def test_validate_patient_data_wrong_type():
    """Test validation catches type mismatches."""
    invalid_data = {
        "age": "fifty",  # should be int
        "sex": 1, "cp": 1, "trestbps": 130, "chol": 250,
        "fbs": 0, "restecg": 0, "thalach": 150, "exang": 0,
        "oldpeak": 1.0, "slope": 1, "ca": 0, "thal": 2
    }
    with pytest.raises(ValidationError, match="must be"):
        validate_patient_data(invalid_data)


def test_validate_email_valid():
    """Test email validation with valid email."""
    validate_email("test@example.com")  # Should not raise


def test_validate_email_invalid():
    """Test email validation with invalid email."""
    with pytest.raises(ValidationError, match="Invalid email"):
        validate_email("invalid-email")


def test_validate_password_valid():
    """Test password validation with valid password."""
    validate_password("securepass123")  # Should not raise


def test_validate_password_too_short():
    """Test password validation catches short passwords."""
    with pytest.raises(ValidationError, match="at least 6 characters"):
        validate_password("pass")
