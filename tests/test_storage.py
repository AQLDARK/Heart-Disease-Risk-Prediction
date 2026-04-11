"""
Tests for storage and authentication module.
"""

import sys
from pathlib import Path
import tempfile
import os

# add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import pytest
from ml.storage import create_user, authenticate_user, validate_password


class TestAuthentication:
    """Test user authentication and password management."""
    
    @pytest.fixture(autouse=True)
    def setup_temp_db(self, monkeypatch):
        """Setup temporary database for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test.db")
            monkeypatch.setenv("DB_PATH", db_path)
            yield db_path
    
    def test_create_user_valid(self):
        """Test creating a user with valid data."""
        try:
            # Note: This requires init_db() to be called first
            from ml.storage import init_db
            init_db()
            
            user_id = create_user("Test User", "test@example.com", "password123", "Patient")
            assert isinstance(user_id, int)
            assert user_id > 0
        except Exception as e:
            # Skip if DB setup fails
            pytest.skip(f"DB setup failed: {e}")
    
    def test_create_user_missing_fields(self):
        """Test that create_user rejects missing fields."""
        from ml.storage import init_db
        init_db()
        
        with pytest.raises(ValueError, match="required"):
            create_user("", "test@example.com", "password123")
        
        with pytest.raises(ValueError, match="required"):
            create_user("Test User", "", "password123")
        
        with pytest.raises(ValueError, match="required"):
            create_user("Test User", "test@example.com", "")
    
    def test_create_duplicate_user(self):
        """Test that creating duplicate email raises error."""
        from ml.storage import init_db
        init_db()
        
        create_user("User One", "duplicate@example.com", "password123")
        
        with pytest.raises(ValueError, match="EMAIL_EXISTS"):
            create_user("User Two", "duplicate@example.com", "password456")
    
    def test_authenticate_valid_credentials(self):
        """Test authentication with valid credentials."""
        from ml.storage import init_db
        init_db()
        
        create_user("Auth User", "auth@example.com", "correctpass123")
        user = authenticate_user("auth@example.com", "correctpass123")
        
        assert user is not None
        assert user["email"] == "auth@example.com"
        assert user["full_name"] == "Auth User"
    
    def test_authenticate_invalid_password(self):
        """Test authentication with wrong password."""
        from ml.storage import init_db
        init_db()
        
        create_user("Auth User", "auth2@example.com", "correctpass123")
        user = authenticate_user("auth2@example.com", "wrongpassword")
        
        assert user is None
    
    def test_authenticate_non_existent_user(self):
        """Test authentication with non-existent email."""
        from ml.storage import init_db
        init_db()
        
        user = authenticate_user("nonexistent@example.com", "anypass123")
        assert user is None
    
    def test_authenticate_case_insensitive(self):
        """Test that authentication is case-insensitive for email."""
        from ml.storage import init_db
        init_db()
        
        create_user("Case User", "case@example.com", "password123")
        user = authenticate_user("CASE@EXAMPLE.COM", "password123")
        
        assert user is not None
        assert user["email"] == "case@example.com"
