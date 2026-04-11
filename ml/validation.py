"""
Input validation and constraint checking for patient data.
"""

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


FEATURE_CONSTRAINTS = {
    "age": {"min": 1, "max": 120, "type": int},
    "sex": {"min": 0, "max": 1, "type": int},
    "cp": {"min": 0, "max": 3, "type": int},
    "trestbps": {"min": 50, "max": 250, "type": int},
    "chol": {"min": 50, "max": 600, "type": int},
    "fbs": {"min": 0, "max": 1, "type": int},
    "restecg": {"min": 0, "max": 2, "type": int},
    "thalach": {"min": 50, "max": 250, "type": int},
    "exang": {"min": 0, "max": 1, "type": int},
    "oldpeak": {"min": 0.0, "max": 10.0, "type": float},
    "slope": {"min": 0, "max": 2, "type": int},
    "ca": {"min": 0, "max": 3, "type": int},
    "thal": {"min": 0, "max": 3, "type": int},
}


def validate_patient_data(user_dict: dict) -> dict:
    """
    Validate patient input data against constraints.
    
    Args:
        user_dict: Dictionary of patient features
        
    Returns:
        Validated dictionary (type-converted)
        
    Raises:
        ValidationError: If any constraint is violated
    """
    validated = {}
    
    for feature, constraints in FEATURE_CONSTRAINTS.items():
        if feature not in user_dict:
            raise ValidationError(f"Missing required feature: {feature}")
        
        value = user_dict[feature]
        
        # Type check
        try:
            value = constraints["type"](value)
        except (ValueError, TypeError):
            raise ValidationError(
                f"Feature '{feature}' must be {constraints['type'].__name__}, "
                f"got {type(value).__name__}: {value}"
            )
        
        # Range check
        min_val = constraints["min"]
        max_val = constraints["max"]
        
        if value < min_val or value > max_val:
            raise ValidationError(
                f"Feature '{feature}' out of range [{min_val}, {max_val}], got {value}"
            )
        
        validated[feature] = value
    
    return validated


def validate_email(email: str) -> None:
    """
    Basic email validation.
    
    Raises:
        ValidationError: If email format is invalid
    """
    if not email or "@" not in email or len(email) < 5:
        raise ValidationError("Invalid email format")


def validate_password(password: str) -> None:
    """
    Password strength validation.
    
    Raises:
        ValidationError: If password is too weak
    """
    if not password or len(password) < 6:
        raise ValidationError("Password must be at least 6 characters")
