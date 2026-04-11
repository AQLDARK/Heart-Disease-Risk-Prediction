"""
Configuration management using environment variables.
Supports .env file via python-dotenv.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
env_file = Path(".env")
if env_file.exists():
    load_dotenv(env_file)


class Config:
    """Application configuration."""
    
    # Database
    DB_PATH = os.getenv("DB_PATH", str(Path("data") / "app.db"))
    
    # Logging
    LOG_FILE = os.getenv("LOG_FILE", "heart_disease_app.log")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10 MB
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    
    # Model artifacts
    MODELS_DIR = os.getenv("MODELS_DIR", "models")
    MODEL_FILE = os.getenv("MODEL_FILE", "best_model.pkl")
    PREPROCESS_FILE = os.getenv("PREPROCESS_FILE", "preprocess.pkl")
    FEATURE_SCHEMA_FILE = os.getenv("FEATURE_SCHEMA_FILE", "feature_schema.json")
    SHAP_FILE = os.getenv("SHAP_FILE", "global_shap.json")
    SHAP_GROUPED_FILE = os.getenv("SHAP_GROUPED_FILE", "global_shap_grouped.json")
    METRICS_FILE = os.getenv("METRICS_FILE", "metrics.json")
    
    # App settings
    APP_TITLE = os.getenv("APP_TITLE", "Heart Disease Risk Prediction System")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Bcrypt
    BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))
    
    # Session/Security
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
    
    @classmethod
    def validate(cls):
        """Validate that required configuration values exist."""
        required = [cls.DB_PATH, cls.MODELS_DIR, cls.LOG_FILE]
        for val in required:
            if not val:
                raise ValueError(f"Missing required configuration")
        return True


def get_config() -> Config:
    """Get application configuration."""
    Config.validate()
    return Config
